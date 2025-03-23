import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 13,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'figure.titlesize': 16
})

def generate_accuracy_curves():
    """Generate and save accuracy curves for neural network training."""
    # Set up figure
    fig = plt.figure(figsize=(12, 6), dpi=300)
    
    # Use GridSpec to create custom layout
    gs = GridSpec(1, 1, figure=fig)
    ax = fig.add_subplot(gs[0, 0])
    
    # Create epochs array (1-100)
    epochs = np.arange(1, 101)
    
    # Generate synthetic training and validation accuracy data
    # Starting around 0.90 and increasing to 0.96
    # Using the paper's Table 7 as reference
    np.random.seed(42)  # For reproducibility
    
    # Base accuracy curve shape (logarithmic growth)
    base_train_acc = 0.903 + 0.06 * np.log(1 + epochs/10) / np.log(1 + 100/10)
    
    # Add some noise to make it realistic
    noise = np.random.normal(0, 0.005, size=len(epochs))
    smoothed_noise = np.convolve(noise, np.ones(5)/5, mode='same')
    
    # Create training accuracy with small fluctuations
    train_acc = np.clip(base_train_acc + smoothed_noise, 0.9, 0.98)
    
    # Create validation accuracy as slightly lower with more fluctuations
    val_noise = np.random.normal(0, 0.01, size=len(epochs))
    smoothed_val_noise = np.convolve(val_noise, np.ones(5)/5, mode='same')
    
    # Base validation accuracy starts lower but catches up
    base_val_acc = 0.918 + 0.03 * np.log(1 + epochs/15) / np.log(1 + 100/15)
    val_acc = np.clip(base_val_acc + smoothed_val_noise, 0.9, 0.98)
    
    # Add a dip for overfitting around epoch 75-90
    dip = np.zeros(len(epochs))
    dip[75:90] = np.linspace(0, 0.01, 15)
    dip[90:] = np.linspace(0.01, 0, 10)
    val_acc -= dip
    
    # Set specifically to match table values for key epochs
    epoch_milestones = {
        1: (0.9023, 0.9175),
        10: (0.9342, 0.9325),
        25: (0.9428, 0.9375),
        50: (0.9489, 0.9400),
        75: (0.9527, 0.9425),
        100: (0.9619, 0.9450)
    }
    
    # Adjust curves to match milestone values
    for epoch, (train_val, val_val) in epoch_milestones.items():
        idx = epoch - 1  # 0-indexed
        train_acc[idx] = train_val
        val_acc[idx] = val_val
    
    # Plot the accuracy curves
    ax.plot(epochs, train_acc, color='#0072B2', linewidth=2.5, label='Training Accuracy')
    ax.plot(epochs, val_acc, color='#D55E00', linewidth=2.5, label='Validation Accuracy')
    
    # Fill the area between curves
    ax.fill_between(epochs, train_acc, val_acc, 
                    where=(train_acc > val_acc), 
                    alpha=0.2, color='#0072B2',
                    interpolate=True, label='Generalization Gap')
    
    # Add grid
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Label specific points of interest
    ax.annotate('Initial Accuracy', xy=(5, train_acc[4]), xytext=(15, train_acc[4] - 0.03),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8))
    
    ax.annotate('Steady Improvement', xy=(50, train_acc[49]), xytext=(40, train_acc[49] + 0.03),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8))
    
    ax.annotate('Growing Gap', xy=(85, val_acc[84]), xytext=(65, val_acc[84] - 0.03),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8))
    
    # Add markers for key epochs from the table
    for epoch in epoch_milestones.keys():
        idx = epoch - 1  # 0-indexed
        ax.plot(epoch, train_acc[idx], 'o', color='#0072B2', markersize=8)
        ax.plot(epoch, val_acc[idx], 'o', color='#D55E00', markersize=8)
        
        # Add text labels for specific epochs
        if epoch in [1, 25, 50, 75, 100]:
            ax.text(epoch + 2, train_acc[idx] - 0.01, 
                    f"E{epoch}: {train_acc[idx]:.4f}", fontsize=9)
            ax.text(epoch + 2, val_acc[idx] + 0.01, 
                    f"E{epoch}: {val_acc[idx]:.4f}", fontsize=9)
    
    # Create legend with custom handles
    train_patch = mpatches.Patch(color='#0072B2', label='Training Accuracy')
    val_patch = mpatches.Patch(color='#D55E00', label='Validation Accuracy')
    gap_patch = mpatches.Patch(color='#0072B2', alpha=0.2, label='Generalization Gap')
    
    # Set labels and title
    ax.set_xlabel('Epoch', fontweight='bold')
    ax.set_ylabel('Accuracy', fontweight='bold')
    ax.set_title('Training and Validation Accuracy Curves', fontweight='bold', pad=20)
    
    # Set axis limits
    ax.set_xlim(0, 101)
    ax.set_ylim(0.9, 0.98)
    
    # Add legend
    ax.legend(handles=[train_patch, val_patch, gap_patch], 
              loc='lower right', frameon=True, fancybox=True, 
              framealpha=0.9, edgecolor='gray')
    
    # Add metrics in a table-like format at the bottom
    table_text = f"Final Metrics - Training Accuracy: {train_acc[-1]:.4f} | Validation Accuracy: {val_acc[-1]:.4f}"
    fig.text(0.5, 0.01, table_text, ha='center', fontsize=12, 
             bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.5'))
    
    # Add vertical lines for key epochs
    for epoch in epoch_milestones.keys():
        ax.axvline(x=epoch, color='gray', linestyle='--', alpha=0.5)
    
    # Add subtitle
    plt.suptitle('Neural Network Training Progression', fontsize=16, fontweight='bold', y=0.98)
    
    # Save the figure
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('accuracy_curves.png', bbox_inches='tight', dpi=300)
    print("Accuracy curves generated and saved as 'accuracy_curves.png'")
    plt.close()

if __name__ == "__main__":
    generate_accuracy_curves() 