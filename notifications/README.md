# JobOS Daily Digest — macOS Notifications

A lightweight daily notification that tells you how many pending tasks are in your `todo.md`, broken down by priority. Nudges you to open a planning session — nothing more.

## What it does

Once a day at your chosen time, you get a native macOS notification like:

> **JobOS — 4 pending task(s)**
> 1 urgent, 1 high priority, 2 normal. Time for a planning session.

If your todo list is empty:

> **JobOS — All Clear**
> No pending tasks. Nice work.

## Setup

1. Copy the `notifications/` folder into your JobOS repo (or anywhere on your Mac)
2. Run the setup script:

```bash
cd notifications
chmod +x setup.sh jobos-notify.sh
./setup.sh
```

3. Follow the prompts — enter your repo path and preferred notification time
4. Test it immediately:

```bash
bash ~/.config/jobos/jobos-notify.sh
```

## How it works

- `setup.sh` saves your repo path to `~/.config/jobos/config`, copies the notification script, and installs a `launchd` schedule
- `launchd` runs the script once daily at your chosen time (even without Terminal open)
- The script reads `todo.md`, counts tasks by priority, and fires a native macOS notification via `osascript`
- Zero dependencies — uses only built-in macOS tools

## Change notification time

Re-run `setup.sh` — it will overwrite the existing schedule.

## Uninstall

```bash
launchctl unload ~/Library/LaunchAgents/com.jobos.daily-digest.plist
rm ~/Library/LaunchAgents/com.jobos.daily-digest.plist
rm -rf ~/.config/jobos
```

## Logs

If something isn't working, check:
- `~/.config/jobos/notify.log`
- `~/.config/jobos/notify-error.log`
