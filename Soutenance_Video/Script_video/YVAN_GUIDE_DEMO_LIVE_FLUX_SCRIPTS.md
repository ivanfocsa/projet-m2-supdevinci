# Guide Yvan FOCSA - Démo live flux, pfSense et scripts

Ce guide sert à préparer la partie vidéo de Yvan FOCSA. L’objectif n’est pas de tout tester, mais de montrer une chaîne crédible et compréhensible : architecture, règles pfSense, journalisation, alerte Wazuh.

## 1. Ce que Yvan doit défendre

Yvan présente le rôle d’architecte solution. Sa partie répond à trois questions client :

1. Comment le réseau Daylight est-il structuré ?
2. Comment pfSense contrôle-t-il les flux ?
3. Comment un blocage réseau devient-il exploitable par le SOC Wazuh ?

Phrase d’ouverture conseillée :

> Mon rôle est de présenter l’architecture réseau du démonstrateur. L’idée est de montrer que le SOC ne se limite pas à Wazuh : il repose aussi sur une segmentation claire, des flux maîtrisés et un firewall capable de produire des événements utiles pour l’analyse SOC.

## 2. Fichiers à ouvrir avant de filmer

Ouvrir ces fichiers dans cet ordre :

| Ordre | Fichier | Ce que ça prouve |
|---|---|---|
| 1 | `Participants/Yvan_FOCSA/Architecture_schemas/YVAN_Schemas_Architecture-Architecture globale.drawio.png` | Vision d’ensemble : USERS, SERVERS, DMZ, MGMT, SOC, WAN. |
| 2 | `Participants/Yvan_FOCSA/Architecture_schemas/YVAN_Schemas_Architecture-pfSense flux et regles.drawio.png` | Flux autorisés, flux bloqués et journalisation SOC. |
| 3 | `Participants/Yvan_FOCSA/Captures_pfSense/dashboard.png` | pfSense est bien déployé en VM. |
| 4 | `Participants/Yvan_FOCSA/Captures_pfSense/Interfaces Assignements.png` | WAN sur `em0`, LAN sur `em1`. |
| 5 | `Participants/Yvan_FOCSA/Captures_pfSense/Aliases.png` | Les règles utilisent des objets lisibles : `ADMIN_SUBNET`, `SOC_WAZUH`, `DAYLIGHT_APP`. |
| 6 | `Participants/Yvan_FOCSA/Captures_pfSense/Rules LAN.png` | Politique LAN : autoriser le nécessaire, bloquer les zones sensibles. |
| 7 | `Participants/Yvan_FOCSA/Captures_pfSense/regles wan.png` | Posture WAN restrictive : aucun flux entrant inutile. |
| 8 | `Participants/Yvan_FOCSA/Captures_pfSense/Syslog Wazuh.png` | pfSense envoie les logs vers Wazuh en UDP 514. |
| 9 | `Participants/Yvan_FOCSA/Captures_pfSense/wazuh traffict entrabnt bloqué WAN - loiuvement lateral vert MGMT.png` | Les événements pfSense apparaissent dans Wazuh avec les règles `110010` et `110020`. |

## 3. Scripts à expliquer

### `generate_demo_logs.py`

Ce script génère des logs de démonstration dans `Demonstrateur_Technique/Demo_Logs`.

Il crée plusieurs fichiers :

| Fichier | Source simulée |
|---|---|
| `pfsense.log` | Firewall pfSense : scan WAN, mouvement latéral, VPN, flux suspect. |
| `daylight_app.log` | Application métier Daylight. |
| `ad_files.log` | Active Directory et fichiers patients. |
| `mail_phishing.log` | Messagerie et phishing. |
| `endpoint_usb.log` | Poste utilisateur et USB. |

Commande :

```powershell
python .\Demonstrateur_Technique\Outils_utiles\generate_demo_logs.py
```

Phrase à dire :

> Ce script permet de rejouer des événements réalistes sans dépendre d’une attaque réelle. Il sert à alimenter le démonstrateur avec des logs contrôlés et reproductibles.

### `send_demo_logs_to_syslog.py`

Ce script lit les logs générés et les envoie vers une cible syslog, par exemple Wazuh.

Mode vérification sans envoi :

```powershell
python .\Demonstrateur_Technique\Outils_utiles\send_demo_logs_to_syslog.py --file pfsense.log --dry-run
```

Envoi vers Wazuh en UDP 514 :

```powershell
python .\Demonstrateur_Technique\Outils_utiles\send_demo_logs_to_syslog.py --host 10.10.50.10 --port 514 --protocol udp --file pfsense.log
```

Si Wazuh tourne sur la machine locale :

```powershell
python .\Demonstrateur_Technique\Outils_utiles\send_demo_logs_to_syslog.py --host 127.0.0.1 --port 514 --protocol udp --file pfsense.log
```

Phrase à dire :

> Ce script rejoue les logs vers Wazuh. Il permet de prouver la partie industrialisable : on peut générer, rejouer et qualifier les événements de manière reproductible.

### `local_rules_daylight_pfsense.xml`

Ce fichier contient les règles Wazuh associées au projet.

Règles importantes pour Yvan :

| Règle | Niveau | Sens |
|---|---:|---|
| `110010` | 8 | pfSense : trafic entrant bloqué sur WAN. |
| `110020` | 10 | pfSense : tentative de mouvement latéral vers MGMT. |
| `110021` | 10 | pfSense : tentative de mouvement latéral vers SERVERS. |
| `110022` | 10 | pfSense : tentative de mouvement latéral vers SOC. |
| `110040` | 7 | pfSense : connexion VPN admin. |
| `110050` | 11 | pfSense : flux sortant suspect volumineux. |

Phrase à dire :

> Les règles Wazuh transforment un log firewall brut en événement SOC qualifiable. Par exemple, un blocage vers la zone d’administration devient une alerte de mouvement latéral.

## 4. Tests live conseillés

Avant de filmer, lancer :

```powershell
.\Demonstrateur_Technique\Outils_utiles\test_yvan_live_flux.ps1
```

### Test 1 : accès interface pfSense

Commande manuelle :

```powershell
Test-NetConnection 10.10.40.1 -Port 443
```

Résultat attendu :

`TcpTestSucceeded : True`

Phrase :

> Ce test montre que l’interface d’administration pfSense est accessible depuis le réseau d’administration du lab.

### Test 2 : ICMP vers pfSense

Commande :

```powershell
C:\Windows\System32\ping.exe -n 2 10.10.40.1
```

Résultat possible :

Le ping peut échouer. Ce n’est pas bloquant : l’interface HTTPS peut être disponible même si l’ICMP est filtré.

Phrase :

> Ici, l’important n’est pas que tout réponde au ping, mais que les flux soient contrôlés. Le firewall peut laisser passer l’administration HTTPS tout en bloquant d’autres protocoles.

### Test 3 : tentative vers une zone sensible

Commande :

```powershell
Test-NetConnection 10.10.20.20 -Port 445
```

Résultat attendu :

`TcpTestSucceeded : False`

Phrase :

> Ce test simule une tentative d’accès depuis la zone d’administration ou utilisateur vers un serveur interne. L’échec est attendu : il prouve la logique de segmentation.

### Test 4 : logs pfSense rejoués

Commande :

```powershell
python .\Demonstrateur_Technique\Outils_utiles\send_demo_logs_to_syslog.py --file pfsense.log --dry-run
```

Phrase :

> Je montre d’abord les logs en mode dry-run pour expliquer ce qui va être envoyé : un scan WAN bloqué, une tentative de mouvement latéral vers MGMT, un accès HTTPS métier et un événement VPN.

### Test 5 : recherche Wazuh

Dans Wazuh, chercher :

```text
rule.id:110010 OR rule.id:110020 OR pfsense-fw-01
```

Phrase :

> Cette recherche isole les événements pfSense liés à l’architecture réseau. On voit que le firewall alimente bien la supervision SOC.

## 5. Déroulé vidéo recommandé

### Minute 0:00 à 0:30

Montrer le schéma global.

Dire :

> J’ai découpé l’architecture en zones pour éviter un réseau plat. Les postes, les serveurs, la DMZ, l’administration et le SOC sont séparés logiquement. Cette segmentation est essentielle pour limiter les mouvements latéraux.

### Minute 0:30 à 1:10

Montrer le schéma pfSense flux.

Dire :

> Les flux verts correspondent aux usages nécessaires, par exemple l’accès HTTPS à l’application Daylight. Les flux rouges représentent les accès bloqués vers les zones sensibles. Le flux violet correspond à la journalisation vers le SOC.

### Minute 1:10 à 2:00

Montrer pfSense dashboard, interfaces et aliases.

Dire :

> Dans le lab, pfSense est déployé en VM. Les interfaces WAN et LAN sont configurées, et les aliases rendent les règles compréhensibles. Cela permet de parler en objets métier plutôt qu’en IP brutes.

### Minute 2:00 à 2:45

Montrer règles LAN/WAN.

Dire :

> La politique est volontairement simple : autoriser ce qui est nécessaire, bloquer l’accès direct aux zones sensibles, journaliser les refus utiles. Côté WAN, aucune règle entrante permissive n’est ajoutée dans le démonstrateur.

### Minute 2:45 à 3:30

Montrer syslog puis Wazuh.

Dire :

> Le point important est la supervision. pfSense envoie ses logs vers Wazuh en syslog UDP 514. Les règles Wazuh `110010` et `110020` montrent que les blocages réseau deviennent des alertes SOC exploitables.

### Fin

Transition vers Youssef :

> Une fois cette base réseau posée, Youssef peut montrer comment Wazuh collecte, corrèle et affiche les événements dans les dashboards.

## 6. Si le live ne marche pas

Ne pas dire que le projet ne marche pas.

Dire :

> Pour garder une démonstration stable, je bascule sur les preuves validées du lab.

Puis montrer :

1. `Rules LAN.png`
2. `Syslog Wazuh.png`
3. `wazuh traffict entrabnt bloqué WAN - loiuvement lateral vert MGMT.png`

Phrase :

> La preuve importante reste la chaîne complète : règle pfSense, log firewall, remontée Wazuh, alerte qualifiable.

