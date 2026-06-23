# Backlog et planning - Daylight / Cyber Trust

## Objectif

Ce document complete le rapport technique avec une vision projet : taches, responsables, priorites, statut et preuves attendues.

## Backlog

| ID | Tache | Responsable | Priorite | Statut | Preuve attendue |
|---|---|---|---|---|---|
| B-001 | Lire cahier des charges et cadre pedagogique | Tous | Haute | Fait | Registre exigences |
| B-002 | Definir roles equipe | Kilyan + Yvan | Haute | Fait | Rapport groupe |
| B-003 | Concevoir architecture demo | Yvan | Haute | Fait | Rapport groupe + rendu Yvan |
| B-004 | Deployer Wazuh single-node | Youssef | Haute | Fait | Documentation SIEM |
| B-005 | Connecter endpoint `poste-01` | Youssef | Haute | Fait selon doc SIEM | Capture agent |
| B-006 | Connecter serveur `serveur-01` | Youssef | Haute | Fait selon doc SIEM | Capture agent + alerte SSH |
| B-007 | Integrer logs applicatifs Daylight | Youssef | Haute | Fait selon doc SIEM | Alertes `100110` a `100140` |
| B-008 | Creer dashboards technique et executif | Youssef + Kilyan | Haute | Fait selon doc SIEM | Captures dashboards |
| B-009 | Definir matrice de qualification | Kilyan | Haute | Fait | Playbooks + rendu Kilyan |
| B-010 | Configurer RBAC | Youssef | Moyenne | Fait selon doc SIEM | Capture acces analyste |
| B-011 | Rediger playbooks | Mahamadou | Haute | Fait | `03_PLAYBOOKS_PROCEDURES_REX.md` |
| B-012 | Rediger REX incidents simules | Mahamadou | Haute | Fait | `03_PLAYBOOKS_PROCEDURES_REX.md` |
| B-013 | Rediger guide de deploiement | Mahamadou + Youssef | Haute | Fait | `02_GUIDE_DEPLOIEMENT_UTILISATION.md` |
| B-014 | Rediger rapport groupe | Yvan + tous | Haute | Fait | PDF groupe |
| B-015 | Rediger rendus individuels | Chaque membre | Haute | Fait | PDFs individuels |
| B-016 | Preparer script video | Kilyan + tous | Haute | Fait | `04_SCRIPT_VIDEO_DEMO.md` |
| B-017 | Enregistrer video | Tous | Haute | A faire | MP4 ou lien YouTube non repertorie |
| B-018 | Inserer captures finales | Tous | Haute | A faire | Annexes ou PDF final enrichi |
| B-019 | Creer ZIP final | Kilyan | Haute | A faire | Archive nommee selon consigne |

## Planning propose

| Sequence | Duree | Travaux |
|---|---:|---|
| S1 - Cadrage | 1 jour | Lecture consignes, roles, backlog, architecture cible. |
| S2 - Construction SIEM | 2 a 3 jours | Wazuh, agents, serveur simule, logs Daylight, RBAC. |
| S3 - Detection et dashboards | 1 a 2 jours | Regles, alertes, dashboards technique et executif. |
| S4 - Procedures | 1 jour | Playbooks, redemarrage, REX, guide utilisateur. |
| S5 - Consolidation | 1 jour | Rapport groupe, rendus individuels, exports PDF. |
| S6 - Video | 0,5 a 1 jour | Repetition, enregistrement, verification sonore et visuelle. |

## RACI simplifie

| Activite | Yvan | Youssef | Kilyan | Mahamadou |
|---|---|---|---|---|
| Architecture | R/A | C | C | C |
| SIEM Wazuh | C | R/A | C | C |
| Detection et qualification | C | C | R/A | C |
| Dashboards | C | R | A | C |
| Playbooks | C | C | C | R/A |
| VM / conteneurs / redemarrage | C | R | C | A |
| Rapport groupe | R/A | C | C | C |
| Video | C | C | R/A | C |

R = responsable, A = accountable, C = consulte.

## Critere de pret pour la soutenance

Le projet est pret pour l'enregistrement video quand :

1. Wazuh Dashboard se lance en moins de deux minutes.
2. Les agents `poste-01` et `serveur-01` sont visibles.
3. Les alertes `5712`, `100110`, `100120`, `100130`, `100140` sont montrables.
4. Les dashboards technique et executif sont accessibles.
5. Le compte analyste est limite en lecture.
6. Chaque membre sait exactement quoi dire pendant sa sequence.
7. Les PDF groupe et individuels sont generes.
