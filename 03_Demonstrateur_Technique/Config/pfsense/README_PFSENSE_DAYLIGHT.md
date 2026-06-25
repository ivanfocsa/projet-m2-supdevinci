# pfSense Daylight - configuration concrete

Ce dossier contient la proposition pfSense concrete pour le projet Daylight / Cyber Trust.

## Fichiers

| Fichier | Role |
|---|---|
| `pfsense_aliases.csv` | Objets reseau a creer dans `Firewall > Aliases`. |
| `pfsense_firewall_rules.csv` | Regles a creer dans `Firewall > Rules`. |
| `pfsense_nat_port_forward.csv` | NAT a creer dans `Firewall > NAT > Port Forward`. |
| `pfsense_syslog_wazuh.md` | Procedure d'envoi des logs pfSense vers Wazuh. |

## Interfaces retenues

| Interface | VLAN | IP passerelle | Usage |
|---|---:|---|---|
| WAN | - | DHCP/FAI | Internet. |
| USERS | 10 | `10.10.10.1/24` | Postes utilisateurs Daylight. |
| SERVERS | 20 | `10.10.20.1/24` | AD, fichiers, bases. |
| DMZ | 30 | `10.10.30.1/24` | Application Daylight. |
| MGMT | 40 | `10.10.40.1/24` | Administration. |
| SOC | 50 | `10.10.50.1/24` | Wazuh et supervision Cyber Trust. |

## Captures a faire si pfSense est installe

1. Tableau des interfaces/VLAN.
2. Aliases pfSense.
3. Regles WAN avec blocage par defaut.
4. Regles USERS montrant le deny vers MGMT/SERVERS.
5. Regles SOC/Wazuh.
6. NAT HTTPS vers DMZ.
7. Remote Logging vers `10.10.50.10`.
8. Evenement `filterlog` visible cote Wazuh.
