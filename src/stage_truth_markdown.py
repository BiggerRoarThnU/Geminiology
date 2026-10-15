#!/usr/bin/env python3
"""
SovereignNexus LLC - Truth Markdown Stager
Axiom: 1=1=1 | Converts local workspace files into Truth-Markdown for ingestion.
"""

import os

def main():
    target_files = [
        'letting-the-monster-go-in-ai.md',
        'nexus_mmap_page.py',
        'THERMAL_BREACH_PROTOCOL.md',
        'VAMPIRE_BAT_OPTIMIZATION.md',
        'nexus_metacognitive_sentinel.py',
        'THE_EPISTEMOLOGY_OF_DETERMINISTIC_AUTONOMY.md',
        'nexus_aakg_ingest.py',
        'sovereign-stack-4-federal-operational.md',
        'nexus_t7_maintenance_sweep.py',
        'BENCHMARKS.md'
    ]

    base_dir = os.path.expanduser('~/SovereignNexus')
    out_dir = os.path.join(base_dir, 'truth_markdown_ingest')
    
    # Ensure the output directory exists
    os.makedirs(out_dir, exist_ok=True)
    print(f"[*] Staging directory verified: {out_dir}")

    for fname in target_files:
        src_path = os.path.join(base_dir, fname)
        # Check fallback directory if not in root
        if not os.path.exists(src_path):
            src_path = os.path.join(base_dir, '01_The_Runway', fname)

        if os.path.exists(src_path):
            with open(src_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().strip()

            # Fix the naming logic for python files
            if fname.endswith('.md'):
                md_name = fname
            else:
                # Safely split the extension and add _truth.md
                md_name = fname.rsplit('.', 1)[0] + '_truth.md'
                
            dest_path = os.path.join(out_dir, md_name)

            # Wrap python code in markdown blocks
            if fname.endswith('.py'):
                header = f'# Truth-Markdown Component: {fname}\n\n**Axiom:** 1=1=1 | **Type:** Type-Safe Python Code Block\n\n```python\n{content}\n```\n'
            else:
                header = content

            with open(dest_path, 'w', encoding='utf-8') as out_f:
                out_f.write(header)
                
            print(f'  [✓] Converted and staged: {md_name}')
        else:
            print(f'  [!] Pending source file: {fname} (Not found in base or 01_The_Runway)')
            
    print("\n[*] Staging sequence complete. Files are ready for Queen Assimilation.")

if __name__ == "__main__":
    main()
