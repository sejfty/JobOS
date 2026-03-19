#!/bin/bash

# JobOS Daily Digest — macOS notification
# Reads todo.md and sends a native notification with pending task summary.

# --- Configuration ---
CONFIG_DIR="$HOME/.config/jobos"
CONFIG_FILE="$CONFIG_DIR/config"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "JobOS config not found. Run setup.sh first."
    exit 1
fi

source "$CONFIG_FILE"

if [ -z "$JOBOS_PATH" ]; then
    echo "JOBOS_PATH not set in $CONFIG_FILE"
    exit 1
fi

TODO_FILE="$JOBOS_PATH/todo.md"

if [ ! -f "$TODO_FILE" ]; then
    osascript -e 'display notification "todo.md not found. Run a planning session." with title "JobOS" subtitle "No todo file"'
    exit 0
fi

# --- Parse todo.md ---
# Count non-header, non-separator, non-empty table rows
TOTAL=$(awk -F'|' '
    NR > 4 && NF >= 3 && $0 !~ /^[[:space:]]*$/ && $0 !~ /^[[:space:]]*\|[-]+/ {
        count++
    }
    END { print count+0 }
' "$TODO_FILE")

URGENT=$(awk -F'|' '
    NR > 4 && NF >= 3 && $0 !~ /^[[:space:]]*$/ && $0 !~ /^[[:space:]]*\|[-]+/ {
        gsub(/[[:space:]]/, "", $5)
        if (tolower($5) == "urgent") count++
    }
    END { print count+0 }
' "$TODO_FILE")

HIGH=$(awk -F'|' '
    NR > 4 && NF >= 3 && $0 !~ /^[[:space:]]*$/ && $0 !~ /^[[:space:]]*\|[-]+/ {
        gsub(/[[:space:]]/, "", $5)
        if (tolower($5) == "high") count++
    }
    END { print count+0 }
' "$TODO_FILE")

# --- Build notification ---
if [ "$TOTAL" -eq 0 ]; then
    TITLE="JobOS — All Clear"
    MESSAGE="No pending tasks. Nice work."
else
    TITLE="JobOS — $TOTAL pending task(s)"
    PARTS=()
    if [ "$URGENT" -gt 0 ]; then
        PARTS+=("$URGENT urgent")
    fi
    if [ "$HIGH" -gt 0 ]; then
        PARTS+=("$HIGH high priority")
    fi
    NORMAL=$((TOTAL - URGENT - HIGH))
    if [ "$NORMAL" -gt 0 ]; then
        PARTS+=("$NORMAL normal")
    fi

    MESSAGE=$(IFS=', '; echo "${PARTS[*]}")
    MESSAGE="$MESSAGE. Time for a planning session."
fi

osascript -e "display notification \"$MESSAGE\" with title \"$TITLE\""
