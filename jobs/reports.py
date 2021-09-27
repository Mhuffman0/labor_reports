import os
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv

from .sql import execute_select_query_from_file
from .send_email import default_email
from .excel import create_sheet

# Loading database variables for SQL connection & email
load_dotenv()


def format_date_time(input_date_time, return_string=False, return_time=False):
    """Takes a date or time and returns that value properly formatted

    :param input_date_time: date or time to be formatted
    :param return_time: Default value = False)
    :param return_string:  (Default value = False)

    """
    if return_time:
        input_date_time = input_date_time.strftime("%m/%d/%Y @ %H:%M %p")
    else:
        input_date_time = input_date_time.strftime("%m/%d/%Y")
    if return_string:
        input_date_time = str(input_date_time)
    return input_date_time


def excel_report(
    *reports,
    file_name,
    additional_send_to="",
    wip_date="",
    boss_only=False,
    exclude_partner=False,
):
    """Given at least one report, runs the specificed SQL query for that report, creates
    an .xlsx file of the results, and emails to the relevant partner send to's.
    additional_send_to, wip_date, boss_only, and exclude_partner are all optional.

    :param *reports: report to be run wich the optional paramaters of header, dollar_ranges, color_scale_row, and color_scale_ranges
    :param file_name: .sql file used for the report.
    :param additional_send_to: emails other than partner to send the report to (Default value = "")
    :param wip_date: max wip date to be considered for report (Default value = "")
    :param boss_only: report is only to be run for boss (Default value = False)
    :param exclude_partner: Partner is not to be included in email (Default value = False)

    """

    now = format_date_time(datetime.now(), return_time=True)
    if not wip_date:
        wip_date = now

    # Pulls a list of active partners and returns information on each
    partner_df = execute_select_query_from_file(
        query_file="sql/return_partners.sql",
        sqlserver=os.getenv("SQLSERVER"),
        database=os.getenv("DATABASE"),
        username=os.getenv("UID"),
        password=os.getenv("PASSWORD"),
    )

    # Removes lines for other partners if report is boss-specific
    if boss_only:
        partner_df = partner_df[partner_df.emplname == "boss"]

    df_dict = {}

    # Saves the attributes of the reports to the same dictionary under the 'relevant' key
    for report in reports:
        report_name = report["sql_query"]
        df_dict[report_name] = {}
        for key in (
            "header",
            "dollar_ranges",
            "color_scale_rows",
            "color_scale_ranges",
        ):
            if key in report:
                df_dict[report_name][key] = report[key]
            else:
                df_dict[report_name][key] = []

        # Executes a for loop for each partner
        for index, row in partner_df.iterrows():

            # Executes the select queries for the given partner and saves the results
            # to a dictionary of dataframes under the 'result' key
            df_dict[report_name]["results"] = {}
            df_dict[report_name]["results"][
                row["empnum"]
            ] = execute_select_query_from_file(
                row["empnum"],
                wip_date,
                query_file=f"sql/{report_name}.sql",
                sqlserver=os.getenv("SQLSERVER"),
                database=os.getenv("DATABASE"),
                username=os.getenv("UID"),
                password=os.getenv("PASSWORD"),
            )

        # sets up file name for saving results of xlsx workbook
        if boss_only:
            workbook_path = f"tables/{file_name}.xlsx"
        else:
            workbook_path = f"tables/{file_name}_{row['emplname'].title()}.xlsx"

        writer = pd.ExcelWriter(
            workbook_path, engine="xlsxwriter", datetime_format="mm/dd/yyyy"
        )
        workbook = writer.book

        for df in df_dict:
            header = f"&L{now}&CCompany\n&20&B{df_dict[df]['header']}\n&11&B WIP as of {wip_date}"
            for emp in df_dict[df]["results"]:
                create_sheet(
                    df_dict[df]["results"][emp],
                    workbook,
                    writer,
                    df,
                    header,
                    df_dict[df]["dollar_ranges"],
                    df_dict[df]["color_scale_rows"],
                    df_dict[df]["color_scale_ranges"],
                )

        writer.save()

        if exclude_partner:
            send_to_list = additional_send_to
        else:
            send_to_list = row["empemail"] + "," + additional_send_to

        default_email(
            "john.doe@company.com",
            send_to_list,
            file_name.replace("_", " ").title(),
            workbook_path,
        )
