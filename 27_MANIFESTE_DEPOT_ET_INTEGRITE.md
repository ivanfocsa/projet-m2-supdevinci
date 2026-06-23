# Manifeste depot et integrite - Daylight / Cyber Trust

## Role du livrable

Ce document explique comment verifier le rendu final avant depot. L'etat dynamique du dossier est genere dans les fichiers suivants :

- `MANIFEST_DEPOT.md` : lecture rapide pour le groupe, avec statut, captures restantes et pieces critiques.
- `MANIFEST_DEPOT.json` : inventaire complet des fichiers hashes en SHA-256.
- `PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.zip.sha256` : empreinte finale de l'archive ZIP, conservee a cote du ZIP.

Le manifeste est separe du hash final du ZIP parce que l'archive contient elle-meme le manifeste. Une archive ne peut donc pas contenir une empreinte finale d'elle-meme sans changer cette empreinte.

## Controle concret avant depot

1. Regenerer les preuves et rapports locaux :

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\post_capture_finalize.ps1
```

2. Relire le manifeste lisible :

```powershell
Get-Content .\MANIFEST_DEPOT.md
```

3. Verifier le hash final du ZIP :

```powershell
Get-FileHash -Algorithm SHA256 .\PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.zip
Get-Content .\PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.zip.sha256
```

Les deux valeurs doivent etre identiques.

## Regle de decision

Le dossier peut etre considere pret structurellement si les PDF, configurations, logs, dashboards, scripts, rapports et ZIP sont presents. Le depot officiel doit attendre les preuves reelles suivantes si le manifeste les signale encore :

| Preuve | Responsable | Action attendue |
|---|---|---|
| `CAP-01_wazuh-dashboard-login.png` | Youssef | Capturer le dashboard Wazuh connecte. |
| `CAP-02_agents-poste01-serveur01.png` | Youssef | Capturer les agents ou sources collectees. |
| `CAP-03_alerte-5712-brute-force-ssh.png` | Youssef | Capturer le detail d'alerte brute force SSH. |
| `CAP-25_preflight-demo-ok.png` | Mahamadou | Capturer le preflight OK apres relance du lab. |
| Video YouTube ou MP4 | Equipe | Ajouter le lien non repertorie ou le fichier MP4 final. |

## Pieces a montrer au jury

| Element | Emplacement |
|---|---|
| Dossier groupe complet | `Rendus_PDF/PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_DossierGroupeComplet.pdf` |
| Rapport groupe | `Rendus_PDF/PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_RapportGroupe.pdf` |
| Solutions concretes | `Rendu_Final/Solutions_Concretes/` |
| Config pfSense | `Rendu_Final/Config_PfSense/` |
| Config Wazuh | `Rendu_Final/Config_Wazuh/` |
| Dashboard offline | `Rendu_Final/Dashboards_Offline/daylight_soc_dashboard.html` |
| Manifeste | `Rendu_Final/Manifeste_Depot/MANIFEST_DEPOT.md` |

Ce livrable ne remplace pas les captures reelles : il sert a prouver que l'equipe sait exactement quoi livrer, quoi verifier et quoi completer avant le depot officiel.

