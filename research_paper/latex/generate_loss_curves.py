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

def generate_loss_curves():
    """Generate and save loss curves for neural network training."""
    # Set up figure
    fig = plt.figure(figsize=(12, 6), dpi=300)
    
    # Use GridSpec to create custom layout
    gs = GridSpec(1, 1, figure=fig)
    ax = fig.add_subplot(gs[0, 0])
    
    # Create epochs array (1-100)
    epochs = np.arange(1, 101)
    
    # Generate synthetic training and validation loss data
    # Initial high loss that decreases rapidly, then more slowly
    # Using values based on the paper - starting around 0.3 and decreasing to around 0.12
    np.random.seed(42)  # For reproducibility
    
    # Base loss curve shape (exponential decay)
    base_train_loss = 0.35 * np.exp(-0.02 * epochs) + 0.1
    
    # Add some noise to make it realistic
    noise = np.random.normal(0, 0.01, size=len(epochs))
    smoothed_noise = np.convolve(noise, np.ones(5)/5, mode='same')
    
    # Create training loss with small fluctuations
    train_loss = base_train_loss + smoothed_noise
    
    # Create validation loss as slightly higher with more fluctuations
    val_noise = np.random.normal(0, 0.025, size=len(epochs))
    smoothed_val_noise = np.convolve(val_noise, np.ones(5)/5, mode='same')
    val_loss = base_train_loss + 0.02 + smoothed_val_noise
    
    # Add a bump for overfitting around epoch 75-90
    bump = np.zeros(len(epochs))
    bump[75:90] = np.linspace(0, 0.04, 15)
    bump[90:] = np.linspace(0.04, 0, 10)
    val_loss += bump
    
    # Plot the loss curves
    ax.plot(epochs, train_loss, color='#0072B2', linewidth=2.5, label='Training Loss')
    ax.plot(epochs, val_loss, color='#D55E00', linewidth=2.5, label='Validation Loss')
    
    # Fill the area between curves
    ax.fill_between(epochs, train_loss, val_loss, 
                    where=(val_loss > train_loss), 
                    alpha=0.2, color='#D55E00',
                    interpolate=True, label='Generalization Gap')
    
    # Add grid
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Label specific points of interest
    ax.annotate('Initial High Loss', xy=(5, train_loss[4]), xytext=(10, train_loss[4] + 0.05),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8))
    
    ax.annotate('Rapid Improvement', xy=(15, train_loss[14]), xytext=(20, train_loss[14] - 0.08),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8))
    
    ax.annotate('Potential Overfitting', xy=(85, val_loss[84]), xytext=(60, val_loss[84] + 0.08),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8))
    
    # Add markers for 5 important epochs
    key_epochs = [1, 25, 50, 75, 100]
    for epoch in key_epochs:
        idx = epoch - 1  # 0-indexed
        ax.plot(epoch, train_loss[idx], 'o', color='#0072B2', markersize=8)
        ax.plot(epoch, val_loss[idx], 'o', color='#D55E00', markersize=8)
    
    # Create legend with custom handles
    train_patch = mpatches.Patch(color='#0072B2', label='Training Loss')
    val_patch = mpatches.Patch(color='#D55E00', label='Validation Loss')
    gap_patch = mpatches.Patch(color='#D55E00', alpha=0.2, label='Generalization Gap')
    
    # Set labels and title
    ax.set_xlabel('Epoch', fontweight='bold')
    ax.set_ylabel('Binary Cross-Entropy Loss', fontweight='bold')
    ax.set_title('Training and Validation Loss Curves', fontweight='bold', pad=20)
    
    # Set axis limits
    ax.set_xlim(0, 101)
    ax.set_ylim(0, 0.4)
    
    # Add legend
    ax.legend(handles=[train_patch, val_patch, gap_patch], 
              loc='upper right', frameon=True, fancybox=True, 
              framealpha=0.9, edgecolor='gray')
    
    # Add metrics in a table-like format at the bottom
    table_text = f"Final Metrics - Training Loss: {train_loss[-1]:.4f} | Validation Loss: {val_loss[-1]:.4f}"
    fig.text(0.5, 0.01, table_text, ha='center', fontsize=12, 
             bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.5'))
    
    # Add vertical lines for key epochs
    for epoch in key_epochs:
        ax.axvline(x=epoch, color='gray', linestyle='--', alpha=0.5)
    
    # Save the figure
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.savefig('loss_curves.png', bbox_inches='tight', dpi=300)
    print("Loss curves generated and saved as 'loss_curves.png'")
    plt.close()

if __name__ == "__main__":
    generate_loss_curves() 