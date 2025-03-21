#!/usr/bin/env python3
"""
Unit tests for Razorpay API integration module
"""

import unittest
import os
import sys
import uuid
from unittest.mock import patch, MagicMock

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from razorpay_api import RazorpayIntegration

class TestRazorpayModule(unittest.TestCase):
    """Test cases for Razorpay API Module"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a test instance in test mode with dummy keys
        self.razorpay = RazorpayIntegration(test_mode=True)
        
        # Test data
        self.test_amount = 50000  # ₹500.00
        self.test_currency = "INR"
        self.test_receipt = f"test_receipt_{uuid.uuid4().hex[:8]}"
        self.test_notes = {"purpose": "test"}
        
        # Sample customer
        self.test_customer = {
            "name": "Test Customer",
            "email": "test@example.com",
            "contact": "+919999999999"
        }
    
    def test_initialization(self):
        """Test Razorpay client initialization"""
        # Test with test mode
        razorpay_test = RazorpayIntegration(test_mode=True)
        self.assertTrue(razorpay_test.test_mode, "Test mode should be enabled")
        self.assertIsNotNone(razorpay_test.key_id, "Key ID should not be None")
        self.assertIsNotNone(razorpay_test.key_secret, "Key secret should not be None")
        
        # Test without keys in environment
        with patch.dict(os.environ, {}, clear=True):
            razorpay_test = RazorpayIntegration(test_mode=True)
            self.assertTrue(razorpay_test.test_mode, "Test mode should be enabled")
            self.assertEqual(razorpay_test.key_id, "rzp_test_dummy_key_id", 
                             "Dummy key ID should be used in test mode")
    
    def test_create_order(self):
        """Test order creation"""
        order = self.razorpay.create_order(
            amount=self.test_amount,
            currency=self.test_currency,
            receipt=self.test_receipt,
            notes=self.test_notes
        )
        
        # Check order properties
        self.assertIsNotNone(order, "Order should not be None")
        self.assertIn('id', order, "Order should have an ID")
        self.assertEqual(order['amount'], self.test_amount, "Order amount should match input")
        self.assertEqual(order['currency'], self.test_currency, "Order currency should match input")
        self.assertEqual(order['receipt'], self.test_receipt, "Order receipt should match input")
        self.assertEqual(order['notes'], self.test_notes, "Order notes should match input")
        self.assertEqual(order['status'], 'created', "Order status should be 'created'")
    
    def test_create_payment_link(self):
        """Test payment link creation"""
        description = "Test payment link"
        payment_link = self.razorpay.create_payment_link(
            amount=self.test_amount,
            currency=self.test_currency,
            description=description,
            customer=self.test_customer
        )
        
        # Check payment link properties
        self.assertIsNotNone(payment_link, "Payment link should not be None")
        self.assertIn('id', payment_link, "Payment link should have an ID")
        self.assertEqual(payment_link['amount'], self.test_amount, "Payment link amount should match input")
        self.assertEqual(payment_link['currency'], self.test_currency, "Payment link currency should match input")
        self.assertEqual(payment_link['description'], description, "Payment link description should match input")
        self.assertIn('short_url', payment_link, "Payment link should have a short URL")
    
    def test_verify_payment_signature(self):
        """Test payment signature verification"""
        # Create a test order
        order = self.razorpay.create_order(
            amount=self.test_amount,
            currency=self.test_currency
        )
        
        # Generate a random payment ID
        payment_id = f"pay_test_{uuid.uuid4().hex[:16]}"
        
        # Test with dummy signature
        result = self.razorpay.verify_payment_signature(
            payment_id=payment_id,
            order_id=order['id'],
            signature="dummy_signature"
        )
        
        # In test mode with dummy keys, verification should always succeed
        self.assertTrue(result, "Signature verification should succeed in test mode")
        
        # Test with real API client (should call utility.verify_payment_signature)
        with patch.object(self.razorpay.client.utility, 'verify_payment_signature', 
                          side_effect=Exception("Invalid signature")):
            # Override the dummy key check
            self.razorpay.key_id = "rzp_test_real_key"
            
            result = self.razorpay.verify_payment_signature(
                payment_id=payment_id,
                order_id=order['id'],
                signature="invalid_signature"
            )
            
            # Should fail with invalid signature
            self.assertFalse(result, "Signature verification should fail with invalid signature")
    
    def test_get_payment_details(self):
        """Test retrieving payment details"""
        # Generate a random payment ID
        payment_id = f"pay_test_{uuid.uuid4().hex[:16]}"
        
        # Get payment details
        payment = self.razorpay.get_payment_details(payment_id)
        
        # Check payment properties
        self.assertIsNotNone(payment, "Payment details should not be None")
        self.assertEqual(payment['id'], payment_id, "Payment ID should match input")
        self.assertIn('status', payment, "Payment should have a status")
        self.assertIn('amount', payment, "Payment should have an amount")
        self.assertIn('currency', payment, "Payment should have a currency")
    
    def test_refund_payment(self):
        """Test refunding a payment"""
        # Generate a random payment ID
        payment_id = f"pay_test_{uuid.uuid4().hex[:16]}"
        
        # Full refund
        refund = self.razorpay.refund_payment(payment_id)
        
        # Check refund properties
        self.assertIsNotNone(refund, "Refund should not be None")
        self.assertIn('id', refund, "Refund should have an ID")
        self.assertEqual(refund['payment_id'], payment_id, "Refund payment ID should match input")
        self.assertIn('status', refund, "Refund should have a status")
        
        # Partial refund
        partial_amount = 25000  # ₹250.00
        partial_refund = self.razorpay.refund_payment(payment_id, amount=partial_amount)
        
        # Check partial refund properties
        self.assertEqual(partial_refund['amount'], partial_amount, "Partial refund amount should match input")
    
    def test_capture_payment(self):
        """Test capturing a payment"""
        # Generate a random payment ID
        payment_id = f"pay_test_{uuid.uuid4().hex[:16]}"
        
        # Capture payment
        capture = self.razorpay.capture_payment(
            payment_id=payment_id,
            amount=self.test_amount,
            currency=self.test_currency
        )
        
        # Check capture properties
        self.assertIsNotNone(capture, "Capture should not be None")
        self.assertEqual(capture['id'], payment_id, "Capture payment ID should match input")
        self.assertEqual(capture['amount'], self.test_amount, "Capture amount should match input")
        self.assertEqual(capture['currency'], self.test_currency, "Capture currency should match input")
        self.assertEqual(capture['status'], 'captured', "Capture status should be 'captured'")
    
    def test_real_api_client(self):
        """Test with a real Razorpay client (mocked)"""
        # Mock the Razorpay client
        mock_client = MagicMock()
        mock_order = MagicMock()
        mock_order.create.return_value = {
            'id': 'order_real_test',
            'amount': self.test_amount,
            'currency': self.test_currency,
            'status': 'created'
        }
        
        # Set up the mock client
        mock_client.order = mock_order
        
        # Replace the client in our test instance
        self.razorpay.client = mock_client
        self.razorpay.key_id = "rzp_test_real_key"  # Not a dummy key
        
        # Test order creation with mocked client
        order = self.razorpay.create_order(
            amount=self.test_amount,
            currency=self.test_currency
        )
        
        # Verify the API call
        mock_order.create.assert_called_once()
        self.assertEqual(order['id'], 'order_real_test', "Order ID should match mock response")

if __name__ == '__main__':
    unittest.main()
