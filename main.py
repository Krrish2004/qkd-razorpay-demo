#!/usr/bin/env python3
"""
Main Module - Demonstrates complete flow of QKD-secured Razorpay transactions
"""

import os
import time
import json
import logging
import argparse
from datetime import datetime

# Import project modules
from qkd_module import QKDSimulator
from encryption import QuantumEncryption
from razorpay_api import RazorpayIntegration
from fraud_detection import FraudDetectionAI

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Main')

def initialize_dotenv():
    """Create a .env file with placeholder Razorpay credentials if not exists"""
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write("# Razorpay API Keys (Replace with your actual test keys)\n")
            f.write("RAZORPAY_KEY_ID=rzp_test_dummy_key_id\n")
            f.write("RAZORPAY_KEY_SECRET=rzp_test_dummy_key_secret\n")
        logger.info("Created .env file with placeholder Razorpay credentials")

def simulate_transaction(n_bits=1000, error_rate=0.01, eavesdropper=False, amount=50000, 
                        visualize=True, test_mode=True, fraud_model="heuristic", fraud_sensitivity=0.7):
    """
    Demonstrate a complete QKD-secured Razorpay transaction flow
    
    Args:
        n_bits (int): Number of qubits to exchange in QKD
        error_rate (float): Simulated quantum channel error rate
        eavesdropper (bool): Whether to simulate an eavesdropper in the quantum channel
        amount (int): Transaction amount in smallest currency unit (paise for INR)
        visualize (bool): Whether to generate visualization of the QKD protocol
        test_mode (bool): Whether to use test mode for Razorpay
        fraud_model (str): Type of fraud detection model ('heuristic', 'ml', 'quantum')
        fraud_sensitivity (float): Sensitivity for fraud detection (0.0-1.0)
        
    Returns:
        bool: True if transaction completed successfully, False otherwise
    """
    # Header
    logger.info("=" * 80)
    logger.info("QUANTUM KEY DISTRIBUTION (QKD) SECURED RAZORPAY TRANSACTION DEMO")
    logger.info("=" * 80)
    
    # Step 1: Generate quantum-secured keys using BB84 protocol
    logger.info("\n\nSTEP 1: QUANTUM KEY DISTRIBUTION")
    logger.info("-" * 50)
    
    start_time = time.time()
    qkd = QKDSimulator(n_bits=n_bits, error_rate=error_rate, eavesdropper=eavesdropper)
    success, quantum_key = qkd.generate_quantum_keys(key_length=32)  # 256-bit key
    qkd_time = time.time() - start_time
    
    if not success:
        if qkd.eavesdropper:
            logger.error("CRITICAL SECURITY ALERT: QKD key generation failed with eavesdropper present!")
            logger.error("Possible quantum channel tampering detected. Transaction ABORTED for security reasons.")
            # Print a more visible security warning
            print("\n" + "!" * 80)
            print("!! SECURITY BREACH DETECTED: Quantum channel compromised by eavesdropper !!")
            print("!! All transactions have been blocked as a security precaution        !!")
            print("!" * 80 + "\n")
        else:
            logger.error("QKD key generation failed due to technical issues. Aborting transaction.")
        return False
    
    logger.info(f"Generated quantum-secured key: {quantum_key.hex()}")
    logger.info(f"QKD completed in {qkd_time:.2f} seconds")
    
    # Visualize QKD process if requested
    if visualize:
        logger.info("Generating QKD visualization...")
        qkd.visualize_protocol()
    
    # Step 2: Initialize encryption with quantum key
    logger.info("\n\nSTEP 2: ENCRYPTION INITIALIZATION")
    logger.info("-" * 50)
    
    encryption = QuantumEncryption(quantum_key=quantum_key)
    logger.info("Encryption module initialized with quantum-generated key")
    
    # Step 3: Create payment data
    logger.info("\n\nSTEP 3: PREPARE PAYMENT DATA")
    logger.info("-" * 50)
    
    # Sample payment data (in real app, this would come from user input)
    payment_data = {
        "amount": amount,
        "currency": "INR",
        "customer": {
            "name": "Jane Smith",
            "email": "jane@example.com",
            "contact": "+919876543210"
        },
        "payment_capture": True,
        "notes": {
            "purpose": "QKD-secured transaction demo",
            "timestamp": datetime.now().isoformat()
        }
    }
    
    logger.info(f"Prepared payment data: {json.dumps(payment_data, indent=2)}")
    
    # Step 4: Encrypt the payment data using quantum key
    logger.info("\n\nSTEP 4: ENCRYPT PAYMENT DATA")
    logger.info("-" * 50)
    
    start_time = time.time()
    encrypted_data = encryption.encrypt_data(payment_data)
    encryption_time = time.time() - start_time
    
    logger.info(f"Payment data encrypted successfully in {encryption_time*1000:.2f} ms")
    logger.info(f"Encrypted data size: {len(json.dumps(encrypted_data))} bytes")
    
    # Step 5: Initialize Razorpay client and create order
    logger.info("\n\nSTEP 5: RAZORPAY INTEGRATION")
    logger.info("-" * 50)
    
    razorpay_client = RazorpayIntegration(test_mode=test_mode)
    
    start_time = time.time()
    order = razorpay_client.create_order(
        amount=payment_data["amount"],
        currency=payment_data["currency"],
        notes=payment_data["notes"]
    )
    api_time = time.time() - start_time
    
    logger.info(f"Created Razorpay order with ID: {order['id']}")
    logger.info(f"API call completed in {api_time*1000:.2f} ms")
    
    # Step 6: Create a payment link
    payment_link = razorpay_client.create_payment_link(
        amount=payment_data["amount"],
        currency=payment_data["currency"],
        description="QKD-secured payment transaction",
        customer=payment_data["customer"]
    )
    
    logger.info(f"Created payment link: {payment_link.get('short_url', 'N/A')}")
    
    # Step 7: Simulate payment completion (in a real app, user would complete payment)
    logger.info("\n\nSTEP 7: SIMULATE PAYMENT COMPLETION")
    logger.info("-" * 50)
    
    # In a real app, we would wait for webhook or user to return after payment
    logger.info("Simulating payment completion by customer...")
    time.sleep(2)  # Simulate payment processing time
    
    # Generate a simulated payment ID (in real app, this would come from Razorpay)
    payment_id = f"pay_qkd_{order['id'][6:]}"
    
    # New Step: Fraud Detection Analysis
    logger.info("\n\nSTEP 8: FRAUD DETECTION ANALYSIS")
    logger.info("-" * 50)
    
    # Initialize fraud detection system
    fraud_detector = FraudDetectionAI(model_type=fraud_model, sensitivity=fraud_sensitivity)
    logger.info(f"Performing fraud detection using {fraud_model} model with {fraud_sensitivity} sensitivity")
    
    # Get payment details
    payment_details = razorpay_client.get_payment_details(payment_id)
    
    # Collect device and user info (in a real app, these would be actual values)
    device_info = {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "ip_address": "192.168.1.1",
        "browser": "Chrome",
        "device_type": "desktop"
    }
    
    user_info = {
        "account_age_days": 120,
        "num_previous_transactions": 5,
        "last_transaction_days": 14
    }
    
    # Prepare transaction data for fraud analysis
    transaction_data = {
        "id": payment_id,
        "amount": payment_data["amount"],
        "currency": payment_data["currency"],
        "payment_method": "card",
        "timestamp": datetime.now().isoformat(),
        "customer": payment_data["customer"],
        "order_id": order['id']
    }
    
    # Perform fraud detection
    start_time = time.time()
    fraud_result = fraud_detector.analyze_transaction(
        payment_data=transaction_data,
        user_data=user_info,
        device_info=device_info
    )
    fraud_detection_time = time.time() - start_time
    
    # Log fraud detection results
    logger.info(f"Fraud detection completed in {fraud_detection_time*1000:.2f} ms")
    logger.info(f"Risk score: {fraud_result['risk_score']:.3f} (threshold: {fraud_result['threshold']:.3f})")
    if fraud_result["risk_factors"]:
        logger.info(f"Risk factors identified: {', '.join(fraud_result['risk_factors'])}")
    
    # Check if transaction is flagged as fraudulent
    if fraud_result["is_fraudulent"]:
        logger.error(f"TRANSACTION BLOCKED: Potential fraud detected with {fraud_result['confidence']:.1%} confidence")
        logger.error(f"Risk factors: {', '.join(fraud_result['risk_factors'])}")
        return False
    else:
        logger.info(f"Transaction passed fraud checks with {fraud_result['confidence']:.1%} confidence")
    
    # Step 9: Payment Verification and Decryption (previously Step 8)
    logger.info("\n\nSTEP 9: PAYMENT VERIFICATION AND DECRYPTION")
    logger.info("-" * 50)
    
    # Verify payment signature (simulated)
    signature_valid = razorpay_client.verify_payment_signature(
        payment_id=payment_id,
        order_id=order['id'],
        signature="dummy_signature_for_demo"
    )
    
    if not signature_valid:
        logger.error("Payment signature verification failed. Possible tampering detected.")
        return False
    
    logger.info("Payment signature verification successful")
    
    # Decrypt the original payment data to confirm integrity
    start_time = time.time()
    decrypted_data = encryption.decrypt_data(encrypted_data)
    decryption_time = time.time() - start_time
    
    logger.info(f"Decryption completed in {decryption_time*1000:.2f} ms")
    
    # Verify decrypted data matches original data
    data_valid = decrypted_data == payment_data
    logger.info(f"Decrypted data validation: {'Successful' if data_valid else 'Failed'}")
    
    if not data_valid:
        logger.error("Decrypted data does not match original data. Possible tampering.")
        return False
    
    # Step 10: Transaction summary
    logger.info("\n\nTRANSACTION SUMMARY")
    logger.info("=" * 50)
    logger.info(f"Order ID: {order['id']}")
    logger.info(f"Payment ID: {payment_id}")
    logger.info(f"Amount: {payment_details['amount']/100} {payment_details['currency']}")
    logger.info(f"Status: {payment_details['status']}")
    logger.info(f"QKD Bits Used: {qkd.bit_count}")
    logger.info(f"QKD Time: {qkd_time:.2f} seconds")
    logger.info(f"Encryption Time: {encryption_time*1000:.2f} ms")
    logger.info(f"Decryption Time: {decryption_time*1000:.2f} ms")
    logger.info(f"API Call Time: {api_time*1000:.2f} ms")
    logger.info(f"Fraud Detection Time: {fraud_detection_time*1000:.2f} ms")
    logger.info(f"Fraud Risk Score: {fraud_result['risk_score']:.3f}")
    logger.info(f"Fraud Model: {fraud_model}")
    logger.info(f"Total Transaction Time: {time.time() - (start_time - encryption_time - api_time):.2f} seconds")
    logger.info(f"Transaction successful: {signature_valid and data_valid}")
    
    # Step 11: Performance comparison
    logger.info("\n\nPERFORMANCE ANALYSIS")
    logger.info("-" * 50)
    
    # Measure standard encryption performance for comparison
    standard_metrics = QuantumEncryption.measure_encryption_performance(
        data_size=len(json.dumps(payment_data).encode()),
        iterations=10
    )
    
    logger.info("Performance Comparison:")
    logger.info(f"  Quantum Key Generation: {qkd_time:.2f} seconds for {n_bits} qubits")
    logger.info(f"  QKD-based Encryption: {encryption_time*1000:.2f} ms")
    logger.info(f"  QKD-based Decryption: {decryption_time*1000:.2f} ms")
    logger.info(f"  Standard Encryption: {standard_metrics['avg_encryption_time_ms']:.2f} ms")
    logger.info(f"  Standard Decryption: {standard_metrics['avg_decryption_time_ms']:.2f} ms")
    
    logger.info("\nOverhead of QKD-based approach:")
    enc_overhead = (encryption_time*1000 / standard_metrics['avg_encryption_time_ms'] - 1) * 100
    dec_overhead = (decryption_time*1000 / standard_metrics['avg_decryption_time_ms'] - 1) * 100
    logger.info(f"  Encryption: {enc_overhead:.2f}% slower")
    logger.info(f"  Decryption: {dec_overhead:.2f}% slower")
    logger.info(f"  One-time QKD Setup: {qkd_time:.2f} seconds")
    
    # Final success message
    logger.info("\n\n" + "=" * 80)
    logger.info("QKD-SECURED TRANSACTION COMPLETED SUCCESSFULLY")
    logger.info("=" * 80)
    
    return True

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='QKD-Secured Razorpay Transaction Demo')
    parser.add_argument('--qubits', type=int, default=1000, help='Number of qubits for QKD (default: 1000)')
    parser.add_argument('--error-rate', type=float, default=0.01, help='Simulated quantum channel error rate (default: 0.01)')
    parser.add_argument('--eavesdropper', action='store_true', help='Simulate an eavesdropper in the quantum channel')
    parser.add_argument('--amount', type=int, default=50000, help='Transaction amount in paise (default: 50000 = ₹500.00)')
    parser.add_argument('--no-visualize', action='store_true', help='Skip QKD visualization')
    parser.add_argument('--production', action='store_true', help='Use production mode for Razorpay (NOT RECOMMENDED)')
    parser.add_argument('--fraud-model', type=str, choices=['heuristic', 'ml', 'quantum'], default='heuristic', 
                        help='Type of fraud detection model to use (default: heuristic)')
    parser.add_argument('--fraud-sensitivity', type=float, default=0.7, 
                        help='Sensitivity level for fraud detection (0.0-1.0, default: 0.7)')
    return parser.parse_args()

if __name__ == "__main__":
    # Ensure .env file exists
    initialize_dotenv()
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Run transaction demo
    simulate_transaction(
        n_bits=args.qubits,
        error_rate=args.error_rate,
        eavesdropper=args.eavesdropper,
        amount=args.amount,
        visualize=not args.no_visualize,
        test_mode=not args.production,
        fraud_model=args.fraud_model,
        fraud_sensitivity=args.fraud_sensitivity
    )
