import pandas as pd
import tabula


# Function to read PDF and Excel, merge data, and write to CSV
def process_pdf_and_excel(pdf_path, excel_path, output_csv_path):
    # Read data from PDF
    pdf_data = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)

    # Assuming the table of interest is in the first table extracted from the PDF
    pdf_table = pdf_data[0]

    # Read data from Excel
    excel_data = pd.read_excel(excel_path)

    # Merge data based on SKU
    merged_data = pd.merge(pdf_table, excel_data, on='SKU', how='left')

    # Drop the original 'Location' column from the PDF table
    merged_data.drop('Location_x', axis=1, inplace=True)

    # Rename the 'Location_y' column to 'Location'
    merged_data.rename(columns={'Location_y': 'Location'}, inplace=True)

    # Write the result to CSV
    merged_data.to_csv(output_csv_path, index=False)


# Replace 'your_pdf_file.pdf', 'your_excel_file.xlsx', and 'output_result.csv' with your actual file paths
process_pdf_and_excel('sku_summary.pdf', 'sku_locations.csv', 'output_sku_summary.csv')
