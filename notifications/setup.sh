#!/bin/bash

# JobOS Daily Digest — Setup
# Configures the repo path and installs the macOS launchd schedule.

echo "=== JobOS Daily Digest Setup ==="
echo ""

# --- Get repo path ---
read -p "Enter the full path to your JobOS repo (e.g., /Users/martin/projects/Job-OS-WIP): " REPO_PATH

# Remove trailing slash
REPO_PATH="${REPO_PATH%/}"

if [ ! -d "$REPO_PATH" ]; then
    echo "Error: Directory '$REPO_PATH' does not exist."
    exit 1
fi

if [ ! -f "$REPO_PATH/todo.md" ] && [ ! -f "$REPO_PATH/pipeline.md" ]; then
    echo "Warning: This doesn't look like a JobOS repo (no todo.md or pipeline.md found)."
    read -p "Continue anyway? (y/n): " CONFIRM
    if [ "$CONFIRM" != "y" ]; then
        exit 1
    fi
fi

# --- Ask for notification time ---
read -p "What time should the daily digest run? (HH:MM, 24h format, default 09:00): " NOTIFY_TIME
NOTIFY_TIME="${NOTIFY_TIME:-09:00}"

HOUR=$(echo "$NOTIFY_TIME" | cut -d: -f1)
MINUTE=$(echo "$NOTIFY_TIME" | cut -d: -f2)

# Validate
if ! [[ "$HOUR" =~ ^[0-9]{1,2}$ ]] || ! [[ "$MINUTE" =~ ^[0-9]{1,2}$ ]] || [ "$HOUR" -gt 23 ] || [ "$MINUTE" -gt 59 ]; then
    echo "Error: Invalid time format."
    exit 1
fi

# --- Create config ---
CONFIG_DIR="$HOME/.config/jobos"
mkdir -p "$CONFIG_DIR"

cat > "$CONFIG_DIR/config" << EOF
JOBOS_PATH="$REPO_PATH"
EOF

echo "Config saved to $CONFIG_DIR/config"

# --- Copy script ---
SCRIPT_PATH="$CONFIG_DIR/jobos-notify.sh"
SCRIPT_SOURCE="$(cd "$(dirname "$0")" && pwd)/jobos-notify.sh"

if [ ! -f "$SCRIPT_SOURCE" ]; then
    echo "Error: jobos-notify.sh not found next to this setup script."
    exit 1
fi

cp "$SCRIPT_SOURCE" "$SCRIPT_PATH"
chmod +x "$SCRIPT_PATH"
echo "Script installed to $SCRIPT_PATH"

# --- Create and install launchd plist ---
PLIST_NAME="com.jobos.daily-digest"
PLIST_PATH="$HOME/Library/LaunchAgents/$PLIST_NAME.plist"

cat > "$PLIST_PATH" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$PLIST_NAME</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$SCRIPT_PATH</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>$HOUR</integer>
        <key>Minute</key>
        <integer>$MINUTE</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>$CONFIG_DIR/notify.log</string>
    <key>StandardErrorPath</key>
    <string>$CONFIG_DIR/notify-error.log</string>
</dict>
</plist>
EOF

# Unload if already loaded, then load
launchctl unload "$PLIST_PATH" 2>/dev/null
launchctl load "$PLIST_PATH"

echo ""
echo "=== Setup Complete ==="
echo "  Repo path: $REPO_PATH"
echo "  Daily notification at: $NOTIFY_TIME"
echo "  Plist: $PLIST_PATH"
echo "  Script: $SCRIPT_PATH"
echo "  Config: $CONFIG_DIR/config"
echo ""
echo "To test now, run: bash $SCRIPT_PATH"
echo "To uninstall: launchctl unload $PLIST_PATH && rm $PLIST_PATH"
