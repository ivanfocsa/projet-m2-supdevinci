# Mode operatoire pfSense + Wazuh lab - Daylight / Cyber Trust

## Objectif

Ce document donne une procedure concrete pour monter une demonstration firewall/routeur autour de pfSense et raccorder les evenements a Wazuh. Il sert a completer la partie architecture avec quelque chose de testable devant le jury.

Le principe retenu pour la demo est simple : une VM pfSense avec plusieurs cartes reseau virtuelles, une zone SOC contenant Wazuh, et des machines de test simulant USERS, SERVERS, DMZ et MGMT.

## 1. Topologie lab recommandee

| VM / machine | Interface | Reseau virtuel | IP | Role |
|---|---|---|---|---|
| `pfsense-fw-01` | WAN | NAT hyperviseur | DHCP | Acces Internet de demo. |
| `pfsense-fw-01` | USERS | `DAYLIGHT_USERS` | `10.10.10.1/24` | Passerelle utilisateurs. |
| `pfsense-fw-01` | SERVERS | `DAYLIGHT_SERVERS` | `10.10.20.1/24` | Passerelle serveurs. |
| `pfsense-fw-01` | DMZ | `DAYLIGHT_DMZ` | `10.10.30.1/24` | Passerelle application exposee. |
| `pfsense-fw-01` | MGMT | `DAYLIGHT_MGMT` | `10.10.40.1/24` | Passerelle administration. |
| `pfsense-fw-01` | SOC | `DAYLIGHT_SOC` | `10.10.50.1/24` | Passerelle supervision. |
| `wazuh-manager` | SOC | `DAYLIGHT_SOC` | `10.10.50.10/24` | SIEM Cyber Trust. |
| `poste-01` | USERS | `DAYLIGHT_USERS` | `10.10.10.54/24` | Poste utilisateur. |
| `serveur-01` | SERVERS | `DAYLIGHT_SERVERS` | `10.10.20.20/24` | Serveur interne. |
| `daylight-app-01` | DMZ | `DAYLIGHT_DMZ` | `10.10.30.20/24` | Application metier. |
| `admin-01` | MGMT | `DAYLIGHT_MGMT` | `10.10.40.21/24` | Poste administrateur. |

Cette topologie evite d'avoir besoin d'un switch physique ou d'un trunk VLAN. Chaque zone est un reseau virtuel separe dans VirtualBox, VMware ou Hyper-V.

## 2. Prerequis

| Element | Valeur concrete |
|---|---|
| pfSense | ISO pfSense CE ou image equivalente fournie par l'enseignant. |
| VM pfSense | 2 vCPU, 2 Go RAM, 16 Go disque, 6 cartes reseau. |
| Wazuh | Lab deja prepare par Youssef ou Wazuh Docker single-node. |
| Poste admin | Navigateur web pour acceder a `https://10.10.40.1`. |
| Logs demo | `Demo_Logs/` genere par `tools/generate_demo_logs.py`. |
| Pack demo pfSense | `Dashboards_Offline/daylight_pfsense_firewall_review.html`, `config/pfsense/README_IMPORT_PFSENSE_DAYLIGHT.md`, `config/pfsense/pfsense_demo_test_plan.csv`. |

## 3. Creation de la VM pfSense

1. Creer une VM `pfsense-fw-01`.
2. Attacher l'ISO pfSense.
3. Ajouter les cartes reseau :

| Carte | Mode hyperviseur | Nom reseau |
|---:|---|---|
| 1 | NAT | WAN |
| 2 | Internal/Host-only | `DAYLIGHT_USERS` |
| 3 | Internal/Host-only | `DAYLIGHT_SERVERS` |
| 4 | Internal/Host-only | `DAYLIGHT_DMZ` |
| 5 | Internal/Host-only | `DAYLIGHT_MGMT` |
| 6 | Internal/Host-only | `DAYLIGHT_SOC` |

4. Installer pfSense avec les options par defaut.
5. Au premier demarrage, assigner les interfaces :

| pfSense | Role |
|---|---|
| `em0` ou equivalent | WAN |
| `em1` | USERS |
| `em2` | SERVERS |
| `em3` | DMZ |
| `em4` | MGMT |
| `em5` | SOC |

Les noms peuvent varier selon l'hyperviseur (`em`, `vtnet`, `hn`). Ce qui compte est l'ordre des cartes.

## 4. Adressage pfSense

Depuis le menu console pfSense, choisir `Set interface(s) IP address` et appliquer :

| Interface | Adresse | DHCP |
|---|---|---|
| WAN | DHCP | Non modifie |
| USERS | `10.10.10.1/24` | Optionnel, plage `10.10.10.100-10.10.10.199` |
| SERVERS | `10.10.20.1/24` | Non |
| DMZ | `10.10.30.1/24` | Non |
| MGMT | `10.10.40.1/24` | Optionnel |
| SOC | `10.10.50.1/24` | Non |

Depuis `admin-01`, configurer :

```text
IP      : 10.10.40.21
Masque  : 255.255.255.0
Gateway : 10.10.40.1
DNS     : 10.10.40.1
```

Puis ouvrir :

```text
https://10.10.40.1
```

## 5. Configuration des aliases

Dans pfSense, aller dans `Firewall > Aliases` et creer les objets du fichier :

```text
config/pfsense/pfsense_aliases.csv
```

Objets prioritaires a creer en premier :

| Alias | Valeur |
|---|---|
| `SOC_WAZUH` | `10.10.50.10` |
| `DAYLIGHT_APP` | `10.10.30.20` |
| `DAYLIGHT_DB` | `10.10.20.30` |
| `ADMIN_SUBNET` | `10.10.40.0/24` |
| `USERS_SUBNET` | `10.10.10.0/24` |
| `SERVERS_SUBNET` | `10.10.20.0/24` |
| `DMZ_SUBNET` | `10.10.30.0/24` |
| `SOC_SUBNET` | `10.10.50.0/24` |

## 6. Configuration des regles firewall

Dans `Firewall > Rules`, creer les regles dans l'ordre du fichier :

```text
config/pfsense/pfsense_firewall_rules.csv
```

Regles a montrer absolument :

| Interface | Action | Source | Destination | Pourquoi |
|---|---|---|---|---|
| WAN | Block | any | any | Refus entrant par defaut. |
| USERS | Pass | USERS_SUBNET | DAYLIGHT_APP:443 | Usage metier autorise. |
| USERS | Block | USERS_SUBNET | ADMIN_SUBNET | Pas d'acces admin depuis utilisateurs. |
| USERS | Block | USERS_SUBNET | SERVERS_SUBNET | Limite le mouvement lateral. |
| DMZ | Pass | DAYLIGHT_APP | DAYLIGHT_DB:5432 | Flux applicatif minimal. |
| SOC | Pass | any | SOC_WAZUH:514/1514/1515 | Collecte SOC. |

Activer `Log packets that are handled by this rule` sur les regles de blocage et sur les flux SOC importants.

## 7. NAT de demonstration

Dans `Firewall > NAT > Port Forward`, creer :

| Interface | Port externe | Destination | Port destination |
|---|---:|---|---:|
| WAN | 443/TCP | `10.10.30.20` | 443 |
| WAN | 1194/UDP | pfSense | 1194 |

Le detail est dans :

```text
config/pfsense/pfsense_nat_port_forward.csv
```

## 8. Envoi syslog pfSense vers Wazuh

Dans pfSense :

1. Aller dans `Status > System Logs > Settings`.
2. Activer `Remote Logging`.
3. Serveur distant : `10.10.50.10:514`.
4. Transport : UDP.
5. Categories : Firewall Events, System Events, DHCP, DNS Resolver, VPN.

Dans Wazuh, verifier ou ajouter l'ecoute syslog :

```xml
<remote>
  <connection>syslog</connection>
  <port>514</port>
  <protocol>udp</protocol>
  <allowed-ips>10.10.0.0/16</allowed-ips>
</remote>
```

Importer les regles :

```text
config/wazuh/local_rules_daylight_pfsense.xml
```

## 9. Tests concrets a lancer

### Depuis `poste-01` en USERS

Test autorise vers l'application :

```powershell
Test-NetConnection 10.10.30.20 -Port 443
```

Resultat attendu : `TcpTestSucceeded : True` si `daylight-app-01` ecoute en 443.

Test bloque vers MGMT :

```powershell
Test-NetConnection 10.10.40.1 -Port 443
```

Resultat attendu : echec ou blocage, avec log pfSense sur la regle USERS vers MGMT.

Test bloque vers serveur interne :

```powershell
Test-NetConnection 10.10.20.20 -Port 22
```

Resultat attendu : echec ou blocage, avec log pfSense sur la regle USERS vers SERVERS.

### Depuis `admin-01` en MGMT

Test autorise vers pfSense :

```powershell
Test-NetConnection 10.10.40.1 -Port 443
```

Resultat attendu : acces a l'interface pfSense.

Test autorise vers Wazuh :

```powershell
Test-NetConnection 10.10.50.10 -Port 443
```

Resultat attendu : acces Wazuh Dashboard si le service ecoute.

## 10. Rejeu des logs demo vers Wazuh

Generer les logs :

```powershell
python .\tools\generate_demo_logs.py
```

Verifier sans envoi reseau :

```powershell
python .\tools\send_demo_logs_to_syslog.py --dry-run
```

Envoyer les logs vers Wazuh si le port 514 UDP est pret :

```powershell
python .\tools\send_demo_logs_to_syslog.py --host 10.10.50.10 --port 514 --protocol udp
```

Envoyer seulement les logs pfSense :

```powershell
python .\tools\send_demo_logs_to_syslog.py --host 10.10.50.10 --port 514 --protocol udp --file pfsense.log
```

## 11. Recherches Wazuh a montrer

Dans Wazuh, chercher :

```text
pfsense-fw-01
```

Puis :

```text
rule.id:110010 OR rule.id:110020 OR rule.id:110040
```

Puis :

```text
DAYLIGHT_APP OR DAYLIGHT_AD OR DAYLIGHT_MAIL OR DAYLIGHT_ENDPOINT
```

## 12. Captures finales a produire

| Capture | Ecran |
|---|---|
| `CAP-13_pfsense-regles-firewall.png` | Regles USERS avec autorisation app et blocage MGMT/SERVERS. |
| `CAP-14_pfsense-syslog-wazuh.png` | Remote logging pfSense vers `10.10.50.10`. |
| `CAP-19_wazuh-pfsense-alertes.png` | Alertes Wazuh `110010` ou `110020`. |
| `CAP-20_wazuh-rejeu-logs-demo.png` | Rejeu logs demo ou recherche Wazuh associee. |

## 13. Plan B si pfSense n'est pas installe le jour J

Si la VM pfSense n'est pas prete, ne pas faire semblant. Montrer :

1. `Dashboards_Offline/daylight_pfsense_firewall_review.html` pour montrer la revue firewall complete en navigateur.
2. `config/pfsense/README_IMPORT_PFSENSE_DAYLIGHT.md` pour montrer les clics exacts dans pfSense.
3. `config/pfsense/pfsense_demo_test_plan.csv` pour montrer les tests attendus et les preuves Wazuh associees.
4. `config/pfsense/pfsense_firewall_rules.csv` et `config/pfsense/pfsense_syslog_wazuh.md` pour montrer la source technique.
5. `config/wazuh/local_rules_daylight_pfsense.xml`.
6. `python .\tools\send_demo_logs_to_syslog.py --dry-run`.
7. Les recherches Wazuh si le lab SIEM est disponible.

Phrase a utiliser :

> La configuration pfSense est fournie comme matrice concrete et reproductible. Si la VM pfSense n'est pas lancee pendant la soutenance, nous montrons les regles, le raccordement syslog et le rejeu de logs vers Wazuh sans presenter ces logs comme des preuves de production.
