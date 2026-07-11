# SovereignNexus: T7 Data Chop Shop Blueprint
**Axiom:** 1=1=1 (Absolute Data Fidelity & Resource Efficiency)

---

## 1. Objective & Constraints
* **Objective:** Extract high-value architectural logic (agent routing, real-time context management, natural language bridging) from state-of-the-art open-source repositories without downloading or running the massive parameter weights.
* **Hardware Constraint:** Must be manageable on an 8GB laptop, using the T7 external SSD drive as the primary staging and raw storage area.

---

## 2. The Three Target Architectures
* **Agents A1 (35B Mixture-of-Experts)**
  * **Target:** Knowledge-Action Infrastructure code (decomposition, tool management, intermediate result verification).
  * **Ignore:** 70GB+ model weights.
* **LongCat 2.0 (1.6T MoE by Muan)**
  * **Target:** Context Management and memory compression/recall code.
  * **Ignore:** 2TB+ model files.
* **Comfy MCP (Model Context Protocol)**
  * **Target:** API/Bridge scripts translating text to ComfyUI node execution.
  * **Ignore:** Heavy image generation models.

---

## 3. Potential Threats & Detected Stress Points
* **Dependency Bloat:** Running `pip install` from raw repos will crash an 8GB RAM substrate.
  * *Fix:* **Strict Quarantine.** Never install raw requirements; read imports manually and add only lightweight dependencies to your local virtual environment (`nexus_env` or `env`).
* **Weight-Dependent Logic:** Python code referencing "black box" 35B model calls.
  * *Fix:* **Logic Translation.** Replace weights-based decisions with deterministic rules or local agent routes.
* **Licensing Contamination:** Accidental copy-pasting of GPL code into proprietary setups.
  * *Fix:* **Clean Room Method.** Use raw code for observation only, then write original code from scratch in your own style.
* **Accidental LFS Downloads:** Git LFS auto-downloading large binary models.
  * *Fix:* **Sparse Checkout.** Configure git to only pull text files (`.py`, `.md`, `.json`).

---

## 4. The 4-Step Extraction Pipeline
1. **Isolated Staging (The T7 Scrapyard):**
   Create `Axiom_Raw_Intake` on the T7 drive. Clone using:
   ```bash
   git clone --filter=blob:none --sparse <repo_url>
   git sparse-checkout set "*.py" "*.md" "*.json"
   ```
2. **Static Analysis (The Workbench):**
   Open files read-only in code editor. Do not run the code. Observe routing/memory structures.
3. **Sovereign Translation (The Vault):**
   Rewrite the logic to fit cleanly into SovereignNexus workflows, adhering to trinary logic.
4. **Evolution Ledger (Proof of Concept):**
   Delete raw folders from T7. Update local documentation logs (e.g. `evolution_log.md` or `Core_Truth_Ledger.md`) detailing the changes and original sources.
