from jobs.reports import excel_report

excel_report(
    {
        'sql_query':'client_list',
        'header':'Client Listing',
        'dollar_columns':''
    },
    file_name='Client_List',
    additional_send_to='john.doe@company.com',
    boss_only=True,
    exclude_partner=True
)
