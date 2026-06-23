# Dashboard SOC offline - Daylight / Cyber Trust

## Objectif

Ce livrable fournit une demonstration concrete des alertes, dashboards et qualifications SOC meme si le lab Wazuh n'est pas disponible au moment de la preparation. Il est genere depuis les fichiers de logs du projet et depuis la matrice de qualification Wazuh.

Il ne remplace pas les captures Wazuh finales `CAP-01`, `CAP-02` et `CAP-03`. Il sert de support demonstrable et de secours pour expliquer la logique metier au jury/client.

## Fichiers generes

| Fichier | Usage pendant la demo |
|---|---|
| `Dashboards_Offline/daylight_soc_dashboard.html` | Dashboard navigable hors-ligne avec KPI, timeline, top regles et qualification. |
| `Annexes_Captures/CAP-06_alerte-100120-acces-patient.png` | Fiche alerte acces patient, exploitable par Kilyan pour la qualification. |
| `Annexes_Captures/CAP-07_dashboard-technique.png` | Dashboard technique SOC : severites, sources, top regles, timeline. |
| `Annexes_Captures/CAP-08_dashboard-executif.png` | Dashboard executif Daylight : KPI client et incidents a commenter. |
| `Annexes_Captures/CAP-23_qualification-alerte-100120.png` | Capture optionnelle de qualification detaillee. |

## Sources de donnees

| Source | Role |
|---|---|
| `Demo_Logs/pfsense.log` | Evenements firewall : scan WAN, inter-VLAN, flux sortant volumineux. |
| `Demo_Logs/daylight_app.log` | Evenements applicatifs : auth failure, acces patient, export rendez-vous. |
| `Demo_Logs/ad_files.log` | Evenements AD/fichiers : groupe privilegie, partage patient, password spray. |
| `Demo_Logs/mail_phishing.log` | Evenements phishing : signalement, clic bloque. |
| `Demo_Logs/endpoint_usb.log` | Evenements endpoint : USB non autorise, processus non signe. |
| `config/wazuh/daylight_alert_qualification_matrix.csv` | SLA, checks, actions immediates et escalades. |

## Evenements couverts

| Regle | Scenario | Preuve concrete |
|---|---|---|
| `100110` | Brute force applicatif / password spray | `daylight_app.log`, `ad_files.log`. |
| `100120` | Acces anormal dossier patient | `CAP-06`, `CAP-23`, log patient access. |
| `100130` | Modification groupe privilegie | `ad_files.log`. |
| `100140` | USB non autorise | `endpoint_usb.log`. |
| `100150` | Phishing signale | `mail_phishing.log`. |
| `110010` | Scan WAN bloque | `pfsense.log`. |
| `110020` | Inter-VLAN vers MGMT/SERVERS | `pfsense.log`. |
| `110050` | Flux sortant volumineux | `pfsense.log`. |

## Commande de generation

```powershell
python .\tools\generate_demo_logs.py
python .\tools\build_offline_soc_dashboard.py
python .\tools\build_capture_annex.py
python .\tools\check_capture_pack.py
```

La commande est aussi integree dans `tools/finalize_project.ps1` pour que le ZIP final embarque automatiquement le HTML et les captures de dashboard.

## Sequence de presentation conseillee

| Intervenant | Ecran | Message |
|---|---|---|
| Kilyan | `CAP-08_dashboard-executif.png` | Vue client : nombre d'alertes, critiques, donnees patients, blocages reseau. |
| Kilyan | `CAP-07_dashboard-technique.png` | Vue analyste : severites, sources, top regles, timeline. |
| Kilyan | `CAP-06_alerte-100120-acces-patient.png` | Qualification de l'incident patient avec SLA 15 minutes. |
| Mahamadou | `CAP-23_qualification-alerte-100120.png` | Procedure de traitement, escalade et REX. |
| Yvan | `CAP-13_pfsense-regles-firewall.png` | Lien entre segmentation pfSense et alertes reseau `110010/110020/110050`. |

## Limites annoncees proprement

- Le dashboard offline est base sur les logs de demonstration du dossier.
- Les captures Wazuh natives doivent encore etre prises quand le lab est lance.
- Les preuves offline ne sont pas de fausses captures Wazuh : elles sont des exports demonstrables, reproductibles et coherents avec les regles Wazuh preparees.

Phrase orale utile :

> Si Wazuh est disponible pendant la demo, nous montrons les memes evenements directement dans Wazuh. Si le lab est indisponible, ce dashboard offline permet de prouver la logique SOC a partir des logs et de la matrice de qualification.
