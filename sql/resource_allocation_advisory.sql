--'287' Harriman, Robbie
--'304' Maraziti, Adam
--'414' Connolly, Emily
--'374' Haapaoja, Greg
--'384' Kamperides, Jill
--'382' Upton, Katelyn
--'436' Cunningham, Katie
--'434' Fulgencio, Silviano

/*Returns Work Hours for Clients by Employee*/
SELECT
	wcltname 'ClientName',
	ISNULL([287],0) 'Harriman, Robbie', ISNULL([304],0) 'Maraziti, Adam',	ISNULL([414],0) 'Connolly, Emily', ISNULL([374],0) 'Haapaoja, Greg',
	ISNULL([384],0) 'Kamperides, Jill', ISNULL([382],0) 'Upton, Katelyn', ISNULL([436],0) 'Cunningham, Katie', ISNULL([434],0) 'Fulgencio, Silviano',
	'',
		ISNULL([287],0) + ISNULL([304],0) + ISNULL([414],0) +	ISNULL([374],0) +
		ISNULL([384],0) + ISNULL([382],0) + ISNULL([436],0) + ISNULL([434],0) 'ClientTotal'
FROM (
	SELECT wcltname, wempid, whours
	FROM pmcompany.dbo.wip
	WHERE
		MONTH(wip.wdate) = MONTH(GETDATE())
		AND YEAR(wip.wdate) = YEAR(GETDATE())
		AND wempid IN (
			287, 304, 414, 374,
			384, 382, 436, 434
		)
) w

PIVOT(
	SUM(whours)
	FOR wempid IN (
			[287], [304], [414], [374],
			[384], [382], [436], [434]
	)
) pvt
	
UNION ALL

/*Returns Total Work Hours by Employee*/
SELECT
	'EmployeeTotal' 'ClientName',
	ISNULL([287],0) 'Harriman, Robbie', ISNULL([304],0) 'Maraziti, Adam', ISNULL([414],0) 'Connolly, Emily', ISNULL([374],0) 'Haapaoja, Greg',
	ISNULL([384],0) 'Kamperides, Jill', ISNULL([382],0) 'Upton, Katelyn', ISNULL([436],0) 'Cunningham, Katie', ISNULL([434],0) 'Fulgencio, Silviano',
	'',
		ISNULL([287],0) + ISNULL([304],0) +	ISNULL([414],0) + ISNULL([374],0) +
		ISNULL([384],0) + ISNULL([382],0) + ISNULL([436],0) + ISNULL([434],0) 'TOTAL'
FROM (
	SELECT wempid, whours
	FROM pmcompany.dbo.wip
	WHERE
		MONTH(wip.wdate) = MONTH(GETDATE())
		AND YEAR(wip.wdate) = YEAR(GETDATE())
		AND wempid IN (
			287, 304, 414, 374,
			384, 287, 436, 434
		)
) w

PIVOT(
	SUM(whours) FOR wempid IN (
		[287], [304], [414], [374],
		[384], [382], [436], [434]
	)
) pvt
	
UNION ALL
/*Returns Total Remaining Work Hours by Employee*/
SELECT
	'RemainingHours' 'ClientName',
	160 - ISNULL([287],0) 'Harriman, Robbie',	160 - ISNULL([304],0) 'Maraziti, Adam', 160 - ISNULL([414],0) 'Connolly, Emily', 160 - ISNULL([374],0) 'Haapaoja, Greg',
	160 - ISNULL([384],0) 'Kamperides, Jill', 160 - ISNULL([382],0) 'Upton, Katelyn', 160 - ISNULL([436],0) 'Cunningham, Katie', 160 - ISNULL([434],0) 'Fulgencio, Silviano',
	'',
	10 * 160 - (
		ISNULL([287],0) + ISNULL([304],0) + ISNULL([414],0) + ISNULL([374],0) +
		ISNULL([384],0) + ISNULL([382],0) + ISNULL([436],0) + ISNULL([434],0)
	) 'TOTAL'

FROM (
	SELECT wempid, whours
	FROM pmcompany.dbo.wip
	WHERE
		MONTH(wip.wdate) = MONTH(GETDATE())
		AND YEAR(wip.wdate) = YEAR(GETDATE())
		AND wempid IN (
			287, 304, 414, 374,
			384, 382, 436, 434
		)
) w

PIVOT(
	SUM(whours) FOR wempid IN (
		[287], [304], [414], [374],
		[384], [382], [436], [434]
	)
) pvt