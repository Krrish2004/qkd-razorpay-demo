#!/usr/bin/env python3
"""
Train Fraud Detection Model

This script loads the synthetic dataset and trains the fraud detection neural network model.
"""

import os
import sys
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import joblib
import logging

# Import the FraudDetectionAI and SimpleNN from the fraud_detection module
sys.path.append('.')  # Add current directory to path
try:
    from fraud_detection import FraudDetectionAI, SimpleNN
except ImportError:
    print("Error: Could not import from fraud_detection.py")
    print("Please ensure you're running this script from the project root directory.")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Train Fraud Model')

def load_dataset(data_path='data/fraud_detection_data.csv'):
    """
    Load the synthetic fraud detection dataset
    
    Args:
        data_path (str): Path to the CSV file
        
    Returns:
        pandas.DataFrame: The loaded dataset
    """
    try:
        logger.info(f"Loading dataset from {data_path}")
        df = pd.read_csv(data_path)
        logger.info(f"Dataset loaded successfully with {len(df)} rows and {len(df.columns)} columns")
        return df
    except Exception as e:
        logger.error(f"Error loading dataset: {str(e)}")
        raise

def prepare_data_for_training(df, test_size=0.2, random_state=42):
    """
    Prepare the dataset for model training
    
    Args:
        df (pandas.DataFrame): The dataset
        test_size (float): Proportion of data to use for testing
        random_state (int): Random seed for reproducibility
        
    Returns:
        tuple: (X_train, X_test, y_train, y_test, scaler)
    """
    logger.info("Preparing data for training...")
    
    # Select features used by the model
    features = [
        'step', 'amount', 'oldbalanceOrg', 'newbalanceOrig', 
        'oldbalanceDest', 'newbalanceDest', 'type_PAYMENT', 
        'type_TRANSFER', 'type_CASH_OUT', 'type_DEBIT', 
        'type_CASH_IN', 'amount_deducted', 'amount_credited'
    ]
    
    # Check if all required features are in the dataframe
    missing_features = [f for f in features if f not in df.columns]
    if missing_features:
        logger.error(f"Missing features in dataset: {missing_features}")
        raise ValueError(f"Dataset is missing required features: {missing_features}")
    
    # Split dataset into features and target
    X = df[features].values
    y = df['is_fraud'].values
    
    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    logger.info(f"Data prepared: {X_train.shape[0]} training samples, {X_test.shape[0]} test samples")
    logger.info(f"Fraud ratio in training set: {np.mean(y_train):.4f}")
    logger.info(f"Fraud ratio in test set: {np.mean(y_test):.4f}")
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler

def train_model(X_train, y_train, X_test, y_test, model_dir='models', epochs=100, batch_size=64, learning_rate=0.001):
    """
    Train the neural network model
    
    Args:
        X_train (numpy.ndarray): Training features
        y_train (numpy.ndarray): Training labels
        X_test (numpy.ndarray): Test features
        y_test (numpy.ndarray): Test labels
        model_dir (str): Directory to save the model
        epochs (int): Number of training epochs
        batch_size (int): Batch size for training
        learning_rate (float): Learning rate
        
    Returns:
        tuple: (model, train_losses, test_losses, train_accuracies, test_accuracies)
    """
    logger.info(f"Training neural network model with {epochs} epochs")
    
    # Create model directory if it doesn't exist
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    
    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info(f"Using device: {device}")
    
    # Initialize model
    input_size = X_train.shape[1]
    model = SimpleNN(input_size).to(device)
    
    # Convert data to PyTorch tensors
    X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
    X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)
    
    # Create datasets and dataloaders
    train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    
    test_dataset = TensorDataset(X_test_tensor, y_test_tensor)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    
    # Define loss function and optimizer
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    # Track metrics
    train_losses = []
    test_losses = []
    train_accuracies = []
    test_accuracies = []
    
    # Training loop
    for epoch in range(epochs):
        # Training phase
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            
            # Zero the parameter gradients
            optimizer.zero_grad()
            
            # Forward pass
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            
            # Backward pass and optimize
            loss.backward()
            optimizer.step()
            
            # Statistics
            running_loss += loss.item() * inputs.size(0)
            predicted = (torch.sigmoid(outputs) > 0.5).float()
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        
        epoch_loss = running_loss / len(train_loader.dataset)
        epoch_acc = correct / total
        train_losses.append(epoch_loss)
        train_accuracies.append(epoch_acc)
        
        # Evaluation phase
        model.eval()
        test_loss = 0.0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for inputs, labels in test_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                
                test_loss += loss.item() * inputs.size(0)
                predicted = (torch.sigmoid(outputs) > 0.5).float()
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        
        test_loss = test_loss / len(test_loader.dataset)
        test_acc = correct / total
        test_losses.append(test_loss)
        test_accuracies.append(test_acc)
        
        # Log progress
        if (epoch + 1) % 10 == 0 or epoch == 0:
            logger.info(f'Epoch {epoch+1}/{epochs} - '
                        f'Train Loss: {epoch_loss:.4f}, Train Acc: {epoch_acc:.4f}, '
                        f'Test Loss: {test_loss:.4f}, Test Acc: {test_acc:.4f}')
    
    # Save the model
    model_path = os.path.join(model_dir, 'simple_nn_model.pth')
    torch.save(model.state_dict(), model_path)
    logger.info(f"Model saved to {model_path}")
    
    return model, train_losses, test_losses, train_accuracies, test_accuracies

def evaluate_model(model, X_test, y_test, scaler, results_dir='results'):
    """
    Evaluate the trained model and generate performance metrics
    
    Args:
        model (SimpleNN): The trained model
        X_test (numpy.ndarray): Test features
        y_test (numpy.ndarray): Test labels
        scaler (StandardScaler): The feature scaler
        results_dir (str): Directory to save results
        
    Returns:
        dict: Performance metrics
    """
    logger.info("Evaluating model performance...")
    
    # Create results directory if it doesn't exist
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Convert test data to PyTorch tensors
    X_test_tensor = torch.tensor(X_test, dtype=torch.float32).to(device)
    
    # Set model to evaluation mode
    model.eval()
    
    # Get predictions
    with torch.no_grad():
        outputs = model(X_test_tensor)
        probabilities = torch.sigmoid(outputs).cpu().numpy().flatten()
        predictions = (probabilities > 0.5).astype(int)
    
    # Calculate metrics
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_curve, auc
    
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)
    conf_matrix = confusion_matrix(y_test, predictions)
    
    # Calculate ROC curve and AUC
    fpr, tpr, _ = roc_curve(y_test, probabilities)
    roc_auc = auc(fpr, tpr)
    
    # Log metrics
    logger.info(f"Accuracy: {accuracy:.4f}")
    logger.info(f"Precision: {precision:.4f}")
    logger.info(f"Recall: {recall:.4f}")
    logger.info(f"F1 Score: {f1:.4f}")
    logger.info(f"AUC: {roc_auc:.4f}")
    logger.info(f"Confusion Matrix:\n{conf_matrix}")
    
    # Create visualizations
    
    # 1. Confusion Matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Not Fraud', 'Fraud'],
                yticklabels=['Not Fraud', 'Fraud'])
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'confusion_matrix.png'))
    plt.close()
    
    # 2. ROC Curve
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.3f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.savefig(os.path.join(results_dir, 'roc_curve.png'))
    plt.close()
    
    # 3. Precision-Recall curve
    from sklearn.metrics import precision_recall_curve, average_precision_score
    
    precision_curve, recall_curve, _ = precision_recall_curve(y_test, probabilities)
    avg_precision = average_precision_score(y_test, probabilities)
    
    plt.figure(figsize=(8, 6))
    plt.plot(recall_curve, precision_curve, color='blue', lw=2, 
             label=f'Precision-Recall curve (AP = {avg_precision:.3f})')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.legend(loc="lower left")
    plt.grid(True)
    plt.savefig(os.path.join(results_dir, 'precision_recall_curve.png'))
    plt.close()
    
    # Return metrics
    metrics = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'auc': roc_auc,
        'confusion_matrix': conf_matrix.tolist(),
        'avg_precision': avg_precision
    }
    
    # Save metrics to a file
    import json
    with open(os.path.join(results_dir, 'model_metrics.json'), 'w') as f:
        json.dump(metrics, f, indent=4)
    
    logger.info(f"Evaluation results saved to {results_dir}")
    
    return metrics

def plot_training_history(train_losses, test_losses, train_accuracies, test_accuracies, results_dir='results'):
    """
    Plot training and validation loss/accuracy curves
    
    Args:
        train_losses (list): Training losses
        test_losses (list): Validation losses
        train_accuracies (list): Training accuracies
        test_accuracies (list): Validation accuracies
        results_dir (str): Directory to save plots
    """
    # Create directory if it doesn't exist
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    # Plot losses
    plt.figure(figsize=(10, 5))
    epochs = range(1, len(train_losses) + 1)
    plt.plot(epochs, train_losses, 'b-', label='Training Loss')
    plt.plot(epochs, test_losses, 'r-', label='Validation Loss')
    plt.title('Training and Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(results_dir, 'loss_curves.png'))
    plt.close()
    
    # Plot accuracies
    plt.figure(figsize=(10, 5))
    plt.plot(epochs, train_accuracies, 'g-', label='Training Accuracy')
    plt.plot(epochs, test_accuracies, 'm-', label='Validation Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(results_dir, 'accuracy_curves.png'))
    plt.close()
    
    logger.info(f"Training history plots saved to {results_dir}")

def main():
    """Main function to train and evaluate the fraud detection model"""
    logger.info("Starting fraud detection model training process")
    
    # Load dataset
    try:
        df = load_dataset()
    except Exception as e:
        logger.error(f"Failed to load dataset: {str(e)}")
        return
    
    # Prepare data
    try:
        X_train, X_test, y_train, y_test, scaler = prepare_data_for_training(df)
    except Exception as e:
        logger.error(f"Failed to prepare data: {str(e)}")
        return
    
    # Save the scaler
    model_dir = 'models'
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    scaler_path = os.path.join(model_dir, 'feature_scaler.joblib')
    joblib.dump(scaler, scaler_path)
    logger.info(f"Feature scaler saved to {scaler_path}")
    
    # Train model
    try:
        model, train_losses, test_losses, train_accs, test_accs = train_model(
            X_train, y_train, X_test, y_test, epochs=100
        )
    except Exception as e:
        logger.error(f"Failed to train model: {str(e)}")
        return
    
    # Plot training history
    plot_training_history(train_losses, test_losses, train_accs, test_accs)
    
    # Evaluate model
    try:
        metrics = evaluate_model(model, X_test, y_test, scaler)
    except Exception as e:
        logger.error(f"Failed to evaluate model: {str(e)}")
        return
    
    logger.info("Model training and evaluation completed successfully")
    
    # Print summary of results
    print("\n" + "="*50)
    print("FRAUD DETECTION MODEL TRAINING SUMMARY")
    print("="*50)
    print(f"Dataset size: {len(df)} records")
    print(f"Fraud prevalence: {df['is_fraud'].mean()*100:.2f}%")
    print(f"Training records: {X_train.shape[0]}")
    print(f"Testing records: {X_test.shape[0]}")
    print("\nModel Performance:")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall: {metrics['recall']:.4f}")
    print(f"F1 Score: {metrics['f1_score']:.4f}")
    print(f"AUC: {metrics['auc']:.4f}")
    print("\nModel and results saved to the 'models' and 'results' directories")
    print("="*50)

if __name__ == "__main__":
    main() 