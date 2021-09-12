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
	pmcompany.dbo.clients clients,
	pmcompany.dbo.Employee emps
WHERE
	wip.wscdesc = 'WORK OUTSIDE SCOPE'
	AND wip.wcltid = clients.ID
	AND wip.winvnum = 0
	AND wip.wfee > 0
	AND emps.id = wip.wempid
	AND (
		-- Logic for Frank O'Brien's Team
		('{0}' = '140' AND emps.empnum IN (
			'140', --O'Brien, Francis
			'491', --Schroll, Patrick
			'563', --Burke, Cameron
			'628'  --Bruno, Ashley
			)
		)
		-- Logic for Lauren Carnes' Team
		OR ('{0}' = '070' AND emps.empnum IN (
			'070', --CarnesL, Lauren
			'184', --Salamone, Jennifer
			'357', --Kaczkowska, Kasia
			'473', --McDonell, Ryan
			'488', --McDonough, Derek
			'496', --Keefe, Jessica
			'513', --Imbriani, Victoria
			'520', --Feuerbach, Matthew
			'569', --Gassett, Emma
			'583', --Ames, Jonathan
			'609'  --Luo, Lucy
			)
		)
		-- Logic for Other partners
		OR ('{0}' NOT IN ('070','140') AND emps.empnum = '{0}'))
	AND wip.wdate <= '{1}'
	AND wip.wdate >= '2018-1-1'
ORDER BY
	'Working Partner',
	'Client Num.Eng',
	'WIP Date',
	'Emp Last Name'