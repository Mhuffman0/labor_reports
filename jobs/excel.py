def create_sheet(df, workbook, writer, s_name, header, dollar_ranges, color_scale_rows, color_scale_ranges):
    
    df.to_excel(
        excel_writer=writer, sheet_name=s_name,
        index=False, freeze_panes = (1,0)
    )
    
    worksheet = writer.sheets[s_name]
    money_fmt = workbook.add_format({'num_format': '$#,##0.00'})
    
    if dollar_ranges:
        for dollar_range in dollar_ranges:
            worksheet.set_column(dollar_range, None, money_fmt)
        
    if color_scale_rows:
        for color_scale_row in color_scale_rows:
            for i in range (2, df.shape[0]):
                worksheet.conditional_format(
                    color_scale_row.replace('#',str(i)), {
                        'type': '3_color_scale',
                        'min_color': "#63BE7B",
                        'mid_color': "#FFEB84",
                        'max_color': "#F8696B",
                        'mid_type': "percent"}
                    )
                
    if color_scale_ranges:
        for color_scale_range in color_scale_ranges:
            worksheet.conditional_format(
                color_scale_range + str(df.shape[0]-1), {
                    'type': '3_color_scale',
                    'min_color': "#63BE7B",
                    'mid_color': "#FFEB84",
                    'max_color': "#F8696B",
                    'mid_type': "percent"}
                )
            
    # Loop through all data in dataframe
    for index, col in enumerate(df):
                series = df[col]
                max_len = max((
                    # len of largest item
                    series.astype(str).map(len).max(),
                    # len of column name
                    len(str(series.name))  
                )) + 5
                worksheet.set_column(index, index, max_len)
                worksheet.autofilter(0, 0, df.shape[0], df.shape[1]-1)

    worksheet.set_margins(0.25, 0.25, 1.15, 0.5)
    worksheet.set_header(header)
    worksheet.repeat_rows(0)
    worksheet.fit_to_pages(1, 0)
    worksheet.set_footer('&CPage &P of &N')
    worksheet.set_landscape()