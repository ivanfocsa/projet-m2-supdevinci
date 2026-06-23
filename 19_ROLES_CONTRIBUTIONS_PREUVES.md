# Roles, contributions et preuves - Daylight / Cyber Trust

## Objectif

Cette fiche sert a rendre la soutenance plus concrete : chaque membre sait quoi montrer, quel livrable prouve son travail et quelle phrase utiliser devant le jury. Elle complete le rapport groupe et evite que les roles se chevauchent de facon floue.

## Repartition finale conseillee

| Membre | Role public | Responsabilites | Preuves a montrer |
|---|---|---|---|
| Yvan FOCSA | Architecte solution | Architecture cible, segmentation, choix pfSense/Wazuh, coherence cahier des charges. | `01_RAPPORT_TECHNIQUE_GROUPE.md`, `18_SOLUTIONS_CONCRETES_DEMO.md`, `config/pfsense/`. |
| Youssef GUERNIOU | Ingenieur SIEM / Wazuh | Deploiement SIEM, agents, regles, RBAC, dashboards et lab. | `Youssef GUERNIOU/setup-siem-lab.ps1`, documentation SIEM, Wazuh Dashboard. |
| Kilyan FELIX | Chef de projet SOC / lead detection | Planning, qualification, severite, alertes, dashboards, priorisation client. | `05_BACKLOG_PLANNING.md`, `13_PLAN_RECETTE_ACCEPTATION.md`, dashboards, matrice d'alertes. |
| Mahamadou DIACOUMBA | Exploitation, VM, playbooks, REX | VM/lab, procedures de redemarrage, playbooks, REX incidents. | `03_PLAYBOOKS_PROCEDURES_REX.md`, `10_MODE_OPERATOIRE_DEMO_JOUR_J.md`, logs demo. |

## Ce que chacun montre a l'ecran

| Temps | Membre | Ecran concret | Message simple |
|---:|---|---|---|
| 01:30 | Yvan | Schema rapport + `pfsense_firewall_rules.csv` | Daylight est segmente par VLAN et les flux sont controles par pfSense. |
| 03:30 | Yvan | `pfsense_syslog_wazuh.md` | Les logs firewall partent vers Wazuh en syslog pour alimenter le SOC. |
| 04:30 | Youssef | Wazuh Dashboard | Le SIEM centralise les agents, logs systeme et logs metier. |
| 06:30 | Youssef | Detail alerte Wazuh | Les regles natives et custom transforment les logs en alertes. |
| 08:30 | Kilyan | Dashboard technique/executif | La detection est qualifiee par severite et restituee lisiblement au client. |
| 11:30 | Mahamadou | Playbook PB-001 ou PB-002 | Une alerte declenche une procedure de triage, confinement et REX. |
| 13:30 | Mahamadou | `Demo_Logs/` + dry-run syslog | Les scenarios peuvent etre rejoues en lab sans inventer de preuves. |
| 15:00 | Equipe | Checklist depot | Il reste les captures et la video officielle a produire en conditions reelles. |

## Commandes utiles pendant la repetition

Generer les logs :

```powershell
python .\tools\generate_demo_logs.py
```

Voir les logs sans rien envoyer :

```powershell
python .\tools\send_demo_logs_to_syslog.py --dry-run
```

Rejouer seulement les logs pfSense vers Wazuh local en UDP 514 :

```powershell
python .\tools\send_demo_logs_to_syslog.py --host 127.0.0.1 --port 514 --protocol udp --file pfsense.log
```

Rejouer tous les logs vers un Wazuh Manager de lab :

```powershell
python .\tools\send_demo_logs_to_syslog.py --host 10.10.50.10 --port 514 --protocol udp
```

## Phrases pretes pour la soutenance

| Membre | Phrase courte |
|---|---|
| Yvan | "Mon role a ete de transformer le besoin Daylight en architecture exploitable : zones reseau, flux autorises, firewall pfSense, collecte syslog et integration SIEM." |
| Youssef | "J'ai porte la partie SIEM : Wazuh, agents, collecte, regles, RBAC et preuves techniques du lab." |
| Kilyan | "J'ai structure la qualification SOC : criticite, priorisation, dashboards, criteres de recette et pilotage de la demonstration." |
| Mahamadou | "J'ai formalise l'exploitation : procedures, redemarrage du lab, playbooks et retour d'experience apres incident." |

## Points a ne pas promettre

| Sujet | Formulation propre |
|---|---|
| Captures manquantes | "Les captures finales doivent etre prises sur le lab lance ; le dossier liste les captures attendues sans les inventer." |
| pfSense non installe localement | "pfSense est fourni comme configuration concrete et trajectoire demonstrable ; si le lab pfSense n'est pas lance, on montre la matrice de regles et le raccordement syslog." |
| Logs de demo | "Ce sont des logs de demonstration pour tester les regles et la collecte, pas des preuves de production." |
| Production reelle | "La production necessite un pilote, du dimensionnement et une validation Daylight." |

## Mini-RACI

| Activite | Yvan | Youssef | Kilyan | Mahamadou |
|---|---|---|---|---|
| Architecture cible | R | C | C | C |
| Wazuh et agents | C | R | C | C |
| Regles et detections | C | R | R | C |
| Dashboards | C | R | R | C |
| pfSense / segmentation | R | C | C | C |
| Playbooks | C | C | C | R |
| REX incidents | C | C | C | R |
| Planning / depot | C | C | R | C |
| Video finale | R | R | R | R |

R = responsable principal, C = contributeur.

## Livrables recents a citer pendant la correction

| Membre | Livrables recents | Pourquoi c'est concret |
|---|---|---|
| Yvan FOCSA | `Config_PfSense/`, `CAP-12`, `CAP-13`, `MANIFEST_DEPOT.md` | Architecture, firewall, flux, integrite depot. |
| Youssef GUERNIOU | `extract_youssef_wazuh_proofs.py`, `CAP-01`, `CAP-02`, `CAP-03`, `local_rules_daylight_pfsense.xml` | Preuves Wazuh, agents, alertes, regles custom. |
| Kilyan FELIX | `daylight_video_teleprompter.html`, `Video_Overlays/`, `CAP-06`, `CAP-07`, `CAP-08`, `CAP-23` | Soutenance, noms visibles, dashboards, qualification. |
| Mahamadou DIACOUMBA | `repair_lab_and_capture_cap25.ps1`, `lab-cap25-recovery-report.txt`, `CAP-10`, `CAP-11`, `CAP-20`, `CAP-27` | Exploitation lab, playbooks, REX, CAP-25 non fabrique. |

Phrase commune a garder : "Les preuves finales manquantes ne sont pas inventees ; le dossier fournit les procedures et controles pour les produire en conditions reelles."
