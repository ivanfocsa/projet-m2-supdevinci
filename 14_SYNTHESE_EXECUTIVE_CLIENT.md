# Synthese executive client - Daylight / Cyber Trust

## Message principal

Cyber Trust propose a Daylight un demonstrateur de SOC externalise capable de centraliser les evenements de securite, detecter les comportements suspects, restituer les alertes dans des dashboards lisibles et guider la reponse par des playbooks.

La solution est construite pour une demonstration reproductible, mais elle prepare aussi une trajectoire industrialisable pour un reseau d'environ trente centres d'audioprothesistes.

## Probleme client

Daylight manipule des donnees sensibles : dossiers patients, rendez-vous, donnees CRM, comptes utilisateurs et traces techniques. Le SI est distribue sur plusieurs sites, avec des postes, serveurs, applications metier, messagerie et equipements reseau.

Sans SOC interne, Daylight manque de visibilite sur :

- les tentatives d'intrusion ;
- les acces anormaux aux dossiers patients ;
- les elevations de privileges ;
- les usages endpoint suspects ;
- les incidents necessitant une reponse rapide.

## Reponse Cyber Trust

| Besoin Daylight | Reponse Cyber Trust |
|---|---|
| Centraliser les logs | Wazuh comme SIEM open-source centralise. |
| Collecter plusieurs sources | Endpoint `poste-01`, serveur `serveur-01`, logs applicatifs Daylight. |
| Detecter les incidents | Regles `5712`, `100110`, `100120`, `100130`, `100140`. |
| Rendre les alertes lisibles | Dashboard technique et dashboard executif. |
| Segmenter les acces | RBAC admin / analyste / supervision. |
| Reagir efficacement | Playbooks, procedures et REX incidents. |
| Industrialiser | Architecture cible multi-site et plan de deploiement. |

## Valeur pour Daylight

1. **Visibilite cyber immediate** : les evenements importants sont centralises dans Wazuh.
2. **Priorisation des risques** : les alertes critiques sont distinguees des alertes informatives.
3. **Protection des donnees patients** : l'acces anormal aux dossiers patients est un scenario central.
4. **Exploitation claire** : les playbooks indiquent quoi verifier, qui prevenir et quoi documenter.
5. **Pilotage client** : le dashboard executif permet une lecture simple des alertes et tendances.
6. **Reproductibilite** : scripts, guide et preflight facilitent la relance du lab.

## Demonstrateur livre

| Element | Statut |
|---|---|
| Wazuh single-node Docker | Documente dans le perimetre SIEM |
| Sources endpoint / serveur / application | Documentees et preparees pour demonstration |
| Alertes principales | Documentees |
| Dashboards | Documentes |
| RBAC | Documente |
| Guide de deploiement | Livre |
| Playbooks et REX | Livres |
| Rapport groupe et rendus individuels | Livres |
| PowerPoint et notes orateur | Livres |
| Preflight et reconstruction ZIP | Livres |

## Limites assumees

Le demonstrateur n'est pas une production haute disponibilite. Il prouve le fonctionnement du SOC, mais une mise en production demanderait :

- separation des composants Wazuh ;
- sauvegarde et retention formalisees ;
- integration firewall, messagerie et Active Directory ;
- MFA et durcissement d'administration ;
- ticketing ou SOAR ;
- SLA et contrat de sous-traitance securite.

## Recommandation finale

Cyber Trust recommande de valider le demonstrateur sur un pilote Daylight, puis d'etendre progressivement la collecte aux centres. La priorite de production doit etre de couvrir les donnees patients, les comptes privilegies, les endpoints et les flux critiques.

Le projet fournit donc une base SOC claire, defendable et evolutive.
