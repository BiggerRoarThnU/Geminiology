"""
SOVEREIGN ARCHIVE: notebook
CAPTURED: 2026-02-24T16:04:23.707354
SOURCE: .\geminiology_one\ROOM_1_ARCHIVE\knowledge_vault\AI Model & DATA SETS FOR M&I\wisdom_vault\knowledge_vault\models\tanaos_anonymizer\notebook.ipynb
PROTOCOL: OMEGA-NOTEBOOK
"""

!pip install artifex

from artifex import Artifex

ta = Artifex().text_anonymization

print(ta("John Doe lives at 123 Main St, New York. His phone number is (555) 123-4567."))

!pip install transformers

from transformers import pipeline

ta = pipeline(
    task="text-anonymization",
    model="tanaos/tanaos-text-anonymizer-v1",
    aggregation_strategy="first"
)

print(ta("John Doe lives at 123 Main St, New York. His phone number is (555) 123-4567."))