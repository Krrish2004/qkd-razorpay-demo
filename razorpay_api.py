#!/usr/bin/env python3
"""
Razorpay API Module - Handles integration with Razorpay payment gateway
"""

import os
import json
import logging
import uuid
import time
from datetime import datetime
import razorpay
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Razorpay API Module')

class RazorpayIntegration:
    """
    Handles integration with Razorpay payment gateway
    """
    
    def __init__(self, test_mode=True):
        """
        Initialize Razorpay client
        
        Args:
            test_mode (bool): Whether to use test mode (test credentials)
        """
        # Get API keys from environment variables
        self.key_id = os.getenv('RAZORPAY_KEY_ID')
        self.key_secret = os.getenv('RAZORPAY_KEY_SECRET')
        
        if not self.key_id or not self.key_secret:
            logger.warning("Razorpay API keys not found in environment variables")
            if test_mode:
                # Use dummy keys for testing only
                self.key_id = "rzp_test_dummy_key_id"
                self.key_secret = "rzp_test_dummy_key_secret"
                logger.warning("Using dummy API keys for testing")
            else:
                raise ValueError("Razorpay API keys not found. Set RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET environment variables.")
        
        # Initialize Razorpay client
        self.client = razorpay.Client(auth=(self.key_id, self.key_secret))
        
        # Set test mode
        self.test_mode = test_mode
        if test_mode:
            logger.info("Razorpay integration initialized in TEST mode")
        else:
            logger.info("Razorpay integration initialized in PRODUCTION mode")
    
    def create_order(self, amount, currency="INR", receipt=None, notes=None):
        """
        Create a new order in Razorpay
        
        Args:
            amount (int): Amount in smallest currency unit (paise for INR)
            currency (str): Currency code (default: INR)
            receipt (str): Your receipt id (optional)
            notes (dict): Key-value pair for storing additional information (optional)
            
        Returns:
            dict: Order details as returned by Razorpay
        """
        # Generate receipt ID if not provided
        if not receipt:
            receipt = f"qkd_receipt_{uuid.uuid4().hex[:8]}"
        
        # Prepare data
        data = {
            'amount': amount,
            'currency': currency,
            'receipt': receipt,
        }
        
        if notes:
            data['notes'] = notes
        
        # Log transaction initiation
        logger.info(f"Creating order for amount {amount/100} {currency}, receipt: {receipt}")
        
        try:
            # In test mode, we can either use the actual Razorpay test API or simulate a response
            if self.test_mode and self.key_id.startswith("rzp_test_dummy"):
                # Simulate API response for testing
                order_id = f"order_qkd_{uuid.uuid4().hex[:16]}"
                response = {
                    'id': order_id,
                    'entity': 'order',
                    'amount': amount,
                    'amount_paid': 0,
                    'amount_due': amount,
                    'currency': currency,
                    'receipt': receipt,
                    'status': 'created',
                    'attempts': 0,
                    'notes': notes or {},
                    'created_at': int(time.time())
                }
                logger.info(f"Simulated order created with ID: {order_id}")
            else:
                # Make actual API call
                response = self.client.order.create(data=data)
                logger.info(f"Order created with ID: {response['id']}")
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to create order: {str(e)}")
            raise
    
    def create_payment_link(self, amount, currency="INR", description=None, customer=None, expire_by=None, reference_id=None):
        """
        Create a payment link that can be shared with customers
        
        Args:
            amount (int): Amount in smallest currency unit (paise for INR)
            currency (str): Currency code (default: INR)
            description (str): Description of the payment
            customer (dict): Customer details (name, email, contact)
            expire_by (int): Timestamp at which the link expires
            reference_id (str): Reference ID for the payment
            
        Returns:
            dict: Payment link details as returned by Razorpay
        """
        # Generate reference ID if not provided
        if not reference_id:
            reference_id = f"qkd_ref_{uuid.uuid4().hex[:8]}"
        
        # Prepare data
        data = {
            'amount': amount,
            'currency': currency,
            'accept_partial': False,
            'reference_id': reference_id,
            'description': description or f"Payment of {amount/100} {currency}",
        }
        
        if customer:
            data['customer'] = customer
        
        if expire_by:
            data['expire_by'] = expire_by
        
        # Log transaction initiation
        logger.info(f"Creating payment link for amount {amount/100} {currency}, ref: {reference_id}")
        
        try:
            # In test mode, we can either use the actual Razorpay test API or simulate a response
            if self.test_mode and self.key_id.startswith("rzp_test_dummy"):
                # Simulate API response for testing
                payment_id = f"plink_qkd_{uuid.uuid4().hex[:16]}"
                response = {
                    'id': payment_id,
                    'entity': 'payment_link',
                    'amount': amount,
                    'currency': currency,
                    'description': data['description'],
                    'reference_id': reference_id,
                    'status': 'created',
                    'short_url': f"https://rzp.io/i/qkd_{uuid.uuid4().hex[:8]}",
                    'created_at': int(time.time())
                }
                logger.info(f"Simulated payment link created with ID: {payment_id}")
            else:
                # Make actual API call
                response = self.client.payment_link.create(data=data)
                logger.info(f"Payment link created with ID: {response['id']}")
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to create payment link: {str(e)}")
            raise
    
    def verify_payment_signature(self, payment_id, order_id, signature):
        """
        Verify that payment signature is valid
        
        Args:
            payment_id (str): ID of the payment
            order_id (str): ID of the order
            signature (str): Signature received from Razorpay
            
        Returns:
            bool: True if signature is valid, False otherwise
        """
        logger.info(f"Verifying payment signature for payment_id: {payment_id}, order_id: {order_id}")
        
        try:
            # Prepare data
            data = {
                'razorpay_payment_id': payment_id,
                'razorpay_order_id': order_id,
                'razorpay_signature': signature
            }
            
            # In test mode with dummy keys, always return True
            if self.test_mode and self.key_id.startswith("rzp_test_dummy"):
                logger.info("Test mode: Simulating successful signature verification")
                return True
                
            # Verify signature
            self.client.utility.verify_payment_signature(data)
            logger.info("Payment signature verification successful")
            return True
            
        except Exception as e:
            logger.error(f"Payment signature verification failed: {str(e)}")
            return False
    
    def get_payment_details(self, payment_id):
        """
        Get details of a payment
        
        Args:
            payment_id (str): ID of the payment
            
        Returns:
            dict: Payment details as returned by Razorpay
        """
        logger.info(f"Fetching payment details for payment_id: {payment_id}")
        
        try:
            # In test mode with dummy keys, simulate a response
            if self.test_mode and self.key_id.startswith("rzp_test_dummy"):
                # Simulate API response
                response = {
                    'id': payment_id,
                    'entity': 'payment',
                    'amount': 50000,
                    'currency': 'INR',
                    'status': 'captured',
                    'method': 'card',
                    'card_id': f"card_{uuid.uuid4().hex[:16]}",
                    'bank': 'HDFC',
                    'wallet': None,
                    'vpa': None,
                    'email': 'customer@example.com',
                    'contact': '+919999999999',
                    'created_at': int(time.time())
                }
                logger.info(f"Simulated payment details retrieved for payment_id: {payment_id}")
            else:
                # Make actual API call
                response = self.client.payment.fetch(payment_id)
                logger.info(f"Payment details retrieved for payment_id: {payment_id}")
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to fetch payment details: {str(e)}")
            raise
    
    def refund_payment(self, payment_id, amount=None):
        """
        Refund a payment
        
        Args:
            payment_id (str): ID of the payment to refund
            amount (int, optional): Amount to refund in smallest currency unit
                                   If None, the entire payment is refunded
            
        Returns:
            dict: Refund details as returned by Razorpay
        """
        logger.info(f"Initiating refund for payment_id: {payment_id}, amount: {amount or 'full'}")
        
        try:
            # Prepare data
            data = {}
            if amount:
                data['amount'] = amount
            
            # In test mode with dummy keys, simulate a response
            if self.test_mode and self.key_id.startswith("rzp_test_dummy"):
                # Simulate API response
                refund_id = f"rfnd_qkd_{uuid.uuid4().hex[:16]}"
                response = {
                    'id': refund_id,
                    'entity': 'refund',
                    'amount': amount or 50000,  # Use dummy amount if not specified
                    'payment_id': payment_id,
                    'status': 'processed',
                    'speed_processed': 'normal',
                    'created_at': int(time.time())
                }
                logger.info(f"Simulated refund initiated with ID: {refund_id}")
            else:
                # Make actual API call
                response = self.client.payment.refund(payment_id, data)
                logger.info(f"Refund initiated with ID: {response['id']}")
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to initiate refund: {str(e)}")
            raise
    
    def capture_payment(self, payment_id, amount, currency="INR"):
        """
        Capture an authorized payment
        
        Args:
            payment_id (str): ID of the payment to capture
            amount (int): Amount to capture in smallest currency unit
            currency (str): Currency code (default: INR)
            
        Returns:
            dict: Payment details as returned by Razorpay
        """
        logger.info(f"Capturing payment for payment_id: {payment_id}, amount: {amount} {currency}")
        
        try:
            # Prepare data
            data = {
                'amount': amount,
                'currency': currency
            }
            
            # In test mode with dummy keys, simulate a response
            if self.test_mode and self.key_id.startswith("rzp_test_dummy"):
                # Simulate API response
                response = {
                    'id': payment_id,
                    'entity': 'payment',
                    'amount': amount,
                    'currency': currency,
                    'status': 'captured',
                    'method': 'card',
                    'captured': True,
                    'created_at': int(time.time())
                }
                logger.info(f"Simulated payment capture successful for payment_id: {payment_id}")
            else:
                # Make actual API call
                response = self.client.payment.capture(payment_id, amount, {"currency": currency})
                logger.info(f"Payment capture successful for payment_id: {payment_id}")
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to capture payment: {str(e)}")
            raise

# Example usage
if __name__ == "__main__":
    # Initialize Razorpay integration in test mode
    razorpay_client = RazorpayIntegration(test_mode=True)
    
    # Create an order
    order = razorpay_client.create_order(
        amount=50000,  # ₹500.00
        currency="INR",
        notes={"purpose": "QKD Demo"}
    )
    print(f"Created order: {order}")
    
    # Create a payment link
    payment_link = razorpay_client.create_payment_link(
        amount=50000,
        description="Test payment for QKD-secured transaction",
        customer={
            "name": "John Doe",
            "email": "john@example.com",
            "contact": "+919999999999"
        }
    )
    print(f"Created payment link: {payment_link}")
    
    # Simulate a successful payment
    payment_id = f"pay_qkd_{uuid.uuid4().hex[:16]}"
    
    # Get payment details
    payment = razorpay_client.get_payment_details(payment_id)
    print(f"Payment details: {payment}")
    
    # Verify payment signature (simulate)
    signature_valid = razorpay_client.verify_payment_signature(
        payment_id=payment_id,
        order_id=order['id'],
        signature="dummy_signature"
    )
    print(f"Signature verification result: {signature_valid}")
    
    # Capture payment
    capture = razorpay_client.capture_payment(payment_id, 50000, "INR")
    print(f"Captured payment: {capture}")
    
    # Refund payment
    refund = razorpay_client.refund_payment(payment_id, 25000)  # Partial refund
    print(f"Refund initiated: {refund}")
