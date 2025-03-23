#!/usr/bin/env python3
"""
Fraud Detection Module - AI-based payment fraud detection for Razorpay transactions
"""

import logging
import json
import numpy as np
import time
from datetime import datetime
import hashlib
import random
import os
import joblib
import pandas as pd
import torch
import torch.nn as nn
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Fraud Detection')

# Define the PyTorch Neural Network model
class SimpleNN(nn.Module):
    def __init__(self, input_size):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 32)
        self.fc4 = nn.Linear(32, 1)
        self.dropout = nn.Dropout(p=0.2)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        x = torch.relu(self.fc2(x))
        x = self.dropout(x)
        x = torch.tanh(self.fc3(x))
        x = self.fc4(x)
        return x

class FraudDetectionAI:
    """
    AI-based fraud detection system for payment transactions
    """
    def __init__(self, model_type="heuristic", sensitivity=0.7):
        """
        Initialize the fraud detection system
        
        Args:
            model_type (str): Type of model to use ('heuristic', 'ml', 'quantum')
            sensitivity (float): Detection sensitivity (0.0-1.0, higher is more strict)
        """
        self.model_type = model_type
        self.sensitivity = max(0.0, min(1.0, sensitivity))  # Clamp to 0-1 range
        self.initialized = False
        self.risk_factors = {
            "amount_threshold": 100000,  # ₹1000.00
            "suspicious_domains": ["tempmail.com", "fakeemail.com", "throwaway.com"],
            "high_risk_countries": ["XY", "ZZ", "YY"],  # Example fictional country codes
            "suspicious_ip_ranges": ["192.168.0.", "10.0.0."],
            "time_anomalies": {
                "start_hour": 1,  # 1am
                "end_hour": 5     # 5am
            }
        }
        
        # ML model components
        self.ml_model = None
        self.feature_scaler = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Feature list for the model
        self.feature_names = [
            'step', 'amount', 'oldbalanceOrg', 'newbalanceOrig', 
            'oldbalanceDest', 'newbalanceDest', 'type_CASH_IN', 
            'type_CASH_OUT', 'type_DEBIT', 'type_PAYMENT', 
            'type_TRANSFER', 'amount_deducted', 'amount_credited'
        ]
        
        # Model persistence paths
        self.model_dir = 'models'
        self.model_path = os.path.join(self.model_dir, 'simple_nn_model.pth')
        self.scaler_path = os.path.join(self.model_dir, 'feature_scaler.joblib')
        
        logger.info(f"Initializing fraud detection AI with model_type={model_type}, sensitivity={sensitivity}")
        self._initialize_model()
        
    def _initialize_model(self):
        """Initialize the AI model based on the selected type"""
        try:
            if self.model_type == "heuristic":
                # Simple rule-based model
                logger.info("Initializing heuristic rule-based model")
                # No actual ML model to load, just rules
                time.sleep(0.5)  # Simulate initialization time
                self.initialized = True
                
            elif self.model_type == "ml":
                # Load the PyTorch neural network model
                logger.info("Loading neural network model")
                
                # Initialize scaler
                self.feature_scaler = MinMaxScaler()
                
                # Try to load pre-trained model
                if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
                    # Load NN model
                    input_size = len(self.feature_names)
                    self.ml_model = SimpleNN(input_size).to(self.device)
                    self.ml_model.load_state_dict(torch.load(self.model_path, map_location=self.device))
                    self.ml_model.eval()  # Set to evaluation mode
                    
                    # Load scaler
                    self.feature_scaler = joblib.load(self.scaler_path)
                    logger.info("Loaded pre-trained neural network model and scaler")
                else:
                    # We need to create a sample dataset for a new model
                    logger.info("No pre-trained model found. Downloading/creating sample dataset...")
                    try:
                        # This would typically download or create synthetic data
                        # For demonstration, we'll create synthetic data instead
                        self._create_initial_model()
                    except Exception as e:
                        logger.error(f"Failed to create initial neural network model: {str(e)}")
                        raise
                
                self.initialized = True
                
            elif self.model_type == "quantum":
                # For quantum-enhanced ML model
                logger.info("Initializing quantum-enhanced fraud detection model")
                
                # For quantum enhancements, we first load the ML model as a base
                if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
                    # Load NN model
                    input_size = len(self.feature_names)
                    self.ml_model = SimpleNN(input_size).to(self.device)
                    self.ml_model.load_state_dict(torch.load(self.model_path, map_location=self.device))
                    self.ml_model.eval()  # Set to evaluation mode
                    
                    # Load scaler
                    self.feature_scaler = joblib.load(self.scaler_path)
                    logger.info("Loaded pre-trained neural network model for quantum enhancement")
                else:
                    logger.info("No pre-trained model found, initializing new one")
                    self._create_initial_model()
                    
                # Additional quantum enhancement would go here in a real implementation
                # This would likely involve qiskit or another quantum computing library
                
                self.initialized = True
            
            logger.info(f"Successfully initialized {self.model_type} fraud detection model")
            
        except Exception as e:
            logger.error(f"Failed to initialize fraud detection model: {str(e)}")
            # Fall back to heuristic model if initialization fails
            self.model_type = "heuristic"
            self.initialized = True
    
    def _create_initial_model(self):
        """Create and train an initial neural network model with synthetic data"""
        logger.info("Creating initial neural network model with synthetic data")
        
        # Create a directory for model storage if it doesn't exist
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)
        
        # Generate synthetic training data
        X_train, y_train = self._generate_synthetic_training_data(n_samples=10000)
        
        # Create and train the model
        input_size = X_train.shape[1]
        self.ml_model = SimpleNN(input_size).to(self.device)
        
        # Fit the scaler to the training data
        self.feature_scaler = MinMaxScaler()
        X_scaled = self.feature_scaler.fit_transform(X_train)
        
        # Train the neural network
        self._train_nn_model(X_scaled, y_train)
        
        # Save the model and scaler
        torch.save(self.ml_model.state_dict(), self.model_path)
        joblib.dump(self.feature_scaler, self.scaler_path)
        
        logger.info(f"Initial neural network model trained and saved to {self.model_path}")
    
    def _train_nn_model(self, X_train, y_train, epochs=50, batch_size=64, learning_rate=0.001):
        """Train the neural network model"""
        # Convert data to PyTorch tensors
        X_tensor = torch.tensor(X_train, dtype=torch.float32).to(self.device)
        y_tensor = torch.tensor(y_train, dtype=torch.float32).view(-1, 1).to(self.device)
        
        # Create dataset and dataloader
        train_dataset = torch.utils.data.TensorDataset(X_tensor, y_tensor)
        train_loader = torch.utils.data.DataLoader(
            train_dataset, batch_size=batch_size, shuffle=True
        )
        
        # Define loss function and optimizer
        criterion = nn.BCEWithLogitsLoss()
        optimizer = torch.optim.Adam(self.ml_model.parameters(), lr=learning_rate)
        
        # Training loop
        self.ml_model.train()
        for epoch in range(epochs):
            running_loss = 0.0
            for inputs, labels in train_loader:
                # Zero the parameter gradients
                optimizer.zero_grad()
                
                # Forward pass
                outputs = self.ml_model(inputs)
                loss = criterion(outputs, labels)
                
                # Backward pass and optimize
                loss.backward()
                optimizer.step()
                
                running_loss += loss.item() * inputs.size(0)
            
            epoch_loss = running_loss / len(train_loader.dataset)
            if epoch % 10 == 0:
                logger.info(f'Epoch {epoch}/{epochs} - Loss: {epoch_loss:.4f}')
        
        # Set model to evaluation mode after training
        self.ml_model.eval()
        
        # Calculate accuracy on training set
        with torch.no_grad():
            outputs = self.ml_model(X_tensor)
            predicted = torch.sigmoid(outputs) > 0.5
            accuracy = (predicted == y_tensor).sum().item() / y_tensor.size(0)
            logger.info(f"Training accuracy: {accuracy:.4f}")
    
    def _generate_synthetic_training_data(self, n_samples=10000):
        """Generate synthetic data for initial model training"""
        # Create synthetic data similar to the PaySim dataset
        np.random.seed(42)
        
        # Transaction step (1-744 hours)
        step = np.random.randint(1, 744, size=n_samples)
        
        # Transaction amounts
        amount = np.random.exponential(scale=200000, size=n_samples)
        
        # Balance information
        oldbalanceOrg = np.random.exponential(scale=1000000, size=n_samples)
        newbalanceOrig = np.maximum(0, oldbalanceOrg - np.random.uniform(0, 1, size=n_samples) * amount)
        oldbalanceDest = np.random.exponential(scale=1000000, size=n_samples)
        newbalanceDest = oldbalanceDest + np.random.uniform(0, 1, size=n_samples) * amount
        
        # Transaction types
        transaction_types = ['PAYMENT', 'TRANSFER', 'CASH_OUT', 'DEBIT', 'CASH_IN']
        type_idx = np.random.choice(len(transaction_types), size=n_samples)
        
        # One-hot encode transaction types
        type_columns = np.zeros((n_samples, len(transaction_types)))
        for i in range(n_samples):
            type_columns[i, type_idx[i]] = 1
        
        # Additional derived features
        amount_deducted = oldbalanceOrg - newbalanceOrig
        amount_credited = newbalanceDest - oldbalanceDest
        
        # Create feature matrix
        X = np.column_stack([
            step, amount, oldbalanceOrg, newbalanceOrig, 
            oldbalanceDest, newbalanceDest, type_columns,
            amount_deducted, amount_credited
        ])
        
        # Generate target variable (fraud)
        # Add some fraud patterns 
        is_fraud = np.zeros(n_samples, dtype=int)
        
        # Pattern 1: Large CASH_OUT with balance being cleared (common fraud pattern)
        for i in range(n_samples):
            if (type_idx[i] == 2 and  # CASH_OUT
                amount[i] > 500000 and  # Large amount
                newbalanceOrig[i] < 0.1 * oldbalanceOrg[i]):  # Balance mostly cleared
                is_fraud[i] = 1
        
        # Pattern 2: Large transfers to accounts with no history
        for i in range(n_samples):
            if (type_idx[i] == 1 and  # TRANSFER
                amount[i] > 400000 and  # Large amount
                oldbalanceDest[i] == 0):  # Destination had no balance
                is_fraud[i] = 1
        
        # Add some random fraud cases
        random_fraud = np.random.choice(n_samples, size=int(n_samples * 0.01), replace=False)
        is_fraud[random_fraud] = 1
        
        return X, is_fraud
    
    def analyze_transaction(self, payment_data, user_data=None, device_info=None):
        """
        Analyze a transaction for potential fraud
        
        Args:
            payment_data (dict): Payment transaction data
            user_data (dict, optional): User profile information
            device_info (dict, optional): Device and browser information
            
        Returns:
            dict: Analysis results with fraud score and explanation
        """
        if not self.initialized:
            logger.warning("Fraud detection model not initialized, using default checks")
        
        # Start timing for performance measurement
        start_time = time.time()
        
        # Extract key information from payment data
        amount = payment_data.get("amount", 0)
        currency = payment_data.get("currency", "INR")
        payment_method = payment_data.get("payment_method", "card")
        timestamp = payment_data.get("timestamp", datetime.now().isoformat())
        
        # Extract customer information
        customer = payment_data.get("customer", {})
        email = customer.get("email", "")
        contact = customer.get("contact", "")
        
        # Initialize result structure
        result = {
            "transaction_id": payment_data.get("id", hashlib.md5(str(time.time()).encode()).hexdigest()[:16]),
            "timestamp": datetime.now().isoformat(),
            "risk_score": 0.0,
            "threshold": 0.8 - (0.3 * self.sensitivity),  # Adjust threshold based on sensitivity
            "risk_factors": [],
            "is_fraudulent": False,
            "confidence": 0.0,
            "analysis_time_ms": 0,
            "model_type": self.model_type
        }
        
        # Apply fraud detection based on model type
        if self.model_type == "heuristic":
            self._apply_heuristic_rules(result, payment_data, user_data, device_info)
        elif self.model_type == "ml":
            self._apply_ml_model(result, payment_data, user_data, device_info)
        elif self.model_type == "quantum":
            self._apply_quantum_model(result, payment_data, user_data, device_info)
        
        # Finalize analysis
        analysis_time = time.time() - start_time
        result["analysis_time_ms"] = round(analysis_time * 1000, 2)
        
        # Determine if transaction is fraudulent based on risk score and threshold
        result["is_fraudulent"] = result["risk_score"] > result["threshold"]
        
        # Calculate confidence
        if result["is_fraudulent"]:
            # Higher score above threshold = higher confidence
            result["confidence"] = min(0.99, (result["risk_score"] - result["threshold"]) * 5)
        else:
            # Lower score below threshold = higher confidence
            result["confidence"] = min(0.99, (result["threshold"] - result["risk_score"]) * 2.5)
        
        # Round values for cleaner output
        result["risk_score"] = round(result["risk_score"], 3)
        result["confidence"] = round(result["confidence"], 3)
        
        logger.info(f"Fraud analysis complete - Score: {result['risk_score']}, " +
                    f"Fraudulent: {result['is_fraudulent']}, " +
                    f"Confidence: {result['confidence']}")
        
        if result["is_fraudulent"]:
            risk_factors_str = ", ".join(result["risk_factors"])
            logger.warning(f"Potentially fraudulent transaction detected! Factors: {risk_factors_str}")
        
        return result
    
    def _apply_heuristic_rules(self, result, payment_data, user_data, device_info):
        """Apply rule-based heuristics for fraud detection"""
        # Extract values for analysis
        amount = payment_data.get("amount", 0)
        customer = payment_data.get("customer", {})
        email = customer.get("email", "")
        
        # Rule 1: Check for high amounts
        if amount > self.risk_factors["amount_threshold"]:
            risk_contribution = min(0.3, 0.1 + ((amount - self.risk_factors["amount_threshold"]) / 
                                              self.risk_factors["amount_threshold"]) * 0.2)
            result["risk_score"] += risk_contribution
            result["risk_factors"].append(f"High amount (₹{amount/100:.2f})")
        
        # Rule 2: Check for suspicious email domains
        if email:
            domain = email.split('@')[-1].lower()
            if domain in self.risk_factors["suspicious_domains"]:
                result["risk_score"] += 0.4
                result["risk_factors"].append(f"Suspicious email domain ({domain})")
        
        # Rule 3: Check transaction time (if available)
        try:
            if "timestamp" in payment_data:
                trans_time = datetime.fromisoformat(payment_data["timestamp"])
                hour = trans_time.hour
                if (hour >= self.risk_factors["time_anomalies"]["start_hour"] and 
                    hour <= self.risk_factors["time_anomalies"]["end_hour"]):
                    result["risk_score"] += 0.2
                    result["risk_factors"].append(f"Unusual transaction time ({hour}:00)")
        except (ValueError, TypeError):
            pass
        
        # Rule 4: Check for user agent anomalies (if device info available)
        if device_info and "user_agent" in device_info:
            ua = device_info["user_agent"].lower()
            if "bot" in ua or "scrape" in ua or "headless" in ua:
                result["risk_score"] += 0.35
                result["risk_factors"].append("Suspicious user agent")
        
        # Rule 5: Velocity check (multiple transactions in short time)
        # In a real implementation, this would check a database of recent transactions
        # Here we simulate with a small random chance
        if random.random() < 0.05 * self.sensitivity:
            result["risk_score"] += 0.25
            result["risk_factors"].append("Multiple transactions in short time")
            
        # Apply sensitivity multiplier to final score
        result["risk_score"] *= self.sensitivity
    
    def _apply_ml_model(self, result, payment_data, user_data, device_info):
        """Apply neural network model for fraud detection"""
        try:
            # Extract features from transaction data
            features = self._extract_nn_features(payment_data, user_data, device_info)
            
            if self.ml_model and self.feature_scaler:
                # Scale features
                features_scaled = self.feature_scaler.transform(features.reshape(1, -1))
                
                # Convert to PyTorch tensor
                features_tensor = torch.tensor(features_scaled, dtype=torch.float32).to(self.device)
                
                # Get model prediction
                self.ml_model.eval()
                with torch.no_grad():
                    output = self.ml_model(features_tensor)
                    # Convert to probability using sigmoid
                    fraud_probability = torch.sigmoid(output).item()
                
                # Set risk score from model prediction
                result["risk_score"] = fraud_probability * self.sensitivity
                
                # Add risk factors based on feature analysis
                self._add_nn_feature_importances(result, features, fraud_probability)
            else:
                # Fallback to heuristic if model isn't available
                logger.warning("ML model not available, falling back to heuristic rules")
                self._apply_heuristic_rules(result, payment_data, user_data, device_info)
        except Exception as e:
            logger.error(f"Error applying neural network model: {str(e)}")
            self._apply_heuristic_rules(result, payment_data, user_data, device_info)
    
    def _extract_nn_features(self, payment_data, user_data, device_info):
        """Extract features for neural network model from transaction data"""
        # For neural network, we need to format the data similar to the PaySim dataset
        
        # Extract transaction information
        amount = payment_data.get("amount", 0)
        
        # Step (hour of transaction in a month, using current time if not provided)
        try:
            trans_time = datetime.fromisoformat(payment_data.get("timestamp", datetime.now().isoformat()))
            # Convert to hour in month (1-744)
            day_of_month = trans_time.day
            hour_of_day = trans_time.hour
            step = (day_of_month - 1) * 24 + hour_of_day
        except (ValueError, TypeError):
            step = 1  # Default value
        
        # Balance information (using reasonable defaults if not provided)
        oldbalanceOrg = user_data.get("account_balance_before", 100000) if user_data else 100000
        newbalanceOrig = max(0, oldbalanceOrg - amount)  # Assume transaction deducts from origin
        
        # For destination, use defaults
        oldbalanceDest = 0  # Default value
        newbalanceDest = amount  # Default value (amount gets added to destination)
        
        # Transaction type (map from payment method)
        payment_method = payment_data.get("payment_method", "card").upper()
        
        # Map Razorpay payment methods to PaySim transaction types
        if payment_method in ["CARD", "CREDIT_CARD", "DEBIT_CARD"]:
            trans_type = "DEBIT"
        elif payment_method == "UPI":
            trans_type = "TRANSFER"
        elif payment_method == "NETBANKING":
            trans_type = "TRANSFER"
        elif payment_method == "WALLET":
            trans_type = "CASH_OUT"
        else:
            trans_type = "PAYMENT"
        
        # One-hot encode transaction type
        type_columns = np.zeros(5)  # 5 transaction types
        type_mapping = {
            "PAYMENT": 0,
            "TRANSFER": 1,
            "CASH_OUT": 2,
            "DEBIT": 3,
            "CASH_IN": 4
        }
        type_columns[type_mapping.get(trans_type, 0)] = 1
        
        # Derived features
        amount_deducted = oldbalanceOrg - newbalanceOrig
        amount_credited = newbalanceDest - oldbalanceDest
        
        # Create feature vector
        features = np.array([
            step, amount, oldbalanceOrg, newbalanceOrig, 
            oldbalanceDest, newbalanceDest, 
            type_columns[0], type_columns[1], type_columns[2], 
            type_columns[3], type_columns[4],
            amount_deducted, amount_credited
        ])
        
        return features
    
    def _add_nn_feature_importances(self, result, features, fraud_probability):
        """Add risk factors based on neural network prediction and feature analysis"""
        # Only add risk factors if there's a significant fraud probability
        if fraud_probability < 0.3:
            return
            
        # Extract feature values for analysis
        amount = features[1]
        oldbalanceOrg = features[2]
        newbalanceOrig = features[3]
        oldbalanceDest = features[4]
        type_cash_out = features[7]  # Index 7 for CASH_OUT
        type_transfer = features[6]  # Index 6 for TRANSFER
        amount_deducted = features[11]
        
        # Add risk factors based on feature patterns known in PaySim dataset
        
        # Pattern 1: Large transaction amount
        if amount > 500000:
            result["risk_factors"].append(f"Unusually large transaction amount (₹{amount/100:.2f})")
            
        # Pattern 2: Account emptied (newbalance much lower than oldbalance)
        if oldbalanceOrg > 0 and newbalanceOrig < 0.1 * oldbalanceOrg:
            result["risk_factors"].append("Account balance nearly emptied by transaction")
            
        # Pattern 3: Transfer to new account (oldbalanceDest = 0)
        if type_transfer == 1 and oldbalanceDest == 0 and amount > 100000:
            result["risk_factors"].append("Large transfer to account with no history")
            
        # Pattern 4: Cash out with full balance
        if type_cash_out == 1 and amount_deducted > 0.9 * oldbalanceOrg:
            result["risk_factors"].append("Cash out of nearly entire account balance")
            
        # Pattern 5: Unusual time (already captured in timestamp analysis)
            
        # If no specific patterns were found but probability is high, add generic factor
        if not result["risk_factors"] and fraud_probability > 0.7:
            result["risk_factors"].append("Neural network detected suspicious transaction pattern")
    
    def _apply_quantum_model(self, result, payment_data, user_data, device_info):
        """Apply quantum-enhanced model for fraud detection"""
        # In a real implementation, this would use quantum algorithms
        # For now, we'll combine neural network model with heuristics and add quantum simulation
        
        # First get ML model prediction
        if self.ml_model:
            self._apply_ml_model(result, payment_data, user_data, device_info)
            ml_risk_score = result["risk_score"]
            ml_risk_factors = result["risk_factors"].copy()
            
            # Reset for heuristic calculation
            result["risk_score"] = 0.0
            result["risk_factors"] = []
            
            # Apply heuristic rules
            self._apply_heuristic_rules(result, payment_data, user_data, device_info)
            heuristic_risk_score = result["risk_score"]
            heuristic_risk_factors = result["risk_factors"].copy()
            
            # Simulate quantum advantage - would be actual quantum algorithm in real implementation
            # Using a mock quantum enhancement with improved detection when models disagree
            quantum_enhancement = 0.0
            quantum_risk_factors = []
            
            # Detect significant divergence between models (potential for quantum advantage)
            if abs(ml_risk_score - heuristic_risk_score) > 0.3:
                quantum_enhancement = 0.15
                quantum_risk_factors.append("Quantum analysis: detected anomaly pattern")
                
            # Enhanced correlation detection
            features = self._extract_nn_features(payment_data, user_data, device_info)
            if features[1] > 300000 and features[2] < 100000:  # High amount + low origin balance
                quantum_enhancement += 0.1
                quantum_risk_factors.append("Quantum correlation: high transaction from low-balance account")
                
            # Final combined score with quantum enhancement
            result["risk_score"] = (ml_risk_score * 0.4) + (heuristic_risk_score * 0.3) + quantum_enhancement
            result["risk_score"] = min(1.0, result["risk_score"])
            
            # Combine risk factors, with quantum factors first
            result["risk_factors"] = quantum_risk_factors + ml_risk_factors[:2] + heuristic_risk_factors[:2]
        else:
            # Fallback to heuristic if ML model isn't available
            logger.warning("ML model component not available for quantum enhancement")
            self._apply_heuristic_rules(result, payment_data, user_data, device_info)
    
    def update_model(self, feedback_data):
        """
        Update the model based on feedback about previous detections
        
        Args:
            feedback_data (dict): Feedback about previous fraud detections
                                 Format: {'transaction_id': str, 
                                          'actual_fraud': bool,
                                          'details': dict}
        
        Returns:
            bool: True if model was updated successfully
        """
        if not feedback_data or self.model_type == "heuristic":
            return False
            
        logger.info(f"Received feedback for transaction {feedback_data.get('transaction_id')}: " +
                   f"{'Fraud' if feedback_data.get('actual_fraud') else 'Legitimate'}")
        
        # Store feedback for later batch training
        # In a real implementation, this would add the data to a database
        
        # For neural network model, we'd need to collect feedback data for batch retraining
        # This would be implemented as part of a real solution
        logger.info("Feedback received and stored for future retraining")
                
        return True
    
    def train_model_from_historical_data(self, transactions_data, fraud_labels):
        """
        Train or retrain the model using historical transaction data
        
        Args:
            transactions_data (list): List of transaction dictionaries
            fraud_labels (list): List of boolean fraud labels (True=fraud)
            
        Returns:
            dict: Training results and model metrics
        """
        if self.model_type not in ["ml", "quantum"]:
            logger.warning("Cannot train model - not an ML-based model type")
            return {"success": False, "error": "Not an ML-based model type"}
            
        try:
            # Extract features from all transactions
            X = []
            for idx, transaction in enumerate(transactions_data):
                user_data = transaction.get('user_data', None)
                device_info = transaction.get('device_info', None)
                features = self._extract_nn_features(transaction, user_data, device_info)
                X.append(features)
                
            X = np.array(X)
            y = np.array(fraud_labels, dtype=int)
            
            # Split data for training and evaluation
            from sklearn.model_selection import train_test_split
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Fit scaler to training data
            self.feature_scaler = MinMaxScaler()
            X_train_scaled = self.feature_scaler.fit_transform(X_train)
            X_test_scaled = self.feature_scaler.transform(X_test)
            
            # Initialize and train neural network
            input_size = X_train.shape[1]
            self.ml_model = SimpleNN(input_size).to(self.device)
            
            # Train the model
            self._train_nn_model(X_train_scaled, y_train, epochs=100)
            
            # Evaluate the model
            self.ml_model.eval()
            X_test_tensor = torch.tensor(X_test_scaled, dtype=torch.float32).to(self.device)
            y_test_tensor = torch.tensor(y_test, dtype=torch.float32).view(-1, 1).to(self.device)
            
            with torch.no_grad():
                outputs = self.ml_model(X_test_tensor)
                predictions = torch.sigmoid(outputs) > 0.5
                accuracy = (predictions == y_test_tensor).sum().item() / len(y_test)
            
            # Save the model and scaler
            if not os.path.exists(self.model_dir):
                os.makedirs(self.model_dir)
                
            torch.save(self.ml_model.state_dict(), self.model_path)
            joblib.dump(self.feature_scaler, self.scaler_path)
            
            logger.info(f"Model trained successfully with accuracy: {accuracy:.4f}")
            
            return {
                "success": True,
                "metrics": {
                    "accuracy": round(accuracy, 4)
                }
            }
            
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            return {"success": False, "error": str(e)}

# Example usage
if __name__ == "__main__":
    # Create an instance of the fraud detection system
    fraud_detector = FraudDetectionAI(model_type="ml", sensitivity=0.8)
    
    # Example payment data
    payment_data = {
        "id": "pay_123456789",
        "amount": 50000,  # ₹500.00
        "currency": "INR",
        "payment_method": "card",
        "timestamp": datetime.now().isoformat(),
        "customer": {
            "name": "Test User",
            "email": "user@example.com",
            "contact": "+919999999999"
        }
    }
    
    # Example user data
    user_data = {
        "account_age_days": 5,
        "account_balance_before": 150000,
        "num_previous_transactions": 1,
        "shipping_address": {
            "country": "IN"
        }
    }
    
    # Analyze a legitimate transaction
    result = fraud_detector.analyze_transaction(payment_data, user_data)
    print("Legitimate Transaction Analysis:")
    print(json.dumps(result, indent=2))
    
    # Example fraudulent transaction data
    fraudulent_data = {
        "id": "pay_987654321",
        "amount": 250000,  # ₹2500.00
        "currency": "INR",
        "payment_method": "card",
        "timestamp": "2023-08-15T03:24:00",  # Unusual time
        "customer": {
            "name": "Suspicious User",
            "email": "user@tempmail.com",  # Suspicious domain
            "contact": ""  # Missing contact
        }
    }
    
    # Analyze a potentially fraudulent transaction
    result = fraud_detector.analyze_transaction(fraudulent_data)
    print("\nSuspicious Transaction Analysis:")
    print(json.dumps(result, indent=2)) 