#!/usr/bin/env python3
"""Batch TTS via subprocess isolation. Each episode runs in its own process with hard timeout.
Usage: python3 tools/batch_sub.py --ids 1001,1002,1003
"""
import sys, os, subprocess, time, argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ids", required=True)
    args = parser.parse_args()

    ids = [int(x) for x in args.ids.split(',') if x.strip()]
    total = len(ids)
    ok = 0
    fail = 0
    failed_ids = []

    print(f"Generating {total} episodes via subprocess isolation", flush=True)
    start = time.time()

    for i, eid in enumerate(ids, 1):
        print(f"\n[{i}/{total}] Episode {eid}:", flush=True)
        for attempt in range(3):
            try:
                result = subprocess.run(
                    [sys.executable, "tools/gen_chunked.py", str(eid)],
                    capture_output=True, text=True, timeout=1260
                )
                output = (result.stdout + result.stderr).strip()
                print(f"  {output}", flush=True)
                if result.returncode == 0:
                    ok += 1
                    break
                elif "SKIP exists" in output or "SKIP" in output:
                    ok += 1
                    break
                else:
                    if attempt < 2:
                        print(f"  RETRY attempt {attempt+2}/3...", flush=True)
                        time.sleep(5)
                    else:
                        fail += 1
                        failed_ids.append(eid)
            except subprocess.TimeoutExpired:
                print(f"  TIMEOUT killed (attempt {attempt+1}/3)", flush=True)
                if attempt < 2:
                    time.sleep(5)
                else:
                    fail += 1
                    failed_ids.append(eid)

    elapsed = time.time() - start
    print(f"\nDone! {ok} ok, {fail} fail, {elapsed/60:.1f} min", flush=True)
    if failed_ids:
        print(f"Failed IDs: {failed_ids}", flush=True)

if __name__ == "__main__":
    main()
