import pandas as pd
import ast

def process_employee_growth_by_role(df_raw):
    data = []

    for _, row in df_raw.iterrows():
        domain_name = row['domain_name']

        # Parse the nested dictionary safely
        try:
            monthly_data = ast.literal_eval(row['employee_count_by_month_by_role'])
        except (ValueError, SyntaxError):
            continue

        # Convert the monthly data into a DataFrame
        monthly_df = pd.DataFrame.from_dict(monthly_data, orient='index')
        monthly_df.index = pd.to_datetime(monthly_df.index, format='%Y-%m')  # Convert to datetime
        monthly_df['quarter'] = monthly_df.index.to_period('Q')  # Add quarter information

        # Process data for each role
        for role in monthly_df.columns.difference(['quarter']):  # Exclude non-role columns
            role_data = monthly_df[['quarter', role]].rename(columns={role: 'employee_count'})

            # Group by quarter and calculate percent increase
            for quarter, group in role_data.groupby('quarter'):
                first_month_count = group.iloc[0]['employee_count']
                last_month_count = group.iloc[-1]['employee_count']

                if first_month_count == 0:  # Avoid division by zero
                    continue

                percent_increase = ((last_month_count - first_month_count) / first_month_count) * 100

                # Append data for the new DataFrame
                data.append({
                    'created_at': group.index[-1],  # Use the last month's date as created_at
                    'domain_name': domain_name,
                    'role': role,
                    'quarter': str(quarter),
                    'percent_increase': percent_increase
                })

    # Create the final DataFrame
    employee_growth_per_role_per_quarter = pd.DataFrame(data)
    return employee_growth_per_role_per_quarter
