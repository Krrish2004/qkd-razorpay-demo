#!/usr/bin/env python3
"""
Generate Synthetic Dataset for Fraud Detection Model

This script creates a realistic synthetic dataset for training and testing the 
fraud detection model. The dataset follows the feature structure required by
the model and incorporates realistic fraud patterns.
"""

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

def generate_synthetic_dataset(n_samples=10000, fraud_ratio=0.05, save_path='data'):
    """
    Generate synthetic transaction data similar to the PaySim dataset
    
    Args:
        n_samples (int): Number of samples to generate
        fraud_ratio (float): Approximate ratio of fraudulent transactions
        save_path (str): Directory to save the dataset
    
    Returns:
        pandas.DataFrame: The generated dataset
    """
    print(f"Generating synthetic dataset with {n_samples} samples...")
    np.random.seed(42)  # For reproducibility
    
    # Create a directory for the data if it doesn't exist
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    # 1. Generate basic transaction features
    
    # Transaction step (1-744 hours, representing hours in a month)
    step = np.random.randint(1, 744, size=n_samples)
    
    # Transaction timestamp (for the current month)
    now = datetime.now()
    start_of_month = datetime(now.year, now.month, 1)
    timestamps = []
    for s in step:
        # Calculate date and time from step
        # Convert numpy.int64 to Python int
        s_int = int(s)
        ts = start_of_month + timedelta(hours=s_int)
        timestamps.append(ts.isoformat())
    
    # Transaction amounts - using exponential distribution for realistic skew
    amount = np.round(np.random.exponential(scale=200000, size=n_samples))
    
    # Customer IDs
    num_customers = int(n_samples * 0.2)  # 20% of transactions count as number of unique customers
    customer_ids = np.random.randint(10000, 99999, size=num_customers)
    transaction_customer_ids = np.random.choice(customer_ids, size=n_samples)
    
    # Merchant IDs
    num_merchants = int(n_samples * 0.1)  # 10% of transactions count as number of unique merchants
    merchant_ids = np.random.randint(1000, 9999, size=num_merchants)
    transaction_merchant_ids = np.random.choice(merchant_ids, size=n_samples)
    
    # Balance information
    oldbalanceOrg = np.random.exponential(scale=1000000, size=n_samples)
    newbalanceOrig = np.maximum(0, oldbalanceOrg - np.random.uniform(0, 1, size=n_samples) * amount)
    oldbalanceDest = np.random.exponential(scale=1000000, size=n_samples)
    newbalanceDest = oldbalanceDest + np.random.uniform(0, 1, size=n_samples) * amount
    
    # Transaction types
    transaction_types = ['PAYMENT', 'TRANSFER', 'CASH_OUT', 'DEBIT', 'CASH_IN']
    type_probabilities = [0.4, 0.3, 0.15, 0.1, 0.05]  # More realistic distribution
    type_idx = np.random.choice(len(transaction_types), size=n_samples, p=type_probabilities)
    transaction_type = [transaction_types[i] for i in type_idx]
    
    # One-hot encoded transaction types (for the model)
    type_one_hot = np.zeros((n_samples, len(transaction_types)))
    for i in range(n_samples):
        type_one_hot[i, type_idx[i]] = 1
    
    # Additional derived features
    amount_deducted = oldbalanceOrg - newbalanceOrig
    amount_credited = newbalanceDest - oldbalanceDest
    
    # Payment methods mapped from transaction types
    payment_methods = []
    for t_type in transaction_type:
        if t_type == 'PAYMENT':
            payment_methods.append(np.random.choice(['CARD', 'UPI', 'NETBANKING'], p=[0.6, 0.3, 0.1]))
        elif t_type == 'TRANSFER':
            payment_methods.append(np.random.choice(['UPI', 'NETBANKING'], p=[0.7, 0.3]))
        elif t_type == 'CASH_OUT':
            payment_methods.append('WALLET')
        elif t_type == 'DEBIT':
            payment_methods.append('CARD')
        else:  # CASH_IN
            payment_methods.append(np.random.choice(['CARD', 'UPI'], p=[0.4, 0.6]))
    
    # 2. Create target variable (fraud)
    is_fraud = np.zeros(n_samples, dtype=int)
    
    # Apply fraud patterns based on the code in fraud_detection.py
    
    # Pattern 1: Large CASH_OUT with balance being cleared
    for i in range(n_samples):
        if (transaction_type[i] == 'CASH_OUT' and
            amount[i] > 500000 and  # Large amount
            newbalanceOrig[i] < 0.1 * oldbalanceOrg[i]):  # Balance mostly cleared
            is_fraud[i] = 1
    
    # Pattern 2: Large transfers to accounts with no history
    for i in range(n_samples):
        if (transaction_type[i] == 'TRANSFER' and
            amount[i] > 400000 and  # Large amount
            oldbalanceDest[i] < 1000):  # Destination had minimal balance
            is_fraud[i] = 1
    
    # Pattern 3: Suspicious midnight transactions
    for i in range(n_samples):
        hour = datetime.fromisoformat(timestamps[i]).hour
        if (hour >= 1 and hour <= 4 and  # Between 1am and 4am
            amount[i] > 300000):  # Significant amount
            is_fraud[i] = 1
    
    # Add some random fraud cases to reach target fraud ratio
    current_fraud_ratio = is_fraud.sum() / n_samples
    if current_fraud_ratio < fraud_ratio:
        # Calculate how many more fraud cases we need
        additional_fraud_count = int(n_samples * fraud_ratio) - is_fraud.sum()
        # Find non-fraud indices
        non_fraud_indices = np.where(is_fraud == 0)[0]
        # Randomly select some to convert to fraud
        random_fraud = np.random.choice(non_fraud_indices, 
                                        size=min(additional_fraud_count, len(non_fraud_indices)), 
                                        replace=False)
        is_fraud[random_fraud] = 1
    
    # 3. Create DataFrame
    df = pd.DataFrame({
        'step': step,
        'timestamp': timestamps,
        'amount': amount,
        'customer_id': transaction_customer_ids,
        'merchant_id': transaction_merchant_ids,
        'transaction_type': transaction_type,
        'payment_method': payment_methods,
        'oldbalanceOrg': oldbalanceOrg,
        'newbalanceOrig': newbalanceOrig,
        'oldbalanceDest': oldbalanceDest,
        'newbalanceDest': newbalanceDest,
        'amount_deducted': amount_deducted,
        'amount_credited': amount_credited,
        'is_fraud': is_fraud
    })
    
    # Add one-hot encoded columns for the model
    for i, t_type in enumerate(transaction_types):
        df[f'type_{t_type}'] = type_one_hot[:, i]
    
    # 4. Save the dataset
    csv_path = os.path.join(save_path, 'fraud_detection_data.csv')
    df.to_csv(csv_path, index=False)
    print(f"Dataset saved to {csv_path}")
    
    # 5. Generate and save summary statistics
    stats_path = os.path.join(save_path, 'dataset_stats.txt')
    with open(stats_path, 'w') as f:
        f.write(f"Dataset Statistics - Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total samples: {n_samples}\n")
        f.write(f"Fraud samples: {is_fraud.sum()} ({is_fraud.sum()/n_samples*100:.2f}%)\n")
        f.write(f"Non-fraud samples: {n_samples - is_fraud.sum()} ({(n_samples - is_fraud.sum())/n_samples*100:.2f}%)\n\n")
        
        f.write("Transaction type distribution:\n")
        type_counts = df['transaction_type'].value_counts()
        for t_type, count in type_counts.items():
            f.write(f"  {t_type}: {count} ({count/n_samples*100:.2f}%)\n")
        
        f.write("\nPayment method distribution:\n")
        method_counts = df['payment_method'].value_counts()
        for method, count in method_counts.items():
            f.write(f"  {method}: {count} ({count/n_samples*100:.2f}%)\n")
        
        f.write("\nAmount statistics:\n")
        f.write(f"  Min: {df['amount'].min()}\n")
        f.write(f"  Max: {df['amount'].max()}\n")
        f.write(f"  Mean: {df['amount'].mean():.2f}\n")
        f.write(f"  Median: {df['amount'].median()}\n")
        
        # Fraud by transaction type
        f.write("\nFraud distribution by transaction type:\n")
        fraud_by_type = df.groupby('transaction_type')['is_fraud'].mean() * 100
        for t_type, fraud_pct in fraud_by_type.items():
            f.write(f"  {t_type}: {fraud_pct:.2f}%\n")
    
    print(f"Dataset statistics saved to {stats_path}")
    
    # 6. Generate visualizations
    visualize_dataset(df, save_path)
    
    return df

def visualize_dataset(df, save_path):
    """Generate visualizations of the dataset"""
    print("Generating dataset visualizations...")
    
    # Create visualizations directory
    viz_path = os.path.join(save_path, 'visualizations')
    if not os.path.exists(viz_path):
        os.makedirs(viz_path)
    
    # Set the style
    sns.set(style="whitegrid")
    
    # 1. Transaction amount distribution
    plt.figure(figsize=(12, 6))
    sns.histplot(data=df, x='amount', hue='is_fraud', bins=50, log_scale=(False, True))
    plt.title('Transaction Amount Distribution by Fraud Status')
    plt.xlabel('Amount')
    plt.ylabel('Count (log scale)')
    plt.savefig(os.path.join(viz_path, 'amount_distribution.png'))
    plt.close()
    
    # 2. Transaction types distribution
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='transaction_type', hue='is_fraud')
    plt.title('Transaction Types by Fraud Status')
    plt.xlabel('Transaction Type')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.savefig(os.path.join(viz_path, 'transaction_types.png'))
    plt.close()
    
    # 3. Fraud by hour of day
    df['hour'] = df['timestamp'].apply(lambda x: datetime.fromisoformat(x).hour)
    plt.figure(figsize=(12, 6))
    fraud_by_hour = df.groupby('hour')['is_fraud'].mean() * 100
    sns.lineplot(x=fraud_by_hour.index, y=fraud_by_hour.values)
    plt.title('Fraud Percentage by Hour of Day')
    plt.xlabel('Hour of Day')
    plt.ylabel('Fraud %')
    plt.xticks(range(0, 24))
    plt.savefig(os.path.join(viz_path, 'fraud_by_hour.png'))
    plt.close()
    
    # 4. Balance changes for fraud vs non-fraud
    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=df, x='oldbalanceOrg', y='newbalanceOrig', hue='is_fraud', alpha=0.5)
    plt.title('Origin Account Balance Changes')
    plt.xlabel('Original Balance')
    plt.ylabel('New Balance')
    plt.savefig(os.path.join(viz_path, 'balance_changes.png'))
    plt.close()
    
    # 5. Correlation matrix of numeric features
    plt.figure(figsize=(12, 10))
    numeric_df = df.select_dtypes(include=['number'])
    corr_matrix = numeric_df.corr()
    sns.heatmap(corr_matrix, annot=False, cmap='coolwarm')
    plt.title('Feature Correlation Matrix')
    plt.tight_layout()
    plt.savefig(os.path.join(viz_path, 'correlation_matrix.png'))
    plt.close()
    
    print(f"Visualizations saved to {viz_path}")

if __name__ == "__main__":
    # Generate a dataset with 10,000 samples and approximately 5% fraud
    df = generate_synthetic_dataset(n_samples=10000, fraud_ratio=0.05)
    
    # Print dataset head and summary
    print("\nDataset Sample:")
    print(df.head())
    
    print("\nDataset Summary:")
    print(f"Shape: {df.shape}")
    print(f"Fraud cases: {df['is_fraud'].sum()} ({df['is_fraud'].mean()*100:.2f}%)")
    print(f"Transaction types: {df['transaction_type'].value_counts().to_dict()}") 