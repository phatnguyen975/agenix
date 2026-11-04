#!/usr/bin/env python3
"""Run a command repeatedly and report its pass/fail rate.

Measure and compare reproduction rates (before and after a fix) and raise the reproduction
rate of intermittent failures.

Usage:
  python repeat-run.py --runs N [--parallel K] [--timeout SECONDS] [--cwd DIR]
                       [--stop-on-fail] [--show-failures M] [--tail-lines L]
                       [--json] -- COMMAND [ARGS...]

A run passes when the command exits with code 0. Each run receives the environment variable
REPEAT_RUN_INDEX (0-based) so a command can derive unique temporary paths or ports. Output
excerpts are printed as captured and are not redacted; redact them before sharing.

Exit codes: 0 every executed run passed; 1 at least one run failed or timed out; 2 usage error
or the command could not be started.
"""

import argparse
import concurrent.futures
import json
import math
import os
import signal
import statistics
import subprocess
import sys
import threading
import time


def _kill_tree(proc):
    """Kill the command tree; return whether tree-wide termination succeeded."""
    if os.name == "nt":
        try:
            result = subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                capture_output=True,
                check=False,
            )
        except OSError:
            try:
                proc.kill()
            except OSError:
                pass
            return False

        if result.returncode != 0:
            try:
                proc.kill()
            except OSError:
                pass
            return False
        return True

    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except OSError:
        try:
            proc.kill()
        except OSError:
            pass
        return False
    return True


def run_once(index, argv, cwd, timeout, stop_event, stop_on_fail=False):
    result = _run_once(index, argv, cwd, timeout, stop_event)
    if result and stop_on_fail and result["status"] != "passed":
        stop_event.set()
    return result


def _run_once(index, argv, cwd, timeout, stop_event):
    if stop_event.is_set():
        return None
    env = dict(os.environ, REPEAT_RUN_INDEX=str(index))
    started = time.monotonic()
    try:
        if os.name != "nt":
            proc = subprocess.Popen(
                argv,
                cwd=cwd,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                errors="replace",
                start_new_session=True,
            )
        else:
            proc = subprocess.Popen(
                argv,
                cwd=cwd,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                errors="replace",
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            )
    except OSError as exc:
        return {
            "index": index,
            "status": "error",
            "exit_code": None,
            "seconds": 0.0,
            "output": str(exc),
        }

    try:
        output, _ = proc.communicate(timeout=timeout)
        return {
            "index": index,
            "status": "passed" if proc.returncode == 0 else "failed",
            "exit_code": proc.returncode,
            "seconds": time.monotonic() - started,
            "output": output or "",
        }
    except subprocess.TimeoutExpired as exc:
        tree_killed = _kill_tree(proc)
        if os.name == "nt" and not tree_killed:
            try:
                proc.wait(timeout=1.0)
            except subprocess.TimeoutExpired:
                try:
                    proc.kill()
                except OSError:
                    pass
                try:
                    proc.wait(timeout=1.0)
                except subprocess.TimeoutExpired:
                    pass

            output = exc.output or ""
            if isinstance(output, bytes):
                output = output.decode(errors="replace")
        else:
            output, _ = proc.communicate()

        return {
            "index": index,
            "status": "timeout",
            "exit_code": None,
            "seconds": time.monotonic() - started,
            "output": output or "",
        }


def shorten(line, limit=300):
    if len(line) <= limit:
        return line
    half = (limit - 5) // 2
    return line[:half] + " ... " + line[-half:]


def tail(text, lines):
    kept = text.splitlines()[-lines:] if lines > 0 else []
    return "\n".join(shorten(line) for line in kept)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--runs", type=int, required=True, help="number of runs")
    parser.add_argument(
        "--parallel",
        type=int,
        default=1,
        help="concurrent runs (default 1); shared resources can change the rate",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=None,
        help="per-run timeout in seconds; a timed-out run counts as failed",
    )
    parser.add_argument("--cwd", default=None, help="working directory for each run")
    parser.add_argument(
        "--stop-on-fail",
        action="store_true",
        help="stop scheduling new runs after the first failure",
    )
    parser.add_argument(
        "--show-failures",
        type=int,
        default=3,
        help="number of failing runs whose output tail is shown (default 3)",
    )
    parser.add_argument(
        "--tail-lines",
        type=int,
        default=15,
        help="lines of output kept per shown failure (default 15)",
    )
    parser.add_argument("--json", action="store_true", help="print the summary as JSON")
    parser.add_argument(
        "command", nargs=argparse.REMAINDER, help="command to run, after a literal --"
    )
    args = parser.parse_args()

    argv = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not argv:
        parser.error("a command is required after --")
    if args.runs < 1 or args.parallel < 1:
        parser.error("--runs and --parallel must be at least 1")
    if args.timeout is not None and (
        not math.isfinite(args.timeout) or args.timeout < 0
    ):
        parser.error("--timeout must be a finite, non-negative number")

    stop_event = threading.Event()
    results = []
    start_error = None
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.parallel) as pool:
        if args.stop_on_fail:
            next_index = 0
            while next_index < args.runs:
                batch_end = min(next_index + args.parallel, args.runs)
                futures = [
                    pool.submit(
                        run_once,
                        index,
                        argv,
                        args.cwd,
                        args.timeout,
                        stop_event,
                        True,
                    )
                    for index in range(next_index, batch_end)
                ]
                next_index = batch_end
                batch_failed = False

                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    if result is None:
                        continue
                    if result["status"] == "error":
                        if start_error is None:
                            start_error = result
                        stop_event.set()
                        continue
                    results.append(result)
                    if result["status"] != "passed":
                        batch_failed = True

                if start_error is not None or batch_failed:
                    break
        else:
            futures = [
                pool.submit(
                    run_once, i, argv, args.cwd, args.timeout, stop_event, False
                )
                for i in range(args.runs)
            ]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result is None:
                    continue
                if result["status"] == "error":
                    start_error = result
                    stop_event.set()
                    break
                results.append(result)

    if start_error is not None:
        print(
            "error: could not start the command: " + start_error["output"],
            file=sys.stderr,
        )
        return 2

    results.sort(key=lambda r: r["index"])
    executed = len(results)
    passed = sum(r["status"] == "passed" for r in results)
    timed_out = sum(r["status"] == "timeout" for r in results)
    failed = executed - passed - timed_out
    codes = {}
    for r in results:
        key = "timeout" if r["exit_code"] is None else str(r["exit_code"])
        codes[key] = codes.get(key, 0) + 1
    seconds = [r["seconds"] for r in results]
    bad = [r for r in results if r["status"] != "passed"]
    summary = {
        "command": argv,
        "runs_requested": args.runs,
        "runs_executed": executed,
        "parallel": args.parallel,
        "passed": passed,
        "failed": failed,
        "timed_out": timed_out,
        "failure_rate": round((failed + timed_out) / executed, 4) if executed else None,
        "exit_codes": codes,
        "seconds": {
            "min": round(min(seconds), 3),
            "median": round(statistics.median(seconds), 3),
            "max": round(max(seconds), 3),
        }
        if seconds
        else None,
        "failures": [
            {
                "run": r["index"],
                "status": r["status"],
                "exit_code": r["exit_code"],
                "output_tail": tail(r["output"], args.tail_lines),
            }
            for r in bad[: max(args.show_failures, 0)]
        ],
    }

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        pct = lambda n: f"{100.0 * n / executed:.1f}%"
        print(
            f"runs requested: {args.runs}, executed: {executed}, parallel: {args.parallel}"
        )
        print(
            f"passed: {passed} ({pct(passed)}), failed: {failed} ({pct(failed)}), "
            f"timed out: {timed_out}"
        )
        print("exit codes: " + ", ".join(f"{k} x{v}" for k, v in sorted(codes.items())))
        s = summary["seconds"]
        print(f"seconds per run: min {s['min']}, median {s['median']}, max {s['max']}")
        if args.parallel > 1:
            print(
                "note: runs executed concurrently; shared resources can change the rate"
            )
        for item in summary["failures"]:
            print(
                f"--- run {item['run']} ({item['status']}, exit code {item['exit_code']}) ---"
            )
            print(item["output_tail"])
    return 0 if failed + timed_out == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        sys.exit(1)
