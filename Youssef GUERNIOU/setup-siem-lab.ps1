# =====================================================================
#  setup-siem-lab.ps1  --  Perimetre Ingenieur SIEM (Youssef GUERNIOU)
# ---------------------------------------------------------------------
#  Reproduit en UNE commande la partie SIEM du lab SOC :
#    1. serveur-01  : conteneur Linux + agent Wazuh + SSH/rsyslog
#                     + fix auth.log + test SSH (alertes 5710/5503/5551/5763,
#                       et 5712 selon version/correlation Wazuh)
#    2. RBAC        : utilisateurs supervision / analyste + role
#                     lecture seule "soc_readonly" + mapping
#    3. (optionnel) : source applicative Daylight via les scripts npm
#
#  PREREQUIS : Docker Desktop lance + lab Wazuh demarre
#              (npm run lab:start). A lancer depuis la racine du projet.
#
#  USAGE :     .\Youssef GUERNIOU\setup-siem-lab.ps1
# =====================================================================

$ErrorActionPreference = "Stop"
$serverContainer  = "serveur-01"
$indexerContainer = "single-node-wazuh.indexer-1"

function Write-Step($msg) { Write-Host "`n=== $msg ===" -ForegroundColor Cyan }

# ---------------------------------------------------------------------
# 0. Verification Docker
# ---------------------------------------------------------------------
try { docker info | Out-Null }
catch {
    Write-Host "[X] Docker ne repond pas. Lance Docker Desktop puis reessaie." -ForegroundColor Red
    exit 1
}

# ---------------------------------------------------------------------
# 1. serveur-01  (source 2 : serveur Linux simule)
# ---------------------------------------------------------------------
Write-Step "1/3  Serveur simule serveur-01"

$exists = docker ps -a --format '{{.Names}}' | Select-String -Pattern "^$serverContainer$"
if ($exists) {
    Write-Host "[*] $serverContainer existe deja -> demarrage." -ForegroundColor Yellow
    docker start $serverContainer | Out-Null
} else {
    Write-Host "[*] Creation du conteneur $serverContainer (Ubuntu 22.04)..." -ForegroundColor Green
    docker run -d --name $serverContainer --hostname $serverContainer ubuntu:22.04 sleep infinity | Out-Null
}

$serverBash = @'
#!/usr/bin/env bash
AGENT_VERSION="4.14.5-1"
DEB="wazuh-agent_${AGENT_VERSION}_amd64.deb"
MANAGER="host.docker.internal"
NAME="serveur-01"

echo "[*] Mise a jour des paquets..."
apt-get update -qq

echo "[*] Installation des prerequis systeme..."
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq wget ca-certificates gnupg openssh-server openssh-client rsyslog sshpass passwd

echo "[*] Telechargement de l'agent Wazuh ${AGENT_VERSION}..."
cd /tmp
wget -q -O "${DEB}" "https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/${DEB}"

echo "[*] Installation de l'agent (manager=${MANAGER})..."
WAZUH_MANAGER="$MANAGER" WAZUH_AGENT_NAME="$NAME" dpkg -i "./${DEB}" || true

echo "[*] Resolution des dependances (python3, lsb-release)..."
apt-get -y -qq --fix-broken install
WAZUH_MANAGER="$MANAGER" WAZUH_AGENT_NAME="$NAME" dpkg --configure -a || true

echo "[*] Preparation SSH et utilisateur de test..."
mkdir -p /run/sshd
if ! id daylightadmin >/dev/null 2>&1; then
  useradd -m -s /bin/bash daylightadmin
  echo "daylightadmin:Daylight2026!" | chpasswd
fi

echo "[*] Ajout du suivi de /var/log/auth.log (si absent)..."
if ! grep -q "/var/log/auth.log" /var/ossec/etc/ossec.conf; then
cat >> /var/ossec/etc/ossec.conf <<'CONF'
<ossec_config>
  <localfile>
    <log_format>syslog</log_format>
    <location>/var/log/auth.log</location>
  </localfile>
</ossec_config>
CONF
  echo "    -> directive ajoutee."
else
  echo "    -> deja present."
fi

echo "[*] Demarrage des services..."
rsyslogd 2>/dev/null || true
service ssh start
/var/ossec/bin/wazuh-control restart
sleep 5

echo "[*] Simulation SSH : utilisateur inexistant + mauvais mot de passe..."
for i in $(seq 1 8); do
  sshpass -p wrong ssh -o StrictHostKeyChecking=no -o ConnectTimeout=3 hacker@localhost true 2>/dev/null || true
done
for i in $(seq 1 8); do
  sshpass -p wrong ssh -o StrictHostKeyChecking=no -o ConnectTimeout=3 daylightadmin@localhost true 2>/dev/null || true
done
NB=$(grep -c "Failed password" /var/log/auth.log 2>/dev/null || echo 0)
echo "[OK] $NB echecs d'authentification ecrits dans auth.log."
echo "[OK] Alertes Wazuh attendues : 5710 utilisateur inexistant, 5503 echec PAM, 5551/5763 brute force, 5712 possible selon version."
'@

$serverBash = $serverBash -replace "`r`n", "`n"
$tmp1 = Join-Path $env:TEMP "setup-serveur-01.sh"
[IO.File]::WriteAllText($tmp1, $serverBash)
docker cp $tmp1 "${serverContainer}:/tmp/setup-serveur-01.sh" | Out-Null
docker exec $serverContainer bash /tmp/setup-serveur-01.sh

# ---------------------------------------------------------------------
# 2. RBAC  (vues supervision / analyste / admin)
# ---------------------------------------------------------------------
Write-Step "2/3  RBAC : utilisateurs + role lecture seule"

$rbacBash = @'
#!/usr/bin/env bash
IDX="https://localhost:9200"
AUTH="admin:SecretPassword"

echo "[*] Utilisateur supervision..."
curl -k -s -u "$AUTH" -X PUT "$IDX/_plugins/_security/api/internalusers/supervision" \
  -H 'Content-Type: application/json' \
  -d '{"password":"CTView2026!Blue"}'; echo

echo "[*] Utilisateur analyste..."
curl -k -s -u "$AUTH" -X PUT "$IDX/_plugins/_security/api/internalusers/analyste" \
  -H 'Content-Type: application/json' \
  -d '{"password":"CTRead2026!Blue"}'; echo

echo "[*] Role lecture seule soc_readonly..."
curl -k -s -u "$AUTH" -X PUT "$IDX/_plugins/_security/api/roles/soc_readonly" \
  -H 'Content-Type: application/json' \
  -d '{"cluster_permissions":["cluster_composite_ops_ro","cluster_monitor"],"index_permissions":[{"index_patterns":["wazuh-*"],"allowed_actions":["read","indices_monitor"]},{"index_patterns":[".kibana*"],"allowed_actions":["read"]}],"tenant_permissions":[{"tenant_patterns":["global_tenant"],"allowed_actions":["kibana_all_read"]}]}'; echo

echo "[*] Mapping supervision + analyste -> soc_readonly..."
curl -k -s -u "$AUTH" -X PUT "$IDX/_plugins/_security/api/rolesmapping/soc_readonly" \
  -H 'Content-Type: application/json' \
  -d '{"users":["analyste","supervision"]}'; echo

echo "[OK] RBAC configure : admin (complet) / analyste + supervision (lecture seule)."
'@

$rbacBash = $rbacBash -replace "`r`n", "`n"
$tmp2 = Join-Path $env:TEMP "setup-rbac.sh"
[IO.File]::WriteAllText($tmp2, $rbacBash)
docker cp $tmp2 "${indexerContainer}:/tmp/setup-rbac.sh" | Out-Null
docker exec $indexerContainer bash /tmp/setup-rbac.sh

# ---------------------------------------------------------------------
# 3. (optionnel) Source applicative Daylight via les scripts npm
# ---------------------------------------------------------------------
Write-Step "3/3  Source applicative Daylight (optionnel)"
if (Test-Path ".\package.json") {
    try {
        npm run generate:logs
        npm run lab:deploy-daylight
        Start-Sleep -Seconds 45
        npm run lab:replay-daylight
        Write-Host "[OK] Logs Daylight integres (alertes 100100-100140)." -ForegroundColor Green
    } catch {
        Write-Host "[!] Etape Daylight ignoree (a lancer manuellement : npm run generate:logs / lab:deploy-daylight / lab:replay-daylight)." -ForegroundColor Yellow
    }
} else {
    Write-Host "[!] package.json introuvable : lance ce script depuis la racine du projet pour l'etape Daylight." -ForegroundColor Yellow
}

# ---------------------------------------------------------------------
Write-Host "`n=== TERMINE ===" -ForegroundColor Cyan
Write-Host "Dashboard : https://localhost   (admin / SecretPassword)" -ForegroundColor Cyan
Write-Host "Comptes RBAC : analyste / CTRead2026!Blue   -   supervision / CTView2026!Blue" -ForegroundColor Cyan
Write-Host "Verifie : Agents (poste-01, serveur-01 Active) + alertes SSH 5710/5503/5551/5763 et 100120." -ForegroundColor Cyan
