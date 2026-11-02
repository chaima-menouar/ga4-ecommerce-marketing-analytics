WITH events_base AS (
  SELECT
    user_pseudo_id,
    (
      SELECT value.int_value
      FROM UNNEST(event_params)
      WHERE key = 'ga_session_id'
    ) AS session_id,
    event_name,
    event_timestamp
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
  GROUP BY s.user_pseudo_id, s.session_id, s.view_time
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
    s.view_time, s.cart_time
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
    s.view_time, s.cart_time, s.checkout_time
),

funnel AS (
  SELECT
    COUNTIF(view_time IS NOT NULL) AS product_views,
    COUNTIF(cart_time IS NOT NULL) AS cart_additions,
    COUNTIF(checkout_time IS NOT NULL) AS checkouts,
    COUNTIF(purchase_time IS NOT NULL) AS purchases
  FROM purchase_step
)

SELECT
  1 AS step_order,
  'Product View' AS funnel_step,
  product_views AS sessions,
  100.00 AS conversion_rate
FROM funnel

UNION ALL

SELECT
  2,
  'Add to Cart',
  cart_additions,
  ROUND(SAFE_DIVIDE(cart_additions, product_views) * 100, 2)
FROM funnel

UNION ALL

SELECT
  3,
  'Begin Checkout',
  checkouts,
  ROUND(SAFE_DIVIDE(checkouts, cart_additions) * 100, 2)
FROM funnel

UNION ALL

SELECT
  4,
  'Purchase',
  purchases,
  ROUND(SAFE_DIVIDE(purchases, checkouts) * 100, 2)
FROM funnel

ORDER BY step_order;