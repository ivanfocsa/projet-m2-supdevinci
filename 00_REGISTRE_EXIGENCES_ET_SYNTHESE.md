# Projet 4 - Daylight / Cyber Trust

## But du document

Ce registre sert de garde-fou pour ne rien oublier par rapport aux deux documents sources :

- `Cadre Pedagogique - Projet Etude - CS - 2025[26].pdf`
- `Cahier des charges - Projet Etude - M2 - CS - 2025[41].pdf`

Il decrit aussi l'etat reel du dossier au moment de la reprise : seuls le script SIEM et la documentation SIEM de Youssef sont deja presents. Les autres dossiers etaient vides et sont donc alimentes par les livrables ci-dessous.

## Contexte retenu

Daylight est le client fictif : un reseau d'environ trente centres d'audioprothesistes en France. L'entreprise manipule des donnees sensibles liees aux rendez-vous, aux dossiers patients, au CRM, aux postes de travail, aux serveurs internes, a la messagerie et aux equipements reseau.

Cyber Trust est le prestataire retenu pour concevoir un SOC externalise, demonstrable, documente, securise et industrialisable.

## Roles projet

| Membre | Role principal | Contribution attendue |
|---|---|---|
| Yvan FOCSA | Architecte de la solution | Architecture SOC, segmentation, choix techniques, dossier d'architecture, industrialisation, couts et trajectoire cible. |
| Youssef GUERNIOU | Ingenieur SIEM / Wazuh | Deploiement Wazuh, collecte multi-source, integration agents et logs, RBAC, dashboards, script d'automatisation. |
| Kilyan FELIX | Chef de projet SOC et lead detection | Planning, backlog, coordination demo, qualification des alertes, matrice de severite, specifications dashboards et reporting. |
| Mahamadou DIACOUMBA | Responsable exploitation, VM, playbooks et REX | Environnement VM/conteneurs, procedures d'exploitation, playbooks de reponse, REX incidents et maintien en conditions operationnelles. |

## Etat du dossier

| Zone | Etat observe | Decision |
|---|---:|---|
| Dossier racine | 2 PDF de consignes | Utilises comme reference de cadrage. |
| `Youssef GUERNIOU/` | 1 PDF technique SIEM + 1 script PowerShell | Conserve comme preuve technique existante. |
| `Yvan FOCSA/` | Vide | Creation d'un rendu individuel architecture. |
| `Kilyan FELIX/` | Vide | Creation d'un rendu individuel pilotage/detection. |
| `Mahamadou DIACOUMBA/` | Vide | Creation d'un rendu individuel exploitation/playbooks/REX. |

## Correspondance exigences / preuves

| Exigence | Source | Fichier du dossier qui y repond | Statut |
|---|---|---|---|
| Analyse initiale du besoin client | Cahier des charges | `01_RAPPORT_TECHNIQUE_GROUPE.md` | Redige |
| Document d'architecture technique | Cahier des charges + cadre pedagogique | `01_RAPPORT_TECHNIQUE_GROUPE.md`, `Yvan FOCSA/PE-2526_M2CS_YvanFOCSA.md` | Redige |
| Demonstrateur SOC operationnel | Cahier des charges | `Youssef GUERNIOU/setup-siem-lab.ps1`, `Youssef GUERNIOU/Documentation_SIEM_Youssef_GUERNIOU.pdf` | Base deja presente |
| Collecte multi-source | Cahier des charges | Documentation SIEM Youssef, rapport groupe | Preuve annoncee dans le PDF SIEM |
| SIEM open-source centralise | Cahier des charges | Wazuh single-node Docker decrit dans la doc SIEM | Preuve annoncee dans le PDF SIEM |
| Regles de detection et alerting | Cahier des charges | `03_PLAYBOOKS_PROCEDURES_REX.md`, doc SIEM | Redige + preuve SIEM |
| Dashboards lisibles et segmentes | Cahier des charges | doc SIEM + rendu Kilyan | Preuve annoncee dans le PDF SIEM |
| Playbooks de reponse | Cahier des charges | `03_PLAYBOOKS_PROCEDURES_REX.md`, rendu Mahamadou | Redige |
| Reporting exportable | Cahier des charges | Rapport groupe, script video, dashboards SIEM | Redige |
| Interface web segmentee par roles | Cahier des charges | RBAC decrit dans la doc SIEM | Preuve annoncee dans le PDF SIEM |
| Guide de deploiement et d'utilisation | Cahier des charges | `02_GUIDE_DEPLOIEMENT_UTILISATION.md` | Redige |
| Rapport technique complet | Cadre pedagogique | `01_RAPPORT_TECHNIQUE_GROUPE.md` | Redige |
| Gestion des couts M2 | Cadre pedagogique | `01_RAPPORT_TECHNIQUE_GROUPE.md` | Redige |
| Planning, roles, methodologie | Cadre pedagogique | `01_RAPPORT_TECHNIQUE_GROUPE.md`, `04_SCRIPT_VIDEO_DEMO.md` | Redige |
| REX incidents | Cadre pedagogique | `03_PLAYBOOKS_PROCEDURES_REX.md` | Redige |
| Rendu individuel par membre | Cadre pedagogique | Dossiers de Yvan, Youssef, Kilyan, Mahamadou | Redige en Markdown, a exporter en PDF |
| Video 15-20 min avec parole de tous | Cadre pedagogique | `04_SCRIPT_VIDEO_DEMO.md` | Storyboard redige, video a enregistrer |

## Points a prouver pendant la demo

1. L'interface Wazuh est accessible via navigateur.
2. Les sources de logs visibles sont au minimum : endpoint Windows `poste-01`, serveur Linux `serveur-01`, application metier Daylight.
3. Les alertes importantes sont visibles : brute force SSH `5712`, acces anormal dossier patient `100120`, brute force applicatif `100110`, modification de groupe privilegie `100130`, usage USB `100140`.
4. Les dashboards technique et executif existent et sont exploitables.
5. Les profils RBAC supervision / analyste / admin sont differencies.
6. Au moins un playbook est deroule en direct ou explique avec un incident simule.

## Priorites immediates avant rendu

1. Relire les Markdown, corriger les noms/prenoms si l'ecole impose une graphie exacte.
2. Inserer les captures d'ecran manquantes dans le rapport groupe et les rendus individuels.
3. Exporter le rapport groupe et chaque rendu individuel en PDF.
4. Enregistrer la video selon le storyboard, avec nom de chaque personne affiche pendant sa prise de parole.
5. Creer le ZIP final avec la nomenclature de la promo.
