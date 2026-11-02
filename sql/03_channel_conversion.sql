WITH events_base AS (
  SELECT
    user_pseudo_id,
    (
      SELECT value.int_value
      FROM UNNEST(event_params)
      WHERE key = 'ga_session_id'
    ) AS session_id,
    event_name,
    event_timestamp,
    COALESCE(
      traffic_source.medium, '(not set)'
    ) AS medium
  FROM
    `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
  WHERE
    _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
    AND event_name IN (
      'view_item',
      'add_to_cart',
      'begin_checkout',
      'purchase'
    )
    AND user_pseudo_id IS NOT NULL
),

sessions AS (
  SELECT
    user_pseudo_id,
    session_id,
    ANY_VALUE(medium) AS medium,
    MIN(IF(
      event_name = 'view_item',
      event_timestamp, NULL
    )) AS view_time
  FROM events_base
  WHERE session_id IS NOT NULL
  GROUP BY user_pseudo_id, session_id
),

cart_step AS (
  SELECT
    s.*,
    MIN(IF(
      e.event_name = 'add_to_cart'
      AND e.event_timestamp >= s.view_time,
      e.event_timestamp, NULL
    )) AS cart_time
  FROM sessions s
  LEFT JOIN events_base e
    USING (user_pseudo_id, session_id)
  GROUP BY
    s.user_pseudo_id, s.session_id,
    s.medium, s.view_time
),

checkout_step AS (
  SELECT
    s.*,
    MIN(IF(
      e.event_name = 'begin_checkout'
      AND e.event_timestamp >= s.cart_time,
      e.event_timestamp, NULL
    )) AS checkout_time
  FROM cart_step s
  LEFT JOIN events_base e
    USING (user_pseudo_id, session_id)
  GROUP BY
    s.user_pseudo_id, s.session_id,
    s.medium, s.view_time, s.cart_time
),

purchase_step AS (
  SELECT
    s.*,
    MIN(IF(
      e.event_name = 'purchase'
      AND e.event_timestamp >= s.checkout_time,
      e.event_timestamp, NULL
    )) AS purchase_time
  FROM checkout_step s
  LEFT JOIN events_base e
    USING (user_pseudo_id, session_id)
  GROUP BY
    s.user_pseudo_id, s.session_id,
    s.medium, s.view_time, s.cart_time,
    s.checkout_time
)

SELECT
  medium,

  COUNTIF(view_time IS NOT NULL)
    AS product_view_sessions,

  COUNTIF(cart_time IS NOT NULL)
    AS add_to_cart_sessions,

  COUNTIF(checkout_time IS NOT NULL)
    AS checkout_sessions,

  COUNTIF(purchase_time IS NOT NULL)
    AS purchase_sessions,

  ROUND(
    SAFE_DIVIDE(
      COUNTIF(purchase_time IS NOT NULL),
      COUNTIF(view_time IS NOT NULL)
    ) * 100,
    2
  ) AS conversion_rate,

  ROUND(
    (1 - SAFE_DIVIDE(
      COUNTIF(purchase_time IS NOT NULL),
      COUNTIF(view_time IS NOT NULL)
    )) * 100,
    2
  ) AS abandonment_rate

FROM purchase_step
WHERE view_time IS NOT NULL
GROUP BY medium
HAVING COUNTIF(view_time IS NOT NULL) >= 100
ORDER BY conversion_rate DESC;