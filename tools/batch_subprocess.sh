#!/bin/bash
# Batch generate audio using subprocess isolation (kills hung TTS properly)
# Usage: bash tools/batch_subprocess.sh id1,id2,id3,...
IFS=',' read -ra IDS <<< "$1"
TOTAL=${#IDS[@]}
OK=0
FAIL=0
for i in "${!IDS[@]}"; do
    ID=${IDS[$i]}
    NUM=$((i + 1))
    echo "[$NUM/$TOTAL] Episode $ID..."
    # Run gen_single.py with 660s timeout (10 min TTS + 1 min buffer)
    timeout 660 python3 tools/gen_single.py "$ID"
    RC=$?
    if [ $RC -eq 0 ]; then
        OK=$((OK + 1))
    elif [ $RC -eq 124 ]; then
        echo "  TIMEOUT killed for $ID"
        FAIL=$((FAIL + 1))
    else
        FAIL=$((FAIL + 1))
        # Retry once
        echo "  RETRY $ID..."
        sleep 3
        timeout 660 python3 tools/gen_single.py "$ID"
        if [ $? -eq 0 ]; then
            OK=$((OK + 1))
            FAIL=$((FAIL - 1))
        fi
    fi
done
echo "Done! $OK ok, $FAIL fail out of $TOTAL"
