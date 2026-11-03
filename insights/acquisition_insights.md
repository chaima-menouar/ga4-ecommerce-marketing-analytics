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

## Complement for the dashboard (Member 3): traffic rhythm

- **Peak:** 8 December 2020 is the busiest day (7,526 sessions), followed by 9 December (6,211) and 10 December (5,759). A second high point is 6 January 2021 (5,952).
- **Black Friday:** 27 November 2020 recorded 3,928 sessions, close to the November daily average (about 3,553). No spike is visible on that day in these data.
- **Weekly pattern:** average daily sessions are highest on Tuesday (about 4,600) and Wednesday (about 4,500) and lowest on Saturday (about 3,060) and Sunday (about 2,860).
- **Holidays:** 24 and 25 December and 1 January are among the lowest days (2,774; 2,624; 2,289).
- No cause is attributed to the December peak: campaign or sales data would be needed.

## Complement for the dashboard (Member 3): from acquisition to conversion

Source: `results/03_Channel_Conversion_Data.csv`. Channels are grouped by `traffic_source.medium` (first-user acquisition). The base is sessions with a product view, and a purchase means a complete ordered funnel (product view, add to cart, begin checkout, purchase).

| Medium | Product-view sessions | Purchase sessions | Purchase rate |
|---|---|---|---|
| `referral` | 14,090 | 609 | 4.32% |
| `(none)` | 17,678 | 643 | 3.64% |
| `organic` | 25,740 | 798 | 3.10% |
| `cpc` | 3,168 | 91 | 2.87% |
| `<Other>` | 10,589 | 299 | 2.82% |
| `(data deleted)` | 5,755 | 394 | 6.85% |
| All channels | 77,020 | 2,834 | 3.68% |

- Organic is the largest source of product-view sessions (33.4%) but converts below the 3.68% average.
- `cpc` brings the smallest volume (4.1% of product-view sessions, 3.2% of purchase sessions) with a below-average rate. Without cost data, its return cannot be judged.
- `(data deleted)` shows the highest rate (6.85%) but is masked data and must not drive decisions.
- `referral` includes `shop.googlemerchandisestore.com` (26,065 users in `source_medium.csv`), which looks like the store's own domain. Part of the referral performance may therefore come from internal traffic.
