# Script complet de presentation video - Daylight / Cyber Trust

## Format recommande

Duree cible : 15 a 17 minutes.

Ordre conseille :

| Temps | Intervenant | Partie |
|---:|---|---|
| 00:00 - 01:30 | Kilyan FELIX | Introduction client, contexte, objectifs |
| 01:30 - 04:00 | Yvan FOCSA | Architecture, segmentation, pfSense |
| 04:00 - 08:30 | Youssef GUERNIOU | Wazuh, collecte, alertes, RBAC |
| 08:30 - 11:30 | Kilyan FELIX | Dashboards, qualification, SLA |
| 11:30 - 14:30 | Mahamadou DIACOUMBA | Lab, VM, runbooks, playbooks, REX |
| 14:30 - 17:00 | Yvan + equipe | Industrialisation, limites, conclusion |

## Avant de lancer l'enregistrement

Ouvrir les onglets ou fichiers suivants :

1. `Presentation_Daylight_CyberTrust.pptx`
2. `Annexes_Captures/CAP-12_architecture-solution.png`
3. `Architecture_DayLight_CyberTrust/Daylight_CyberTrust_Architecture_Equipements_Zones.xlsx`
4. `Dashboards_Offline/daylight_pfsense_firewall_review.html`
5. Wazuh Dashboard : `https://localhost/`
6. Wazuh Security events avec filtre SSH :
   `agent.name: serveur-01 AND (rule.id:5710 OR rule.id:5503 OR rule.id:5551 OR rule.id:5763 OR rule.id:5712)`
7. Wazuh Security events avec filtre pfSense :
   `rule.id:110010 OR rule.id:110020 OR pfsense-fw-01`
8. `Dashboards_Offline/daylight_soc_dashboard.html`
9. `03_PLAYBOOKS_PROCEDURES_REX.md`
10. `22_EXPLOITATION_VM_RUNBOOK_REX.md`

## 1. Introduction - Kilyan FELIX

Ecran a montrer : slide d'introduction ou presentation groupe.

Texte :

> Bonjour, nous sommes l'equipe Cyber Trust. Nous presentons notre projet de SOC externalise pour Daylight, un client fictif qui represente un reseau de centres d'audioprothesistes.
>
> Le besoin de Daylight est de mieux superviser son systeme d'information, centraliser les evenements de securite, detecter les incidents importants et disposer de tableaux de bord comprehensibles pour les analystes comme pour la direction.
>
> Notre solution combine une architecture segmentee, un firewall pfSense, un SIEM Wazuh, des regles de detection, des dashboards, du RBAC et des procedures de reponse aux incidents.
>
> Dans l'equipe, Yvan FOCSA est responsable de l'architecture et de pfSense. Youssef GUERNIOU est responsable du perimetre SIEM Wazuh. Je gere la partie detection, qualification, alertes et dashboards. Mahamadou DIACOUMBA gere le lab, les VM, les playbooks, les procedures et les retours d'experience.

Transition :

> Je laisse maintenant Yvan presenter l'architecture de la solution.

## 2. Architecture et pfSense - Yvan FOCSA

Ecran a montrer : `CAP-12_architecture-solution.png`, puis Excel architecture ou revue pfSense.

Texte :

> Ma partie concerne l'architecture de la solution. L'objectif est de proposer une architecture claire, securisee et demonstrable pour Daylight.
>
> Le principe principal est la segmentation reseau. On separe les utilisateurs, les serveurs internes, la DMZ, l'administration et la zone SOC. Cette separation limite les deplacements lateraux si un poste utilisateur est compromis.
>
> Les zones sont les suivantes : USERS pour les postes utilisateurs, SERVERS pour les serveurs internes, DMZ pour l'application Daylight exposee, MGMT pour l'administration, SOC pour Wazuh et la supervision, et WAN pour l'acces externe.
>
> pfSense est place comme firewall central et passerelle de chaque zone. Il applique une logique de securite simple : on autorise uniquement les flux necessaires et on bloque le reste.

Montrer les regles pfSense.

> Par exemple, les utilisateurs peuvent acceder a l'application Daylight en HTTPS sur le port 443. En revanche, ils ne peuvent pas acceder directement aux serveurs internes, a la zone d'administration ou au SOC.
>
> La DMZ peut communiquer avec la base de donnees uniquement sur le port 5432, mais elle ne peut pas administrer le reseau interne. Les serveurs peuvent envoyer leurs logs vers Wazuh sur les ports 1514, 1515 et 514. La zone MGMT est reservee aux administrateurs.
>
> pfSense ne sert donc pas seulement a router le trafic. Il reduit la surface d'attaque, journalise les flux sensibles et envoie ses logs vers Wazuh en syslog UDP sur le port 514.

Phrase importante :

> Dans Wazuh, pfSense n'apparait pas comme agent, car il n'a pas d'agent Wazuh. Il apparait dans les evenements de securite via ses logs syslog, par exemple avec les regles 110010 et 110020.

Transition :

> Maintenant que l'architecture bloque et journalise les flux sensibles, Youssef va presenter la supervision Wazuh.

## 3. SIEM Wazuh - Youssef GUERNIOU

Ecran a montrer : Wazuh `https://localhost/`, puis Agents, puis Security events.

Texte :

> Je presente la partie SIEM. Nous avons choisi Wazuh parce que c'est une solution open-source qui permet de collecter des agents, des logs syslog, des logs applicatifs, de creer des regles et de restituer les alertes dans des dashboards.
>
> Le lab est deploye en mode single-node Docker avec Wazuh Manager, Wazuh Indexer et Wazuh Dashboard. Cela permet d'avoir un environnement reproductible pour la demonstration.
>
> Le perimetre SIEM documente trois sources principales : l'endpoint `poste-01`, le serveur Linux simule `serveur-01`, et l'application metier Daylight. Dans le live actuel, on voit surtout `serveur-01` comme agent actif. Les preuves `poste-01` et les dashboards historiques sont dans le dossier SIEM de reference.

Montrer la page Agents.

> Ici, on voit `serveur-01` actif. C'est normal que pfSense ne soit pas dans cette liste, car pfSense remonte en syslog et pas comme agent.

Montrer le filtre SSH :
`agent.name: serveur-01 AND (rule.id:5710 OR rule.id:5503 OR rule.id:5551 OR rule.id:5763 OR rule.id:5712)`

> Sur `serveur-01`, nous avons installe SSH et rsyslog, puis ajoute le suivi de `/var/log/auth.log`. Ensuite, le script de preparation simule des echecs de connexion SSH.
>
> Wazuh detecte les tentatives avec plusieurs regles : `5710` pour un utilisateur inexistant, `5503` pour un echec PAM, et `5551` ou `5763` pour la correlation brute force. La documentation SIEM contient aussi la preuve historique `5712`.

Montrer le filtre pfSense :
`rule.id:110010 OR rule.id:110020 OR pfsense-fw-01`

> Pour pfSense, les logs arrivent en syslog. La regle `110010` correspond au trafic entrant bloque sur le WAN, et `110020` correspond a une tentative de mouvement inter-zones vers une zone sensible comme MGMT.

Montrer ou expliquer RBAC.

> Nous avons aussi mis en place du RBAC avec trois profils : admin pour l'acces complet, analyste pour la consultation et supervision pour les vues de pilotage. Cela permet de separer les droits et d'eviter qu'un compte de consultation puisse modifier la configuration du SIEM.

Transition :

> Je laisse Kilyan presenter maintenant la qualification des alertes et les dashboards.

## 4. Detection, qualification et dashboards - Kilyan FELIX

Ecran a montrer : dashboard technique, dashboard executif ou dashboard offline.

Texte :

> Ma partie consiste a transformer les alertes en information exploitable par un SOC. Une alerte seule ne suffit pas : il faut la qualifier, lui donner une priorite, un SLA de traitement et une procedure d'escalade.
>
> Nous avons donc construit une matrice de qualification. Par exemple, l'acces anormal a un dossier patient avec la regle `100120` est critique, car il touche des donnees sensibles et peut avoir un impact RGPD. Une brute force SSH est haute, car elle peut annoncer une tentative de compromission. Une tentative inter-zones pfSense `110020` est critique si elle vise MGMT ou SERVERS.

Montrer dashboard technique.

> Le dashboard technique est destine aux analystes SOC. Il affiche les alertes par severite, les sources, les regles les plus declenchees et les evenements importants. Il aide l'analyste a prioriser rapidement.

Montrer dashboard executif.

> Le dashboard executif est destine a Daylight. Il ne rentre pas dans tous les details techniques, mais montre les volumes d'alertes, les alertes critiques et les tendances. Cela permet au client de piloter le service de supervision.
>
> Cette separation entre dashboard technique et dashboard executif repond a deux besoins differents : investiguer cote SOC et rendre compte cote client.

Transition :

> Une fois les alertes qualifiees, il faut savoir quoi faire. Mahamadou va presenter la partie exploitation, playbooks et retour d'experience.

## 5. Exploitation, playbooks et REX - Mahamadou DIACOUMBA

Ecran a montrer : runbook lab puis playbooks.

Texte :

> Ma partie concerne l'exploitation du lab et les procedures operationnelles. L'objectif est que la demonstration soit relancable, mais aussi que les incidents aient une reponse claire.
>
> Pour le lab, nous avons documente les composants, les conteneurs, les commandes de redemarrage et le preflight. Par exemple, apres extinction du PC, il faut verifier Docker, relancer Wazuh si necessaire, demarrer `serveur-01`, puis verifier SSH, rsyslog et l'agent Wazuh.

Montrer commande ou runbook :

> Les commandes importantes sont `docker start serveur-01`, puis dans le conteneur `rsyslogd`, `service ssh start` et `/var/ossec/bin/wazuh-control start` si besoin.
>
> Nous avons aussi des playbooks. Pour une brute force SSH, l'analyste verifie la source, l'utilisateur vise, le nombre d'echecs et s'il y a eu une connexion reussie ensuite. Si c'est confirme, on bloque la source, on verifie le compte et on conserve les preuves.
>
> Pour un acces anormal a un dossier patient, on verifie le role de l'utilisateur, le dossier concerne, le site Daylight et l'heure. Comme ce sont des donnees sensibles, on escalade au referent Daylight et au DPO si necessaire.
>
> Le REX permet ensuite de documenter ce qui s'est passe, ce qui a ete bien gere et ce qu'il faut ameliorer.

Transition :

> Je repasse la parole a Yvan pour la partie industrialisation et conclusion.

## 6. Industrialisation, limites et conclusion - Yvan FOCSA puis equipe

Ecran a montrer : rapport groupe, architecture cible, checklist finale.

Texte Yvan :

> Le demonstrateur montre que la solution fonctionne sur un lab. Dans le lab actuel, Wazuh tourne en single-node Docker avec trois conteneurs : Manager, Indexer et Dashboard. Ce n'est pas encore une architecture de production complete.
>
> En production, nous ne garderions pas ce format simplifie. Nous separerions les composants Wazuh, avec un manager, un indexer, un dashboard, des sauvegardes, une retention adaptee et une supervision des composants.
>
> Cote reseau, le lab presente surtout des zones logiques : USERS, SERVERS, DMZ, MGMT et SOC. En production, ces zones seraient portees par des VLAN ou par des interfaces dediees pfSense, avec des regles journalisees, du NAT controle, une administration isolee et des flux SOC explicites.
>
> La limite principale du projet est que tout n'est pas un environnement de production complet. En revanche, les elements essentiels sont presents : architecture, firewall, collecte, detection, dashboards, RBAC, playbooks et preuves.

Texte equipe ou Kilyan :

> Pour conclure, Cyber Trust propose a Daylight une solution de SOC externalise qui combine prevention et detection. Dans le lab, pfSense est modelise par des zones, des regles et des logs syslog ; dans la cible, il porterait la segmentation reseau reelle. Wazuh collecte et detecte les evenements. Les dashboards permettent de suivre l'activite. Les playbooks permettent de reagir.
>
> Le projet est donc demonstrable, documente et extensible vers une version industrialisee pour plusieurs sites Daylight.

Derniere phrase :

> Merci pour votre attention. Nous sommes prets a repondre aux questions sur l'architecture, les choix techniques, les detections et l'exploitation du SOC.

## Phrases de secours si quelque chose ne marche pas en live

Si `poste-01` n'apparait pas :

> Dans le live actuel, `poste-01` n'est pas reconnecte, mais la preuve endpoint est integree dans la documentation SIEM de Youssef. Le live montre `serveur-01`, pfSense en syslog et les alertes rejouees.

Si pfSense n'apparait pas dans Agents :

> C'est normal : pfSense n'est pas un agent Wazuh. Il est visible dans Security events via syslog avec les regles `110010` et `110020`.

Si `5712` n'apparait pas :

> Selon la correlation Wazuh, le live peut sortir `5710`, `5503`, `5551` ou `5763`. La preuve `5712` est conservee dans la documentation SIEM historique.

Si Wazuh charge lentement :

> Le preflight confirme que Wazuh repond. En cas de latence d'interface, nous avons les captures et le dashboard offline comme preuves de secours.
