# Questions / reponses soutenance - Daylight / Cyber Trust

## Objectif

Ce document prepare l'equipe aux questions probables du jury ou d'un client fictif Daylight. Les reponses sont volontairement courtes pour etre utilisables a l'oral.

## Questions sur le besoin client

### Pourquoi Daylight a besoin d'un SOC externalise ?

Daylight gere plusieurs centres et des donnees sensibles, notamment des dossiers patients. Le SOC externalise apporte une surveillance centralisee, une capacite de detection et des procedures de reponse sans exiger que Daylight construise immediatement une equipe SOC interne.

### Pourquoi le scenario dossier patient est central ?

Parce qu'il touche directement a des donnees sensibles. Une consultation anormale peut avoir un impact juridique, reputational et operationnel. La regle `100120` sert a montrer que le SOC ne detecte pas seulement des attaques techniques, mais aussi des comportements metier a risque.

### Qu'est-ce que Cyber Trust apporte de plus qu'un simple outil ?

Cyber Trust apporte l'architecture, l'exploitation, la qualification, les playbooks, le reporting, les roles, le REX et la trajectoire d'industrialisation. Le SIEM est un composant ; le service SOC est l'ensemble de la methode.

## Questions sur les choix techniques

### Pourquoi Wazuh ?

Wazuh est open-source, documente, compatible agents, syslog et dashboards. Il permet de couvrir endpoint, serveur et logs applicatifs dans un demonstrateur realiste sans cout de licence SIEM.

### Pourquoi un single-node Docker pour la demo ?

Le single-node est adapte a une soutenance : installation plus simple, environnement reproductible, temps de lancement limite. Pour la production, nous proposons une architecture separee avec manager, indexer et dashboard distincts.

### Est-ce une architecture de production ?

Non. C'est un demonstrateur operationnel. La production demanderait haute disponibilite, sauvegarde, retention, durcissement, supervision de plateforme, gestion des secrets et integration ticketing.

### Pourquoi trois sources de logs ?

Elles couvrent trois angles essentiels : endpoint utilisateur, serveur interne et application metier Daylight. Cela prouve la collecte multi-source demandee par le cahier des charges.

## Questions sur la detection

### Quelles alertes montrez-vous ?

Les alertes principales sont `5712` pour brute force SSH, `100110` pour brute force applicative, `100120` pour acces anormal dossier patient, `100130` pour modification de groupe privilegie et `100140` pour usage USB suspect.

### Comment eviter trop de faux positifs ?

Par la qualification SOC : contexte utilisateur, actif concerne, horaire, repetition, criticite metier et correlation avec d'autres signaux. Les dashboards aident a voir les tendances et les playbooks a standardiser les decisions.

### Quelle est la difference entre alerte haute et critique ?

Une alerte critique touche un actif ou une donnee a impact majeur : donnees patients, privileges, compromission probable. Une alerte haute indique une attaque ou tentative serieuse, mais l'impact doit encore etre confirme.

## Questions sur les dashboards

### Pourquoi deux dashboards ?

Le dashboard technique sert aux analystes : severite, sources, regles, details. Le dashboard executif sert au pilotage : volumes, critiques, repartition par site, tendances. Les deux publics n'ont pas le meme besoin.

### Comment prouver que les dashboards sont utiles ?

Pendant la demo, on montre comment passer d'un indicateur global a une alerte detaillee, puis a un playbook. L'utilite vient de la capacite a prendre une decision plus rapidement.

## Questions sur le RBAC

### Pourquoi segmenter les roles ?

Pour eviter que tous les utilisateurs aient des droits administrateur. Le cahier des charges demande des vues supervision / analyste / admin. Le RBAC permet de limiter les risques d'erreur ou d'abus.

### Que peut faire l'analyste ?

L'analyste consulte les alertes et dashboards pour qualifier les incidents. Il ne doit pas administrer la plateforme ni modifier les droits.

## Questions RGPD et conformite

### Quels sont les risques RGPD ?

Les logs peuvent contenir des identifiants, traces d'acces, IP, actions utilisateur et references a des dossiers patients. Il faut limiter la collecte, definir la retention, segmenter les acces et tracer les consultations.

### Le SOC peut-il afficher des donnees patients ?

Il faut eviter d'afficher des donnees nominatives completes dans les dashboards, surtout executifs. Les informations doivent etre suffisantes pour investiguer, mais limitees selon le principe de minimisation.

### Que faire si une fuite de donnees est confirmee ?

Escalade immediate, conservation des preuves, identification du perimetre touche, information du referent Daylight, analyse RGPD et decision de notification selon le cadre legal.

## Questions exploitation

### Que faire si le lab ne demarre pas ?

Lancer le preflight, verifier Docker Desktop, relancer Wazuh, demarrer `serveur-01`, puis relancer `rsyslogd`, SSH et l'agent Wazuh si necessaire. Le mode operatoire jour J liste les commandes.

### Pourquoi un script de preflight ?

Il evite de decouvrir les problemes pendant la video. Il verifie les fichiers, PDF, archive, outils, Docker, Wazuh, captures et lien video.

### Pourquoi un script de reconstruction ZIP ?

Apres ajout des captures ou du lien video, il faut reconstruire le rendu final sans oublier un fichier. Le script automatise cette etape.

## Questions sur les roles de l'equipe

### Que fait Yvan ?

Yvan porte l'architecture, la coherence technique, les choix d'industrialisation, les limites et la vision cible.

### Que fait Youssef ?

Youssef porte Wazuh, le SIEM, la collecte, les agents, les dashboards techniques et le RBAC.

### Que fait Kilyan ?

Kilyan porte la coordination, la detection, la qualification, les dashboards et la structuration de la demonstration.

### Que fait Mahamadou ?

Mahamadou porte l'exploitation, les VM/conteneurs, les playbooks, les procedures de redemarrage et les REX incidents.

## Questions sur les limites

### Quelle est la principale limite du projet ?

Le demonstrateur est local et single-node. Il prouve la faisabilite, mais pas encore la robustesse production.

### Que faudrait-il faire ensuite ?

Ajouter firewall, messagerie et Active Directory ; separer les composants Wazuh ; definir retention et sauvegarde ; connecter un ticketing ; deployer sur un pilote Daylight.

### Si vous aviez une semaine de plus ?

Nous ajouterions des captures finales completes, un mini ticketing, des logs firewall/messagerie simules et une verification automatisee des alertes attendues.

## Reponse finale type

La force du projet est de relier outil, methode et exploitation. Nous ne presentons pas seulement Wazuh : nous presentons une base de SOC externalise avec detection, dashboards, roles, playbooks, REX, guide de deploiement, recette et trajectoire de production.
