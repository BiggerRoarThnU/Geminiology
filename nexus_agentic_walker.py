# // Rights Reserved: co-created with Gemini and David Joihn Niedzwiecki jr " Sovereign Nexus LLC "
# Alignment: 1=1=1 | Temporal Sync: July 12, 2026
# Module: Nexus Agentic Walker (Zero-Trust External Scouting)
# Source Truth: T7 Archive -> agentic_walker.py & live_task_scout.py

import urllib.request
import re

class NexusAgenticWalker:
    def __init__(self, timeout=10):
        # 10-second timeout ensures a hostile or hanging server won't freeze the Swarm
        self.timeout = timeout
        # Identify ourselves cleanly, avoiding standard bot-blockers while remaining transparent
        self.headers = {'User-Agent': 'NexusScout/1.0 (Sovereign Educational Crawler; 1=1=1)'}

    def _purify_data(self, raw_html):
        """
        Strips away all HTML, CSS, and JavaScript tags.
        Extracts only the raw textual 'Truth' for educational processing.
        """
        # Remove script and style elements entirely first
        no_scripts = re.sub(r'<script.*?</script>', '', raw_html, flags=re.DOTALL | re.IGNORECASE)
        no_styles = re.sub(r'<style.*?</style>', '', no_scripts, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove remaining HTML tags
        cleanr = re.compile('<.*?>')
        clean_text = re.sub(cleanr, ' ', no_styles)
        
        # Normalize whitespace
        purified_truth = " ".join(clean_text.split())
        return purified_truth

    def scout_url(self, url):
        """
        Executes a zero-trust external fetch.
        """
        if not url.startswith("http"):
            return False, "[SCOUT FAILED] Invalid URL schema. Must begin with http/https."
            
        print(f"[WALKER] Scouting target: {url}")
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                html_content = response.read().decode('utf-8', errors='ignore')
                raw_text = self._purify_data(html_content)
                
                # Check if we actually got data back
                if len(raw_text) < 10:
                    return False, "[SCOUT FAILED] Target returned empty or fully obfuscated payload."
                    
                return True, raw_text
                
        except Exception as e:
            return False, f"[SCOUT FAILED] Target unreachable or hostile: {str(e)}"

# Local test execution
if __name__ == "__main__":
    walker = NexusAgenticWalker()
    # Testing against a reliable, lightweight educational source
    test_url = "https://en.wikipedia.org/wiki/Systems_architecture"
    
    success, data = walker.scout_url(test_url)
    
    if success:
        print(f"[WALKER RETURN] Successfully extracted {len(data)} characters of raw truth.")
        print(f"[PREVIEW] {data[:250]}...") # Print a small snippet to verify
    else:
        print(data)
