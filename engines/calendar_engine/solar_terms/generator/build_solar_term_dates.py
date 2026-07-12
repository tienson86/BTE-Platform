"""
===============================================================================
Build Solar Term Dates
-------------------------------------------------------------------------------
Sinh dữ liệu solar_term_dates.csv từ bảng ngày chuẩn.

Version : V1.0

V1.0
-----
Sử dụng ngày chuẩn (Base Dates).

V2.0
-----
Thay bằng thuật toán thiên văn Jean Meeus.

Output
------
solar_term_dates.csv
===============================================================================
"""

from __future__ import annotations

import csv
from pathlib import Path


# =============================================================================
# PATH
# =============================================================================

CURRENT_DIR = Path(__file__).resolve().parent

DATA_DIR = CURRENT_DIR.parent / "data"

BASE_FILE = DATA_DIR / "solar_term_base_dates.csv"

OUTPUT_FILE = DATA_DIR / "solar_term_dates.csv"


# =============================================================================
# CONFIG
# =============================================================================

START_YEAR = 1900

END_YEAR = 2100


DEFAULT_TIME = "12:00:00"


# =============================================================================
# LOAD BASE DATA
# =============================================================================


def load_base_dates():

    items = []

    with open(
        BASE_FILE,
        "r",
        encoding="utf-8-sig",
    ) as f:

        reader = csv.DictReader(f)

        for row in reader:

            items.append(row)

    return items


# =============================================================================
# BUILD
# =============================================================================


def build():

    base_dates = load_base_dates()

    rows = []

    record_id = 1

    for year in range(
        START_YEAR,
        END_YEAR + 1,
    ):

        for item in base_dates:

            rows.append(
                {
                    "id": record_id,
                    "year": year,
                    "term_index": item["term_index"],
                    "code": item["code"],
                    "term_name": item["term_name"],
                    "month": item["month"],
                    "day": item["day"],
                    "date": f"{year}-{int(item['month']):02d}-{int(item['day']):02d}",
                    "time": DEFAULT_TIME,
                    "datetime": (
                        f"{year}-"
                        f"{int(item['month']):02d}-"
                        f"{int(item['day']):02d} "
                        f"{DEFAULT_TIME}"
                    ),
                    "solar_longitude": item["longitude"],
                    "is_major": item["is_major"],
                }
            )

            record_id += 1

    return rows


# =============================================================================
# SAVE
# =============================================================================


def save(rows):

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "id",
                "year",
                "term_index",
                "code",
                "term_name",
                "month",
                "day",
                "date",
                "time",
                "datetime",
                "solar_longitude",
                "is_major",
            ],
        )

        writer.writeheader()

        writer.writerows(rows)


# =============================================================================
# MAIN
# =============================================================================


def main():

    print("=" * 70)

    print("Building solar_term_dates.csv ...")

    rows = build()

    save(rows)

    print(f"Records : {len(rows)}")

    print(f"Output  : {OUTPUT_FILE}")

    print("Done.")

    print("=" * 70)


if __name__ == "__main__":

    main()
