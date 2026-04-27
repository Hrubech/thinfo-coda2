# Rapport d'audit DevSecOps — Krypto SAS

**Étudiant(e) :** ___________________________  
**Date :** ___________________________  
**Promotion :** M1 Cybersécurité  

---

## Partie 1 — Fiches de vulnérabilités

---

### VULN-01

| Champ | Valeur |
|---|---|
| Fichier & ligne | |
| Nom | |
| CWE | |
| Score CVSS v3.1 | |
| Vecteur CVSS | |

**Description :**  
_(3 à 5 lignes d'explication technique)_

**Preuve d'exploitabilité :**  
```
# Commande ou payload ici
```

**Impact :**  
_(Ce qu'un attaquant peut faire concrètement)_

---

### VULN-02

| Champ | Valeur |
|---|---|
| Fichier & ligne | |
| Nom | |
| CWE | |
| Score CVSS v3.1 | |
| Vecteur CVSS | |

**Description :**  

**Preuve d'exploitabilité :**  
```

```

**Impact :**  

---

### VULN-03

| Champ | Valeur |
|---|---|
| Fichier & ligne | |
| Nom | |
| CWE | |
| Score CVSS v3.1 | |
| Vecteur CVSS | |

**Description :**  

**Preuve d'exploitabilité :**  
```

```

**Impact :**  

---

### VULN-04

| Champ | Valeur |
|---|---|
| Fichier & ligne | |
| Nom | |
| CWE | |
| Score CVSS v3.1 | |
| Vecteur CVSS | |

**Description :**  

**Preuve d'exploitabilité :**  
```

```

**Impact :**  

---

### VULN-05

| Champ | Valeur |
|---|---|
| Fichier & ligne | |
| Nom | |
| CWE | |
| Score CVSS v3.1 | |
| Vecteur CVSS | |

**Description :**  

**Preuve d'exploitabilité :**  
```

```

**Impact :**  

---

## Partie 2 — Fichiers corrigés

> Joindre les fichiers corrigés dans l'archive ZIP.  
> Résumer ici les principales modifications apportées.

### Modifications dans `ci-secure.yml`

- [ ] Secrets déplacés dans GitHub Secrets
- [ ] Bloc `permissions:` ajouté
- [ ] Scan SAST (Bandit ou Semgrep) intégré
- [ ] Scan SCA (OWASP DC ou pip-audit) intégré
- [ ] Scan image Docker (Trivy) intégré
- [ ] Utilisateur non-root pour le déploiement SSH

### Modifications dans `app_secure.py`

- [ ] Route `/ping` — shell=True remplacé par liste d'arguments
- [ ] Route `/ping` — validation de l'entrée par liste blanche
- [ ] Route `/load` — pickle remplacé par JSON
- [ ] `debug=False` et bind sur `127.0.0.1`

---

## Partie 3 — Note de synthèse pour le CTO

_(1 page maximum, ton adapté à un non-technicien)_

**À : CTO de Krypto SAS**  
**De :** ___________________________  
**Objet :** Résultats de l'audit de sécurité DevSecOps — Pipeline CI/CD et API backend

---

_(Votre synthèse ici)_

---

*Rapport rédigé dans le cadre du TP DevSecOps — M1 Cybersécurité*
