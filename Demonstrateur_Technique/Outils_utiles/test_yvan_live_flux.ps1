param(
    [string]$PfsenseLanIp = "10.10.40.1",
    [string]$SensitiveServerIp = "10.10.20.20",
    [string]$SyslogHost = "127.0.0.1",
    [int]$SyslogPort = 514,
    [switch]$SendSyslog
)

$ErrorActionPreference = "Continue"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$syslogScript = Join-Path $repoRoot "Demonstrateur_Technique\Outils_utiles\send_demo_logs_to_syslog.py"

function Write-Section {
    param([string]$Title)
    Write-Host ""
    Write-Host "=== $Title ===" -ForegroundColor Cyan
}

function Test-TcpQuick {
    param(
        [string]$HostName,
        [int]$Port,
        [int]$TimeoutMs = 3000
    )
    try {
        $client = New-Object System.Net.Sockets.TcpClient
        $async = $client.BeginConnect($HostName, $Port, $null, $null)
        $ok = $async.AsyncWaitHandle.WaitOne($TimeoutMs, $false)
        if ($ok -and $client.Connected) {
            $client.EndConnect($async)
            $client.Close()
            return $true
        }
        $client.Close()
        return $false
    } catch {
        return $false
    }
}

Write-Section "1. Interfaces locales utiles"
Get-NetIPAddress -AddressFamily IPv4 |
    Where-Object { $_.IPAddress -like "10.10.*" -or $_.IPAddress -like "192.168.*" } |
    Select-Object InterfaceAlias, IPAddress, PrefixLength |
    Format-Table -AutoSize

Write-Section "2. Test interface pfSense HTTPS"
$pfsense443 = Test-TcpQuick -HostName $PfsenseLanIp -Port 443
if ($pfsense443) {
    Write-Host "[OK] pfSense repond en HTTPS sur ${PfsenseLanIp}:443" -ForegroundColor Green
} else {
    Write-Host "[WARN] pfSense ne repond pas en HTTPS sur ${PfsenseLanIp}:443" -ForegroundColor Yellow
    Write-Host "A verifier avant video : VM pfSense demarree, interface LAN sur VMnet1, IP LAN $PfsenseLanIp."
}

Write-Section "3. Test ICMP pfSense"
& "$env:SystemRoot\System32\ping.exe" -n 2 $PfsenseLanIp
Write-Host "Note : l'echec ICMP n'est pas bloquant si HTTPS fonctionne. Il peut simplement etre filtre."

Write-Section "4. Test flux vers zone sensible"
$server445 = Test-TcpQuick -HostName $SensitiveServerIp -Port 445
if ($server445) {
    Write-Host "[WARN] Le port 445 repond sur $SensitiveServerIp. Pour la demo segmentation, ce flux devrait etre controle." -ForegroundColor Yellow
} else {
    Write-Host "[OK] Le flux vers ${SensitiveServerIp}:445 ne repond pas. C'est coherent avec le blocage lateral attendu." -ForegroundColor Green
}

Write-Section "5. Docker / Wazuh"
try {
    $dockerOutput = docker ps --format "{{.Names}} | {{.Status}} | {{.Ports}}" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[WARN] Docker ne repond pas. Lancer Docker Desktop puis le lab Wazuh avant la demo live." -ForegroundColor Yellow
    } elseif ($dockerOutput) {
        $dockerOutput
    } else {
        Write-Host "[INFO] Docker repond mais aucun conteneur actif n'est liste."
    }
} catch {
    Write-Host "[WARN] Docker indisponible. Utiliser les captures Wazuh si le lab n'est pas lance." -ForegroundColor Yellow
}

Write-Section "6. Rejeu logs pfSense"
if ($SendSyslog) {
    Write-Host "Envoi des logs pfsense.log vers ${SyslogHost}:$SyslogPort en UDP..."
    python $syslogScript --host $SyslogHost --port $SyslogPort --protocol udp --file pfsense.log
} else {
    Write-Host "Dry-run, aucun envoi reseau. Ajouter -SendSyslog pour envoyer vers Wazuh."
    python $syslogScript --file pfsense.log --dry-run
}

Write-Section "7. Requete Wazuh a montrer"
Write-Host "rule.id:110010 OR rule.id:110020 OR pfsense-fw-01"
Write-Host ""
Write-Host "Phrase video : la chaine attendue est regle pfSense -> log firewall -> syslog UDP 514 -> alerte Wazuh."
