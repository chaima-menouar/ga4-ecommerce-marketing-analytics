# Fiche projet — Mesure marketing GA4, BigQuery et Looker Studio

**Problématique.** Comment mesurer les visites, les achats et les étapes de conversion d'une boutique e-commerce pour identifier des pistes d'amélioration marketing ?

**Cas.** Export public GA4 obfusqué de Google Merchandise Store (novembre 2020 à janvier 2021).

**Outils.** BigQuery SQL (calculs), Streamlit + Plotly (prototype local), Looker Studio (livrable de visualisation à publier), GitHub (versionnement).

**Méthode.** Extraire les sessions par jour, les événements purchase et le revenu déclaré, regrouper les sessions par source d'acquisition du premier utilisateur, compter les sessions contenant des événements de parcours d'achat. Présenter les limites d'attribution et de séquentialité.

**Résultats réels.** À compléter après exécution vérifiée des requêtes BigQuery :
- Sessions : …
- Achats : …
- Revenu : … (devise à vérifier)
- Source principale : …
- Étape présentant la plus grande perte : … (sur un véritable funnel séquentiel si calculé)

**Trois recommandations à vérifier avec les données.**
1. Prioriser les canaux apportant des sessions acheteuses, en distinguant acquisition utilisateur et attribution session.
2. Auditer les étapes de panier et checkout avec un funnel ordonné avant d'attribuer les abandons à une cause.
3. Améliorer la qualité du marquage et le recueil du consentement, sans assimiler les données manquantes à zéro.

**Limites.** Données historiques, anonymisées, biais de consentement, absence de coût média, règles de session et d'attribution simplifiées.

**Liens.** Repository : https://github.com/chaima-menouar/ga4-ecommerce-marketing-analytics · Dashboard Looker Studio : à renseigner.
