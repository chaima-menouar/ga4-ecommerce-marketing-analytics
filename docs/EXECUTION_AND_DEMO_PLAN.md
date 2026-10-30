# GA4 → BigQuery → ATLAS : exécution vérifiable

## 1. Pourquoi cette requête ?
Le jeu public GA4 e-commerce permet de mesurer les sessions, achats et revenus historiques par source/medium. Le projet reste un exercice analytique : les données sont obfusquées et datent de 2020–2021.

## 2. Exécution BigQuery
1. Ouvrir BigQuery Studio dans un projet Google Cloud avec accès BigQuery et facturation configurée.
2. Coller `sql/ga4_channel_performance_verified.sql` et afficher l'estimation de coût / bytes processed avant exécution.
3. Exécuter. Vérifier que des lignes sont retournées et sauvegarder une capture de la requête et du tableau.
4. Exporter les résultats en CSV; conserver le fichier brut et noter la date d'exécution.
5. Ne pas prétendre que ces chiffres sont issus de données 2026.

## 3. Attention aux KPI
- **Sessions** : couples distincts `user_pseudo_id + ga_session_id` avec identifiant de session présent.
- **Achats** : sessions avec au moins un événement `purchase` (pas nombre total de commandes).
- **Leads** : sessions avec `generate_lead`. Cet événement peut être absent du jeu e-commerce; des zéros sont donc possibles.
- **Revenu** : `ecommerce.purchase_revenue_in_usd` en **USD**, pas MAD.
- **Attribution** : source/medium récupérés de paramètres d'événement quand disponibles, sinon `traffic_source`. Ce n'est pas l'attribution officielle GA4 session-scoped.
- **ROAS** : impossible à calculer honnêtement sans coûts publicitaires. Le jeu public ne contient pas de dépenses marketing vérifiées.
- **Funnel** : `leads` n'est pas forcément une étape entre sessions et achats; ne pas imposer `purchases <= leads` sur des résultats GA4 réels.

## 4. Limite actuelle d'ATLAS
Le prototype CSV existant impose `sessions >= leads >= purchases`, un coût et des revenus en MAD. **Ne pas importer directement le CSV BigQuery dans ATLAS** : il faut un adaptateur de schéma et un mode analytique sans coût/lead. Sinon la démonstration serait trompeuse.

## 5. Démonstration devant la prof (4 min)
- 0:00–0:40 : expliquer le problème : mesurer la performance d'acquisition.
- 0:40–1:40 : montrer la requête BigQuery et les résultats réellement exécutés.
- 1:40–2:40 : montrer le tableau Looker Studio construit à partir de l'export réel, ou à défaut le CSV de résultats dans un tableur (ne pas appeler cela Looker Studio).
- 2:40–3:30 : montrer ATLAS avec `demo/data/experiment.csv` **explicitement étiqueté données de test synthétiques**.
- 3:30–4:00 : test négatif `invalid.csv` et limites (attribution, historique, coût).

## 6. Questions probables
**Pourquoi BigQuery ?** Pour analyser les événements GA4 par SQL de façon reproductible.

**Pourquoi un dataset public ?** Il permet une démonstration sans exposer de données privées.

**Pourquoi le ROAS n'est pas présenté sur le jeu réel ?** Il faut les dépenses marketing par canal; elles ne sont pas disponibles dans l'export GA4 public.

**Est-ce une IA ?** Non, cette partie est analytique SQL et simulation à règles. On ne présente pas d'IA entraînée.

## 7. À faire avant la soutenance
- [ ] Exécuter et valider la requête sur BigQuery.
- [ ] Vérifier noms et unités des colonnes dans le résultat.
- [ ] Construire et tester le dashboard Looker Studio.
- [ ] Enregistrer une courte vidéo de secours.
- [ ] Confirmer le sujet officiel et les critères de la prof.
