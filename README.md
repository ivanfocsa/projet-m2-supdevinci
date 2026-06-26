# Projet M2 SUP DE VINCI - Cyber Trust pour Daylight

Ce dépôt contient la version propre des livrables utiles pour le projet M2 Cybersécurité.
Les fichiers ont été triés par usage et par participant afin d’éviter les doublons, les anciennes versions et les fichiers de travail inutiles.

## À rendre en priorité

| Élément | Emplacement |
|---|---|
| Rapport groupe final Word | `Rendu_Groupe/Rapport_final/PE-2526_MSI526CSB_RapportGroupe_CyberTrust.docx` |
| Rapport groupe final PDF | `Rendu_Groupe/Rapport_final/PE-2526_MSI526CSB_RapportGroupe_CyberTrust.pdf` |
| Rapport individuel Yvan Word | `Participants/Yvan_FOCSA/Rapport_individuel/PE-2526_MSI526CSB_FocsaYvan.docx` |
| Rapport individuel Yvan PDF | `Participants/Yvan_FOCSA/Rapport_individuel/PE-2526_MSI526CSB_FocsaYvan.pdf` |
| Script vidéo équipe | `Soutenance_Video/Script_video/05_Script_Video_Equipe_CyberTrust_Daylight.docx` |
| Cahier des charges et cadre pédagogique | `Consignes/` |

## Organisation du dépôt

| Dossier | Contenu |
|---|---|
| `Consignes` | Cahier des charges et cadre pédagogique du projet. |
| `Rendu_Groupe` | Rapport groupe final et annexes de contrôle. |
| `Participants/Yvan_FOCSA` | Rapport individuel, contribution groupe, schémas, captures pfSense et configuration réseau. |
| `Participants/Youssef_GUERNIOU` | Documentation SIEM, Wazuh, règles, scripts et rapport individuel. |
| `Participants/Kilyan_FELIX` | Détection, qualification, dashboards, matrices d’alertes et rapport individuel. |
| `Participants/Mahamadou_DIACOUMBA` | Exploitation, playbooks, procédures, REX et rapport individuel. |
| `Demonstrateur_Technique` | Configuration, logs de démo, captures, dashboards offline et scripts utiles. |
| `Soutenance_Video` | Script oral, support de présentation et éléments vidéo. |

## Répartition des rôles

| Participant | Rôle projet | Périmètre principal |
|---|---|---|
| Yvan FOCSA | Architecte solution | Architecture cible, segmentation réseau, pfSense, zones, flux, supervision firewall. |
| Youssef GUERNIOU | Ingénieur SIEM Wazuh | Déploiement Wazuh, collecte, règles de détection, dashboards, RBAC. |
| Kilyan FELIX | Chef projet détection | Qualification des alertes, priorisation, synthèse client, suivi des dashboards. |
| Mahamadou DIACOUMBA | Exploitation SOC | Runbooks, playbooks, procédures, REX incidents, exploitation du lab. |

## Notes d’utilisation

Le dossier `Demonstrateur_Technique` sert à justifier le fonctionnement du démonstrateur. Il contient notamment les configurations pfSense et Wazuh, les logs de démonstration et les captures de preuve.

Le dossier `Participants` permet de retrouver rapidement ce qui est associé à chaque membre de l’équipe. Pour la soutenance, il est recommandé d’ouvrir d’abord le rapport groupe, puis les dossiers individuels uniquement si le jury demande une preuve détaillée.

