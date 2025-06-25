from pathlib import Path
from pipeline.database import setup_database
from pipeline.stats_tracker import process_file, get_stats

# Direcotory containing input CSV files
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def print_current_stats():
    count, avg, min_p, max_p = get_stats()
    if any(v is None for v in [count, avg, min_p, max_p]):
        print("Statistics incomplete: not enough data.")
    else:
        print(f"Count: {count} | Avg Price: {avg:.2f} | Min Price: {min_p} | Max Price: {max_p}")

def main():
    setup_database()

    #Get all CSV files except validation
    input_files = sorted(
        f for f in DATA_DIR.glob("*.csv") if f.name != "validation.csv"
    )

    # Process each input file incrementally
    for file_path in input_files:
        process_file(file_path)
        print(f"Processed: {file_path.name}")
        print_current_stats()

    # Process the validation file separately at end
    print("\n--- Validation ---")
    validation_file = DATA_DIR / "validation.csv"
    if validation_file.exists():
        process_file(validation_file)
        print("Processed: validation.csv")
        print_current_stats()
    else:
        print("No validation.csv file found")

if __name__ == "__main__":
    main()