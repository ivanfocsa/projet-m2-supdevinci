# pfSense vers Wazuh - procedure syslog

## Objectif

Envoyer les logs pfSense au Wazuh Manager Cyber Trust pour detecter les refus WAN, mouvements inter-VLAN, evenements VPN et modifications d'administration.

## Cote pfSense

1. Ouvrir `Status > System Logs > Settings`.
2. Cocher `Enable Remote Logging`.
3. Dans `Remote log servers`, saisir `10.10.50.10:514`.
4. Choisir `UDP` pour le lab de demonstration.
5. Cocher les categories :
   - Firewall Events
   - System Events
   - DHCP Events
   - DNS Resolver
   - VPN
6. Sauvegarder.
7. Generer un evenement : tentative de connexion bloquee depuis USERS vers MGMT ou scan depuis WAN.

## Cote Wazuh Manager

Ajouter dans `ossec.conf` si l'ecoute syslog n'est pas deja active :

```xml
<remote>
  <connection>syslog</connection>
  <port>514</port>
  <protocol>udp</protocol>
  <allowed-ips>10.10.0.0/16</allowed-ips>
  <local_ip>10.10.50.10</local_ip>
</remote>
```

Puis copier les regles :

```powershell
copy .\config\wazuh\local_rules_daylight_pfsense.xml local_rules.xml
```

Dans un conteneur Wazuh, le chemin habituel est :

```text
/var/ossec/etc/rules/local_rules.xml
```

Redemarrer le manager apres ajout des regles.

## Preuve attendue

Dans Wazuh Discover ou Security Events, chercher :

```text
pfsense OR filterlog OR rule.id:110010 OR rule.id:110020
```

Captures conseillees :

1. Configuration remote logging pfSense.
2. Ligne `filterlog` brute.
3. Alerte Wazuh `110010` ou `110020`.
4. Dashboard avec source `pfsense-fw-01`.
