"""
Separation Models for Hydrogen Purification

This module handles:
- Flash separation (water removal)
- CO2 removal (chemical absorption)
- PSA (Pressure Swing Adsorption) for H2 purification
"""

import sys
import os
from typing import Dict, Tuple

# Add parent directory to path for config import
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import cantera_config as config


class SeparationModels:
    """Model downstream separation processes"""

    def __init__(self):
        """Initialize separation models"""
        pass

    def flash_separation(self, inlet_composition: Dict[str, float],
                        temperature_C: float = None,
                        pressure_bar: float = None) -> Tuple[Dict, Dict]:
        """
        Flash separation to remove water

        Args:
            inlet_composition: Inlet mole fractions
            temperature_C: Flash temperature (default from config)
            pressure_bar: Flash pressure (default atmospheric)

        Returns:
            tuple: (vapor_composition, liquid_composition)

        Assumptions:
            - Perfect separation of water (all water to liquid)
            - All other species to vapor
            - Simple model for hydrogen production focus
        """
        if temperature_C is None:
            temperature_C = config.FLASH_TEMPERATURE_C
        if pressure_bar is None:
            pressure_bar = 1.013  # Atmospheric

        # Vapor phase: all non-water species
        vapor_moles = {}
        liquid_moles = {}

        for species, mole_frac in inlet_composition.items():
            if species == 'H2O':
                # Most water to liquid (99.9% removal)
                liquid_moles['H2O'] = mole_frac * 0.999
                vapor_moles['H2O'] = mole_frac * 0.001
            else:
                # All other species to vapor
                vapor_moles[species] = mole_frac

        # Normalize
        total_vapor = sum(vapor_moles.values())
        total_liquid = sum(liquid_moles.values())

        vapor_composition = {sp: mole / total_vapor
                           for sp, mole in vapor_moles.items()}
        liquid_composition = {sp: mole / total_liquid
                            for sp, mole in liquid_moles.items()}

        return vapor_composition, liquid_composition

    def co2_removal(self, inlet_composition: Dict[str, float],
                   removal_efficiency: float = None) -> Tuple[Dict, Dict]:
        """
        CO2 removal by chemical absorption (e.g., amine scrubbing)

        Args:
            inlet_composition: Inlet mole fractions
            removal_efficiency: CO2 removal efficiency (default from config)

        Returns:
            tuple: (treated_gas, co2_stream)

        Process:
            - Removes specified % of CO2
            - Small losses of H2, CO, CH4 with CO2 stream
        """
        if removal_efficiency is None:
            removal_efficiency = config.CO2_REMOVAL_EFFICIENCY

        treated_moles = {}
        co2_stream_moles = {}

        for species, mole_frac in inlet_composition.items():
            if species == 'CO2':
                # Remove specified efficiency
                co2_stream_moles['CO2'] = mole_frac * removal_efficiency
                treated_moles['CO2'] = mole_frac * (1 - removal_efficiency)

            elif species in config.CO2_REMOVAL_LOSSES:
                # Component losses with CO2
                loss_fraction = config.CO2_REMOVAL_LOSSES[species]
                co2_stream_moles[species] = mole_frac * loss_fraction
                treated_moles[species] = mole_frac * (1 - loss_fraction)

            else:
                # No loss
                treated_moles[species] = mole_frac

        # Normalize
        total_treated = sum(treated_moles.values())
        total_co2_stream = sum(co2_stream_moles.values())

        treated_composition = {sp: mole / total_treated
                             for sp, mole in treated_moles.items()}
        co2_composition = {sp: mole / total_co2_stream
                          for sp, mole in co2_stream_moles.items()}

        return treated_composition, co2_composition

    def psa_separation(self, inlet_composition: Dict[str, float],
                      h2_recovery: float = None,
                      h2_purity: float = None,
                      pressure_bar: float = None) -> Tuple[Dict, Dict]:
        """
        PSA (Pressure Swing Adsorption) for H2 purification

        Args:
            inlet_composition: Inlet mole fractions
            h2_recovery: H2 recovery efficiency (default from config)
            h2_purity: Target H2 purity (default from config)
            pressure_bar: PSA operating pressure (default from config)

        Returns:
            tuple: (h2_product, tail_gas)

        Process:
            - Adsorbs CO2, CO, CH4, N2 on zeolite/carbon
            - Produces high-purity H2 (>99.9%)
            - Tail gas contains unrecovered H2 + impurities
        """
        if h2_recovery is None:
            h2_recovery = config.PSA_H2_RECOVERY
        if h2_purity is None:
            h2_purity = config.PSA_H2_PURITY
        if pressure_bar is None:
            pressure_bar = config.PSA_PRESSURE_BAR

        # Calculate H2 distribution
        h2_inlet = inlet_composition.get('H2', 0.0)
        h2_to_product = h2_inlet * h2_recovery
        h2_to_tail = h2_inlet * (1 - h2_recovery)

        # Calculate impurity in product to achieve target purity
        # Purity = H2 / (H2 + impurities)
        # impurities = H2 * (1 - purity) / purity
        impurity_in_product = h2_to_product * (1 - h2_purity) / h2_purity

        # Distribute impurities proportionally
        total_impurities = sum(v for k, v in inlet_composition.items() if k != 'H2')

        h2_product_moles = {'H2': h2_to_product}
        tail_gas_moles = {'H2': h2_to_tail}

        for species, mole_frac in inlet_composition.items():
            if species != 'H2' and total_impurities > 0:
                # Fraction of this impurity
                impurity_fraction = mole_frac / total_impurities

                # Split between product and tail
                to_product = impurity_in_product * impurity_fraction
                to_tail = mole_frac - to_product

                h2_product_moles[species] = to_product
                tail_gas_moles[species] = to_tail

        # Normalize
        total_product = sum(h2_product_moles.values())
        total_tail = sum(tail_gas_moles.values())

        h2_product = {sp: mole / total_product
                     for sp, mole in h2_product_moles.items()}
        tail_gas = {sp: mole / total_tail
                   for sp, mole in tail_gas_moles.items()}

        return h2_product, tail_gas

    def calculate_stream_split(self, inlet_flow: float,
                              stream1_composition: Dict[str, float],
                              stream2_composition: Dict[str, float],
                              species: str = 'H2') -> Tuple[float, float]:
        """
        Calculate flow split based on species balance

        Args:
            inlet_flow: Inlet molar flow (mol/s)
            stream1_composition: Stream 1 mole fractions
            stream2_composition: Stream 2 mole fractions
            species: Species to balance on

        Returns:
            tuple: (stream1_flow, stream2_flow) in mol/s
        """
        # This is a simplified model
        # In reality, would solve mass balance equations

        # For now, estimate based on H2 distribution
        x_feed = inlet_flow  # Total inlet
        x1_frac = stream1_composition.get(species, 0.0)
        x2_frac = stream2_composition.get(species, 0.0)

        # Assume 88% recovery to product (from config)
        stream1_flow = inlet_flow * 0.88
        stream2_flow = inlet_flow * 0.12

        return stream1_flow, stream2_flow


# ==============================================================================
# TESTING AND VALIDATION
# ==============================================================================

def test_separation_models():
    """Test separation models with typical syngas composition"""
    print("\n" + "="*80)
    print("TESTING SEPARATION MODELS")
    print("="*80)

    sep = SeparationModels()

    # Typical syngas after LTS
    # (from literature: steam reforming + WGS)
    syngas = {
        'H2': 0.45,    # 45% H2
        'CO2': 0.25,   # 25% CO2
        'H2O': 0.20,   # 20% H2O
        'CO': 0.05,    # 5% CO
        'CH4': 0.03,   # 3% CH4
        'N2': 0.02     # 2% N2
    }

    print("\nInput Syngas Composition:")
    for species, mole_frac in sorted(syngas.items(),
                                    key=lambda x: x[1], reverse=True):
        print(f"    {species:8s}: {mole_frac:6.4f} ({mole_frac*100:5.2f}%)")

    # Test 1: Flash separation
    print("\n" + "-"*80)
    print("Test 1: Flash Separation (Water Removal)")
    print("-"*80)

    vapor, liquid = sep.flash_separation(syngas)

    print(f"\nVapor Phase (to CO2 removal):")
    for species, mole_frac in sorted(vapor.items(),
                                    key=lambda x: x[1], reverse=True):
        print(f"    {species:8s}: {mole_frac:6.4f} ({mole_frac*100:5.2f}%)")

    print(f"\nLiquid Phase (wastewater):")
    for species, mole_frac in sorted(liquid.items(),
                                    key=lambda x: x[1], reverse=True):
        print(f"    {species:8s}: {mole_frac:6.4f} ({mole_frac*100:5.2f}%)")

    # Test 2: CO2 removal
    print("\n" + "-"*80)
    print("Test 2: CO2 Removal (95% efficiency)")
    print("-"*80)

    treated, co2_stream = sep.co2_removal(vapor)

    print(f"\nTreated Gas (to PSA):")
    for species, mole_frac in sorted(treated.items(),
                                    key=lambda x: x[1], reverse=True):
        print(f"    {species:8s}: {mole_frac:6.4f} ({mole_frac*100:5.2f}%)")

    co2_removed = (syngas['CO2'] - treated['CO2']) / syngas['CO2'] * 100
    print(f"\nCO2 Removal: {co2_removed:.1f}%")

    # Test 3: PSA separation
    print("\n" + "-"*80)
    print("Test 3: PSA Separation (88% H2 recovery, 99.9% purity)")
    print("-"*80)

    h2_product, tail_gas = sep.psa_separation(treated)

    print(f"\nH2 Product:")
    for species, mole_frac in sorted(h2_product.items(),
                                    key=lambda x: x[1], reverse=True):
        print(f"    {species:8s}: {mole_frac:6.4f} ({mole_frac*100:5.2f}%)")

    h2_purity = h2_product['H2'] * 100
    print(f"\n    H2 Purity: {h2_purity:.2f}%")

    print(f"\nTail Gas (fuel/recycle):")
    for species, mole_frac in sorted(tail_gas.items(),
                                    key=lambda x: x[1], reverse=True):
        if mole_frac > 0.001:  # Only significant species
            print(f"    {species:8s}: {mole_frac:6.4f} ({mole_frac*100:5.2f}%)")

    # Test 4: Overall H2 recovery
    print("\n" + "-"*80)
    print("Test 4: Overall H2 Recovery")
    print("-"*80)

    h2_in = syngas['H2']
    h2_out = h2_product['H2']

    # Approximate recovery (simplified)
    # In reality would track molar flows
    print(f"\nH2 in syngas: {h2_in*100:.2f}%")
    print(f"H2 in product: {h2_out*100:.2f}%")
    print(f"Target recovery: {config.PSA_H2_RECOVERY*100:.1f}%")
    print(f"Target purity: {config.PSA_H2_PURITY*100:.1f}%")

    if h2_purity >= config.PSA_H2_PURITY * 100:
        print("[PASS] Purity target achieved")
    else:
        print(f"[WARNING] Purity below target")

    print("\n" + "="*80)
    print("SEPARATION MODELS TEST COMPLETE")
    print("="*80)


if __name__ == "__main__":
    test_separation_models()
