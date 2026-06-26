# Guide de déploiement & d'utilisation - MVP SOC Daylight

Ce guide accompagne le livrable `08_GUIDE_DEPLOIEMENT_UTILISATION.pdf`.

## Démarrage rapide

```bash
cd Demonstrateur_Technique
python3 Outils_utiles/generate_demo_logs.py
python3 Outils_utiles/send_demo_logs_to_syslog.py --dry-run
```

## Rejeu pfSense uniquement

```bash
cd Demonstrateur_Technique
python3 Outils_utiles/send_demo_logs_to_syslog.py --dry-run --file pfsense.log
```

## Envoi vers Wazuh si le lab tourne

```bash
cd Demonstrateur_Technique
python3 Outils_utiles/send_demo_logs_to_syslog.py --host 10.10.50.10 --port 514 --protocol udp
```

## Requêtes Wazuh utiles

```text
filterlog OR rule.id:(110010 OR 110020 OR 110050)
rule.id:(100110 OR 100120 OR 100130 OR 100140 OR 100150)
```

## Preuves à montrer

- Architecture : `Participants/Yvan_FOCSA/Architecture_schemas/`
- pfSense : `Participants/Yvan_FOCSA/Captures_pfSense/`
- Wazuh / démonstrateur : `Demonstrateur_Technique/Preuves_Captures/`
- Playbooks : `Participants/Mahamadou_DIACOUMBA/Exploitation_playbooks_REX/`
- Script vidéo : `Soutenance_Video/Script_video/`
