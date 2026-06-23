# Guide manuel projet - Daylight / Cyber Trust

Ce document est fait pour travailler a la main sans se perdre dans tous les fichiers du projet. Il resume le projet complet, ce qui existe deja, ce qu'il faut montrer, ce qu'il faut faire a la main, et detaille surtout la partie Yvan FOCSA : architecture, pfSense, segmentation, flux, preuves et presentation.

## 1. Resume tres court du projet

Le client fictif est **Daylight**, un reseau de centres d'audioprothesistes. Daylight manipule des donnees sensibles liees aux patients, aux rendez-vous, aux dossiers metier et aux comptes utilisateurs.

Le prestataire est **Cyber Trust**. L'objectif est de proposer un **SOC externalise** capable de :

- centraliser les evenements de securite ;
- superviser plusieurs sources de logs ;
- detecter des incidents concrets ;
- qualifier les alertes ;
- produire des dashboards exploitables ;
- documenter des procedures de reponse aux incidents ;
- montrer une architecture securisee et industrialisable.

Le projet est un **demonstrateur**, pas une production complete. Il doit prouver la faisabilite technique et organisationnelle.

## 2. Equipe et roles

| Personne | Role projet | Ce qu'elle defend |
|---|---|---|
| Yvan FOCSA | Architecte solution | Architecture, segmentation, pfSense, zones reseau, flux, securisation, cible production |
| Youssef GUERNIOU | Ingenieur SIEM Wazuh | Wazuh, agents, collecte, alertes, RBAC, dashboards SIEM |
| Kilyan FELIX | Chef projet detection | Qualification des alertes, dashboards, SLA, priorisation, synthese client |
| Mahamadou DIACOUMBA | Exploitation lab | VM, conteneurs, runbooks, playbooks, procedures, REX |

## 3. Ce qui existe deja dans le dossier

### Rendus principaux

| Fichier | Utilite |
|---|---|
| `Rendu_Simple_5PDF/00_PROJET_COMPLET_Daylight_CyberTrust.docx` | Rendu groupe editable |
| `Rendu_Simple_5PDF/01_Yvan_FOCSA_Architecte_Solution_pfSense.docx` | Rendu individuel Yvan |
| `Rendu_Simple_5PDF/02_Youssef_GUERNIOU_SIEM_Wazuh.docx` | Rendu individuel Youssef |
| `Rendu_Simple_5PDF/03_Kilyan_FELIX_Detection_Dashboards_Qualification.docx` | Rendu individuel Kilyan |
| `Rendu_Simple_5PDF/04_Mahamadou_DIACOUMBA_Playbooks_VM_REX.docx` | Rendu individuel Mahamadou |
| `Presentation_Daylight_CyberTrust.pptx` | Support PowerPoint |
| `SCRIPT_PRESENTATION_COMPLET_EQUIPE.md` | Script complet pour la video |

### Architecture et pfSense

| Fichier | Utilite |
|---|---|
| `Architecture_DayLight_CyberTrust/Daylight_CyberTrust_Architecture_Equipements_Zones.xlsx` | Excel complet zones, equipements, regles, flux, alertes |
| `Architecture_DayLight_CyberTrust/01_architecture_globale_daylight_cybertrust.drawio` | Schema global |
| `Architecture_DayLight_CyberTrust/02_architecture_pfsense_flux.drawio` | Schema pfSense et flux |
| `Architecture_DayLight_CyberTrust/03_architecture_soc_wazuh.drawio` | Schema chaine SOC Wazuh |
| `Annexes_Captures/CAP-12_architecture-solution.png` | Capture architecture |
| `Annexes_Captures/CAP-13_pfsense-regles-firewall.png` | Capture regles firewall |
| `Annexes_Captures/CAP-14_pfsense-syslog-wazuh.png` | Capture syslog pfSense vers Wazuh |
| `Dashboards_Offline/daylight_pfsense_firewall_review.html` | Revue pfSense presentable si la VM pfSense n'est pas live |

### Wazuh et logs

| Fichier | Utilite |
|---|---|
| `Youssef GUERNIOU/setup-siem-lab.ps1` | Script de preparation SIEM |
| `Youssef GUERNIOU/Documentation_SIEM_Youssef_GUERNIOU.pdf` | Preuves SIEM historiques |
| `config/wazuh/local_rules_daylight_pfsense.xml` | Regles Wazuh Daylight + pfSense |
| `config/wazuh/local_rules_pfsense_only.xml` | Regles pfSense seules utilisees en live |
| `Demo_Logs/pfsense.log` | Logs pfSense de demonstration |
| `Demo_Logs/daylight_app.log` | Logs application Daylight |
| `tools/send_demo_logs_to_syslog.py` | Script pour rejouer les logs vers Wazuh |

## 4. Difference importante : lab vs production

Il faut etre tres clair en presentation.

### Ce qui est vraiment present dans le lab

- Wazuh en Docker avec trois conteneurs :
  - `single-node-wazuh.manager-1`
  - `single-node-wazuh.indexer-1`
  - `single-node-wazuh.dashboard-1`
- Dashboard Wazuh accessible sur `https://localhost/`.
- Agent `serveur-01` actif.
- Logs pfSense rejouables en syslog UDP 514.
- Regles pfSense `110010` et `110020` visibles dans Security events.
- Zones reseau documentees : USERS, SERVERS, DMZ, MGMT, SOC.
- Regles pfSense documentees dans CSV et dashboard offline.
- Dashboards et captures pour le rendu.

### Ce qui est une cible production, pas forcement live

- vrais VLAN 802.1Q ;
- interfaces pfSense reelles dediees dans une infra client ;
- cluster Wazuh haute disponibilite ;
- sauvegardes automatisees ;
- politique de retention dimensionnee ;
- supervision complete des composants ;
- ticketing et automatisation SOC ;
- raccordement a de vrais equipements Daylight.

Phrase a dire :

> Dans le lab, nous presentons des zones logiques et des flux documentes. En production, ces zones seraient portees par des VLAN ou des interfaces dediees pfSense, avec des regles journalisees et une supervision complete.

## 5. Partie Yvan FOCSA - objectif

Ton objectif est de montrer que Cyber Trust ne fait pas seulement de la detection apres incident. Tu dois montrer que la securite est pensee **des l'architecture**.

Ta these principale :

> pfSense segmente et controle les flux. Wazuh detecte et qualifie les evenements. Les deux ensemble permettent de reduire la surface d'attaque et de rendre les incidents visibles pour le SOC.

Tu dois prouver trois choses :

1. L'architecture est segmentee en zones claires.
2. Les flux autorises et bloques sont concrets.
3. Les logs pfSense remontent dans Wazuh pour etre exploites par le SOC.

## 6. Architecture a presenter pour Yvan

### Zones

| Zone | Reseau lab | Role |
|---|---|---|
| WAN | NAT hyperviseur | Exposition externe / Internet |
| USERS | `10.10.10.0/24` | Postes utilisateurs Daylight |
| SERVERS | `10.10.20.0/24` | Serveurs internes |
| DMZ | `10.10.30.0/24` | Application Daylight exposee |
| MGMT | `10.10.40.0/24` | Administration |
| SOC | `10.10.50.0/24` | Wazuh et supervision |

### Equipements

| Equipement | Zone | Adresse | Role |
|---|---|---|---|
| `pfsense-fw-01` | multi-zone | `.1` dans chaque zone | Firewall et passerelle |
| `wazuh-manager` | SOC | `10.10.50.10` ou `https://localhost` en lab | SIEM |
| `poste-01` | USERS | `10.10.10.54` | Poste utilisateur |
| `serveur-01` | SERVERS | `10.10.20.20` ou Docker | Serveur Linux simule |
| `daylight-app-01` | DMZ | `10.10.30.20` | Application Daylight |
| `admin-01` | MGMT | `10.10.40.21` | Poste administrateur |

### Phrase simple

> L'architecture separe les usages : les utilisateurs, les serveurs, l'application exposee, l'administration et le SOC. pfSense controle les passages entre ces zones. L'objectif est qu'un poste utilisateur compromis ne puisse pas atteindre directement les serveurs, l'administration ou Wazuh.

## 7. Regles pfSense a expliquer

Tu n'as pas besoin de lire toutes les regles. Il faut presenter les plus importantes.

### Flux autorises

| Flux | Pourquoi il est autorise |
|---|---|
| USERS vers DAYLIGHT_APP en `443/tcp` | Les utilisateurs doivent acceder a l'application metier |
| WAN vers DAYLIGHT_APP en `443/tcp` via NAT | Publication HTTPS controlee de l'application |
| DMZ vers DAYLIGHT_DB en `5432/tcp` | L'application doit joindre sa base |
| SERVERS vers SOC_WAZUH en `1514/1515/tcp` | Agents Wazuh vers manager |
| SERVERS vers SOC_WAZUH en `514/udp` | Syslog vers Wazuh |
| MGMT vers pfSense en `443/tcp` | Administration firewall depuis zone admin |
| MGMT vers serveurs en `22/3389/5985/5986` | Administration systeme controlee |

### Flux bloques

| Flux | Pourquoi il est bloque |
|---|---|
| USERS vers MGMT | Un utilisateur ne doit pas administrer |
| USERS vers SERVERS | Limiter mouvement lateral |
| USERS vers SOC | Wazuh ne doit pas etre expose aux utilisateurs |
| DMZ vers MGMT | Une application exposee ne doit pas administrer |
| DMZ vers SERVERS sauf flux explicite | La DMZ doit etre strictement controlee |
| WAN vers any par defaut | Refus entrant par defaut |

### Phrase a dire

> La logique est du moindre privilege : on autorise les flux metier indispensables et on bloque le reste. Les blocages importants sont journalises pour etre visibles dans Wazuh.

## 8. pfSense vers Wazuh

Dans le projet, pfSense n'apparait pas dans la page Agents de Wazuh. C'est normal.

Explication :

> pfSense n'est pas un agent Wazuh. Il envoie ses logs en syslog vers Wazuh, sur le port UDP 514. On le voit donc dans Security events, pas dans Agents.

Regles a montrer :

| Regle | Signification |
|---|---|
| `110010` | Trafic entrant bloque sur WAN |
| `110020` | Tentative de mouvement inter-zones vers MGMT |
| `110050` | Flux sortant volumineux suspect |

Filtre Wazuh :

```text
rule.id:110010 OR rule.id:110020 OR pfsense-fw-01
```

Commande pour rejouer les logs pfSense :

```powershell
python .\tools\send_demo_logs_to_syslog.py --host 127.0.0.1 --port 514 --protocol udp --file pfsense.log
```

Ensuite attendre 5 a 10 secondes et chercher `110010` ou `110020` dans Wazuh.

## 9. Ce que Yvan doit faire a la main

### Avant la video

- Ouvrir `SCRIPT_PRESENTATION_COMPLET_EQUIPE.md`.
- Ouvrir `CAP-12_architecture-solution.png`.
- Ouvrir l'Excel architecture.
- Ouvrir `Dashboards_Offline/daylight_pfsense_firewall_review.html`.
- Ouvrir Wazuh sur `https://localhost/`.
- Preparer le filtre pfSense : `rule.id:110010 OR rule.id:110020 OR pfsense-fw-01`.
- Rejouer les logs pfSense si besoin.
- Verifier que les alertes `110010` et `110020` apparaissent.

### Pendant la video

Ordre de ta partie :

1. Montrer schema architecture.
2. Expliquer les zones.
3. Montrer pfSense comme point central.
4. Montrer les flux autorises et bloques.
5. Expliquer que pfSense envoie ses logs vers Wazuh.
6. Montrer dans Wazuh les alertes `110010` et `110020`.
7. Dire clairement que les VLAN sont une cible production, pas obligatoirement montes dans le lab.

### Apres la video

- Copier le lien YouTube non repertorie dans le fichier lien video si necessaire.
- Relancer le check video si vous finalisez le depot.
- Mettre a jour les captures si vous en avez repris de meilleures.

## 10. Script pret a lire pour Yvan

### Partie architecture

> Ma partie concerne l'architecture de la solution. L'objectif est de proposer une architecture claire, securisee et demonstrable pour Daylight.
>
> Le principe principal est la segmentation. Dans le lab, nous avons des zones logiques : USERS pour les postes utilisateurs, SERVERS pour les serveurs internes, DMZ pour l'application Daylight, MGMT pour l'administration, SOC pour Wazuh et WAN pour l'acces externe.
>
> pfSense est place comme firewall central. Il controle les flux entre les zones. Cela permet d'eviter qu'un poste utilisateur compromis puisse atteindre directement les serveurs, l'administration ou le SOC.

### Partie regles pfSense

> La logique appliquee est le moindre privilege. On autorise uniquement les flux necessaires.
>
> Par exemple, les utilisateurs peuvent acceder a l'application Daylight en HTTPS sur le port 443. En revanche, les utilisateurs ne peuvent pas acceder directement aux serveurs internes, a la zone d'administration ou a Wazuh.
>
> La DMZ peut joindre la base de donnees sur le port 5432, mais elle ne peut pas administrer le reseau interne. Les serveurs peuvent envoyer leurs logs vers Wazuh sur les ports 1514, 1515 et 514.

### Partie Wazuh / pfSense

> Les regles sensibles sont journalisees. pfSense envoie ses logs vers Wazuh en syslog UDP sur le port 514.
>
> C'est important : pfSense n'apparait pas dans la page Agents, car ce n'est pas un agent Wazuh. Il apparait dans les evenements de securite via ses logs.
>
> Ici, la regle `110010` correspond au trafic entrant bloque sur le WAN. La regle `110020` correspond a une tentative de mouvement inter-zones vers MGMT.

### Partie limites / production

> Le lab prouve la faisabilite. En production, les zones logiques seraient portees par des VLAN ou par des interfaces dediees pfSense. On ajouterait aussi une architecture Wazuh plus robuste, avec composants separes, sauvegardes, retention et supervision.
>
> Le projet ne pretend donc pas etre une production complete, mais il montre une trajectoire claire : segmentation, filtrage, journalisation, detection et exploitation SOC.

## 11. Ce qu'il faut dire si le jury pose des questions

### Pourquoi pfSense ?

> pfSense est concret, open-source et suffisant pour demontrer la segmentation, le NAT, les regles firewall, la journalisation et l'envoi syslog vers Wazuh.

### Pourquoi pas seulement Wazuh ?

> Wazuh detecte, mais il ne remplace pas le controle reseau. pfSense reduit la surface d'attaque en bloquant certains flux avant meme qu'ils deviennent un incident.

### Pourquoi pfSense n'est pas dans Agents ?

> Parce que pfSense n'a pas d'agent Wazuh dans notre lab. Il envoie ses logs en syslog vers Wazuh. On le voit dans Security events avec `pfsense-fw-01`, `110010` et `110020`.

### Est-ce que les VLAN sont vraiment deployes ?

> Dans le lab, non : nous avons surtout une segmentation logique et des regles documentees. En production, ces zones seraient implementees par des VLAN ou par des interfaces dediees pfSense.

### Est-ce que c'est de la production ?

> Non. C'est un demonstrateur. Il prouve les choix techniques et les flux. La production demanderait du durcissement, de la haute disponibilite, une politique de sauvegarde, de retention et une supervision des composants.

## 12. Commandes utiles

### Tester Wazuh

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\preflight_demo.ps1 -WriteReport
```

### Relancer le setup SIEM

```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File ".\Youssef GUERNIOU\setup-siem-lab.ps1"
```

### Rejouer les logs pfSense

```powershell
python .\tools\send_demo_logs_to_syslog.py --host 127.0.0.1 --port 514 --protocol udp --file pfsense.log
```

### Filtre SSH Wazuh

```text
agent.name: serveur-01 AND (rule.id:5710 OR rule.id:5503 OR rule.id:5551 OR rule.id:5763 OR rule.id:5712)
```

### Filtre pfSense Wazuh

```text
rule.id:110010 OR rule.id:110020 OR pfsense-fw-01
```

## 13. Checklist express pour Yvan

Avant d'enregistrer :

- [ ] Wazuh ouvert sur `https://localhost/`
- [ ] `serveur-01` visible dans Agents
- [ ] pfSense visible dans Security events via `110010` ou `110020`
- [ ] `CAP-12_architecture-solution.png` ouvert
- [ ] Excel architecture ouvert
- [ ] Revue pfSense offline ouverte
- [ ] Script equipe ouvert
- [ ] Phrase "lab vs production" preparee

Pendant ta partie :

- [ ] Dire que ce sont des zones logiques dans le lab
- [ ] Dire que les VLAN sont une cible production
- [ ] Expliquer USERS / SERVERS / DMZ / MGMT / SOC
- [ ] Expliquer les flux autorises
- [ ] Expliquer les flux bloques
- [ ] Dire que pfSense envoie ses logs a Wazuh
- [ ] Montrer `110010` et `110020` si possible

## 14. Ce qu'il ne faut pas dire

Ne pas dire :

- "On a deploye des VLAN reels" si ce n'est pas monte dans l'hyperviseur.
- "pfSense est un agent Wazuh".
- "Tout est en production".
- "Wazuh est en haute disponibilite".
- "Les sauvegardes et la retention sont deja automatisees".

Dire plutot :

- "Le lab modelise les zones et les flux."
- "pfSense remonte en syslog."
- "La production ajouterait VLAN ou interfaces dediees."
- "La production ajouterait sauvegarde, retention et supervision."

## 15. Plan manuel si tu veux refaire pfSense vraiment

Si tu veux monter pfSense a la main dans VirtualBox, VMware ou Hyper-V :

1. Creer une VM `pfsense-fw-01`.
2. Ajouter 6 cartes reseau :
   - WAN : NAT
   - USERS : reseau interne `DAYLIGHT_USERS`
   - SERVERS : reseau interne `DAYLIGHT_SERVERS`
   - DMZ : reseau interne `DAYLIGHT_DMZ`
   - MGMT : reseau interne `DAYLIGHT_MGMT`
   - SOC : reseau interne `DAYLIGHT_SOC`
3. Installer pfSense.
4. Assigner les interfaces dans l'ordre.
5. Configurer les IP :
   - USERS : `10.10.10.1/24`
   - SERVERS : `10.10.20.1/24`
   - DMZ : `10.10.30.1/24`
   - MGMT : `10.10.40.1/24`
   - SOC : `10.10.50.1/24`
6. Creer les aliases depuis `config/pfsense/pfsense_aliases.csv`.
7. Creer les regles depuis `config/pfsense/pfsense_firewall_rules.csv`.
8. Creer le NAT depuis `config/pfsense/pfsense_nat_port_forward.csv`.
9. Activer remote logging vers `10.10.50.10:514 UDP`.
10. Tester les flux :
    - USERS vers app 443 : autorise.
    - USERS vers MGMT 443 : bloque.
    - USERS vers SERVERS 22 : bloque.
    - pfSense logs vers Wazuh : visibles.

## 16. Plan de presentation minimal si tu manques de temps

Si tu n'as que 2 minutes :

> J'ai defini l'architecture reseau de Daylight autour de pfSense et de Wazuh. Le lab separe les zones USERS, SERVERS, DMZ, MGMT et SOC. pfSense controle les flux entre ces zones : les utilisateurs peuvent acceder a l'application Daylight, mais ils ne peuvent pas aller vers les serveurs, l'administration ou le SOC. Les flux sensibles sont journalises et envoyes a Wazuh en syslog. Dans Wazuh, on retrouve les alertes pfSense avec `110010` pour un trafic WAN bloque et `110020` pour une tentative vers MGMT. En production, ces zones seraient portees par des VLAN ou des interfaces dediees pfSense, avec sauvegardes, retention et supervision renforcees.

## 17. Fichiers a ouvrir pour ta partie

Ouvre dans cet ordre :

1. `Annexes_Captures/CAP-12_architecture-solution.png`
2. `Architecture_DayLight_CyberTrust/Daylight_CyberTrust_Architecture_Equipements_Zones.xlsx`
3. `Dashboards_Offline/daylight_pfsense_firewall_review.html`
4. `config/pfsense/pfsense_firewall_rules.csv`
5. Wazuh `https://localhost/`
6. `SCRIPT_PRESENTATION_COMPLET_EQUIPE.md`

## 18. Etat final a retenir

Le projet est presentable.

Le plus important pour Yvan :

- architecture claire ;
- zones reseau expliquees ;
- pfSense justifie ;
- flux autorises/bloques concrets ;
- logs pfSense envoyes a Wazuh ;
- difference lab/production assumee ;
- discours propre, sans promettre des choses non deployees.
