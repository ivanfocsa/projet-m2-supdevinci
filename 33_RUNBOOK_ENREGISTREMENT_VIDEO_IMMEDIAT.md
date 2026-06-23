# Runbook enregistrement video immediat - Daylight / Cyber Trust

## Objectif

Enregistrer une video de 15 a 20 minutes qui prouve le MVP Cyber Trust pour le client fictif Daylight : architecture, pfSense, Wazuh, alertes, dashboards, qualification, playbooks, REX et depot final.

Ce runbook est fait pour tourner la video tout de suite, sans improviser. Un membre partage son ecran, les autres prennent la parole dans l'ordre. La video finale doit etre publiee en YouTube non repertorie ou deposee en MP4 avec le nom attendu.

## Fichiers a ouvrir avant de lancer l'enregistrement

| Ordre | Fichier ou ecran | Usage pendant la video |
|---|---|---|
| 1 | `Presentation_Daylight_CyberTrust.pptx` | Introduction et fil conducteur. |
| 2 | `Dashboards_Offline/daylight_demo_control_center.html` | Centre de controle pour ouvrir toutes les preuves. |
| 3 | `Dashboards_Offline/daylight_pfsense_firewall_review.html` | Partie Yvan : pfSense, segmentation, tests. |
| 4 | `Dashboards_Offline/daylight_soc_dashboard.html` | Partie Kilyan : dashboards SOC, alertes, qualification. |
| 5 | `Dashboards_Offline/daylight_video_teleprompter.html` | Texte court par intervenant. |
| 6 | `Dashboards_Offline/daylight_video_recording_pack.html` | Scenes, preuves et checklist video. |
| 7 | `Annexes_Captures/CAP-25_preflight-demo-ok.png` | Preuve Docker/Wazuh OK. |
| 8 | `config/video/youtube_description_daylight.txt` | Description a coller sur YouTube. |

## Reglages OBS ou Teams

| Reglage | Valeur conseillee |
|---|---|
| Format | 1920x1080 si possible, sinon 1280x720. |
| Audio | Micro actif pour la personne qui parle ; couper les autres micros. |
| Capture | Partage ecran complet ou fenetre navigateur avec zoom 100 %. |
| Chronometre | Objectif 17 minutes, marge acceptee 15-20 minutes. |
| Nom des intervenants | Afficher les overlays PNG dans `Video_Overlays/` ou annoncer clairement le nom au debut de chaque segment. |

## Deroule minute par minute

| Temps | Intervenant | Ecran a montrer | Message attendu |
|---|---|---|---|
| 00:00-01:30 | Kilyan FELIX | `Presentation_Daylight_CyberTrust.pptx` | Presenter Daylight, le besoin SOC externalise, Cyber Trust, les quatre roles et le plan de demo. |
| 01:30-02:30 | Yvan FOCSA | `01_RAPPORT_TECHNIQUE_GROUPE.md` ou slide architecture | Expliquer l'architecture cible : sites Daylight, pfSense, Wazuh, sources de logs, dashboards et runbooks. |
| 02:30-04:00 | Yvan FOCSA | `daylight_pfsense_firewall_review.html` | Montrer les VLAN, regles firewall, NAT, flux syslog vers Wazuh et plan de tests pfSense. |
| 04:00-05:30 | Youssef GUERNIOU | `CAP-01`, `CAP-02` ou Wazuh live | Montrer l'acces Wazuh, les agents poste/serveur et la centralisation SIEM. |
| 05:30-07:00 | Youssef GUERNIOU | `CAP-03`, `CAP-05`, regles Wazuh | Montrer une alerte brute force SSH et les regles custom Daylight. |
| 07:00-08:30 | Youssef GUERNIOU | `CAP-09` | Expliquer le RBAC : admin, analyste, supervision lecture seule. |
| 08:30-10:00 | Kilyan FELIX | `daylight_soc_dashboard.html` ou `CAP-07` | Montrer le dashboard technique : severite, sources, top regles, timeline. |
| 10:00-11:30 | Kilyan FELIX | `21_DASHBOARDS_ALERTES_QUALIFICATION.md` | Qualifier une alerte : priorite, SLA, escalade, statut, responsable. |
| 11:30-13:00 | Mahamadou DIACOUMBA | `22_EXPLOITATION_VM_RUNBOOK_REX.md` et `CAP-25` | Montrer le runbook VM/lab, Docker/Wazuh OK et la relance preflight. |
| 13:00-14:30 | Mahamadou DIACOUMBA | `03_PLAYBOOKS_PROCEDURES_REX.md` | Presenter le playbook brute force, l'incident patient et le REX. |
| 14:30-16:00 | Yvan FOCSA | `14_SYNTHESE_EXECUTIVE_CLIENT.md` ou rapport groupe | Donner la conclusion architecture : couts, limites, industrialisation et pilote. |
| 16:00-17:00 | Equipe | `11_CHECKLIST_DEPOT_FINAL.md` puis ZIP/hash | Conclure : 39+ PDF, captures, CAP-25, hash, seule preuve finale video ajoutee apres upload. |

## Phrases courtes par role

### Kilyan FELIX

Je suis Kilyan, chef de projet detection et qualification. Je pilote le deroule, les criteres d'acceptation, les alertes metier, les dashboards et la logique de triage afin que Daylight puisse exploiter le SOC au quotidien.

### Yvan FOCSA

Je suis Yvan, architecte de la solution. Je presente l'architecture cible, la segmentation pfSense, les flux reseau, le lien syslog vers Wazuh et la logique d'industrialisation pour de nouveaux sites Daylight.

### Youssef GUERNIOU

Je suis Youssef, responsable SIEM et Wazuh. Je montre la collecte des logs, les agents, les alertes, les regles personnalisees et le controle d'acces par roles dans l'interface Wazuh.

### Mahamadou DIACOUMBA

Je suis Mahamadou, responsable exploitation lab, playbooks et REX. Je montre la relance des VM/conteneurs, le preflight Docker/Wazuh, les procedures d'incident et le retour d'experience.

## Preuves obligatoires a l'ecran

| Preuve | Pourquoi elle compte |
|---|---|
| `CAP-25_preflight-demo-ok.png` | Prouve Docker + Wazuh OK au moment du rendu. |
| `daylight_pfsense_firewall_review.html` | Prouve une solution firewall concrete, pas seulement conceptuelle. |
| `daylight_soc_dashboard.html` | Prouve les dashboards detection/qualification. |
| `local_rules_daylight_pfsense.xml` | Prouve les regles Wazuh personnalisables. |
| `daylight_alert_qualification_matrix.csv` | Prouve la qualification et l'exploitation SOC. |
| `03_PLAYBOOKS_PROCEDURES_REX.md` | Prouve les playbooks, procedures et REX. |
| `PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.zip.sha256` | Prouve l'integrite du depot final. |

## Apres l'enregistrement

1. Exporter la video en MP4 ou publier sur YouTube en non repertorie.
2. Si YouTube : coller l'URL dans `PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_video-lien.txt`.
3. Si MP4 : nommer le fichier `PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.mp4` et le placer a la racine du projet.
4. Relancer : `python .\tools\check_video_ready.py`.
5. Relancer : `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\post_capture_finalize.ps1 -AllowWarnings`.
6. Verifier que `validation-rendu-final.txt` ne contient plus de warning video.

## Titre YouTube conseille

`Projet M2 Cybersecurite - Daylight / Cyber Trust - Demonstrateur SOC Wazuh pfSense`

## Description courte a coller

Projet d'etude M2 Cybersecurite. Cyber Trust presente pour le client fictif Daylight une solution SOC externalisee concrete : architecture, pfSense, Wazuh, detection, dashboards, qualification, playbooks, exploitation VM et REX. Equipe : Yvan FOCSA, Youssef GUERNIOU, Kilyan FELIX, Mahamadou DIACOUMBA.

## Controle final attendu

Le rendu est complet quand ces deux lignes passent en OK :

```powershell
python .\tools\check_video_ready.py
python .\tools\validate_rendu_final.py
```

Sans lien YouTube ou MP4 final, le projet reste structurellement pret mais pas totalement pret pour depot officiel.
