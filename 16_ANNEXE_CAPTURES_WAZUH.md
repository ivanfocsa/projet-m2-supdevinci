# Annexe captures et preuves - Daylight / Cyber Trust

## Objectif

Cette annexe assemble les captures et preuves visuelles du demonstrateur SOC. Elle est generee automatiquement depuis `config/captures/daylight_capture_checklist.csv` et le dossier `Annexes_Captures/`.

Regeneration :

```powershell
python .\tools\render_static_proof_images.py
python .\tools\build_capture_annex.py
python .\tools\export_markdown_to_pdf.py
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File .\tools\rebuild_rendu_final.ps1
```

## Synthese des preuves

| ID | Statut | Priorite | Obligatoire depot | Fichier | Preuve | Responsable |
|---|---|---:|---|---|---|---|
| CAP-01 | OK | 1 | yes | `CAP-01_wazuh-dashboard-login.png` | Wazuh accessible | Youssef |
| CAP-02 | OK | 1 | yes | `CAP-02_agents-poste01-serveur01.png` | Collecte multi-source | Youssef |
| CAP-03 | OK | 1 | yes | `CAP-03_alerte-5712-brute-force-ssh.png` | Detection brute force SSH | Youssef |
| CAP-04 | OK | 2 | no | `CAP-04_source-endpoint-poste01-sca.png` | Endpoint/SCA | Youssef |
| CAP-05 | OK | 2 | no | `CAP-05_daylight-alertes-metier.png` | Custom rules Daylight | Youssef |
| CAP-06 | OK | 1 | yes | `CAP-06_alerte-100120-acces-patient.png` | Patient data protection | Kilyan |
| CAP-07 | OK | 1 | yes | `CAP-07_dashboard-technique.png` | Dashboard analyste | Kilyan |
| CAP-08 | OK | 1 | yes | `CAP-08_dashboard-executif.png` | Dashboard client | Kilyan |
| CAP-09 | OK | 2 | no | `CAP-09_rbac-analyste-lecture-seule.png` | RBAC | Youssef |
| CAP-10 | OK | 2 | no | `CAP-10_playbook-brute-force.png` | Playbook | Mahamadou |
| CAP-11 | OK | 2 | no | `CAP-11_rex-incident-acces-patient.png` | REX incident | Mahamadou |
| CAP-12 | OK | 2 | no | `CAP-12_architecture-solution.png` | Architecture | Yvan |
| CAP-13 | OK | 1 | yes | `CAP-13_pfsense-regles-firewall.png` | Firewall/routeur concret | Yvan |
| CAP-14 | OK | 2 | no | `CAP-14_pfsense-syslog-wazuh.png` | Syslog firewall | Yvan/Youssef |
| CAP-15 | OK | 2 | no | `CAP-15_script-setup-siem-lab.png` | Automation lab | Youssef |
| CAP-16 | OK | 2 | no | `CAP-16_auth-log-serveur01.png` | Source SSH brute force | Mahamadou |
| CAP-17 | OK | 2 | no | `CAP-17_compte-supervision-dashboard.png` | RBAC supervision | Youssef |
| CAP-18 | OK | 2 | no | `CAP-18_export-dashboard-report.png` | Reporting export | Kilyan |
| CAP-19 | OK | 2 | no | `CAP-19_wazuh-pfsense-alertes.png` | pfSense alerting | Yvan/Youssef |
| CAP-20 | OK | 2 | no | `CAP-20_wazuh-rejeu-logs-demo.png` | Log replay | Mahamadou |
| CAP-21 | OK | 2 | no | `CAP-21_dashboard-technique-requetes.png` | Dashboard queries | Kilyan |
| CAP-22 | OK | 2 | no | `CAP-22_dashboard-executif-daylight.png` | Executive dashboard | Kilyan |
| CAP-23 | OK | 2 | no | `CAP-23_qualification-alerte-100120.png` | Alert qualification | Kilyan |
| CAP-24 | OK | 2 | no | `CAP-24_qualification-alerte-110020.png` | Firewall alert qualification | Kilyan |
| CAP-25 | OK | 1 | yes | `CAP-25_preflight-demo-ok.png` | Lab exploitation | Mahamadou |
| CAP-26 | MANQUANT | 2 | no | `CAP-26_docker-conteneurs-lab.png` | Containers | Mahamadou |
| CAP-27 | OK | 2 | no | `CAP-27_rejeu-logs-dry-run.png` | Replay logs | Mahamadou |
| CAP-28 | OK | 2 | no | `CAP-28_rex-incident-rempli.png` | REX completed | Mahamadou |

Captures/preuves presentes : **27 / 28**.
Captures prioritaires presentes : **8 / 8**.

## Captures integrees

### CAP-01 - Wazuh accessible

Responsable : Youssef  
Priorite : 1  
Obligatoire depot : yes

<figure class="capture">
  <img src="file:///C:/Users/Ivan/Pictures/PROJET%20M2/Annexes_Captures/CAP-01_wazuh-dashboard-login.png" alt="Wazuh Dashboard logged in">
  <figcaption>Wazuh Dashboard logged in</figcaption>
</figure>


### CAP-02 - Collecte multi-source

Responsable : Youssef  
Priorite : 1  
Obligatoire depot : yes

<figure class="capture">
  <img src="file:///C:/Users/Ivan/Pictures/PROJET%20M2/Annexes_Captures/CAP-02_agents-poste01-serveur01.png" alt="Wazuh agents page">
  <figcaption>Wazuh agents page</figcaption>
</figure>


### CAP-03 - Detection brute force SSH

Responsable : Youssef  
Priorite : 1  
Obligatoire depot : yes

<figure class="capture">
  <img src="file:///C:/Users/Ivan/Pictures/PROJET%20M2/Annexes_Captures/CAP-03_alerte-5712-brute-force-ssh.png" alt="Wazuh alert detail 5712">
  <figcaption>Wazuh alert detail 5712</figcaption>
</figure>


### CAP-04 - Endpoint/SCA

Responsable : Youssef  
Priorite : 2  
Obligatoire depot : no

<figure class="capture">
  <img src="file:///C:/Users/Ivan/Pictures/PROJET%20M2/Annexes_Captures/CAP-04_source-endpoint-poste01-sca.png" alt="Windows endpoint or SCA screen">
  <figcaption>Windows endpoint or SCA screen</figcaption>
</figure>


### CAP-05 - Custom rules Daylight

Responsable : Youssef  
Priorite : 2  
Obligatoire depot : no

<figure class="capture">
  <img src="file:///C:/Users/Ivan/Pictures/PROJET%20M2/Annexes_Captures/CAP-05_daylight-alertes-metier.png" alt="Search results 100110-100150">
  <figcaption>Search results 100110-100150</figcaption>
</figure>


### CAP-06 - Patient data protection

Responsable : Kilyan  
Priorite : 1  
Obligatoire depot : yes

<figure class="capture">
  <img src="file:///C:/Users/Ivan/Pictures/PROJET%20M2/Annexes_Captures/CAP-06_alerte-100120-acces-patient.png" alt="Alert detail 100120">
  <figcaption>Alert detail 100120</figcaption>
</figure>


### CAP-07 - Dashboard analyste

Responsable : Kilyan  
Priorite : 1  
Obligatoire depot : yes

<figure class="capture">
  <img src="file:///C:/Users/Ivan/Pictures/PROJET%20M2/Annexes_Captures/CAP-07_dashboard-technique.png" alt="Technical dashboard severity/source/rules">
  <figcaption>Technical dashboard severity/source/rules</figcaption>
</figure>


### CAP-08 - Dashboard client

Responsable : Kilyan  
Priorite : 1  
Obligatoire depot : yes

<figure class="capture">
  <img src="file:///C:/Users/Ivan/Pictures/PROJET%20M2/Annexes_Captures/CAP-08_dashboard-executif.png" alt="Executive dashboard KPIs">
  <figcaption>Executive dashboard KPIs</figcaption>
</figure>


### CAP-09 - RBAC

Responsable : Youssef  
Priorite : 2  
Obligatoire depot : no

<figure class="capture">
  <img src="file:///C:/Users/Ivan/Pictures/PROJET%20M2/Annexes_Captures/CAP-09_rbac-analyste-lecture-seule.png" alt="Readonly analyst cannot access admin">
  <figcaption>Readonly analyst cannot access admin</figcaption>
</figure>


### CAP-10 - Playbook

Responsable : Mahamadou  
Priorite : 2  
Obligatoire depot : no

<figure class="capture">
  <img src="file:///C:/Users/Ivan/Pictures/PROJET%20M2/Annexes_Captures/CAP-10_playbook-brute-force.png" alt="PB-001 brute force opened">
  <figcaption>PB-001 brute force opened</figcaption>
</figure>


### CAP-11 - REX incident

Responsable : Mahamadou  
Priorite : 2  
Obligatoire depot : no

<figure class="capture">
  <img src="file:///C:/Users/Ivan/Pictures/PROJET%20M2/Annexes_Captures/CAP-11_rex-incident-acces-patient.png" alt="Incident REX section or filled template">
  <figcaption>Incident REX section or filled template</figcaption>
</figure>


### CAP-12 - Architecture

Responsable : Yvan  
Priorite : 2  
Obligatoire depot : no

<figure class="capture">
  <img src="file:///C:/Users/Ivan/Pictures/PROJET%20M2/Annexes_Captures/CAP-12_architecture-solution.png" alt="Architecture diagram">
  <figcaption>Architecture diagram</figcaption>
</figure>


### CAP-13 - Firewall/routeur concret

Responsable : Yvan  
Priorite : 1  
Obligatoire depot : yes

<figure class="capture">
  <img src="file:///C:/Users/Ivan/Pictures/PROJET%20M2/Annexes_Captures/CAP-13_pfsense-regles-firewall.png" alt="pfSense rules or CSV matrix">
  <figcaption>pfSense rules or CSV matrix</figcaption>
</figure>


### CAP-14 - Syslog firewall

Responsable : Yvan/Youssef  
Priorite : 2  
Obligatoire depot : no

<figure class="capture">
  <img src="file:///C:/Users/Ivan/Pictures/PROJET%20M2/Annexes_Captures/CAP-14_pfsense-syslog-wazuh.png" alt="pfSense remote logging to Wazuh">
  <figcaption>pfSense remote logging to Wazuh</figcaption>
</figure>


### CAP-15 - Automation lab

Responsable : Youssef  
Priorite : 2  
Obligatoire depot : no

<figure class="capture">
  <img src="file:///C:/Users/Ivan/Pictures/PROJET%20M2/Annexes_Captures/CAP-15_script-setup-siem-lab.png" alt="setup-siem-lab.ps1">
  <figcaption>setup-siem-lab.ps1</figcaption>
</figure>


### CAP-16 - Source SSH brute force

Responsable : Mahamadou  
Priorite : 2  
Obligatoire depot : no

<figure class="capture">
  <img src="file:///C:/Users/Ivan/Pictures/PROJET%20M2/Annexes_Captures/CAP-16_auth-log-serveur01.png" alt="auth.log or docker logs">
  <figcaption>auth.log or docker logs</figcaption>
</figure>


### CAP-17 - RBAC supervision

Responsable : Youssef  
Priorite : 2  
Obligatoire depot : no

<figure class="capture">
  <img src="file:///C:/Users/Ivan/Pictures/PROJET%20M2/Annexes_Captures/CAP-17_compte-supervision-dashboard.png" alt="Supervision profile dashboard">
  <figcaption>Supervision profile dashboard</figcaption>
</figure>


### CAP-18 - Reporting export

Responsable : Kilyan  
Priorite : 2  
Obligatoire depot : no

<figure class="capture">
  <img src="file:///C:/Users/Ivan/Pictures/PROJET%20M2/Annexes_Captures/CAP-18_export-dashboard-report.png" alt="Dashboard/report export">
  <figcaption>Dashboard/report export</figcaption>
</figure>


### CAP-19 - pfSense alerting

Responsable : Yvan/Youssef  
Priorite : 2  
Obligatoire depot : no

<figure class="capture">
  <img src="file:///C:/Users/Ivan/Pictures/PROJET%20M2/Annexes_Captures/CAP-19_wazuh-pfsense-alertes.png" alt="Wazuh alert 110010 or 110020">
  <figcaption>Wazuh alert 110010 or 110020</figcaption>
</figure>


### CAP-20 - Log replay

Responsable : Mahamadou  
Priorite : 2  
Obligatoire depot : no

<figure class="capture">
  <img src="file:///C:/Users/Ivan/Pictures/PROJET%20M2/Annexes_Captures/CAP-20_wazuh-rejeu-logs-demo.png" alt="Wazuh/dry-run log replay">
  <figcaption>Wazuh/dry-run log replay</figcaption>
</figure>


### CAP-21 - Dashboard queries

Responsable : Kilyan  
Priorite : 2  
Obligatoire depot : no

<figure class="capture">
  <img src="file:///C:/Users/Ivan/Pictures/PROJET%20M2/Annexes_Captures/CAP-21_dashboard-technique-requetes.png" alt="Technical query dashboard">
  <figcaption>Technical query dashboard</figcaption>
</figure>


### CAP-22 - Executive dashboard

Responsable : Kilyan  
Priorite : 2  
Obligatoire depot : no

<figure class="capture">
  <img src="file:///C:/Users/Ivan/Pictures/PROJET%20M2/Annexes_Captures/CAP-22_dashboard-executif-daylight.png" alt="Client dashboard">
  <figcaption>Client dashboard</figcaption>
</figure>


### CAP-23 - Alert qualification

Responsable : Kilyan  
Priorite : 2  
Obligatoire depot : no

<figure class="capture">
  <img src="file:///C:/Users/Ivan/Pictures/PROJET%20M2/Annexes_Captures/CAP-23_qualification-alerte-100120.png" alt="100120 qualification view">
  <figcaption>100120 qualification view</figcaption>
</figure>


### CAP-24 - Firewall alert qualification

Responsable : Kilyan  
Priorite : 2  
Obligatoire depot : no

<figure class="capture">
  <img src="file:///C:/Users/Ivan/Pictures/PROJET%20M2/Annexes_Captures/CAP-24_qualification-alerte-110020.png" alt="110020 qualification view">
  <figcaption>110020 qualification view</figcaption>
</figure>


### CAP-25 - Lab exploitation

Responsable : Mahamadou  
Priorite : 1  
Obligatoire depot : yes

<figure class="capture">
  <img src="file:///C:/Users/Ivan/Pictures/PROJET%20M2/Annexes_Captures/CAP-25_preflight-demo-ok.png" alt="preflight report after restart">
  <figcaption>preflight report after restart</figcaption>
</figure>


### CAP-26 - Containers

Responsable : Mahamadou  
Priorite : 2  
Obligatoire depot : no

> Capture/preuve manquante : `CAP-26_docker-conteneurs-lab.png`


### CAP-27 - Replay logs

Responsable : Mahamadou  
Priorite : 2  
Obligatoire depot : no

<figure class="capture">
  <img src="file:///C:/Users/Ivan/Pictures/PROJET%20M2/Annexes_Captures/CAP-27_rejeu-logs-dry-run.png" alt="dry-run output">
  <figcaption>dry-run output</figcaption>
</figure>


### CAP-28 - REX completed

Responsable : Mahamadou  
Priorite : 2  
Obligatoire depot : no

<figure class="capture">
  <img src="file:///C:/Users/Ivan/Pictures/PROJET%20M2/Annexes_Captures/CAP-28_rex-incident-rempli.png" alt="Filled REX example">
  <figcaption>Filled REX example</figcaption>
</figure>


## Lecture du statut

- `OK` signifie que l'image existe dans `Annexes_Captures/` et sera integree au PDF.
- `MANQUANT` signifie que la preuve doit encore etre capturee ou produite depuis le lab/document correspondant.
- Les images statiques generees depuis les fichiers de configuration sont admises uniquement quand la checklist les decrit comme preuve documentaire, par exemple la matrice pfSense.
- Aucune capture Wazuh n'est simulee : l'annexe reflete l'etat reel du dossier.
