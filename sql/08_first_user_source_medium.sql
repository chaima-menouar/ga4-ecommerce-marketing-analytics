-- First-user acquisition source/medium; NOT session-level attribution.
-- Distinct IDs per group may overlap and must not be summed as total unique users.
SELECT
  COALESCE(traffic_source.source, '(not set)') AS source,
  COALESCE(traffic_source.medium, '(not set)') AS medium,
  COUNT(DISTINCT user_pseudo_id) AS total_users
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
GROUP BY source, medium
ORDER BY total_users DESC;
