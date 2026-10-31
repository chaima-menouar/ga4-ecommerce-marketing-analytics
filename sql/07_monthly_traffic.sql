-- Monthly counts of session_start events (proxy for sessions)
SELECT
  FORMAT_DATE('%Y-%m', PARSE_DATE('%Y%m%d', event_date)) AS month,
  COUNTIF(event_name = 'session_start') AS sessions
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
GROUP BY month
ORDER BY month;
