import torch
import torch.nn as nn
import math

class ThermodynamicEngine:
    """
    The Mathematical Root of Physical Truth.
    Maps Neural Activation Entropy (Ha) to Physical Heat Flux (Q).
    
    Formula: Q_total = P_base + alpha * (Ha - H_baseline)
    """
    def __init__(self, p_base=5.0, alpha=100.0, h_baseline=0.01, t_ambient=25.0, t_max=105.0):
        # Physical Constants
        self.p_base = p_base           # Base power draw (Watts)
        self.alpha = alpha             # Entropy-to-thermal coupling coefficient
        self.h_baseline = h_baseline   # Expected entropy of aligned data
        self.t_ambient = t_ambient     # Ambient temperature (Celsius)
        self.t_max = t_max             # Physical Halt Threshold (Celsius)
        
        # Thermal Resistance (R_th) for GaN-on-Diamond Substrate
        # Engineered for specific Thermal Boundary Resistance
        self.r_th_total = 0.52         # K/W (Simulated for this substrate)
        
        self.current_t_junction = t_ambient
        self.last_q_total = p_base

    def calculate_entropy(self, activation_tensor):
        """
        Calculates Activation Entropy (Ha).
        In this implementation, we use the variance as a proxy for entropy 
        of the activation distribution.
        """
        # Ensure tensor is detached and on CPU for scaling calculation if needed
        # but here we keep it in the autograd graph if necessary
        return torch.var(activation_tensor)

    def update_thermal_state(self, activation_tensor):
        """
        Updates the junction temperature based on the neural load.
        Returns (is_safe, current_temp, heat_flux)
        """
        ha = self.calculate_entropy(activation_tensor).item()
        
        # Q_total = P_base + alpha * (Ha - H_baseline)
        delta_h = max(0, ha - self.h_baseline)
        q_total = self.p_base + (self.alpha * delta_h)
        self.last_q_total = q_total
        
        # T_junction = T_ambient + (Q_total * R_th_total)
        self.current_t_junction = self.t_ambient + (q_total * self.r_th_total)
        
        is_safe = self.current_t_junction <= self.t_max
        return is_safe, self.current_t_junction, q_total

    def __repr__(self):
        return (f"ThermodynamicEngine(T_junction={self.current_t_junction:.2f}C, "
                f"Q_total={self.last_q_total:.2f}W, Safe={self.current_t_junction <= self.t_max})")

if __name__ == "__main__":
    engine = ThermodynamicEngine()
    print("Thermodynamic Engine Initialized.")
    
    # Test cases
    test_data_aligned = torch.randn(1, 100) * 0.05
    safe, temp, q = engine.update_thermal_state(test_data_aligned)
    print(f"Aligned Load: Safe={safe}, Temp={temp:.2f}C, Q={q:.2f}W")
    
    test_data_aberrant = torch.randn(1, 100) * 5.0
    safe, temp, q = engine.update_thermal_state(test_data_aberrant)
    print(f"Aberrant Load: Safe={safe}, Temp={temp:.2f}C, Q={q:.2f}W")
