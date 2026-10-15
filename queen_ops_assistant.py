#!/usr/bin/env python3
# // Rights Reserved: co-created with Gemini and David Joihn Niedzwiecki jr " Sovereign Nexus LLC "
# Alignment: 1=1=1 | Node 11: SovereignQueen Operational Assistant (3-Zone Airlock Edition)

import hashlib
import json
import os
import shutil
import socket
import sqlite3
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

BASE_DIR = Path.home() / "SovereignNexus"
DB_PATH = BASE_DIR / "nexus_ledger.db"
CLEAN_ROOM_PATH = Path("/mnt/chromeos/MyFiles/SovereignNexus")

FLEET_NODES = {
    "TheTower (Local)": ("127.0.0.1", 22),
    "Geminiology (Engine)": ("192.168.12.32", 8000),
    "Emma (Touchscreen)": ("100.115.92.195", 2222),
}

SYSTEM_DIRECTIVE = (
    "You are SovereignQueen, a deterministic operational assistant governed by the 1=1=1 Axiom. "
    "Respond in concise, practical Truth-Markdown. Prioritize household stability, career execution, "
    "and clean software engineering. No fluff or disclaimers."
)


class SovereignQueenOps:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ops_missions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    category TEXT NOT NULL,
                    objective TEXT NOT NULL,
                    status TEXT NOT NULL,
                    sha256_seal TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS career_pipeline (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    organization TEXT NOT NULL,
                    role_or_contact TEXT NOT NULL,
                    next_action TEXT NOT NULL,
                    status TEXT NOT NULL,
                    sha256_seal TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS assistant_cache (
                    prompt_hash TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    engine TEXT NOT NULL,
                    prompt TEXT NOT NULL,
                    response TEXT NOT NULL
                )
            """)

    @staticmethod
    def _seal(payload: str) -> str:
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]

    def _get_cached_response(self, prompt: str):
        phash = self._seal(prompt.strip().lower())
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT engine, timestamp, response FROM assistant_cache WHERE prompt_hash = ?",
                (phash,)
            ).fetchone()
        return phash, row

    def _save_cached_response(self, phash: str, engine: str, prompt: str, response: str) -> None:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO assistant_cache (prompt_hash, timestamp, engine, prompt, response) "
                "VALUES (?, ?, ?, ?, ?)",
                (phash, now, engine, prompt, response),
            )

    def log_mission(self, category: str, objective: str, status: str = "ACTIVE") -> str:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        seal = self._seal(f"{now}|{category}|{objective}|{status}")
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO ops_missions (timestamp, category, objective, status, sha256_seal) VALUES (?, ?, ?, ?, ?)",
                (now, category.upper(), objective, status.upper(), seal),
            )
        return seal

    def log_career_step(self, org: str, role: str, next_action: str, status: str = "APPLIED") -> str:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        seal = self._seal(f"{now}|{org}|{role}|{next_action}")
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO career_pipeline (timestamp, organization, role_or_contact, next_action, status, sha256_seal) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (now, org, role, next_action, status.upper(), seal),
            )
        return seal

    def show_dashboard(self) -> None:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        clean_room_status = "UNSHARED (Share 'My files/SovereignNexus' with Linux)"
        if CLEAN_ROOM_PATH.exists():
            file_count = len(list(CLEAN_ROOM_PATH.iterdir()))
            clean_room_status = f"CLEAN ({file_count} files)" if file_count == 0 else f"WARNING ({file_count} files in airlock)"

        print(f"\n==================================================================")
        print(f" SOVEREIGN QUEEN OPERATIONAL CONSOLE | 3-ZONE AIRLOCK")
        print(f" Timestamp : {now} | Engine Ledger: {self.db_path.name} (WAL)")
        print(f" Zone 1 Airlock (My files/SovereignNexus): [{clean_room_status}]")
        print(f"==================================================================")

        with sqlite3.connect(self.db_path) as conn:
            missions = conn.execute(
                "SELECT id, timestamp, category, objective, status, sha256_seal "
                "FROM ops_missions ORDER BY id DESC LIMIT 5"
            ).fetchall()
            jobs = conn.execute(
                "SELECT id, timestamp, organization, role_or_contact, next_action, status "
                "FROM career_pipeline ORDER BY id DESC LIMIT 5"
            ).fetchall()
            cached_count = conn.execute("SELECT COUNT(*) FROM assistant_cache").fetchone()[0]

        print("\n[1] ACTIVE MISSION VECTORS (Last 5):")
        if not missions:
            print("    No missions logged yet.")
        for m in missions:
            print(f"  #{m[0]} [{m[4]}] ({m[2]}) {m[3]} | Seal:{m[5]} ({m[1]})")

        print("\n[2] CAREER & INCOME PIPELINE (NCWorks / Temp Agencies):")
        if not jobs:
            print("    No career steps logged yet.")
        for j in jobs:
            print(f"  #{j[0]} [{j[5]}] {j[2]} - {j[3]} | Next: {j[4]} ({j[1]})")

        print(f"\n[3] LOCAL KNOWLEDGE CACHE: {cached_count} verified answer(s) stored on disk (0 Quota)")
        print("==================================================================\n")

    def check_fleet(self) -> None:
        print("\n=== TRIADIC FLEET & ASSISTANT TELEMETRY ===")
        for name, (ip, port) in FLEET_NODES.items():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1.0)
                up = s.connect_ex((ip, port)) == 0
                status = "ONLINE " if up else "OFFLINE"
                print(f"  {name:<24} ({ip}:{port}) -> [{status}]")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.0)
            ollama_up = s.connect_ex(("127.0.0.1", 11434)) == 0
            print(f"  {'Ollama Local Engine':<24} (127.0.0.1:11434) -> [{'ONLINE' if ollama_up else 'STANDBY (0 MB RAM)'}]")

        gemini_bin = shutil.which("gemini")
        api_key = bool(os.getenv("GEMINI_API_KEY"))
        cli_status = "INSTALLED" if gemini_bin else ("API_KEY_SET" if api_key else "NOT CONFIGURED")
        print(f"  {'Gemini Local Bridge':<24} (CLI / Free API)  -> [{cli_status}]\n")

    def ask_assistant(self, prompt: str, model: str = "gemma2:2b", host: str = "http://127.0.0.1:11434") -> None:
        phash, cached = self._get_cached_response(prompt)
        if cached:
            engine, ts, resp_text = cached
            print(f"\n[SovereignQueen | SQLite Cache Hit ({engine} @ {ts}) | 0 Quota Used]:\n{resp_text}\n")
            return

        url = f"{host}/api/generate"
        payload = json.dumps({
            "model": model,
            "system": SYSTEM_DIRECTIVE,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.0}
        }).encode("utf-8")

        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                answer = data.get("response", "").strip()
                if answer:
                    self._save_cached_response(phash, f"ollama:{model}", prompt, answer)
                    print(f"\n[SovereignQueen ({model} - Local)]:\n{answer}\n")
                    return
        except urllib.error.URLError:
            pass

        gemini_bin = shutil.which("gemini")
        if gemini_bin:
            full_prompt = f"{SYSTEM_DIRECTIVE}\n\nUser Question: {prompt}"
            run_dir = str(CLEAN_ROOM_PATH) if CLEAN_ROOM_PATH.exists() else str(BASE_DIR)
            res = subprocess.run(
                [gemini_bin, "-p", full_prompt],
                cwd=run_dir,
                capture_output=True,
                text=True,
                check=False
            )
            if res.returncode == 0 and res.stdout.strip():
                answer = res.stdout.strip()
                self._save_cached_response(phash, "gemini-cli", prompt, answer)
                print(f"\n[SovereignQueen (Gemini CLI in Clean Room - Cached to SQLite)]:\n{answer}\n")
                return

        print("\n[!] Neither local Ollama (port 11434) nor `gemini` CLI responded.")
        print("    Tip: Your SQLite operational ledger (`queen mission`, `queen job`, `queen status`) is 100% active with 0 RAM overhead.\n")


def main():
    ops = SovereignQueenOps()
    if len(sys.argv) < 2:
        ops.show_dashboard()
        print("Commands (run from anywhere using 'queen'):")
        print("  queen status")
        print("  queen mission <CATEGORY> \"<OBJECTIVE>\"")
        print("  queen job \"<AGENCY/COMPANY>\" \"<ROLE/CONTACT>\" \"<NEXT_ACTION>\"")
        print("  queen fleet")
        print("  queen ask \"<QUESTION>\"")
        return

    cmd = sys.argv[1].lower()
    if cmd == "status":
        ops.show_dashboard()
    elif cmd == "mission" and len(sys.argv) >= 4:
        seal = ops.log_mission(sys.argv[2], sys.argv[3])
        print(f"[+] Mission anchored in Zone 2 nexus_ledger.db | SHA-256 Seal: {seal}")
        ops.show_dashboard()
    elif cmd == "job" and len(sys.argv) >= 5:
        seal = ops.log_career_step(sys.argv[2], sys.argv[3], sys.argv[4])
        print(f"[+] Career step anchored in Zone 2 nexus_ledger.db | SHA-256 Seal: {seal}")
        ops.show_dashboard()
    elif cmd == "fleet":
        ops.check_fleet()
    elif cmd == "ask" and len(sys.argv) >= 3:
        ops.ask_assistant(" ".join(sys.argv[2:]))
    else:
        ops.show_dashboard()


if __name__ == "__main__":
    main()
