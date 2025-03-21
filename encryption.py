#!/usr/bin/env python3
"""
Encryption Module - Handles encryption and decryption of data using quantum-generated keys
"""

import os
import json
import base64
import logging
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Encryption Module')

class QuantumEncryption:
    """
    Provides encryption and decryption functionality using AES-GCM with quantum-generated keys
    """
    
    def __init__(self, quantum_key=None):
        """
        Initialize the encryption module
        
        Args:
            quantum_key (bytes, optional): Quantum-generated key to use for encryption/decryption
                                          If None, a random key will be generated (for testing only)
        """
        if quantum_key is None:
            # For testing only - in real usage, always provide a quantum-generated key
            self.key = os.urandom(32)
            logger.warning("Using randomly generated key instead of quantum key")
        else:
            self.key = quantum_key
            logger.info("Initialized encryption with quantum-generated key")
    
    def _derive_key(self, salt, info=b"QKD-Razorpay-Demo"):
        """
        Derive a key from the quantum key using PBKDF2
        
        Args:
            salt (bytes): Salt for key derivation
            info (bytes): Application info string
            
        Returns:
            bytes: Derived key
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # 256-bit key
            salt=salt,
            iterations=100000,
        )
        return kdf.derive(self.key + info)
    
    def encrypt_data(self, data, additional_data=None):
        """
        Encrypt data using AES-GCM with the quantum-generated key
        
        Args:
            data (dict or str): Data to encrypt (will be JSON-encoded if dict)
            additional_data (bytes, optional): Additional authenticated data
            
        Returns:
            dict: Dictionary containing the encrypted data, nonce, and salt
                  Format: {'encrypted': base64 encoded encrypted data,
                           'nonce': base64 encoded nonce,
                           'salt': base64 encoded salt,
                           'aad': base64 encoded additional data (if provided)}
        """
        # Convert data to bytes if it's a dictionary or string
        if isinstance(data, dict):
            plaintext = json.dumps(data).encode('utf-8')
        elif isinstance(data, str):
            plaintext = data.encode('utf-8')
        else:
            plaintext = data
            
        # Log data size for performance analysis
        logger.info(f"Encrypting {len(plaintext)} bytes of data")
        
        # Generate random salt and nonce
        salt = os.urandom(16)
        nonce = os.urandom(12)  # 96 bits as recommended for AES-GCM
        
        # Derive encryption key using PBKDF2
        encryption_key = self._derive_key(salt)
        
        # Initialize AESGCM with the key
        aesgcm = AESGCM(encryption_key)
        
        # Prepare additional authenticated data
        aad = additional_data if additional_data else b""
        
        # Encrypt the data
        try:
            ciphertext = aesgcm.encrypt(nonce, plaintext, aad)
            logger.info(f"Successfully encrypted data (output size: {len(ciphertext)} bytes)")
            
            # Prepare result dictionary
            result = {
                'encrypted': base64.b64encode(ciphertext).decode('utf-8'),
                'nonce': base64.b64encode(nonce).decode('utf-8'),
                'salt': base64.b64encode(salt).decode('utf-8')
            }
            
            if additional_data:
                result['aad'] = base64.b64encode(aad).decode('utf-8')
                
            return result
            
        except Exception as e:
            logger.error(f"Encryption failed: {str(e)}")
            raise
    
    def decrypt_data(self, encrypted_data, output_format='json'):
        """
        Decrypt data using AES-GCM with the quantum-generated key
        
        Args:
            encrypted_data (dict): Dictionary containing encrypted data, nonce, and salt
                                  Format: {'encrypted': base64 encoded encrypted data,
                                           'nonce': base64 encoded nonce, 
                                           'salt': base64 encoded salt,
                                           'aad': base64 encoded additional data (optional)}
            output_format (str): Format of the output data ('json', 'str', or 'bytes')
            
        Returns:
            The decrypted data in the specified format
        """
        # Extract and decode components
        try:
            ciphertext = base64.b64decode(encrypted_data['encrypted'])
            nonce = base64.b64decode(encrypted_data['nonce'])
            salt = base64.b64decode(encrypted_data['salt'])
            aad = base64.b64decode(encrypted_data.get('aad', '')) or b""
            
            logger.info(f"Decrypting {len(ciphertext)} bytes of data")
            
            # Derive encryption key using PBKDF2
            encryption_key = self._derive_key(salt)
            
            # Initialize AESGCM with the key
            aesgcm = AESGCM(encryption_key)
            
            # Decrypt the data
            plaintext = aesgcm.decrypt(nonce, ciphertext, aad)
            logger.info(f"Successfully decrypted data (output size: {len(plaintext)} bytes)")
            
            # Return in the requested format
            if output_format == 'json':
                return json.loads(plaintext.decode('utf-8'))
            elif output_format == 'str':
                return plaintext.decode('utf-8')
            else:  # bytes
                return plaintext
                
        except Exception as e:
            logger.error(f"Decryption failed: {str(e)}")
            raise
    
    @staticmethod
    def measure_encryption_performance(data_size=1024, iterations=10):
        """
        Measure encryption/decryption performance
        
        Args:
            data_size (int): Size of test data in bytes
            iterations (int): Number of encryption/decryption cycles to perform
            
        Returns:
            dict: Dictionary with performance metrics
        """
        import time
        
        # Create random test data
        test_data = os.urandom(data_size)
        
        # Initialize with random key (for testing only)
        enc = QuantumEncryption()
        
        # Measure encryption time
        enc_times = []
        for _ in range(iterations):
            start = time.time()
            encrypted = enc.encrypt_data(test_data)
            enc_times.append(time.time() - start)
        
        # Measure decryption time
        dec_times = []
        for _ in range(iterations):
            start = time.time()
            dec = enc.decrypt_data(encrypted, output_format='bytes')
            dec_times.append(time.time() - start)
        
        # Verify decryption is correct
        assert dec == test_data, "Decryption produced incorrect result"
        
        # Calculate metrics
        avg_enc_time = sum(enc_times) / iterations
        avg_dec_time = sum(dec_times) / iterations
        
        metrics = {
            'data_size_bytes': data_size,
            'iterations': iterations,
            'avg_encryption_time_ms': avg_enc_time * 1000,
            'avg_decryption_time_ms': avg_dec_time * 1000,
            'encryption_throughput_mbps': (data_size / 1024 / 1024) / avg_enc_time,
            'decryption_throughput_mbps': (data_size / 1024 / 1024) / avg_dec_time
        }
        
        return metrics

# Example usage
if __name__ == "__main__":
    # Example data to encrypt
    payment_data = {
        "amount": 50000,
        "currency": "INR",
        "order_id": "order_DBJOWzybf0sJbb",
        "customer_id": "cust_DAtJtPiGBQDXTk",
        "payment_method": "card",
        "card": {
            "number": "4111111111111111",
            "expiry_month": "12",
            "expiry_year": "2023",
            "cvv": "123"
        }
    }
    
    # Create encryption instance with random key (for testing)
    encryption = QuantumEncryption()
    
    # Encrypt the payment data
    encrypted_data = encryption.encrypt_data(payment_data)
    print(f"Encrypted payment data: {encrypted_data}")
    
    # Decrypt the payment data
    decrypted_data = encryption.decrypt_data(encrypted_data)
    print(f"Decrypted payment data: {decrypted_data}")
    
    # Verify data is preserved
    assert decrypted_data == payment_data, "Decryption produced incorrect result"
    
    # Measure performance
    performance = QuantumEncryption.measure_encryption_performance()
    print(f"Performance metrics: {performance}")
