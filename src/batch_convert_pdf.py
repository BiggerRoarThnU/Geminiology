import os
import re
from fpdf import FPDF

class BatchPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(100, 110, 120)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}} | SovereignNexus Portfolio", 0, 0, "C")

def clean_unicode_characters(text):
    """
    Replaces non-latin-1 characters with standard ASCII equivalents
    to prevent FPDF Unicode Encoding exceptions.
    """
    replacements = {
        "\u2013": "-",   # en-dash
        "\u2014": "-",   # em-dash
        "\u2018": "'",   # left single quote
        "\u2019": "'",   # right single quote
        "\u201c": '"',   # left double quote
        "\u201d": '"',   # right double quote
        "&ndash;": "-",
        "&mdash;": "-",
        "&rsquo;": "'",
        "&lsquo;": "'",
        "&ldquo;": '"',
        "&rdquo;": '"',
        "™": " (TM)",
        "•": "*",
        "…": "..."
    }
    for orig, rep in replacements.items():
        text = text.replace(orig, rep)
    
    # Remove any other non-ASCII characters just in case
    return text.encode("ascii", "ignore").decode("ascii")

def markdown_to_html(md_text):
    """
    Very basic markdown parsing for fpdf2's write_html module.
    Converts headers, lists, bold text, and double line breaks.
    """
    lines = md_text.split("\n")
    html_lines = []
    in_list = False
    
    for line in lines:
        stripped = line.strip()
        
        # Handle Headers
        if stripped.startswith("# "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f'<h1 align="center"><b>{stripped[2:]}</b></h1><hr>')
            continue
        elif stripped.startswith("## "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f'<h3><b>{stripped[3:]}</b></h3>')
            continue
        elif stripped.startswith("### "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f'<h4><b>{stripped[4:]}</b></h4>')
            continue
        
        # Handle List Items
        if stripped.startswith("* ") or stripped.startswith("- "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            content = stripped[2:]
            html_lines.append(f'<li>{content}</li>')
            continue
        else:
            if in_list and stripped != "":
                # If we were in a list and get text, close list
                html_lines.append("</ul>")
                in_list = False
        
        # Handle Blank Lines (Paragraph dividers)
        if stripped == "":
            html_lines.append("<br>")
        else:
            html_lines.append(stripped)
            
    if in_list:
        html_lines.append("</ul>")
        
    full_html = "<br>".join(html_lines)
    
    # Handle bold elements (**bold**)
    full_html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', full_html)
    
    # Wrap in font tag
    return f'<font face="helvetica" size="10">{full_html}</font>'

def convert_all_markdowns():
    target_dir = "/home/geminiology/Hubstaff_Portfolio_Uploads"
    web_dir = "/home/geminiology/SovereignNexus/Hubstaff_Portfolio_Uploads"
    
    # Create the web output directory if it doesn't exist
    os.makedirs(web_dir, exist_ok=True)
    
    # List all markdown files in the portfolio directory
    files = [f for f in os.listdir(target_dir) if f.endswith(".md")]
    
    print(f"[*] Found {len(files)} markdown files for conversion.")
    
    for filename in files:
        md_path = os.path.join(target_dir, filename)
        pdf_name = filename.replace(".md", ".pdf")
        
        pdf_path_1 = os.path.join(target_dir, pdf_name)
        pdf_path_2 = os.path.join(web_dir, pdf_name)
        
        print(f"[-] Converting {filename} to PDF...")
        
        try:
            with open(md_path, "r", encoding="utf-8", errors="ignore") as f:
                md_content = f.read()
                
            clean_md = clean_unicode_characters(md_content)
            html_content = markdown_to_html(clean_md)
            
            # Setup PDF Document
            pdf = BatchPDF()
            pdf.alias_nb_pages()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            
            # Feed HTML content
            pdf.write_html(html_content)
            
            # Output PDF to both directories
            pdf.output(pdf_path_1)
            pdf.output(pdf_path_2)
            
            # Clean up the original .md file since they are converted
            os.remove(md_path)
            # Also clean up from web root
            web_md_path = os.path.join(web_dir, filename)
            if os.path.exists(web_md_path):
                os.remove(web_md_path)
                
            print(f"[+] SUCCESS: Generated {pdf_name}")
            
        except Exception as e:
            print(f"[ERROR] Failed to convert {filename}: {str(e)}")

if __name__ == "__main__":
    convert_all_markdowns()
