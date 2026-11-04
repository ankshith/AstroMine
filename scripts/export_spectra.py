"""Convert raw SMASS-II .tab spectra to long-form CSV for exploration.

Usage:
    python scripts/export_spectra.py /path/to/extracted/smassii spectral_points.csv

No AWS calls, taxonomy joins, interpolation or model training are performed.
"""
import argparse
import csv
from pathlib import Path


def export_spectra(source: Path, output: Path) -> tuple[int, int]:
    files = sorted(source.rglob("*.tab"))
    if not files:
        raise FileNotFoundError(f"No .tab spectral files found under {source}")
    output.parent.mkdir(parents=True, exist_ok=True)
    nrows = 0
    with output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["spectrum_id", "wavelength_um", "reflectance", "uncertainty"])
        for path in files:
            for lineno, line in enumerate(path.read_text(encoding="ascii", errors="replace").splitlines(), 1):
                parts = line.split()
                if not parts:
                    continue
                if len(parts) != 3:
                    raise ValueError(f"Expected three columns at {path}:{lineno}")
                writer.writerow([path.relative_to(source).as_posix(), *(float(value) for value in parts)])
                nrows += 1
    return len(files), nrows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    files, rows = export_spectra(args.source, args.output)
    print(f"Exported {rows:,} rows from {files:,} files")
