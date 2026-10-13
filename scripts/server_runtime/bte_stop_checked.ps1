param([Parameter(Mandatory=$true)][string]$BteRoot)
$ErrorActionPreference = 'Stop'
try {
    $BteRoot = (Resolve-Path -LiteralPath $BteRoot).Path
    $BtePython = Join-Path $BteRoot '.venv\Scripts\python.exe'
    $BteTargets = @{8000='applications.api.app:app';8686='applications.customer_portal.app:app'}
    $BteReport = Join-Path $BteRoot 'logs\BTE_Khoi_Dong_Da_Kiem_Tra.json'
    if (Test-Path -LiteralPath $BteReport) {
        $BteState = Get-Content -LiteralPath $BteReport -Raw -Encoding UTF8 | ConvertFrom-Json
        if ($BteState.root -ne $BteRoot) { throw 'Startup report belongs to a different BTE folder.' }
        $BteTargets = @{}
        $BteTargets[[int]$BteState.api_port] = 'applications.api.app:app'
        $BteTargets[[int]$BteState.portal_port] = 'applications.customer_portal.app:app'
    }
    $BtePlans = @()
    foreach ($BtePort in $BteTargets.Keys) {
        $BteListeners = @(Get-NetTCPConnection -State Listen -ErrorAction Stop | Where-Object { $_.LocalPort -eq $BtePort })
        foreach ($BteProcessId in @($BteListeners.OwningProcess | Select-Object -Unique)) {
            if (-not $BteProcessId) { continue }
            $BteProcess = Get-CimInstance Win32_Process -Filter "ProcessId=$BteProcessId"
            if (-not $BteProcess) { continue }
            $BteCommand = [string]$BteProcess.CommandLine
            $BteOwnedExecutable = ([string]$BteProcess.ExecutablePath -ieq $BtePython) -or ($BteCommand.IndexOf($BtePython, [StringComparison]::OrdinalIgnoreCase) -ge 0)
            $BteOwnedModule = $BteCommand -match [regex]::Escape($BteTargets[$BtePort])
            $BteUvicorn = $BteCommand -match '(?i)\s-m\s+uvicorn\s'
            if (-not ($BteOwnedExecutable -and $BteOwnedModule -and $BteUvicorn)) {
                throw "Port $BtePort is held by PID $BteProcessId that cannot be verified as this BTE. Nothing will be stopped."
            }
            $BtePlans += [pscustomobject]@{Id=$BteProcessId;Port=$BtePort;Module=$BteTargets[$BtePort];Created=$BteProcess.CreationDate}
        }
    }
    # Validate every target before stopping any of them. Recheck PID reuse.
    foreach ($BtePlan in $BtePlans) {
        $BteCurrent = Get-CimInstance Win32_Process -Filter "ProcessId=$($BtePlan.Id)"
        if (-not $BteCurrent) { continue }
        if ($BteCurrent.CreationDate -ne $BtePlan.Created) { throw 'A process ID changed during validation. Please run again.' }
        Write-Output "Stopping verified BTE PID $($BtePlan.Id), port $($BtePlan.Port), module $($BtePlan.Module)."
        Stop-Process -Id $BtePlan.Id -ErrorAction Stop
    }
    $BteDeadline = (Get-Date).AddSeconds(10)
    do {
        $BteRemaining = @(Get-NetTCPConnection -State Listen -ErrorAction Stop | Where-Object { $BteTargets.ContainsKey([int]$_.LocalPort) })
        if ($BteRemaining.Count -eq 0) { break }
        Start-Sleep -Milliseconds 300
    } while ((Get-Date) -lt $BteDeadline)
    if ($BteRemaining.Count -ne 0) { throw 'A BTE port is still occupied. Startup has been cancelled.' }
    Write-Output 'STOP_OK: API and Portal ports are free. No account or chart data was changed.'
    exit 0
} catch {
    Write-Output ('STOP_FAILED: ' + $_.Exception.Message)
    exit 1
}
