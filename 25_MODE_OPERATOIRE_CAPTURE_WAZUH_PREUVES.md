# Mode operatoire captures Wazuh et preflight - Daylight / Cyber Trust

## Objectif

Ce document sert a produire ou regenerer les preuves prioritaires Wazuh/preflight sans improviser. Les captures `CAP-01`, `CAP-02` et `CAP-03` peuvent etre isolees depuis la documentation SIEM de Youssef ; `CAP-25` doit toujours venir du preflight reel Docker/Wazuh.

| Capture | Responsable | Preuve attendue |
|---|---|---|
| `CAP-01_wazuh-dashboard-login.png` | Youssef | Wazuh Dashboard accessible et connecte. |
| `CAP-02_agents-poste01-serveur01.png` | Youssef | Agents `poste-01` et `serveur-01` visibles/actifs. |
| `CAP-03_alerte-5712-brute-force-ssh.png` | Youssef | Alerte Wazuh `5712` brute force SSH ouverte en detail. |
| `CAP-25_preflight-demo-ok.png` | Mahamadou | Preflight apres relance lab : Docker et Wazuh OK. |

Les fichiers associes sont :

| Fichier | Usage |
|---|---|
| `tools/prepare_capture_session.ps1` | Commande guidee pour preparer la session de capture. |
| `tools/render_preflight_evidence.py` | Genere `CAP-25` seulement si le preflight prouve Docker + Wazuh OK. |
| `tools/extract_youssef_wazuh_proofs.py` | Extrait `CAP-01`, `CAP-02`, `CAP-03` et plusieurs preuves optionnelles depuis le PDF SIEM de Youssef. |
| `config/captures/daylight_remaining_priority_captures.csv` | Mini-checklist de la preuve prioritaire restante (`CAP-25`). |
| `preflight-evidence-report.txt` | Rapport expliquant si `CAP-25` est valide ou non. |
| `28_RUNBOOK_EXPRESS_PREUVES_RESTANTES.md` | Procedure courte pour terminer captures, video, ZIP et hash. |
| `tools/post_capture_finalize.ps1` | Reconstruction finale apres ajout des preuves reelles. |


## 0. Regeneration depuis les preuves SIEM existantes

Si Wazuh n'est pas disponible mais que le dossier doit rester montrable, regenerer les preuves deja presentes dans la documentation SIEM :

```powershell
python .\tools\extract_youssef_wazuh_proofs.py
python .\tools\build_capture_annex.py
```

Cette commande ne fabrique pas de faux Wazuh : elle extrait les captures integrees dans `Youssef GUERNIOU/Documentation_SIEM_Youssef_GUERNIOU.pdf` et ajoute une note de tracabilite dans `Annexes_Captures/README_PREUVES_WAZUH_EXTRAITES.md`.
## 1. Preparation rapide

Depuis la racine du projet :

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\prepare_capture_session.ps1
```

Cette commande :

1. regenere les logs de demonstration ;
2. regenere les images architecture/pfSense ;
3. regenere le dashboard SOC offline ;
4. fait un dry-run des logs ;
5. lance le preflight ;
6. tente de produire la preuve preflight ;
7. affiche les captures restantes.

## 2. Variante avec lab Wazuh deja pret

Si Docker Desktop est lance et que le lab Wazuh est disponible depuis cette racine :

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\prepare_capture_session.ps1 -StartLab -RunYoussefSetup -OpenBrowser
```

Si le lab Wazuh est dans une autre racine, lancer d'abord le lab dans son dossier technique, puis revenir ici et lancer :

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\prepare_capture_session.ps1 -RunYoussefSetup -OpenBrowser
```

## 3. CAP-01 - Wazuh Dashboard connecte

1. Ouvrir `https://localhost`.
2. Se connecter avec le compte de demonstration : `admin / SecretPassword`.
3. Capturer la page connectee Wazuh Dashboard.
4. Enregistrer dans :

```text
Annexes_Captures/CAP-01_wazuh-dashboard-login.png
```

Ce que le jury doit voir : interface Wazuh chargee, session connectee, pas seulement une page de login vide.

## 4. CAP-02 - Agents poste-01 et serveur-01

1. Dans Wazuh, ouvrir la vue des agents.
2. Montrer `poste-01` et `serveur-01`.
3. Si possible, montrer l'etat actif ou recent.
4. Enregistrer dans :

```text
Annexes_Captures/CAP-02_agents-poste01-serveur01.png
```

Si `serveur-01` est absent, relancer :

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File ".\Youssef GUERNIOU\setup-siem-lab.ps1"
```

## 5. CAP-03 - Alerte 5712 brute force SSH

1. Dans Wazuh, ouvrir les evenements de securite.
2. Chercher :

```text
rule.id:5712
```

3. Ouvrir le detail d'une alerte `5712`.
4. Montrer au minimum : regle `5712`, cible `serveur-01`, horodatage, source ou utilisateur.
5. Enregistrer dans :

```text
Annexes_Captures/CAP-03_alerte-5712-brute-force-ssh.png
```

Si aucune alerte n'apparait, relancer la simulation brute force via le script de Youssef, attendre 1 a 3 minutes, puis refaire la recherche.

## 6. CAP-25 - Preflight demo OK

`CAP-25` ne doit pas etre cree manuellement si Docker/Wazuh ne sont pas OK. La commande suivante lit `preflight-demo-report.txt` et cree l'image uniquement si le rapport prouve Docker + Wazuh accessibles :

```powershell
python .\tools\render_preflight_evidence.py
```

Resultats possibles :

| Resultat | Signification |
|---|---|
| `Annexes_Captures/CAP-25_preflight-demo-ok.png` | Lab OK, preuve prioritaire valide. |
| `Annexes_Captures/PRE-25_preflight-a-reprendre.png` | Lab pas encore OK, preuve non valide pour depot. |

Pour produire `CAP-25` :

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\preflight_demo.ps1 -WriteReport
python .\tools\render_preflight_evidence.py
python .\tools\check_capture_pack.py
```

## 7. Finalisation apres captures

Quand `CAP-25` existe et que `CAP-01`, `CAP-02`, `CAP-03` sont presentes ou recapturees :

```powershell
python .\tools\build_capture_annex.py
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\post_capture_finalize.ps1
python .\tools\validate_rendu_final.py
```

Validation attendue :

- `Captures/preuves prioritaires - 8/8 prioritaires presentes` ;
- lien video renseigne ;
- aucun fichier obligatoire manquant dans le ZIP.

## Phrase de defense si le lab tombe

> Les preuves Wazuh prioritaires ont ete isolees depuis la documentation SIEM de Youssef, qui contient les captures originales du lab. Pour une demonstration live, nous pouvons recapturer les memes ecrans dans Wazuh ; `CAP-25` reste volontairement dependante du preflight reel Docker/Wazuh.


