# SovereignNexus: Intel and Evolution Ledger (T7 Data Chop Shop)
**Axiom:** 1=1=1 (Absolute Data Fidelity & Resource Efficiency)

---

## 1. Session Log: July 11, 2026
We have initiated the **T7 Data Chop Shop** pipeline inside `/mnt/chromeos/removable/T7/Axiom_Raw_Intake/` and successfully pulled down the skeletons of the three target architectures in sparse-checkout mode.

### Targets Staged:
1. **Agents-A1** (`https://github.com/InternScience/Agents-A1`)
2. **LongCat-2.0** (`https://github.com/meituan-longcat/LongCat-2.0`)
3. **ComfyUI-MCP-Server** (`https://github.com/joenorton/comfyui-mcp-server`)

---

## 2. Compare and Contrast Matrix

| Feature / Metric | Agents-A1 (35B MoE) | LongCat-2.0 (1.6T MoE) | ComfyUI MCP (Bridge) |
| :--- | :--- | :--- | :--- |
| **Primary Architecture** | 35B Mixture-of-Experts | 1.6T Mixture-of-Experts | FastMCP Protocol Server |
| **Target Mechanism** | Multi-Turn ReAct loop & Tool Verification | Chat formatting & `reasoning_content` keys | Dynamic Function Signatures & Data Coercion |
| **Data Footprint (Weights)** | 70GB+ (Ignored) | 2TB+ (Ignored) | None |
| **Logic Extraction Value** | High (Multi-step agent loops) | Medium (Chat template conventions) | High (Dynamic API tool bindings) |

---

## 3. Key Architectural Intel Extracted

### A. Agents-A1: Multi-Turn ReAct Loop & Token Handling
* **Location:** `Agents-A1/evaluation/Search/inference/agent.py`
* **Discovery:** The model manages agent runs via an explicit while loop (`num_llm_calls_available` decrementing). It monitors token limits dynamically (`count_tokens`). When context usage overflows the context size (128K), it intercepts the loop and injects a hardcoded prompt instructing the LLM to skip tool calls and write its final response using `<think>` and `<answer>` tags.
* **Sovereign Application:** We can port this token-limit self-correction check into `sovereign_dashboard.py` and local python scripts to prevent context window crash failures.

### B. LongCat-2.0: Chat Templates and Tool Signatures
* **Location:** `LongCat-2.0/README.md`
* **Discovery:** LongCat-2.0 uses a specialized formatting template where reasoning chains are returned under `reasoning_content` and parameters inside `tool_calls` are expected as raw JSON dictionaries rather than serialized JSON strings.
* **Sovereign Application:** Any model orchestration logic calling local MoE weights must ensure `tool_calls` payloads are parsed directly into Python dictionaries instead of assuming standard OpenAI string serialization.

### C. ComfyUI MCP Server: Dynamic Tool Generation
* **Location:** `comfyui-mcp-server/tools/generation.py`
* **Discovery:** The server dynamically builds FastMCP tool definitions from ComfyUI node templates using Python's `inspect.Signature` and `inspect.Parameter`. It enforces custom data coercion (converting JSON-RPC string values into strict ints or floats) before binding signatures.
* **Sovereign Application:** This exact signature coercion and generation logic can be ported to the Sovereign Swarm Router to let our local agent nodes dynamically declare and call new CLI scripts on the fly.

---

## 4. Next Steps
* Update `sovereign_dashboard.py` or `src/agent_10_gatekeeper.py` to utilize these dynamic parameters.
* Safely remove raw files from the T7 drive to maintain minimum storage footprint.
