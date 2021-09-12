SELECT
	wip.wcltnum + '.' + wip.weng 'Client Num.Eng',
	wip.wcltname 'Client Name',
	clients.cpplname + ' ' + clients.cppnum 'Working Partner',
	wip.wemplname 'Emp Last Name',
	wip.wdate 'WIP Date',
	wip.whours 'Hours',
	wip.wfee 'WIP Amount',
	--SUBSTRING(ISNULL(wip.wref,''),1,20) 'Reference'
	ISNULL(wip.wref,'') 'Reference'
FROM
	pmcompany.dbo.wip wip,
	pmcompany.dbo.clients clients ,
	pmcompany.dbo.employee emps
WHERE
	wip.wscdesc = 'WORK OUTSIDE SCOPE'
	AND wip.wcltid = clients.ID
	AND wip.winvnum = 0
	AND emps.id = wip.wempid
	AND wip.wfee > 0
	AND clients.cppnum = '{0}'
	AND wip.wdate <= '{1}'
	AND wip.wdate >= '2018-1-1'
ORDER BY
	'Working Partner',
	'Client Num.Eng',
	'WIP Date',
	'Emp Last Name'