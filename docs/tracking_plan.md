# Plan de marquage GA4 (Tracking Plan)

## 1. Objectifs business
- Mesurer le trafic (visiteurs, sessions) et son évolution.
- Identifier les canaux d'acquisition qui amènent des sessions et des achats.
- Comprendre le parcours d'achat (vue produit, panier, paiement, achat) et repérer où les clients abandonnent.
- Fournir des données fiables au tableau de bord et aux décisions marketing.

## 2. Architecture de collecte
Site e-commerce → couche de données (dataLayer) → Google Tag Manager (GTM) → Google Analytics 4 (GA4) → export vers BigQuery → Looker Studio.

Dans ce projet, nous partons de l'export BigQuery public de la Google Merchandise Store (du 1er novembre 2020 au 31 janvier 2021). Le marquage n'est donc pas implémenté par l'équipe : il est documenté ici pour expliquer d'où viennent les données analysées. Chaîne réellement utilisée : export BigQuery public → requêtes SQL (`sql/`) → CSV (`results/`) → Google Sheets → Looker Studio.

## 3. Événements suivis
| Événement | Déclencheur | Paramètres clés | Utilisation dans le projet |
|---|---|---|---|
| session_start | Début d'une session (automatique) | ga_session_id | Identifier et compter les sessions |
| page_view | Chargement d'une page (automatique) | page_location, page_title | Mesurer le trafic |
| view_item | Consultation d'une fiche produit | currency, value, items | Étape 1 du funnel |
| add_to_cart | Ajout d'un produit au panier | currency, value, items | Étape 2 du funnel |
| begin_checkout | Début du paiement | currency, value, items | Étape 3 du funnel |
| purchase | Commande confirmée | transaction_id, currency, value, items | Étape 4 du funnel et revenu |

## 4. Attribution des canaux (UTM)
Les liens des campagnes portent trois paramètres UTM : `utm_source` (la plateforme, ex. google), `utm_medium` (le type de canal, ex. cpc, email) et `utm_campaign` (le nom de la campagne). GA4 les traduit en source et medium. Le trafic organique et le trafic direct sont détectés automatiquement, sans UTM.

Dans l'export BigQuery, `traffic_source.source` et `traffic_source.medium` décrivent la première acquisition de l'utilisateur, pas la source de chaque session. Les analyses par canal de ce projet sont donc des analyses par canal de première acquisition.

## 5. Conventions de nommage
- Noms d'événements en minuscules avec underscores (snake_case).
- Utiliser les noms d'événements e-commerce recommandés par GA4 (view_item, add_to_cart, begin_checkout, purchase) plutôt que des noms personnalisés.
- Paramètres d'articles standards : item_id, item_name, price, quantity.
- Devise au format ISO (ex. USD, MAD).

## 6. Exemple de couche de données (add_to_cart)
```js
dataLayer.push({ ecommerce: null });  // vide l'ancien objet ecommerce
dataLayer.push({
  event: 'add_to_cart',
  ecommerce: {
    currency: 'USD',
    value: 25.0,
    items: [{ item_id: 'SKU123', item_name: 'T-shirt', price: 25.0, quantity: 1 }]
  }
});
```
Une balise GTM de type « événement GA4 » écoute l'événement `add_to_cart` et envoie ces paramètres à GA4.

## 7. Plan de validation avant mise en production
1. Tester dans le mode Aperçu de GTM : vérifier que chaque balise se déclenche une seule fois.
2. Contrôler dans GA4 DebugView : noms d'événements, paramètres, devise, tableau `items`.
3. Vérifier que `transaction_id` est unique pour éviter de compter deux fois le même achat.
4. Le lendemain, comparer les volumes dans BigQuery (l'export quotidien arrive avec un délai).

## 8. Lien avec les requêtes SQL du projet
| Besoin | Événements utilisés | Fichier |
|---|---|---|
| Sessions par jour | ga_session_id (paramètre) | `sql/01_daily_sessions.sql` |
| Funnel et abandon | view_item, add_to_cart, begin_checkout, purchase | `sql/01_funnel_analysis.sql`, `sql/02_abandonment_analysis.sql` |
| Conversion par canal | mêmes événements et `traffic_source.medium` | `sql/03_channel_conversion.sql` |

Le funnel est ordonné : une session n'est comptée à une étape que si les étapes précédentes ont eu lieu avant, dans l'ordre. Le nombre d'achats du funnel (2 834) correspond donc à des sessions au parcours complet, pas à l'ensemble des achats du site.

## 9. Consent Mode v2

### Pourquoi
Dans l'Espace économique européen, un visiteur peut refuser les cookies de mesure et de publicité. Sans adaptation, les balises Google soit continuent à collecter sans accord (non conforme), soit sont bloquées et les données de ces visiteurs disparaissent. Consent Mode permet d'adapter le comportement des balises Google au choix de chaque visiteur.

### Les quatre signaux
| Signal | Ce qu'il contrôle |
|---|---|
| `analytics_storage` | Cookies de mesure d'audience (GA4) |
| `ad_storage` | Cookies publicitaires |
| `ad_user_data` | Envoi des données utilisateur à Google à des fins publicitaires (ajouté en v2) |
| `ad_personalization` | Personnalisation publicitaire et remarketing (ajouté en v2) |

Chaque signal vaut `granted` (accordé) ou `denied` (refusé). Google exige la v2 pour utiliser les fonctions publicitaires (audiences, remarketing, mesure des conversions) avec le trafic de l'Espace économique européen.

### Deux modes d'implémentation
- **Mode basique** : aucune balise Google ne se charge avant le choix du visiteur. S'il refuse, aucune donnée n'est envoyée.
- **Mode avancé** : les balises se chargent dès l'arrivée. Si le visiteur refuse, elles envoient seulement des signaux sans cookies et sans identifiant, qui servent à la modélisation.

### Fonctionnement technique
1. Le visiteur arrive sur le site.
2. Une plateforme de gestion du consentement (CMP, bannière) s'affiche. Le consentement par défaut est défini **avant** le chargement des balises, en général sur `denied` pour l'Espace économique européen :
   ```js
   gtag('consent', 'default', {
     analytics_storage: 'denied',
     ad_storage: 'denied',
     ad_user_data: 'denied',
     ad_personalization: 'denied'
   });
   ```
3. Après le choix du visiteur, la CMP met à jour les signaux :
   ```js
   gtag('consent', 'update', {
     analytics_storage: 'granted',
     ad_storage: 'denied',
     ad_user_data: 'denied',
     ad_personalization: 'denied'
   });
   ```
4. Les balises Google adaptent leur comportement : cookies et identifiants si `granted`, signaux anonymes ou absence de collecte si `denied`.

### Modélisation des données manquantes
Quand des visiteurs refusent le consentement, GA4 et Google Ads estiment ce qui manque à partir du comportement des visiteurs qui ont accepté :
- **Modélisation comportementale (GA4)** : estimation des utilisateurs, sessions et événements non observés.
- **Modélisation des conversions (Google Ads)** : estimation des conversions non observées.

La modélisation n'est disponible que si le volume de données est suffisant. Google indique des seuils de l'ordre de 1 000 événements par jour avec `analytics_storage` refusé pendant au moins 7 jours, et d'au moins 1 000 utilisateurs par jour avec consentement accordé sur une partie des 28 jours précédents. Ces seuils évoluent : vérifier la documentation Google avant de les citer.

### Impact marketing
- Sans Consent Mode, le trafic et les conversions sont sous-estimés, et seuls les visiteurs qui acceptent les cookies sont mesurés. Les décisions budgétaires reposent alors sur un échantillon biaisé.
- Avec Consent Mode en mode avancé et assez de volume, GA4 comble une partie de l'écart par modélisation.

### Ce que cela change pour ce projet
- Le jeu de données public date de 2020 à 2021 et ne contient aucune information de consentement : cette section est explicative, elle ne s'applique pas aux chiffres du tableau de bord.
- Les données modélisées apparaissent dans les rapports GA4 mais ne sont pas exportées vers BigQuery. Une analyse en SQL, comme la nôtre, ne porte donc que sur des données observées, ce qui sous-estime l'activité réelle quand une partie des visiteurs refuse le consentement.
- Les signaux de consentement ne remplacent pas un recueil de consentement conforme. Pour un site ciblant des visiteurs européens, la CMP doit être certifiée par Google. Pour un site marocain, la loi 09-08 (CNDP) encadre aussi le traitement des données personnelles. À vérifier avec un juriste et la documentation officielle.

## 10. Limites
- Le jeu de données est historique (2020-2021), anonymisé et non représentatif de la performance actuelle d'une entreprise.
- L'attribution des sessions de ce projet n'est pas équivalente aux rapports de canaux de l'interface GA4 (première acquisition de l'utilisateur, valeurs `(data deleted)` et `<Other>` non interprétables).
- Les achats du funnel sont des sessions au parcours complet, pas tous les achats du site.
- Les CSV exportés ne contiennent ni revenu ni coût média : ROAS et panier moyen ne sont pas calculables.
