# Manifeste depot et integrite - Daylight / Cyber Trust

Ce manifeste sert de controle final lisible par le groupe avant depot. Il liste l'etat reel du dossier, les pieces critiques et les empreintes SHA-256 utiles pour verifier qu'un fichier n'a pas ete modifie.

## Etat synthetique

- Statut : `pret_structurellement_avec_preuves_reelles_restantes`
- Generation : `2026-06-23T20:00:15`
- PDF detectes : `40`
- Pages du dossier groupe complet : `93`
- Captures CAP-*.png : `27`
- Captures prioritaires presentes : `8/8`
- Video prete : `non`
- Fichiers hashes dans `MANIFEST_DEPOT.json` : `186`

## Points restants avant depot officiel

- Lien YouTube non repertorie ou MP4 final absent : PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_video-lien.txt

## Captures prioritaires

| Capture | Responsable | Preuve attendue | Etat |
|---|---|---|---|
| `CAP-01_wazuh-dashboard-login.png` | Youssef | Wazuh accessible | presente |
| `CAP-02_agents-poste01-serveur01.png` | Youssef | Collecte multi-source | presente |
| `CAP-03_alerte-5712-brute-force-ssh.png` | Youssef | Detection brute force SSH | presente |
| `CAP-06_alerte-100120-acces-patient.png` | Kilyan | Patient data protection | presente |
| `CAP-07_dashboard-technique.png` | Kilyan | Dashboard analyste | presente |
| `CAP-08_dashboard-executif.png` | Kilyan | Dashboard client | presente |
| `CAP-13_pfsense-regles-firewall.png` | Yvan | Firewall/routeur concret | presente |
| `CAP-25_preflight-demo-ok.png` | Mahamadou | Lab exploitation | presente |

## Pieces critiques et empreintes

| Piece | Taille | SHA-256 court |
|---|---:|---|
| `Rendus_PDF/PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_DossierGroupeComplet.pdf` | 16641441 | `7cebb4e0e6efbcb8` |
| `Rendus_PDF/PE-2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA_RapportGroupe.pdf` | 1325067 | `02f6f8fce281eeed` |
| `Presentation_Daylight_CyberTrust.pptx` | 30175 | `f8270543508bd0eb` |
| `Rendus_PDF/16_ANNEXE_CAPTURES_WAZUH.pdf` | 1452551 | `24ecafac502e572f` |
| `Rendus_PDF/18_SOLUTIONS_CONCRETES_DEMO.pdf` | 777768 | `02a7c632952cf3cc` |
| `Rendus_PDF/20_MODE_OPERATOIRE_PFSENSE_WAZUH_LAB.pdf` | 942221 | `668b9318bb3674a1` |
| `Rendus_PDF/21_DASHBOARDS_ALERTES_QUALIFICATION.pdf` | 740199 | `e7f0c0807c7590cf` |
| `Rendus_PDF/24_DASHBOARD_SOC_OFFLINE.pdf` | 408524 | `ffac01958bb252eb` |
| `Rendus_PDF/25_MODE_OPERATOIRE_CAPTURE_WAZUH_PREUVES.pdf` | 681913 | `4e25a8b5dd9d5131` |
| `Rendus_PDF/26_MODE_OPERATOIRE_VIDEO_DEPOT.pdf` | 595056 | `591d3d4e846b196c` |
| `Rendus_PDF/27_MANIFESTE_DEPOT_ET_INTEGRITE.pdf` | 318121 | `7a30ffe87ff1f622` |
| `Rendus_PDF/28_RUNBOOK_EXPRESS_PREUVES_RESTANTES.pdf` | 511329 | `c78d14ad766e10d6` |
| `Rendus_PDF/29_IMPORT_PREUVES_FINALES.pdf` | 368807 | `8402cf2e8befe92c` |
| `Rendus_PDF/30_TABLEAU_BORD_STATUT_FINAL.pdf` | 240742 | `b90d21f9d83e7be6` |
| `README_LIVRABLES.md` | 13362 | `a97a0501030110ea` |
| `tools/post_capture_finalize.ps1` | 5312 | `75716876d010224a` |
| `tools/import_final_evidence.ps1` | 5169 | `5306d949da1c5663` |
| `tools/build_final_evidence_dashboard.py` | 9648 | `ff634e0c9a373206` |
| `tools/build_demo_control_center.py` | 18665 | `a55947d815f6f82c` |
| `tools/open_demo_control_center.ps1` | 2025 | `845517ce058b611e` |
| `tools/repair_lab_and_capture_cap25.ps1` | 9063 | `46b7ccec032f981a` |
| `Dashboards_Offline/daylight_demo_control_center.html` | 14797 | `a03f6f86d57b3e14` |
| `Dashboards_Offline/daylight_video_overlays.html` | 2687 | `649925aba7153851` |
| `Video_Overlays/README_VIDEO_OVERLAYS.md` | 1010 | `f97d2277ab97a65c` |
| `Video_Overlays/overlay_yvan_focsa.png` | 26646 | `c8b3c242059266fc` |
| `Video_Overlays/overlay_youssef_guerniou.png` | 29516 | `a4948a6e5f6f9ca3` |
| `Video_Overlays/overlay_kilyan_felix.png` | 24678 | `d9b0d06a17134709` |
| `Video_Overlays/overlay_mahamadou_diacoumba.png` | 31433 | `8cf5f50e41e1e1c6` |

## Verification recommandee

```powershell
python .\tools\build_delivery_manifest.py
Get-FileHash -Algorithm SHA256 .\PE_2526_M2CS_FOCSA_GUERNIOU_FELIX_DIACOUMBA.zip
```

Le fichier `MANIFEST_DEPOT.json` contient la liste complete des fichiers hashes. Le hash final du ZIP est conserve dans le fichier `.sha256` adjacent apres reconstruction de l'archive.
