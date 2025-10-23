# Penguin Stats (Project 1)

Minimal instructions to run the analysis and tests.

Run the script (auto-detects data in `Project/data/penguins.csv`):

```bash
python3 output/main.py
```

Specify data and output directory:

```bash
python3 output/main.py --data Project/data/penguins.csv --outdir output
```

Skip internal assertions/tests:

```bash
python3 output/main.py --no-tests
```

Run tests (requires pytest):

```bash
pip install pytest
pytest -q
```
