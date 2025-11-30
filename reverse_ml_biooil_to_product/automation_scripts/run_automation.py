"""
==============================================================================
ASPEN AUTOMATION - MAIN EXECUTION SCRIPT (BATCH MODE)
==============================================================================
Purpose: Run all 1,170 simulations in batches with pause/review capability
Author: Orhun Uzdiyem
Date: 2025-11-16

Features:
- Batch mode (run 100, pause, continue)
- Resume capability (skip completed simulations)
- Error handling and logging
- Progress tracking
- Statistics reporting
==============================================================================
"""

import pandas as pd
import time
import json
import os
from datetime import datetime
import sys

import config
from aspen_interface import AspenInterface
from database_operations import DatabaseOperations


class AutomationRunner:
    """Main automation runner with batch mode support."""

    def __init__(self):
        """Initialize automation runner."""
        self.aspen = AspenInterface()
        self.db = DatabaseOperations()
        self.start_time = None
        self.stats = {
            'total': 0,
            'completed': 0,
            'converged': 0,
            'failed': 0,
            'skipped': 0,
            'current_batch': 0
        }

    def load_simulation_matrix(self):
        """Load simulation scenarios from CSV."""
        print("\n[LOADER] Loading simulation matrix...")
        print(f"  File: {config.INPUT_DATA_PATH}")

        try:
            df = pd.read_csv(config.INPUT_DATA_PATH)
            print(f"  [OK] Loaded {len(df)} simulations")
            self.stats['total'] = len(df)
            return df
        except Exception as e:
            print(f"  [ERROR] Failed to load: {e}")
            return None

    def get_completed_simulations(self):
        """Get set of already completed simulation IDs."""
        print("\n[RESUME] Checking for completed simulations...")

        try:
            completed = self.db.get_completed_simulations()
            print(f"  Found {len(completed)} completed BiooilIds")
            return completed
        except Exception as e:
            print(f"  [ERROR] Failed to check: {e}")
            return set()

    def prepare_bio_oil_composition(self, row):
        """Extract bio-oil composition from simulation row."""
        comp = {
            'aromatics': row['aromatics'] / 100.0,  # Convert % to fraction
            'acids': row['acids'] / 100.0,
            'alcohols': row['alcohols'] / 100.0,
            'furans': row['furans'] / 100.0,
            'phenols': row['phenols'] / 100.0,
            'aldehyde_ketone': row['aldehyde_ketone'] / 100.0
        }

        # Normalize to sum = 1.0
        total = sum(comp.values())
        if total > 0:
            comp = {k: v/total for k, v in comp.items()}

        return comp

    def run_single_simulation(self, row):
        """
        Run a single simulation.

        Args:
            row: Row from simulation matrix DataFrame

        Returns:
            'converged', 'failed', or 'error'
        """
        sim_id = row['SimulationId']
        biooil_id = row['BiooilId']

        if config.VERBOSE_MODE:
            print(f"\n  [{sim_id}] BiooilId={biooil_id}, "
                  f"T={row['ReformerTemperature_C']:.0f}°C, "
                  f"P={row['ReformerPressure_bar']:.1f}bar, "
                  f"S/C={row['SteamToCarbonRatio']:.1f}")

        try:
            # 1. Set bio-oil composition
            comp = self.prepare_bio_oil_composition(row)
            if not self.aspen.set_biooil_composition(comp):
                return 'error'

            # 2. Set process conditions
            if not self.aspen.set_process_conditions(
                temp_c=row['ReformerTemperature_C'],
                pres_bar=row['ReformerPressure_bar'],
                sc_ratio=row['SteamToCarbonRatio'],
                biooil_flow_kgh=row['BiooilFeedRate_kgh']
            ):
                return 'error'

            # 3. Run simulation
            converged = self.aspen.run_simulation()

            if not converged:
                # Mark as failed in database
                self.db.mark_simulation_failed(
                    biooil_id=biooil_id,
                    error_message='Did not converge'
                )
                if config.VERBOSE_MODE:
                    print(f"      Status: FAILED (no convergence)")
                return 'failed'

            # 4. Extract results
            h2_data = self.aspen.extract_h2_properties()
            if not h2_data:
                self.db.mark_simulation_failed(
                    biooil_id=biooil_id,
                    error_message='Failed to extract H2 data'
                )
                return 'error'

            # 5. Store in database
            # Insert simulation record
            db_sim_id = self.db.insert_simulation(
                biooil_id=biooil_id,
                convergence_status='Converged',
                mass_error=0.05,  # Placeholder
                energy_error=0.8,  # Placeholder
                notes=f'Automation: SimId {sim_id}'
            )

            if not db_sim_id:
                return 'error'

            # Insert reforming conditions
            self.db.insert_reforming_conditions(
                simulation_id=db_sim_id,
                temp_c=row['ReformerTemperature_C'],
                pres_bar=row['ReformerPressure_bar'],
                sc_ratio=row['SteamToCarbonRatio'],
                biooil_flow=row['BiooilFeedRate_kgh'],
                steam_flow=row['SteamFeedRate_kgh']
            )

            # Insert H2 product data
            self.db.insert_hydrogen_product(db_sim_id, h2_data)

            # Insert syngas compositions at 4 locations
            for location, stream in config.SYNGAS_STREAMS.items():
                syngas_data = self.aspen.extract_syngas_composition(stream)
                if syngas_data:
                    self.db.insert_syngas_composition(db_sim_id, location, syngas_data)

            # Insert energy balance
            energy_data = self.aspen.extract_energy_data()
            if energy_data:
                self.db.insert_energy_balance(db_sim_id, energy_data)

            # Success
            if config.VERBOSE_MODE:
                print(f"      Status: CONVERGED "
                      f"(H2: {h2_data['H2_Yield_kg']:.2f} kg, "
                      f"Purity: {h2_data['H2_Purity_percent']:.2f}%)")

            return 'converged'

        except Exception as e:
            print(f"      [ERROR] Exception: {str(e)[:100]}")
            self.db.mark_simulation_failed(
                biooil_id=biooil_id,
                error_message=str(e)[:500]
            )
            return 'error'

    def run_batch(self, df_batch, batch_num):
        """
        Run a batch of simulations.

        Args:
            df_batch: DataFrame subset for this batch
            batch_num: Batch number (for display)

        Returns:
            Dictionary with batch statistics
        """
        print("\n" + "="*70)
        print(f"BATCH {batch_num}: Running {len(df_batch)} simulations")
        print("="*70)

        batch_stats = {'converged': 0, 'failed': 0, 'error': 0, 'skipped': 0}
        batch_start = time.time()

        for idx, row in df_batch.iterrows():
            # Run simulation
            result = self.run_single_simulation(row)

            # Update statistics
            batch_stats[result] += 1
            self.stats[result] += 1
            self.stats['completed'] += 1

            # Progress update
            if self.stats['completed'] % config.PROGRESS_UPDATE_FREQ == 0:
                self.print_progress()

        batch_time = time.time() - batch_start

        # Batch summary
        print("\n" + "-"*70)
        print(f"BATCH {batch_num} COMPLETE ({batch_time:.1f} seconds)")
        print(f"  Converged: {batch_stats['converged']}")
        print(f"  Failed:    {batch_stats['failed']}")
        print(f"  Errors:    {batch_stats['error']}")
        print("-"*70)

        return batch_stats

    def pause_between_batches(self, batch_num, total_batches):
        """Pause and ask user to review before continuing."""
        print("\n" + "="*70)
        print(f"BATCH {batch_num} of {total_batches} COMPLETED")
        print("="*70)

        # Show overall progress
        self.print_summary()

        # Pause
        if config.PAUSE_BETWEEN_BATCHES and batch_num < total_batches:
            print("\n[PAUSE] Review results above.")

            if config.AUTO_CONTINUE_DELAY > 0:
                print(f"  Auto-continuing in {config.AUTO_CONTINUE_DELAY} seconds...")
                print("  Press Ctrl+C to abort")
                try:
                    time.sleep(config.AUTO_CONTINUE_DELAY)
                except KeyboardInterrupt:
                    print("\n[ABORT] User interrupted")
                    return False
            else:
                print("  Press Enter to continue, or Ctrl+C to abort")
                try:
                    input()
                except KeyboardInterrupt:
                    print("\n[ABORT] User interrupted")
                    return False

        return True

    def print_progress(self):
        """Print current progress."""
        pct = (self.stats['completed'] / self.stats['total']) * 100
        elapsed = time.time() - self.start_time
        rate = self.stats['completed'] / elapsed if elapsed > 0 else 0
        remaining = (self.stats['total'] - self.stats['completed']) / rate if rate > 0 else 0

        print(f"\n  Progress: {self.stats['completed']}/{self.stats['total']} "
              f"({pct:.1f}%) | "
              f"Success: {self.stats['converged']} | "
              f"Failed: {self.stats['failed']} | "
              f"Rate: {rate:.2f} sim/s | "
              f"ETA: {remaining/60:.1f} min")

    def print_summary(self):
        """Print overall summary."""
        elapsed = time.time() - self.start_time if self.start_time else 0

        print("\n" + "="*70)
        print("OVERALL SUMMARY")
        print("="*70)
        print(f"Total Simulations:    {self.stats['total']}")
        print(f"Completed:            {self.stats['completed']}")
        print(f"  - Converged:        {self.stats['converged']} "
              f"({self.stats['converged']/self.stats['completed']*100:.1f}%)")
        print(f"  - Failed:           {self.stats['failed']}")
        print(f"  - Errors:           {self.stats['error']}")
        print(f"Skipped (existing):   {self.stats['skipped']}")
        print(f"Remaining:            {self.stats['total'] - self.stats['completed']}")
        print(f"Elapsed Time:         {elapsed/3600:.2f} hours")
        if self.stats['completed'] > 0:
            avg_time = elapsed / self.stats['completed']
            print(f"Average per sim:      {avg_time:.1f} seconds")
        print("="*70)

    def run(self, resume=True):
        """
        Main execution function with batch mode.

        Args:
            resume: Skip already completed simulations if True
        """
        print("="*70)
        print("ASPEN AUTOMATION - BATCH MODE")
        print("="*70)
        print(f"Batch Size: {config.BATCH_SIZE} simulations")
        print(f"Pause Between Batches: {'Yes' if config.PAUSE_BETWEEN_BATCHES else 'No'}")
        print(f"Resume Mode: {'Enabled' if resume else 'Disabled'}")
        print("="*70)

        self.start_time = time.time()

        # 1. Connect to Aspen
        if not self.aspen.connect():
            print("\n[ABORT] Failed to connect to Aspen")
            return False

        # 2. Load Aspen model
        if not self.aspen.load_model():
            print("\n[ABORT] Failed to load Aspen model")
            return False

        # 3. Connect to database
        if not self.db.connect():
            print("\n[ABORT] Failed to connect to database")
            return False

        # 4. Load simulation matrix
        df = self.load_simulation_matrix()
        if df is None:
            print("\n[ABORT] Failed to load simulation matrix")
            return False

        # 5. Check for completed simulations (resume mode)
        if resume:
            completed = self.get_completed_simulations()
            if completed:
                # Filter out completed
                df = df[~df['BiooilId'].isin(completed)]
                self.stats['skipped'] = len(completed)
                print(f"  [RESUME] Skipping {len(completed)} completed BiooilIds")
                print(f"  Remaining: {len(df)} simulations")

                if len(df) == 0:
                    print("\n[INFO] All simulations already completed!")
                    return True

        # 6. Run in batches
        total_batches = (len(df) + config.BATCH_SIZE - 1) // config.BATCH_SIZE
        print(f"\n[INFO] Will run {total_batches} batches of up to {config.BATCH_SIZE} simulations")

        for batch_num in range(1, total_batches + 1):
            # Get batch subset
            start_idx = (batch_num - 1) * config.BATCH_SIZE
            end_idx = min(start_idx + config.BATCH_SIZE, len(df))
            df_batch = df.iloc[start_idx:end_idx]

            # Run batch
            self.run_batch(df_batch, batch_num)

            # Pause between batches
            if not self.pause_between_batches(batch_num, total_batches):
                print("\n[ABORT] User interrupted automation")
                break

        # 7. Final summary
        print("\n" + "="*70)
        print("AUTOMATION COMPLETE")
        print("="*70)
        self.print_summary()

        # 8. Get database statistics
        print("\n[DATABASE] Querying final statistics...")
        db_stats = self.db.get_simulation_statistics()
        if db_stats:
            print("\nDatabase Statistics:")
            for status, stats in db_stats.items():
                print(f"  {status}: {stats['count']} records")

        # 9. Cleanup
        self.aspen.close()
        self.db.close()

        print("\n[DONE] Automation finished successfully!")
        return True


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

def main():
    """Main entry point."""
    # Print configuration
    config.print_config_summary()

    # Validate configuration
    issues = config.validate_config()
    if issues:
        print("\n[ERROR] Configuration issues:")
        for issue in issues:
            print(f"  - {issue}")
        print("\nPlease fix configuration before running automation.")
        return 1

    # Ask user to confirm
    print("\nReady to start automation?")
    print("  - Press Enter to start")
    print("  - Press Ctrl+C to abort")

    try:
        input()
    except KeyboardInterrupt:
        print("\n[ABORT] User cancelled")
        return 0

    # Run automation
    runner = AutomationRunner()
    success = runner.run(resume=True)

    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
