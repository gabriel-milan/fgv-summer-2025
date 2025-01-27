"""
Script to generate sample data for testing
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Generate sample data
n_rows = 1000

# Generate random dates within the last year
end_date = datetime.now()
start_date = end_date - timedelta(days=365)
dates = [start_date + timedelta(days=x) for x in range(n_rows)]

data = {
    "id": range(1, n_rows + 1),
    "name": [f"Person_{i}" for i in range(n_rows)],
    "age": np.random.randint(18, 80, n_rows),
    "salary": np.random.uniform(30000, 120000, n_rows).round(2),
    "department": np.random.choice(
        ["HR", "IT", "Sales", "Marketing", "Finance"], n_rows
    ),
    "is_active": np.random.choice([True, False], n_rows),
    "hire_date": dates,
    "performance_score": np.random.uniform(1, 5, n_rows).round(1),
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
output_file = "data/sample_employees.csv"
df.to_csv(output_file, index=False)

# Save to Parquet
df.to_parquet(output_file.replace(".csv", ".parquet"))

print(f"Generated {output_file} with {n_rows} rows")
print("\nFirst few rows:")
print(df.head())
print("\nData types:")
print(df.dtypes)
