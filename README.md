# Time-Series Aggregator

A **command-line Python utility** for time-series data analysis.  
Supports flexible time grouping, multiple sensors, customizable statistical aggregations, and CSV output for reporting.

---

## Features

- **Flexible Time Grouping** – Hourly, daily, weekly, monthly, or custom intervals like 30 minutes, 5 minutes, or even 10 seconds.  
- **Multiple Sensor Support** – Aggregate any number of sensor columns from your CSV file.  
- **Custom Statistics** – Calculate `mean`, `min`, `max`, `median`, `mode`.  
- **Readable Output** – Prints tables in the terminal and saves results to CSV.  
- **Handles Missing Data Gracefully** – Ignores NaNs in calculations.  

---

## Installation

1. Install [Python 3.9+](https://www.python.org/downloads/)  
2. Install required dependencies:

## bash
pip install pandas numpy scipy

## Run the Python script from the command line:

python data_aggregator.py --input sensor_data.csv --group-by 30T --stats min --columns PH_DAC02_Humidity PH_DAC02_Temperature
