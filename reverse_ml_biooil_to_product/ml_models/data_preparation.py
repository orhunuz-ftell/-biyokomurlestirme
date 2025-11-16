"""
Data Preparation Module for Reverse ML Project
Purpose: Prepare Aspen simulation data for machine learning training
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')


class ReverseMLDataPreparation:
    """
    Prepares data for reverse ML: Product properties → Bio-oil properties
    """

    def __init__(self):
        self.scaler = StandardScaler()
        self.input_features = []   # Product properties
        self.output_targets = []   # Bio-oil properties

    def load_simulation_data(self, filepath):
        """
        Load raw simulation data from Aspen outputs

        Parameters:
        -----------
        filepath : str
            Path to CSV file containing simulation results

        Returns:
        --------
        df : DataFrame
            Raw simulation data
        """
        df = pd.read_csv(filepath)
        print(f"Loaded {len(df)} simulation runs from {filepath}")
        return df

    def define_features_targets(self, df):
        """
        Define input features (product properties) and output targets (bio-oil properties)

        Parameters:
        -----------
        df : DataFrame
            Complete simulation dataset
        """
        # OUTPUT TARGETS: Bio-oil properties (what we want to predict)
        self.output_targets = [
            'biooil_aromatics',
            'biooil_acids',
            'biooil_alcohols',
            'biooil_furans',
            'biooil_phenols',
            'biooil_aldehyde_ketone',
            'biooil_esters',
            'biooil_aliphatic'
            # Add more bio-oil components as needed
        ]

        # INPUT FEATURES: Product properties (from Aspen simulation outputs)
        # TODO: Update these based on actual Aspen output
        self.input_features = [
            # Product composition
            'product_component_1',
            'product_component_2',
            # Physical properties
            'product_density',
            'product_viscosity',
            'product_boiling_point',
            # Process conditions
            'reactor_temperature',
            'reactor_pressure',
            'residence_time',
            # Performance metrics
            'conversion_rate',
            'yield',
            # Add more features as needed
        ]

        print(f"Defined {len(self.input_features)} input features")
        print(f"Defined {len(self.output_targets)} output targets")

        return self.input_features, self.output_targets

    def clean_data(self, df):
        """
        Clean and validate simulation data

        Parameters:
        -----------
        df : DataFrame
            Raw simulation data

        Returns:
        --------
        df_clean : DataFrame
            Cleaned data
        """
        initial_rows = len(df)

        # Remove failed simulations (non-converged)
        if 'convergence_status' in df.columns:
            df = df[df['convergence_status'] == 'Converged']
            print(f"Removed {initial_rows - len(df)} non-converged simulations")

        # Remove rows with missing values in critical columns
        df = df.dropna(subset=self.output_targets)

        # Check for unrealistic values
        # TODO: Add specific checks based on process knowledge

        print(f"Data cleaning complete. {len(df)} valid simulations remaining")
        return df

    def feature_engineering(self, df):
        """
        Create derived features if needed

        Parameters:
        -----------
        df : DataFrame
            Cleaned simulation data

        Returns:
        --------
        df : DataFrame
            Data with engineered features
        """
        # Example: Create ratio features
        # df['H_to_C_ratio'] = df['hydrogen_content'] / df['carbon_content']

        # Example: Create interaction features
        # df['temp_pressure_interaction'] = df['temperature'] * df['pressure']

        print("Feature engineering complete")
        return df

    def normalize_data(self, X_train, X_test):
        """
        Normalize/standardize input features

        Parameters:
        -----------
        X_train : DataFrame
            Training features
        X_test : DataFrame
            Test features

        Returns:
        --------
        X_train_scaled, X_test_scaled : DataFrames
            Normalized features
        """
        self.scaler.fit(X_train)

        X_train_scaled = pd.DataFrame(
            self.scaler.transform(X_train),
            columns=X_train.columns,
            index=X_train.index
        )

        X_test_scaled = pd.DataFrame(
            self.scaler.transform(X_test),
            columns=X_test.columns,
            index=X_test.index
        )

        print("Data normalization complete")
        return X_train_scaled, X_test_scaled

    def prepare_train_test_split(self, df, test_size=0.2, random_state=42):
        """
        Split data into training and test sets

        Parameters:
        -----------
        df : DataFrame
            Complete prepared dataset
        test_size : float
            Proportion of data for testing
        random_state : int
            Random seed for reproducibility

        Returns:
        --------
        X_train, X_test, y_train, y_test : DataFrames
            Split datasets
        """
        X = df[self.input_features]
        y = df[self.output_targets]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )

        print(f"\nDataset split:")
        print(f"Training set: {X_train.shape}")
        print(f"Test set: {X_test.shape}")

        return X_train, X_test, y_train, y_test

    def save_processed_data(self, X_train, X_test, y_train, y_test, output_dir='../data/processed'):
        """
        Save processed data to files
        """
        X_train.to_csv(f'{output_dir}/X_train.csv', index=False)
        X_test.to_csv(f'{output_dir}/X_test.csv', index=False)
        y_train.to_csv(f'{output_dir}/y_train.csv', index=False)
        y_test.to_csv(f'{output_dir}/y_test.csv', index=False)

        print(f"Processed data saved to {output_dir}")

    def run_full_pipeline(self, input_filepath, output_dir='../data/processed'):
        """
        Execute complete data preparation pipeline

        Parameters:
        -----------
        input_filepath : str
            Path to raw simulation data
        output_dir : str
            Directory to save processed data
        """
        print("="*60)
        print("REVERSE ML DATA PREPARATION PIPELINE")
        print("="*60)

        # Load data
        df = self.load_simulation_data(input_filepath)

        # Define features and targets
        self.define_features_targets(df)

        # Clean data
        df_clean = self.clean_data(df)

        # Feature engineering
        df_engineered = self.feature_engineering(df_clean)

        # Train-test split
        X_train, X_test, y_train, y_test = self.prepare_train_test_split(df_engineered)

        # Normalize features
        X_train_scaled, X_test_scaled = self.normalize_data(X_train, X_test)

        # Save processed data
        self.save_processed_data(X_train_scaled, X_test_scaled, y_train, y_test, output_dir)

        print("\n" + "="*60)
        print("DATA PREPARATION COMPLETE")
        print("="*60)

        return X_train_scaled, X_test_scaled, y_train, y_test


if __name__ == "__main__":
    # Example usage
    prep = ReverseMLDataPreparation()

    # TODO: Update with actual file path once simulation data is available
    # X_train, X_test, y_train, y_test = prep.run_full_pipeline(
    #     input_filepath='../data/raw/simulation_results.csv'
    # )

    print("Data preparation module loaded successfully")
    print("Waiting for Aspen simulation data...")
