# Captura de precios cambiarios ejecutables (solo lectura de APIs públicas; sin órdenes ni claves).
#
#   powershell -ExecutionPolicy Bypass -File recolectar_fx.ps1 [-Start 10:00] [-Until 15:05]
#
# Escribe lab_data/fx_ar/fx-AAAAMMDD.jsonl (una captura por minuto). Si se relanza el mismo
# día (reinicio de la notebook), sigue agregando al mismo archivo; los minutos sin captura
# quedan como faltantes, no se rellenan. Sábados y domingos no captura.
# La tarea programada "PieAPie FX" lo lanza los días hábiles y al iniciar sesión.
param(
    [string]$Start = "10:00",
    [string]$Until = "15:05",
    [int]$IntervalSec = 60
)
Set-Location $PSScriptRoot
$now = Get-Date
if ($now.DayOfWeek -in @([DayOfWeek]::Saturday, [DayOfWeek]::Sunday)) { exit 0 }
$stamp = $now.ToString("yyyyMMdd")
New-Item -ItemType Directory -Force "lab_data\fx_ar" | Out-Null
$out = "lab_data\fx_ar\fx-$stamp.jsonl"
$log = "lab_data\fx_ar\capture-$stamp.log"
$startArg = $now.ToString("yyyy-MM-dd") + "T" + $Start     # antes de la hora de inicio, espera
cmd /c "python -X utf8 -m lab.research.fx_capture $out $Until $IntervalSec $startArg >> $log 2>&1"
