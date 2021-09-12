from jobs.reports import excel_report

excel_report(
    {
        'sql_query':'wip_details',
        'header':'Open WIP by Manager && Employee',
        'dollar_ranges':['F:F']
    },
    {
        'sql_query':'wip_summary',
        'header':'Open WIP by Manager',
        'dollar_ranges':['E:E']
    },
    file_name='WIP_Status',
    additional_send_to='john.doe@company.com,john.doe@company.com,john.doe@company.com,john.doe@company.com,john.doe@company.com',
    boss_only=True
)

excel_report(
    {
        'sql_query':'wip_details_emp',
        'header':'Open WIP by Manager && Employee'
    },
    {
        'sql_query':'wip_summary_emp',
        'header':'Open WIP by Manager'
    },
    file_name='WIP_Status_Employee',
    additional_send_to='john.doe@company.com,john.doe@company.com,john.doe@company.com',
    boss_only=True,
    exclude_partner=True
)
