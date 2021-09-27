import datetime
from jobs.reports import excel_report

today = datetime.date.today()
first = today.replace(day=1)
last_month = first - datetime.timedelta(days=1)

excel_report(
    {
        "sql_query": "wos_by_employee",
        "header": "Work Outside Scope by Employee Name",
        "dollar_ranges": ["G:G"],
    },
    {
        "sql_query": "wos_by_working_partner",
        "header": "Work Outside Scope by Working Partner",
        "dollar_ranges": ["G:G"],
    },
    file_name="WOS_Status",
    additional_send_to="john.doe@company.com,john.doe@company.com,john.doe@company.com",
    wip_date=last_month.strftime("%m/%d/%Y"),
    boss_only=False,
    exclude_partner=True,
)
