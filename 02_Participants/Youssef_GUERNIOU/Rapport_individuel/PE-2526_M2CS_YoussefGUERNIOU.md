# Rendu individuel developpe - Youssef GUERNIOU

## Identification

| Champ | Valeur |
|---|---|
| Projet | Projet 4 - SOC externalise Daylight |
| Client fictif | Daylight |
| Prestataire | Cyber Trust |
| Membre | Youssef GUERNIOU |
| Role principal | Ingenieur SIEM / Wazuh |
| Perimetre defendu | Deploiement Wazuh, agents, collecte, regles de detection, RBAC, dashboards, preuves SIEM |

## Synthese personnelle

Mon role est de construire le coeur technique du SOC : la plateforme SIEM. Le projet doit montrer que Cyber Trust ne se contente pas de decrire une supervision, mais sait mettre en place une chaine de collecte, de detection et de restitution des alertes.

J'ai donc travaille sur :

- le deploiement Wazuh en environnement de demonstration ;
- le raccordement de sources de logs ;
- la creation ou validation de regles adaptees au contexte Daylight ;
- la preuve des alertes dans Wazuh Dashboard ;
- les dashboards techniques et executifs ;
- la logique RBAC pour separer les droits ;
- un script de lab pour rendre la demonstration reproductible.

La partie SIEM est centrale : sans collecte fiable et sans alertes visibles, les playbooks, dashboards et procedures ne peuvent pas etre defendus.

## Objectifs SIEM

Le SIEM doit repondre a quatre objectifs operationnels :

1. centraliser les evenements provenant de plusieurs sources ;
2. detecter des comportements suspects pertinents pour Daylight ;
3. restituer des alertes lisibles dans Wazuh Dashboard ;
4. fournir des preuves utilisables par les autres membres de l'equipe.

Les sources prioritaires sont :

| Source | Exemple | Interet SOC |
|---|---|---|
| Endpoint | `poste-01` | Activite poste, SCA, hygiene, evenements endpoint |
| Serveur | `serveur-01` | Authentification SSH, brute force, logs systeme |
| Application Daylight | Logs metier | Dossiers patients, authentification applicative, privileges |
| Firewall pfSense | filterlog/syslog | Blocages WAN, mouvement lateral, VPN, administration |

## Architecture Wazuh de demonstration

La solution de demonstration repose sur Wazuh en mode single-node. Ce choix est adapte a un projet de soutenance parce qu'il permet de regrouper manager, indexer et dashboard dans un lab plus simple a lancer.

Les composants attendus sont :

- Wazuh Manager : reception et analyse des evenements ;
- Wazuh Indexer : stockage et recherche ;
- Wazuh Dashboard : interface web pour la consultation ;
- agents Wazuh : endpoints et serveurs ;
- syslog : integration pfSense et logs reseau.

![Connexion Wazuh Dashboard](../Annexes_Captures/CAP-01_wazuh-dashboard-login.png)

## Script de lab

Le fichier principal rattache a mon perimetre est :

`Youssef GUERNIOU/setup-siem-lab.ps1`

Son objectif est de reduire les manipulations manuelles. Il sert a preparer le lab, creer ou configurer le serveur simule, activer des services, raccorder des logs et faciliter la reproduction de la demonstration.

Les actions attendues autour du script :

| Etape | Action | Resultat attendu |
|---|---|---|
| 1 | Verifier Docker et Wazuh | Plateforme accessible |
| 2 | Demarrer `serveur-01` | Conteneur en fonctionnement |
| 3 | Activer SSH et rsyslog | Logs systeme produits |
| 4 | Ajouter le suivi `auth.log` | Brute force SSH detectable |
| 5 | Generer des evenements Daylight | Regles `100xxx` testables |
| 6 | Valider agents et dashboards | Preuves visibles |

![Script setup SIEM](../Annexes_Captures/CAP-15_script-setup-siem-lab.png)

## Collecte des agents

La page agents doit prouver que Wazuh recoit des sources differentes. Dans le demonstrateur, les sources importantes sont :

- `poste-01` pour l'endpoint ;
- `serveur-01` pour le serveur Linux ;
- logs Daylight pour les evenements metier ;
- logs pfSense pour la partie reseau.

![Agents poste et serveur](../Annexes_Captures/CAP-02_agents-poste01-serveur01.png)

Pour la soutenance, cette capture prouve que la supervision n'est pas mono-source. Elle soutient directement l'exigence de centralisation.

## Detection brute force SSH

La detection brute force SSH repose sur les logs d'authentification du serveur. L'alerte Wazuh native importante est :

| Regle | Scenario | Severite | Action SOC |
|---|---|---:|---|
| `5712` | Plusieurs echecs SSH | Haute | Verifier IP source, utilisateur cible, succes apres echecs |

Le test consiste a generer plusieurs echecs d'authentification puis a verifier l'apparition de l'alerte.

Commandes de verification cote lab :

```powershell
docker start serveur-01
docker exec -it serveur-01 bash
service ssh status
tail -f /var/log/auth.log
```

Point de controle Wazuh :

- l'alerte doit etre visible dans Security events ;
- `agent.name` doit pointer vers `serveur-01` ;
- la regle `5712` doit etre identifiable ;
- l'heure doit correspondre au test.

![Alerte brute force SSH](../Annexes_Captures/CAP-03_alerte-5712-brute-force-ssh.png)

## Regles Daylight metier

Pour adapter Wazuh au client, le projet contient des regles metier dans :

`config/wazuh/local_rules_daylight_pfsense.xml`

Les regles Daylight couvrent les incidents les plus pertinents pour un reseau d'audioprothesistes.

| Regle | Niveau | Scenario | Raison metier |
|---|---:|---|---|
| `100110` | 10 | Brute force applicatif Daylight | Protection de l'interface metier |
| `100120` | 12 | Acces anormal dossier patient | Donnees sensibles et risque RGPD |
| `100130` | 12 | Modification groupe privilegie | Elevation de privileges |
| `100140` | 8 | Support USB non autorise | Risque endpoint et fuite de donnees |
| `100150` | 9 | Phishing signale | Risque messagerie |

Exemple de logique de detection :

```xml
<rule id="100120" level="12">
  <decoded_as>syslog</decoded_as>
  <regex>DAYLIGHT_APP.*event=patient_record_access.*risk=high</regex>
  <description>Daylight - acces anormal a un dossier patient</description>
  <group>daylight_app,gdpr,patient_data,</group>
</rule>
```

Cette regle est critique parce qu'elle relie la technique au metier : un acces suspect a un dossier patient doit etre traite plus vite qu'un evenement d'hygiene standard.

![Alertes metier Daylight](../Annexes_Captures/CAP-05_daylight-alertes-metier.png)

## Regles pfSense dans Wazuh

La contribution architecture de Yvan produit des flux firewall. Ma partie SIEM doit permettre leur detection dans Wazuh.

Regles importantes :

| Regle | Scenario | Niveau | Utilite SOC |
|---|---|---:|---|
| `110010` | Blocage WAN | 8 | Suivi scans et tentatives externes |
| `110020` | Mouvement lateral inter-VLAN | 10 | Priorite reseau interne |
| `110030` | Connexion admin pfSense | 6 | Tracabilite administration |
| `110040` | Connexion VPN admin | 7 | Controle acces distants |
| `110050` | Flux sortant suspect | 11 | Suspicion exfiltration |

![Alertes pfSense dans Wazuh](../Annexes_Captures/CAP-19_wazuh-pfsense-alertes.png)

## Dashboards Wazuh

Deux familles de dashboards sont attendues.

Le dashboard technique sert aux analystes :

- alertes par severite ;
- top regles ;
- alertes par source ;
- timeline des evenements critiques ;
- evenements Daylight ;
- evenements pfSense.

Le dashboard executif sert a Daylight et a la supervision :

- total alertes ;
- alertes critiques ;
- alertes donnees patients ;
- tentatives reseau bloquees ;
- tendance sur la periode.

![Dashboard technique](../Annexes_Captures/CAP-21_dashboard-technique-requetes.png)

![Dashboard executif](../Annexes_Captures/CAP-22_dashboard-executif-daylight.png)

Les requetes et widgets sont formalises dans :

`config/wazuh/daylight_dashboard_queries.csv`

Cela permet de montrer que les dashboards ne sont pas seulement visuels : ils reposent sur des requetes precises.

## RBAC et separation des droits

Le SOC doit separer les droits selon les profils. En demonstration, trois profils sont defendus :

| Profil | Droits attendus | Justification |
|---|---|---|
| Admin | Configuration, regles, agents | Maintenance technique |
| Analyste | Lecture alertes, investigation | Qualification sans modification critique |
| Supervision | Vue dashboard, reporting | Suivi client ou management |

L'objectif est d'eviter qu'un utilisateur de supervision puisse modifier la configuration du SIEM. Le RBAC prouve que la solution prend en compte la securite d'exploitation.

![RBAC analyste lecture seule](../Annexes_Captures/CAP-09_rbac-analyste-lecture-seule.png)

## Matrice de qualification rattachee au SIEM

Les alertes ne doivent pas rester de simples lignes dans Wazuh. Elles sont reliees a une matrice de qualification :

`config/wazuh/daylight_alert_qualification_matrix.csv`

Extrait :

| Regle | Scenario | SLA triage | Escalade |
|---|---|---|---|
| `5712` | Brute force SSH | 30 min | SOC + exploitation |
| `100120` | Acces dossier patient | 15 min | SOC + referent Daylight + DPO |
| `100130` | Privilege | 15 min | SOC + admin AD + management |
| `110020` | Inter-VLAN | 15 min | SOC + reseau |

Ce lien entre detection et qualification est important : Wazuh detecte, mais l'equipe SOC decide et documente.

## Mode de test des alertes

La verification d'une alerte doit suivre un chemin simple :

1. generer ou rejouer un log ;
2. verifier que le log arrive dans Wazuh ;
3. verifier que la regle attendue se declenche ;
4. ouvrir le detail de l'alerte ;
5. comparer avec la matrice de qualification ;
6. capturer la preuve ;
7. rattacher au playbook.

Exemple pour les logs de demonstration :

```powershell
python .\tools\generate_demo_logs.py
python .\tools\send_demo_logs_to_syslog.py --dry-run
```

Le mode `--dry-run` permet de verifier les evenements sans envoyer de flux destructif.

![Rejeu logs demo](../Annexes_Captures/CAP-20_wazuh-rejeu-logs-demo.png)

## Preuves rattachees a mon perimetre

| Preuve | Usage dans la soutenance |
|---|---|
| `CAP-01_wazuh-dashboard-login.png` | Prouver l'acces Wazuh Dashboard |
| `CAP-02_agents-poste01-serveur01.png` | Prouver la collecte multi-source |
| `CAP-03_alerte-5712-brute-force-ssh.png` | Prouver la detection SSH |
| `CAP-04_source-endpoint-poste01-sca.png` | Prouver l'endpoint/SCA |
| `CAP-05_daylight-alertes-metier.png` | Prouver les regles Daylight |
| `CAP-09_rbac-analyste-lecture-seule.png` | Prouver la separation des droits |
| `CAP-19_wazuh-pfsense-alertes.png` | Prouver l'integration firewall |
| `CAP-21_dashboard-technique-requetes.png` | Prouver les requetes dashboard |
| `CAP-22_dashboard-executif-daylight.png` | Prouver la restitution client |

## Documents et fichiers livrables

| Fichier | Role |
|---|---|
| `Youssef GUERNIOU/Documentation_SIEM_Youssef_GUERNIOU.pdf` | Documentation SIEM initiale et preuves sources |
| `Youssef GUERNIOU/setup-siem-lab.ps1` | Automatisation de lab |
| `config/wazuh/local_rules_daylight_pfsense.xml` | Regles Wazuh custom |
| `config/wazuh/daylight_dashboard_queries.csv` | Definition des dashboards |
| `config/wazuh/daylight_alert_qualification_matrix.csv` | Lien alertes/SLA/actions |
| `tools/extract_youssef_wazuh_proofs.py` | Extraction des preuves depuis le PDF SIEM |
| `youssef-wazuh-proof-extraction-report.txt` | Rapport d'extraction des preuves |

## Troubleshooting SIEM

| Probleme | Diagnostic | Correction |
|---|---|---|
| Dashboard inaccessible | Verifier Docker et ports | Relancer Wazuh / Docker |
| Agent absent | Verifier service agent | Reenregistrer l'agent |
| Pas d'alerte `5712` | Verifier `/var/log/auth.log` | Relancer SSH/rsyslog et refaire test |
| Regles `100xxx` absentes | Verifier `local_rules.xml` | Copier le XML puis redemarrer Wazuh Manager |
| Logs pfSense absents | Verifier UDP 514 et remote syslog | Corriger pfSense et firewall |
| RBAC non visible | Verifier profil connecte | Utiliser compte analyste/supervision |

## Trajectoire production

Pour passer en production Daylight, la plateforme SIEM doit evoluer :

- separer manager, indexer et dashboard ;
- activer TLS et gestion de certificats pour les agents ;
- definir une retention par type de log ;
- superviser la sante Wazuh ;
- sauvegarder regles, dashboards et index critiques ;
- connecter la qualification a un outil ITSM ;
- automatiser le deploiement agent par site ;
- mettre en place un processus de changement pour les regles.

Cette trajectoire est importante car le lab prouve le fonctionnement, mais la production exige de la robustesse.

## Ce que je dois montrer pendant la video

Mon passage doit prouver la chaine SIEM :

1. ouvrir Wazuh Dashboard ;
2. montrer les agents `poste-01` et `serveur-01` ;
3. montrer l'alerte brute force SSH `5712` ;
4. montrer les alertes Daylight `100xxx` ;
5. expliquer une regle custom ;
6. montrer un dashboard technique ;
7. montrer un profil RBAC ou expliquer la separation des droits.

Texte court possible :

> Je suis Youssef GUERNIOU, responsable SIEM Wazuh. Ma partie prouve que Cyber Trust sait collecter plusieurs sources, detecter des incidents concrets et restituer les alertes dans des dashboards exploitables.

## Limites assumees

La solution de lab n'est pas une production complete :

- single-node Wazuh ;
- volumetrie limitee ;
- certains logs sont simules ;
- pas de ticketing connecte ;
- pas de haute disponibilite ;
- tests realises sur un environnement local.

Ces limites sont acceptees dans le cadre du MVP, mais elles sont documentees pour ne pas sur-vendre la solution.

## Apport personnel

Ce projet m'a permis de travailler sur une chaine SOC complete : installation, collecte, detection, visualisation et preuve. J'ai compris que la difficulte n'est pas seulement de declencher une alerte, mais de produire une alerte utile, qualifiable et comprehensible par les autres membres.

La qualite d'un SIEM repose sur trois points :

- les sources doivent etre fiables ;
- les regles doivent etre adaptees au contexte ;
- les dashboards doivent aider a prendre une decision.

## Conclusion individuelle

Ma contribution donne au projet son socle technique SIEM. Les alertes Wazuh, les agents, les regles custom Daylight, les evenements pfSense, les dashboards et le RBAC prouvent que la solution Cyber Trust est demonstrable.

Le resultat attendu pour le jury est clair : on peut voir les sources, voir les alertes, comprendre leur criticite et les relier aux procedures de reponse.
