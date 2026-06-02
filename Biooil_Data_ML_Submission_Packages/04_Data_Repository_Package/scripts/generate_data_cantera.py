"""
Cantera Data Generation System - Main Controller

This script orchestrates the complete data generation workflow:
1. Load simulation matrix (1,170 scenarios)
2. Run Cantera equilibrium calculations
3. Apply separation models
4. Calculate properties and ML features
5. Validate results
6. Write to SQL Server database

Author: Orhun Uzdiyem
Version: 1.0.0
"""

import sys
import os
import time
from datetime import datetime
from typing import Dict, List

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

# Import all modules
from config import cantera_config as config
from modules.cantera_input_processor import InputProcessor
from modules.cantera_equilibrium import EquilibriumCalculator
from modules.separation_models import SeparationModels
from modules.property_calculator import PropertyCalculator
from modules.database_writer import DatabaseWriter
from modules.validation import ValidationEngine


class CanteraDataGenerator:
    """Main controller for Cantera-based data generation"""

    def __init__(self):
        """Initialize all components"""
        print("\n" + "="*80)
        print("CANTERA DATA GENERATION SYSTEM")
        print("="*80)
        print(f"Version: 1.0.0")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Database: {config.DB_SERVER} / {config.DB_DATABASE}")
        print("="*80 + "\n")

        # Initialize modules
        print("Initializing modules...")
        self.input_processor = InputProcessor()
        self.equilibrium_calc = EquilibriumCalculator()
        self.separation_models = SeparationModels()
        self.property_calc = PropertyCalculator()
        self.database_writer = DatabaseWriter()
        self.validator = ValidationEngine()

        # Statistics
        self.stats = {
            'total': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'validation_failed': 0
        }

        print("[OK] All modules initialized\n")

    def run_single_simulation(self, cantera_input: Dict) -> Dict:
        """
        Run complete simulation for one scenario

        Args:
            cantera_input: Input dictionary from InputProcessor

        Returns:
            dict: Complete simulation results
        """
        try:
            # Extract process conditions
            biooil_id = cantera_input['BiooilId']
            temperature_K = cantera_input['temperature_K']
            pressure_Pa = cantera_input['pressure_Pa']
            composition = cantera_input['composition']
            sc_ratio = cantera_input['SC_ratio']

            # Stage 1: Reformer equilibrium
            reformer_out = self.equilibrium_calc.reformer_equilibrium(
                composition, temperature_K, pressure_Pa
            )

            # Stage 2: High-Temperature Shift (HTS)
            hts_temp_K = config.HTS_TEMPERATURE_C + 273.15
            hts_out = self.equilibrium_calc.wgs_equilibrium(
                reformer_out['mole_fractions'], hts_temp_K, pressure_Pa
            )

            # Stage 3: Low-Temperature Shift (LTS)
            lts_temp_K = config.LTS_TEMPERATURE_C + 273.15
            lts_out = self.equilibrium_calc.wgs_equilibrium(
                hts_out['mole_fractions'], lts_temp_K, pressure_Pa
            )

            # Stage 4: Flash separation (water removal)
            flash_vapor, flash_liquid = self.separation_models.flash_separation(
                lts_out['mole_fractions']
            )

            # Stage 5: CO2 removal
            co2_treated, co2_stream = self.separation_models.co2_removal(
                flash_vapor
            )

            # Stage 6: PSA (H2 purification)
            h2_product, tail_gas = self.separation_models.psa_separation(
                co2_treated
            )

            # Calculate carbon content for property calculations
            carbon_in_biooil = self.input_processor.calculate_carbon_content(
                self.input_processor.prepare_bio_oil_composition(
                    {'aromatics': cantera_input['composition'].get('C7H8', 0)*92.14,
                     'acids': cantera_input['composition'].get('CH3COOH', 0)*60.05,
                     'alcohols': cantera_input['composition'].get('C2H5OH', 0)*46.07,
                     'furans': cantera_input['composition'].get('C4H4O', 0)*68.07,
                     'phenols': cantera_input['composition'].get('C6H6O', 0)*94.11,
                     'aldehyde_ketone': cantera_input['composition'].get('C3H6O', 0)*58.08}
                )
            )

            # Simplified carbon in gas (sum of C-containing species)
            carbon_in_gas = (
                lts_out['mole_fractions'].get('CO', 0.0) +
                lts_out['mole_fractions'].get('CO2', 0.0) +
                lts_out['mole_fractions'].get('CH4', 0.0)
            )

            # Approximate H2 moles (simplified basis: 100 kg bio-oil)
            # This is a simplified calculation for demonstration
            h2_moles = h2_product.get('H2', 0.0) * 1000.0

            # Assemble simulation data
            simulation_data = {
                'BiooilId': biooil_id,
                'Temperature_C': cantera_input['Temperature_C'],
                'Pressure_bar': cantera_input['Pressure_bar'],
                'SC_ratio': sc_ratio,
                'converged': True,
                'reformer': reformer_out,
                'hts': hts_out,
                'lts': lts_out,
                'flash_vapor': {
                    'mole_fractions': flash_vapor,
                    'temperature_K': config.FLASH_TEMPERATURE_C + 273.15,
                    'pressure_Pa': 1.01e5
                },
                'flash_liquid': flash_liquid,
                'co2_treated': {
                    'mole_fractions': co2_treated,
                    'temperature_K': config.FLASH_TEMPERATURE_C + 273.15,
                    'pressure_Pa': 1.01e5
                },
                'co2_stream': co2_stream,
                'h2_product': h2_product,
                'tail_gas': tail_gas,
                'h2_moles_total': h2_moles,
                'carbon_in_biooil': carbon_in_biooil,
                'carbon_in_gas': carbon_in_gas,
                'process_conditions': cantera_input
            }

            # Calculate ML features
            ml_features = self.property_calc.calculate_ml_features(simulation_data)
            simulation_data['ml_features'] = ml_features

            # Calculate energy balance (simplified)
            h2_yield_kg = ml_features['H2_Yield']
            energy_balance = {
                'feed_enthalpy': config.HHV['biooil'] * 100.0,  # MJ for 100 kg bio-oil
                'product_enthalpy': config.HHV['H2'] * h2_yield_kg,
                'heat_input_reformer': 500.0,  # Simplified
                'heat_output_hts': 50.0,
                'heat_output_lts': 30.0,
                'heat_output_flash': 20.0,
                'net_heat_duty': 400.0,
                'cold_gas_efficiency': ml_features['EnergyEfficiency'],
                'thermal_efficiency': ml_features['EnergyEfficiency'] * 1.08,
                'exergy_efficiency': ml_features['EnergyEfficiency'] * 0.92,
                'co2_emissions': lts_out['mole_fractions'].get('CO2', 0.0) * 44.01,
                'energy_per_kg_h2': (config.HHV['biooil'] * 100.0) / h2_yield_kg if h2_yield_kg > 0 else 0
            }
            simulation_data['energy_balance'] = energy_balance

            return simulation_data

        except Exception as e:
            print(f"[ERROR] Simulation failed: {e}")
            raise

    def process_all_simulations(self, start_index: int = 0, max_simulations: int = None):
        """
        Process all simulation scenarios

        Args:
            start_index: Starting index (for resume capability)
            max_simulations: Maximum number to process (None = all)
        """
        # Connect to database
        if not self.database_writer.connect():
            print("[ERROR] Cannot connect to database. Aborting.")
            return

        # Load simulation matrix
        print("Loading simulation matrix from database...")
        self.input_processor.load_simulation_matrix()
        cantera_inputs = self.input_processor.process_all_scenarios()

        total_scenarios = len(cantera_inputs)
        if max_simulations:
            total_scenarios = min(total_scenarios, max_simulations)

        print(f"\nTotal scenarios to process: {total_scenarios}")
        print(f"Starting from index: {start_index}\n")

        self.stats['total'] = total_scenarios

        # Check existing progress
        existing_count = self.database_writer.get_completion_count()
        print(f"Existing Cantera simulations in database: {existing_count}\n")

        start_time = time.time()

        # Main processing loop
        for idx in range(start_index, total_scenarios):
            cantera_input = cantera_inputs[idx]

            # Progress header
            if idx % config.PROGRESS_UPDATE_FREQ == 0 or idx == 0:
                print(f"\n{'-'*80}")
                print(f"Progress: {idx}/{total_scenarios} ({idx/total_scenarios*100:.1f}%)")
                print(f"Successful: {self.stats['successful']}, "
                      f"Failed: {self.stats['failed']}, "
                      f"Skipped: {self.stats['skipped']}")
                print(f"{'-'*80}")

            try:
                # Run simulation
                if config.VERBOSE and idx % config.PROGRESS_UPDATE_FREQ == 0:
                    print(f"\n[{idx}] Bio-oil {cantera_input['BiooilId']}, "
                          f"T={cantera_input['Temperature_C']}°C, "
                          f"P={cantera_input['Pressure_bar']}bar, "
                          f"S/C={cantera_input['SC_ratio']}")

                simulation_data = self.run_single_simulation(cantera_input)

                # Validate
                validation_report = self.validator.validate_complete_simulation(simulation_data)

                if not validation_report['overall_valid']:
                    print(f"[WARNING] Simulation {idx} failed validation")
                    if config.VERBOSE:
                        self.validator.print_validation_report(validation_report, f"Sim_{idx}")
                    self.stats['validation_failed'] += 1
                    # Still write to database but mark for review
                    simulation_data['converged'] = False

                # Write to database
                success = self.database_writer.write_complete_simulation(simulation_data)

                if success:
                    self.stats['successful'] += 1
                else:
                    self.stats['failed'] += 1

            except KeyboardInterrupt:
                print("\n\n[INTERRUPTED] User interrupted. Saving progress...")
                self.print_final_report(time.time() - start_time, interrupted=True, last_index=idx)
                break

            except Exception as e:
                print(f"[ERROR] Simulation {idx} failed: {e}")
                self.stats['failed'] += 1
                continue

        # Final report
        if idx >= total_scenarios - 1:
            self.print_final_report(time.time() - start_time)

    def print_final_report(self, elapsed_time: float, interrupted: bool = False, last_index: int = None):
        """
        Print final summary report

        Args:
            elapsed_time: Total elapsed time (seconds)
            interrupted: Whether run was interrupted
            last_index: Last processed index if interrupted
        """
        print("\n" + "="*80)
        if interrupted:
            print("INTERRUPTED - PARTIAL RESULTS")
        else:
            print("FINAL REPORT")
        print("="*80)

        print(f"\nTotal scenarios: {self.stats['total']}")
        print(f"Successful: {self.stats['successful']}")
        print(f"Failed: {self.stats['failed']}")
        print(f"Skipped: {self.stats['skipped']}")
        print(f"Validation warnings: {self.stats['validation_failed']}")

        if interrupted and last_index is not None:
            print(f"\nLast processed index: {last_index}")
            print(f"To resume, run with start_index={last_index + 1}")

        # Performance metrics
        print(f"\nElapsed time: {elapsed_time:.1f} seconds ({elapsed_time/60:.1f} minutes)")
        if self.stats['successful'] > 0:
            print(f"Average time per simulation: {elapsed_time/self.stats['successful']:.2f} seconds")

        # Success rate
        if self.stats['total'] > 0:
            success_rate = (self.stats['successful'] / self.stats['total']) * 100
            print(f"Success rate: {success_rate:.1f}%")

        print("\n" + "="*80)

        # Database summary
        final_count = self.database_writer.get_completion_count()
        print(f"\nTotal Cantera simulations in database: {final_count}")
        print(f"Target: 1,170")
        if final_count >= 1170:
            print("[SUCCESS] All simulations complete!")
        else:
            print(f"Remaining: {1170 - final_count}")

        print("="*80 + "\n")

    def close(self):
        """Clean up resources"""
        self.input_processor.close()
        self.database_writer.close()


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate hydrogen production data using Cantera"
    )
    parser.add_argument(
        '--start',
        type=int,
        default=0,
        help='Starting index (for resume capability)'
    )
    parser.add_argument(
        '--max',
        type=int,
        default=None,
        help='Maximum number of simulations to run (default: all)'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run test mode (first 10 simulations only)'
    )

    args = parser.parse_args()

    # Create generator
    generator = CanteraDataGenerator()

    try:
        if args.test:
            print("[TEST MODE] Running first 10 simulations only\n")
            generator.process_all_simulations(start_index=0, max_simulations=10)
        else:
            generator.process_all_simulations(
                start_index=args.start,
                max_simulations=args.max
            )

    except Exception as e:
        print(f"\n[FATAL ERROR] {e}")
        import traceback
        traceback.print_exc()

    finally:
        generator.close()


if __name__ == "__main__":
    main()
