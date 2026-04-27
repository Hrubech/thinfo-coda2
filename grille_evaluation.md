# Grille d'évaluation — TP DevSecOps M1 Cyber

**Total : 20 points + 1 bonus**

---

## Partie 1 — Audit des vulnérabilités (8 pts)

| # | Vulnérabilité | Points | Critères |
|---|---|---|---|
| VULN-01 | Secrets en clair dans le pipeline | 2 pts | Fichier + ligne identifiés, CWE-312 mentionné, impact expliqué |
| VULN-02 | Permissions GITHUB_TOKEN trop larges | 2 pts | Absence de bloc `permissions:` relevée, risque de pivot expliqué |
| VULN-03 | Absence de scan SCA/SAST/image | 2 pts | Au moins 2 types de scan manquants cités avec outils correspondants |
| VULN-04 | Injection de commande OS (RCE) | 1 pt | `shell=True` identifié, payload d'exploitation fourni |
| VULN-05 | Désérialisation pickle non sécurisée | 1 pt | CWE-502 ou OWASP A08 mentionné, risque expliqué |

---

## Partie 2 — Remédiation (8 pts)

| Correction | Points | Critères |
|---|---|---|
| Secrets déplacés dans GitHub Secrets | 2 pts | Syntaxe `${{ secrets.NOM }}` correcte, `--password-stdin` utilisé |
| Bloc `permissions:` ajouté avec moindre privilège | 2 pts | `contents: read` minimum, justification présente |
| Bandit ET Trivy intégrés dans le pipeline | 2 pts | Les deux outils présents, `exit-code: 1` ou équivalent sur Trivy |
| `app.py` corrigé — RCE + pickle | 2 pts | Liste d'arguments subprocess, validation regex, JSON à la place de pickle |

**Malus :** -1 pt si le code corrigé est syntaxiquement incorrect ou non fonctionnel.

---

## Partie 3 — Note de synthèse CTO (4 pts)

| Critère | Points |
|---|---|
| Vulnérabilités classées par priorité (criticité) | 1 pt |
| Recommandations concrètes et réalistes | 1 pt |
| Proposition d'outillage DevSecOps justifiée | 1 pt |
| Clarté, concision, ton adapté à un non-technicien | 1 pt |

---

## Bonus (1 pt)

**+1 pt** : Score CVSS v3.1 complet pour la VULN-04 (RCE) avec vecteur justifié métrique par métrique (AV/AC/PR/UI/S/C/I/A).

Score attendu : **9.8 CRITIQUE** — `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H`

---

## Barème global

| Note | Seuil |
|---|---|
| Très bien (≥16) | Toutes les vulnérabilités trouvées, corrections fonctionnelles, synthèse claire |
| Bien (13-15) | 4/5 vulnérabilités, corrections correctes avec quelques imprécisions |
| Passable (10-12) | 3/5 vulnérabilités, corrections partielles |
| Insuffisant (<10) | Moins de 3 vulnérabilités ou corrections non fonctionnelles |
