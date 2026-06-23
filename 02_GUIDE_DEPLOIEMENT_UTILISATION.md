# Guide de deploiement et d'utilisation - SOC Daylight

## Objectif

Ce guide explique comment preparer, lancer et verifier le demonstrateur SOC Cyber Trust pour Daylight. Il s'appuie sur le perimetre SIEM deja documente par Youssef GUERNIOU et sur le script `Youssef GUERNIOU/setup-siem-lab.ps1`.

## Prerequis

| Prerequis | Utilite |
|---|---|
| Windows avec droits administrateur | Execution Docker, agents et scripts. |
| Docker Desktop lance | Conteneurs Wazuh et serveur Linux simule. |
| PowerShell | Execution du script de preparation SIEM. |
| Navigateur web | Acces a Wazuh Dashboard. |
| npm | Optionnel, si le lab applicatif Daylight est disponible. |

## Composants attendus

| Nom | Type | Role |
|---|---|---|
| `single-node-wazuh.manager-1` | Conteneur | Analyse et gestion Wazuh. |
| `single-node-wazuh.indexer-1` | Conteneur | Indexation et stockage. |
| Wazuh Dashboard | Interface web | Consultation alertes et dashboards. |
| `poste-01` | Agent endpoint | Source poste Windows. |
| `serveur-01` | Conteneur Ubuntu | Source serveur Linux, SSH, auth.log. |
| Daylight logs | Source applicative | CRM, RDV, dossiers patients. |

## Lancement standard

Depuis la racine technique du lab Wazuh, lancer les commandes de demarrage prevues par ce lab. Si cette racine contient un `package.json`, utiliser :

```powershell
npm run lab:bootstrap
npm run lab:start
```

Dans la racine actuelle du rendu (`C:\Users\Ivan\Pictures\PROJET M2`), aucun `package.json` n'est attendu : on y lance les scripts de controle et de packaging, pas le demarrage npm du lab.

Puis executer le script SIEM :

```powershell
.\Youssef GUERNIOU\setup-siem-lab.ps1
```

Le script realise :

1. verification Docker ;
2. creation ou demarrage du conteneur `serveur-01` ;
3. installation de l'agent Wazuh sur le serveur simule ;
4. installation SSH et rsyslog ;
5. suivi de `/var/log/auth.log` ;
6. simulation d'une brute force SSH ;
7. creation des comptes RBAC `analyste` et `supervision` ;
8. creation du role `soc_readonly` ;
9. tentative d'integration des logs Daylight si `package.json` est present.

## Acces a l'interface

| Profil | Identifiant | Mot de passe | Usage |
|---|---|---|---|
| Admin | `admin` | `SecretPassword` | Administration complete. |
| Analyste | `analyste` | `Analyste2026!SOC` | Lecture alertes et dashboards. |
| Supervision | `supervision` | `Supervision2026!SOC` | Lecture reporting et vues de supervision. |

URL attendue :

```text
https://localhost
```

## Verification des sources

Dans Wazuh Dashboard, verifier les agents et evenements suivants :

| Source | Verification |
|---|---|
| `poste-01` | Agent actif, evenements endpoint, SCA CIS Windows 11. |
| `serveur-01` | Agent actif, evenements SSH, logs `auth.log`. |
| Daylight | Alertes metier, regles `100110`, `100120`, `100130`, `100140`. |

## Scenarios de test

### Brute force SSH

Le script declenche 15 tentatives SSH invalides contre `serveur-01`. L'alerte attendue est :

```text
5712 - sshd: brute force
```

Preuves a capturer :

- detail de l'alerte ;
- niveau de severite ;
- source `serveur-01` ;
- extrait ou compteur d'echecs dans `/var/log/auth.log`.

### Acces anormal dossier patient

Le scenario Daylight doit produire une alerte :

```text
100120 - acces anormal dossier patient
```

Preuves a capturer :

- utilisateur concerne ;
- patient ou dossier cible si simule ;
- site Daylight ;
- horodatage ;
- qualification critique.

### Modification de privilege

Alerte attendue :

```text
100130 - modification groupe privilegie
```

Preuves a capturer :

- compte modifie ;
- groupe concerne ;
- source ;
- decision d'escalade.

## Procedure de redemarrage apres extinction

Les services dans les conteneurs ne redemarrent pas tous automatiquement. Procedure :

```powershell
# Depuis la racine technique du lab Wazuh, si package.json existe :
npm run lab:start

# Puis revenir dans ce dossier projet :
cd "C:\Users\Ivan\Pictures\PROJET M2"
docker start serveur-01
docker exec -it serveur-01 bash
```

Dans le conteneur :

```bash
rsyslogd
service ssh start
/var/ossec/bin/wazuh-control start
exit
```

Puis verifier dans Wazuh :

- agent `serveur-01` actif ;
- dashboard accessible ;
- nouvelles alertes visibles.

## Utilisation quotidienne SOC

1. Ouvrir le dashboard technique.
2. Filtrer sur les alertes critiques et hautes.
3. Qualifier selon la matrice de severite.
4. Ouvrir une fiche incident si l'alerte est confirmee.
5. Appliquer le playbook correspondant.
6. Documenter les preuves, actions et decisions.
7. Mettre a jour le REX si l'incident est clos.

## Points de controle avant soutenance

| Controle | Statut attendu |
|---|---|
| Wazuh Dashboard accessible | OK |
| Compte admin fonctionnel | OK |
| Compte analyste lecture seule | OK |
| Compte supervision lecture seule | OK |
| Agent `poste-01` visible | OK |
| Agent `serveur-01` visible | OK |
| Alertes Daylight visibles | OK |
| Dashboard technique charge | OK |
| Dashboard executif charge | OK |
| Captures integrees au rapport | A faire avant export PDF |


