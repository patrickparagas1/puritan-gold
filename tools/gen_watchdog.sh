#!/bin/bash
# Watchdog: runs gen_chunked.py for each episode, kills hung edge_tts processes
# Usage: bash tools/gen_watchdog.sh id1,id2,id3,...

IFS=',' read -ra IDS <<< "$1"
TOTAL=${#IDS[@]}
OK=0
FAIL=0

echo "Generating $TOTAL episodes with watchdog"

for i in "${!IDS[@]}"; do
    ID=${IDS[$i]}
    NUM=$((i + 1))
    echo ""
    echo "[$NUM/$TOTAL] Episode $ID:"

    # Run gen_chunked.py in background
    python3 tools/gen_chunked.py "$ID" &
    PID=$!

    # Watchdog: check every 30 seconds, kill if edge_tts hung for >200s
    WAIT=0
    while kill -0 $PID 2>/dev/null; do
        sleep 30
        WAIT=$((WAIT + 30))

        # Check for hung edge_tts (0% CPU for >200s)
        EDGE_PID=$(pgrep -f "edge_tts.*ep_${ID}" 2>/dev/null | head -1)
        if [ -n "$EDGE_PID" ]; then
            EDGE_CPU=$(ps -o %cpu= -p "$EDGE_PID" 2>/dev/null | tr -d ' ')
            if [ "$EDGE_CPU" = "0.0" ] && [ $WAIT -gt 200 ]; then
                echo "  WATCHDOG: Killing hung edge_tts (PID $EDGE_PID)"
                kill -9 "$EDGE_PID" 2>/dev/null
            fi
        fi

        # Hard timeout: 15 minutes per episode
        if [ $WAIT -gt 900 ]; then
            echo "  WATCHDOG: Hard timeout, killing episode $ID"
            kill -9 $PID 2>/dev/null
            pkill -9 -f "edge_tts.*chunk" 2>/dev/null
            break
        fi
    done

    wait $PID 2>/dev/null
    RC=$?

    if [ -f "audio/ep${ID}.mp3" ] && [ "$(stat -f%z "audio/ep${ID}.mp3" 2>/dev/null)" -gt 10000 ]; then
        OK=$((OK + 1))
        echo "  DONE ($OK/$TOTAL ok)"
    else
        FAIL=$((FAIL + 1))
        echo "  FAILED"
    fi
done

echo ""
echo "Done! $OK ok, $FAIL fail out of $TOTAL"
