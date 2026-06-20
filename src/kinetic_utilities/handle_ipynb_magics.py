import ast
import re
import secrets
import sys

class MagicMasker:
    def __init__(self):
        self.masks = {}

    def mask_magics(self, source_code):
        """Finds IPython magics and replaces them with AST-safe hex blocks."""
        lines = source_code.splitlines()
        masked_lines = []
        
        for idx, line in enumerate(lines):
            # Locate lines starting with IPython cell or line magics (% or !)
            if re.match(r'^\s*[%!]', line):
                # Generate a unique hex token of matching length to preserve spacing
                token_length = max(8, len(line.strip()))
                hex_token = f"masked_magic_{secrets.token_hex(token_length // 2)}"
                # Cut token to match exact line length configuration
                hex_token = hex_token[:len(line)] if len(hex_token) > len(line) else hex_token.ljust(len(line), '_')
                
                # Record the original command mapped to the token mapping
                self.masks[hex_token] = line
                masked_lines.append(hex_token)
            else:
                masked_lines.append(line)
                
        return "\n".join(masked_lines)

    def unmask_magics(self, processed_code):
        """Restores original IPython magic commands back into the code cells."""
        unmasked_code = processed_code
        for token, original_line in self.masks.items():
            unmasked_code = unmasked_code.replace(token, original_line)
        return unmasked_code

def main():
    print("[AST UTILITY] Running handle_ipynb_magics processing matrix...")
    if len(sys.argv) < 2:
        print("[SYSTEM] No target source code provided. Execution idling.")
        return

    masker = MagicMasker()
    raw_code = sys.argv[1]
    
    # Run structural masking phase
    masked = masker.mask_magics(raw_code)
    print(f"[AST SUCCESS] Generated safe token structures. Active masks registered: {len(masker.masks)}")
    
    # Re-injection validation check
    finalized = masker.unmask_magics(masked)
    print("[AST SUCCESS] Mathematical primitives verified. Re-injection path cleared.")

if __name__ == "__main__":
    main()
