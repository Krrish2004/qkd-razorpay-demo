import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch
import matplotlib.patheffects as PathEffects

# Set up the figure with higher DPI for better quality
plt.figure(figsize=(10, 6), dpi=300)
plt.tight_layout()
ax = plt.gca()

# Set background color to white
ax.set_facecolor('white')
plt.gcf().set_facecolor('white')

# Remove axes
ax.set_axis_off()

# Colors
INPUT_COLOR = '#D6EAF8'
HIDDEN1_COLOR = '#AED6F1'
HIDDEN2_COLOR = '#85C1E9'
HIDDEN3_COLOR = '#3498DB'
OUTPUT_COLOR = '#D5F5E3'
ARROW_COLOR = '#333333'

# Layer positions
layer_x = [1, 3, 5, 7, 9]
layer_nodes = [7, 12, 8, 4, 1]
layer_names = ['Input Layer', 'Hidden Layer 1', 'Hidden Layer 2', 'Hidden Layer 3', 'Output Layer']
layer_colors = [INPUT_COLOR, HIDDEN1_COLOR, HIDDEN2_COLOR, HIDDEN3_COLOR, OUTPUT_COLOR]
layer_details = ['7 neurons', '12 neurons\nReLU + Dropout (0.3)', '8 neurons\nReLU + Dropout (0.2)', '4 neurons\nReLU', '1 neuron\nSigmoid']

# Draw nodes for each layer
nodes = []
max_nodes = max(layer_nodes)
node_size = 0.15

for i, (x, num_nodes, color) in enumerate(zip(layer_x, layer_nodes, layer_colors)):
    # Calculate spacing for different numbers of nodes
    total_height = 4
    spacing = total_height / (num_nodes + 1)
    
    layer_nodes_list = []
    # Create nodes
    for j in range(num_nodes):
        y_pos = total_height / 2 - spacing * (j + 1)
        
        if num_nodes > 5 and j > 1 and j < num_nodes - 2 and i != 4:  # Skip drawing some middle nodes for dense layers
            if j == 2:  # Only draw dots for the first hidden "skipped" node
                plt.text(x, y_pos, '⋮', fontsize=20, ha='center', va='center')
            continue
            
        circle = plt.Circle((x, y_pos), node_size, color=color, ec='black', zorder=10)
        ax.add_artist(circle)
        layer_nodes_list.append((x, y_pos))
    
    nodes.append(layer_nodes_list)
    
    # Add layer labels
    plt.text(x, -2.3, f"{layer_names[i]}\n{layer_details[i]}", ha='center', va='center', fontsize=10, 
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', boxstyle='round,pad=0.2'))

# Draw connections between nodes
for i in range(len(nodes) - 1):
    start_nodes = nodes[i]
    end_nodes = nodes[i + 1]
    
    # Draw a subset of connections to avoid clutter
    for j, start in enumerate(start_nodes):
        for k, end in enumerate(end_nodes):
            # Limit connections to avoid visual clutter
            if (i == 0 and j % 2 == 0) or (i > 0 and (j+k) % 2 == 0):
                arrow = FancyArrowPatch(start, end, connectionstyle="arc3,rad=0", 
                                      arrowstyle='->', color=ARROW_COLOR, linewidth=0.5,
                                      alpha=0.7, zorder=5)
                ax.add_artist(arrow)

# Add notes about input features
feature_text = (
    "Input Features:\n"
    "• Transaction Amount\n"
    "• Time Since Last Transaction\n"
    "• Transaction Velocity\n"
    "• Geographic Risk Score\n"
    "• Device Reputation\n"
    "• Payment Method Risk\n"
    "• Customer History Score"
)
plt.text(1, -4.5, feature_text, fontsize=9, ha='center', va='top',
         bbox=dict(facecolor='#F8F9F9', alpha=1, edgecolor='#D5DBDB', boxstyle='round,pad=0.5'))

# Add notes about model details
model_text = (
    "Model Details:\n"
    "• Optimizer: Adam (lr=0.001)\n"
    "• Loss: Binary Cross-Entropy\n"
    "• Metrics: AUC, Precision, Recall\n"
    "• Training: 50 epochs with early stopping\n"
    "• Output: Fraud probability (0-1)"
)
plt.text(9, -4.5, model_text, fontsize=9, ha='center', va='top',
         bbox=dict(facecolor='#F8F9F9', alpha=1, edgecolor='#D5DBDB', boxstyle='round,pad=0.5'))

# Add title
title_text = plt.text(5, 2.9, "Neural Network Architecture for Fraud Detection", 
                     fontsize=14, weight='bold', ha='center', va='bottom')
title_text.set_path_effects([PathEffects.withStroke(linewidth=3, foreground='white')])

# Set the limits to include all elements
plt.xlim(0, 10)
plt.ylim(-6, 3)

# Save the figure with tight layout to eliminate extra whitespace
plt.savefig('neural_network.png', bbox_inches='tight', pad_inches=0.1, dpi=300)
plt.close()

print("Neural network diagram created successfully!") 