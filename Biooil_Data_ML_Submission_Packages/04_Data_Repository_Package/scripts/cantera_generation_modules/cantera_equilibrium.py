"""
Cantera Equilibrium Calculator

This module handles:
- Gibbs free energy minimization for reformer
- Water-gas shift reactions (HTS and LTS)
- Equilibrium composition calculations
"""

import cantera as ct
import sys
import os
from typing import Dict, Tuple

# Add parent directory to path for config import
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import cantera_config as config


class EquilibriumCalculator:
    """Calculate chemical equilibrium using Cantera"""

    def __init__(self):
        """Initialize equilibrium calculator"""
        self.gas = None
        self.load_mechanism()

    def load_mechanism(self):
        """
        Load chemical mechanism (GRI-Mech 3.0)

        GRI-Mech 3.0 includes:
        - 53 species (H2, CO, CO2, CH4, H2O, C2H4, etc.)
        - 325 reactions
        - Thermodynamic data for bio-oil surrogate species
        """
        try:
            # Try primary mechanism
            self.gas = ct.Solution(config.MECHANISM)
            if config.VERBOSE:
                print(f"[OK] Loaded mechanism: {config.MECHANISM}")
                print(f"    Species: {self.gas.n_species}")
                print(f"    Reactions: {self.gas.n_reactions}")

        except Exception as e:
            # Try backup mechanisms
            for backup in config.BACKUP_MECHANISMS:
                try:
                    self.gas = ct.Solution(backup)
                    if config.VERBOSE:
                        print(f"[OK] Loaded backup mechanism: {backup}")
                    return
                except:
                    continue

            raise RuntimeError(f"Could not load any mechanism: {e}")

    def reformer_equilibrium(self, composition: Dict[str, float],
                           temperature_K: float,
                           pressure_Pa: float) -> Dict:
        """
        Calculate reformer equilibrium using Gibbs minimization

        Args:
            composition: Mole fractions of bio-oil + steam
            temperature_K: Reformer temperature (K)
            pressure_Pa: Reformer pressure (Pa)

        Returns:
            dict: Equilibrium composition and properties

        Process:
            Bio-oil + H2O → H2 + CO + CO2 + CH4 + ... (at equilibrium)
        """
        try:
            # Set initial state
            self.gas.TPX = temperature_K, pressure_Pa, composition

            # Perform Gibbs minimization
            self.gas.equilibrate('TP')  # Constant T, P

            # Extract results
            results = {
                'temperature_K': self.gas.T,
                'pressure_Pa': self.gas.P,
                'mole_fractions': {},
                'mass_fractions': {},
                'molar_concentrations': {},  # mol/m³
                'mean_molecular_weight': self.gas.mean_molecular_weight,
                'density_kg_m3': self.gas.density,
                'enthalpy_J_kg': self.gas.enthalpy_mass,
                'entropy_J_kgK': self.gas.entropy_mass
            }

            # Get composition
            for i, species_name in enumerate(self.gas.species_names):
                mole_frac = self.gas.X[i]
                if mole_frac > 1e-10:  # Only non-negligible species
                    results['mole_fractions'][species_name] = mole_frac
                    results['mass_fractions'][species_name] = self.gas.Y[i]
                    results['molar_concentrations'][species_name] = self.gas[species_name].concentrations[0]

            return results

        except Exception as e:
            print(f"[ERROR] Reformer equilibrium failed: {e}")
            raise

    def wgs_equilibrium(self, inlet_composition: Dict[str, float],
                       temperature_K: float,
                       pressure_Pa: float) -> Dict:
        """
        Calculate water-gas shift equilibrium

        Args:
            inlet_composition: Inlet mole fractions
            temperature_K: WGS temperature (K)
            pressure_Pa: WGS pressure (Pa)

        Returns:
            dict: Equilibrium composition after WGS

        Reaction:
            CO + H2O ⇌ CO2 + H2

        At HTS (370°C): Forward reaction favored
        At LTS (210°C): Further shift to products
        """
        try:
            # Set inlet state
            self.gas.TPX = temperature_K, pressure_Pa, inlet_composition

            # Equilibrate at WGS conditions
            self.gas.equilibrate('TP')

            # Extract results (same format as reformer)
            results = {
                'temperature_K': self.gas.T,
                'pressure_Pa': self.gas.P,
                'mole_fractions': {},
                'mass_fractions': {},
                'mean_molecular_weight': self.gas.mean_molecular_weight,
                'density_kg_m3': self.gas.density,
                'enthalpy_J_kg': self.gas.enthalpy_mass,
                'entropy_J_kgK': self.gas.entropy_mass
            }

            # Get composition
            for i, species_name in enumerate(self.gas.species_names):
                mole_frac = self.gas.X[i]
                if mole_frac > 1e-10:
                    results['mole_fractions'][species_name] = mole_frac
                    results['mass_fractions'][species_name] = self.gas.Y[i]

            return results

        except Exception as e:
            print(f"[ERROR] WGS equilibrium failed: {e}")
            raise

    def get_species_flowrate(self, composition: Dict[str, float],
                            total_flow_mol_s: float,
                            species: str) -> float:
        """
        Calculate species molar flowrate

        Args:
            composition: Mole fractions
            total_flow_mol_s: Total molar flow (mol/s)
            species: Species name

        Returns:
            float: Species molar flowrate (mol/s)
        """
        return composition.get(species, 0.0) * total_flow_mol_s

    def calculate_conversion(self, inlet_composition: Dict[str, float],
                           outlet_composition: Dict[str, float],
                           species: str) -> float:
        """
        Calculate species conversion

        Args:
            inlet_composition: Inlet mole fractions
            outlet_composition: Outlet mole fractions
            species: Species name

        Returns:
            float: Conversion (0-1)

        Formula:
            Conversion = (inlet - outlet) / inlet
        """
        inlet_frac = inlet_composition.get(species, 0.0)
        outlet_frac = outlet_composition.get(species, 0.0)

        if inlet_frac < 1e-10:
            return 0.0

        conversion = (inlet_frac - outlet_frac) / inlet_frac
        return max(0.0, min(1.0, conversion))  # Clamp to [0, 1]


# ==============================================================================
# TESTING AND VALIDATION
# ==============================================================================

def test_equilibrium_calculator():
    """Test the equilibrium calculator with simple reforming case"""
    print("\n" + "="*80)
    print("TESTING EQUILIBRIUM CALCULATOR")
    print("="*80)

    calc = EquilibriumCalculator()

    # Test case: Ethanol steam reforming
    # C2H5OH + 3H2O → 6H2 + 2CO2 (theoretical)
    print("\nTest Case: Ethanol Steam Reforming")

    # Input composition (ethanol + steam, S/C = 3)
    composition = {
        'C2H5OH': 0.25,  # 25% ethanol
        'H2O': 0.75      # 75% steam (S/C = 3)
    }

    # Reformer conditions
    T_reformer = 800 + 273.15  # 800°C
    P_reformer = 15e5          # 15 bar

    print(f"\nInput:")
    print(f"    Temperature: 800 °C")
    print(f"    Pressure: 15 bar")
    print(f"    Composition: C2H5OH = 25%, H2O = 75%")

    # Test 1: Reformer equilibrium
    print("\nTest 1: Reformer Equilibrium")
    try:
        reformer_out = calc.reformer_equilibrium(composition, T_reformer, P_reformer)
        print("[PASS] Reformer equilibrium calculated")

        print(f"\nReformer Output (major species):")
        major_species = {k: v for k, v in reformer_out['mole_fractions'].items()
                        if v > 0.01}  # Show species > 1%
        for species, mole_frac in sorted(major_species.items(),
                                        key=lambda x: x[1], reverse=True):
            print(f"    {species:8s}: {mole_frac:7.4f} ({mole_frac*100:5.2f}%)")

    except Exception as e:
        print(f"[FAIL] Reformer equilibrium: {e}")
        return

    # Test 2: HTS equilibrium
    print("\nTest 2: High-Temperature Shift (HTS)")
    T_hts = config.HTS_TEMPERATURE_C + 273.15
    P_hts = P_reformer

    try:
        hts_out = calc.wgs_equilibrium(reformer_out['mole_fractions'], T_hts, P_hts)
        print(f"[PASS] HTS equilibrium calculated at {config.HTS_TEMPERATURE_C}°C")

        # Compare CO conversion
        co_conversion = calc.calculate_conversion(
            reformer_out['mole_fractions'],
            hts_out['mole_fractions'],
            'CO'
        )
        print(f"    CO conversion: {co_conversion*100:.2f}%")

        print(f"\nHTS Output (major species):")
        major_species = {k: v for k, v in hts_out['mole_fractions'].items()
                        if v > 0.01}
        for species, mole_frac in sorted(major_species.items(),
                                        key=lambda x: x[1], reverse=True):
            print(f"    {species:8s}: {mole_frac:7.4f} ({mole_frac*100:5.2f}%)")

    except Exception as e:
        print(f"[FAIL] HTS equilibrium: {e}")
        return

    # Test 3: LTS equilibrium
    print("\nTest 3: Low-Temperature Shift (LTS)")
    T_lts = config.LTS_TEMPERATURE_C + 273.15
    P_lts = P_reformer

    try:
        lts_out = calc.wgs_equilibrium(hts_out['mole_fractions'], T_lts, P_lts)
        print(f"[PASS] LTS equilibrium calculated at {config.LTS_TEMPERATURE_C}°C")

        # Compare CO conversion
        co_conversion = calc.calculate_conversion(
            hts_out['mole_fractions'],
            lts_out['mole_fractions'],
            'CO'
        )
        print(f"    CO conversion: {co_conversion*100:.2f}%")

        print(f"\nLTS Output (major species):")
        major_species = {k: v for k, v in lts_out['mole_fractions'].items()
                        if v > 0.01}
        for species, mole_frac in sorted(major_species.items(),
                                        key=lambda x: x[1], reverse=True):
            print(f"    {species:8s}: {mole_frac:7.4f} ({mole_frac*100:5.2f}%)")

        # Check H2 enrichment
        h2_initial = reformer_out['mole_fractions'].get('H2', 0.0)
        h2_final = lts_out['mole_fractions'].get('H2', 0.0)
        print(f"\nH2 Enrichment:")
        print(f"    Reformer: {h2_initial*100:.2f}%")
        print(f"    After LTS: {h2_final*100:.2f}%")
        print(f"    Increase: {(h2_final - h2_initial)*100:.2f} percentage points")

    except Exception as e:
        print(f"[FAIL] LTS equilibrium: {e}")
        return

    print("\n" + "="*80)
    print("EQUILIBRIUM CALCULATOR TEST COMPLETE")
    print("="*80)


if __name__ == "__main__":
    test_equilibrium_calculator()
