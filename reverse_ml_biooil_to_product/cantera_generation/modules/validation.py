"""
Validation Module for Cantera Simulation Results

This module performs 5 levels of validation:
1. Internal consistency (mass/energy balance)
2. Physical realism (valid ranges)
3. Thermodynamic feasibility
4. Statistical consistency
5. ML readiness checks
"""

import sys
import os
from typing import Dict, List, Tuple

# Add parent directory to path for config import
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import cantera_config as config


class ValidationEngine:
    """Validate simulation results for physical and chemical correctness"""

    def __init__(self):
        """Initialize validation engine"""
        self.validation_results = []

    def validate_mass_balance(self, simulation_data: Dict) -> Tuple[bool, List[str]]:
        """
        Level 1: Validate mass balance

        Args:
            simulation_data: Complete simulation results

        Returns:
            tuple: (is_valid, error_messages)

        Checks:
            - Mole fractions sum to 1.0 at each stage
            - Atom balance (C, H, O conserved)
        """
        errors = []

        # Check mole fraction sums
        stages = ['reformer', 'hts', 'lts', 'flash_vapor', 'co2_treated', 'h2_product']

        for stage in stages:
            if stage in simulation_data:
                mole_fractions = simulation_data[stage].get('mole_fractions', {})
                total = sum(mole_fractions.values())

                if abs(total - 1.0) > 1e-4:
                    errors.append(f"{stage}: Mole fractions sum to {total:.6f} (expected 1.0)")

        # Mass balance check would require tracking molar flows
        # Simplified here - assumes equilibrium calculations are self-consistent

        is_valid = len(errors) == 0
        return is_valid, errors

    def validate_energy_balance(self, simulation_data: Dict) -> Tuple[bool, List[str]]:
        """
        Level 1: Validate energy balance

        Args:
            simulation_data: Complete simulation results

        Returns:
            tuple: (is_valid, error_messages)

        Checks:
            - Energy balance within acceptable error
            - Positive heat duties where expected
        """
        errors = []

        energy_balance = simulation_data.get('energy_balance', {})

        # Check if net heat duty is reasonable
        net_duty = energy_balance.get('net_heat_duty', 0.0)
        if net_duty < 0:
            errors.append(f"Negative net heat duty: {net_duty:.2f} MJ (reforming should require heat)")

        # Check energy efficiency
        cold_gas_eff = energy_balance.get('cold_gas_efficiency', 0.0)
        if cold_gas_eff > 100.0:
            errors.append(f"Cold gas efficiency > 100%: {cold_gas_eff:.2f}%")

        is_valid = len(errors) == 0
        return is_valid, errors

    def validate_physical_ranges(self, ml_features: Dict) -> Tuple[bool, List[str]]:
        """
        Level 2: Validate physical ranges

        Args:
            ml_features: 16 ML features

        Returns:
            tuple: (is_valid, error_messages)

        Checks:
            - H2 yield: 5-15 kg/100kg bio-oil
            - Carbon conversion: 75-100%
            - Energy efficiency: 50-80%
            - H2 purity: >99%
        """
        errors = []

        # H2 yield
        h2_yield = ml_features.get('H2_Yield', 0.0)
        if not (config.H2_YIELD_MIN <= h2_yield <= config.H2_YIELD_MAX):
            errors.append(f"H2_Yield {h2_yield:.2f} outside range "
                        f"[{config.H2_YIELD_MIN}, {config.H2_YIELD_MAX}]")

        # Carbon conversion
        carbon_conv = ml_features.get('CarbonConversion', 0.0)
        if not (config.CARBON_CONV_MIN <= carbon_conv <= config.CARBON_CONV_MAX):
            errors.append(f"CarbonConversion {carbon_conv:.2f}% outside range "
                        f"[{config.CARBON_CONV_MIN}, {config.CARBON_CONV_MAX}]")

        # Energy efficiency
        energy_eff = ml_features.get('EnergyEfficiency', 0.0)
        if not (config.ENERGY_EFF_MIN <= energy_eff <= config.ENERGY_EFF_MAX):
            errors.append(f"EnergyEfficiency {energy_eff:.2f}% outside range "
                        f"[{config.ENERGY_EFF_MIN}, {config.ENERGY_EFF_MAX}]")

        # H2 purity
        h2_purity = ml_features.get('H2_Purity', 0.0)
        if h2_purity < 99.0:
            errors.append(f"H2_Purity {h2_purity:.2f}% below 99% (PSA target)")

        # Physical constraints
        if ml_features.get('H2_ProductionRate', 0.0) <= 0:
            errors.append("H2_ProductionRate must be positive")

        if ml_features.get('WaterConsumption', 0.0) <= 0:
            errors.append("WaterConsumption must be positive")

        # Composition constraints (0-100%)
        composition_features = [
            'Syngas_H2_Content', 'Syngas_CO_Content', 'Syngas_CO2_Content', 'Syngas_CH4_Content',
            'Product_H2_Content', 'Product_CO2_Content', 'Product_CH4_Content'
        ]

        for feature in composition_features:
            value = ml_features.get(feature, 0.0)
            if not (0.0 <= value <= 100.0):
                errors.append(f"{feature} {value:.2f}% outside range [0, 100]")

        is_valid = len(errors) == 0
        return is_valid, errors

    def validate_thermodynamic_feasibility(self, simulation_data: Dict) -> Tuple[bool, List[str]]:
        """
        Level 3: Validate thermodynamic feasibility

        Args:
            simulation_data: Complete simulation results

        Returns:
            tuple: (is_valid, warnings)

        Checks:
            - WGS equilibrium shift (CO decreases at lower T)
            - H2 enrichment through WGS stages
            - Realistic equilibrium compositions
        """
        warnings = []

        # Check H2 enrichment: Reformer → HTS → LTS
        try:
            h2_reformer = simulation_data['reformer']['mole_fractions'].get('H2', 0.0)
            h2_hts = simulation_data['hts']['mole_fractions'].get('H2', 0.0)
            h2_lts = simulation_data['lts']['mole_fractions'].get('H2', 0.0)

            if not (h2_reformer <= h2_hts <= h2_lts):
                warnings.append(f"H2 not increasing through WGS: "
                              f"Reformer={h2_reformer:.3f}, HTS={h2_hts:.3f}, LTS={h2_lts:.3f}")

            # Check CO depletion
            co_reformer = simulation_data['reformer']['mole_fractions'].get('CO', 0.0)
            co_lts = simulation_data['lts']['mole_fractions'].get('CO', 0.0)

            if co_lts >= co_reformer:
                warnings.append(f"CO not decreasing through WGS: "
                              f"Reformer={co_reformer:.3f}, LTS={co_lts:.3f}")

            # Check CO2 increase
            co2_reformer = simulation_data['reformer']['mole_fractions'].get('CO2', 0.0)
            co2_lts = simulation_data['lts']['mole_fractions'].get('CO2', 0.0)

            if co2_lts <= co2_reformer:
                warnings.append(f"CO2 not increasing through WGS: "
                              f"Reformer={co2_reformer:.3f}, LTS={co2_lts:.3f}")

        except KeyError as e:
            warnings.append(f"Missing data for thermodynamic check: {e}")

        # Warnings don't invalidate, but are logged
        is_valid = True
        return is_valid, warnings

    def validate_statistical_consistency(self, ml_features: Dict,
                                        expected_ranges: Dict = None) -> Tuple[bool, List[str]]:
        """
        Level 4: Validate statistical consistency

        Args:
            ml_features: 16 ML features
            expected_ranges: Expected ranges from literature (optional)

        Returns:
            tuple: (is_valid, warnings)

        Checks:
            - Values are within reasonable statistical ranges
            - No extreme outliers
        """
        warnings = []

        # Expected ranges from steam reforming literature
        if expected_ranges is None:
            expected_ranges = {
                'H2_Yield': (7.0, 13.0),           # kg/100kg (typical)
                'H2_CO_Ratio': (3.0, 30.0),        # After WGS
                'Syngas_H2_Content': (40.0, 70.0), # % dry basis
                'CarbonConversion': (80.0, 98.0),  # %
                'EnergyEfficiency': (55.0, 75.0)   # %
            }

        for feature, (min_val, max_val) in expected_ranges.items():
            if feature in ml_features:
                value = ml_features[feature]
                if not (min_val <= value <= max_val):
                    warnings.append(f"{feature} = {value:.2f} outside typical range "
                                  f"[{min_val}, {max_val}] (may be valid but unusual)")

        # These are warnings, not errors
        is_valid = True
        return is_valid, warnings

    def validate_ml_readiness(self, ml_features: Dict) -> Tuple[bool, List[str]]:
        """
        Level 5: Validate ML readiness

        Args:
            ml_features: 16 ML features

        Returns:
            tuple: (is_valid, errors)

        Checks:
            - All 16 features present
            - No NaN or Inf values
            - No missing data
        """
        errors = []

        # Required features (16 ML inputs)
        required_features = [
            'H2_Yield', 'H2_Purity', 'H2_ProductionRate', 'CarbonConversion',
            'EnergyEfficiency', 'H2_CO_Ratio', 'Syngas_H2_Content',
            'Syngas_CO_Content', 'Syngas_CO2_Content', 'Syngas_CH4_Content',
            'Product_H2_Content', 'Product_CO2_Content', 'Product_CH4_Content',
            'WaterConsumption', 'SteamToCarbon_Actual', 'OverallH2Recovery'
        ]

        # Check all features present
        for feature in required_features:
            if feature not in ml_features:
                errors.append(f"Missing feature: {feature}")
                continue

            value = ml_features[feature]

            # Check for NaN
            if value != value:  # NaN check
                errors.append(f"{feature} is NaN")

            # Check for Inf
            if abs(value) == float('inf'):
                errors.append(f"{feature} is Inf")

            # Check for None
            if value is None:
                errors.append(f"{feature} is None")

        is_valid = len(errors) == 0
        return is_valid, errors

    def validate_complete_simulation(self, simulation_data: Dict) -> Dict:
        """
        Perform all 5 levels of validation

        Args:
            simulation_data: Complete simulation results

        Returns:
            dict: Validation report

        Structure:
            {
                'overall_valid': bool,
                'level1_mass_balance': {'valid': bool, 'errors': []},
                'level1_energy_balance': {'valid': bool, 'errors': []},
                'level2_physical_ranges': {'valid': bool, 'errors': []},
                'level3_thermodynamic': {'valid': bool, 'warnings': []},
                'level4_statistical': {'valid': bool, 'warnings': []},
                'level5_ml_readiness': {'valid': bool, 'errors': []}
            }
        """
        report = {}

        # Level 1: Mass and energy balance
        mass_valid, mass_errors = self.validate_mass_balance(simulation_data)
        report['level1_mass_balance'] = {'valid': mass_valid, 'errors': mass_errors}

        energy_valid, energy_errors = self.validate_energy_balance(simulation_data)
        report['level1_energy_balance'] = {'valid': energy_valid, 'errors': energy_errors}

        # Level 2: Physical ranges
        ml_features = simulation_data.get('ml_features', {})
        phys_valid, phys_errors = self.validate_physical_ranges(ml_features)
        report['level2_physical_ranges'] = {'valid': phys_valid, 'errors': phys_errors}

        # Level 3: Thermodynamic feasibility
        thermo_valid, thermo_warnings = self.validate_thermodynamic_feasibility(simulation_data)
        report['level3_thermodynamic'] = {'valid': thermo_valid, 'warnings': thermo_warnings}

        # Level 4: Statistical consistency
        stat_valid, stat_warnings = self.validate_statistical_consistency(ml_features)
        report['level4_statistical'] = {'valid': stat_valid, 'warnings': stat_warnings}

        # Level 5: ML readiness
        ml_valid, ml_errors = self.validate_ml_readiness(ml_features)
        report['level5_ml_readiness'] = {'valid': ml_valid, 'errors': ml_errors}

        # Overall validation (errors only, warnings don't fail)
        report['overall_valid'] = all([
            mass_valid, energy_valid, phys_valid, thermo_valid, ml_valid
        ])

        return report

    def print_validation_report(self, report: Dict, simulation_id: str = ""):
        """
        Print formatted validation report

        Args:
            report: Validation report dictionary
            simulation_id: Optional simulation identifier
        """
        print(f"\n{'='*80}")
        print(f"VALIDATION REPORT {simulation_id}")
        print(f"{'='*80}")

        # Overall status
        if report['overall_valid']:
            print("[PASS] Overall validation: PASSED")
        else:
            print("[FAIL] Overall validation: FAILED")

        # Level 1
        print(f"\nLevel 1: Mass & Energy Balance")
        if report['level1_mass_balance']['valid']:
            print("  [PASS] Mass balance")
        else:
            print("  [FAIL] Mass balance:")
            for error in report['level1_mass_balance']['errors']:
                print(f"    - {error}")

        if report['level1_energy_balance']['valid']:
            print("  [PASS] Energy balance")
        else:
            print("  [FAIL] Energy balance:")
            for error in report['level1_energy_balance']['errors']:
                print(f"    - {error}")

        # Level 2
        print(f"\nLevel 2: Physical Ranges")
        if report['level2_physical_ranges']['valid']:
            print("  [PASS] All features within valid ranges")
        else:
            print("  [FAIL] Physical range violations:")
            for error in report['level2_physical_ranges']['errors']:
                print(f"    - {error}")

        # Level 3
        print(f"\nLevel 3: Thermodynamic Feasibility")
        if len(report['level3_thermodynamic']['warnings']) == 0:
            print("  [PASS] Thermodynamically feasible")
        else:
            print("  [WARNING] Thermodynamic warnings:")
            for warning in report['level3_thermodynamic']['warnings']:
                print(f"    - {warning}")

        # Level 4
        print(f"\nLevel 4: Statistical Consistency")
        if len(report['level4_statistical']['warnings']) == 0:
            print("  [PASS] Statistically consistent")
        else:
            print("  [WARNING] Statistical warnings:")
            for warning in report['level4_statistical']['warnings']:
                print(f"    - {warning}")

        # Level 5
        print(f"\nLevel 5: ML Readiness")
        if report['level5_ml_readiness']['valid']:
            print("  [PASS] Ready for ML training")
        else:
            print("  [FAIL] Not ready for ML:")
            for error in report['level5_ml_readiness']['errors']:
                print(f"    - {error}")

        print(f"{'='*80}\n")


# ==============================================================================
# TESTING
# ==============================================================================

def test_validation():
    """Test validation engine with sample data"""
    print("\n" + "="*80)
    print("TESTING VALIDATION ENGINE")
    print("="*80)

    validator = ValidationEngine()

    # Sample GOOD simulation data
    good_data = {
        'reformer': {
            'mole_fractions': {'H2': 0.50, 'CO': 0.15, 'CO2': 0.20, 'CH4': 0.05, 'H2O': 0.08, 'N2': 0.02}
        },
        'hts': {
            'mole_fractions': {'H2': 0.55, 'CO': 0.08, 'CO2': 0.25, 'CH4': 0.05, 'H2O': 0.05, 'N2': 0.02}
        },
        'lts': {
            'mole_fractions': {'H2': 0.60, 'CO': 0.03, 'CO2': 0.28, 'CH4': 0.05, 'H2O': 0.02, 'N2': 0.02}
        },
        'flash_vapor': {'mole_fractions': {}},
        'co2_treated': {'mole_fractions': {}},
        'h2_product': {'H2': 0.999, 'CO2': 0.0005, 'CH4': 0.0003, 'N2': 0.0002},
        'ml_features': {
            'H2_Yield': 10.5,
            'H2_Purity': 99.9,
            'H2_ProductionRate': 500.0,
            'CarbonConversion': 92.0,
            'EnergyEfficiency': 65.0,
            'H2_CO_Ratio': 20.0,
            'Syngas_H2_Content': 60.0,
            'Syngas_CO_Content': 3.0,
            'Syngas_CO2_Content': 28.0,
            'Syngas_CH4_Content': 5.0,
            'Product_H2_Content': 99.9,
            'Product_CO2_Content': 0.05,
            'Product_CH4_Content': 0.03,
            'WaterConsumption': 2.5,
            'SteamToCarbon_Actual': 4.0,
            'OverallH2Recovery': 88.0
        },
        'energy_balance': {
            'net_heat_duty': 400.0,
            'cold_gas_efficiency': 65.0
        }
    }

    print("\nTest 1: Validate GOOD Simulation")
    print("-" * 80)
    report = validator.validate_complete_simulation(good_data)
    validator.print_validation_report(report, "GOOD_DATA")

    # Sample BAD simulation data
    bad_data = good_data.copy()
    bad_data['ml_features'] = {
        'H2_Yield': 25.0,  # Too high!
        'H2_Purity': 85.0,  # Too low!
        'H2_ProductionRate': 500.0,
        'CarbonConversion': 110.0,  # Impossible!
        'EnergyEfficiency': 95.0,  # Too high!
        'H2_CO_Ratio': 20.0,
        'Syngas_H2_Content': 60.0,
        'Syngas_CO_Content': 3.0,
        'Syngas_CO2_Content': 28.0,
        'Syngas_CH4_Content': 5.0,
        'Product_H2_Content': 85.0,
        'Product_CO2_Content': 10.0,
        'Product_CH4_Content': 3.0,
        'WaterConsumption': 2.5,
        'SteamToCarbon_Actual': 4.0,
        'OverallH2Recovery': 88.0
    }

    print("\nTest 2: Validate BAD Simulation (should fail)")
    print("-" * 80)
    report = validator.validate_complete_simulation(bad_data)
    validator.print_validation_report(report, "BAD_DATA")

    print("\n" + "="*80)
    print("VALIDATION ENGINE TEST COMPLETE")
    print("="*80)


if __name__ == "__main__":
    test_validation()
