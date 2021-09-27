from jobs.reports import excel_report

excel_report(
    {"sql_query": "wip_aging", "header": "Aged WIP", "dollar_ranges": ["D:K"]},
    file_name="WIP_Aging",
    additional_send_to="john.john.doe@company.com,john.john.doe@company.com,"
    "john.doe@company.com,john.john.doe@company.com",
    boss_only=True,
)
