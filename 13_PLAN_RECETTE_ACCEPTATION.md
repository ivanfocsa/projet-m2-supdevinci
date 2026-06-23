# Plan de recette et criteres d'acceptation - SOC Daylight

## Objectif

Ce plan de recette permet de prouver que le demonstrateur Cyber Trust repond au cahier des charges Daylight. Chaque test associe une exigence, une action, un resultat attendu et une preuve a fournir.

## Perimetre de recette

| Inclus | Non inclus dans la demo |
|---|---|
| Wazuh single-node Docker | Haute disponibilite production |
| Endpoint `poste-01` | Parc complet des trente centres |
| Serveur simule `serveur-01` | Tous les serveurs internes reels |
| Logs applicatifs Daylight | Connecteurs applicatifs definitifs |
| Dashboards technique et executif | Portail client dedie |
| RBAC admin / analyste / supervision | IAM complet avec SSO/MFA |
| Playbooks et REX | SOAR complet automatise |

## Criteres d'acceptation globaux

Le demonstrateur est considere acceptable si :

1. l'interface Wazuh est accessible via navigateur ;
2. au moins trois sources de logs sont documentees ou visibles ;
3. les alertes prioritaires sont montrables ;
4. deux dashboards minimum sont presentes ;
5. le RBAC est explique et prouve ;
6. au moins deux playbooks sont disponibles ;
7. le rapport groupe et les rendus individuels sont fournis ;
8. une video de 15 a 20 minutes montre la solution avec prise de parole de chaque membre.

## Tests de recette

| ID | Exigence | Action | Resultat attendu | Preuve |
|---|---|---|---|---|
| T-01 | Interface web | Ouvrir `https://localhost` | Wazuh Dashboard accessible | CAP-01 |
| T-02 | Collecte endpoint | Afficher `poste-01` | Agent visible et actif | CAP-02, CAP-04 |
| T-03 | Collecte serveur | Afficher `serveur-01` | Agent visible et actif | CAP-02 |
| T-04 | Detection brute force SSH | Lancer simulation SSH | Alerte `5712` | CAP-03 |
| T-05 | Logs metier Daylight | Rejouer logs Daylight | Regles `100110` a `100140` visibles | CAP-05 |
| T-06 | Acces patient suspect | Afficher detail `100120` | Alerte critique contextualisee | CAP-06 |
| T-07 | Dashboard technique | Ouvrir vue technique | Severite, source, top regles | CAP-07 |
| T-08 | Dashboard executif | Ouvrir vue executive | Total, critiques, sites | CAP-08 |
| T-09 | RBAC analyste | Connexion analyste | Administration bloquee | CAP-09 |
| T-10 | Playbook brute force | Ouvrir PB-001 | Procedure exploitable | CAP-10 |
| T-11 | REX incident | Ouvrir REX acces patient | REX documente | CAP-11 |
| T-12 | Architecture | Montrer schema solution | Flux comprehensible | CAP-12 |
| T-13 | Reproductibilite | Lancer preflight | Rapport genere | `preflight-demo-report.txt` |
| T-14 | Rendu documentaire | Ouvrir ZIP final | PDF et preuves presents | ZIP final |
| T-15 | Video | Lire video ou lien | 15-20 min, tous parlent | TXT lien ou MP4 |

## Fiche de validation

| Test | Statut | Commentaire |
|---|---|---|
| T-01 | A valider | |
| T-02 | A valider | |
| T-03 | A valider | |
| T-04 | A valider | |
| T-05 | A valider | |
| T-06 | A valider | |
| T-07 | A valider | |
| T-08 | A valider | |
| T-09 | A valider | |
| T-10 | A valider | |
| T-11 | A valider | |
| T-12 | A valider | |
| T-13 | Valide partiellement | Preflight fonctionne, mais Docker/Wazuh doivent etre lances pour validation complete. |
| T-14 | Valide | ZIP et PDF generes. |
| T-15 | A valider | Video ou lien a ajouter. |

## Proces-verbal de recette a completer

```text
Projet :
Client :
Prestataire :
Date :
Version du ZIP :
Participants :

Tests valides :
Tests non valides :
Reserves :
Decision :
Signature equipe :
```

## Gestion des reserves

| Reserve | Gravite | Traitement |
|---|---|---|
| Capture manquante | Moyenne | Rejouer la sequence et ajouter capture dans `Annexes_Captures/`. |
| Alerte non visible | Haute | Verifier source, relancer logs ou script SIEM. |
| Dashboard incomplet | Moyenne | Montrer la preuve dans la documentation SIEM et completer apres demo. |
| RBAC non prouve | Moyenne | Refaire capture avec compte analyste. |
| Video hors duree | Haute | Remonter la video selon storyboard. |

## Conclusion

Ce plan de recette transforme les exigences du cahier des charges en controles verifiables. Il permet a Cyber Trust de defendre le demonstrateur avec une logique professionnelle : chaque fonction annoncee doit avoir une preuve associee.
