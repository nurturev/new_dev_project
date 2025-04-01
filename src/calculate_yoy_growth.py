import pandas as pd
import json

def calculate_yoy_growth(row):
    # Skip rows with missing or invalid data in 'employee_count_by_month_by_level'
    if pd.isnull(row['employee_count_by_month_by_level']):
        return []

    try:
        # Fix single quotes in JSON
        raw_counts = row['employee_count_by_month_by_level'].replace("'", '"')
        counts = json.loads(raw_counts)
    except (json.JSONDecodeError, AttributeError):
        return []  # Skip rows with invalid JSON

    # Aggregate yearly data
    yearly_data = {}
    for month, levels in counts.items():
        year = month.split('-')[0]
        if year not in yearly_data:
            yearly_data[year] = {}
        for level, count in levels.items():
            yearly_data[year][level] = yearly_data[year].get(level, 0) + count

    # Calculate YoY growth
    results = []
    sorted_years = sorted(yearly_data.keys())
    for i in range(1, len(sorted_years)):
        curr_year, prev_year = sorted_years[i], sorted_years[i - 1]
        for level in yearly_data[curr_year]:
            if level in yearly_data[prev_year]:
                prev_count = yearly_data[prev_year][level]
                curr_count = yearly_data[curr_year][level]
                if prev_count > 0:  # Avoid division by zero
                    percent_increase = ((curr_count - prev_count) / prev_count) * 100
                    results.append({
                        "created_at": row["created_at"],
                        "domain_name": row["domain_name"],
                        "level": level,
                        "year": curr_year,
                        "percent_increase": percent_increase
                    })
    return results

# Apply the function and combine results
results = []
for _, row in df_raw.iterrows():
    results.extend(calculate_yoy_growth(row))

# Convert results to DataFrame
output_df = pd.DataFrame(results)
return output_df
