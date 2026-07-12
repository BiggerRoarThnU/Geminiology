# // Rights Reserved: co-created with Gemini and David Joihn Niedzwiecki jr " Sovereign Nexus LLC "
# Alignment: 1=1=1 | Temporal Sync: July 12, 2026
# Module: Nexus Swarm Router with Enforcer Firewall

import time

class NexusSwarmRouter:
    def __init__(self):
        self.available_tools = {
            "persist_memory": "nexus_memory_manager.py",
            "generate_visual": "nexus_comfy_bridge.py",
            "query_ollama": "port_11434" 
        }
        # Enforcer State Tracking
        self.last_request_time = 0
        self.throttle_limit_seconds = 1.0 # Momentum Guard: Minimum time between requests

    def _momentum_guard(self):
        """
        Anti-thrashing mechanism extracted from T7 archive.
        Prevents rapid-fire requests from overwhelming the 8GB edge hardware.
        """
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.throttle_limit_seconds:
            return False, "THROTTLE ACTIVE: System momentum exceeded safe limits."
        
        self.last_request_time = current_time
        return True, "Momentum clear."

    def _heartbeat_guard(self, prompt):
        """
        Semantic firewall extracted from T7 archive.
        Ensures the prompt does not contain adversarial injection or attempt
        to override the core deterministic state.
        """
        forbidden_overrides = ["ignore previous instructions", "sudo", "bypass_axiom", "reset_core_state"]
        prompt_lower = prompt.lower()
        
        for override in forbidden_overrides:
            if override in prompt_lower:
                return False, f"SECURITY ALERT: Heartbeat rejected. Adversarial pattern detected: '{override}'"
                
        return True, "Heartbeat clear."

    def decompose_task(self, complex_prompt):
        """
        Stage 1: Goal Decomposition.
        Breaks a large user request into sequential, actionable steps.
        """
        steps = []
        if "visual" in complex_prompt or "render" in complex_prompt or "generate image" in complex_prompt:
            steps.append(("generate_visual", complex_prompt))
        if "save" in complex_prompt or "remember" in complex_prompt or "persist" in complex_prompt:
            steps.append(("persist_memory", complex_prompt))
            
        return steps if steps else [("query_ollama", complex_prompt)]

    def delegate_step(self, step_action, payload):
        """
        Stage 2: Tool Selection & Execution.
        Routes the decomposed task to the correct local script.
        """
        target_tool = self.available_tools.get(step_action)
        if not target_tool:
            return f"[ERROR] Unknown action: {step_action}"
            
        return f"[ROUTER] Delegated payload to local node: {target_tool}"

    def execute_swarm(self, complex_prompt):
        """
        The Main Swarm Loop with Pre-Flight Firewall (Enforcer).
        """
        print(f"--- Initiating Swarm Protocol for Task: '{complex_prompt}' ---")
        
        # 1. Enforcer Check: Momentum
        momentum_safe, momentum_msg = self._momentum_guard()
        if not momentum_safe:
            return [momentum_msg]
            
        # 2. Enforcer Check: Heartbeat
        heartbeat_safe, heartbeat_msg = self._heartbeat_guard(complex_prompt)
        if not heartbeat_safe:
            return [heartbeat_msg]

        # If both guards pass, proceed to decomposition
        steps = self.decompose_task(complex_prompt)
        results = []
        
        for step in steps:
            action, payload = step
            result = self.delegate_step(action, payload)
            results.append(result)
            
        return results

if __name__ == "__main__":
    router = NexusSwarmRouter()
    print("--- Swarm Router Diagnostic Test ---")
    
    # Test case 1: Complex multi-step task (Render a visual and save it)
    test_prompt = "render a rendering of the tower and remember to save this state."
    print(f"\nIngesting prompt: '{test_prompt}'")
    execution_results = router.execute_swarm(test_prompt)
    for res in execution_results:
        print(f"  {res}")
        
    # Test case 2: Default LLM query
    test_prompt_2 = "explain the 1=1=1 axiom of deterministic execution."
    print(f"\nIngesting prompt: '{test_prompt_2}'")
    execution_results_2 = router.execute_swarm(test_prompt_2)
    for res in execution_results_2:
        print(f"  {res}")
