SELECT
	clients.cpplname 'Partner_Name',
	clients.cltnum + '.' + clients.clteng 'Client_Code',
	ISNULL(nullif(clients.cltname,'' ),wip.wcltname) 'Client_Name',
	ISNULL(SUM(wip.wfee),0) 'Outstanding_WIP',
	ISNULL(SUM(CASE WHEN DATEDIFF(month, wdate, getdate()) < 2 THEN wip.wfee END),0) 'Current',
	ISNULL(SUM(CASE WHEN DATEDIFF(month, wdate, getdate()) = 2 THEN wip.wfee END),0) '31 - 60',
	ISNULL(SUM(CASE WHEN DATEDIFF(month, wdate, getdate()) = 3 THEN wip.wfee END),0) '61 - 90',
	ISNULL(SUM(CASE WHEN DATEDIFF(month, wdate, getdate()) = 4 THEN wip.wfee END),0) '91 - 120',
	ISNULL(SUM(CASE WHEN DATEDIFF(month, wdate, getdate()) = 5 THEN wip.wfee END),0) '121 - 150',
	ISNULL(SUM(CASE WHEN DATEDIFF(month, wdate, getdate()) = 6 THEN wip.wfee END),0) '151 - 180',
	ISNULL(SUM(CASE WHEN DATEDIFF(month, wdate, getdate()) > 6 THEN wip.wfee END),0) '181 +'
FROM
	pmcompany.dbo.clients clients
	JOIN pmcompany.dbo.wip wip ON
		wip.wcltnum = clients.cltnum
		AND wip.weng = clients.clteng
WHERE
	wip.windicator = 'W'
	AND wip.wbillable = '1'
	AND wip.wfee <> 0
	AND clients.cppnum = '{0}'
	AND wip.wdate <= '{1}'
GROUP BY
	clients.cpplname,
	clients.cltnum + '.' + clients.clteng,
	ISNULL(nullif(clients.cltname,'' ),wip.wcltname)
ORDER BY
	'Client_Code'