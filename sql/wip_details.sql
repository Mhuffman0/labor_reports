SELECT
	emps2.emplname + ', ' + emps2.empfname 'Manager Name',
	clients.cltname 'Client Name',
	clients.cltnum + '.' + clients.clteng 'Client Code',
	emps.emplname + ', ' + emps.empfname 'Employee Name',
	SUM(wip.whours) 'Used Hours',
	SUM(wip.wfee) 'Ext $'
FROM
	pmcompany.dbo.wip wip
	INNER JOIN pmcompany.dbo.clients clients ON
		wip.wcltnum = clients.cltnum 
		AND wip.weng = clients.clteng
	LEFT JOIN pmcompany.dbo.employee emps ON
		wip.wempid = emps.id 
	LEFT JOIN pmcompany.dbo.employee emps2 ON
		clients.engmgr = emps2.id
WHERE
	wip.windicator = 'W'
	AND wip.wbillable = 1
	AND wip.wfee <> 0
	AND clients.cppnum = '{}'
GROUP BY
	emps2.emplname + ', ' + emps2.empfname,
	clients.cltname,
	clients.cltnum + '.' + clients.clteng,
	emps.Emplname + ', ' + emps.empfname
ORDER BY
	emps2.emplname + ', ' + emps2.empfname,
	cltname,
	emps.emplname + ', ' + emps.empfname