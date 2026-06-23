# Mode operatoire demo jour J - Daylight / Cyber Trust

## Objectif

Ce mode operatoire sert a lancer, verifier et enregistrer la demonstration du SOC Daylight sans oublier une preuve. Il complete le guide de deploiement, le support PowerPoint et le dossier de captures.

## Avant de commencer

Verifier que les fichiers suivants sont accessibles :

- `Presentation_Daylight_CyberTrust.pptx`
- `04_SCRIPT_VIDEO_DEMO.md`
- `09_NOTES_ORATEUR_SOUTENANCE.md`
- `07_DOSSIER_PREUVES_CAPTURES.md`
- `Youssef GUERNIOU/setup-siem-lab.ps1`
- `Annexes_Captures/`

## T-30 minutes - Preparation technique

1. Brancher le PC sur secteur.
2. Fermer les applications inutiles.
3. Lancer Docker Desktop.
4. Ouvrir PowerShell dans la racine du projet.
5. Lancer le preflight :

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\preflight_demo.ps1 -WriteReport
python .\tools\render_static_proof_images.py
```

6. Lire `preflight-demo-report.txt` si le script l'a genere.

## T-25 minutes - Lancement du lab

Depuis la racine technique du lab Wazuh, si `package.json` existe dans cette racine technique :

```powershell
npm run lab:start
```

Puis lancer ou relancer la preparation SIEM :

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File ".\Youssef GUERNIOU\setup-siem-lab.ps1"
```

Si le script est execute depuis une autre racine que le lab npm, l'etape Daylight peut etre ignoree par le script. Dans ce cas, lancer les commandes Daylight depuis la racine technique qui contient `package.json`.

## T-20 minutes - Redemarrage manuel de `serveur-01` si necessaire

Si `serveur-01` existe mais ne remonte pas correctement :

```powershell
docker start serveur-01
docker exec -it serveur-01 bash
```

Dans le conteneur :

```bash
rsyslogd
service ssh start
/var/ossec/bin/wazuh-control start
exit
```

## T-15 minutes - Verification Wazuh

Ouvrir :

```text
https://localhost
```

Verifier :

| Element | Attendu |
|---|---|
| Connexion admin | OK |
| Agent `poste-01` | Visible |
| Agent `serveur-01` | Visible |
| Alertes SSH | Regle `5712` visible |
| Alertes Daylight | Regles `100110`, `100120`, `100130`, `100140` visibles |
| Dashboard technique | Charge |
| Dashboard executif | Charge |
| Compte analyste | Lecture seule |

## T-10 minutes - Captures obligatoires

Deposer les captures dans `Annexes_Captures/`.

Priorite haute :

1. `CAP-01_wazuh-dashboard-login.png`
2. `CAP-02_agents-poste01-serveur01.png`
3. `CAP-03_alerte-5712-brute-force-ssh.png`
4. `CAP-06_alerte-100120-acces-patient.png`
5. `CAP-07_dashboard-technique.png`
6. `CAP-08_dashboard-executif.png`
7. `CAP-13_pfsense-regles-firewall.png`
8. `CAP-25_preflight-demo-ok.png`

Priorite utile :

1. `CAP-10_playbook-brute-force.png`
2. `CAP-11_rex-incident-acces-patient.png`
3. `CAP-12_architecture-solution.png`
4. `CAP-14_pfsense-syslog-wazuh.png`
5. `CAP-15_script-setup-siem-lab.png`
6. `CAP-16_auth-log-serveur01.png`

## T-5 minutes - Preparation video

1. Ouvrir le PowerPoint.
2. Ouvrir Wazuh Dashboard dans des onglets deja prepares.
3. Ouvrir les notes orateur.
4. Tester le micro.
5. Verifier que chaque intervenant a sa sequence.
6. Preparer l'affichage du nom de l'intervenant.

## Sequence video recommandee

| Temps | Intervenant | Ecran |
|---:|---|---|
| 00:00 - 01:30 | Kilyan | Slides 1 a 4 |
| 01:30 - 04:00 | Yvan | Slides 5 et 6 |
| 04:00 - 08:30 | Youssef | Wazuh : agents, sources, alertes |
| 08:30 - 11:30 | Kilyan | Dashboards et qualification |
| 11:30 - 14:30 | Mahamadou | Playbooks, REX, redemarrage |
| 14:30 - 17:00 | Yvan + equipe | Couts, limites, conclusion |

## Deroulement de demo minimal si le temps manque

Si la video doit etre plus courte, montrer absolument :

1. contexte Daylight ;
2. architecture Cyber Trust ;
3. agents Wazuh ;
4. alerte `5712` ;
5. alerte `100120` ;
6. dashboard technique ;
7. dashboard executif ;
8. RBAC analyste ;
9. playbook PB-001 ou PB-002 ;
10. conclusion industrialisation.

## Depannage rapide

| Probleme | Verification | Action |
|---|---|---|
| Docker ne repond pas | `docker info` | Lancer Docker Desktop, attendre, relancer la commande. |
| Wazuh inaccessible | `https://localhost` | Relancer le lab depuis sa racine technique ; si elle contient `package.json`, utiliser `npm run lab:start`. |
| `serveur-01` arrete | `docker ps -a` | `docker start serveur-01`. |
| Pas d'alerte SSH | Logs `auth.log` | Relancer la simulation via le script SIEM. |
| Pas de logs Daylight | Presence `package.json` | Lancer les scripts npm Daylight depuis la bonne racine. |
| Compte analyste trop permissif | Role `soc_readonly` | Relancer l'etape RBAC du script SIEM. |
| Capture illisible | Zoom navigateur | Monter le zoom a 110 ou 125 %. |

## Apres enregistrement

1. Verifier que la video dure 15 a 20 minutes.
2. Verifier que chaque membre parle.
3. Verifier que les noms sont affiches.
4. Mettre le lien YouTube non repertorie dans :

```text
PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_video-lien.txt
```

5. Regenerer le ZIP final si des captures ou le lien ont ete ajoutes : `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\post_capture_finalize.ps1`.

## Commandes de regeneration

```powershell
python .\tools\export_markdown_to_pdf.py
python .\tools\build_presentation_pptx.py
```

Puis reconstruire l'archive finale si necessaire.





