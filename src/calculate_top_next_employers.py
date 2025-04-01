import pandas as pd
import ast

def calculate_top_next_employers(df_raw):
    data = []

    for _, row in df_raw.iterrows():
        domain_name = row['domain_name']
        created_at = row['created_at']

        # Parse the JSON-like strings in the columns
        try:
            prev_employers = ast.literal_eval(row['top_previous_employers_by_role'])
            next_employers = ast.literal_eval(row['top_next_employers_by_role'])
        except (ValueError, SyntaxError):
            continue

        # Calculate role-wise sums for previous and next employers
        prev_sums = {role: sum(employees.values()) for role, employees in prev_employers.items()}
        next_sums = {role: sum(employees.values()) for role, employees in next_employers.items()}

        # Calculate percent increase for each role
        for role in prev_sums.keys():
            prev_sum = prev_sums.get(role, 0)
            next_sum = next_sums.get(role, 0)

            # Avoid division by zero
            if prev_sum == 0:
                continue

            percent_increase = ((next_sum - prev_sum) / prev_sum) * 100
            data.append({
                'created_at': created_at,
                'domain_name': domain_name,
                'role': role,
                'percent_increase': percent_increase
            })

    # Create the final DataFrame
    top_next_employers_by_org = pd.DataFrame(data)
    return top_next_employers_by_org
