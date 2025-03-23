import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrow, Rectangle, Circle
from matplotlib.lines import Line2D

# Set the style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.size': 12,
    'font.family': 'sans-serif',
    'font.weight': 'bold',
    'axes.labelweight': 'bold',
    'axes.titleweight': 'bold',
    'figure.titleweight': 'bold',
    'figure.figsize': (12, 7),
})

# Color scheme
COLORS = {
    'background': '#f8f9fa',
    'input_layer': '#4e79a7',
    'hidden_layer1': '#59a14f',
    'hidden_layer2': '#9c755f',
    'hidden_layer3': '#f28e2b',
    'output_layer': '#e15759',
    'text': '#1e1e1e',
    'connections': '#cccccc',
    'arrow': '#888888',
    'neuron': '#ffffff',
    'neuron_edge': '#333333',
}

def create_neural_network_diagram():
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 7), facecolor=COLORS['background'])
    ax.set_facecolor(COLORS['background'])
    
    # Remove spines and ticks
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Layer configuration
    input_neurons = 7
    hidden_neurons = [12, 8, 4]
    output_neurons = 1
    
    # Define positions
    layers_x = [1, 3, 5, 7, 9]
    max_neurons = max(input_neurons, max(hidden_neurons), output_neurons)
    
    # Vertical spacing based on max neurons
    vertical_spacing = 5 / max_neurons
    
    # Function to calculate y-positions for a layer
    def calculate_y_positions(num_neurons):
        total_height = (num_neurons - 1) * vertical_spacing
        start_y = (5 - total_height) / 2
        return [start_y + i * vertical_spacing for i in range(num_neurons)]
    
    # Draw neurons for each layer
    input_y = calculate_y_positions(input_neurons)
    hidden1_y = calculate_y_positions(hidden_neurons[0])
    hidden2_y = calculate_y_positions(hidden_neurons[1])
    hidden3_y = calculate_y_positions(hidden_neurons[2])
    output_y = calculate_y_positions(output_neurons)
    
    # Connect all neurons between adjacent layers
    # Input to Hidden1
    for i in range(input_neurons):
        for j in range(hidden_neurons[0]):
            ax.plot([layers_x[0], layers_x[1]], [input_y[i], hidden1_y[j]], 
                   color=COLORS['connections'], linewidth=0.3, alpha=0.7, zorder=1)
    
    # Hidden1 to Hidden2
    for i in range(hidden_neurons[0]):
        for j in range(hidden_neurons[1]):
            ax.plot([layers_x[1], layers_x[2]], [hidden1_y[i], hidden2_y[j]], 
                   color=COLORS['connections'], linewidth=0.3, alpha=0.7, zorder=1)
    
    # Hidden2 to Hidden3
    for i in range(hidden_neurons[1]):
        for j in range(hidden_neurons[2]):
            ax.plot([layers_x[2], layers_x[3]], [hidden2_y[i], hidden3_y[j]], 
                   color=COLORS['connections'], linewidth=0.3, alpha=0.7, zorder=1)
    
    # Hidden3 to Output
    for i in range(hidden_neurons[2]):
        for j in range(output_neurons):
            ax.plot([layers_x[3], layers_x[4]], [hidden3_y[i], output_y[j]], 
                   color=COLORS['connections'], linewidth=0.3, alpha=0.7, zorder=1)
    
    # Draw neuron circles
    neuron_radius = 0.15
    
    # Input layer
    input_circles = []
    for y in input_y:
        circle = plt.Circle((layers_x[0], y), neuron_radius, color=COLORS['neuron'], 
                          ec=COLORS['input_layer'], lw=2, zorder=2)
        ax.add_patch(circle)
        input_circles.append(circle)
    
    # Hidden layer 1
    hidden1_circles = []
    for y in hidden1_y:
        circle = plt.Circle((layers_x[1], y), neuron_radius, color=COLORS['neuron'], 
                          ec=COLORS['hidden_layer1'], lw=2, zorder=2)
        ax.add_patch(circle)
        hidden1_circles.append(circle)
    
    # Hidden layer 2
    hidden2_circles = []
    for y in hidden2_y:
        circle = plt.Circle((layers_x[2], y), neuron_radius, color=COLORS['neuron'], 
                          ec=COLORS['hidden_layer2'], lw=2, zorder=2)
        ax.add_patch(circle)
        hidden2_circles.append(circle)
    
    # Hidden layer 3
    hidden3_circles = []
    for y in hidden3_y:
        circle = plt.Circle((layers_x[3], y), neuron_radius, color=COLORS['neuron'], 
                          ec=COLORS['hidden_layer3'], lw=2, zorder=2)
        ax.add_patch(circle)
        hidden3_circles.append(circle)
    
    # Output layer
    output_circles = []
    for y in output_y:
        circle = plt.Circle((layers_x[4], y), neuron_radius, color=COLORS['neuron'], 
                          ec=COLORS['output_layer'], lw=2, zorder=2)
        ax.add_patch(circle)
        output_circles.append(circle)
    
    # Add layer labels
    ax.text(layers_x[0], 5.3, "Input Layer", ha='center', va='center', 
           fontsize=14, color=COLORS['input_layer'], fontweight='bold')
    ax.text(layers_x[0], 0.3, f"{input_neurons} neurons", ha='center', va='center', 
           fontsize=10, color=COLORS['input_layer'])
    
    ax.text(layers_x[1], 5.3, "Hidden Layer 1", ha='center', va='center', 
           fontsize=14, color=COLORS['hidden_layer1'], fontweight='bold')
    ax.text(layers_x[1], 0.3, f"{hidden_neurons[0]} neurons\nReLU + Dropout(0.2)", ha='center', va='center', 
           fontsize=10, color=COLORS['hidden_layer1'])
    
    ax.text(layers_x[2], 5.3, "Hidden Layer 2", ha='center', va='center', 
           fontsize=14, color=COLORS['hidden_layer2'], fontweight='bold')
    ax.text(layers_x[2], 0.3, f"{hidden_neurons[1]} neurons\nReLU + Dropout(0.2)", ha='center', va='center', 
           fontsize=10, color=COLORS['hidden_layer2'])
    
    ax.text(layers_x[3], 5.3, "Hidden Layer 3", ha='center', va='center', 
           fontsize=14, color=COLORS['hidden_layer3'], fontweight='bold')
    ax.text(layers_x[3], 0.3, f"{hidden_neurons[2]} neurons\ntanh + Dropout(0.2)", ha='center', va='center', 
           fontsize=10, color=COLORS['hidden_layer3'])
    
    ax.text(layers_x[4], 5.3, "Output Layer", ha='center', va='center', 
           fontsize=14, color=COLORS['output_layer'], fontweight='bold')
    ax.text(layers_x[4], 0.3, f"{output_neurons} neuron\nSigmoid", ha='center', va='center', 
           fontsize=10, color=COLORS['output_layer'])
    
    # Add feature labels for input layer
    input_features = [
        "Transaction Amount",
        "Time Since Last Txn",
        "User Account Age",
        "Location Mismatch",
        "Device Fingerprint",
        "Transaction Frequency",
        "Quantum Encryption Flag"
    ]
    
    for i, feature in enumerate(input_features):
        ax.text(layers_x[0] - 0.5, input_y[i], feature, ha='right', va='center', 
               fontsize=10, color=COLORS['text'])
    
    # Add prediction label for output
    ax.text(layers_x[4] + 0.5, output_y[0], "Fraud Score\n(0.0 - 1.0)", ha='left', va='center', 
           fontsize=10, color=COLORS['text'])
    
    # Add title
    ax.set_title("Neural Network Architecture for Fraud Detection", fontsize=18, pad=20)
    
    # Add model details box
    model_details = (
        "Model Details:\n"
        "- Optimizer: Adam (lr=0.001)\n"
        "- Loss: Binary Cross-Entropy\n"
        "- Metrics: Accuracy, AUC\n"
        "- Batch Size: 64\n"
        "- Epochs: 100"
    )
    
    props = dict(boxstyle='round', facecolor='white', alpha=0.9, ec='#cccccc')
    ax.text(5, -0.3, model_details, ha='center', va='center', fontsize=10, 
           bbox=props, color=COLORS['text'])
    
    # Set limits
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.8, 5.8)
    
    # Save figure with tight layout
    plt.tight_layout()
    plt.savefig('neural_network.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    create_neural_network_diagram()
    print("Neural network diagram generated as 'neural_network.png'") 