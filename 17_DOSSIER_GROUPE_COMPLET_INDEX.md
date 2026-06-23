# Dossier groupe complet - Daylight / Cyber Trust

## Objet du PDF consolide

Ce document sert de page d'entree au PDF groupe complet. Le fichier consolide est genere automatiquement dans :

```text
Rendus_PDF/PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_DossierGroupeComplet.pdf
```

Il rassemble les pieces groupe les plus utiles pour une lecture jury/client, dans un ordre logique : decision, architecture, exploitation, preuves, recette et soutenance.

## Composition du dossier consolide

| Ordre | Document | Role |
|---:|---|---|
| 1 | Synthese executive client | Lecture rapide pour Daylight. |
| 2 | Rapport technique groupe | Coeur du rendu collectif. |
| 3 | Pack solutions concretes demo | pfSense, regles Wazuh custom, logs demonstrables. |
| 4 | Roles, contributions et preuves | Ce que chaque membre montre, avec commandes et preuves associees. |
| 5 | Mode operatoire pfSense/Wazuh lab | Procedure VM, interfaces, tests et captures firewall/SIEM. |
| 6 | Dashboards, alertes et qualification | Requetes Wazuh, widgets et matrice SOC. |
| 7 | Dashboard SOC offline | HTML et captures de secours generes depuis les logs demo. |
| 8 | Exploitation VM, runbook et REX | Inventaire lab, relance, incidents et preuves exploitation. |
| 9 | Preuves finales captures/video/depot | Checklist officielle, proprietaires et controles avant ZIP. |
| 10 | Mode operatoire captures Wazuh/preflight | Procedure exacte pour CAP-01, CAP-02, CAP-03 et CAP-25. |
| 11 | Mode operatoire video et depot | Procedure YouTube/MP4, description et controle video. |
| 12 | Manifeste depot et integrite | Etat reel du dossier, empreintes SHA-256 et pieces restantes. |
| 13 | Runbook express preuves restantes | Procedure courte pour produire les captures/video et reconstruire le ZIP. |
| 14 | Import des preuves finales | Import automatique des captures, lien YouTube ou MP4 au bon nom. |
| 15 | Tableau de bord statut final | Vue HTML locale du reste a faire captures/video/ZIP. |
| 16 | Registre exigences et synthese | Correspondance cahier des charges / livrables. |
| 17 | Guide de deploiement et utilisation | Reproductibilite et exploitation. |
| 18 | Playbooks, procedures et REX | Reponse incident et amelioration continue. |
| 19 | Risques, RGPD et conformite | Lecture client, donnees sensibles et obligations. |
| 20 | Plan de recette et acceptation | Criteres de validation du demonstrateur. |
| 21 | Dossier de preuves et captures | Liste des preuves attendues. |
| 22 | Annexe captures Wazuh | Etat reel des captures presentes/manquantes. |
| 23 | Audit final des consignes | Verification de couverture des attendus. |
| 24 | Backlog et planning | Organisation projet et RACI. |
| 25 | Mode operatoire demo jour J | Procedure de repetition et enregistrement. |
| 26 | Checklist depot final | Derniers controles avant depot. |
## Remarque importante

Les captures Wazuh et le lien video dependent de l'environnement de demonstration et de l'enregistrement par l'equipe. Le PDF consolide reflete l'etat reel du dossier au moment de sa generation : aucune capture n'est inventee ou simulee.

## Commandes de regeneration

```powershell
python .\tools\build_capture_annex.py
python .\tools\export_markdown_to_pdf.py
python .\tools\build_group_dossier_pdf.py
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\rebuild_rendu_final.ps1
```






