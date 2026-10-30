-- BigQuery Standard SQL | GA4 public obfuscated e-commerce sample
-- Source: bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*
-- Historical data: 2020-11-01 through 2021-01-31.
-- Run this in your Google Cloud project; check bytes billed before executing.
-- Output schema matches demo/data GA4 adapter (see README).
WITH events AS (
 SELECT
   user_pseudo_id,
   event_name,
   event_timestamp,
   (SELECT ep.value.int_value FROM UNNEST(event_params) ep WHERE ep.key='ga_session_id') AS session_id,
   COALESCE(
     (SELECT ep.value.string_value FROM UNNEST(event_params) ep WHERE ep.key='source'),
     traffic_source.source,
     '(direct)'
   ) AS source,
   COALESCE(
     (SELECT ep.value.string_value FROM UNNEST(event_params) ep WHERE ep.key='medium'),
     traffic_source.medium,
     '(none)'
   ) AS medium,
   ecommerce.purchase_revenue_in_usd AS purchase_revenue_usd
 FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
 WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
   AND user_pseudo_id IS NOT NULL
),
sessions AS (
 SELECT user_pseudo_id, session_id,
   ARRAY_AGG(STRUCT(source,medium) ORDER BY event_timestamp LIMIT 1)[OFFSET(0)] AS attribution,
   COUNTIF(event_name='generate_lead')>0 AS lead,
   COUNTIF(event_name='purchase')>0 AS purchase,
   SUM(IF(event_name='purchase',COALESCE(purchase_revenue_usd,0),0)) AS revenue_usd
 FROM events WHERE session_id IS NOT NULL
 GROUP BY 1,2
)
SELECT
 CONCAT(attribution.source,' / ',attribution.medium) AS channel,
 COUNT(*) AS sessions,
 COUNTIF(lead) AS leads,
 COUNTIF(purchase) AS purchases,
 ROUND(SUM(revenue_usd),2) AS revenue_usd
FROM sessions
GROUP BY channel
ORDER BY sessions DESC;
