# Import des preuves finales - Daylight / Cyber Trust

## Objectif

Ce livrable evite les erreurs de nommage au moment ou les captures Wazuh et la video sont enfin disponibles. Il sert a importer un fichier pris manuellement, le renommer exactement comme attendu, puis relancer les controles.

## Outil

```text
tools/import_final_evidence.ps1
```

L'outil gere :

| Type | Action |
|---|---|
| `CAP-01` | Copie une capture PNG vers `Annexes_Captures/CAP-01_wazuh-dashboard-login.png`. |
| `CAP-02` | Copie une capture PNG vers `Annexes_Captures/CAP-02_agents-poste01-serveur01.png`. |
| `CAP-03` | Copie une capture PNG vers `Annexes_Captures/CAP-03_alerte-5712-brute-force-ssh.png`. |
| `CAP-25` | Copie une capture PNG ou tente de generer la preuve depuis le preflight. |
| `VIDEO-LINK` | Ecrit le lien YouTube non repertorie dans le fichier attendu. |
| `VIDEO-MP4` | Copie un MP4 final a la racine avec la nomenclature attendue. |

## Importer les captures Wazuh

Apres avoir pris les captures depuis Wazuh, lancer :

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\import_final_evidence.ps1 -Item CAP-01 -SourcePath "C:\Temp\capture-wazuh-login.png" -RunChecks
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\import_final_evidence.ps1 -Item CAP-02 -SourcePath "C:\Temp\capture-agents.png" -RunChecks
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\import_final_evidence.ps1 -Item CAP-03 -SourcePath "C:\Temp\capture-alerte-5712.png" -RunChecks
```

L'outil refuse les fichiers non PNG et les captures trop petites, afin d'eviter d'importer un mauvais fichier.

## Produire ou importer CAP-25

Si Docker et Wazuh repondent, executer d'abord :

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\preflight_demo.ps1 -WriteReport
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\import_final_evidence.ps1 -Item CAP-25 -RunChecks
```

Si le script genere `PRE-25_preflight-a-reprendre.png` au lieu de `CAP-25_preflight-demo-ok.png`, le lab n'est pas encore valide. Relancer Docker/Wazuh puis refaire le preflight.

## Importer la video

Option YouTube non repertoriee :

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\import_final_evidence.ps1 -Item VIDEO-LINK -YoutubeUrl "https://youtu.be/xxxx" -RunChecks
```

Option MP4 :

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\import_final_evidence.ps1 -Item VIDEO-MP4 -SourcePath "C:\Temp\demo-daylight.mp4" -RunChecks
```

Le MP4 doit depasser 10 Mo pour etre accepte par `tools/check_video_ready.py`.

## Finaliser apres toutes les preuves

Quand `CAP-01`, `CAP-02`, `CAP-03`, `CAP-25` et la video sont disponibles :

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\import_final_evidence.ps1 -Item VIDEO-LINK -YoutubeUrl "https://youtu.be/xxxx" -Finalize
```

Ou lancer directement :

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\post_capture_finalize.ps1
```

## Resultat attendu

La validation doit finir par :

```text
[OK] Rendu final complet selon les controles automatises.
```

Si des warnings restent, lire `capture-pack-report.txt`, `video-readiness-report.txt` et `validation-rendu-final.txt`.
