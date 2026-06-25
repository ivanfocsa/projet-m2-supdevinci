# Demo logs Daylight / Cyber Trust

Ces fichiers sont des logs de demonstration, crees pour montrer les sources que le SOC Cyber Trust collecte et correle.

## Fichiers generes

| Fichier | Source simulee |
|---|---|
| `pfsense.log` | Firewall pfSense, VLAN, WAN, VPN. |
| `daylight_app.log` | Application metier Daylight. |
| `ad_files.log` | Annuaire et serveur fichiers. |
| `mail_phishing.log` | Messagerie et phishing. |
| `endpoint_usb.log` | Endpoint et support USB. |

## Usage

1. Les ouvrir pendant la video pour montrer les evenements bruts.
2. Les envoyer vers Wazuh via syslog ou un agent si le lab est disponible.
3. Les rapprocher des regles `config/wazuh/local_rules_daylight_pfsense.xml`.

Ces logs ne remplacent pas les captures Wazuh finales demandees dans `Annexes_Captures/`.
