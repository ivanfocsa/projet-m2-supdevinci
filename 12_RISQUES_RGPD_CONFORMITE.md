# Risques, RGPD et conformite - Daylight / Cyber Trust

## Objectif

Cette annexe complete le rapport technique avec une lecture client : quels risques Daylight doit maitriser, quelles mesures Cyber Trust propose et quels points de vigilance RGPD doivent etre traites dans une industrialisation du SOC.

## Donnees sensibles traitees par Daylight

| Donnee | Sensibilite | Risque principal |
|---|---|---|
| Dossiers patients | Tres elevee | Consultation non autorisee, fuite de donnees personnelles de sante. |
| Rendez-vous | Moyenne a elevee | Profilage client, perturbation d'activite. |
| Donnees CRM | Elevee | Vol de base client, phishing cible. |
| Comptes utilisateurs | Elevee | Usurpation, elevation de privileges. |
| Logs techniques | Moyenne a elevee | Exposition d'identifiants, IP, traces utilisateur. |

## Matrice des risques

| ID | Risque | Probabilite | Impact | Niveau | Mesures Cyber Trust |
|---|---|---:|---:|---:|---|
| R-01 | Acces anormal a un dossier patient | Moyenne | Tres fort | Critique | Regle `100120`, dashboard critique, playbook PB-002, escalade client. |
| R-02 | Brute force applicatif | Moyenne | Fort | Haut | Regle `100110`, blocage source, reinitialisation mot de passe. |
| R-03 | Brute force SSH serveur | Moyenne | Fort | Haut | Regle `5712`, suivi `auth.log`, playbook PB-001. |
| R-04 | Elevation de privileges | Faible a moyenne | Tres fort | Critique | Regle `100130`, validation changement, retrait privilege. |
| R-05 | Usage USB non autorise | Moyenne | Moyen a fort | Moyen/Haut | Regle `100140`, controle endpoint, sensibilisation. |
| R-06 | Phishing messagerie | Elevee | Fort | Haut | Playbook phishing, surveillance messagerie a ajouter en production. |
| R-07 | Indisponibilite SOC | Faible en demo, moyenne en prod | Fort | Haut | Architecture cible separee, sauvegarde, supervision sante plateforme. |
| R-08 | Sur-retention de logs | Moyenne | Moyen | Moyen | Politique de retention, minimisation, purge. |

## Points RGPD

Le projet manipule ou simule des donnees associees a des patients. Meme dans un demonstrateur, la posture attendue est celle d'un prestataire professionnel.

| Sujet RGPD | Recommandation |
|---|---|
| Finalite | Limiter l'usage des logs a la securite, la detection et la reponse incident. |
| Minimisation | Ne collecter que les champs utiles a la detection et a l'investigation. |
| Retention | Definir une duree de conservation des logs selon les besoins legaux et operationnels. |
| Acces | Segmenter les droits via RBAC : admin, analyste, supervision. |
| Tracabilite | Journaliser les acces a la plateforme SOC et aux alertes sensibles. |
| Donnees patients | Eviter d'afficher des donnees nominatives completes dans les dashboards executifs. |
| Sous-traitance | Formaliser Cyber Trust comme sous-traitant securite dans une convention de service. |
| Notification | Prevoir une procedure d'escalade si incident de donnees personnelles confirme. |

## Mesures de securite proposees

### Dans le demonstrateur

- Centralisation Wazuh.
- Collecte endpoint, serveur et application metier.
- Alertes critiques sur acces patient et privileges.
- RBAC lecture seule pour analyste et supervision.
- Playbooks de reponse et REX.
- Documentation de redemarrage et preflight demo.

### Pour la production

- Chiffrement des flux agents vers manager.
- Durcissement des serveurs Wazuh.
- Sauvegarde et restauration de l'indexer.
- Rotation et coffre des secrets.
- MFA pour les administrateurs.
- Retention differenciee selon criticite.
- Supervision de la sante de la plateforme SOC.
- Integration ticketing pour tracer les decisions.

## Recommandations contractuelles Cyber Trust / Daylight

| Clause | Contenu conseille |
|---|---|
| Perimetre | Sites, sources de logs, applications, comptes, exclusions. |
| SLA de qualification | Delai cible selon severite critique, haute, moyenne, basse. |
| Escalade | Contacts Daylight, astreinte, canaux de crise. |
| Reporting | Rapport mensuel, indicateurs, incidents majeurs, ameliorations. |
| Confidentialite | Protection des logs, preuves et donnees personnelles. |
| Reversibilite | Export des donnees et transfert documentaire en fin de contrat. |
| Amelioration continue | REX, tuning des regles, revue trimestrielle. |

## Indicateurs de conformite a suivre

| KPI | Objectif |
|---|---|
| Sources actives / sources attendues | Mesurer la couverture de supervision. |
| Alertes critiques qualifiees dans le SLA | Prouver la performance SOC. |
| Incidents avec REX | Alimenter l'amelioration continue. |
| Comptes admin revus | Eviter les privileges dormants. |
| Regles modifiees avec justification | Maintenir la tracabilite du tuning. |
| Logs purges selon retention | Controler le risque RGPD. |

## Conclusion

Le demonstrateur Cyber Trust couvre les premiers besoins de detection et de reaction. Pour une mise en production Daylight, la dimension RGPD et contractuelle doit etre formalisee : finalites, retention, acces, notification, SLA et reversibilite. Cette annexe donne la base de discussion entre le client et le prestataire.
