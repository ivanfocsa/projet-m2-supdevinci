# Runbook express preuves restantes - Daylight / Cyber Trust

## Objectif 10 minutes

Ce document sert au jour de finalisation. Il ne remplace pas les modes operatoires detailles : il donne l'ordre exact pour terminer le depot sans perdre de temps.

## Etat actuel attendu

| Element | Etat |
|---|---|
| PDF groupe et individuels | Deja generes. |
| pfSense, Wazuh rules, logs demo, dashboard offline | Deja presents. |
| Captures prioritaires deja presentes | `CAP-01`, `CAP-02`, `CAP-03`, `CAP-06`, `CAP-07`, `CAP-08`, `CAP-13`. |
| Capture prioritaire restante | `CAP-25_preflight-demo-ok.png`. |
| Video restante | Lien YouTube non repertorie ou MP4 final. |


## 0. Preuves Wazuh deja isolees depuis le PDF SIEM

Les captures `CAP-01`, `CAP-02` et `CAP-03` ont ete extraites depuis `Youssef GUERNIOU/Documentation_SIEM_Youssef_GUERNIOU.pdf`, qui contient les captures Wazuh originales du perimetre SIEM. Pour les regenerer :

```powershell
python .\tools\extract_youssef_wazuh_proofs.py
```

Pour une video ou une soutenance live, il reste preferable de recapturer les memes ecrans directement dans Wazuh si Docker et le dashboard repondent.
## 1. Lancer l'environnement reel

1. Ouvrir Docker Desktop et attendre que le moteur reponde.
2. Depuis la racine technique du lab Wazuh, demarrer Wazuh si necessaire.
3. Revenir dans ce dossier projet :

```powershell
cd "C:\Users\Ivan\Pictures\PROJET M2"
```

4. Lancer le setup SIEM de Youssef :

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File ".\Youssef GUERNIOU\setup-siem-lab.ps1"
```

5. Controler le preflight :

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\preflight_demo.ps1 -WriteReport
```

## 2. Produire la capture prioritaire restante ou recapturer Wazuh

| Ordre | Fichier exact | Responsable | Ecran a capturer |
|---:|---|---|---|
| 1 | `Annexes_Captures/CAP-01_wazuh-dashboard-login.png` | Youssef | `https://localhost`, session Wazuh connectee `admin / SecretPassword`. |
| 2 | `Annexes_Captures/CAP-02_agents-poste01-serveur01.png` | Youssef | Wazuh > Agents, `poste-01` et `serveur-01` visibles/actifs. |
| 3 | `Annexes_Captures/CAP-03_alerte-5712-brute-force-ssh.png` | Youssef | Security events, recherche `agent.name: serveur-01 AND (rule.id:5710 OR rule.id:5503 OR rule.id:5551 OR rule.id:5763 OR rule.id:5712)`, detail d'alerte ouvert. |
| 4 | `Annexes_Captures/CAP-25_preflight-demo-ok.png` | Mahamadou | Generee par `tools\repair_lab_and_capture_cap25.ps1` seulement si Docker + Wazuh OK. |

Commande pour tenter la capture restante `CAP-25` apres preflight OK :

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\repair_lab_and_capture_cap25.ps1 -StartDockerDesktop -StartKnownContainers -WaitSeconds 180
```

Si le lab de Youssef doit etre initialise, utiliser ensuite :

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\repair_lab_and_capture_cap25.ps1 -RunYoussefSetup -StartKnownContainers -WaitSeconds 180
```

Si `PRE-25_preflight-a-reprendre.png` est cree au lieu de `CAP-25`, Docker ou Wazuh n'est pas encore pret. Le rapport `lab-cap25-recovery-report.txt` indique l'etape qui bloque.

## 3. Verifier les captures
Avant le controle, il est possible d'importer une capture prise manuellement avec `tools/import_final_evidence.ps1`, par exemple :

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\import_final_evidence.ps1 -Item CAP-01 -SourcePath "C:\Temp\capture-wazuh-login.png" -RunChecks
```


```powershell
python .\tools\check_capture_pack.py
```

Resultat attendu avant depot officiel :

```text
Captures prioritaires presentes : 8/8
```

## 4. Ajouter la video

Option recommandee : YouTube non repertorie.

1. Enregistrer la video 15-20 minutes avec les 4 membres.
2. Publier en `Non repertoriee`.
3. Coller l'URL dans :

```text
PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_video-lien.txt
```

Controle :

```powershell
python .\tools\check_video_ready.py
```

Resultat attendu : `Lien YouTube : OK` ou `MP4 final : OK`.

## 5. Reconstruction finale en une commande

Quand `CAP-25` et la video sont la :

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\post_capture_finalize.ps1
```

Ce script reconstruit l'annexe captures, les PDF, le dossier groupe complet, le manifeste, le ZIP et le hash SHA-256.

## 6. Critere final

Le depot est pret uniquement quand la validation affiche :

```text
[OK] Rendu final complet selon les controles automatises.
```

Tant que la validation affiche les warnings `CAP-25`/video, le dossier reste montrable en soutenance de preparation mais pas totalement pret pour depot officiel.


