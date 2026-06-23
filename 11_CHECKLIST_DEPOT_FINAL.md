# Checklist depot final - Daylight / Cyber Trust

## Objectif

Cette checklist sert pour les 30 dernieres minutes avant depot officiel. Elle verifie que le ZIP contient le bon fond, le bon format et les preuves les plus importantes.

## 1. Nomenclature

| Element | Verification |
|---|---|
| Code promo | Remplacer `M2CS` si le code promo officiel est different. |
| Nom ZIP | `PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.zip` |
| Rapport groupe | `PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_RapportGroupe.pdf` |
| Rendus individuels | Un PDF par membre dans `Rendus_PDF/`. |
| Video | Lien YouTube non repertorie dans le TXT ou MP4 selon consigne retenue. |

## 2. Pieces obligatoires dans le ZIP

| Piece | Attendu |
|---|---|
| Rapport groupe PDF | Present |
| Rendus individuels PDF | Yvan, Youssef, Kilyan, Mahamadou |
| Guide de deploiement | Present |
| Playbooks et REX | Present |
| Script video / notes orateur | Present |
| PowerPoint | Present |
| Preuves SIEM de Youssef | PDF + script PowerShell |
| Pack solutions concretes | pfSense, Wazuh custom rules, logs demo |
| Captures Wazuh | A ajouter dans `Annexes_Captures/` |
| Lien video | A coller dans le fichier TXT |

## 3. Captures prioritaires

Les captures minimales validees par `config/captures/daylight_capture_checklist.csv` sont :

1. `CAP-01_wazuh-dashboard-login.png` - Wazuh Dashboard connecte.
2. `CAP-02_agents-poste01-serveur01.png` - agents ou sources `poste-01` et `serveur-01`.
3. `CAP-03_alerte-5712-brute-force-ssh.png` - alerte brute force SSH `5712` ouverte en detail.
4. `CAP-06_alerte-100120-acces-patient.png` - alerte acces dossier patient `100120`.
5. `CAP-07_dashboard-technique.png` - dashboard technique analyste.
6. `CAP-08_dashboard-executif.png` - dashboard executif client.
7. `CAP-13_pfsense-regles-firewall.png` - matrice/regles pfSense concretes.
8. `CAP-25_preflight-demo-ok.png` - preflight OK apres relance Docker/Wazuh.

Les captures deja presentes et les manquantes sont controlees par :

```powershell
python .\tools\check_capture_pack.py
```

Pour la procedure courte, ouvrir `28_RUNBOOK_EXPRESS_PREUVES_RESTANTES.md`.
## 4. Commande finale recommandee

Apres ajout des captures ou du lien video, lancer toute la chaine :

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\post_capture_finalize.ps1
```

## 5. Commandes de controle

Lancer le preflight :

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\preflight_demo.ps1 -WriteReport
```

Generer et verifier les logs de demonstration concrets :

```powershell
python .\tools\generate_demo_logs.py
python .\tools\send_demo_logs_to_syslog.py --dry-run
```

Regenerer l'annexe captures apres depot des images :

```powershell
python .\tools\build_capture_annex.py
```

Regenerer les PDF :

```powershell
python .\tools\export_markdown_to_pdf.py
```

Regenerer le dossier groupe complet :

```powershell
python .\tools\build_group_dossier_pdf.py
```

Regenerer le PowerPoint :

```powershell
python .\tools\build_presentation_pptx.py
```

Reconstruire le dossier final et le ZIP :

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\rebuild_rendu_final.ps1
```

## 6. Validation finale

Avant depot, ouvrir :

- `Rendu_Final/README_A_LIRE.md`
- `Rendu_Final/Rendus_PDF/PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_RapportGroupe.pdf`
- `Rendu_Final/Presentation/Presentation_Daylight_CyberTrust.pptx`
- `Rendu_Final/Video/PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_video-lien.txt`

Le depot est pret quand :

- les captures sont presentes ;
- le lien video est renseigne ;
- le ZIP final a ete regenere apres ces ajouts ;
- le preflight ne signale plus que Docker/Wazuh eteint si le lab n'a pas besoin d'etre rendu avec l'archive.




