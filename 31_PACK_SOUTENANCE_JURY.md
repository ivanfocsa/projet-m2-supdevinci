# Pack soutenance jury - Daylight / Cyber Trust

## Objectif

Ce document donne a l'equipe une fiche courte pour defendre le projet devant le jury : parcours de demonstration, questions probables, reponses courtes et preuves a ouvrir.

## Parcours demo recommande

| # | Owner | Ouvrir | Message | Plan B |
|---|---|---|---|---|
| 01 | Kilyan FELIX | `Presentation/Presentation_Daylight_CyberTrust.pptx` | Contexte Daylight, objectif Cyber Trust, roles de l'equipe. | `06_SUPPORT_PRESENTATION.md` |
| 02 | Yvan FOCSA | `Annexes_Captures/CAP-12_architecture-solution.png` | Architecture cible, segmentation et sources raccordees. | `01_RAPPORT_TECHNIQUE_GROUPE.md` |
| 03 | Yvan FOCSA | `Dashboards_Offline/daylight_pfsense_firewall_review.html` | pfSense concret : interfaces, NAT, regles, logs et tests. | `Config_PfSense/pfsense_firewall_rules.csv` |
| 04 | Youssef GUERNIOU | `Annexes_Captures/CAP-01_wazuh-dashboard-login.png` | Acces Wazuh, agents et preuves SIEM disponibles. | `Preuves_SIEM_Youssef/Documentation_SIEM_Youssef_GUERNIOU.pdf` |
| 05 | Youssef GUERNIOU | `Annexes_Captures/CAP-03_alerte-5712-brute-force-ssh.png` | Detection brute force SSH et logique de regles. | `Config_Wazuh/local_rules_daylight_pfsense.xml` |
| 06 | Kilyan FELIX | `Dashboards_Offline/daylight_soc_dashboard.html` | Dashboard technique, dashboard executif et qualification. | `21_DASHBOARDS_ALERTES_QUALIFICATION.md` |
| 07 | Mahamadou DIACOUMBA | `03_PLAYBOOKS_PROCEDURES_REX.md` | Playbook, procedure, REX et exploitation VM/lab. | `22_EXPLOITATION_VM_RUNBOOK_REX.md` |
| 08 | Equipe Cyber Trust | `Dashboards_Offline/daylight_demo_control_center.html` | Etat final, preuves restantes, ZIP, hash, limites honnetes. | `30_TABLEAU_BORD_STATUT_FINAL.md` |

## Questions jury et reponses

| Theme | Question | Reponse courte | Intervenant | Preuve |
|---|---|---|---|---|
| Besoin client | Pourquoi Daylight a besoin d'un SOC externalise ? | Daylight manipule des donnees patients sur plusieurs centres. Cyber Trust apporte une surveillance centralisee, des alertes qualifiees, des dashboards et des procedures sans imposer a Daylight de creer tout de suite un SOC interne. | Kilyan FELIX | `14_SYNTHESE_EXECUTIVE_CLIENT.md` |
| Architecture | Pourquoi pfSense dans votre solution ? | pfSense apporte une brique concrete de segmentation : VLAN, NAT, refus par defaut, journalisation des flux et envoi syslog vers Wazuh. La revue firewall montre exactement les regles et les tests attendus. | Yvan FOCSA | `Dashboards_Offline/daylight_pfsense_firewall_review.html` |
| Architecture | Votre lab est-il une architecture de production ? | Non. Le lab prouve la faisabilite. En production, nous separons manager, indexer, dashboard, stockage, sauvegarde, haute disponibilite, supervision et gestion des secrets. | Yvan FOCSA | `01_RAPPORT_TECHNIQUE_GROUPE.md` |
| SIEM | Pourquoi Wazuh ? | Wazuh est open-source, compatible agents et syslog, et assez complet pour couvrir endpoint, serveur, application, firewall, RBAC et dashboards dans un demonstrateur realiste sans cout de licence SIEM. | Youssef GUERNIOU | `Youssef GUERNIOU/Documentation_SIEM_Youssef_GUERNIOU.pdf` |
| Detection | Quelles alertes sont vraiment demontrees ? | Nous montrons 5712 pour brute force SSH, 100120 pour acces anormal a un dossier patient, 110020 pour mouvement lateral firewall, et les regles Daylight autour de l'application, des privileges, du phishing et des endpoints. | Kilyan FELIX | `21_DASHBOARDS_ALERTES_QUALIFICATION.md` |
| Dashboards | Pourquoi deux dashboards ? | Le dashboard technique aide l'analyste a investiguer. Le dashboard executif aide Daylight a piloter le service. Les deux vues servent des publics differents. | Kilyan FELIX | `Dashboards_Offline/daylight_soc_dashboard.html` |
| Exploitation | Que faire si Docker ou Wazuh ne demarre pas pendant la soutenance ? | On ne simule pas une preuve live. On montre le preflight, le rapport d'echec, la commande de relance, les captures deja extraites du dossier SIEM, le dashboard offline et la procedure CAP-25. | Mahamadou DIACOUMBA | `Rapports_Preflight/preflight-demo-report.txt` |
| Playbooks | Comment passez-vous d'une alerte a une action ? | Chaque alerte a une qualification, un SLA, des verifications, une action immediate, une escalade et un REX. Les playbooks evitent que l'analyste improvise. | Mahamadou DIACOUMBA | `03_PLAYBOOKS_PROCEDURES_REX.md` |
| RGPD | Comment limitez-vous les risques RGPD ? | Nous appliquons minimisation, RBAC, retention limitee, journalisation des consultations et dashboards qui evitent d'exposer des donnees patients completes au public executif. | Yvan FOCSA | `12_RISQUES_RGPD_CONFORMITE.md` |
| Video | Comment prouver que toute l'equipe a participe ? | Le shotlist, le pack d'enregistrement, les overlays nom/role et les rapports individuels associent chaque sequence a un intervenant et a une preuve ouverte a l'ecran. | Equipe Cyber Trust | `Dashboards_Offline/daylight_video_recording_pack.html` |

## Phrase si Docker/Wazuh ne repond pas

> Nous ne presentons pas une capture live fabriquee. Le preflight montre que Docker/Wazuh ne repond pas sur cette machine a cet instant. Nous avons donc deux preuves honnetes : les captures SIEM deja extraites du dossier de Youssef, et les supports reproductibles qui montrent comment relancer le lab et produire CAP-25 quand Docker/Wazuh sont disponibles.

## Commandes de cloture

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\repair_lab_and_capture_cap25.ps1 -StartDockerDesktop -StartKnownContainers -WaitSeconds 180
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\import_final_evidence.ps1 -Item VIDEO-LINK -YoutubeUrl "https://youtu.be/xxxx" -RunChecks
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\post_capture_finalize.ps1 -AllowWarnings
```
