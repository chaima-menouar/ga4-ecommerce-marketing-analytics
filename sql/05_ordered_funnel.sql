-- Ordered session funnel: view_item -> add_to_cart -> begin_checkout -> purchase.
-- Counts sessions where each step occurs strictly after the previous step.
WITH events AS (
 SELECT user_pseudo_id,
 (SELECT value.int_value FROM UNNEST(event_params) WHERE key='ga_session_id') AS sid,
 event_name, event_timestamp
 FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
 WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
 AND event_name IN ('view_item','add_to_cart','begin_checkout','purchase')
), sessions AS (
 SELECT user_pseudo_id,sid,
 ARRAY_AGG(STRUCT(event_name,event_timestamp) ORDER BY event_timestamp) AS ev
 FROM events WHERE user_pseudo_id IS NOT NULL AND sid IS NOT NULL
 GROUP BY 1,2
), steps AS (
 SELECT
 (SELECT MIN(x.event_timestamp) FROM UNNEST(ev) x WHERE x.event_name='view_item') AS t1,
 ev FROM sessions
), steps2 AS (
 SELECT t1,
 (SELECT MIN(x.event_timestamp) FROM UNNEST(ev) x WHERE x.event_name='add_to_cart' AND x.event_timestamp>t1) AS t2,
 ev FROM steps
), steps3 AS (
 SELECT t1,t2,
 (SELECT MIN(x.event_timestamp) FROM UNNEST(ev) x WHERE x.event_name='begin_checkout' AND x.event_timestamp>t2) AS t3,
 ev FROM steps2
), steps4 AS (
 SELECT t1,t2,t3,
 (SELECT MIN(x.event_timestamp) FROM UNNEST(ev) x WHERE x.event_name='purchase' AND x.event_timestamp>t3) AS t4
 FROM steps3
)
SELECT COUNTIF(t1 IS NOT NULL) AS view_item_sessions,
 COUNTIF(t2 IS NOT NULL) AS add_to_cart_sessions,
 COUNTIF(t3 IS NOT NULL) AS checkout_sessions,
 COUNTIF(t4 IS NOT NULL) AS purchase_sessions
FROM steps4;
