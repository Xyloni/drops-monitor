$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $projectRoot

$python = Join-Path $projectRoot ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $python)) {
    python -m venv .venv
}
if (-not (Test-Path -LiteralPath $python)) {
    throw "Не удалось создать виртуальное окружение Python."
}

& $python -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw "Не удалось установить зависимости сборки." }

& $python -m PyInstaller `
    --noconfirm `
    --clean `
    --onefile `
    --windowed `
    --name "DropsMonitor" `
    --distpath "dist" `
    --icon "assets\icons\drops-monitor.ico" `
    --add-data "index.html;." `
    --add-data "assets;assets" `
    "desktop\main.py"
if ($LASTEXITCODE -ne 0) { throw "Сборка DropsMonitor.exe завершилась с ошибкой." }

Write-Host "Готово: $projectRoot\dist\DropsMonitor.exe"
