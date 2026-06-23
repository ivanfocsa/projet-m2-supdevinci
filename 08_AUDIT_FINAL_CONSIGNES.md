# Audit final des consignes - Daylight / Cyber Trust

## Objectif

Ce document verifie la couverture des consignes du cadre pedagogique et du cahier des charges. Il distingue ce qui est deja produit dans le dossier de ce qui doit encore etre prouve par une capture ou par la video.

## Sources de reference

| Source | Role |
|---|---|
| `Cadre Pedagogique - Projet Etude - CS - 2025[26].pdf` | Modalites d'evaluation, rapport, video, rendus individuels. |
| `Cahier des charges - Projet Etude - M2 - CS - 2025[41].pdf` | Attendus SOC externalise Daylight. |
| `Youssef GUERNIOU/Documentation_SIEM_Youssef_GUERNIOU.pdf` | Preuves techniques SIEM deja presentes. |

## Audit des livrables pedagogiques

| Exigence | Statut dossier | Preuve |
|---|---|---|
| Rapport technique complet groupe | Pret | `01_RAPPORT_TECHNIQUE_GROUPE.md` + PDF groupe |
| Rendu individuel Yvan | Pret | `Yvan FOCSA/PE-2526_M2CS_YvanFOCSA.md` + PDF |
| Rendu individuel Youssef | Pret | `Youssef GUERNIOU/PE-2526_M2CS_YoussefGUERNIOU.md` + PDF |
| Rendu individuel Kilyan | Pret | `Kilyan FELIX/PE-2526_M2CS_KilyanFELIX.md` + PDF |
| Rendu individuel Mahamadou | Pret | `Mahamadou DIACOUMBA/PE-2526_M2CS_MahamadouDIACOUMBA.md` + PDF |
| Gestion des couts M2 | Pret | Section 9 du rapport groupe |
| Organisation / planning / methodologie | Pret | `05_BACKLOG_PLANNING.md` + rapport groupe |
| Documentation technique et utilisateur | Pret | `02_GUIDE_DEPLOIEMENT_UTILISATION.md` |
| REX incidents | Pret | `03_PLAYBOOKS_PROCEDURES_REX.md` |
| Video 15-20 min avec tous les membres | Prepare, a enregistrer | `04_SCRIPT_VIDEO_DEMO.md`, `06_SUPPORT_PRESENTATION.md`, fichier lien TXT |
| Mode operatoire demo et preflight | Pret | `10_MODE_OPERATOIRE_DEMO_JOUR_J.md`, `tools/preflight_demo.ps1` |
| Nomenclature ZIP | Preparee avec code provisoire `M2CS` | Archive `PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.zip` |

## Audit des exigences SOC

| Exigence cahier des charges | Statut dossier | Preuve / action |
|---|---|---|
| SOC externalise centralisant les evenements | Pret | Rapport groupe + doc SIEM |
| Environnement de demonstration operationnel | Base presente | Script `setup-siem-lab.ps1`, a relancer avant demo |
| Solution industrialisable | Pret | Architecture cible et trajectoire dans rapport groupe |
| Collecte multi-source | Documentee et concretisee | Doc SIEM Youssef ; pack pfSense/syslog/logs demo ; captures a ajouter dans `Annexes_Captures/` |
| SIEM open-source centralise | Pret | Wazuh documente |
| Regles de detection personnalisables | Pret | Regles `5712`, `100110`, `100120`, `100130`, `100140`, `110010`, `110020` |
| Dashboards lisibles et segmentes | Documente | Doc SIEM + dossier de captures |
| Playbooks de reponse semi-automatises | Pret | `03_PLAYBOOKS_PROCEDURES_REX.md` |
| Reporting simple et exportable | Pret | Rapport PDF + dashboards executifs |
| Interface web accessible | Documentee | Wazuh Dashboard, capture CAP-01 a produire |
| Acces par roles supervision / analyste / admin | Documente | RBAC doc SIEM, capture CAP-09 a produire |
| Simulation sites clients / VMs / conteneurs | Pret | `serveur-01`, Wazuh Docker, guide de deploiement |
| Generation logs attaque/safe | Pret | `tools/generate_demo_logs.py`, logs Daylight, pfSense, AD/fichiers, mail, endpoint |
| Templates de deploiement client | Pret pour demo | Guide + script + configs pfSense/Wazuh ; a industrialiser pour production |

## Manques restants avant depot final

Ces points ne bloquent pas la structure du dossier, mais doivent etre faits avant un rendu officiel :

1. Remplacer `M2CS` par le code promo exact si necessaire.
2. Lancer le preflight avec `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\preflight_demo.ps1 -WriteReport`.
3. Lancer le lab Wazuh et capturer les ecrans listes dans `07_DOSSIER_PREUVES_CAPTURES.md`.
4. Ajouter les captures dans `Annexes_Captures/`.
5. Enregistrer la video de 15 a 20 minutes.
6. Coller le lien YouTube non repertorie dans `PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_video-lien.txt`, ou remplacer ce TXT par la video MP4 selon le mode de depot choisi.
7. Regenerer l'archive ZIP apres ajout des captures et du lien ou de la video.

## Decision

Le dossier documentaire est pret pour repetition de soutenance. La validation finale depend des preuves visuelles et de l'enregistrement video, car ces elements necessitent l'environnement Wazuh lance et la participation orale de chaque membre.

