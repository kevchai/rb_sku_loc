import pandas as pd
import tabula
import os


def process_pdf_and_excel(pdf_path, excel_path, output_csv_path):
    # Read data from PDF
    pdf_data = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)

    # Assuming the table of interest is in the first table extracted from the PDF
    pdf_table = pdf_data[0]

    # Convert pdf_table column names to lowercase
    pdf_table.columns = pdf_table.columns.str.lower()

    print("Columns in pdf_table:", pdf_table.columns)

    # Check if the Excel file exists before attempting to read it
    if os.path.exists(excel_path):
        # Read data from Excel
        excel_data = pd.read_excel(excel_path, header=None)

        print("Rows and columns in excel_data:", excel_data.shape)

        # Ensure 'SKU', 'Qty', 'Product Title', and 'Location' are present in excel_data
        required_columns = ['sku', 'qty', 'product title', 'location']

        for col in required_columns:
            if col not in excel_data.iloc[0].tolist():
                print(f"Adding column '{col}' to excel_data.")
                excel_data = pd.concat([excel_data, pd.DataFrame(columns=[col])], axis=1)

        # Concatenate DataFrames vertically
        merged_data = pd.concat([pdf_table, excel_data], axis=0, ignore_index=True)

        # Write the result to CSV
        merged_data.to_csv(output_csv_path, index=False)
    else:
        print(f"Error: Excel file '{excel_path}' not found.")


# Replace file paths with your actual file paths
process_pdf_and_excel('Print SKU Summary.pdf', 'sku_locations.xls', 'output_sku_summary.csv')