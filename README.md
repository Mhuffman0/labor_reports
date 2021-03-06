# JOBS #
----
This folder contains the actual report jobs and their component modules

## excel.py ##
General excel writer functions

### create_sheet ###
Creates a formatted report sheet in an excel file given the following parameters:  
* An excel writer
* A sheet name
* A data frame

## reports.py ##
Consolitory functions used for running reports
### default_report ###
Runs a sql query (parameter 1) from within the sql folder and returns results for each partner named Mike boss.  
Emails with a csv of the results and an html table are then sent to the partner and any other emails provided in parameter 2 or greater.

### wos ###
Runs a sql query returning the info for all active partners.
From here, returns results of __wos_all.sql__ and __wos_partner_only.sql__ as sheets in an excel files and emails results to partner.

## send_email.py ##
### default_email ###
Sends a default report email provided the following parameters:
* smtp server
* smtp port
* send from
* send to
* subject
* attachments

## sql.py ##
### execute_select_query_from_file ###
Executes a given sql query and returns results as a dataframe.
# SQL #
----
This folder contains copies of the sql queries used to extract information for the various reports
## resource_allocation.sql ##
Custom report for Mike boss that returns shared team members' hours worked and availability for the month.

## return_partners.sql ##
Returns a list of all active partners' id, last name, first name, and email

## wip_aging.sql ##
Returns information on how WIP is aging in 30 day incremements and then > 180

## wip_details.sql ##
Returns information on WIP broken up by client, manager, and employee

## wip_summary.sql ##
Returns information on WIP broken up by client, and manager

## wos_all.sql ##
Returns information on work outside scope performed by employee's for a given partner's clients broken up by client.

## wos_partner_only.sql ##
Returns information on work outside scope performed by a given partner broken up by client.

# TABLES #
----
This folder contains the .csv or .xlsx results of the report jobs.  
Files here can be deleted without consequence if they are no longer required.

