# GA4 tracking plan

| Event | Trigger | Important parameters |
|---|---|---|
| page_view | Page loaded / route change | page_location, page_title |
| view_item | Product details viewed | currency, value, items |
| add_to_cart | Item added | currency, value, items |
| begin_checkout | Checkout started | currency, value, items |
| purchase | Successful order | transaction_id, currency, value, items |

Validate event names, currency, transaction IDs, duplicate purchase prevention, and item arrays with GA4 DebugView before production deployment.

## Consent Mode v2
Explain `analytics_storage`, `ad_storage`, `ad_user_data` and `ad_personalization`. Consent signals are not a substitute for lawful consent collection. Modelled conversions and missing data cannot be reconstructed exactly from this public BigQuery export. Review the local legal requirements and Google documentation.

## Limitations
Public dataset is historical (2020–2021), obfuscated, and not representative of current business performance. Session attribution in this starter is not equivalent to GA4 UI channel reporting.
