q1 = """
SELECT 
	o.id
	, a.id
	, o.name
	, o.stagename 
FROM 
	sf_account a 
LEFT JOIN 
	sf_opportunity o 
ON 
	a.id = o.nearest_partner_account__c 
WHERE
	a.name = 'Justine PETERSEN' 
LIMIT 100
"""

q3 = """
SELECT
       a.name
       , ((SUM(CASE WHEN o.decision_status__c IN ('Approved', 'Booked') THEN 1 ELSE 0 END)::float/SUM(CASE WHEN o.decision_status__c IN ('Approved', 'Booked', 'Declined') THEN 1 ELSE 0 END)::float)*100)::int AS Approval_Rate
       , (SUM(CASE WHEN o.decision_status__c IN ('Booked') THEN 1 ELSE 0 END)::float/SUM(CASE WHEN o.decision_status__c IN ('Approved', 'Booked') THEN 1 ELSE 0 END)::float)*100 AS booking_rate
       , AVG(CASE WHEN o.on_deck_score_recalculated__c >= 0 THEN o.on_deck_score_recalculated__c ELSE NULL END)::int AS avg_odsr
       , (AVG(CASE WHEN o.decision_status__c = 'Booked' THEN o.maximum_loan_amount__c ELSE NULL END))/1000::int AS avg_loan_amount
       , AVG(o.apr__c)::INT AS APR
FROM
       sf_account a
LEFT JOIN
       sf_opportunity o
ON
       o.nearest_partner_account__c = a.id
WHERE
       a.name = 'Justine PETERSEN'
GROUP BY
       a.name
LIMIT 1000;
"""