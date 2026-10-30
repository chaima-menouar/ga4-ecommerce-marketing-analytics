-- Session-level, non-sequential funnel presence. Do not interpret as ordered steps.
WITH e AS (
 SELECT user_pseudo_id,
 (SELECT value.int_value FROM UNNEST(event_params) WHERE key='ga_session_id') sid,
 event_name
 FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
 WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
)
SELECT COUNT(*) AS sessions,
 COUNTIF(view_item) AS sessions_view_item,
 COUNTIF(add_to_cart) AS sessions_add_to_cart,
 COUNTIF(begin_checkout) AS sessions_begin_checkout,
 COUNTIF(purchase) AS sessions_purchase
FROM (
 SELECT user_pseudo_id,sid,
 LOGICAL_OR(event_name='view_item') view_item,
 LOGICAL_OR(event_name='add_to_cart') add_to_cart,
 LOGICAL_OR(event_name='begin_checkout') begin_checkout,
 LOGICAL_OR(event_name='purchase') purchase
 FROM e WHERE user_pseudo_id IS NOT NULL AND sid IS NOT NULL GROUP BY 1,2
);
