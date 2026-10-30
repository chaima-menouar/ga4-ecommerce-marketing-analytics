# Démonstration pratique — jeudi 5 novembre

## Objectif
Montrer un pipeline transparent **données agrégées → contrôle qualité → KPI → comparaison des canaux → simulation**. L'application est une démonstration locale; elle ne se connecte pas directement à GA4/BigQuery.

## Préparation
Ouvrir `demo/index.html` dans Chrome (ou via GitHub Pages si activé). Télécharger les deux fichiers CSV du dossier `demo/data`.

## Script et clics (4 minutes)

**0:00–0:40 — Problème.** « Une entreprise investit sur plusieurs canaux marketing, mais ne sait pas lesquels transforment réellement les visites en achats. Nous réunissons les mesures dans un tableau de bord vérifiable. » Montrer les cartes Sessions, Leads, Achats, Revenu.

**0:40–1:25 — Méthode.** « Chaque ligne correspond à un canal et contient sessions, leads, achats, revenu et coût. La conversion est achats divisés par sessions; le ROAS est revenu divisé par coût. Les données initiales sont synthétiques. » Montrer le tableau.

**1:25–2:15 — Test réel.** Cliquer **Importer CSV** → sélectionner `experiment.csv`. Montrer les valeurs attendues : **500 sessions, 70 leads, 15 achats, 15 000 MAD, 3 % de conversion, ROAS global = 5×**. « Les résultats ont été recalculés à partir du fichier importé, pas copiés dans le HTML. »

**2:15–2:45 — Contrôle qualité.** Importer `invalid.csv`. « Ce fichier annonce 15 achats pour 10 leads; notre validation le rejette sans effacer les données valides. » Vérifier que les KPI restent inchangés.

**2:45–3:30 — Scénario.** Choisir **Paid Search**, budget **5 000 MAD**, cliquer **Calculer**. Résultats attendus : revenu estimé **25 000 MAD**, achats théoriques **25**, ROAS **5×**. « Cette extrapolation suppose une performance stable, ce n'est pas une prévision certaine. »

**3:30–4:00 — Limites.** « Les données de démo sont synthétiques; pour une étude réelle, nous exécutons les requêtes SQL du dépôt sur le jeu public GA4 dans BigQuery, puis importons l'export agrégé. Les limites incluent attribution, consentement, données manquantes et coûts. »

## Fonctions à maîtriser
- `parseCSV(text)` : transforme un CSV simple en lignes numériques; vérifie colonnes, nombres et cohérence du funnel. Rejette le fichier complet si une ligne est incorrecte. Ce parseur pédagogique ne gère pas les CSV avec virgules entre guillemets.
- `render()` : recalcule les totaux et reconstruit cartes, barres, funnel et tableau depuis `rows`.
- `pct(a,b)` : retourne le pourcentage `a/b×100`; gère le dénominateur nul.
- `safe(s)` : échappe les caractères HTML dans les noms de canaux importés.
- Gestionnaire `change` : lit le fichier local et met à jour les données uniquement après validation.
- Gestionnaire `simulate` : multiplie le budget par le ROAS et le taux d'achats historiques du canal; ne prétend pas entraîner un modèle prédictif.
- Gestionnaire `export` : exporte les lignes agrégées courantes.

## Vérifications avant le cours
- [ ] Ouvrir le fichier HTML hors connexion.
- [ ] Importer `experiment.csv`, contrôler les 5 KPI.
- [ ] Importer `invalid.csv`, contrôler le message d'erreur et la conservation des KPI.
- [ ] Exécuter la simulation Paid Search.
- [ ] Exporter le CSV et vérifier le contenu.
- [ ] Garder une copie locale et une courte vidéo de secours.
- [ ] Envoyer slides, code, données et fiche d'une page avant la séance.

## À ne pas prétendre
Pas de synchronisation GA4 en direct, pas de requête BigQuery exécutée dans ce prototype, pas de modèle IA entraîné, pas de données client réelles. Les requêtes SQL du dépôt constituent le chemin d'intégration réel à exécuter et vérifier séparément.
