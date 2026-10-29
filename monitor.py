"""Generate a local Evidently data-drift report using synthetic UAT data.

This is a repeatable configuration smoke test, not a production monitoring feed.
Replace the reference/current DataFrames with approved UAT/production extracts
when real monitoring data becomes available.
"""

from pathlib import Path

import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset


def build_demo_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (current_data, reference_data) with deliberate distribution shift."""
    reference_data = pd.DataFrame(
        {
            "age": [21, 23, 24, 25, 26, 22, 27, 24, 28, 23, 25, 26,
                    22, 24, 27, 21, 23, 25, 26, 28, 22, 24, 27, 23,
                    25, 26, 21, 24, 28, 22],
            "monthly_spend": [800, 950, 1100, 900, 1200, 850, 1050, 980, 1300, 920,
                              1150, 1000, 870, 1080, 1250, 890, 970, 1120, 1040, 1280,
                              860, 1090, 1230, 940, 1170, 1020, 880, 1060, 1320, 910],
            "region": ["West", "East", "West", "North", "East", "South", "West", "East",
                       "North", "West", "South", "East", "West", "North", "East", "South",
                       "West", "East", "North", "West", "South", "East", "West", "North",
                       "East", "South", "West", "East", "North", "West"],
        }
    )

    current_data = pd.DataFrame(
        {
            "age": [34, 38, 41, 36, 45, 39, 43, 35, 48, 40, 37, 44,
                    42, 36, 47, 39, 41, 46, 35, 43, 38, 45, 40, 49,
                    37, 42, 44, 36, 46, 39],
            "monthly_spend": [1800, 2100, 1950, 2300, 2500, 2050, 2200, 1900, 2700, 2150,
                              2000, 2400, 2250, 1850, 2600, 2080, 2350, 2550, 1920, 2180,
                              2030, 2450, 2120, 2800, 1980, 2280, 2380, 1880, 2580, 2060],
            "region": ["Central", "Central", "South", "Central", "Central", "West", "Central", "South",
                       "Central", "Central", "South", "Central", "Central", "West", "Central", "South",
                       "Central", "Central", "Central", "South", "Central", "Central", "West", "Central",
                       "Central", "South", "Central", "Central", "Central", "South"],
        }
    )
    return current_data, reference_data


def main() -> None:
    """Create an HTML drift report and JSON snapshot under reports/."""
    output_dir = Path("reports")
    output_dir.mkdir(parents=True, exist_ok=True)

    current_data, reference_data = build_demo_data()
    report = Report([DataDriftPreset()])
    snapshot = report.run(current_data, reference_data)

    html_path = output_dir / "evidently_data_drift.html"
    json_path = output_dir / "evidently_data_drift.json"
    snapshot.save_html(str(html_path))
    json_path.write_text(snapshot.json(), encoding="utf-8")

    print("Evidently monitoring smoke test completed.")
    print(f"Reference rows: {len(reference_data)}")
    print(f"Current rows:   {len(current_data)}")
    print(f"HTML report:    {html_path.resolve()}")
    print(f"JSON snapshot:  {json_path.resolve()}")
    print("Note: synthetic sample data is used; this is not a production alerting service.")


if __name__ == "__main__":
    main()
