SELECT
	emps.emplname + ', ' + emps.empfname 'Manager Name',
	ISNULL(nullif(clients.cltname,'' ),wip.wcltname) 'Client Name',
	clients.cltnum + '.' + clients.clteng 'Client Code',
	SUM(wip.whours) 'Used Hours'
FROM
	pmcompany.dbo.wip wip
	INNER JOIN pmcompany.dbo.clients clients ON
		wip.wcltnum = clients.cltnum 
		AND wip.weng = clients.clteng
	LEFT JOIN pmcompany.dbo.employee emps ON
		clients.engmgr = emps.id
WHERE
	wip.windicator = 'W'
	AND wip.wbillable = 1
	AND wip.wfee <> 0
	AND clients.cppnum = '{}'
GROUP BY
	emps.emplname + ', ' + emps.empfname,
	ISNULL(nullif(clients.cltname,'' ),wip.wcltname),
	clients.cltnum + '.' + clients.clteng
ORDER BY
	'Manager Name',
	'Client Code'