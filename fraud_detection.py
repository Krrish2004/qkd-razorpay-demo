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

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Fraud Detection')

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
                
            elif self.model_type == "ml":
                # Simulate loading a machine learning model
                logger.info("Loading machine learning model")
                # In a real implementation, would load a trained model here
                # Example: self.model = joblib.load('fraud_detection_model.pkl')
                time.sleep(1.0)  # Simulate model loading time
                
            elif self.model_type == "quantum":
                # Simulate a quantum-enhanced ML model
                logger.info("Initializing quantum-enhanced fraud detection model")
                # In a real implementation, would initialize a quantum model
                time.sleep(1.5)  # Simulate initialization time
            
            self.initialized = True
            logger.info(f"Successfully initialized {self.model_type} fraud detection model")
            
        except Exception as e:
            logger.error(f"Failed to initialize fraud detection model: {str(e)}")
            # Fall back to heuristic model if initialization fails
            self.model_type = "heuristic"
            self.initialized = True
    
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
        """Apply machine learning model for fraud detection"""
        # In a real implementation, this would:
        # 1. Preprocess and transform the payment data into features
        # 2. Apply a pre-trained ML model to predict fraud probability
        # 3. Return the prediction and feature importance
        
        # For this demo, we simulate ML analysis
        
        # Extract features that would be used by ML model
        feature_vector = self._extract_ml_features(payment_data, user_data, device_info)
        
        # Simulate model prediction (in reality would be model.predict_proba(features))
        base_score = self._simulate_ml_prediction(feature_vector)
        
        # Simulate feature importance
        important_features = self._simulate_feature_importance(feature_vector, base_score)
        
        # Set risk score from model prediction
        result["risk_score"] = base_score * self.sensitivity
        
        # Add important features as risk factors
        result["risk_factors"] = important_features
    
    def _extract_ml_features(self, payment_data, user_data, device_info):
        """Extract features for ML model from transaction data"""
        # In a real implementation, this would transform raw data into features
        # For simulation, we create a simplified feature vector
        
        features = {
            "amount": payment_data.get("amount", 0) / 100000,  # Normalized amount
            "has_email": 1 if payment_data.get("customer", {}).get("email") else 0,
            "has_phone": 1 if payment_data.get("customer", {}).get("contact") else 0,
            "card_payment": 1 if payment_data.get("payment_method") == "card" else 0,
            "upi_payment": 1 if payment_data.get("payment_method") == "upi" else 0,
            "new_customer": 0 if user_data and user_data.get("account_age_days", 0) > 30 else 1,
            "mobile_device": 1 if device_info and "mobile" in device_info.get("user_agent", "").lower() else 0,
            # Add more features as needed
        }
        
        return features
    
    def _simulate_ml_prediction(self, feature_vector):
        """Simulate an ML model prediction"""
        # Calculate a base risk score using the features
        # In reality, this would be the output of a trained model
        
        base_score = 0.0
        
        # Higher amounts increase risk
        base_score += feature_vector["amount"] * 0.3
        
        # Lack of contact info increases risk
        if not feature_vector["has_email"]:
            base_score += 0.2
        if not feature_vector["has_phone"]:
            base_score += 0.15
            
        # New customers are higher risk
        if feature_vector["new_customer"]:
            base_score += 0.25
            
        # Add some randomness to simulate model complexity
        base_score += random.uniform(-0.1, 0.1)
        
        # Ensure score is between 0 and 1
        return max(0.0, min(1.0, base_score))
    
    def _simulate_feature_importance(self, feature_vector, base_score):
        """Simulate feature importance from an ML model"""
        important_features = []
        
        # Check which features contributed most to the risk score
        if feature_vector["amount"] > 0.5:
            important_features.append(f"High transaction amount (₹{feature_vector['amount']*100000/100:.2f})")
            
        if not feature_vector["has_email"]:
            important_features.append("Missing email address")
            
        if not feature_vector["has_phone"]:
            important_features.append("Missing phone number")
            
        if feature_vector["new_customer"]:
            important_features.append("New customer account")
            
        # Add at least one random factor if list is empty
        if not important_features and base_score > 0.3:
            potential_factors = [
                "Unusual purchase pattern",
                "Behavioral anomaly",
                "Device fingerprint mismatch",
                "IP address risk"
            ]
            important_features.append(random.choice(potential_factors))
            
        return important_features
    
    def _apply_quantum_model(self, result, payment_data, user_data, device_info):
        """Apply quantum-enhanced model for fraud detection"""
        # In a real implementation, this would use a quantum algorithm or
        # a quantum-inspired classical algorithm for anomaly detection
        
        # For this demonstration, we combine the heuristic and ML approaches
        # and add a "quantum advantage" simulation
        
        # Apply both previous models
        self._apply_heuristic_rules(result, payment_data, user_data, device_info)
        
        # Save heuristic score
        heuristic_score = result["risk_score"]
        result["risk_score"] = 0.0
        result["risk_factors"] = []
        
        # Apply ML model
        self._apply_ml_model(result, payment_data, user_data, device_info)
        
        # Combine scores with "quantum advantage"
        ml_score = result["risk_score"]
        
        # Simulate quantum enhancement: better anomaly detection and pattern recognition
        # In a real quantum model, this might use quantum feature maps or quantum neural networks
        quantum_advantage = 0.0
        
        # Detect anomalies more effectively
        if abs(heuristic_score - ml_score) > 0.3:
            quantum_advantage = 0.15
            result["risk_factors"].append("Quantum anomaly detection: inconsistent risk patterns")
        
        # Enhanced correlation detection
        if "amount" in payment_data and "customer" in payment_data:
            if payment_data["amount"] > 10000 and not payment_data["customer"].get("email"):
                quantum_advantage += 0.1
                result["risk_factors"].append("Quantum correlation: high amount with missing contact info")
        
        # Final quantum-enhanced score
        result["risk_score"] = (heuristic_score * 0.3) + (ml_score * 0.5) + quantum_advantage
        result["risk_score"] = min(1.0, result["risk_score"])
    
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
        if not feedback_data:
            return False
            
        # In a real implementation, this would:
        # 1. Store the feedback data to use for retraining
        # 2. Periodically retrain the model with new data
        # 3. Adjust the model parameters or rules based on feedback
        
        logger.info(f"Received feedback for transaction {feedback_data.get('transaction_id')}: " +
                   f"{'Fraud' if feedback_data.get('actual_fraud') else 'Legitimate'}")
        
        # For the demo, just log that we received feedback
        return True

# Example usage
if __name__ == "__main__":
    # Create an instance of the fraud detection system
    fraud_detector = FraudDetectionAI(model_type="heuristic", sensitivity=0.8)
    
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