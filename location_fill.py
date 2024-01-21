import pandas as pd
import tabula
import os

def process_pdf_and_excel(pdf_path, excel_path, output_xlsx_path):
    # Read data from PDF
    pdf_data = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)

    # Assuming the table of interest is in the first table extracted from the PDF
    pdf_table = pdf_data[0]

    # Convert pdf_table column names to lowercase
    pdf_table.columns = pdf_table.columns.str.lower()

    # Read data from Excel
    if os.path.exists(excel_path):
        excel_data = pd.read_excel(excel_path)

        # Convert 'sku' column to the same data type (object) in both tables
        pdf_table['sku'] = pdf_table['sku'].astype(str)
        excel_data['sku'] = excel_data['sku'].astype(str)

        # Merge data based on 'sku'
        merged_data = pd.merge(pdf_table, excel_data, on='sku', how='left')

        # Fill empty 'location' in the PDF table with values from 'location' in Excel
        merged_data['location_x'].fillna(merged_data['location_y'], inplace=True)

        # Drop unnecessary columns from the result
        merged_data.drop(['location_y'], axis=1, inplace=True)

        # Rename the merged 'location_x' column to 'location'
        merged_data.rename(columns={'location_x': 'location'}, inplace=True)

        # Drop rows where 'sku' contains the string 'nan'
        merged_data = merged_data[~merged_data['sku'].str.lower().eq('nan')]

        # Drop the 'product title' column
        merged_data.drop(['product title'], axis=1, inplace=True)

        # Sort by the 'location' column
        merged_data.sort_values(by='location', inplace=True)

        # Write the result to Excel
        merged_data.to_excel(output_xlsx_path, index=False)
    else:
        print(f"Error: Excel file '{excel_path}' not found.")

# Replace file paths with your actual file paths
process_pdf_and_excel('Print SKU Summary.pdf', 'sku_locations.xlsx', 'output_sku_summary.xlsx')
