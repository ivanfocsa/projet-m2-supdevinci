# Storyboard video 15-20 minutes - Projet Daylight / Cyber Trust

## Contraintes a respecter

- Duree cible : 15 a 20 minutes.
- Tous les membres parlent.
- Le nom de la personne qui parle doit etre affiche a l'ecran.
- Structure conseillee : besoin client, solution, organisation, demonstration, conclusion.
- Montrer des preuves : logs, alertes, dashboards, RBAC, playbooks.
- Video a rendre en MP4 dans un ZIP ou via lien YouTube non repertorie selon la consigne finale de l'ecole.

## Repartition proposee

| Temps | Intervenant | Contenu |
|---:|---|---|
| 00:00 - 01:30 | Kilyan FELIX | Introduction, presentation Daylight et Cyber Trust, objectif du SOC externalise. |
| 01:30 - 04:00 | Yvan FOCSA | Architecture de la solution, segmentation pfSense, choix Wazuh, sources de logs, architecture demo et cible. |
| 04:00 - 08:30 | Youssef GUERNIOU | Demonstration Wazuh : agents, collecte `poste-01`, `serveur-01`, Daylight, alertes. |
| 08:30 - 11:30 | Kilyan FELIX | Detection, qualification, dashboards technique et executif, priorisation des alertes. |
| 11:30 - 14:30 | Mahamadou DIACOUMBA | Playbooks, procedure de redemarrage, REX incident brute force ou acces patient. |
| 14:30 - 17:00 | Yvan + equipe | Industrialisation, couts, limites, ameliorations, conclusion client. |

## Texte conducteur

### 1. Introduction - Kilyan

Bonjour, nous sommes Cyber Trust. Dans cette demonstration, nous presentons le projet 4 : la mise en place d'un SOC externalise pour Daylight, un reseau de centres d'audioprothesistes. Le besoin de Daylight est de centraliser ses evenements de securite, detecter les comportements suspects, fournir des dashboards lisibles et disposer de procedures de reponse exploitables par un SOC.

Notre objectif est de montrer un demonstrateur operationnel, mais aussi une solution industrialisable pour un modele d'infogerance.

### 2. Architecture - Yvan

La solution repose sur Wazuh, un SIEM open-source adapte a une demonstration reproductible. Nous avons retenu trois sources principales : un poste endpoint `poste-01`, un serveur Linux simule `serveur-01`, et des logs applicatifs Daylight representant le CRM, les rendez-vous et les dossiers patients.

Le flux est simple : les sources envoient les evenements au Wazuh Manager, les donnees sont indexees, puis restituees dans le dashboard web. Pour la cible industrielle, Cyber Trust prevoit une separation manager, indexer et dashboard, avec collecte multi-site et procedures SOC.

### 3. Demonstration SIEM - Youssef

Je presente maintenant la partie SIEM. Wazuh est deployee en mode Docker single-node pour garantir une installation rapide. Le script `setup-siem-lab.ps1` cree ou relance `serveur-01`, installe l'agent Wazuh, active SSH et rsyslog, puis genere une simulation de brute force SSH.

A l'ecran, nous voyons les agents et les sources de logs. Nous avons `poste-01` pour les evenements endpoint, `serveur-01` pour les evenements systeme et SSH, et les logs applicatifs Daylight. La detection `5712` montre la brute force SSH. Les regles Daylight montrent notamment l'acces anormal a un dossier patient avec la regle `100120`.

### 4. Detection et dashboards - Kilyan

La qualification SOC repose sur une matrice de severite. Les alertes liees aux donnees patients et aux privileges sont critiques, les attaques de brute force sont hautes, et les evenements comme l'usage USB peuvent etre moyens ou hauts selon le contexte.

Nous avons deux vues : un dashboard technique pour les analystes, avec les alertes par severite, source et regle ; et un dashboard executif pour la supervision, avec les volumes globaux, les alertes critiques et la repartition par site.

### 5. Playbooks et REX - Mahamadou

Une detection seule ne suffit pas. Pour rendre le SOC exploitable, nous avons formalise des playbooks. Par exemple, pour une brute force SSH, l'analyste verifie l'adresse source, les comptes vises, la presence eventuelle d'une connexion reussie, puis propose un blocage et documente les preuves.

Pour un acces anormal a un dossier patient, la severite est critique. Il faut verifier le profil de l'utilisateur, le site, les dossiers touches, puis escalader au referent Daylight et conserver une trace pour le REX.

Je montre egalement la procedure de redemarrage du lab apres extinction : relancer Wazuh, demarrer `serveur-01`, relancer `rsyslogd`, SSH et l'agent Wazuh.

### 6. Conclusion - Yvan puis equipe

Le demonstrateur repond aux attentes du cahier des charges : collecte multi-source, SIEM centralise, alertes personnalisees, dashboards, RBAC et playbooks. La limite principale est que la version actuelle est un lab single-node. En production, nous recommandons une architecture separee, un pilote sur quelques centres, puis une generalisation progressive.

Cyber Trust peut ainsi fournir a Daylight une supervision externalisee, documentee et evolutive.

## Checklist capture video

| Preuve | Responsable | Capture / sequence |
|---|---|---|
| Page Wazuh accessible | Youssef | Connexion dashboard. |
| Agents visibles | Youssef | `poste-01`, `serveur-01`. |
| Alerte brute force SSH `5712` | Youssef | Detail alerte. |
| Alerte Daylight `100120` | Youssef / Kilyan | Detail acces patient. |
| Dashboard technique | Kilyan | Severite, source, top regles. |
| Requetes Wazuh et matrice qualification | Kilyan | `21_DASHBOARDS_ALERTES_QUALIFICATION.md` + CSV Wazuh. |
| Dashboard executif | Kilyan | Total alertes, critiques, repartition site. |
| RBAC analyste lecture seule | Youssef | Page admin bloquee. |
| Playbook incident | Mahamadou | Deroulement PB-001 ou PB-002. |
| Runbook VM et REX | Mahamadou | `22_EXPLOITATION_VM_RUNBOOK_REX.md` + CSV lab. |
| Architecture | Yvan | Schema dans rapport ou slide. |
| Matrice pfSense | Yvan | VLAN, regles firewall, syslog Wazuh. |

## Conseils de montage

1. Afficher le nom de l'intervenant en bas de l'ecran pendant chaque prise de parole.
2. Garder les captures Wazuh lisibles : zoom navigateur a 110 ou 125 pour les details.
3. Eviter les longues attentes de chargement : preparer les onglets avant l'enregistrement.
4. Enregistrer une courte introduction face camera ou slide, puis enchainer sur le screencast.
5. Terminer avec une slide de synthese : exigences couvertes, limites, prochaines etapes.
