# Name: Hiram Williams
# Student ID: 26065490
# Email: hiramw@umich.edu 
# AI Tools Used: Microsoft Copilot for debugging and help with questions


import csv
import os

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


   

data = load_data(csv_filepath())
male_pct = calculate_male_percentage(data)
species_yield = calculate_species_yield(data)

# Around half the penguins are male; expect between 40% and 60%
assert 40 <= male_pct <= 60, f"Unexpected male percentage: {male_pct}"

# Expect Gentoo to have the highest % >5000 g, Adelie the lowest
assert "Gentoo" in species_yield and species_yield["Gentoo"] > 40
assert "Adelie" in species_yield and species_yield["Adelie"] < 10
assert "Chinstrap" in species_yield

print("All tests passed.")

def main():
    data = load_data(csv_filepath())

    avg_flipper = calculate_avg_flipper_length(data)
    avg_mass = calculate_avg_body_mass(data)

    
    # SECTION FOR DONOVAN
    male_pct = calculate_male_percentage(data)
    species_yield_pct = calculate_species_yield(data)
        
    results = {
        "Average Flipper Length (mm)": avg_flipper,
        "Average Body Mass (g)": avg_mass,
        "Male Percentage": male_pct,
         "Species Yield ": species_yield_pct
    }
        
    write_results(results, "output/results.txt")
    run_tests(data)

def write_results(results, filename):
    """
    Write the results dictionary to a file, one key-value pair per line.
    """
    with open(filename, "w") as f:
        for key, value in results.items():
            f.write(f"{key}: {value}\n")

if __name__ == "__main__":
    main()
