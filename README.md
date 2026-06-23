# Projet M2 - Daylight / Cyber Trust

Rendu simplifie du projet M2 SUPDEVINCI pour le client fictif Daylight, realise par l'equipe Cyber Trust.

## Rendu a deposer

Le dossier principal a utiliser est `Rendu_Simple_5PDF/`.

Il contient uniquement les 5 PDF demandes :

- `00_PROJET_COMPLET_Daylight_CyberTrust.pdf`
- `01_Yvan_FOCSA_Architecte_Solution_pfSense.pdf`
- `02_Youssef_GUERNIOU_SIEM_Wazuh.pdf`
- `03_Kilyan_FELIX_Detection_Dashboards_Qualification.pdf`
- `04_Mahamadou_DIACOUMBA_Playbooks_VM_REX.pdf`

Une archive prete a transmettre est aussi disponible :

- `PE_2526_M2CS_Daylight_CyberTrust_Rendu_5PDF.zip`

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
