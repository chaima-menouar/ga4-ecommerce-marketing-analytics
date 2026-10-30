-- Purchase events and recorded purchase revenue by day (sample data).
SELECT PARSE_DATE('%Y%m%d',event_date) AS day,
 COUNTIF(event_name='purchase') AS purchases,
 ROUND(SUM(IF(event_name='purchase',ecommerce.purchase_revenue,0)),2) AS purchase_revenue
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
GROUP BY day ORDER BY day;
