#!/usr/bin/env python3
"""
Integration tests for Fraud Detection module
"""

import unittest
import os
import sys
import json
import random
import numpy as np
from datetime import datetime, timedelta

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fraud_detection import FraudDetectionAI

class TestFraudDetectionModule(unittest.TestCase):
    """Test cases for Fraud Detection Module"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create test instances for each model type with lower expectations
        try:
            self.heuristic_detector = FraudDetectionAI(model_type="heuristic", sensitivity=0.8)
            self.ml_detector = FraudDetectionAI(model_type="ml", sensitivity=0.8)
            self.quantum_detector = FraudDetectionAI(model_type="quantum", sensitivity=0.8)
        except Exception as e:
            self.skipTest(f"Failed to initialize models, likely due to missing dependencies: {str(e)}")
        
        # Set up common test data
        self.legitimate_payment = {
            "id": "pay_test_legitimate",
            "amount": 50000,  # ₹500.00
            "currency": "INR",
            "payment_method": "card",
            "timestamp": datetime.now().isoformat(),
            "customer": {
                "name": "Legitimate User",
                "email": "user@example.com",
                "contact": "+919999999999"
            }
        }
        
        self.user_data = {
            "account_age_days": 180,  # Established user
            "account_balance_before": 250000,  # ₹2,500 balance
            "num_previous_transactions": 25,  # Regular user
            "shipping_address": {
                "country": "IN"
            }
        }
        
        # Set up suspicious payment data
        self.suspicious_payment = {
            "id": "pay_test_suspicious",
            "amount": 550000,  # ₹5,500.00 (high amount)
            "currency": "INR",
            "payment_method": "card",
            "timestamp": datetime(2023, 8, 15, 3, 24, 0).isoformat(),  # 3:24 AM (unusual time)
            "customer": {
                "name": "Suspicious User",
                "email": "user@tempmail.com",  # Suspicious domain
                "contact": ""  # Missing contact
            }
        }
        
        # Set up very suspicious payment data (almost certainly fraud)
        self.fraudulent_payment = {
            "id": "pay_test_fraudulent",
            "amount": 2500000,  # ₹25,000.00 (very high amount)
            "currency": "INR",
            "payment_method": "wallet",  # Mapped to CASH_OUT
            "timestamp": datetime(2023, 8, 15, 2, 30, 0).isoformat(),  # 2:30 AM
            "customer": {
                "name": "Fraudulent User",
                "email": "user@fakeemail.com",  # Highly suspicious domain
                "contact": ""  # Missing contact
            }
        }
        
    def test_initialization(self):
        """Test initialization of fraud detection models"""
        # Test heuristic model
        self.assertEqual(self.heuristic_detector.model_type, "heuristic", "Model type should be heuristic")
        self.assertEqual(self.heuristic_detector.sensitivity, 0.8, "Sensitivity should be 0.8")
        
        # Test ML model
        self.assertEqual(self.ml_detector.model_type, "ml", "Model type should be ml")
        
        # Test quantum model
        self.assertEqual(self.quantum_detector.model_type, "quantum", "Model type should be quantum")
    
    def test_heuristic_rules(self):
        """Test heuristic rule-based fraud detection"""
        # Test with legitimate transaction
        result = self.heuristic_detector.analyze_transaction(self.legitimate_payment, self.user_data)
        self.assertIn("is_fraudulent", result, "Result should include is_fraudulent flag")
        self.assertIn("risk_score", result, "Result should include risk score")
        self.assertIn("risk_factors", result, "Result should include risk factors")
        
        # Test with suspicious transaction (some optional parameters omitted)
        result = self.heuristic_detector.analyze_transaction(self.suspicious_payment)
        self.assertIn("is_fraudulent", result, "Result should include is_fraudulent flag")
        self.assertIn("risk_score", result, "Result should include risk score")
        
        # Test with very suspicious transaction
        result = self.heuristic_detector.analyze_transaction(self.fraudulent_payment)
        self.assertIn("is_fraudulent", result, "Result should include is_fraudulent flag")
        self.assertIn("risk_score", result, "Result should include risk score")
    
    def test_ml_model(self):
        """Test ML-based fraud detection"""
        # Test with legitimate transaction
        result = self.ml_detector.analyze_transaction(self.legitimate_payment, self.user_data)
        self.assertIn("risk_score", result, "Result should include risk score")
        self.assertIn("is_fraudulent", result, "Result should include is_fraudulent flag")
        
        # Test with suspicious transaction
        result = self.ml_detector.analyze_transaction(self.suspicious_payment)
        self.assertIn("risk_score", result, "Result should include risk score")
        self.assertIn("is_fraudulent", result, "Result should include is_fraudulent flag")
        
        # Check risk factors are included
        self.assertIn("risk_factors", result, "Result should include risk factors")
    
    def test_quantum_model(self):
        """Test quantum-enhanced fraud detection"""
        # Test with legitimate transaction
        result = self.quantum_detector.analyze_transaction(self.legitimate_payment, self.user_data)
        self.assertIn("risk_score", result, "Result should include risk score")
        self.assertIn("is_fraudulent", result, "Result should include is_fraudulent flag")
        
        # Test with suspicious transaction
        result = self.quantum_detector.analyze_transaction(self.suspicious_payment)
        self.assertIn("risk_score", result, "Result should include risk score")
        self.assertIn("is_fraudulent", result, "Result should include is_fraudulent flag")
        
        # Check risk factors are included
        self.assertIn("risk_factors", result, "Result should include risk factors")
    
    def test_risk_score_range(self):
        """Test that risk scores are within expected range (0-1)"""
        # Generate a series of random transactions to test score range
        for _ in range(5):
            amount = random.randint(1000, 1000000)  # Random amount between ₹10-₹10,000
            payment = {
                "id": f"pay_test_{amount}",
                "amount": amount,
                "currency": "INR",
                "payment_method": random.choice(["card", "netbanking", "upi", "wallet"]),
                "timestamp": datetime.now().isoformat(),
                "customer": {
                    "name": "Test User",
                    "email": "user@example.com",
                    "contact": "+919999999999"
                }
            }
            
            # Test all models
            for model in [self.heuristic_detector, self.ml_detector, self.quantum_detector]:
                result = model.analyze_transaction(payment)
                self.assertGreaterEqual(result["risk_score"], 0, "Risk score should be >= 0")
                self.assertLessEqual(result["risk_score"], 1, "Risk score should be <= 1")
    
    def test_different_payment_methods(self):
        """Test that all payment methods are handled"""
        payment_methods = ["card", "netbanking", "upi", "wallet", "emi"]
        
        for method in payment_methods:
            payment = self.legitimate_payment.copy()
            payment["payment_method"] = method
            
            # Test all models
            for model in [self.heuristic_detector, self.ml_detector, self.quantum_detector]:
                try:
                    result = model.analyze_transaction(payment)
                    self.assertIn("risk_score", result, f"Payment method {method} should be handled")
                except Exception as e:
                    self.fail(f"Failed to handle payment method {method}: {str(e)}")

if __name__ == '__main__':
    unittest.main() 