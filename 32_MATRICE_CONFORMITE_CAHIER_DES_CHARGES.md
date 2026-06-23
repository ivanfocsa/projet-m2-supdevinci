# Matrice conformite cahier des charges - Daylight / Cyber Trust

## Objectif

Ce document relie les exigences du cadre pedagogique et du cahier des charges aux preuves presentes dans le rendu final. Il sert de garde-fou pour verifier que l'equipe n'oublie pas un attendu.

## Synthese

- Exigences suivies : 18.
- Exigences OK : 17.
- Exigences a finaliser : 1.
- Point reel restant : lien/MP4 video final.

## Matrice

| ID | Source | Exigence | Owner | Statut | Preuve | Note |
|---|---|---|---|---|---|---|
| PED-01 | Cadre pedagogique | Video 15-20 minutes presentant le MVP avec prise de parole individuelle | Equipe | A_FINALISER | `Dashboards_Offline/daylight_video_recording_pack.html; Config_Video/daylight_video_obs_scenes.csv; Video/PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_video-lien.txt` | Script, teleprompteur, overlays et scene pack prets ; lien YouTube/MP4 reel encore absent. |
| PED-02 | Cadre pedagogique | Rapport technique complet avec architecture, configuration, logs, roles, procedures et REX | Equipe | OK | `Rendus_PDF/PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_RapportGroupe.pdf; Rendus_PDF/PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_DossierGroupeComplet.pdf` | Rapport groupe et dossier groupe consolide generes. |
| PED-03 | Cadre pedagogique | Contribution individuelle de chaque membre | Equipe | OK | `Rendus_PDF/PE-2526_M2CS_YvanFOCSA.pdf; Rendus_PDF/PE-2526_M2CS_YoussefGUERNIOU.pdf; Rendus_PDF/PE-2526_M2CS_KilyanFELIX.pdf; Rendus_PDF/PE-2526_M2CS_MahamadouDIACOUMBA.pdf` | Un rendu individuel PDF par membre. |
| PED-04 | Cadre pedagogique | Gestion de projet, planning, roles et methodologie | Kilyan FELIX | OK | `05_BACKLOG_PLANNING.md; 19_ROLES_CONTRIBUTIONS_PREUVES.md; 31_PACK_SOUTENANCE_JURY.md` | Backlog, roles et parcours de soutenance disponibles. |
| SOC-01 | Cahier des charges | Analyse initiale du besoin client Daylight | Kilyan FELIX | OK | `14_SYNTHESE_EXECUTIVE_CLIENT.md; 01_RAPPORT_TECHNIQUE_GROUPE.md` | Contexte client, risques et objectifs formalises. |
| SOC-02 | Cahier des charges | Document architecture technique | Yvan FOCSA | OK | `01_RAPPORT_TECHNIQUE_GROUPE.md; Annexes_Captures/CAP-12_architecture-solution.png` | Architecture de demonstration et cible documentees. |
| SOC-03 | Cahier des charges | Demonstrateur operationnel | Youssef GUERNIOU / Mahamadou DIACOUMBA | OK | `Youssef GUERNIOU/setup-siem-lab.ps1; Preuves_SIEM_Youssef/Documentation_SIEM_Youssef_GUERNIOU.pdf; Rapports_Preflight/preflight-demo-report.txt; Annexes_Captures/CAP-25_preflight-demo-ok.png` | Lab Wazuh operationnel : Docker daemon OK, 3 conteneurs Wazuh UP, dashboard https://localhost en statut 200 via preflight CAP-25. |
| SOC-04 | Cahier des charges | Collecte multi-source agents, syslog ou API | Youssef GUERNIOU | OK | `Youssef GUERNIOU/Documentation_SIEM_Youssef_GUERNIOU.pdf; Demo_Logs/pfsense.log; Demo_Logs/daylight_app.log; Config_PfSense/pfsense_syslog_wazuh.md` | Endpoint, serveur, logs applicatifs, pfSense/syslog et logs demo couverts. |
| SOC-05 | Cahier des charges | SIEM open-source centralise | Youssef GUERNIOU | OK | `Youssef GUERNIOU/Documentation_SIEM_Youssef_GUERNIOU.pdf; 02_GUIDE_DEPLOIEMENT_UTILISATION.md` | Wazuh retenu et documente. |
| SOC-06 | Cahier des charges | Regles de detection et alerting personnalisables | Kilyan FELIX / Youssef GUERNIOU | OK | `Config_Wazuh/local_rules_daylight_pfsense.xml; Config_Wazuh/daylight_alert_qualification_matrix.csv; Annexes_Captures/CAP-03_alerte-5712-brute-force-ssh.png` | Regles 5712, 100xxx et 110xxx referencees et qualifiees. |
| SOC-07 | Cahier des charges | Dashboards lisibles et segmentes | Kilyan FELIX | OK | `Dashboards_Offline/daylight_soc_dashboard.html; Annexes_Captures/CAP-07_dashboard-technique.png; Annexes_Captures/CAP-08_dashboard-executif.png` | Vue analyste et executive disponibles. |
| SOC-08 | Cahier des charges | Playbooks de reponse semi-automatises | Mahamadou DIACOUMBA | OK | `03_PLAYBOOKS_PROCEDURES_REX.md; Annexes_Captures/CAP-10_playbook-brute-force.png; Annexes_Captures/CAP-28_rex-incident-rempli.png` | Playbooks et REX documentes avec preuves visuelles. |
| SOC-09 | Cahier des charges | Reporting simple et exportable | Kilyan FELIX | OK | `Rendus_PDF/; Dashboards_Offline/daylight_final_evidence_status.html; MANIFEST_DEPOT.md` | PDF, dashboards offline, manifeste et hash disponibles. |
| SOC-10 | Cahier des charges | Interface web accessible et segmentee par roles supervision, analyste, admin | Youssef GUERNIOU | OK | `Annexes_Captures/CAP-01_wazuh-dashboard-login.png; Annexes_Captures/CAP-09_rbac-analyste-lecture-seule.png` | Preuves Wazuh et RBAC extraites du dossier SIEM. |
| SOC-11 | Cahier des charges | Simulation d'un ou plusieurs sites clients avec VMs ou conteneurs | Mahamadou DIACOUMBA | OK | `Config_Lab/daylight_vm_inventory.csv; Config_Lab/daylight_lab_runbook.csv; 22_EXPLOITATION_VM_RUNBOOK_REX.md` | Inventaire et runbook VM/conteneurs fournis. |
| SOC-12 | Cahier des charges | Generation de logs realistes attaque et safe | Mahamadou DIACOUMBA | OK | `tools/generate_demo_logs.py; Demo_Logs/; tools/send_demo_logs_to_syslog.py; Annexes_Captures/CAP-27_rejeu-logs-dry-run.png` | Logs pfSense, application, AD/fichiers, mail et endpoint generes. |
| SOC-13 | Cahier des charges | Templates de deploiement client et solution industrialisable | Yvan FOCSA | OK | `02_GUIDE_DEPLOIEMENT_UTILISATION.md; Config_PfSense/README_IMPORT_PFSENSE_DAYLIGHT.md; Config_PfSense/pfsense_demo_test_plan.csv` | Guide, imports pfSense, configs Wazuh et trajectoire cible documentes. |
| SOC-14 | Cahier des charges | CLI ou API exposee si automatisation prevue | Youssef GUERNIOU / Mahamadou DIACOUMBA | OK | `tools/preflight_demo.ps1; tools/send_demo_logs_to_syslog.py; Youssef GUERNIOU/setup-siem-lab.ps1; Wazuh API https://localhost:55000` | Exigence optionnelle couverte par scripts CLI et API native Wazuh ; aucune API custom n'est necessaire pour le MVP. |
