import os
from pathlib import Path
from pipeline.database import setup_database
from pipeline.stats_tracker import process_file, get_stats

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def main():
    setup_database()
    files = sorted([f for f in os.listdir(DATA_DIR) if f.endswith(".csv") and not f.startswith("validation")])
    for fname in files:
        process_file(DATA_DIR / fname)
        print(f"Processed: {fname}")
        print_current_stats()

    # Ahora procesamiento del archivo de validación
    print("\n--- Validación ---")
    process_file(DATA_DIR / "validation.csv")
    print("Processed: validation.csv")
    print_current_stats()

def print_current_stats():
    count, avg, min_p, max_p = get_stats()
    print(f"Count: {count} | Avg Price: {avg:.2f} | Min Price: {min_p} | Max Price: {max_p}")

if __name__ == "__main__":
    main()
