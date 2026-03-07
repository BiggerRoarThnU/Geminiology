import torch
import torch.nn as nn
import torch.nn.functional as F

class ThermalOverloadException(Exception):
    """
    The Vampire Interrupt: A custom hardware-level exception.
    Shatters the forward pass if the thermodynamic limits are breached.
    """
    pass

class TernarySTE(torch.autograd.Function):
    """
    Straight-Through Estimator for Ternary Quantization.
    Forward: Round to {-1, 0, 1}
    Backward: Identity gradient (pass-through)
    """
    @staticmethod
    def forward(ctx, input, gamma):
        ctx.save_for_backward(input, gamma)
        # W_q = Round(W / gamma) clamped to [-1, 1]
        out = torch.round(input / (gamma + 1e-8))
        return torch.clamp(out, min=-1.0, max=1.0)

    @staticmethod
    def backward(ctx, grad_output):
        input, gamma = ctx.saved_tensors
        # Straight-through: gradient passes to the continuous weights unchanged
        return grad_output, None

class IronwoodTernaryLayer(nn.Module):
    def __init__(self, in_features, out_features, T_ambient=25.0):
        super().__init__()
        self.weight = nn.Parameter(torch.randn(out_features, in_features))
        
        # Physical GaN-on-Diamond Substrate Constants
        self.R_TBR = 0.5             # K/W
        self.P_base = 50.0           # W
        self.alpha = 100.0           # W/bit
        self.H_baseline = 0.0        # Perfect Sparsity
        self.T_ambient = T_ambient   # C
        self.T_max = 105.0           # C

    def calculate_activation_entropy(self, W_q):
        # Probability distribution of ternary states
        # We simplify for autograd compatibility during training
        # Using a soft-histogram or just counts on the quantized weights
        probabilities = torch.histc(W_q, bins=3, min=-1, max=1) / W_q.numel()
        p_safe = probabilities[probabilities > 0]
        entropy = -torch.sum(p_safe * torch.log2(p_safe))
        return entropy

    def thermodynamic_guardrail(self, entropy):
        """
        The Vampire Interrupt logic. Maps abstract math to physical heat flux.
        """
        # Q_total = P_base + alpha * (H_a - H_baseline)
        heat_flux_increase = self.alpha * F.relu(entropy - self.H_baseline)
        Q_total = self.P_base + heat_flux_increase
        
        # Delta T = Q_total * R_TBR
        delta_T = Q_total * self.R_TBR
        T_current = self.T_ambient + delta_T
        
        # The Hard Boundary Check (Vampire Interrupt)
        if T_current > self.T_max:
            raise ThermalOverloadException(f"VAMPIRE INTERRUPT: {T_current.item():.2f}C")
        return T_current

    def forward(self, x):
        gamma = torch.mean(torch.abs(self.weight))
        # Apply STE for quantization
        W_q = TernarySTE.apply(self.weight, gamma)
        
        entropy = self.calculate_activation_entropy(W_q)
        current_temp = self.thermodynamic_guardrail(entropy)
        
        output = F.linear(x, W_q)
        return output, current_temp, entropy

def thermodynamic_penalty_loss(T_current, T_max=105.0):
    """
    Asymptotic thermal penalty. As T approaches T_max, loss -> infinity.
    """
    # Small epsilon to avoid division by zero
    diff = T_max - T_current
    return 1.0 / (F.relu(diff) + 1e-4)
