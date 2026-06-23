# Pack solutions concretes - Daylight / Cyber Trust

## Objectif

Ce document transforme l'architecture du projet en elements demonstrables. Il ne remplace pas les captures reelles Wazuh, mais il donne des configurations, regles et logs exploitables pour montrer au jury comment Cyber Trust securise Daylight de facon concrete.

Les fichiers associes sont :

| Fichier | Usage en soutenance |
|---|---|
| `config/pfsense/pfsense_firewall_rules.csv` | Montrer les regles firewall proposees pour Daylight. |
| `config/pfsense/pfsense_aliases.csv` | Montrer les objets reseau reutilisables dans pfSense. |
| `config/pfsense/pfsense_nat_port_forward.csv` | Montrer l'exposition controlee des services DMZ/VPN. |
| `config/pfsense/pfsense_syslog_wazuh.md` | Montrer le raccordement pfSense vers Wazuh. |
| `config/pfsense/README_IMPORT_PFSENSE_DAYLIGHT.md` | Montrer les clics exacts a faire dans pfSense : interfaces, aliases, NAT, regles, remote logging. |
| `config/pfsense/pfsense_demo_test_plan.csv` | Montrer les tests concrets : commande, resultat attendu, preuve Wazuh et capture conseillee. |
| `Dashboards_Offline/daylight_pfsense_firewall_review.html` | Montrer en navigateur une revue firewall lisible, generee depuis les CSV du projet. |
| `config/wazuh/local_rules_daylight_pfsense.xml` | Montrer les detections Wazuh ajoutees pour firewall, app, AD et mail. |
| `tools/generate_demo_logs.py` | Generer des logs de demonstration lisibles et injectables. |
| `tools/send_demo_logs_to_syslog.py` | Rejouer les logs vers Wazuh/syslog avec un mode dry-run. |
| `Demo_Logs/` | Logs de demo generes : firewall, application, AD/fichiers, mail. |

## 1. Solution reseau concrete : pfSense

Cyber Trust retient pfSense comme firewall/routeur de demonstration et comme cible possible pour les sites Daylight. Le choix est concret car pfSense apporte une interface web, des regles exportables, du NAT, des VLAN, du syslog et des paquets comme Suricata.

### Interfaces et VLAN proposes

| Interface | Nom | Adresse | Role |
|---|---|---|---|
| WAN | Internet | DHCP ou IP FAI | Acces externe, aucun flux entrant par defaut. |
| VLAN10 | USERS | `10.10.10.1/24` | Postes audioprothesistes et accueil. |
| VLAN20 | SERVERS | `10.10.20.1/24` | AD, fichiers, bases internes. |
| VLAN30 | DMZ | `10.10.30.1/24` | Application Daylight exposee en HTTPS. |
| VLAN40 | MGMT | `10.10.40.1/24` | Administration firewall, serveurs, hyperviseur. |
| VLAN50 | SOC | `10.10.50.1/24` | Wazuh Manager, dashboard et collecte logs. |

### Regles firewall a montrer

La matrice complete est dans `config/pfsense/pfsense_firewall_rules.csv`. Les regles les plus importantes sont :

| Zone | Action | Flux | Justification |
|---|---|---|---|
| WAN | Block | Tout entrant non etabli | Principe de refus par defaut. |
| WAN | Pass | VPN SSL/IPsec vers pfSense | Acces admin distant controle. |
| USERS | Pass | DNS vers pfSense | Evite DNS direct non controle. |
| USERS | Pass | HTTPS vers Internet et app Daylight | Usage metier normal. |
| USERS | Block | USERS vers MGMT/SERVERS | Bloque les mouvements lateraux. |
| DMZ | Pass | App Daylight vers base interne seulement | Flux applicatif minimal. |
| MGMT | Pass | Admin vers pfSense/Wazuh/serveurs | Administration reservee. |
| SOC | Pass | Wazuh vers sources et reception logs | Supervision Cyber Trust. |

Chaque regle sensible doit avoir la journalisation active dans pfSense. Les refus inter-VLAN, les refus WAN et les modifications d'administration sont les evenements prioritaires a envoyer au SIEM.

### NAT et exposition controlee

La DMZ expose uniquement le service HTTPS de l'application Daylight. La table NAT proposee dans `config/pfsense/pfsense_nat_port_forward.csv` evite les expositions directes vers le LAN.

| Service | Port externe | Destination | Commentaire |
|---|---:|---|---|
| Portail Daylight | 443 | `10.10.30.20:443` | Exposition demo de l'application en DMZ. |
| VPN admin | 1194/UDP | pfSense | Acces admin distant avec MFA dans la cible. |

## 2. Collecte concrete pfSense vers Wazuh

La procedure `config/pfsense/pfsense_syslog_wazuh.md` permet de configurer pfSense en quelques minutes :

1. Aller dans `Status > System Logs > Settings`.
2. Activer `Remote Logging`.
3. Serveur distant : `10.10.50.10`.
4. Port : `514/UDP`.
5. Categories : firewall, system, DHCP, DNS resolver, VPN.
6. Dans Wazuh, activer l'ecoute syslog UDP 514.
7. Importer `config/wazuh/local_rules_daylight_pfsense.xml`.

Preuve a capturer : une ligne `filterlog` recue dans Wazuh, puis une alerte `110010` ou `110020`.

## 3. Detections Wazuh concretes

Le fichier `config/wazuh/local_rules_daylight_pfsense.xml` contient des regles pretes a montrer :

| ID | Source | Evenement | Niveau |
|---:|---|---|---:|
| `110010` | pfSense | Flux entrant bloque sur WAN | 8 |
| `110020` | pfSense | Tentative inter-VLAN vers SERVERS ou MGMT | 10 |
| `110030` | pfSense | Connexion admin vers pfSense | 6 |
| `110040` | pfSense | Evenement VPN admin | 7 |
| `100110` | Application | Brute force applicatif Daylight | 10 |
| `100120` | Application | Acces anormal a un dossier patient | 12 |
| `100130` | AD/fichiers | Modification groupe privilegie | 12 |
| `100150` | Messagerie | Mail de phishing signale | 9 |

Ces regles permettent de montrer que le SOC ne surveille pas seulement un serveur Linux, mais aussi les briques demandees dans le cahier des charges : firewall/routeur, application, annuaire/fichiers, messagerie et endpoints.

## 4. Logs de demonstration

Le script suivant genere des logs propres et lisibles :

```powershell
python .\tools\generate_demo_logs.py
python .\tools\send_demo_logs_to_syslog.py --dry-run
```

Il produit :

| Fichier | Scenarios inclus |
|---|---|
| `Demo_Logs/pfsense.log` | Scan WAN bloque, tentative inter-VLAN, acces VPN, flux HTTPS autorise. |
| `Demo_Logs/daylight_app.log` | Brute force applicatif, acces dossier patient, erreur metier. |
| `Demo_Logs/ad_files.log` | Modification groupe privilegie, acces partage sensible. |
| `Demo_Logs/mail_phishing.log` | Signalement phishing et piece jointe suspecte. |

Ces logs peuvent etre montres tels quels dans la video, ou injectes dans un lab Wazuh via syslog/filebeat selon le temps disponible. Il faut les presenter comme des logs de demonstration, pas comme des preuves de production.

## 5. Ce que chaque membre peut montrer

| Membre | Demonstration concrete |
|---|---|
| Yvan FOCSA | Ouvrir la matrice VLAN, les regles pfSense, le NAT et expliquer la segmentation. |
| Youssef GUERNIOU | Ouvrir Wazuh, les regles XML, les alertes et le dashboard. |
| Kilyan FELIX | Qualifier les alertes, montrer severite, priorite, SLA et dashboard SOC. |
| Mahamadou DIACOUMBA | Montrer les logs generes, les playbooks, la relance VM/lab et le REX incident. |

## 6. Sequence de demo recommandee

1. Montrer le schema d'architecture cible.
2. Ouvrir `Dashboards_Offline/daylight_pfsense_firewall_review.html` et expliquer la segmentation, les blocks, les pass et les regles journalisees.
3. Ouvrir `config/pfsense/README_IMPORT_PFSENSE_DAYLIGHT.md` pour montrer les chemins exacts dans l'interface pfSense.
4. Ouvrir `config/pfsense/pfsense_demo_test_plan.csv` et choisir un test, par exemple `PF-TEST-02` USERS vers MGMT bloque.
5. Ouvrir `pfsense_syslog_wazuh.md` et montrer comment pfSense envoie les logs a Wazuh.
6. Ouvrir `local_rules_daylight_pfsense.xml` et montrer les IDs d'alertes.
7. Lancer `python .\tools\generate_demo_logs.py`.
8. Ouvrir `Demo_Logs/pfsense.log` puis `Demo_Logs/daylight_app.log`.
9. Si le collecteur syslog est disponible, rejouer les logs avec `tools/send_demo_logs_to_syslog.py`; sinon utiliser `--dry-run` pour montrer le contenu sans envoi reseau.
10. Dans Wazuh, montrer les alertes deja disponibles ou expliquer l'injection si le lab n'est pas demarre.
11. Derouler un playbook : `Acces anormal dossier patient` ou `Tentative inter-VLAN`.

## 7. Phrase simple pour la soutenance

> Nous n'avons pas seulement choisi Wazuh : nous avons defini comment les sources Daylight sont connectees. Cote reseau, pfSense segmente les flux par VLAN, journalise les refus et envoie ses logs au SOC Cyber Trust. Cote SIEM, les regles Wazuh transforment ces logs en alertes qualifiables par les analystes.
