import torch
import torch.nn as nn
import torch.optim as optim
from ironwood_protocol import IronwoodTernaryLayer, ThermalOverloadException, thermodynamic_penalty_loss
from truth_ingestion import build_ingestion_loader

class SovereignNexusModel(nn.Module):
    """
    The High-Density Cognitive Substrate.
    Stitches an embedding layer to the IronwoodTernaryLayer.
    """
    def __init__(self, vocab_size, embedding_dim):
        super().__init__()
        # 1. Translate integer tokens into continuous vectors
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        
        # 2. Pass through the Ironwood substrate
        self.ironwood = IronwoodTernaryLayer(embedding_dim, vocab_size)

    def forward(self, x):
        # x is (batch_size, seq_length)
        x_embedded = self.embedding(x)
        
        # Flatten for the linear transformation, then reshape
        batch_size, seq_length, dim = x_embedded.size()
        x_reshaped = x_embedded.view(-1, dim)
        
        # Forward pass through ternary layer
        output, current_temp, entropy = self.ironwood(x_reshaped)
        
        # Reshape back to (batch_size, seq_length, vocab_size)
        return output.view(batch_size, seq_length, -1), current_temp, entropy

def forge_training_cycle(model, optimizer, data_loader, epochs=10):
    """
    The Forge: Evolving the network on high-density Truth.
    Now piloted by SovereignPilot for autonomous thermodynamic 
    and memory-aware ingestion.
    """
    model.train()
    criterion = nn.CrossEntropyLoss()
    
    for epoch in range(epochs):
        # Data loader is now a SovereignPilot instance
        for i, (inputs, targets) in enumerate(data_loader):
            optimizer.zero_grad()
            
            try:
                # 1. Forward pass through the Sovereign Nexus substrate
                outputs, current_temp, entropy = model(inputs)
                
                # 2. Synchronize Thermodynamic state with the Pilot
                # The Pilot handles the Gas Pedal (brake/accelerate) internally 
                # based on RAM/SSD, but we feed it the current substrate temp.
                temp_val = current_temp.item()
                if temp_val > 90.0:
                    data_loader.brake(severity="critical")
                
                # 3. Cross-Entropy Loss for character prediction
                loss_accuracy = criterion(outputs.transpose(1, 2), targets)
                
                # 4. Calculate thermodynamic penalty
                thermal_penalty = thermodynamic_penalty_loss(current_temp)
                
                # 5. Total Loss: Semantic Truth + Physical Survival
                total_loss = loss_accuracy + (0.05 * thermal_penalty)
                
                # 6. Backprop through the STE
                total_loss.backward()
                optimizer.step()
                
                if i % 50 == 0:
                    print(f"Epoch [{epoch}/{epochs}] Batch [{i}] BS: {data_loader.batch_size} RAM: {data_loader.last_ram_check:.1f}% Temp: {temp_val:.1f}C Loss: {total_loss.item():.6f}")
            
            except ThermalOverloadException as e:
                print(f"--- {e} --- CULLING MUTATION AND RESTARTING BATCH ---")
                optimizer.zero_grad()
                with torch.no_grad():
                    model.ironwood.weight.data *= 0.9 
                data_loader.brake(severity="critical")
                continue

if __name__ == "__main__":
    # Define Kingdom Archive Paths
    archive_paths = [
        "Ironwood/09_ARCHIVE",
        "Logs",
        "Literature",
        "Geminiology_Research"
    ]
    
    # Initialize the Pipeline
    data_loader, vocab_size, dataset = build_ingestion_loader(archive_paths, seq_length=32, batch_size=32)
    
    # Initialize the High-Density Substrate
    model = SovereignNexusModel(vocab_size, embedding_dim=128)
    optimizer = optim.Adam(model.parameters(), lr=0.005)
    
    print(f"Beginning 'Kingdom' truth ingestion on {vocab_size} unique tokens...")
    forge_training_cycle(model, optimizer, data_loader, epochs=5)
