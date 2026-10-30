-- Session acquisition approximation using first event's collected source/medium.
-- Not equivalent to GA4 UI's session default channel grouping.
WITH e AS (
 SELECT user_pseudo_id,
 (SELECT value.int_value FROM UNNEST(event_params) WHERE key='ga_session_id') sid,
 event_timestamp, traffic_source.source AS source, traffic_source.medium AS medium,
 event_name
 FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
 WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
), s AS (
 SELECT user_pseudo_id,sid,
 ARRAY_AGG(STRUCT(source,medium) ORDER BY event_timestamp LIMIT 1)[OFFSET(0)] AS acquisition,
 COUNTIF(event_name='purchase') AS purchases
 FROM e WHERE user_pseudo_id IS NOT NULL AND sid IS NOT NULL GROUP BY 1,2
)
SELECT COALESCE(acquisition.source,'(not set)') AS first_user_source,
 COALESCE(acquisition.medium,'(not set)') AS first_user_medium,
 COUNT(*) AS sessions, SUM(purchases) AS purchases,
 SAFE_DIVIDE(COUNTIF(purchases>0),COUNT(*)) AS session_purchase_rate
FROM s GROUP BY 1,2 ORDER BY sessions DESC;
