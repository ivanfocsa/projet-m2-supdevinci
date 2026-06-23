# Tableau de bord statut final - Daylight / Cyber Trust

## Objectif

Ce livrable donne une vue unique de fin de projet : captures prioritaires, video, PDF, ZIP et commandes restantes. Il est utile quand l'equipe prepare le depot ou la soutenance et veut savoir immediatement ce qui bloque encore.

## Fichiers generes

| Fichier | Role |
|---|---|
| `Dashboards_Offline/daylight_final_evidence_status.html` | Tableau de bord HTML ouvrable localement. |
| `evidence-status-report.txt` | Rapport texte court pour archivage. |
| `tools/build_final_evidence_dashboard.py` | Generateur du tableau de bord. |
| `tools/extract_youssef_wazuh_proofs.py` | Regeneration des preuves Wazuh deja presentes dans le PDF SIEM de Youssef. |

## Generation

Depuis la racine du projet :

```powershell
python .\tools\build_final_evidence_dashboard.py
```

Le script lit :

- `config/captures/daylight_capture_checklist.csv` ;
- `Annexes_Captures/` ;
- le fichier lien video ou les MP4 candidats ;
- le ZIP et son fichier `.sha256` ;
- les PDF generes.

## Ce que montre le dashboard

| Bloc | Information |
|---|---|
| Captures prioritaires | Ratio `presentes / attendues`. |
| Video | Lien YouTube ou MP4 final detecte, sinon action restante. |
| PDF | Nombre de PDF exportes. |
| ZIP | Presence de l'archive finale. |
| Commandes restantes | Commandes `import_final_evidence.ps1` et `post_capture_finalize.ps1` pretes a copier. |

## Regle d'usage

Le dashboard est une aide de pilotage. `CAP-01`, `CAP-02` et `CAP-03` peuvent etre regenerees depuis le PDF SIEM de Youssef ou recapturees dans Wazuh si le lab repond. `CAP-25` doit rester une preuve preflight reelle : elle n'est creee que si Docker et Wazuh sont accessibles.

## Commande finale apres preuves

Quand les captures et la video sont ajoutees :

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\post_capture_finalize.ps1
```

