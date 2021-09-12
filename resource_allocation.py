from jobs.reports import excel_report

excel_report(
    {
        'sql_query':'resource_allocation_advisory',
        'header':'Resource Allocation Advisory',
        'color_scale_rows':['B#:I#'],
        'color_scale_ranges':['K2:K']
    },
    {
        'sql_query':'resource_allocation_assurance',
        'header':'Resource Allocation Assurance',
        'color_scale_rows':['B#:E#'],
        'color_scale_ranges':['G2:G']
    },
    file_name='resource_allocation',
    additional_send_to='john.doe@company.com,john.doe@company.com',
    boss_only=True
)
