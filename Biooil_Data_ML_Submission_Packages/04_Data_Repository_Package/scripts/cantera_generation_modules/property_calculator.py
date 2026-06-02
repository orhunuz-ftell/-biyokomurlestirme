"""
Property Calculator for Hydrogen Production Analysis

This module calculates:
- H2 yield and productivity
- Carbon conversion efficiency
- Energy efficiency
- Syngas composition metrics
- All 16 ML input features
"""

import sys
import os
from typing import Dict

# Add parent directory to path for config import
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import cantera_config as config


class PropertyCalculator:
    """Calculate process performance metrics"""

    def __init__(self):
        """Initialize property calculator"""
        pass

    def calculate_h2_yield(self, h2_moles_out: float,
                          biooil_mass_in: float = 100.0) -> float:
        """
        Calculate H2 yield (kg H2 per 100 kg bio-oil)

        Args:
            h2_moles_out: H2 moles produced
            biooil_mass_in: Bio-oil mass input (default 100 kg)

        Returns:
            float: H2 yield (kg per 100 kg bio-oil)
        """
        h2_mass_kg = h2_moles_out * config.MOLECULAR_WEIGHTS['H2'] / 1000.0
        yield_kg_per_100kg = (h2_mass_kg / biooil_mass_in) * 100.0

        return yield_kg_per_100kg

    def calculate_carbon_conversion(self, carbon_in_biooil: float,
                                   carbon_in_products: float) -> float:
        """
        Calculate carbon conversion efficiency

        Args:
            carbon_in_biooil: Carbon moles in bio-oil
            carbon_in_products: Carbon moles in gaseous products

        Returns:
            float: Carbon conversion (%)

        Formula:
            C_conv = (C_in_gas / C_in_biooil) × 100%
        """
        if carbon_in_biooil < 1e-10:
            return 0.0

        conversion = (carbon_in_products / carbon_in_biooil) * 100.0
        return min(conversion, 100.0)  # Cap at 100%

    def calculate_energy_efficiency(self, h2_produced_kg: float,
                                   biooil_consumed_kg: float = 100.0) -> float:
        """
        Calculate energy efficiency (cold gas efficiency)

        Args:
            h2_produced_kg: H2 mass produced (kg)
            biooil_consumed_kg: Bio-oil mass consumed (kg)

        Returns:
            float: Energy efficiency (%)

        Formula:
            η = (HHV_H2 × m_H2) / (HHV_biooil × m_biooil) × 100%
        """
        energy_out = h2_produced_kg * config.HHV['H2']  # MJ
        energy_in = biooil_consumed_kg * config.HHV['biooil']  # MJ

        if energy_in < 1e-10:
            return 0.0

        efficiency = (energy_out / energy_in) * 100.0
        return efficiency

    def calculate_syngas_metrics(self, composition: Dict[str, float]) -> Dict:
        """
        Calculate syngas composition metrics

        Args:
            composition: Mole fractions

        Returns:
            dict: Syngas metrics (H2_content, CO_content, etc.)
        """
        metrics = {
            'H2_content': composition.get('H2', 0.0) * 100.0,      # %
            'CO_content': composition.get('CO', 0.0) * 100.0,      # %
            'CO2_content': composition.get('CO2', 0.0) * 100.0,    # %
            'CH4_content': composition.get('CH4', 0.0) * 100.0,    # %
            'H2O_content': composition.get('H2O', 0.0) * 100.0,    # %
            'N2_content': composition.get('N2', 0.0) * 100.0       # %
        }

        # Calculate H2/CO ratio
        h2 = composition.get('H2', 0.0)
        co = composition.get('CO', 0.0)
        metrics['H2_CO_ratio'] = h2 / co if co > 1e-10 else 999.9

        # Calculate dry gas composition (excluding H2O)
        dry_total = sum(v for k, v in composition.items() if k != 'H2O')
        if dry_total > 1e-10:
            metrics['H2_dry'] = composition.get('H2', 0.0) / dry_total * 100.0
            metrics['CO_dry'] = composition.get('CO', 0.0) / dry_total * 100.0
            metrics['CO2_dry'] = composition.get('CO2', 0.0) / dry_total * 100.0
        else:
            metrics['H2_dry'] = 0.0
            metrics['CO_dry'] = 0.0
            metrics['CO2_dry'] = 0.0

        return metrics

    def calculate_ml_features(self, simulation_data: Dict) -> Dict:
        """
        Calculate all 16 ML input features

        Args:
            simulation_data: Complete simulation results

        Returns:
            dict: 16 ML features for HydrogenProduct table

        Features (from database schema):
            1. H2_Yield (kg per 100 kg bio-oil)
            2. H2_Purity (%)
            3. H2_ProductionRate (mol/s per 100 kg/h bio-oil)
            4. CarbonConversion (%)
            5. EnergyEfficiency (%)
            6. H2_CO_Ratio
            7. Syngas_H2_Content (%)
            8. Syngas_CO_Content (%)
            9. Syngas_CO2_Content (%)
            10. Syngas_CH4_Content (%)
            11. Product_H2_Content (%)
            12. Product_CO2_Content (%)
            13. Product_CH4_Content (%)
            14. WaterConsumption (kg per kg bio-oil)
            15. SteamToCarbon_Actual
            16. OverallH2Recovery (%)
        """
        # Extract key data
        reformer = simulation_data.get('reformer', {})
        hts = simulation_data.get('hts', {})
        lts = simulation_data.get('lts', {})
        flash_vapor = simulation_data.get('flash_vapor', {})
        co2_treated = simulation_data.get('co2_treated', {})
        h2_product = simulation_data.get('h2_product', {})
        process_conditions = simulation_data.get('process_conditions', {})

        # Calculate features
        features = {}

        # Feature 1: H2 Yield
        # Simplified: assume basis of 100 kg bio-oil
        h2_moles = simulation_data.get('h2_moles_total', 0.0)
        features['H2_Yield'] = self.calculate_h2_yield(h2_moles, 100.0)

        # Feature 2: H2 Purity
        features['H2_Purity'] = h2_product.get('H2', 0.0) * 100.0

        # Feature 3: H2 Production Rate (simplified basis)
        # Normalized to 100 kg/h bio-oil feed
        features['H2_ProductionRate'] = h2_moles / 1.0  # mol/s (simplified)

        # Feature 4: Carbon Conversion
        carbon_in = simulation_data.get('carbon_in_biooil', 0.0)
        carbon_out = simulation_data.get('carbon_in_gas', 0.0)
        features['CarbonConversion'] = self.calculate_carbon_conversion(carbon_in, carbon_out)

        # Feature 5: Energy Efficiency
        features['EnergyEfficiency'] = self.calculate_energy_efficiency(
            features['H2_Yield'], 100.0
        )

        # Feature 6: H2/CO Ratio
        syngas_metrics = self.calculate_syngas_metrics(lts.get('mole_fractions', {}))
        features['H2_CO_Ratio'] = syngas_metrics['H2_CO_ratio']

        # Features 7-10: Syngas composition (after LTS)
        features['Syngas_H2_Content'] = syngas_metrics['H2_content']
        features['Syngas_CO_Content'] = syngas_metrics['CO_content']
        features['Syngas_CO2_Content'] = syngas_metrics['CO2_content']
        features['Syngas_CH4_Content'] = syngas_metrics['CH4_content']

        # Features 11-13: Product composition
        features['Product_H2_Content'] = h2_product.get('H2', 0.0) * 100.0
        features['Product_CO2_Content'] = h2_product.get('CO2', 0.0) * 100.0
        features['Product_CH4_Content'] = h2_product.get('CH4', 0.0) * 100.0

        # Feature 14: Water consumption
        # S/C ratio × carbon × MW_H2O / 100 kg biooil
        sc_ratio = process_conditions.get('SC_ratio', 0.0)
        features['WaterConsumption'] = sc_ratio * carbon_in * 18.015 / 100.0

        # Feature 15: Actual S/C ratio (same as input for equilibrium model)
        features['SteamToCarbon_Actual'] = sc_ratio

        # Feature 16: Overall H2 Recovery
        h2_in_syngas = lts.get('mole_fractions', {}).get('H2', 0.0)
        h2_in_product = h2_product.get('H2', 0.0)
        if h2_in_syngas > 1e-10:
            features['OverallH2Recovery'] = (h2_in_product / h2_in_syngas) * 100.0
        else:
            features['OverallH2Recovery'] = 0.0

        return features

    def validate_features(self, features: Dict) -> Dict:
        """
        Validate ML features against physical constraints

        Args:
            features: ML features dictionary

        Returns:
            dict: Validation results {'valid': bool, 'warnings': list}
        """
        warnings = []
        valid = True

        # Check H2 yield range
        if not (config.H2_YIELD_MIN <= features['H2_Yield'] <= config.H2_YIELD_MAX):
            warnings.append(f"H2_Yield {features['H2_Yield']:.2f} outside range "
                          f"[{config.H2_YIELD_MIN}, {config.H2_YIELD_MAX}]")
            valid = False

        # Check carbon conversion
        if not (config.CARBON_CONV_MIN <= features['CarbonConversion'] <= config.CARBON_CONV_MAX):
            warnings.append(f"CarbonConversion {features['CarbonConversion']:.2f}% outside range "
                          f"[{config.CARBON_CONV_MIN}, {config.CARBON_CONV_MAX}]")
            valid = False

        # Check energy efficiency
        if not (config.ENERGY_EFF_MIN <= features['EnergyEfficiency'] <= config.ENERGY_EFF_MAX):
            warnings.append(f"EnergyEfficiency {features['EnergyEfficiency']:.2f}% outside range "
                          f"[{config.ENERGY_EFF_MIN}, {config.ENERGY_EFF_MAX}]")
            valid = False

        # Check H2 purity
        if features['H2_Purity'] < 99.0:  # Should be >99% from PSA
            warnings.append(f"H2_Purity {features['H2_Purity']:.2f}% is low (expected >99%)")

        # Check physical constraints
        if features['H2_ProductionRate'] <= 0:
            warnings.append("H2_ProductionRate must be positive")
            valid = False

        if features['WaterConsumption'] <= 0:
            warnings.append("WaterConsumption must be positive")
            valid = False

        return {
            'valid': valid,
            'warnings': warnings
        }


# ==============================================================================
# TESTING AND VALIDATION
# ==============================================================================

def test_property_calculator():
    """Test property calculator with sample data"""
    print("\n" + "="*80)
    print("TESTING PROPERTY CALCULATOR")
    print("="*80)

    calc = PropertyCalculator()

    # Sample simulation data
    simulation_data = {
        'process_conditions': {
            'Temperature_C': 800,
            'Pressure_bar': 15,
            'SC_ratio': 4.0
        },
        'reformer': {
            'mole_fractions': {
                'H2': 0.50, 'CO': 0.15, 'CO2': 0.20, 'CH4': 0.05,
                'H2O': 0.08, 'N2': 0.02
            }
        },
        'hts': {
            'mole_fractions': {
                'H2': 0.55, 'CO': 0.08, 'CO2': 0.25, 'CH4': 0.05,
                'H2O': 0.05, 'N2': 0.02
            }
        },
        'lts': {
            'mole_fractions': {
                'H2': 0.60, 'CO': 0.03, 'CO2': 0.28, 'CH4': 0.05,
                'H2O': 0.02, 'N2': 0.02
            }
        },
        'flash_vapor': {
            'mole_fractions': {
                'H2': 0.61, 'CO': 0.03, 'CO2': 0.28, 'CH4': 0.05,
                'N2': 0.02, 'H2O': 0.01
            }
        },
        'co2_treated': {
            'mole_fractions': {
                'H2': 0.80, 'CO': 0.04, 'CO2': 0.02, 'CH4': 0.06,
                'N2': 0.03, 'H2O': 0.05
            }
        },
        'h2_product': {
            'H2': 0.999, 'CO2': 0.0005, 'CH4': 0.0003, 'N2': 0.0002
        },
        'h2_moles_total': 500.0,  # mol
        'carbon_in_biooil': 100.0,  # mol
        'carbon_in_gas': 95.0  # mol
    }

    print("\nTest 1: Calculate Syngas Metrics")
    print("-" * 80)

    syngas_metrics = calc.calculate_syngas_metrics(
        simulation_data['lts']['mole_fractions']
    )

    print("Syngas Composition (after LTS):")
    print(f"    H2: {syngas_metrics['H2_content']:.2f}%")
    print(f"    CO: {syngas_metrics['CO_content']:.2f}%")
    print(f"    CO2: {syngas_metrics['CO2_content']:.2f}%")
    print(f"    CH4: {syngas_metrics['CH4_content']:.2f}%")
    print(f"    H2/CO ratio: {syngas_metrics['H2_CO_ratio']:.2f}")

    print("\nTest 2: Calculate ML Features")
    print("-" * 80)

    features = calc.calculate_ml_features(simulation_data)

    print("\n16 ML Features:")
    print(f"    1.  H2_Yield: {features['H2_Yield']:.2f} kg/100kg biooil")
    print(f"    2.  H2_Purity: {features['H2_Purity']:.2f}%")
    print(f"    3.  H2_ProductionRate: {features['H2_ProductionRate']:.2f} mol/s")
    print(f"    4.  CarbonConversion: {features['CarbonConversion']:.2f}%")
    print(f"    5.  EnergyEfficiency: {features['EnergyEfficiency']:.2f}%")
    print(f"    6.  H2_CO_Ratio: {features['H2_CO_Ratio']:.2f}")
    print(f"    7.  Syngas_H2_Content: {features['Syngas_H2_Content']:.2f}%")
    print(f"    8.  Syngas_CO_Content: {features['Syngas_CO_Content']:.2f}%")
    print(f"    9.  Syngas_CO2_Content: {features['Syngas_CO2_Content']:.2f}%")
    print(f"    10. Syngas_CH4_Content: {features['Syngas_CH4_Content']:.2f}%")
    print(f"    11. Product_H2_Content: {features['Product_H2_Content']:.2f}%")
    print(f"    12. Product_CO2_Content: {features['Product_CO2_Content']:.2f}%")
    print(f"    13. Product_CH4_Content: {features['Product_CH4_Content']:.2f}%")
    print(f"    14. WaterConsumption: {features['WaterConsumption']:.2f} kg/kg")
    print(f"    15. SteamToCarbon_Actual: {features['SteamToCarbon_Actual']:.2f}")
    print(f"    16. OverallH2Recovery: {features['OverallH2Recovery']:.2f}%")

    print("\nTest 3: Validate Features")
    print("-" * 80)

    validation = calc.validate_features(features)

    if validation['valid']:
        print("[PASS] All features within valid ranges")
    else:
        print("[WARNING] Some features outside valid ranges:")
        for warning in validation['warnings']:
            print(f"    - {warning}")

    print("\n" + "="*80)
    print("PROPERTY CALCULATOR TEST COMPLETE")
    print("="*80)


if __name__ == "__main__":
    test_property_calculator()
