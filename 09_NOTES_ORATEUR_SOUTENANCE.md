# Notes orateur - Soutenance Daylight / Cyber Trust

## Utilisation

Ces notes accompagnent le PowerPoint `Presentation_Daylight_CyberTrust.pptx`. Elles servent a repartir la parole et a garder une video fluide de 15 a 20 minutes.

## Slide 1 - Titre

**Intervenant : Kilyan**

Bonjour, nous sommes Cyber Trust. Nous allons presenter notre projet de SOC externalise pour Daylight, un reseau de centres d'audioprothesistes. L'objectif est de montrer une solution de supervision securite centralisee, demonstrable et industrialisable.

## Slide 2 - Contexte client

**Intervenant : Kilyan**

Daylight possede plusieurs centres en France. Les utilisateurs manipulent des donnees sensibles : dossiers patients, rendez-vous, CRM et elements administratifs. Le client manque de ressources cyber internes, donc il souhaite externaliser la surveillance et la reponse de premier niveau.

## Slide 3 - Besoin et objectifs

**Intervenant : Kilyan**

Le cahier des charges demande un SOC capable de collecter plusieurs sources, detecter des evenements suspects, afficher des dashboards lisibles, segmenter les acces par role et fournir des playbooks de reponse.

## Slide 4 - Equipe et roles

**Intervenant : Kilyan**

La repartition couvre les quatre dimensions du projet : Yvan pour l'architecture, Youssef pour le SIEM Wazuh, Kilyan pour la coordination et la detection, Mahamadou pour l'exploitation, les procedures et les REX.

## Slide 5 - Architecture de demonstration

**Intervenant : Yvan**

Pour la demonstration, nous avons retenu Wazuh en mode Docker single-node. Les evenements proviennent d'un endpoint Windows, d'un serveur Linux simule et de logs applicatifs Daylight. Les donnees sont centralisees dans Wazuh Manager, indexees, puis consultees via Wazuh Dashboard.

## Slide 6 - Architecture cible

**Intervenant : Yvan**

En production, nous separerions les composants pour ameliorer la disponibilite, la performance et la maintenabilite. L'objectif serait de raccorder progressivement les centres Daylight, en ajoutant les firewalls, la messagerie et l'annuaire.

## Slide 7 - Demonstration SIEM

**Intervenant : Youssef**

Je presente maintenant la partie SIEM. Wazuh est deploye avec Manager, Indexer et Dashboard. Le script automatise le serveur `serveur-01`, installe l'agent, active SSH et rsyslog, puis genere une attaque brute force pour declencher une alerte.

## Slide 8 - Sources de logs

**Intervenant : Youssef**

Nous avons trois familles de sources : `poste-01` pour l'endpoint, `serveur-01` pour le serveur Linux et les logs Daylight pour les evenements metier. Cela repond a l'exigence de collecte multi-source.

## Slide 9 - Alertes cles

**Intervenant : Youssef**

Les alertes importantes sont la brute force SSH `5712`, la brute force applicative `100110`, l'acces anormal a un dossier patient `100120`, la modification de groupe privilegie `100130` et l'usage USB suspect `100140`.

## Slide 10 - Dashboards

**Intervenant : Kilyan**

Le dashboard technique aide l'analyste avec les severites, sources et top regles. Le dashboard executif donne une lecture plus simple pour le client : nombre d'alertes, critiques et repartition par site.

## Slide 11 - Qualification SOC

**Intervenant : Kilyan**

Nous classons les alertes selon leur impact. Les donnees patients et privileges sont critiques. Les brute force sont hautes. L'USB suspect est moyen a haut selon le contexte. Cette matrice evite de traiter toutes les alertes au meme niveau.

## Slide 12 - RBAC

**Intervenant : Youssef**

Le cahier des charges demande des vues par role. Nous avons donc un profil admin complet, un profil analyste en lecture et un profil supervision. Le role `soc_readonly` limite les acces des comptes non administrateurs.

## Slide 13 - Playbooks

**Intervenant : Mahamadou**

Une alerte n'est utile que si elle declenche une action claire. Nous avons donc formalise des playbooks : brute force SSH, acces dossier patient, brute force applicative, modification privilege, USB suspect et phishing.

## Slide 14 - REX incidents

**Intervenant : Mahamadou**

Les REX permettent d'ameliorer le SOC apres chaque incident. Par exemple, apres une brute force SSH, il faut verifier s'il y a eu connexion reussie. Pour un acces patient, il faut verifier le profil metier et les dossiers touches.

## Slide 15 - Guide et exploitation

**Intervenant : Mahamadou**

Nous avons aussi documente le redemarrage du lab. Apres extinction, certains services doivent etre relances : Wazuh, le conteneur `serveur-01`, `rsyslogd`, SSH et l'agent Wazuh. Cela garantit une demo reproductible.

## Slide 16 - Couts et industrialisation

**Intervenant : Yvan**

Wazuh limite les couts de licence, mais une production a quand meme des couts d'infrastructure, stockage, exploitation et formation. La bonne approche est de commencer par un pilote, puis d'etendre progressivement aux centres Daylight.

## Slide 17 - Limites

**Intervenant : Yvan**

La limite principale est que le lab n'est pas une architecture de production haute disponibilite. Il faut encore dimensionner la volumetrie, ajouter des sources comme firewall et messagerie, et connecter un outil de ticketing.

## Slide 18 - Conclusion

**Intervenants : toute l'equipe**

La solution repond au cahier des charges : SIEM open-source, collecte multi-source, alertes, dashboards, RBAC, playbooks, REX et documentation. Cyber Trust fournit ainsi a Daylight une base SOC claire, reproductible et evolutive.

## Derniere checklist video

- Afficher le nom de chaque intervenant.
- Garder Wazuh ouvert avant de lancer l'enregistrement.
- Montrer au minimum agents, alerte `5712`, alerte `100120`, dashboards, RBAC et playbook.
- Ne pas lire mot pour mot : utiliser ces notes comme filet de securite.
