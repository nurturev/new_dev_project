import pandas as pd
import ast

def process_employee_growth(df_raw):
    data = []

    for _, row in df_raw.iterrows():
        domain_name = row['domain_name']

        # Safely evaluate the string to convert it into a dictionary
        try:
            monthly_data = ast.literal_eval(row['employee_count_by_month'])
        except (ValueError, SyntaxError):
            # Skip rows with invalid data
            continue

        # Convert the monthly data into a DataFrame
        monthly_df = pd.DataFrame(list(monthly_data.items()), columns=['month', 'employee_count'])
        monthly_df['month'] = pd.to_datetime(monthly_df['month'], format='%Y-%m')
        monthly_df['quarter'] = monthly_df['month'].dt.to_period('Q')

        # Group by quarters and calculate percent increase
        for quarter, group in monthly_df.groupby('quarter'):
            first_month_count = group.iloc[0]['employee_count']
            last_month_count = group.iloc[-1]['employee_count']
            percent_increase = ((last_month_count - first_month_count) / first_month_count) * 100

            # Append data for the new DataFrame
            data.append({
                'created_at': group.iloc[-1]['month'],  # Use the last month's date as created_at
                'domain_name': domain_name,
                'quarter': str(quarter),
                'percent_increase': percent_increase
            })

    # Create the final DataFrame
    employee_growth_per_quarter = pd.DataFrame(data)
    return employee_growth_per_quarter
