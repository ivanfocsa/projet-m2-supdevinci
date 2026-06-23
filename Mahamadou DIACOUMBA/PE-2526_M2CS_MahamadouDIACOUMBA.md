# Rendu individuel developpe - Mahamadou DIACOUMBA

## Identification

| Champ | Valeur |
|---|---|
| Projet | Projet 4 - SOC externalise Daylight |
| Client fictif | Daylight |
| Prestataire | Cyber Trust |
| Membre | Mahamadou DIACOUMBA |
| Role principal | Responsable exploitation lab/VM, playbooks, procedures et REX incidents |
| Perimetre defendu | Exploitation du demonstrateur, relance Docker/VM, preflight, runbooks, playbooks, REX et preuves de fonctionnement |

## Synthese personnelle

Mon role est de rendre le projet exploitable. Une architecture et un SIEM peuvent etre bien concus, mais si le lab ne redemarre pas, si les procedures ne sont pas claires ou si les incidents ne sont pas documentes, le projet reste fragile.

Ma contribution couvre donc :

- la logique VM/conteneurs du demonstrateur ;
- la procedure de relance du lab ;
- les controles de sante avant demonstration ;
- les playbooks de reponse ;
- les REX incidents ;
- les preuves d'exploitation et de preflight.

Ma partie repond a une question tres concrete : "que fait l'equipe quand une alerte arrive ou quand le lab ne fonctionne pas ?"

## Objectifs d'exploitation

L'exploitation a trois objectifs :

1. rendre le lab redemarrable par l'equipe ;
2. fournir des procedures simples a appliquer ;
3. conserver des preuves et retours d'experience.

Ces objectifs sont importants pour la soutenance, mais aussi pour une future production Cyber Trust. Un SOC externalise doit pouvoir expliquer comment il agit, pas seulement comment il detecte.

## Inventaire du lab

L'inventaire est formalise dans :

`config/lab/daylight_vm_inventory.csv`

| Nom | Type | Zone | Services | Proprietaire principal | Preuve |
|---|---|---|---|---|---|
| `wazuh-manager` | Docker/VM | SOC | Wazuh manager, indexer, dashboard | Youssef | Dashboard login |
| `serveur-01` | Conteneur Docker | SERVERS | SSH, rsyslog, auth.log | Mahamadou | docker ps, alerte 5712 |
| `poste-01` | Endpoint Windows | USERS | Agent Wazuh, SCA | Youssef | Agents page |
| `pfsense-fw-01` | VM pfSense | Multi-zone | Firewall, NAT, syslog | Yvan/Mahamadou | Regles, remote logging |
| `daylight-app-01` | VM/conteneur | DMZ | HTTPS, logs metier | Kilyan/Youssef | Alertes Daylight |
| `admin-01` | Poste admin | MGMT | Navigateur, outils admin | Mahamadou | Acces pfSense/Wazuh |

Cet inventaire sert de base pour savoir quoi verifier avant de tourner la video.

## Procedure de demarrage du lab

Procedure minimale :

```powershell
# 1. Lancer Docker Desktop
# 2. Verifier l'etat Docker
docker ps

# 3. Demarrer les conteneurs utiles
docker start serveur-01

# 4. Entrer dans le serveur simule
docker exec -it serveur-01 bash
```

Dans le conteneur :

```bash
rsyslogd
service ssh start
/var/ossec/bin/wazuh-control start
exit
```

Cette procedure est importante car les services internes d'un conteneur ne sont pas toujours relances automatiquement apres extinction du PC.

## Runbook de preflight

Avant la video ou une demonstration, je dois lancer un controle de sante :

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\preflight_demo.ps1 -WriteReport
```

Le preflight doit verifier :

- presence des fichiers essentiels ;
- disponibilite Docker ;
- etat des conteneurs ;
- accessibilite Wazuh ;
- presence des captures ;
- etat du lien video ;
- presence du ZIP et hash.

Le rapport produit est :

`preflight-demo-report.txt`

Si une preuve CAP-25 est generee, elle doit correspondre a un etat reel du lab.

![Preflight demo OK](../Annexes_Captures/CAP-25_preflight-demo-ok.png)

## Script de reparation CAP-25

Le point fragile du projet etait la preuve de preflight. J'ai donc rattache mon perimetre a un outil de relance :

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe `
  -ExecutionPolicy Bypass `
  -File .\tools\repair_lab_and_capture_cap25.ps1 `
  -StartDockerDesktop `
  -StartKnownContainers `
  -WaitSeconds 180
```

Ce script sert a :

- verifier Docker ;
- lancer Docker Desktop si necessaire ;
- redemarrer les conteneurs connus ;
- relancer le preflight ;
- produire `CAP-25_preflight-demo-ok.png` uniquement si les conditions sont remplies ;
- documenter l'echec dans `lab-cap25-recovery-report.txt` si le lab n'est pas pret.

Point important : il ne faut pas fabriquer une preuve preflight si Wazuh ou Docker ne repondent pas. Le dossier doit rester credible.

## Generation et rejeu des logs

Le demonstrateur contient des logs de test dans :

`Demo_Logs/`

Fichiers importants :

| Fichier | Scenario |
|---|---|
| `pfsense.log` | Evenements firewall |
| `daylight_app.log` | Evenements application Daylight |
| `ad_files.log` | Privileges et fichiers |
| `endpoint_usb.log` | Support USB |
| `mail_phishing.log` | Phishing |

Commandes :

```powershell
python .\tools\generate_demo_logs.py
python .\tools\send_demo_logs_to_syslog.py --dry-run
```

Le `dry-run` est utile avant soutenance : il montre les evenements qui seraient envoyes sans modifier l'etat du SIEM.

![Rejeu logs demo](../Annexes_Captures/CAP-20_wazuh-rejeu-logs-demo.png)

![Dry-run rejeu logs](../Annexes_Captures/CAP-27_rejeu-logs-dry-run.png)

## Playbooks SOC

Les playbooks sont centralises dans :

`03_PLAYBOOKS_PROCEDURES_REX.md`

Ils permettent de passer d'une alerte a une action. Les principaux playbooks sont :

| ID | Incident | Regle associee | Priorite |
|---|---|---|---|
| PB-001 | Brute force SSH | `5712` | Haute |
| PB-002 | Acces anormal dossier patient | `100120` | Critique |
| PB-003 | Brute force applicatif Daylight | `100110` | Haute |
| PB-004 | Modification groupe privilegie | `100130` | Critique |
| PB-005 | USB non autorise | `100140` | Moyenne/Haute |
| PB-006 | Phishing signale | `100150` | Haute |
| PB-007 | Mouvement lateral inter-VLAN | `110020` | Critique |

![Playbook brute force](../Annexes_Captures/CAP-10_playbook-brute-force.png)

## Playbook PB-001 - Brute force SSH

Objectif : verifier si une attaque SSH est en cours ou si un compte a ete compromis.

Etapes :

1. ouvrir l'alerte Wazuh `5712` ;
2. relever l'IP source, l'utilisateur cible, l'heure et le serveur ;
3. verifier s'il existe une connexion reussie apres les echecs ;
4. consulter `/var/log/auth.log` sur `serveur-01` ;
5. bloquer l'IP source si l'attaque est confirmee ;
6. forcer le changement de mot de passe si le compte est suspect ;
7. documenter la preuve Wazuh et le log systeme ;
8. produire un mini REX.

Decision :

| Situation | Decision |
|---|---|
| Echecs seuls, IP externe connue | Blocage et surveillance |
| Echecs puis succes | Incident probable |
| Echecs internes repetes | Verification poste interne |
| Compte admin cible | Escalade prioritaire |

## Playbook PB-002 - Acces anormal dossier patient

Objectif : traiter rapidement un risque sur donnees sensibles.

Etapes :

1. ouvrir l'alerte `100120` ;
2. relever l'utilisateur, le site, le dossier patient, l'horaire ;
3. verifier le role metier de l'utilisateur ;
4. verifier si l'acces correspond a un rendez-vous ou une justification ;
5. si doute : suspendre la session ou le compte ;
6. prevenir le referent Daylight ;
7. escalader au DPO si l'incident est confirme ;
8. conserver les preuves ;
9. produire un REX.

Decision :

| Situation | Decision |
|---|---|
| Acces justifie par rendez-vous | Cloture avec justification |
| Acces hors role | Incident confirme |
| Acces massif | Escalade critique |
| Dossier VIP/sensible | Escalade immediate |

## Playbook PB-007 - Mouvement lateral inter-VLAN

Objectif : reagir a une tentative de contournement de segmentation.

Etapes :

1. ouvrir l'alerte `110020` ;
2. relever source, destination, port et zone cible ;
3. verifier la regle pfSense qui a bloque ;
4. verifier si la source est un poste utilisateur ou un serveur ;
5. chercher d'autres alertes sur la meme source ;
6. isoler la machine si comportement suspect ;
7. verifier presence malware ou compte compromis ;
8. documenter dans le REX.

Cette procedure fait le lien entre pfSense, Wazuh et l'exploitation.

![Qualification alerte pfSense](../Annexes_Captures/CAP-24_qualification-alerte-110020.png)

## REX incident

Le REX sert a apprendre de l'incident. Il doit repondre a ces questions :

| Question | Contenu attendu |
|---|---|
| Que s'est-il passe ? | Resume factuel |
| Quand ? | Horodatage debut/fin |
| Qui/quoi est touche ? | Utilisateur, poste, serveur, site |
| Comment l'alerte a ete detectee ? | Regle Wazuh, source log |
| Quelle action a ete prise ? | Blocage, escalade, verification |
| Quelle cause probable ? | Mot de passe faible, erreur, attaque |
| Quelle prevention ? | Regle, durcissement, sensibilisation |
| Quelle preuve ? | Capture, log, ticket, rapport |

![REX incident patient](../Annexes_Captures/CAP-11_rex-incident-acces-patient.png)

![REX incident rempli](../Annexes_Captures/CAP-28_rex-incident-rempli.png)

## Exploitation journaliere proposee

Pour une exploitation Cyber Trust, je propose la routine suivante :

| Frequence | Action | Responsable |
|---|---|---|
| Debut de journee | Verifier Wazuh, agents, dashboards | Exploitation |
| Quotidien | Lire alertes critiques et hautes | Analyste SOC |
| Quotidien | Verifier sources muettes | Exploitation |
| Hebdomadaire | Revue faux positifs | Kilyan/Youssef |
| Hebdomadaire | Sauvegarde configuration | Exploitation |
| Mensuel | Rapport client Daylight | Kilyan/Cyber Trust |
| Apres incident | REX et amelioration playbook | Mahamadou + equipe |

## Sauvegarde et restauration

Pour rendre la solution exploitable, il faut sauvegarder :

- configurations Wazuh ;
- regles custom ;
- dashboards ;
- fichiers pfSense ;
- scripts de lab ;
- logs de demonstration ;
- rapports de validation ;
- captures prioritaires ;
- ZIP final et hash.

Le manifeste `MANIFEST_DEPOT.md` aide a verifier l'integrite des fichiers. Le hash SHA256 du ZIP permet de prouver que le rendu n'a pas ete modifie apres generation.

## Troubleshooting lab

| Probleme | Diagnostic | Correction |
|---|---|---|
| Docker ne repond pas | `docker ps` echoue | Lancer Docker Desktop |
| `serveur-01` absent | `docker ps -a` | Redemarrer ou recreer conteneur |
| SSH inactif | `service ssh status` | `service ssh start` |
| rsyslog absent | logs non envoyes | `rsyslogd` |
| Agent Wazuh stoppe | pas d'alerte | `/var/ossec/bin/wazuh-control start` |
| Wazuh inaccessible | dashboard KO | relancer stack Wazuh |
| CAP-25 non genere | preflight KO | lire `lab-cap25-recovery-report.txt` |

## Plan de tests exploitation

| Test | Commande / action | Resultat attendu |
|---|---|---|
| EXP-01 | `docker ps` | Docker repond |
| EXP-02 | `docker start serveur-01` | Conteneur actif |
| EXP-03 | `service ssh status` | SSH actif |
| EXP-04 | `tail /var/log/auth.log` | Logs visibles |
| EXP-05 | `python .\tools\generate_demo_logs.py` | Logs demo crees |
| EXP-06 | `python .\tools\send_demo_logs_to_syslog.py --dry-run` | Evenements listes |
| EXP-07 | `preflight_demo.ps1` | Rapport preflight produit |
| EXP-08 | `repair_lab_and_capture_cap25.ps1` | CAP-25 ou rapport d'echec |

## Preuves rattachees a mon perimetre

| Preuve | Usage |
|---|---|
| `CAP-10_playbook-brute-force.png` | Playbook exploitable |
| `CAP-11_rex-incident-acces-patient.png` | REX incident patient |
| `CAP-20_wazuh-rejeu-logs-demo.png` | Rejeu logs |
| `CAP-24_qualification-alerte-110020.png` | Qualification pfSense |
| `CAP-25_preflight-demo-ok.png` | Sante demo |
| `CAP-27_rejeu-logs-dry-run.png` | Test sans envoi |
| `CAP-28_rex-incident-rempli.png` | REX complete |

## Documents et fichiers livrables

| Fichier | Role |
|---|---|
| `03_PLAYBOOKS_PROCEDURES_REX.md` | Playbooks et REX |
| `22_EXPLOITATION_VM_RUNBOOK_REX.md` | Exploitation VM/lab |
| `25_MODE_OPERATOIRE_CAPTURE_WAZUH_PREUVES.md` | Preuves Wazuh et preflight |
| `28_RUNBOOK_EXPRESS_PREUVES_RESTANTES.md` | Actions restantes |
| `config/lab/daylight_vm_inventory.csv` | Inventaire lab |
| `config/lab/daylight_lab_runbook.csv` | Runbook lab |
| `config/lab/daylight_rex_scenarios.csv` | Scenarios REX |
| `tools/preflight_demo.ps1` | Controle sante |
| `tools/repair_lab_and_capture_cap25.ps1` | Relance et preuve CAP-25 |
| `tools/generate_demo_logs.py` | Generation logs |
| `tools/send_demo_logs_to_syslog.py` | Envoi/dry-run logs |

## Ce que je dois montrer pendant la video

Mon passage doit montrer que le projet est exploitable :

1. ouvrir le playbook brute force ;
2. expliquer comment une alerte devient une action ;
3. ouvrir un REX incident ;
4. montrer le preflight ou CAP-25 ;
5. expliquer la procedure si Docker/Wazuh ne repond pas ;
6. montrer le dry-run de logs ou le rapport associe.

Texte court possible :

> Je suis Mahamadou DIACOUMBA, responsable exploitation lab, procedures et REX. Mon role est de garantir que le demonstrateur peut etre relance, teste et exploite, et que chaque incident critique donne lieu a une procedure et a un retour d'experience.

## Limites assumees

La partie exploitation reste adaptee a un demonstrateur :

- environnement local ;
- services parfois manuels a relancer ;
- pas de supervision de production complete ;
- pas de ticketing reel ;
- logs de demonstration partiellement simules.

Ces limites sont compensees par des procedures claires, des scripts de verification et des preuves documentaires.

## Apport personnel

Ce projet m'a montre qu'une solution cyber ne vaut pas seulement par ses outils, mais par sa capacite a etre exploitee. Les playbooks et le REX rendent le SOC plus professionnel : ils donnent une methode, une trace et une amelioration continue.

J'ai appris a penser :

- redemarrage ;
- verification ;
- preuve ;
- procedure ;
- action ;
- retour d'experience.

## Conclusion individuelle

Ma contribution securise la partie operationnelle du projet. Elle permet a Cyber Trust de montrer a Daylight que le SOC n'est pas seulement capable de detecter, mais aussi de reagir, documenter, relancer et ameliorer.

Le resultat concret est un ensemble de runbooks, playbooks, REX, scripts de preflight et preuves qui rendent la demonstration beaucoup plus robuste.
