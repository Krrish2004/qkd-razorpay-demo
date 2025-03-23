import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle
import matplotlib.patheffects as PathEffects

# Set seaborn style
sns.set_style('whitegrid')
plt.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 13,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12
})

def generate_confusion_matrix():
    """Generate and save a confusion matrix visualization for the fraud detection model."""
    # Create data for confusion matrix
    # Values based on the text in the paper (11 true positives, 89 false negatives, 21 false positives)
    conf_matrix = np.array([
        [1879, 21],    # True Negatives, False Positives
        [89, 11]       # False Negatives, True Positives
    ])
    
    # Create a custom colormap (blue-white-red gradient)
    colors = [(0.0, 0.4, 0.8), (1, 1, 1), (0.8, 0.2, 0.2)]  # Blue to white to red
    cmap = LinearSegmentedColormap.from_list('custom_diverging', colors, N=256)
    
    # Create figure with larger size and higher DPI
    plt.figure(figsize=(10, 8), dpi=300)
    
    # Plot confusion matrix as heatmap
    ax = sns.heatmap(conf_matrix, annot=True, fmt='d', cmap=cmap, vmin=0, 
                    cbar_kws={'label': 'Count'}, linewidths=0.5, linecolor='black',
                    annot_kws={"size": 16, "weight": "bold"})
    
    # Add percentage values in smaller font
    total = np.sum(conf_matrix)
    for i in range(2):
        for j in range(2):
            # Calculate percentage
            pct = 100 * conf_matrix[i, j] / total
            # Add text with percentage
            text = ax.text(j + 0.5, i + 0.75, f'({pct:.1f}%)', 
                        ha="center", va="center", color="black", fontsize=11)
            # Add white outline to make text more readable
            text.set_path_effects([PathEffects.withStroke(linewidth=3, foreground='white')])
    
    # Configure axis labels and title
    class_labels = ['Legitimate', 'Fraudulent']
    ax.set_xlabel('Predicted Label', fontsize=13, fontweight='bold')
    ax.set_ylabel('True Label', fontsize=13, fontweight='bold')
    ax.set_title('Confusion Matrix for Fraud Detection', fontsize=15, fontweight='bold', pad=20)
    
    # Set ticks
    ax.set_xticklabels(class_labels)
    ax.set_yticklabels(class_labels)
    
    # Calculate metrics
    tp = conf_matrix[1, 1]
    tn = conf_matrix[0, 0]
    fp = conf_matrix[0, 1]
    fn = conf_matrix[1, 0]
    
    # Calculate performance metrics
    accuracy = 100 * (tp + tn) / (tp + tn + fp + fn)
    precision = 100 * tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = 100 * tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    # Add performance metrics as text
    plt.figtext(0.5, 0.01, f'Accuracy: {accuracy:.1f}% | Precision: {precision:.1f}% | Recall: {recall:.1f}% | F1 Score: {f1:.1f}%', 
                ha='center', fontsize=12, bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.5'))
    
    # Add quadrant labels with colored backgrounds
    # True Negative (top-left)
    plt.text(0.24, 0.24, 'True Negative', 
             ha='center', va='center', fontsize=11, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.6))
    
    # False Positive (top-right)
    plt.text(1.24, 0.24, 'False Positive', 
             ha='center', va='center', fontsize=11, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='salmon', alpha=0.6))
    
    # False Negative (bottom-left)
    plt.text(0.24, 1.24, 'False Negative', 
             ha='center', va='center', fontsize=11, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='salmon', alpha=0.6))
    
    # True Positive (bottom-right)
    plt.text(1.24, 1.24, 'True Positive', 
             ha='center', va='center', fontsize=11, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgreen', alpha=0.6))
    
    # Add a border around the figure
    ax.add_patch(Rectangle((-0.1, -0.1), 2.2, 2.2, fill=False, edgecolor='gray', 
                          lw=2, transform=ax.transData))
    
    # Adjust layout and save
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    plt.savefig('confusion_matrix.png', bbox_inches='tight', dpi=300)
    print("Confusion matrix generated and saved as 'confusion_matrix.png'")
    plt.close()

if __name__ == "__main__":
    generate_confusion_matrix() 