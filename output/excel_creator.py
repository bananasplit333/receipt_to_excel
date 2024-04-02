import xlsxwriter

def create_excel_sheet(json_obj, file_path):
    # Create a workbook and add a worksheet
    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet()

    # Set column widths and define formats
    worksheet.set_column('A:A', 20)
    worksheet.set_column('B:B', 50)
    worksheet.set_column('C:C', 20)
    bold = workbook.add_format({'bold': True})
    currency_format = workbook.add_format({'num_format': '$#,##0.00'})

    # Write headers to the worksheet
    worksheet.write('A1', 'Expense Budget', bold)
    worksheet.write('A2', 'Item', bold)
    worksheet.write('B2', 'Cost', bold)
    worksheet.write('C2', 'Category', bold)

    # Initialize row and category totals variables
    row = 2
    category_totals = {}
    grand_total = 0

    # Iterate over JSON data and write to the worksheet
    for category, items in json_obj.items():
        category_totals[category] = 0
        for item in items:
            worksheet.write(row, 0, item['name'])
            worksheet.write(row, 1, item['price'], currency_format)
            worksheet.write(row, 2, category)
            row += 1
            category_totals[category] += item['price']
            grand_total += item['price']

    # Write category totals to the worksheet
    for category, total in category_totals.items():
        worksheet.write(row, 1, f"Total for {category}", bold)
        worksheet.write(row, 2, total, currency_format)
        row += 1

    # Write the grand total to the worksheet
    worksheet.write(row, 1, "Grand Total", bold)
    worksheet.write(row, 2, grand_total, currency_format)

    # Close the workbook to flush the data to the output stream
    workbook.close()