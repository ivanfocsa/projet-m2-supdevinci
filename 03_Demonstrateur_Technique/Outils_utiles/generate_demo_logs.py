from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Demo_Logs"


FILES: dict[str, list[str]] = {
    "pfsense.log": [
        "2026-06-23T09:14:02+02:00 pfsense-fw-01 filterlog: action=block interface=WAN src=45.155.205.12 src_zone=Internet dst=203.0.113.10 dst_zone=WAN proto=tcp dst_port=22 rule=20 msg=\"WAN scan blocked\"",
        "2026-06-23T09:15:17+02:00 pfsense-fw-01 filterlog: action=block interface=USERS src=10.10.10.54 src_zone=USERS dst=10.10.40.12 dst_zone=MGMT proto=tcp dst_port=443 rule=130 msg=\"User VLAN to management denied\"",
        "2026-06-23T09:16:41+02:00 pfsense-fw-01 filterlog: action=pass interface=WAN src=198.51.100.22 src_zone=Internet dst=10.10.30.20 dst_zone=DMZ proto=tcp dst_port=443 rule=40 msg=\"HTTPS to Daylight portal\"",
        "2026-06-23T09:18:09+02:00 pfsense-fw-01 event=vpn_login user=yvan.focsa src=198.51.100.50 result=success mfa=true",
        "2026-06-23T09:20:32+02:00 pfsense-fw-01 filterlog: action=pass interface=SERVERS src=10.10.20.30 src_zone=SERVERS dst=91.199.212.40 dst_zone=Internet proto=tcp dst_port=443 bytes=84233121 tag=WAN_EXFIL_DEMO msg=\"High outbound transfer demo\"",
    ],
    "daylight_app.log": [
        "2026-06-23T09:22:05+02:00 daylight-app-01 DAYLIGHT_APP event=auth_failure user=alice.martin src=10.10.10.54 count=7 result=blocked",
        "2026-06-23T09:24:11+02:00 daylight-app-01 DAYLIGHT_APP event=patient_record_access user=stagiaire.demo patient_id=DL-PT-88421 center=Lyon risk=high reason=\"access outside role\"",
        "2026-06-23T09:25:42+02:00 daylight-app-01 DAYLIGHT_APP event=appointment_export user=claire.bernard count=42 center=Nantes risk=medium",
        "2026-06-23T09:28:03+02:00 daylight-app-01 DAYLIGHT_APP event=auth_success user=youssef.guerniou src=10.10.40.21 role=soc_admin",
    ],
    "ad_files.log": [
        "2026-06-23T09:31:44+02:00 daylight-ad-01 DAYLIGHT_AD event=privileged_group_change actor=svc-temp target=Domain Admins action=add_member member=helpdesk.demo risk=critical",
        "2026-06-23T09:33:18+02:00 daylight-files-01 DAYLIGHT_FILES event=patient_share_access user=stagiaire.demo path=\\\\daylight-files-01\\patients\\lyon\\2026 result=denied risk=high",
        "2026-06-23T09:35:59+02:00 daylight-ad-01 DAYLIGHT_AD event=password_spray source=10.10.10.54 failures=18 window=5m risk=high",
    ],
    "mail_phishing.log": [
        "2026-06-23T09:40:27+02:00 daylight-mail-01 DAYLIGHT_MAIL event=phishing_reported user=accueil.lyon sender=billing-update@example.net subject=\"Facture mutuelle urgente\" attachment=invoice.html risk=high",
        "2026-06-23T09:41:52+02:00 daylight-mail-01 DAYLIGHT_MAIL event=url_rewrite_click user=accueil.lyon url=http://example.net/login verdict=blocked risk=medium",
    ],
    "endpoint_usb.log": [
        "2026-06-23T09:45:01+02:00 poste-01 DAYLIGHT_ENDPOINT event=usb_insert user=stagiaire.demo device_id=USBSTOR-VID_0951 authorized=false risk=high",
        "2026-06-23T09:45:33+02:00 poste-01 DAYLIGHT_ENDPOINT event=process_start user=stagiaire.demo image=C:\\Users\\Public\\invoice_viewer.exe signer=unknown risk=medium",
    ],
}


README = """# Demo logs Daylight / Cyber Trust

Ces fichiers sont des logs de demonstration, crees pour montrer les sources que le SOC Cyber Trust collecte et correle.

## Fichiers generes

| Fichier | Source simulee |
|---|---|
| `pfsense.log` | Firewall pfSense, VLAN, WAN, VPN. |
| `daylight_app.log` | Application metier Daylight. |
| `ad_files.log` | Annuaire et serveur fichiers. |
| `mail_phishing.log` | Messagerie et phishing. |
| `endpoint_usb.log` | Endpoint et support USB. |

## Usage

1. Les ouvrir pendant la video pour montrer les evenements bruts.
2. Les envoyer vers Wazuh via syslog ou un agent si le lab est disponible.
3. Les rapprocher des regles `config/wazuh/local_rules_daylight_pfsense.xml`.

Ces logs ne remplacent pas les captures Wazuh finales demandees dans `Annexes_Captures/`.
"""


def main() -> int:
    OUT.mkdir(exist_ok=True)
    for filename, lines in FILES.items():
        (OUT / filename).write_text("\n".join(lines) + "\n", encoding="utf-8")
    (OUT / "README.md").write_text(README, encoding="utf-8")

    print(f"Logs de demonstration generes dans : {OUT}")
    for filename in FILES:
        print(f"- {OUT / filename}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
