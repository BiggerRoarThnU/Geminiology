import numpy as np
import random

class VampireBatOptimizer:
    """
    Vampire Bat Optimization (VBO) for Autotelic Evolution.
    A Swarm-Intelligence algorithm based on reciprocal altruism 
    and echolocation (Exploration/Exploitation).
    
    Includes 'Blood Sharing' (Collaboration) and 'Resting' (Sparsity/Energy Conservation).
    """
    def __init__(self, objective_function, n_bats=20, n_dims=10, 
                 max_iter=100, x_min=-1.0, x_max=1.0):
        self.objective_function = objective_function # Function to minimize (or maximize)
        self.n_bats = n_bats                         # Swarm Size
        self.n_dims = n_dims                         # Dimensionality of the problem
        self.max_iter = max_iter                     # Maximum Generations
        
        self.x_min = x_min
        self.x_max = x_max
        
        # Initialize Bats (Population)
        self.bats = np.random.uniform(x_min, x_max, (n_bats, n_dims))
        self.bat_fitness = np.zeros(n_bats)
        
        # Initial Velocities and Echolocation parameters
        self.velocities = np.zeros((n_bats, n_dims))
        self.frequencies = np.zeros(n_bats)
        self.loudness = np.ones(n_bats)
        self.pulse_rate = np.zeros(n_bats)
        
        self.g_best_x = None
        self.g_best_fitness = float('inf') # Minimization
        
        self.fitness_history = []

    def blood_share(self, i, j):
        """
        The Reciprocal Altruism Mechanism.
        A 'Fed' bat shares blood (information) with a 'Starving' bat.
        """
        # Linear interpolation between a strong bat and a weak bat
        self.bats[i] = self.bats[i] + (self.bats[j] - self.bats[i]) * random.uniform(0, 0.5)

    def resting(self, i):
        """
        Sparsity/Energy Conservation mechanism (Resting state).
        Randomly zeroes out dimensions to mimic BitNet 0-state sparsity.
        """
        sparsity_ratio = 0.2
        mask = np.random.choice([0, 1], size=self.n_dims, p=[sparsity_ratio, 1-sparsity_ratio])
        self.bats[i] *= mask

    def optimize(self):
        """
        Main Optimization Loop.
        """
        print(f"VBO Start: Bats={self.n_bats}, Dimensions={self.n_dims}, Iterations={self.max_iter}")
        
        # Initial Evaluation
        for i in range(self.n_bats):
            self.bat_fitness[i] = self.objective_function(self.bats[i])
            if self.bat_fitness[i] < self.g_best_fitness:
                self.g_best_fitness = self.bat_fitness[i]
                self.g_best_x = self.bats[i].copy()
                
        # Main Loop
        for iteration in range(self.max_iter):
            for i in range(self.n_bats):
                # 1. Update Echolocation (Frequency, Velocity, Position)
                self.frequencies[i] = random.uniform(0, 2)
                self.velocities[i] += (self.bats[i] - self.g_best_x) * self.frequencies[i]
                new_bat_x = self.bats[i] + self.velocities[i]
                
                # 2. Local Search (Exploitation)
                if random.random() > self.pulse_rate[i]:
                    new_bat_x = self.g_best_x + 0.01 * np.random.randn(self.n_dims)
                
                # Boundary constraints
                new_bat_x = np.clip(new_bat_x, self.x_min, self.x_max)
                
                # 3. Acceptance Criteria (Loudness)
                new_fitness = self.objective_function(new_bat_x)
                if (new_fitness <= self.bat_fitness[i]) and (random.random() < self.loudness[i]):
                    self.bats[i] = new_bat_x
                    self.bat_fitness[i] = new_fitness
                    
                    # Update parameters (Decrease Loudness, Increase Pulse Rate)
                    # alpha=0.9, gamma=0.9
                    self.loudness[i] *= 0.9
                    self.pulse_rate[i] = (1.0 - np.exp(-0.9 * iteration))
                
                # 4. Social Interaction: Blood Sharing
                # If a bat is in the top 10% fitness, share blood with a random weak bat
                if self.bat_fitness[i] < np.percentile(self.bat_fitness, 10):
                    weak_idx = np.argmax(self.bat_fitness)
                    self.blood_share(weak_idx, i)
                
                # 5. The Sparsity Mechanic: Resting
                if random.random() < 0.1: # 10% chance to rest
                    self.resting(i)
                
                # 6. Global Update
                if self.bat_fitness[i] < self.g_best_fitness:
                    self.g_best_fitness = self.bat_fitness[i]
                    self.g_best_x = self.bats[i].copy()
            
            self.fitness_history.append(self.g_best_fitness)
            
            if iteration % 10 == 0:
                print(f"  Iteration {iteration:03d} | G-Best Fitness: {self.g_best_fitness:.6f}")
                
        print(f"VBO Final G-Best Fitness: {self.g_best_fitness:.6f}")
        return self.g_best_x

if __name__ == "__main__":
    # Test Objective: Sphere Function (Simple minimization)
    def sphere(x):
        return np.sum(x**2)
    
    vbo = VampireBatOptimizer(objective_function=sphere, n_dims=5, max_iter=50)
    best_weights = vbo.optimize()
    print(f"Optimized Parameters (Skeleton): {best_weights}")
