# Recolección exclusiva de CCL durante la rueda (solo observación; sin órdenes ni claves).
#
#   powershell -ExecutionPolicy Bypass -File recolectar_ccl.ps1 [-Run ccl-20261015] [-Date 2026-10-15]
#
# Solo la fuente ccl (BYMA demorado, Nasdaq, data912): sin Polymarket ni futuros.
# Cada captura se guarda al tomarse (lab_data/ccl.sqlite). Si el proceso se corta,
# se reanuda desde la última captura válida (--resume). Al cerrar la ventana, termina.
# Sin -Run usa ccl-AAAAMMDD del día. Sábados y domingos no recolecta (no hay rueda).
# La tarea programada "PieAPie CCL" lo lanza los días hábiles y al iniciar sesión.
param(
    [string]$Run = "",
    [string]$Date = (Get-Date).ToString("yyyy-MM-dd"),
    [string]$Window = "11:00-17:05",
    [string]$Database = "lab_data/ccl.sqlite",
    [int]$MaxRestarts = 20
)
Set-Location $PSScriptRoot
$day = [datetime]::ParseExact($Date, "yyyy-MM-dd", $null)
if ($day.DayOfWeek -in @([DayOfWeek]::Saturday, [DayOfWeek]::Sunday)) { exit 0 }
if (-not $Run) { $Run = "ccl-" + $day.ToString("yyyyMMdd") }
$env:LAB_DB = $Database
$log = "lab_data\$Run.log"
for ($i = 0; $i -le $MaxRestarts; $i++) {
    # cmd /c: el log queda en el mismo texto que imprime Python (PowerShell 5.1 lo pasaría a UTF-16)
    cmd /c "python run_lab.py collect --resume --run $Run --sources ccl --ticks 420 --interval-sec 60 --window-art $Window --date-art $Date --max-rss-mb 300 >> $log 2>&1"
    $code = $LASTEXITCODE
    if ($code -eq 0) { break }        # ventana cerrada o capturas completas
    Add-Content -Encoding ASCII -Path $log -Value "$(Get-Date -Format s) supervisor: salida $code, reanudo en 30 s (intento $($i + 1))"
    Start-Sleep -Seconds 30
}
cmd /c "python run_lab.py verify-collect --run $Run --interval-sec 60 --sources ccl > lab_data\$Run.verify.json 2>&1"
