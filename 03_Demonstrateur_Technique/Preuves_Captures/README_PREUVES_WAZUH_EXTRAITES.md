# Preuves Wazuh extraites

Ces captures proviennent de `Youssef GUERNIOU/Documentation_SIEM_Youssef_GUERNIOU.pdf`.
Elles ne remplacent pas une nouvelle capture live si le lab Wazuh est disponible, mais elles isolent des preuves deja presentes dans la documentation SIEM.

- `CAP-01` : session Wazuh authentifiee, utilisee comme preuve d'acces dashboard.
- `CAP-02` : planche multi-source endpoint / serveur / application Daylight.
- `CAP-03` : alerte SSH brute force `5712` sur `serveur-01`.

Commande de regeneration :

```powershell
python .\tools\extract_youssef_wazuh_proofs.py
```
