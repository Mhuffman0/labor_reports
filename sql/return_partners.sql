SELECT
    empnum,
	emplname,
    empfname,
    empemail
FROM
    dbo.employee
WHERE
    emplevel = '4'
    AND empstatus = 'A'
ORDER BY
    emplname,
    empfname
;