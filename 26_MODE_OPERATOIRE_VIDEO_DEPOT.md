# Mode operatoire video et depot - Daylight / Cyber Trust

## Objectif

Ce document verrouille la derniere partie du rendu : enregistrer une video de 15 a 20 minutes, verifier que les quatre membres parlent, publier le lien YouTube non repertorie ou deposer un MP4, puis reconstruire le ZIP final.

La video n'est pas simulee par le projet. Elle doit etre enregistree par l'equipe. Les fichiers ci-dessous rendent le depot controlable :

| Fichier | Usage |
|---|---|
| `config/video/daylight_video_shotlist.csv` | Deroule minute par minute la video. |
| `config/video/daylight_video_recording_checklist.csv` | Checklist avant, pendant et apres enregistrement. |
| `config/video/daylight_video_obs_scenes.csv` | Scenes a suivre ou a creer dans OBS : timing, intervenant, overlay et fichier a ouvrir. |
| `config/video/daylight_video_evidence_map.csv` | Mapping entre chaque sequence video et la preuve/fichier a montrer. |
| `Dashboards_Offline/daylight_video_recording_pack.html` | Regie video locale avec scenes, overlays, checklist et commandes post-enregistrement. |
| `config/video/youtube_description_daylight.txt` | Description YouTube et chapitres prets a coller. |
| `tools/check_video_ready.py` | Controle le lien YouTube ou le MP4 final et produit `video-readiness-report.txt`. |
| `PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_video-lien.txt` | Fichier ou coller l'URL YouTube non repertoriee. |
| `28_RUNBOOK_EXPRESS_PREUVES_RESTANTES.md` | Procedure courte a suivre apres enregistrement. |
| `tools/post_capture_finalize.ps1` | Recontrole video, captures, PDF, ZIP et hash final. |

## 1. Preparation avant enregistrement

Ouvrir les ecrans dans cet ordre :

1. `Presentation_Daylight_CyberTrust.pptx` ;
2. `CAP-12_architecture-solution.png` ;
3. `CAP-13_pfsense-regles-firewall.png` ;
4. `https://localhost` si Wazuh est disponible ;
5. `Dashboards_Offline/daylight_soc_dashboard.html` en secours ;
6. `Dashboards_Offline/daylight_video_recording_pack.html` pour suivre les scenes et overlays ;
7. `21_DASHBOARDS_ALERTES_QUALIFICATION.md` ;
8. `22_EXPLOITATION_VM_RUNBOOK_REX.md` ;
9. `11_CHECKLIST_DEPOT_FINAL.md`.

Lancer le controle avant prise :

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\preflight_demo.ps1 -WriteReport
python .\tools\check_capture_pack.py
python .\tools\check_video_ready.py
```

## 2. Repartition exacte de parole

| Temps | Intervenant | Message a tenir | Ecran conseille |
|---|---|---|---|
| 00:00 - 01:30 | Kilyan | Client Daylight, besoin, objectifs, equipe Cyber Trust. | PowerPoint intro. |
| 01:30 - 04:00 | Yvan | Architecture, segmentation, pfSense, flux vers Wazuh. | Architecture + CAP-13. |
| 04:00 - 08:30 | Youssef | Wazuh, agents, alerte 5712, regles Daylight. | Wazuh CAP-01/02/03 ou dashboard offline si secours. |
| 08:30 - 11:30 | Kilyan | Dashboards, qualification, SLA, vue client. | CAP-07, CAP-08, CAP-06. |
| 11:30 - 14:30 | Mahamadou | Runbook VM, playbooks, REX, preflight. | Docs 03/22/25. |
| 14:30 - 17:00 | Equipe | Limites, couts, industrialisation, conclusion. | Rapport groupe + checklist. |

## 3. Texte court par membre

### Kilyan

Bonjour, nous sommes Cyber Trust. Nous presentons une solution SOC externalisee pour Daylight. L'objectif est de centraliser les logs, detecter les attaques, qualifier les alertes et donner au client des tableaux de bord lisibles.

### Yvan

L'architecture repose sur une segmentation claire : utilisateurs, serveurs, DMZ, management et SOC. pfSense applique les regles de filtrage, journalise les flux importants et transmet les evenements vers Wazuh pour correlation.

### Youssef

La partie SIEM s'appuie sur Wazuh. Nous montrons les agents, la collecte multi-source et les alertes. La regle `5712` illustre la brute force SSH, tandis que les regles `100xxx` couvrent les evenements metier Daylight.

### Kilyan, partie dashboards

La qualification priorise les alertes selon l'impact : patient, privilege, brute force, phishing ou reseau. Les dashboards permettent une vue technique pour les analystes et une vue executive pour Daylight.

### Mahamadou

Les playbooks transforment l'alerte en action : verifier, contenir, escalader, documenter. Le runbook explique aussi comment relancer le lab et conserver un REX exploitable apres incident.

### Conclusion equipe

La solution couvre la collecte, la detection, les dashboards, la qualification et les procedures. Les limites du lab sont connues, et le passage production passerait par un pilote multi-site puis une industrialisation progressive.

## 4. Publication YouTube non repertoriee

1. Exporter la video en MP4.
2. Envoyer sur YouTube.
3. Choisir visibilite `Non repertoriee`.
4. Copier l'URL dans :

```text
PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_video-lien.txt
```

5. Ne pas laisser la phrase `Coller ici` dans ce fichier.
6. Lancer :

```powershell
python .\tools\check_video_ready.py
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\post_capture_finalize.ps1
```

## 5. Option MP4 dans le ZIP

Si l'ecole demande un fichier MP4 plutot qu'un lien, placer le fichier a la racine avec l'un des noms suivants :

```text
PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.mp4
PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.mp4
```

Le script `check_video_ready.py` accepte un MP4 seulement s'il depasse 10 Mo, afin d'eviter de valider un mauvais export vide.

## 6. Controle final attendu

Apres ajout du lien ou du MP4 :

```powershell
python .\tools\check_video_ready.py
python .\tools\validate_rendu_final.py
```

Resultat attendu :

- `Lien YouTube : OK` ou `MP4 final : OK` ;
- plus de warning `Lien video` dans `validation-rendu-final.txt` ;
- ZIP final reconstruit avec le rapport `video-readiness-report.txt`.


