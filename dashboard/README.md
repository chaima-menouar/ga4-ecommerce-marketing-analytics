# Looker Studio dashboard

## Dashboard Looker Studio partagé
Lien : https://datastudio.google.com/reporting/ccffd417-80be-443e-a156-a38cdfa412db
Export PDF : dashboard_looker_studio.pdf
Pages : Vue d'ensemble, Acquisition marketing, Conversion et Funnel
Sources : CSV du dossier results/ importés dans Google Sheets, connectés à Looker Studio

## Définitions utilisées
- Sessions : sessions distinctes sur la période du 1er novembre 2020 au 31 janvier 2021 (voir sql/01_daily_sessions.sql).
- Achats (parcours complet) : sessions ayant fait view_item, add_to_cart, begin_checkout puis purchase, dans cet ordre (voir sql/01_funnel_analysis.sql). Ce n'est pas le nombre total d'achats du site.
- Taux d'achat par canal : sessions au parcours complet divisées par les sessions avec vue produit, par medium de première acquisition (traffic_source).

## Limites
- Données historiques et anonymisées : les valeurs (data deleted) et <Other> ne sont pas interprétables.
- Le fichier source_medium compte des utilisateurs distincts par ligne : ses lignes ne s'additionnent pas.
- Les CSV exportés ne contiennent ni revenu ni coût média.