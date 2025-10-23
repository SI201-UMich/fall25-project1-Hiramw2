# Name: Hiram Williams
# Student ID: 26065490
# Email: hiramw@umich.edu 
# AI Tools Used: Microsoft Copilot for debugging and help with questions when my code was not working as expected.


import csv
import os
import sys
import argparse
import json
import logging

def csv_filepath():
    """Return path to penguins.csv. Prefer local data/penguins.csv, fall back to ../Project/data/penguins.csv."""
    base = os.path.dirname(__file__)
    local = os.path.join(base, "data", "penguins.csv")
    fallback = os.path.join(base, "..", "Project", "data", "penguins.csv")
    if os.path.exists(local):
        return local
    return os.path.normpath(fallback)
def load_data(filename):
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

def calculate_avg_flipper_length(data):
    lengths = []
    for row in data:
        value = row['flipper_length_mm']
        if value and value != 'NA':
            lengths.append(float(value))
    return round(sum(lengths) / len(lengths), 2) if lengths else 0

def calculate_avg_body_mass(data):
    masses = []
    for row in data:
        value = row['body_mass_g']
        if value and value != 'NA':
            masses.append(float(value))
    return round(sum(masses) / len(masses), 2) if masses else 0







# def calculate_male_percentage(data):
def calculate_male_percentage(data):
    """
    Return the percentage of penguins that are male (0–100), excluding rows with missing sex.
    """
    males = 0
    known = 0
    for row in data:
        sex = row.get('sex')
        if sex and sex != 'NA':
            known += 1
            if sex.strip().lower() == 'male':
                males += 1
    return round((males / known) * 100, 2) if known else 0


# def calculate_species_yield(data):


def calculate_species_yield(data):
    """
    For each species, return the percentage of penguins with body mass > 5000g.
    """
    species_stats = {}  # species -> [num_heavy, total]
    for row in data:
        species = row.get('species')
        mass = row.get('body_mass_g')

        if not species or species == 'NA' or not mass or mass == 'NA':
            continue

        try:
            mass = float(mass)
        except ValueError:
            continue

        if species not in species_stats:
            species_stats[species] = [0, 0]

        species_stats[species][1] += 1
        if mass > 5000:
            species_stats[species][0] += 1

    return {
        species: round((heavy / total) * 100, 2) if total else 0
        for species, (heavy, total) in species_stats.items()
    }
def run_tests(data):
    print("Running test cases...")

  
    assert calculate_avg_flipper_length(data) > 180
    assert calculate_avg_body_mass(data) > 3000

    empty_data = []
    assert calculate_avg_flipper_length(empty_data) == 0 if empty_data else True
    assert calculate_avg_body_mass(empty_data) == 0 if empty_data else True


   

# Note: No top-level execution here so this module can be imported by tests.
def write_results_json(results, filename):
    """Write results dict to filename as JSON."""
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Compute penguin statistics and write results.")
    p.add_argument("--data", help="Path to penguins.csv (overrides default lookup)")
    # default outdir: repo-level 'output' directory (one level up from this script)
    default_out = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "output"))
    p.add_argument("--outdir", default=default_out,
                   help=f"Directory to write results (default: {default_out})")
    p.add_argument("--no-tests", action="store_true", help="Do not run internal tests")
    return p.parse_args(argv)


def main(argv=None):
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = parse_args(argv)

    # determine CSV path
    data_path = args.data if args.data else csv_filepath()
    if not os.path.exists(data_path):
        logging.error("Data file not found: %s", data_path)
        sys.exit(1)

    data = load_data(data_path)

    avg_flipper = calculate_avg_flipper_length(data)
    avg_mass = calculate_avg_body_mass(data)

    # SECTION FOR DONOVAN
    male_pct = calculate_male_percentage(data)
    species_yield_pct = calculate_species_yield(data)

    results = {
        "Average Flipper Length (mm)": avg_flipper,
        "Average Body Mass (g)": avg_mass,
        "Male Percentage": male_pct,
        "Species Yield": species_yield_pct,
        "Data File": os.path.abspath(data_path),
    }

    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)
    txt_path = os.path.join(outdir, "results.txt")
    json_path = os.path.join(outdir, "results.json")

    write_results(results, txt_path)
    write_results_json(results, json_path)

    logging.info("Wrote results to %s and %s", txt_path, json_path)

    if not args.no_tests:
        try:
            run_tests(data)
        except AssertionError as e:
            logging.error("Tests failed: %s", e)
            sys.exit(2)

def write_results(results, filename):
    """
    Write the results dictionary to a file, one key-value pair per line.
    """
    def format_value(v):
        if isinstance(v, dict):
            # pretty-print nested dicts
            lines = []
            for k, val in v.items():
                lines.append(f"  {k}: {val}")
            return "\n" + "\n".join(lines)
        return str(v)

    with open(filename, "w") as f:
        for key, value in results.items():
            f.write(f"{key}: {format_value(value)}\n")

if __name__ == "__main__":
    main()
