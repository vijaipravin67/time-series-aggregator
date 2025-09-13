import argparse
import pandas as pd
import numpy as np
from scipy import stats

def load_data(file_path, datetime_format=None):
    """Load CSV/Excel file and detect datetime column."""
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Use CSV or Excel.")

    # Detect datetime column automatically
    datetime_cols = [col for col in df.columns if "time" in col.lower() or "date" in col.lower()]
    if not datetime_cols:
        raise ValueError("No datetime column found in the input file.")
    
    datetime_col = datetime_cols[0]

    # Parse datetime column
    try:
        if datetime_format:
            df[datetime_col] = pd.to_datetime(df[datetime_col], format=datetime_format, errors="coerce")
        else:
            df[datetime_col] = pd.to_datetime(df[datetime_col], errors="coerce")
    except Exception as e:
        raise ValueError(f"Failed to parse datetime column: {e}")

    df.rename(columns={datetime_col: "timestamp"}, inplace=True)

    # print(f"Using datetime column: {datetime_col}")
    # print("Available columns:", df.columns.tolist())
    return df


def aggregate_data(df, group_by, stats_list, columns=None, time_from=None, time_to=None):
    """Group time-series data and compute statistics."""

    # Filter by time range if provided
    if time_from:
        df = df[df["timestamp"] >= pd.to_datetime(time_from, unit="ms")]
    if time_to:
        df = df[df["timestamp"] <= pd.to_datetime(time_to, unit="ms")]

    df = df.set_index("timestamp")

    # Select only specified columns (validate existence)
    if columns:
        missing = [col for col in columns if col not in df.columns]
        if missing:
            print(f"ERROR: The following columns were not found: {missing}")
            print("Available columns are:", df.columns.tolist())
            sys.exit(1)
        df = df[columns]

    # Define aggregation mapping
    agg_funcs = {}
    for col in df.select_dtypes(include=[np.number]).columns:
        func_list = []
        if "min" in stats_list: func_list.append("min")
        if "max" in stats_list: func_list.append("max")
        if "mean" in stats_list: func_list.append("mean")
        if "median" in stats_list: func_list.append("median")
        if "mode" in stats_list:
            func_list.append(lambda x: stats.mode(x, nan_policy='omit').mode[0] if len(x) > 0 else np.nan)
        agg_funcs[col] = func_list

    # Perform aggregation
    result = df.resample(group_by.lower()).agg(agg_funcs)

    # Flatten column MultiIndex if multiple stats
    result.columns = ['_'.join([str(c) for c in col if c]) for col in result.columns]

    return result.reset_index()


def main():
    parser = argparse.ArgumentParser(description="Time-Series Data Aggregator")
    parser.add_argument("--input", required=True, help="Path to input CSV/Excel file")
    parser.add_argument("--group-by", required=True, help="Grouping interval (e.g., 1h, 1d, 30T, 10s)")
    parser.add_argument("--stats", nargs="+", default=["mean"], help="Stats to compute: min max mean median mode")
    parser.add_argument("--columns", nargs="*", help="Columns to include (default: all numeric)")
    parser.add_argument("--timefrom", type=int, help="Start timestamp (ms since epoch)")
    parser.add_argument("--timeto", type=int, help="End timestamp (ms since epoch)")
    parser.add_argument("--datetime-format", help="Optional datetime format string for parsing")
    parser.add_argument("--output", default="aggregated_output.csv", help="Output CSV file path")

    args = parser.parse_args()

    df = load_data(args.input, args.datetime_format)
    result = aggregate_data(
        df,
        group_by=args.group_by,
        stats_list=args.stats,
        columns=args.columns,
        time_from=args.timefrom,
        time_to=args.timeto
    )

    print(result.head())
    result.to_csv(args.output, index=False)
    print(f"Aggregated data saved to {args.output}")


if __name__ == "__main__":
    main()
