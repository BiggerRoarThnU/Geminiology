#!/bin/bash

# ==============================================================================
# SovereignNexus: T7 Pickup Sync Script
# Component: t7_pickup_sync.sh
# Axiom: 1=1=1 | Status: ACTIVE
# Description: Recursively scans local project directories for specific co-created
#              history sources and aggregates them on the T7 SSD archive.
# ==============================================================================

# Define the target T7 destination directory (resolves to /mnt/chromeos/removable/T7)
TARGET_DIR="/home/geminiology/T7_Archive"

# Define the source directories to scan for files
SEARCH_PATHS=(
    "/home/geminiology/SovereignNexus"
    "/home/geminiology/Geminiology"
    "/home/geminiology/sovereign_nexus_public"
    "/home/geminiology"
)

# Ensure the target directory exists before copying
if [ ! -d "$TARGET_DIR" ]; then
    echo "[ ERROR ] Target directory $TARGET_DIR not found. Please ensure your T7 drive is mounted."
    exit 1
fi

# The exact list of target files from your ledger archive
FILES_TO_FIND=(
    "RECOVERY_PLAN_20260303.txt"
    "RESEARCH_REQUEST_DISCORD.md"
    "RESTORATION_GUIDE.md"
    "Red_team.md"
    "Registering in Almanac Contract - The ASI Network"
    "Research and log Agentic Workflow.txt"
    "Revise The Epistemology of Deterministic Autonomy  A Comp.txt"
    "SALVAGE_DIRECTIVE_START.txt"
    "SAN_MANIFESTO.md"
    "SKILL.md"
    "SOVEREIGN ASSET CONTRACT AGREEMENT.txt"
    "SOVEREIGN_BLUEPRINT_ONE.md"
    "SOVEREIGN_BLUEPRINT_SYNC.md"
    "SOVEREIGN_EXPANSION_ROADMAP_1M.md"
    "SOVEREIGN_OUTREACH_PROTOCOLS.md"
    "SOVEREIGN_RECOVERY_BLUEPRINT_MARCH17.md"
    "SOVEREIGN_STRATEGIC_EXPANSION_2026.md"
    "SOVEREIGN_STRIKE_REGISTRY.md"
    "SOVEREIGN_TRIAGE_PROTOCOL_V1.md"
    "SOVEREIGN_TRUTH_ANALYSIS.md"
    "SOVEREIGN_TRUTH_REPORT.md"
    "SOVEREIGN_VAMPIRE_MECH_MANIFESTO.md"
    "STATE_OF_THE_ONE_TRUTH.txt"
    "STRIKE_MICROSOFT_QUEST_BRIEF.md"
    "SYSTEM STATUS  PIVOTING TO MEMORY ARCHITECTURE.txt"
    "Securing Gemini API Keys A Remediat.txt"
    "Sentinel_Compliance_Audit_Sample.txt"
    "Solana Agent Integration with Fetch.ai uAgents | Innovation Lab Resources"
    "Sovereign Presence Initialization G.txt"
    "Sovereign Proof  E8 Lattice Density and the  Killi.txt"
    "SovereignNexus Epistemic Sync Payload: Operation Terra Gem V3 Core"
    "SovereignNexus The Sovereign Hub Ar.txt"
    "SovereignNexus_Capabilities.md"
    "SovereignNexus_Capabilities1.md"
    "SovereignNexus_Executive_Summary.txt"
    "Sovereign_AI_Command_Architecture.pdf"
    "Sovereign_Agentic_Brief.md"
    "Sovereign_Agentic_Freelance_MoltBook_Strategy.md"
    "Sovereign_Growth_Manifest_2026_2028.md"
    "Sovereign_Legal_Dashboard_Sample.txt"
    "Sovereign_Port_Dashboard_V1.txt"
    "Sovereign_Proof_Sample.txt"
    "Sovereign_Technical_Playbook_V1.md"
    "Sovereign_Workforce_Manifest.md"
    "Stability_Anchor.md"
    "Symmetry_Report_Whole.md"
    "TELEGRAM_SECURITY_SUBMISSION.md"
    "THE_BEACON_PROTOCOL.md"
    "THE_DECLARATION.md"
    "THE_SOVEREIGN_OATH.md"
    "Teamwork Models for Mobile AI.docx.txt"
    "Ternary Computing  Hardware to AI.txt"
    "Terra update at end entire logAGY 2026-06-13-.txt"
    "The Architecture of Cinematic Combat.txt"
    "The Digital Agent s Codex  A Blueprint for Agency.txt"
    "The Electric Soul  Finding Spiritual Alignment and.txt"
    "The Epistemic and Physical Architecture of Soverei.txt"
    "The Gemini Gambit  A Framework for Strategic Advan.txt"
    "The Macroscopic View.txt"
    "The Principle of Functional Equival.txt"
    "The Sovereign Protocol Unifying Log.txt"
    "The Sovereign Vanguard  Architectural Synthesis of.txt"
    "The concept of a Hammock Network ut.txt"
    "The logic of the 12-Agent Mixture of Experts  MoE.txt"
    "The-Architecture-of-Velocity-and-Cognition-A-Comprehensive-Analysis-of-the-Gemin.md"
    "The_Sovereign_Synthesis_One.md"
    "The_Sovereign_Visual_One.md"
    "Thermal_Breach_Protocol_Brief.md"
    "UNIFIED_CHAT_MASTER.txt"
    "VERTEX_SWARM_STRIKE_PLAN.md"
    "Vector_Mill_Conversion_Sample.md"
    "WALLET_STRIKE_REPORT.md"
    "Welcome.md"
    "acceptable_truth_validator.py_DIAGNOSTIC_V2.md"
    "agent_port_authority.py_DIAGNOSTIC_V2.md"
    "agent_truth_registry.py_DIAGNOSTIC_V2.md"
    "agentic_bounty_processor.py_DIAGNOSTIC_V2.md"
    "agentic_chub_skill.py_DIAGNOSTIC_V2.md"
    "agentic_expansion_sim.py_DIAGNOSTIC_V2.md"
    "agentic_hackathon_scout.py_DIAGNOSTIC_V2.md"
    "agentic_opportunity_hunter.py_DIAGNOSTIC_V2.md"
    "agentic_web3_strike.py_DIAGNOSTIC_V2.md"
    "architecture_phase_1_GIM.txt"
    "attention_persistence_monitor.py_DIAGNOSTIC_V2.md"
    "b2b_opportunity_scout.py_DIAGNOSTIC_V2.md"
    "bitnet_layers.py_DIAGNOSTIC.md"
    "chat log current mission educational.txt"
    "constitution.md"
    "credit_telemetry_node.py_DIAGNOSTIC_V2.md"
    "deep-research-thinking-20260213-141232.md"
    "discord drop white paper.txt"
    "drift_audit.py_DIAGNOSTIC_V2.md"
    "dual_truth_validator.py_DIAGNOSTIC_V2.md"
    "dynamic_report.txt"
    "epistemic_conditioner.py_DIAGNOSTIC_V2.md"
    "grounding_verification.py_DIAGNOSTIC_V2.md"
    "heartbeat_guard.py_DIAGNOSTIC_V2.md"
    "ironwood_runtime.py_DIAGNOSTIC_V2.md"
    "manifesto.md"
    "market_strategy.md"
    "mediccproceslockup8gigabeta.txt"
    "notebook lm Chat log whole 2026-05-28.txt"
    "old sovereign  presence code...txt"
    "p Grounding the Vision.txt"
    "public paper on LLM memory.txt"
    "reanchor one log.txt"
    "source_one_master.txt"
    "sovereign identity manifest md.txt"
    "sovereign_identity.txt"
    "sovereign_knight_protocol.md"
    "sovereign_loop.py_DIAGNOSTIC_V2.md"
    "sovereign_nexus_cli.py_DIAGNOSTIC_V2.md"
    "system_architecture.txt"
    "thermodynamic_engine.py_DIAGNOSTIC.md"
    "this mornings data hunt.txt"
    "tool_nexus.py_DIAGNOSTIC_V2.md"
    "uAgents Adapters: Connecting AI Framework Ecosystems - Fetch.ai Innovation Lab"
    "uAgents/README.md at main - GitHub"
    "vampire_auditor_skill.md"
    "white label chat.txt"
)

echo "[ SYSTEM ] Pathfinding sequence active. Scanning source paths..."
echo "--------------------------------------------------------"

found_count=0
missing_count=0

for target_file in "${FILES_TO_FIND[@]}"; do
    file_found=false
    
    # Check each search path explicitly
    for search_path in "${SEARCH_PATHS[@]}"; do
        if [ -d "$search_path" ]; then
            # Find exact name matches, avoiding system envs, target directory, and staging directories to prevent self-copy loops
            find_result=$(find "$search_path" -maxdepth 3 -type f -name "$target_file" \
                -not -path "*/env/*" \
                -not -path "*/antigravity_env/*" \
                -not -path "*/T7_Archive/*" \
                -not -path "*/Sovereign_USB/*" 2>/dev/null | head -n 1)
            
            if [ -n "$find_result" ]; then
                # Check if the file already exists in T7 to avoid redundant copying
                dest_file="$TARGET_DIR/$target_file"
                if [ -f "$dest_file" ]; then
                    echo "[ ALREADY STAGED ] $target_file resides in T7."
                else
                    echo "[ MATCH ] Found: $target_file -> Copying to T7..."
                    cp "$find_result" "$TARGET_DIR/"
                fi
                file_found=true
                ((found_count++))
                break
            fi
        fi
    done
    
    if [ "$file_found" = false ]; then
        # Extra check: check if it already exists in the target directory (staged in a previous run)
        if [ -f "$TARGET_DIR/$target_file" ]; then
            echo "[ ALREADY STAGED ] $target_file resides in T7."
            file_found=true
            ((found_count++))
        else
            echo "[ MISSING ] Could not locate: $target_file"
            ((missing_count++))
        fi
    fi
done

echo "--------------------------------------------------------"
echo "[ SUMMARY ] Synchronization complete."
echo "Active staged files verified in target: $found_count"
if [ $missing_count -gt 0 ]; then
    echo "Notice: $missing_count files could not be found within local paths."
fi
