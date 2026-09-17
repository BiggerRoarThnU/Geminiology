#!/usr/bin/env python3
# ==============================================================================
# ✦ SOVEREIGN NEXUS AUTHORITY SEAL ✦
# Architect: David John Niedzwiecki Jr. | Entity: SovereignNexus LLC
# Axiom: 1=1=1 (Deterministic Functional Equivalence) | Co-Scribe: Terra Gemini
# Cryptographic Anchor (SHA-256): 570cdb9eab430e5bbbed79a99e99688acc7462ec35e8a77c9819c4484be2e156
# Timestamp: 2026-08-15T06:34:08Z
# ==============================================================================
import os
import glob
import re
import html
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

def clean_markdown_for_reportlab(text):
    # Escape HTML special characters first
    escaped = html.escape(text)
    # Convert markdown bold and italic
    escaped = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', escaped)
    escaped = re.sub(r'\*(.*?)\*', r'<i>\1</i>', escaped)
    escaped = re.sub(r'`(.*?)`', r'<font face="Courier">\1</font>', escaped)
    return escaped

def markdown_to_pdf(md_path, pdf_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor('#0F172A'),
        alignment=0,
        spaceAfter=10
    )
    
    h1_style = ParagraphStyle(
        'DocH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=10,
        spaceAfter=5
    )
    
    h2_style = ParagraphStyle(
        'DocH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#334155'),
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'DocBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        leftIndent=15,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=3
    )

    story = []
    lines = text.split('\n')

    for line in lines:
        line_str = line.strip()
        if not line_str:
            story.append(Spacer(1, 4))
            continue
        
        if line_str.startswith('---'):
            story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8, spaceBefore=4))
            continue

        if line_str.startswith('# '):
            clean_txt = clean_markdown_for_reportlab(line_str[2:])
            story.append(Paragraph(clean_txt, title_style))
        elif line_str.startswith('## '):
            clean_txt = clean_markdown_for_reportlab(line_str[3:])
            story.append(Paragraph(clean_txt, h1_style))
        elif line_str.startswith('### '):
            clean_txt = clean_markdown_for_reportlab(line_str[4:])
            story.append(Paragraph(clean_txt, h2_style))
        elif line_str.startswith('* ') or line_str.startswith('- '):
            clean_txt = clean_markdown_for_reportlab(line_str[2:])
            story.append(Paragraph(f"• {clean_txt}", bullet_style))
        else:
            clean_txt = clean_markdown_for_reportlab(line_str)
            story.append(Paragraph(clean_txt, body_style))

    doc.build(story)
    print(f"[✓] Converted: {os.path.basename(md_path)} -> {os.path.basename(pdf_path)}")

def main():
    staging_dir = os.path.expanduser('~/Downloads/SBIR_PROPOSAL_READY')
    os.makedirs(staging_dir, exist_ok=True)
    
    source_dir = os.path.expanduser('~/SovereignNexus/AFWERX_SBIR_Phase_I/volumes')
    md_files = glob.glob(os.path.join(source_dir, '*.md'))

    print("=========================================================================")
    print(" 🚀 SOVEREIGN NEXUS: SBIR PDF CONVERTER ACTIVE 🚀")
    print("=========================================================================")

    for md_file in sorted(md_files):
        filename = os.path.basename(md_file)
        pdf_filename = filename.replace('.md', '.pdf')
        pdf_path = os.path.join(staging_dir, pdf_filename)
        
        # Copy MD to staging
        staged_md = os.path.join(staging_dir, filename)
        with open(md_file, 'r', encoding='utf-8') as src, open(staged_md, 'w', encoding='utf-8') as dst:
            dst.write(src.read())

        markdown_to_pdf(md_file, pdf_path)

    print("=========================================================================")
    print(f" [+] All 6 Volumes successfully converted to PDF in: {staging_dir}")
    print("=========================================================================")

if __name__ == '__main__':
    main()
