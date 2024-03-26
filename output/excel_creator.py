import xlsxwriter

def create_excel_sheet(json_obj):
    workbook = xlsxwriter.Workbook('expenses.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.set_column('A:A', 20)
    worksheet.set_column('B:B', 50)
    worksheet.set_column('C:C', 20)

    bold = workbook.add_format({'bold': True})
    currency_format = workbook.add_format({'num_format': '$#,##0.00'})

    worksheet.write('A1', 'Expense Budget', bold)
    worksheet.write('A2', 'Item', bold)
    worksheet.write('B2', 'Cost', bold)
    worksheet.write('C2', 'Category', bold)

    row = 2
    category_totals = {}
    grand_total = 0

    for category, items in json_obj.items():
        # Initialize the total for each category to 0
        category_totals[category] = 0
        for item in items:
            worksheet.write(row, 0, item['name'])
            worksheet.write(row, 1, item['price'], currency_format)
            worksheet.write(row, 2, category)
            row += 1
            category_totals[category] += item['price']
            grand_total += item['price']

    # Write category totals
    for category, total in category_totals.items():
        worksheet.write(row, 1, f"Total for {category}", bold)
        worksheet.write(row, 2, total, currency_format)  # Apply currency format
        row += 1

    # Write the grand total
    worksheet.write(row, 1, "Grand Total", bold)
    worksheet.write(row, 2, grand_total, currency_format)  # Apply currency format

    workbook.close()
    print('success!')
