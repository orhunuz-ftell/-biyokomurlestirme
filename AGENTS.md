# Repository Guidelines

## Project Structure & Module Organization

This repository is a biomass pyrolysis and bio-oil ML research workspace. The main implementation area is `reverse_ml_biooil_to_product/`, with Aspen automation in `automation_scripts/`, Cantera generation in `cantera_generation/`, ML pipelines in `ml_models/` and `ml_reverse_prediction/`, and reformer-only workflows in `reformer_only_model/`. Legacy or supporting Python work lives in `python_codes/`, including model outputs and processed data. Review-paper projects are organized separately in `RSER_Review_Paper/` and `COMPOSITION_DATA_REVIEW_Paper/`. Literature PDFs, Word documents, figures, and presentation assets are stored in topic folders such as `biyyag_ftir/`, `biooilml/`, `form_foto/`, and root-level report files.

## Build, Test, and Development Commands

Use Python 3.8+ unless a subproject documents stricter requirements. Create a virtual environment outside tracked files or use `.venv/`, which is ignored.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r reverse_ml_biooil_to_product\automation_scripts\requirements.txt
pip install -r reverse_ml_biooil_to_product\cantera_generation\requirements.txt
```

Key scripts:

```powershell
python reverse_ml_biooil_to_product\automation_scripts\test_connection.py
python reverse_ml_biooil_to_product\cantera_generation\generate_data_cantera.py
python reverse_ml_biooil_to_product\ml_models\data_preparation.py
python reverse_ml_biooil_to_product\ml_models\train_models.py
python RSER_Review_Paper\compile_manuscript.py
```

Run commands from the repository root unless a README in the target folder says otherwise.

## Coding Style & Naming Conventions

Prefer clear Python modules with `snake_case` filenames, functions, and variables. Keep configuration in existing `config/` modules rather than hard-coding paths or database settings inside scripts. Use 4-space indentation, concise comments for non-obvious scientific assumptions, and explicit column names for datasets. Preserve existing numbered workflow names such as `02_reformer_simulator.py` when extending staged pipelines.

## Testing Guidelines

There is no centralized test suite yet. Treat executable checks as project tests: run connection checks before Aspen automation, run Cantera generation on a small sample before full data generation, and verify ML scripts complete without changing committed datasets unexpectedly. Name future tests `test_*.py` and colocate them near the module they validate or under a future `tests/` directory.

## Commit & Pull Request Guidelines

Recent commits use short Turkish summaries, for example `sunuma hazir` and `RSER review paper ilerleme dokumani ve literatur dosyalari eklendi`. Keep commit messages brief, imperative or descriptive, and scoped to one logical change. Pull requests should summarize the research/code change, list scripts run, mention data or document assets added, and include screenshots only when figures, diagrams, or manuscript formatting changed.

## Security & Configuration Tips

Do not commit local databases, model binaries, generated CSV/XLSX outputs, logs, or virtual environments; `.gitignore` already excludes these. Keep SQL Server and Aspen machine-specific settings in config files or local notes, and avoid adding credentials beyond Windows-auth connection examples.
