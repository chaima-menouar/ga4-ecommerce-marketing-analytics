-- Daily sessions; a session is user_pseudo_id + ga_session_id.
WITH events AS (
 SELECT PARSE_DATE('%Y%m%d',event_date) AS day, user_pseudo_id,
 (SELECT value.int_value FROM UNNEST(event_params) WHERE key='ga_session_id') AS session_id
 FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
 WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
)
SELECT day, COUNT(DISTINCT IF(user_pseudo_id IS NOT NULL AND session_id IS NOT NULL,
 CONCAT(user_pseudo_id,'.',CAST(session_id AS STRING)),NULL)) AS sessions
FROM events GROUP BY day ORDER BY day;
