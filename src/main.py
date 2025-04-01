from data_loader import load_data_from_s3
from process_employee_growth import process_employee_growth
from process_employee_growth_by_role import process_employee_growth_by_role
from calculate_top_next_employers import calculate_top_next_employers
from calculate_yoy_growth import calculate_yoy_growth

def main():
    df_raw = load_data_from_s3()

    employee_growth_per_quarter = process_employee_growth(df_raw)
    employee_growth_per_role_per_quarter = process_employee_growth_by_role(df_raw)
    top_next_employers_by_org = calculate_top_next_employers(df_raw)
    output_df = calculate_yoy_growth(df_raw)

    print("Processing Complete")

if __name__ == "__main__":
    main()
