<div align="center">

<img src="assets/icons/drops-monitor.png" width="112" alt="Drops Monitor logo">

# Drops Monitor

### A Twitch Drops account checker for Windows

💎　　　　　　　　　　　　　🔮　　　　　　　　　　　　　💎

**Import accounts · inspect campaign progress · review rewards**

[Features](#features) · [Getting started](#getting-started) · [Build](#build-from-source) · [Русский](#русский)

</div>

---

## Features

- Sign in to Twitch with a device code.
- Import accounts from TXT as a full `email:login:password:oauth_token:user_ID:device_ID` row, a `login:oauth_token` row, or one OAuth token per line.
- Validate account tokens with Twitch and check available Drops campaigns and reward progress.
- View progress grouped by campaign, with reward claim status and game artwork when Twitch provides it.
- Recheck accounts with incomplete or undiscovered Drops.
- Choose how many accounts to check in parallel (1–30).

## Getting started

1. Build the application using the instructions below, or download a packaged executable if one is available on the project's Releases page.
2. Start the application and open **Import accounts**.
3. Select a TXT file with one account per line.
4. Use the campaign filter and **Recheck** button to review current results.

The app processes imported accounts on your computer. It does not save account data, passwords, or OAuth tokens to disk; tokens stay in memory only while the app is running. The import concurrency preference is stored locally. Close and reopen the app, then import the file again to reconnect accounts.

## Build from source

Requirements: Windows, Python 3.11+, and Microsoft Edge WebView2 Runtime.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
./build.ps1
```

The executable is written to `dist/DropsMonitor.exe`. Build output and local virtual environments are excluded from Git.

---

<div align="center">

## Русский

💎　　　　　　　　　　　　　🔮　　　　　　　　　　　　　💎

### Чекер аккаунтов и кампаний Twitch Drops для Windows

</div>

## Возможности

- Вход в Twitch по коду устройства.
- Импорт аккаунтов из TXT: полная строка `email:login:password:oauth_token:user_ID:device_ID`, строка `login:oauth_token` или один OAuth-токен на строке.
- Проверка OAuth-токенов через Twitch и получение доступных кампаний Drops и прогресса наград.
- Просмотр прогресса по кампаниям, статусов получения наград и обложек игр, если Twitch их предоставляет.
- Повторная проверка аккаунтов с незавершёнными или не найденными Drops.
- Настройка числа параллельных проверок от 1 до 30.
- Вход через Twitch с кодом устройства, если он доступен.

## Быстрый старт

1. Соберите приложение по инструкции ниже или скачайте готовый EXE со страницы Releases, если он там опубликован.
2. Запустите приложение и нажмите **Импорт аккаунтов**.
3. Выберите TXT-файл, где каждый аккаунт находится на отдельной строке.
4. Используйте фильтр кампаний и кнопку **Перепроверить**, чтобы обновить результаты.

Импорт обрабатывается на вашем компьютере. Данные аккаунта, пароль и OAuth-токен не сохраняются на диск: токен находится только в памяти, пока приложение запущено. Локально сохраняется только настройка параллельности импорта. После перезапуска импортируйте файл заново.

## Сборка из исходников

Требования: Windows, Python 3.11 или новее и Microsoft Edge WebView2 Runtime.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
./build.ps1
```

EXE появится в `dist/DropsMonitor.exe`. Сборочные файлы и локальное виртуальное окружение не включаются в Git.

---

<div align="center">

💎　　　　　　　　　　　　　Drops Monitor　　　　　　　　　　　　　💎

</div>
