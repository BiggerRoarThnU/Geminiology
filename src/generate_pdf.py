import os
from fpdf import FPDF

class ResumePDF(FPDF):
    def header(self):
        # We can draw a subtle border or line if needed
        pass
        
    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(100, 110, 120)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}} | SovereignNexus LLC", 0, 0, "C")

def build_resume():
    pdf = ResumePDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # Enable auto page breaks
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Resume content in clean, parseable HTML
    html_content = """
    <font face="helvetica">
    <h1 align="center"><b>DAVID JOHN NIEDZWIECKI JR.</b></h1>
    <p align="center"><b>Principal AI Systems Architect & Backend Developer</b><br>
    Founder, SovereignNexus LLC<br>
    Location: New Bern, North Carolina<br>
    GitHub: <a href="https://github.com/BiggerRoarThnU/Geminiology">github.com/BiggerRoarThnU/Geminiology</a></p>
    
    <hr>
    
    <h3><b>PROFESSIONAL SUMMARY</b></h3>
    <p>A highly technical, execution-focused backend developer and systems architect specializing in deterministic AI deployments, secure local API gateways, and robust data automation. Founder of SovereignNexus LLC, dedicated to building zero-trust digital infrastructure, orchestrating multi-agent Large Language Model (LLM) pipelines, and engineering air-gapped environments that prioritize data sovereignty, compliance, and operational efficiency.</p>
    
    <h3><b>CORE COMPETENCIES</b></h3>
    <ul>
        <li><b>Languages & Environments:</b> Python, Bash/Shell Scripting, Linux (Ubuntu/Debian), Git.</li>
        <li><b>AI & Machine Learning:</b> Local LLM Deployment (Ollama, vLLM, Qwen, Gemma, Llama), Prompt Filtration, Multi-Agent Orchestration.</li>
        <li><b>Backend Engineering:</b> FastAPI, REST API Development, JSON-RPC 2.0, System Telemetry, SQLite, Data Automation.</li>
        <li><b>System Architecture:</b> Zero-Trust Security, Automated Rsync Backup, Hardware/Thermal Telemetry Daemons.</li>
    </ul>
    
    <h3><b>PROFESSIONAL EXPERIENCE</b></h3>
    <p><b>SovereignNexus LLC</b> - New Bern, NC<br>
    <b>Principal AI Systems Architect & Founder</b> | <i>March 2026 - Present</i></p>
    <ul>
        <li><b>AI Architecture & Local Deployment:</b> Designed and implemented the "Geminiology" framework, a multi-agent AI environment running completely air-gapped on local edge hardware substrates.</li>
        <li><b>Security & Data Sovereignty:</b> Engineered prompt-injection defense layers and middleware proxies (sovereign_defense_core.py) that sanitize inputs using regex and check outputs via vector similarity.</li>
        <li><b>Backend API Integration:</b> Built custom Python/FastAPI wrappers (oracle_server.py) to wrap local model execution (Ollama) in a REST API, enabling secure internal query processing with zero external API fees.</li>
        <li><b>System Automation & Health:</b> Developed metabolic governor loops (sovereign_loop.py) and custom telemetry tools (tools.py) to monitor CPU, RAM, and thermal thresholds, auto-throttling active runs to protect hardware.</li>
        <li><b>Log & Data Processing:</b> Engineered high-throughput rsync backup scripts (master_t7_sync.sh) to mirror 8.5+ GB of files and logs to external solid-state storage.</li>
    </ul>
    
    <h3><b>EDUCATION & CERTIFICATIONS</b></h3>
    <ul>
        <li><b>Google AI Professional Tracks:</b> Local open-source model optimization, prompt engineering, and API gateways.</li>
        <li><b>Coursera AI Fundamentals & Python Programming:</b> Modules in data processing, database management, and scripting.</li>
    </ul>
    </font>
    """
    
    # Write the HTML to the PDF
    pdf.write_html(html_content)
    
    # Save the output file
    output_path = "/home/geminiology/David_Niedzwiecki_Resume.pdf"
    pdf.output(output_path)
    print(f"[SUCCESS] PDF successfully generated at {output_path}")

if __name__ == "__main__":
    build_resume()
