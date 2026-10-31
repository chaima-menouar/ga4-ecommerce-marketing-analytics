# Acquisition & Traffic Insights — Google Merchandise Store

## Scope and methodology
- Public GA4 obfuscated sample ecommerce data in BigQuery.
- Period: 2020-11-01 through 2021-01-31 (92 days).
- Sessions are approximated by counting `session_start` events; users are distinct `user_pseudo_id` values, not necessarily unique people.
- Source/medium comes from `traffic_source`, which describes **first-user acquisition** rather than session-level attribution.

## Key findings

1. **Overall traffic:** 354,970 `session_start` events across the 92-day period, or about 3,858 per day on average.
2. **User reach:** 270,154 distinct anonymized user identifiers over the full period. This is not the number of sessions or an exact count of real people.
3. **Monthly trend:** November 2020 recorded 106,585 sessions; December 2020, 131,836; and January 2021, 116,549.
4. **December peak:** Sessions grew by approximately **23.7%** from November to December. December was the strongest month.
5. **January decline:** Sessions fell by approximately **11.6%** from December to January, but remained about **9.3%** above November.
6. **First-user acquisition:** The largest reported source/medium rows include `google / organic` (103,487 distinct user IDs), `(direct) / (none)` (75,951), and `google / cpc` (15,527). This suggests organic search is an important acquisition route in the sample.
7. **Data-quality caveats:** The anonymized sample includes `<Other>` and `(data deleted)` values, limiting detailed channel attribution. Distinct user counts calculated separately per source/medium row **must not be summed** as if they were deduplicated across all rows. Some users may appear in multiple groups.

## Interpretation and recommendations
- Prioritize analysis of organic search, given its leading reported first-user acquisition count.
- Investigate why traffic peaked in December, but do **not** assume a holiday effect without supporting campaign or sales evidence.
- Use the monthly sessions series to visualize the rise in December and decline in January.
- Treat direct and redacted/aggregated attribution carefully; do not infer that all direct traffic represents typed-in URLs.
- For a true **session acquisition** report, use session-level traffic attribution fields or an appropriate session attribution method instead of `traffic_source`.

## Dashboard handoff
- `results/daily_sessions.csv`: daily `session_start` counts.
- `results/total_users.csv`: overall distinct user identifiers.
- `results/source_medium.csv`: first-user source/medium groups with distinct user counts.
- `results/monthly_traffic.csv`: monthly `session_start` counts.

All figures are descriptive and limited to the anonymized GA4 public sample and the stated date range.
