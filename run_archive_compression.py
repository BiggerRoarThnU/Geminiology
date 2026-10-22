#!/usr/bin/env python3
import os
import sys

# Ensure src is in the path to import the compiler
sys.path.append(os.path.expanduser("~/SovereignNexus/src"))
from nexus_binder_compiler import SemanticDefragmenter

print("[*] Engaging Semantic Defragmenter on Legacy Vaults...")

# Corrected path based on the Ghost Skeleton
source_vault = os.path.expanduser("~/SovereignNexus/Vault/Archive_Legacy/Lucid Build Up/Dual_Master_Q")
output_binder = os.path.expanduser("~/SovereignNexus/MASTER_ARCHIVE_BINDER.md")

compiler = SemanticDefragmenter()
stats = compiler.compile_master_binder(source_vault, output_binder)

print("\n[+] Compression Complete. Ready for Cloud Notebook or Local Ingestion.")
