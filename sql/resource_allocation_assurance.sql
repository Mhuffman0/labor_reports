--'340' Adams, Cera
--'358' Strickland, Thomas
--'429' Estano, Joshua
--'432' Usman, Oladimeji


/*Returns Work Hours for Clients by Employee*/
SELECT
	wcltname 'ClientName',
	ISNULL([340],0) 'Adams, Cera', ISNULL([358],0) 'Strickland, Thomas',	ISNULL([429],0) 'Estano, Joshua', ISNULL([432],0) 'Usman, Oladimeji',
	'',
		ISNULL([340],0) + ISNULL([358],0) + ISNULL([429],0) +	ISNULL([432],0) 'ClientTotal'
FROM (
	SELECT wcltname, wempid, whours
	FROM pmcompany.dbo.wip
	WHERE
		MONTH(wip.wdate) = MONTH(GETDATE())
		AND YEAR(wip.wdate) = YEAR(GETDATE())
		AND wempid IN (
			340, 358, 429, 432
		)
) w

PIVOT(
	SUM(whours)
	FOR wempid IN (
			[340], [358], [429], [432]
	)
) pvt
	
UNION ALL
/*Returns Total Work Hours by Employee*/
SELECT
	'EmployeeTotal' 'ClientName',
	ISNULL([340],0) 'Adams, Cera', ISNULL([358],0) 'Strickland, Thomas', ISNULL([429],0) 'Estano, Joshua', ISNULL([432],0) 'Usman, Oladimeji',
	'',
	ISNULL([340],0) + ISNULL([358],0) +	ISNULL([429],0) + ISNULL([432],0) 'TOTAL'
FROM (
	SELECT wempid, whours
	FROM pmcompany.dbo.wip
	WHERE
		MONTH(wip.wdate) = MONTH(GETDATE())
		AND YEAR(wip.wdate) = YEAR(GETDATE())
		AND wempid IN (
			340, 358, 429, 432
		)
) w

PIVOT(
	SUM(whours) FOR wempid IN (
		[340], [358], [429], [432],
		[384], [382], [436], [434]
	)
) pvt
	
UNION ALL
/*Returns Total Remaining Work Hours by Employee*/
SELECT
	'RemainingHours' 'ClientName',
	160 - ISNULL([340],0) 'Adams, Cera',	160 - ISNULL([358],0) 'Strickland, Thomas', 160 - ISNULL([429],0) 'Estano, Joshua', 160 - ISNULL([432],0) 'Usman, Oladimeji',
	'',
	10 * 160 - (
		ISNULL([340],0) + ISNULL([358],0) + ISNULL([429],0) + ISNULL([432],0)
	) 'TOTAL'

FROM (
	SELECT wempid, whours
	FROM pmcompany.dbo.wip
	WHERE
		MONTH(wip.wdate) = MONTH(GETDATE())
		AND YEAR(wip.wdate) = YEAR(GETDATE())
		AND wempid IN (
			340, 358, 429, 432
		)
) w

PIVOT(
	SUM(whours) FOR wempid IN (
		[340], [358], [429], [432]
	)
) pvt