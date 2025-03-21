#!/usr/bin/env python3
"""
Flask Application for QKD-Razorpay Demo
"""

import os
import time
import json
import uuid
import logging
import threading
from datetime import datetime
from flask import Flask, jsonify, request, render_template, send_file, abort, send_from_directory
from flask_cors import CORS

# Import QKD modules
from qkd_module import QKDSimulator
from encryption import QuantumEncryption
from razorpay_api import RazorpayIntegration
from fraud_detection import FraudDetectionAI
from main import initialize_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('App')

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Ensure static directories exist
os.makedirs('static', exist_ok=True)
os.makedirs('templates', exist_ok=True)

# Ensure .env file exists
initialize_dotenv()

# Store active simulations
simulations = {}

def update_simulation(simulation_id, status, step, progress, **kwargs):
    """Update the simulation status with current progress"""
    if simulation_id in simulations:
        simulations[simulation_id].update({
            'status': status,
            'current_step': step,
            'progress': progress,
            'updated_at': datetime.now().isoformat(),
            **kwargs
        })
        
        # Add step to timeline if it's a new step
        if 'steps' not in simulations[simulation_id]:
            simulations[simulation_id]['steps'] = []
        
        simulations[simulation_id]['steps'].append({
            'name': step,
            'progress': progress,
            'timestamp': datetime.now().isoformat()
        })
        
        logger.info(f"Simulation {simulation_id}: {step} - {progress}%")

def run_simulation(simulation_id, config):
    """
    Run a complete QKD-secured Razorpay transaction simulation
    This function runs in a separate thread to not block the web server
    """
    try:
        # Initialize simulation object if not exists
        if simulation_id not in simulations:
            simulations[simulation_id] = {
                'id': simulation_id,
                'status': 'initializing',
                'current_step': 'Initializing simulation',
                'progress': 0,
                'started_at': datetime.now().isoformat(),
                'config': config,
                'steps': []
            }
        
        # Step 1: Generate quantum-secured keys using BB84 protocol
        update_simulation(
            simulation_id, 'running', 
            'Initializing QKD simulator', 10,
            current_step_index=1  # For UI step tracking
        )
        
        # Create QKD simulator
        n_bits = config.get('qubits', 1000)
        error_rate = config.get('error_rate', 0.01)
        eavesdropper = config.get('eavesdropper', False)
        
        start_time = time.time()
        qkd = QKDSimulator(n_bits=n_bits, error_rate=error_rate, eavesdropper=eavesdropper)
        
        # Generate keys
        update_simulation(
            simulation_id, 'running', 
            'Running quantum key distribution protocol', 15,
            current_step_index=1
        )
        
        success, quantum_key = qkd.generate_quantum_keys(key_length=32)  # 256-bit key
        qkd_time = time.time() - start_time
        
        if not success:
            update_simulation(
                simulation_id, 'failed', 
                'QKD key generation failed', 20,
                error="Could not generate secure key. Too many errors or possible eavesdropper detected."
            )
            return
        
        # Generate visualization
        update_simulation(
            simulation_id, 'running', 
            'Generating QKD visualization', 25,
            current_step_index=1
        )
        
        viz_file = f"static/qkd_viz_{simulation_id}.png"
        qkd.visualize_protocol(output_file=viz_file)
        
        # Store QKD results
        base_match_rate = len(qkd.matched_bases_idx) / qkd.n_bits if hasattr(qkd, 'matched_bases_idx') else 0
        update_simulation(
            simulation_id, 'running', 
            'QKD completed, preparing encryption', 30,
            quantum_key=quantum_key.hex(),
            qkd_time=qkd_time,
            bit_count=qkd.bit_count,
            base_match_rate=base_match_rate,
            visualization_url=f"/{viz_file}",
            current_step_index=2  # Move to encryption step
        )
        
        # Step 2: Initialize encryption with quantum key
        encryption = QuantumEncryption(quantum_key=quantum_key)
        
        # Step 3: Create payment data
        update_simulation(
            simulation_id, 'running', 
            'Preparing payment data', 40,
            current_step_index=2
        )
        
        # Get amount from config (in paise)
        amount = config.get('amount', 50000)
        
        # Sample payment data
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
                "timestamp": datetime.now().isoformat(),
                "simulation_id": simulation_id
            }
        }
        
        # Step 4: Encrypt the payment data using quantum key
        update_simulation(
            simulation_id, 'running', 
            'Encrypting payment data with quantum key', 50,
            current_step_index=2
        )
        
        start_time = time.time()
        encrypted_data = encryption.encrypt_data(payment_data)
        encryption_time = time.time() - start_time
        
        # Step 5: Initialize Razorpay client and create order
        update_simulation(
            simulation_id, 'running', 
            'Creating Razorpay order', 60,
            current_step_index=3  # Move to Razorpay step
        )
        
        razorpay_client = RazorpayIntegration(test_mode=True)
        
        start_time = time.time()
        order = razorpay_client.create_order(
            amount=payment_data["amount"],
            currency=payment_data["currency"],
            notes=payment_data["notes"]
        )
        api_time = time.time() - start_time
        
        # Step 6: Create a payment link
        update_simulation(
            simulation_id, 'running', 
            'Creating payment link', 70,
            order_id=order['id'],
            current_step_index=3
        )
        
        payment_link = razorpay_client.create_payment_link(
            amount=payment_data["amount"],
            currency=payment_data["currency"],
            description="QKD-secured payment transaction",
            customer=payment_data["customer"]
        )
        
        # Step 7: Simulate payment completion
        update_simulation(
            simulation_id, 'running', 
            'Simulating payment completion', 75,
            current_step_index=3
        )
        
        # In a real app, we would wait for webhook or user to return after payment
        time.sleep(1)  # Simulate payment processing time
        
        # Generate a simulated payment ID
        payment_id = f"pay_qkd_{order['id'][6:]}"
        
        # New Step 8: Fraud Detection Analysis
        update_simulation(
            simulation_id, 'running', 
            'Analyzing transaction for fraud patterns', 80,
            current_step_index=4  # Move to fraud detection step
        )
        
        # Get fraud detection settings
        fraud_model = config.get('fraud_model', 'heuristic')
        fraud_sensitivity = float(config.get('fraud_sensitivity', 0.7))
        
        # Initialize fraud detection
        fraud_detector = FraudDetectionAI(model_type=fraud_model, sensitivity=fraud_sensitivity)
        
        # Get payment details
        payment_details = razorpay_client.get_payment_details(payment_id)
        
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
        
        # Simulate device and user data
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
        
        # Perform fraud detection
        start_time = time.time()
        fraud_result = fraud_detector.analyze_transaction(
            payment_data=transaction_data,
            user_data=user_info,
            device_info=device_info
        )
        fraud_detection_time = time.time() - start_time
        
        # Store fraud detection results
        fraud_detection_results = {
            "model_type": fraud_model,
            "risk_score": fraud_result["risk_score"],
            "threshold": fraud_result["threshold"],
            "is_fraudulent": fraud_result["is_fraudulent"],
            "confidence": fraud_result["confidence"],
            "risk_factors": fraud_result["risk_factors"],
            "analysis_time": fraud_detection_time * 1000  # Convert to ms
        }
        
        # Check if transaction is fraudulent
        if fraud_result["is_fraudulent"]:
            update_simulation(
                simulation_id, 'failed', 
                'Transaction blocked: Potential fraud detected', 85,
                payment_id=payment_id,
                transaction_results={
                    "status": "Failed - Fraud Detected",
                    "order_id": order['id'],
                    "payment_id": payment_id,
                    "amount": payment_data["amount"],
                    "currency": payment_data["currency"],
                    "fraud_detection": fraud_detection_results
                },
                error=f"Potential fraud detected with {fraud_result['confidence']:.1%} confidence: {', '.join(fraud_result['risk_factors'])}"
            )
            return
        
        # Step 9: Verify payment and decrypt data
        update_simulation(
            simulation_id, 'running', 
            'Verifying payment and decrypting data', 90,
            payment_id=payment_id,
            current_step_index=5  # Move to verification step
        )
        
        # Verify payment signature (simulated)
        signature_valid = razorpay_client.verify_payment_signature(
            payment_id=payment_id,
            order_id=order['id'],
            signature="dummy_signature_for_demo"
        )
        
        if not signature_valid:
            update_simulation(
                simulation_id, 'failed', 
                'Payment signature verification failed', 95,
                error="Payment signature verification failed. Possible tampering detected."
            )
            return
        
        # Decrypt the original payment data
        start_time = time.time()
        decrypted_data = encryption.decrypt_data(encrypted_data)
        decryption_time = time.time() - start_time
        
        # Verify decrypted data matches original data
        data_valid = decrypted_data == payment_data
        
        if not data_valid:
            update_simulation(
                simulation_id, 'failed', 
                'Decrypted data validation failed', 95,
                error="Decrypted data does not match original data. Possible tampering."
            )
            return
        
        # Measure standard encryption performance for comparison
        standard_metrics = QuantumEncryption.measure_encryption_performance(
            data_size=len(json.dumps(payment_data).encode()),
            iterations=10
        )
        
        # Calculate overhead
        enc_overhead = (encryption_time*1000 / standard_metrics['avg_encryption_time_ms'] - 1) * 100
        dec_overhead = (decryption_time*1000 / standard_metrics['avg_decryption_time_ms'] - 1) * 100
        
        # Prepare transaction results
        transaction_results = {
            "status": "Success",
            "order_id": order['id'],
            "payment_id": payment_id,
            "amount": payment_data["amount"],
            "currency": payment_data["currency"],
            "total_time": time.time() - float(datetime.fromisoformat(simulations[simulation_id]['started_at']).timestamp()),
            "encryption_time": encryption_time * 1000,  # Convert to ms
            "decryption_time": decryption_time * 1000,  # Convert to ms
            "standard_encryption_time": standard_metrics['avg_encryption_time_ms'],
            "standard_decryption_time": standard_metrics['avg_decryption_time_ms'],
            "overhead": (enc_overhead + dec_overhead) / 2,  # Average overhead
            "fraud_detection": fraud_detection_results
        }
        
        # Create metrics for the UI
        qkd_metrics = {
            "key": quantum_key.hex(),
            "time": qkd_time,
            "bits_used": qkd.bit_count,
            "match_rate": base_match_rate
        }
        
        # Mark simulation as completed
        update_simulation(
            simulation_id, 'completed', 
            'Transaction completed successfully', 100,
            completion_time=datetime.now().isoformat(),
            transaction_results=transaction_results,
            qkd_metrics=qkd_metrics,
            current_step_index=6  # For UI completion
        )
        
        logger.info(f"Simulation {simulation_id} completed successfully")
        
    except Exception as e:
        logger.error(f"Simulation {simulation_id} failed with error: {str(e)}")
        update_simulation(
            simulation_id, 'failed', 
            'Simulation failed due to error', 0,
            error=str(e)
        )

# API Routes
@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/start_simulation', methods=['POST'])
def start_simulation():
    """Start a new QKD-secured transaction simulation"""
    try:
        # Get configuration from request
        config = request.json
        
        # Validate config
        if not config:
            return jsonify({'error': 'No configuration provided'}), 400
        
        # Generate unique simulation ID
        simulation_id = str(uuid.uuid4())
        
        # Initialize simulation status
        simulations[simulation_id] = {
            'id': simulation_id,
            'status': 'initializing',
            'current_step': 'Initializing simulation',
            'progress': 0,
            'started_at': datetime.now().isoformat(),
            'config': config
        }
        
        # Start simulation in background thread
        thread = threading.Thread(target=run_simulation, args=(simulation_id, config))
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'simulation_id': simulation_id,
            'status': 'initializing'
        })
        
    except Exception as e:
        logger.error(f"Error starting simulation: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/simulation/<simulation_id>', methods=['GET'])
def get_simulation(simulation_id):
    """Get the status of a simulation"""
    if simulation_id not in simulations:
        return jsonify({'error': 'Simulation not found'}), 404
    
    return jsonify(simulations[simulation_id])

@app.route('/api/simulations', methods=['GET'])
def get_simulations():
    """Get a list of all simulations"""
    simulation_list = list(simulations.values())
    
    # Sort by start time
    simulation_list.sort(key=lambda x: x.get('started_at', ''), reverse=True)
    
    return jsonify(simulation_list)

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

@app.route('/api/visualization/<simulation_id>', methods=['GET'])
def get_visualization(simulation_id):
    """Get the QKD visualization for a simulation"""
    if simulation_id not in simulations:
        return jsonify({'error': 'Simulation not found'}), 404
    
    # Check if visualization exists
    viz_path = f"static/qkd_viz_{simulation_id}.png"
    if not os.path.exists(viz_path):
        return jsonify({'error': 'Visualization not found'}), 404
    
    return jsonify({'visualization_url': f"/{viz_path}"})

if __name__ == '__main__':
    logger.info("Starting QKD-Razorpay Demo Web Application")
    app.run(debug=True, port=5000) 