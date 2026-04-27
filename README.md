# TP DevSecOps — M1 Cybersécurité
## Audit d'un pipeline CI/CD et d'une API Python vulnérables

---

**Durée :** 2h  
**Niveau :** M1 Cybersécurité  
**Rendu :** rapport PDF + fichiers corrigés zippés  

---

## Contexte

Vous venez d'être recruté comme **Security Engineer** chez *Krypto SAS*, une startup qui développe des outils de monitoring réseau.

L'équipe de développement vient de vous soumettre deux fichiers pour revue avant mise en production :
- Le pipeline CI/CD GitHub Actions (`.github/workflows/ci.yml`)
- L'API backend Python Flask (`app/app.py`)

Votre mission : **auditer ces fichiers, identifier toutes les vulnérabilités, expliquer les risques, et proposer les versions corrigées**.

---

## Structure du dépôt fourni

```
tp_devsecops/
├── README.md                  ← ce fichier (énoncé)
├── .github/
│   └── workflows/
│       └── ci.yml             ← pipeline vulnérable à auditer
├── app/
│   ├── app.py                 ← API Flask vulnérable à auditer
│   ├── requirements.txt       ← dépendances Python
│   └── Dockerfile             ← image Docker
├── rapport_template.md        ← template de rapport
└── grille_evaluation.md       ← critères de notation
```

---

## Travail demandé

### Partie 1 — Audit (8 pts)

Pour **chaque vulnérabilité** identifiée, rédiger une fiche de vulnérabilité contenant :

| Champ | Contenu attendu |
|---|---|
| Identifiant | ex. VULN-01 |
| Fichier & ligne | ex. `ci.yml`, ligne 11 |
| Nom de la vulnérabilité | ex. Exposition de secrets |
| Classification | CWE-xxx |
| Score CVSS v3.1 | Score + vecteur complet |
| Description | Explication technique en 3-5 lignes |
| Preuve d'exploitabilité | Payload ou démonstration concrète |
| Impact | Ce qu'un attaquant peut faire |

### Partie 2 — Remédiation (8 pts)

Fournir les **fichiers corrigés et commentés** :
- `.github/workflows/ci-secure.yml` — pipeline corrigé
- `app/app_secure.py` — API corrigée

Chaque correction doit être **commentée dans le code** (`# CORRECTION : explication`).

### Partie 3 — Synthèse (4 pts)

Rédiger une **note de synthèse** (1 page max) à destination du CTO de Krypto SAS :
- Résumé des risques identifiés par ordre de priorité
- Recommandations pour améliorer la posture DevSecOps globale
- Proposition d'intégration d'outils dans le pipeline (avec justification)

---

## Outils autorisés

Vous pouvez utiliser les outils suivants pour valider votre analyse :

```bash
# Analyse statique Python
pip install bandit
bandit -r app/ -ll

# Scan de dépendances
pip install pip-audit
pip-audit -r app/requirements.txt

# Scan d'image Docker (si Docker installé)
trivy image --severity HIGH,CRITICAL <nom_image>

# Recherche de secrets
pip install detect-secrets
detect-secrets scan .
```

---

## Critères de notation

Voir `grille_evaluation.md` pour le détail.

**Barème rapide :**
- Identification des vulnérabilités : 8 pts
- Qualité des corrections : 8 pts  
- Note de synthèse CTO : 4 pts
- Bonus CVSS calculé + justifié : +1 pt

---

## Rendu

- Format : archive ZIP nommée `NOM_Prenom_TP_DevSecOps.zip`
- Contenu : rapport PDF + fichiers corrigés
- Délai : **fin de séance ou 48h par mail**

> **Rappel éthique :** Les techniques d'exploitation vues dans ce TP ne doivent être utilisées que sur des environnements de test avec autorisation explicite. Toute exploitation non autorisée est illégale (loi Godfrain, art. 323-1 CP).
