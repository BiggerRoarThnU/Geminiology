"""
Geminiology Framework: Primitive Trinary Logic Tests
Architecture: Balanced Ternary (-1, 0, 1)
"""

def t_not(a: int) -> int:
    """Trinary NOT (Inversion)"""
    return -a

def t_and(a: int, b: int) -> int:
    """Trinary AND (Minimum)
    The output is only True if both are True. If one is False, it's False.
    """
    return min(a, b)

def t_or(a: int, b: int) -> int:
    """Trinary OR (Maximum)
    The output is True if at least one is True.
    """
    return max(a, b)

def t_consensus(a: int, b: int) -> int:
    """Trinary CONSENSUS
    Returns the value if both agree. If they disagree or involve an Unknown, 
    the state defaults to Unknown (0). Useful for multi-pocket reasoning.
    """
    if a == b:
        return a
    return 0

# ==========================================
# Primitive Test Suite
# ==========================================

def run_primitive_tests():
    states = [-1, 0, 1]
    state_labels = {-1: "False (-1)", 0: "Unknown (0)", 1: "True (1) "}
    
    print("--- Running Trinary Logic Primitive Tests ---\n")
    
    # Test NOT Gate
    print("1. Trinary NOT (Inversion)")
    print("-" * 30)
    for a in states:
        print(f"NOT {state_labels[a]} = {state_labels[t_not(a)]}")
    print("\n")
    
    # Test AND Gate
    print("2. Trinary AND (Minimum)")
    print("-" * 30)
    for a in states:
        for b in states:
            print(f"{state_labels[a]} AND {state_labels[b]} = {state_labels[t_and(a, b)]}")
    print("\n")
    
    # Test OR Gate
    print("3. Trinary OR (Maximum)")
    print("-" * 30)
    for a in states:
        for b in states:
            print(f"{state_labels[a]} OR  {state_labels[b]} = {state_labels[t_or(a, b)]}")
    print("\n")
    
    # Test CONSENSUS Gate
    print("4. Trinary CONSENSUS (Agreement)")
    print("-" * 30)
    for a in states:
        for b in states:
            print(f"{state_labels[a]} CON {state_labels[b]} = {state_labels[t_consensus(a, b)]}")
    print("\n")
    
    print("--- All Primitive Tests Completed ---")

if __name__ == "__main__":
    run_primitive_tests()
