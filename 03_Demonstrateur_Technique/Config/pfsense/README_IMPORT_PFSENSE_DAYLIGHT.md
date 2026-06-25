# Import pfSense Daylight - guide concret

Ce fichier sert de support direct pendant la demo. Il indique quoi creer dans pfSense et comment prouver que la configuration fonctionne.

## 1. Interfaces a creer ou renommer

| Interface pfSense | VLAN | Adresse | Role |
|---|---:|---|---|
| WAN | - | DHCP/FAI | Acces Internet, refus entrant par defaut |
| USERS | 10 | `10.10.10.1/24` | Postes utilisateurs Daylight |
| SERVERS | 20 | `10.10.20.1/24` | AD, fichiers, base interne |
| DMZ | 30 | `10.10.30.1/24` | Portail Daylight expose |
| MGMT | 40 | `10.10.40.1/24` | Administration reservee |
| SOC | 50 | `10.10.50.1/24` | Wazuh et supervision Cyber Trust |

## 2. Aliases

Dans `Firewall > Aliases`, creer les objets du fichier `pfsense_aliases.csv`.

Ordre conseille :

1. Hotes critiques : `SOC_WAZUH`, `SOC_DASHBOARD`, `DAYLIGHT_APP`, `DAYLIGHT_DB`.
2. Reseaux : `USERS_SUBNET`, `SERVERS_SUBNET`, `DMZ_SUBNET`, `ADMIN_SUBNET`, `SOC_SUBNET`.
3. Groupes de controle : `RFC1918`, `DNS_ALLOWED`, `BLOCKLIST_WAN_DEMO`.

## 3. NAT

Dans `Firewall > NAT > Port Forward`, creer les lignes de `pfsense_nat_port_forward.csv`.

Point important a dire au jury : seule la DMZ est exposee, jamais le LAN interne.

## 4. Regles firewall

Dans `Firewall > Rules`, creer les regles de `pfsense_firewall_rules.csv` par interface et dans l'ordre `order`.

Regles a montrer en priorite :

1. WAN block par defaut.
2. WAN NAT HTTPS vers `DAYLIGHT_APP`.
3. USERS autorise DNS/HTTPS et bloque MGMT/SERVERS.
4. DMZ autorise uniquement le flux applicatif vers `DAYLIGHT_DB`.
5. SOC autorise la collecte et l'administration Wazuh.

Activer la journalisation sur toutes les regles de blocage et sur les flux critiques.

## 5. Remote logging vers Wazuh

Aller dans `Status > System Logs > Settings` :

1. Cocher `Enable Remote Logging`.
2. Serveur distant : `10.10.50.10:514`.
3. Protocole : UDP pour le lab.
4. Categories : Firewall Events, System Events, DHCP Events, DNS Resolver, VPN.

Cote Wazuh, utiliser `local_rules_daylight_pfsense.xml` et rechercher :

```text
filterlog OR rule.id:(110010 OR 110020 OR 110040)
```

## 6. Tests a executer

Le plan de tests pret a montrer est dans `pfsense_demo_test_plan.csv`.

En soutenance, ouvrir d'abord `daylight_pfsense_firewall_review.html`, puis ouvrir ce guide pour montrer les chemins exacts dans pfSense.
