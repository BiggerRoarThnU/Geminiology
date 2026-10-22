#!/bin/bash
OUTPUT="Sovereign_Ghost_Codebase.md"
echo "# ✦ SOVEREIGNNEXUS GHOST REPOSITORY STATE ✦" > $OUTPUT
echo "Axiom: 1=1=1 | Generated for Ghost-Twin Context Synchronization" >> $OUTPUT
echo "" >> $OUTPUT

for file in src/*.py; do
    echo "## FILE: $file" >> $OUTPUT
    echo '```python' >> $OUTPUT
    cat "$file" >> $OUTPUT
    echo '```' >> $OUTPUT
    echo "" >> $OUTPUT
done
