# Fiche projet : mesure marketing GA4, BigQuery et Looker Studio

**Problématique.** Comment mesurer les visites, les achats et les étapes de conversion d'une boutique e-commerce pour identifier des pistes d'amélioration marketing ?

**Cas.** Export public GA4 obfusqué de la Google Merchandise Store, du 1er novembre 2020 au 31 janvier 2021 (92 jours).

**Outils.** BigQuery SQL (calculs), Google Sheets (relais des CSV), Looker Studio (tableau de bord partagé), Streamlit + Plotly (prototype local), GitHub (versionnement).

**Méthode.** Les sessions par jour et par mois, les utilisateurs distincts et les utilisateurs par source de première acquisition sont calculés en SQL. Un funnel ordonné (vue produit, ajout au panier, début de paiement, achat) est calculé globalement et par canal. Les résultats sont exportés en CSV, puis contrôlés : les totaux mensuels et journaliers sont identiques (354 970 sessions) et la somme des canaux redonne exactement le funnel global (77 020 sessions avec vue produit, 2 834 achats). Ils alimentent un tableau de bord Looker Studio de trois pages : vue d'ensemble, acquisition marketing, conversion et funnel.

**Résultats réels.**
- Sessions : 354 970 sur la période, soit environ 3 858 par jour. Novembre 106 585, décembre 131 836 (+23,7 %), janvier 116 549 (-11,6 %).
- Utilisateurs : 270 154 identifiants distincts.
- Achats : 2 834 sessions au parcours complet (vue produit, panier, paiement, achat dans l'ordre), soit 3,68 % des 77 020 sessions avec vue produit. Ce n'est pas le nombre total d'achats du site.
- Revenu : non exporté dans `results/`. Il peut être calculé avec `sql/ga4_channel_performance_verified.sql` (en USD).
- Source principale : `google / organic` (103 487 utilisateurs en première acquisition), devant `(direct) / (none)` (75 951).
- Étape présentant la plus grande perte : de la vue produit à l'ajout au panier, avec 80,31 % d'abandon (61 853 sessions). Viennent ensuite le panier vers le paiement (64,29 %) puis le paiement vers l'achat (47,67 %).
- Canaux (taux d'achat sur sessions avec vue produit) : referral 4,32 %, direct 3,64 %, organic 3,10 %, cpc 2,87 %, moyenne 3,68 %.

**Recommandations.**
1. Traiter d'abord la perte entre fiche produit et panier : c'est la plus grande en volume. Tester les fiches produit (prix, photos, livraison) et mesurer le taux d'ajout au panier par catégorie.
2. Relancer les paniers abandonnés (9 751 sessions n'ont pas démarré le paiement) et auditer la page de paiement, où près d'une session sur deux se perd.
3. Améliorer la conversion du trafic organique, premier canal en volume mais sous la moyenne (3,10 % contre 3,68 %). Ne juger le canal cpc (2,87 %) qu'avec les coûts média, absents ici.
4. Fiabiliser la mesure : attribution au niveau de la session, exclusion du trafic interne, mise en place de Consent Mode v2 (voir `docs/tracking_plan.md`).

**Limites.** Données historiques et anonymisées, valeurs `(data deleted)` et `<Other>` non interprétables, canaux basés sur la première acquisition de l'utilisateur, utilisateurs par source non additionnables, aucun revenu ni coût média dans les résultats, funnel ordonné donc restreint aux parcours complets, biais de consentement.

**Liens.** Dépôt : https://github.com/chaima-menouar/ga4-ecommerce-marketing-analytics · Tableau de bord Looker Studio : https://datastudio.google.com/reporting/ccffd417-80be-443e-a156-a38cdfa412db
