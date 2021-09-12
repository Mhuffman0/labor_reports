SELECT
       ID,
       Cltname,
       Cltnum + '.' + CltEng 'Clientcode',
       Engst,
       Engcountry,
       Engentity
FROM
       pmcompany.dbo.clients
WHERE
       id <> 0
ORDER BY
       3, 2
;