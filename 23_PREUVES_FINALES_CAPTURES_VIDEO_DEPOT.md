# Preuves finales, captures, video et depot - Daylight / Cyber Trust

## Objectif

Ce livrable transforme les deux derniers points restants en actions concretes : prendre les captures Wazuh/pfSense et enregistrer la video 15-20 minutes. Il ne cree aucune preuve fictive ; il fournit une checklist exacte, une shotlist video et un controle automatique.

Fichiers associes :

| Fichier | Usage |
|---|---|
| `config/captures/daylight_capture_checklist.csv` | Liste exacte des captures attendues, responsables et priorites. |
| `config/video/daylight_video_shotlist.csv` | Decoupage video minute par minute, ecran a montrer et intervenant. |
| `tools/check_capture_pack.py` | Controle les fichiers `CAP-*.png` presents et genere un rapport. |
| `tools/render_static_proof_images.py` | Genere les preuves visuelles CAP-12 et CAP-13 depuis la topologie et la matrice pfSense. |
| `tools/build_offline_soc_dashboard.py` | Genere le dashboard offline HTML et les captures CAP-06, CAP-07, CAP-08, CAP-23. |
| `tools/render_preflight_evidence.py` | Produit CAP-25 seulement quand le preflight prouve le lab OK. |
| `tools/prepare_capture_session.ps1` | Enchaine les commandes utiles avant capture Wazuh/preflight. |
| `tools/check_video_ready.py` | Controle le lien YouTube ou le MP4 final avant depot. |
| `capture-pack-report.txt` | Rapport produit par le controle des captures. |

## 1. Commandes finales avant enregistrement

```powershell
python .\tools\generate_demo_logs.py
python .\tools\send_demo_logs_to_syslog.py --dry-run
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\preflight_demo.ps1 -WriteReport
python .\tools\check_capture_pack.py
```

Le preflight peut signaler Docker/Wazuh inaccessible si le lab n'est pas lance. Pendant l'enregistrement officiel, il faut lancer Docker/Wazuh avant de refaire le preflight.

## 2. Captures prioritaires

La liste complete est dans `config/captures/daylight_capture_checklist.csv`.

Captures minimales avant depot officiel :

| Priorite | Fichier | Responsable | Preuve |
|---:|---|---|---|
| 1 | `CAP-01_wazuh-dashboard-login.png` | Youssef | Wazuh accessible. |
| 1 | `CAP-02_agents-poste01-serveur01.png` | Youssef | Agents/sources visibles. |
| 1 | `CAP-03_alerte-5712-brute-force-ssh.png` | Youssef | Detection serveur. |
| 1 | `CAP-06_alerte-100120-acces-patient.png` | Kilyan | Donnees patients. |
| 1 | `CAP-07_dashboard-technique.png` | Kilyan | Dashboard analyste. |
| 1 | `CAP-08_dashboard-executif.png` | Kilyan | Vue client. |
| 1 | `CAP-13_pfsense-regles-firewall.png` | Yvan | Firewall concret. |
| 1 | `CAP-25_preflight-demo-ok.png` | Mahamadou | Exploitation lab. |

Objectif : au moins 8 captures de priorite 1 dans `Annexes_Captures/`.

## 3. Controle automatique des captures

Verifier les captures :

```powershell
python .\tools\check_capture_pack.py
```

Le script :

1. lit `config/captures/daylight_capture_checklist.csv` ;
2. cherche les fichiers dans `Annexes_Captures/` ;
3. genere `capture-pack-report.txt` ;
4. retourne un avertissement tant que les captures prioritaires ne sont pas presentes.

## 4. Shotlist video

La shotlist complete est dans `config/video/daylight_video_shotlist.csv`.

| Temps | Intervenant | Ecran principal | Objectif |
|---|---|---|---|
| 00:00 - 01:30 | Kilyan | Slide intro | Client, besoin, equipe. |
| 01:30 - 04:00 | Yvan | Architecture + pfSense | Segmentation et flux. |
| 04:00 - 08:30 | Youssef | Wazuh | Agents, alertes, RBAC. |
| 08:30 - 11:30 | Kilyan | Dashboards | Qualification et KPI. |
| 11:30 - 14:30 | Mahamadou | Runbook/REX | Exploitation et incidents. |
| 14:30 - 17:00 | Equipe | Synthese | Limites, couts, suite. |

## 5. Nommage video

Deux options selon consigne de depot :

| Option | Fichier / lien |
|---|---|
| YouTube non repertorie | Coller l'URL dans `PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_video-lien.txt`. |
| MP4 dans ZIP | `PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.mp4`. |

Ne pas laisser le TXT avec le texte `Coller ici` au moment du depot.

## 6. Procedure apres ajout des captures/video

1. Copier les captures dans `Annexes_Captures/`.
2. Coller le lien video dans le TXT ou ajouter le MP4.
3. Lancer :

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\post_capture_finalize.ps1
```

4. Verifier `validation-rendu-final.txt`.
5. Deposer le ZIP final.

## 7. Phrase propre si une capture manque

> La capture manquante est identifiee dans le rapport `capture-pack-report.txt`. Elle n'a pas ete remplacee par une image simulee ; elle doit etre reprise dans le lab Wazuh/pfSense avant depot officiel.





