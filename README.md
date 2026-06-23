# Projet M2 - Daylight / Cyber Trust

Rendu simplifie du projet M2 SUPDEVINCI pour le client fictif Daylight, realise par l'equipe Cyber Trust.

## Contenu du repository

Ce repository contient le rendu final et les sources utiles du projet :

- `Rendu_Simple_5PDF/` : les 5 PDF finaux a deposer.
- `config/wazuh/` : regles Wazuh, matrice de qualification, requetes dashboards.
- `config/pfsense/` : aliases, regles firewall, NAT, topologie et syslog vers Wazuh.
- `tools/` : scripts de generation, validation, preflight, logs demo, exports PDF.
- `Annexes_Captures/` : captures et preuves du demonstrateur.
- `Dashboards_Offline/` : dashboards HTML consultables sans SIEM live.
- `Demo_Logs/` : logs de demonstration pour rejouer les scenarios.
- `Video_Overlays/` et `config/video/` : supports pour la video de soutenance.
- dossiers individuels : sources des rendus Yvan, Youssef, Kilyan et Mahamadou.

Les dossiers generes en double comme `Rendus_PDF/`, `Rendus_HTML/` et `Rendu_Final/` ne sont pas versionnes car ils sont regenerables.

## Rendu a deposer

Le dossier principal a utiliser est `Rendu_Simple_5PDF/`.

Il contient les 5 PDF demandes et leurs versions modifiables en DOCX :

- `00_PROJET_COMPLET_Daylight_CyberTrust.pdf`
- `01_Yvan_FOCSA_Architecte_Solution_pfSense.pdf`
- `02_Youssef_GUERNIOU_SIEM_Wazuh.pdf`
- `03_Kilyan_FELIX_Detection_Dashboards_Qualification.pdf`
- `04_Mahamadou_DIACOUMBA_Playbooks_VM_REX.pdf`

Archives pretes a transmettre :

- `PE_2526_M2CS_Daylight_CyberTrust_Rendu_5PDF.zip`
- `PE_2526_M2CS_Daylight_CyberTrust_Rendu_5DOCX.zip`

## Roles

- Yvan FOCSA : architecture solution, pfSense, segmentation, flux reseau.
- Youssef GUERNIOU : SIEM Wazuh, agents, regles, RBAC.
- Kilyan FELIX : chef de projet SOC, detection, alertes, dashboards, qualification.
- Mahamadou DIACOUMBA : exploitation lab/VM, playbooks, procedures, REX.

## Validation locale

Commandes utiles :

```powershell
python .\tools\check_capture_pack.py
python .\tools\validate_rendu_final.py
```

Le seul warning attendu avant depot final complet est l'absence de lien YouTube ou MP4 de la video.
