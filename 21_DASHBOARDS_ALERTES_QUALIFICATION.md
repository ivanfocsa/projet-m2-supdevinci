# Dashboards, alertes et qualification SOC - Daylight / Cyber Trust

## Objectif

Ce livrable rend concrete la partie detection, alertes, dashboards et qualification. Il donne des requetes pretes a copier dans Wazuh/OpenSearch Dashboards, des widgets attendus et une matrice de triage SOC utilisable par Kilyan pendant la soutenance.

Fichiers associes :

| Fichier | Usage |
|---|---|
| `config/wazuh/daylight_dashboard_queries.csv` | Requetes concretes pour dashboard technique, executif et firewall. |
| `config/wazuh/daylight_alert_qualification_matrix.csv` | Matrice de qualification : severite, SLA, action et escalade. |
| `config/wazuh/local_rules_daylight_pfsense.xml` | Regles Wazuh custom reliees aux IDs d'alertes. |

## 1. Index et champ temps

Dans Wazuh Dashboard, utiliser l'index pattern :

```text
wazuh-alerts-*
```

Champ temps :

```text
@timestamp
```

Periode recommandee pour la demo :

```text
Last 24 hours
```

Si les logs de demonstration sont rejoues pendant la soutenance, reduire a :

```text
Last 15 minutes
```

## 2. Dashboard technique SOC

Ce dashboard est destine aux analystes Cyber Trust. Il sert a qualifier les alertes et a comprendre les sources.

| Widget | Type | Requete | Champ principal |
|---|---|---|---|
| Alertes par severite | Bar chart | `rule.level >= 7` | `rule.level` |
| Top regles declenchees | Data table | `rule.id:*` | `rule.id`, `rule.description` |
| Alertes par source | Pie chart | `agent.name:* OR data.srcip:*` | `agent.name` ou `data.srcip` |
| Timeline alertes critiques | Line chart | `rule.level >= 12` | `@timestamp` |
| Evenements Daylight metier | Data table | `rule.id:(100110 OR 100120 OR 100130 OR 100140 OR 100150)` | `rule.id` |
| Evenements pfSense | Data table | `rule.id:(110010 OR 110020 OR 110030 OR 110040 OR 110050)` | `rule.id` |

## 3. Dashboard executif Daylight

Ce dashboard est destine au client Daylight. Il doit etre lisible sans expertise SIEM.

| Widget | Type | Requete | Message client |
|---|---|---|---|
| Nombre total d'alertes | Metric | `rule.level >= 3` | Volume surveille par le SOC. |
| Alertes critiques | Metric | `rule.level >= 12` | Points qui demandent une action rapide. |
| Alertes par categorie | Donut | `rule.groups:*` | Nature des risques observes. |
| Alertes donnees patients | Metric | `rule.id:100120` | Protection RGPD / donnees sensibles. |
| Tentatives reseau bloquees | Metric | `rule.id:(110010 OR 110020)` | Valeur du firewall et de la segmentation. |
| Tendance 24h | Line chart | `rule.level >= 7` | Evolution de la menace. |

## 4. Requetes pretes a copier

### Brute force SSH

```text
rule.id:5712 OR rule.description:*SSH* OR rule.groups:authentication_failed
```

### Brute force applicatif Daylight

```text
rule.id:100110 OR full_log:*event=auth_failure*
```

### Acces anormal dossier patient

```text
rule.id:100120 OR full_log:*patient_record_access*
```

### Modification groupe privilegie

```text
rule.id:100130 OR full_log:*privileged_group_change*
```

### USB non autorise

```text
rule.id:100140 OR full_log:*usb_insert*
```

### Phishing signale

```text
rule.id:100150 OR full_log:*phishing_reported*
```

### Scan WAN bloque par pfSense

```text
rule.id:110010 OR full_log:*filterlog* AND full_log:*interface=WAN*
```

### Mouvement lateral inter-VLAN

```text
rule.id:110020 OR full_log:*dst_zone=MGMT* OR full_log:*dst_zone=SERVERS*
```

## 5. Matrice de qualification SOC

La matrice complete est dans `config/wazuh/daylight_alert_qualification_matrix.csv`.

| ID | Scenario | Severite SOC | SLA triage | Escalade |
|---:|---|---|---|---|
| `5712` | Brute force SSH | Haute | 30 min | Analyste SOC puis exploitation. |
| `100110` | Brute force applicatif | Haute | 30 min | SOC + referent applicatif Daylight. |
| `100120` | Acces dossier patient | Critique | 15 min | SOC + DPO/referent Daylight. |
| `100130` | Groupe privilegie modifie | Critique | 15 min | SOC + admin SI + direction IT. |
| `100140` | USB non autorise | Moyenne/Haute | 4 h | Support poste + manager local. |
| `100150` | Phishing signale | Haute | 30 min | SOC + support messagerie. |
| `110010` | Scan WAN bloque | Moyenne | 4 h | Surveillance SOC. |
| `110020` | Inter-VLAN vers MGMT/SERVERS | Critique | 15 min | SOC + exploitation reseau. |
| `110050` | Flux sortant volumineux | Critique | 15 min | SOC + reseau + referent Daylight. |

## 6. Workflow de qualification

1. Identifier la regle : `rule.id`, `rule.description`, `rule.level`.
2. Identifier la source : agent, IP, utilisateur, zone reseau.
3. Verifier le contexte : horaire, poste, role metier, site Daylight.
4. Determiner la criticite : donnees patients, privileges, mouvement lateral, exposition externe.
5. Appliquer le SLA de triage.
6. Escalader si necessaire.
7. Documenter la decision dans le REX ou la fiche incident.

## 7. Exemple de qualification complete

### Alerte `100120` - Acces anormal dossier patient

| Champ | Valeur attendue |
|---|---|
| Severite | Critique |
| Pourquoi | Donnees patients et risque RGPD. |
| Verification | Utilisateur, role, centre, patient_id, heure, volume d'acces. |
| Action immediate | Confirmer si acces legitime ; si non, suspendre le compte ou isoler la session. |
| Escalade | Referent Daylight + DPO si suspicion confirmee. |
| Preuve | Capture detail alerte + extrait `Demo_Logs/daylight_app.log`. |
| REX | Ajouter cause racine, mesure corrective et prevention. |

### Alerte `110020` - Tentative inter-VLAN vers MGMT

| Champ | Valeur attendue |
|---|---|
| Severite | Critique |
| Pourquoi | Mouvement lateral vers zone d'administration. |
| Verification | Source USERS, destination MGMT/SERVERS, port vise, repetitions. |
| Action immediate | Confirmer le blocage pfSense, identifier le poste source. |
| Escalade | Exploitation reseau + support poste. |
| Preuve | Capture regle pfSense + alerte Wazuh `110020`. |
| REX | Durcissement poste, verification malware, sensibilisation utilisateur. |

## 8. Ce que Kilyan peut dire a l'oral

> Mon role est de transformer les evenements techniques en decisions SOC. Pour cela, nous avons defini des dashboards par public, des requetes de recherche, une matrice de criticite et des SLA de triage. Une alerte critique comme `100120` ou `110020` n'est pas seulement affichee : elle declenche une qualification, une escalade et un REX.

## 9. Captures a produire

| Capture | Ecran |
|---|---|
| `CAP-21_dashboard-technique-requetes.png` | Dashboard technique avec top regles et severites. |
| `CAP-22_dashboard-executif-daylight.png` | Vue executive client avec alertes critiques et tendances. |
| `CAP-23_qualification-alerte-100120.png` | Detail et qualification acces dossier patient. |
| `CAP-24_qualification-alerte-110020.png` | Detail et qualification mouvement inter-VLAN. |

## 10. Plan B sans Wazuh ouvert

Si Wazuh n'est pas accessible, montrer :

1. `config/wazuh/daylight_dashboard_queries.csv`.
2. `config/wazuh/daylight_alert_qualification_matrix.csv`.
3. `Demo_Logs/daylight_app.log` et `Demo_Logs/pfsense.log`.
4. Le mode `--dry-run` du script de rejeu syslog.

Phrase propre :

> Les dashboards reels dependent du lab Wazuh lance. En revanche, les requetes, widgets, regles et criteres de qualification sont fournis et reproductibles dans l'environnement.
