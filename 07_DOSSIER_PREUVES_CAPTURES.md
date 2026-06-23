# Dossier de preuves et captures - Daylight / Cyber Trust

## Objectif

Ce document liste les captures a produire pour prouver les exigences du cahier des charges. Il evite d'oublier une preuve pendant la video ou avant l'export final du rapport.

Les captures peuvent etre deposees dans le dossier `Annexes_Captures/` en respectant les noms proposes.

## Nomenclature conseillee

```text
CAP-XX_description-courte.png
```

Exemple :

```text
CAP-03_alerte-5712-brute-force-ssh.png
```

## Captures obligatoires

| ID | Fichier attendu | Exigence prouvee | Ecran a capturer | Responsable |
|---|---|---|---|---|
| CAP-01 | `CAP-01_wazuh-dashboard-login.png` | Interface web accessible | Page Wazuh Dashboard connectee | Youssef |
| CAP-02 | `CAP-02_agents-poste01-serveur01.png` | Collecte multi-source | Liste des agents actifs | Youssef |
| CAP-03 | `CAP-03_alerte-5712-brute-force-ssh.png` | Detection serveur | Detail alerte Wazuh `5712` | Youssef |
| CAP-04 | `CAP-04_source-endpoint-poste01-sca.png` | Monitoring poste | Evenements ou SCA CIS Windows 11 | Youssef |
| CAP-05 | `CAP-05_daylight-alertes-metier.png` | Logs applicatifs Daylight | Regles `100110`, `100120`, `100130`, `100140` | Youssef |
| CAP-06 | `CAP-06_alerte-100120-acces-patient.png` | Protection donnees patients | Detail alerte acces dossier patient | Kilyan |
| CAP-07 | `CAP-07_dashboard-technique.png` | Dashboard technique | Severite, sources, top regles | Kilyan |
| CAP-08 | `CAP-08_dashboard-executif.png` | Dashboard executif | Total alertes, critiques, repartition site | Kilyan |
| CAP-09 | `CAP-09_rbac-analyste-lecture-seule.png` | Segmentation par roles | Compte analyste bloque sur admin | Youssef |
| CAP-10 | `CAP-10_playbook-brute-force.png` | Procedure de reponse | Playbook PB-001 ouvert ou explique | Mahamadou |
| CAP-11 | `CAP-11_rex-incident-acces-patient.png` | REX incident | Fiche REX ou section du document | Mahamadou |
| CAP-12 | `CAP-12_architecture-solution.png` | Architecture technique | Schema architecture demo/cible | Yvan |
| CAP-13 | `CAP-13_pfsense-regles-firewall.png` | Firewall/routeur concret | Matrice de regles pfSense ou interface pfSense | Yvan |
| CAP-14 | `CAP-14_pfsense-syslog-wazuh.png` | Collecte reseau/syslog | Procedure ou configuration remote logging vers Wazuh | Yvan / Youssef |

## Captures optionnelles utiles

| ID | Fichier attendu | Pourquoi utile |
|---|---|---|
| CAP-15 | `CAP-15_script-setup-siem-lab.png` | Prouve l'automatisation du lab. |
| CAP-16 | `CAP-16_auth-log-serveur01.png` | Montre les echecs SSH sources de l'alerte. |
| CAP-17 | `CAP-17_compte-supervision-dashboard.png` | Prouve le profil supervision. |
| CAP-18 | `CAP-18_export-dashboard-report.png` | Prouve le reporting exportable si disponible. |

## Checklist de verification des preuves

| Exigence cahier des charges | Preuve minimale |
|---|---|
| Collecte multi-source agents/syslog/API | CAP-02, CAP-03, CAP-05, CAP-14 |
| SIEM open-source centralise | CAP-01, CAP-07 |
| Regles detection et alerting | CAP-03, CAP-05, CAP-06 |
| Dashboards lisibles et segmentes | CAP-07, CAP-08 |
| Playbooks de reponse semi-automatises | CAP-10, document playbooks |
| Reporting simple et exportable | CAP-08, PDF rapport |
| Interface claire web-based | CAP-01 |
| Acces par roles supervision / analyste / admin | CAP-09, CAP-15 |
| Reproductibilite | CAP-13, guide de deploiement |
| REX incidents | CAP-11, document REX |

## Comment integrer dans le rendu final

1. Copier les images dans `Annexes_Captures/`.
2. Ajouter les captures les plus fortes dans le rapport groupe si le temps le permet.
3. Laisser toutes les captures dans l'archive ZIP en annexe.
4. Montrer au moins CAP-02, CAP-03, CAP-06, CAP-07, CAP-08 et CAP-09 dans la video.

## Statut actuel

Les preuves textuelles et le PDF SIEM de Youssef existent deja. Les captures finales doivent etre recuperees depuis l'environnement Wazuh reel au moment ou le lab est lance.
