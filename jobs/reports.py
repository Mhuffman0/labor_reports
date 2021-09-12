from dotenv import load_dotenv
from datetime import datetime
import os
import pandas as pd
import xlsxwriter

from jobs.sql import execute_select_query_from_file
from jobs.send_email import default_email
from jobs.excel import create_sheet

# Loading database variables for SQL connection & email
load_dotenv()

def format_date_time(date,string=False,time=False):
    if time:
        date = date.strftime('%m/%d/%Y @ %H:%M %p')
    else:
        date = date.strftime('%m/%d/%Y')
    if string:
            date = str(date)
    return(date)

def excel_report( *reports,file_name,additional_send_to='',wip_date='',boss_only=False,exclude_partner=False):
    if wip_date == '':
        wip_date = format_date_time(datetime.now(),True)

    # Pulls a list of active partners and returns information on each
    partner_df = execute_select_query_from_file(
        query_file='sql/return_partners.sql',
        sqlserver=os.getenv('SQLSERVER'),
        database=os.getenv('DATABASE'),
        username=os.getenv('UID'),
        password=os.getenv('PASSWORD')
    )

    # Removes lines for other partners if report is boss-specific
    if boss_only:
        partner_df = partner_df[partner_df.emplname == 'boss']

    df_dict = {}

    # Executes a for loop for each partner
    for index, row in partner_df.iterrows():

        # Executes the select queries for the given partner and saves the results to a dictionary of dataframes under the 'result' key
        for report in reports:

            df_dict[report['sql_query']] = {
                'results':{},
                'header':{},
                'dollar_ranges':{},
                'color_scale_rows':{},
                'color_scale_ranges':{}
            }

            df_dict[report['sql_query']]['results'][row['empnum']] = execute_select_query_from_file(
                row['empnum'],
                wip_date,
                query_file='sql/' + report['sql_query'] + '.sql',
                sqlserver=os.getenv('SQLSERVER'),
                database=os.getenv('DATABASE'),
                username=os.getenv('UID'),
                password=os.getenv('PASSWORD')
            )

            # Saves the headers of the queries to the same dictionary under the 'header' key
            df_dict[report['sql_query']]['header'] = report['header']
            
            try:
                df_dict[report['sql_query']]['dollar_ranges'] = report['dollar_ranges']
            except:
                df_dict[report['sql_query']]['dollar_ranges'] = []
                print("No dollar ranges")
                
            try:
                df_dict[report['sql_query']]['color_scale_rows'] = report['color_scale_rows']
            except:
                df_dict[report['sql_query']]['color_scale_rows'] = []
                print("No color scale rows")
            
            try:
                df_dict[report['sql_query']]['color_scale_ranges'] = report['color_scale_ranges']
            except:
                df_dict[report['sql_query']]['color_scale_ranges'] = []
                print("No color scale ranges")

        # sets up file name for saving results of xlsx workbook
        if boss_only:
            workbook_path = 'tables/' + file_name + '.xlsx'
        else:
            workbook_path = 'tables/' + file_name + '_' + row['emplname'].title() + '.xlsx'

        writer = pd.ExcelWriter(workbook_path,engine='xlsxwriter',datetime_format='mm/dd/yyyy')
        workbook = writer.book

        for df in df_dict:
            #print(df)
            header = '&L' + format_date_time(datetime.now(),time=True) + '&company\n' + '&20&B' + df_dict[df]['header'] + '\n&11&B WIP as of ' + wip_date
            for emp in df_dict[df]['results']:
                create_sheet(
                    df_dict[df]['results'][emp],
                    workbook,
                    writer,
                    df,
                    header,
                    df_dict[df]['dollar_ranges'],
                    df_dict[df]['color_scale_rows'],
                    df_dict[df]['color_scale_ranges']
                )

        writer.save()

        if exclude_partner:
            send_to_list = additional_send_to
        else:
            send_to_list = row['empemail'] + ',' + additional_send_to

        default_email(
            'automate@company.com',
            send_to_list,
            #'me@company.com',
            file_name.replace('_', ' ').title(),
            workbook_path
        )
