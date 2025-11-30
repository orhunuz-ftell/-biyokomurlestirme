"""
==============================================================================
ASPEN AUTOMATION - ASPEN INTERFACE MODULE
==============================================================================
Purpose: Handle all Aspen Plus COM operations
Author: Orhun Uzdiyem
Date: 2025-11-16

Functions:
- Connect to Aspen Plus (V8.8)
- Set bio-oil composition (6 components)
- Set process conditions (T, P, S/C)
- Run simulations
- Extract results (H2 properties, syngas, energy)
- Handle convergence issues
==============================================================================
"""

import win32com.client as win32
import time
import config


class AspenInterface:
    """Interface for Aspen Plus COM automation."""

    def __init__(self):
        """Initialize Aspen interface."""
        self.aspen = None
        self.model_loaded = False
        self.last_simulation_time = 0

    def connect(self):
        """Connect to Aspen Plus."""
        print("\n[ASPEN] Connecting to Aspen Plus V8.8...")

        # Try different dispatch options
        for dispatch_str in config.ASPEN_DISPATCH_OPTIONS:
            try:
                print(f"  Trying: {dispatch_str}")
                self.aspen = win32.Dispatch(dispatch_str)
                print(f"  [OK] Connected using: {dispatch_str}")
                return True
            except Exception as e:
                print(f"  [FAILED] {dispatch_str}: {str(e)[:50]}")
                continue

        print("[ERROR] Could not connect to Aspen Plus!")
        print("Possible solutions:")
        print("  1. Ensure Aspen Plus V8.8 is installed")
        print("  2. Run Python as administrator")
        print("  3. Check Aspen license is active")
        return False

    def load_model(self, model_path=None):
        """Load Aspen simulation file."""
        if model_path is None:
            model_path = config.ASPEN_MODEL_PATH

        print(f"\n[ASPEN] Loading model: {model_path}")

        try:
            self.aspen.InitFromArchive2(model_path)
            self.model_loaded = True
            print("  [OK] Model loaded successfully")
            return True
        except Exception as e:
            print(f"  [ERROR] Failed to load model: {e}")
            return False

    def set_biooil_composition(self, composition_dict):
        """
        Set bio-oil composition in RYIELD block.

        Args:
            composition_dict: Dictionary with keys:
                - aromatics
                - acids
                - alcohols
                - furans
                - phenols
                - aldehyde_ketone
                Values should be mass fractions (0-1)
        """
        try:
            # Normalize composition to ensure sum = 1.0
            total = sum(composition_dict.values())
            if abs(total - 1.0) > 0.01:
                # Normalize
                composition_dict = {k: v/total for k, v in composition_dict.items()}

            # Set each component
            for comp_name, path in config.PATHS_BIOOIL_COMP.items():
                value = composition_dict.get(comp_name, 0.0)
                self.aspen.Tree.FindNode(path).Value = value

            return True

        except Exception as e:
            print(f"  [ERROR] Failed to set bio-oil composition: {e}")
            return False

    def set_process_conditions(self, temp_c, pres_bar, sc_ratio, biooil_flow_kgh=100.0):
        """
        Set process operating conditions.

        Args:
            temp_c: Reformer temperature (°C)
            pres_bar: Reformer pressure (bar)
            sc_ratio: Steam-to-carbon ratio
            biooil_flow_kgh: Bio-oil feed rate (kg/h), default 100
        """
        try:
            # Set reformer temperature
            self.aspen.Tree.FindNode(config.PATHS_INPUT['reformer_temp']).Value = temp_c

            # Set reformer pressure
            self.aspen.Tree.FindNode(config.PATHS_INPUT['reformer_pres']).Value = pres_bar

            # Set bio-oil flow
            self.aspen.Tree.FindNode(config.PATHS_INPUT['biooil_flow']).Value = biooil_flow_kgh

            # Calculate and set steam flow based on S/C ratio
            # Assume bio-oil is ~50% carbon by mass
            carbon_mass = biooil_flow_kgh * 0.5  # kg/h
            carbon_moles = carbon_mass / 12.0    # kmol/h
            steam_moles = carbon_moles * sc_ratio  # kmol/h
            steam_mass = steam_moles * 18.0       # kg/h

            self.aspen.Tree.FindNode(config.PATHS_INPUT['steam_flow']).Value = steam_mass

            # Set HTS and LTS temperatures (fixed)
            self.aspen.Tree.FindNode(config.PATHS_INPUT['hts_temp']).Value = 370.0
            self.aspen.Tree.FindNode(config.PATHS_INPUT['lts_temp']).Value = 210.0

            # Set PSA pressure
            self.aspen.Tree.FindNode(config.PATHS_INPUT['psa_pres']).Value = 25.0

            return True

        except Exception as e:
            print(f"  [ERROR] Failed to set process conditions: {e}")
            return False

    def run_simulation(self, timeout=None):
        """
        Run Aspen simulation.

        Args:
            timeout: Maximum time to wait (seconds), default from config

        Returns:
            True if converged, False otherwise
        """
        if timeout is None:
            timeout = config.ASPEN_TIMEOUT

        try:
            start_time = time.time()

            # Run simulation
            self.aspen.Engine.Run2()

            # Wait for completion (with timeout)
            elapsed = 0
            while elapsed < timeout:
                # Check if results are available
                try:
                    status = self.get_convergence_status()
                    if status is not None:
                        break
                except:
                    pass

                time.sleep(1)
                elapsed = time.time() - start_time

            self.last_simulation_time = time.time() - start_time

            # Check final status
            status = self.get_convergence_status()

            if status and "Converged" in str(status):
                return True
            else:
                return False

        except Exception as e:
            print(f"  [ERROR] Simulation run failed: {e}")
            return False

    def get_convergence_status(self):
        """Get simulation convergence status."""
        try:
            status = self.aspen.Tree.FindNode(
                config.PATHS_OUTPUT['convergence_status']
            ).Value
            return status
        except:
            return None

    def extract_h2_properties(self):
        """
        Extract hydrogen product properties.

        Returns:
            Dictionary with H2 product data, or None if failed
        """
        try:
            results = {}

            # Mass and mole flows
            results['H2_Yield_kg'] = self.aspen.Tree.FindNode(
                config.PATHS_OUTPUT['h2_mass_flow']
            ).Value

            results['H2_MoleFlow_kmolh'] = self.aspen.Tree.FindNode(
                config.PATHS_OUTPUT['h2_mole_flow']
            ).Value

            # Temperature and pressure
            results['H2_Temp_C'] = self.aspen.Tree.FindNode(
                config.PATHS_OUTPUT['h2_temp']
            ).Value

            results['H2_Pres_bar'] = self.aspen.Tree.FindNode(
                config.PATHS_OUTPUT['h2_pres']
            ).Value

            # Composition (mole fractions)
            h2_purity = self.aspen.Tree.FindNode(
                config.PATHS_H2_COMPOSITION['H2']
            ).Value
            results['H2_Purity_percent'] = h2_purity * 100.0

            co_frac = self.aspen.Tree.FindNode(
                config.PATHS_H2_COMPOSITION['CO']
            ).Value
            results['CO_Slip_ppm'] = co_frac * 1e6

            co2_frac = self.aspen.Tree.FindNode(
                config.PATHS_H2_COMPOSITION['CO2']
            ).Value

            ch4_frac = self.aspen.Tree.FindNode(
                config.PATHS_H2_COMPOSITION['CH4']
            ).Value
            results['CH4_Slip_percent'] = ch4_frac * 100.0

            # Calculate H2/CO and H2/CO2 ratios
            if co_frac > 0:
                results['H2_CO_Ratio'] = h2_purity / co_frac
            else:
                results['H2_CO_Ratio'] = 9999.0

            if co2_frac > 0:
                results['H2_CO2_Ratio'] = h2_purity / co2_frac
            else:
                results['H2_CO2_Ratio'] = 9999.0

            # Flow rates
            results['H2_FlowRate_kgh'] = results['H2_Yield_kg']

            # Convert to Nm3/h (assuming STP: 1 kmol = 22.4 Nm3)
            results['H2_FlowRate_Nm3h'] = results['H2_MoleFlow_kmolh'] * 22.4

            return results

        except Exception as e:
            print(f"  [ERROR] Failed to extract H2 properties: {e}")
            return None

    def extract_syngas_composition(self, stream_name):
        """
        Extract syngas composition at a specific location.

        Args:
            stream_name: Name of stream (e.g., 'SYNGAS1')

        Returns:
            Dictionary with composition data, or None if failed
        """
        try:
            results = {}

            for comp in config.SYNGAS_COMPONENTS:
                path = f"\\Data\\Streams\\{stream_name}\\Output\\MOLEFRAC\\MIXED\\{comp}"
                mole_frac = self.aspen.Tree.FindNode(path).Value
                results[f"{comp}_molpercent"] = mole_frac * 100.0

            # Temperature
            temp_path = f"\\Data\\Streams\\{stream_name}\\Output\\TEMP_OUT\\MIXED"
            results['Temperature_C'] = self.aspen.Tree.FindNode(temp_path).Value

            # Pressure
            pres_path = f"\\Data\\Streams\\{stream_name}\\Output\\PRES_OUT\\MIXED"
            results['Pressure_bar'] = self.aspen.Tree.FindNode(pres_path).Value

            # Mass flow
            mass_path = f"\\Data\\Streams\\{stream_name}\\Output\\MASSFLMX\\MIXED"
            results['MassFlowRate_kgh'] = self.aspen.Tree.FindNode(mass_path).Value

            # Molar flow
            mole_path = f"\\Data\\Streams\\{stream_name}\\Output\\MOLEFLMX\\MIXED"
            results['MolarFlowRate_kmolh'] = self.aspen.Tree.FindNode(mole_path).Value

            return results

        except Exception as e:
            print(f"  [ERROR] Failed to extract syngas composition for {stream_name}: {e}")
            return None

    def extract_energy_data(self):
        """
        Extract energy balance data.

        Returns:
            Dictionary with energy data, or None if failed
        """
        try:
            results = {}

            # Reformer duty (MJ/h)
            results['ReformerHeat_MJ'] = self.aspen.Tree.FindNode(
                config.PATHS_OUTPUT['reformer_duty']
            ).Value

            # Preheater duty (MJ/h)
            results['PreheaterHeat_MJ'] = self.aspen.Tree.FindNode(
                config.PATHS_OUTPUT['preheat_duty']
            ).Value

            # Total energy input
            results['TotalEnergyInput_MJ'] = (
                results['ReformerHeat_MJ'] + results['PreheaterHeat_MJ']
            )

            return results

        except Exception as e:
            print(f"  [ERROR] Failed to extract energy data: {e}")
            return None

    def calculate_carbon_conversion(self, biooil_comp):
        """
        Calculate carbon conversion efficiency.

        Args:
            biooil_comp: Bio-oil composition dictionary

        Returns:
            Carbon conversion percentage, or None if failed
        """
        try:
            # Calculate carbon input (approximate)
            # Assume average C content for each component
            carbon_contents = {
                'aromatics': 0.913,     # Toluene: C7H8
                'acids': 0.400,         # Acetic acid: C2H4O2
                'alcohols': 0.522,      # Ethanol: C2H6O
                'furans': 0.706,        # Furan: C4H4O
                'phenols': 0.766,       # Phenol: C6H6O
                'aldehyde_ketone': 0.621  # Acetone: C3H6O
            }

            # Calculate total carbon in bio-oil (kg C / kg bio-oil)
            total_carbon = sum(
                biooil_comp.get(comp, 0) * carbon_contents.get(comp, 0.5)
                for comp in biooil_comp.keys()
            )

            # Get H2 and CO2 production (simplified calculation)
            # In reality, need to check all carbon-containing streams
            # For now, assume most carbon goes to H2 production or CO2

            return 90.0  # Placeholder, needs proper calculation from streams

        except Exception as e:
            print(f"  [ERROR] Failed to calculate carbon conversion: {e}")
            return None

    def get_simulation_time(self):
        """Get last simulation run time."""
        return self.last_simulation_time

    def close(self):
        """Close Aspen Plus."""
        if self.aspen is not None:
            try:
                self.aspen.Close()
                print("\n[ASPEN] Closed successfully")
            except:
                pass
        self.aspen = None
        self.model_loaded = False


# ==============================================================================
# TEST FUNCTIONS
# ==============================================================================

def test_connection():
    """Test Aspen connection."""
    print("="*70)
    print("TESTING ASPEN CONNECTION")
    print("="*70)

    aspen_interface = AspenInterface()

    # Test connection
    if not aspen_interface.connect():
        return False

    # Test model loading
    if not aspen_interface.load_model():
        return False

    print("\n[OK] Aspen connection test passed!")
    aspen_interface.close()
    return True


def test_single_simulation():
    """Test a single simulation run."""
    print("="*70)
    print("TESTING SINGLE SIMULATION")
    print("="*70)

    aspen_interface = AspenInterface()

    # Connect and load
    if not aspen_interface.connect():
        return False
    if not aspen_interface.load_model():
        return False

    # Set test composition
    test_comp = {
        'aromatics': 0.3287,
        'acids': 0.1964,
        'alcohols': 0.0630,
        'furans': 0.0274,
        'phenols': 0.0963,
        'aldehyde_ketone': 0.0653
    }

    print("\nSetting bio-oil composition...")
    aspen_interface.set_biooil_composition(test_comp)

    print("Setting process conditions (800°C, 15 bar, S/C=3.5)...")
    aspen_interface.set_process_conditions(
        temp_c=800.0,
        pres_bar=15.0,
        sc_ratio=3.5
    )

    print("Running simulation...")
    converged = aspen_interface.run_simulation()

    if converged:
        print(f"  [OK] Converged in {aspen_interface.get_simulation_time():.1f} seconds")

        # Extract results
        h2_data = aspen_interface.extract_h2_properties()
        if h2_data:
            print("\nH2 Product Properties:")
            print(f"  Yield: {h2_data['H2_Yield_kg']:.2f} kg/h")
            print(f"  Purity: {h2_data['H2_Purity_percent']:.2f}%")
            print(f"  CO: {h2_data['CO_Slip_ppm']:.1f} ppm")

        syngas_data = aspen_interface.extract_syngas_composition('SYNGAS1')
        if syngas_data:
            print("\nSyngas Composition (Reformer Out):")
            print(f"  H2: {syngas_data['H2_molpercent']:.2f}%")
            print(f"  CO: {syngas_data['CO_molpercent']:.2f}%")
            print(f"  CO2: {syngas_data['CO2_molpercent']:.2f}%")

        print("\n[OK] Single simulation test passed!")
    else:
        print("  [ERROR] Simulation did not converge")

    aspen_interface.close()
    return converged


if __name__ == "__main__":
    # Run tests
    print("\nTest 1: Connection")
    test_connection()

    print("\n\nTest 2: Single Simulation")
    test_single_simulation()
