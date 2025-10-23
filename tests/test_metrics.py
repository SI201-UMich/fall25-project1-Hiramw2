import os
import json
from output import main as m


def test_csv_exists():
    path = m.csv_filepath()
    assert os.path.exists(path), f"CSV not found at {path}"


def test_metrics_ranges():
    data = m.load_data(m.csv_filepath())
    assert m.calculate_avg_flipper_length(data) > 180
    assert m.calculate_avg_body_mass(data) > 3000


def test_male_pct_and_species_yield():
    data = m.load_data(m.csv_filepath())
    male_pct = m.calculate_male_percentage(data)
    species_yield = m.calculate_species_yield(data)
    assert 40 <= male_pct <= 60
    assert "Gentoo" in species_yield
    assert "Adelie" in species_yield


def test_write_results(tmp_path):
    data = m.load_data(m.csv_filepath())
    results = {
        "Average Flipper Length (mm)": m.calculate_avg_flipper_length(data),
        "Average Body Mass (g)": m.calculate_avg_body_mass(data),
        "Male Percentage": m.calculate_male_percentage(data),
        "Species Yield": m.calculate_species_yield(data),
    }
    txt = tmp_path / "results.txt"
    jsonp = tmp_path / "results.json"
    m.write_results(results, str(txt))
    m.write_results_json(results, str(jsonp))
    assert txt.exists()
    assert jsonp.exists()
    # JSON should parse
    with open(jsonp, 'r') as f:
        parsed = json.load(f)
    assert "Average Flipper Length (mm)" in parsed
