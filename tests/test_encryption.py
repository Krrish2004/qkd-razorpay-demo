#!/usr/bin/env python3
"""
Unit tests for the Encryption module
"""

import unittest
import os
import sys
import json

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from encryption import QuantumEncryption

class TestEncryptionModule(unittest.TestCase):
    """Test cases for Encryption Module"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create random key for testing
        self.test_key = os.urandom(32)
        self.encryption = QuantumEncryption(quantum_key=self.test_key)
        
        # Sample data for testing
        self.sample_dict = {
            "amount": 50000,
            "currency": "INR",
            "order_id": "order_test123",
            "customer": {
                "name": "Test User",
                "email": "test@example.com"
            }
        }
        
        self.sample_string = "This is a test string for encryption"
        self.sample_bytes = b"These are test bytes for encryption"
    
    def test_initialization(self):
        """Test encryption module initialization with key"""
        encryption = QuantumEncryption(quantum_key=self.test_key)
        self.assertEqual(encryption.key, self.test_key, "Key should be stored correctly")
        
        # Test initialization without key (should generate random key)
        encryption_no_key = QuantumEncryption()
        self.assertIsNotNone(encryption_no_key.key, "Key should be generated if not provided")
        self.assertEqual(len(encryption_no_key.key), 32, "Generated key should be 32 bytes")
    
    def test_key_derivation(self):
        """Test key derivation function"""
        salt = os.urandom(16)
        derived_key1 = self.encryption._derive_key(salt)
        derived_key2 = self.encryption._derive_key(salt)
        
        # Same salt should produce same derived key
        self.assertEqual(derived_key1, derived_key2, "Same salt should produce same derived key")
        
        # Different salts should produce different derived keys
        different_salt = os.urandom(16)
        derived_key3 = self.encryption._derive_key(different_salt)
        self.assertNotEqual(derived_key1, derived_key3, "Different salts should produce different derived keys")
    
    def test_encrypt_decrypt_dict(self):
        """Test encryption and decryption of dictionary data"""
        # Encrypt dictionary
        encrypted_data = self.encryption.encrypt_data(self.sample_dict)
        
        # Check encrypted data format
        self.assertIn('encrypted', encrypted_data, "Encrypted data should contain 'encrypted' field")
        self.assertIn('nonce', encrypted_data, "Encrypted data should contain 'nonce' field")
        self.assertIn('salt', encrypted_data, "Encrypted data should contain 'salt' field")
        
        # Decrypt dictionary
        decrypted_data = self.encryption.decrypt_data(encrypted_data, output_format='json')
        
        # Verify decryption correctness
        self.assertEqual(decrypted_data, self.sample_dict, "Decrypted data should match original")
    
    def test_encrypt_decrypt_string(self):
        """Test encryption and decryption of string data"""
        # Encrypt string
        encrypted_data = self.encryption.encrypt_data(self.sample_string)
        
        # Decrypt string
        decrypted_data = self.encryption.decrypt_data(encrypted_data, output_format='str')
        
        # Verify decryption correctness
        self.assertEqual(decrypted_data, self.sample_string, "Decrypted string should match original")
    
    def test_encrypt_decrypt_bytes(self):
        """Test encryption and decryption of bytes data"""
        # Encrypt bytes
        encrypted_data = self.encryption.encrypt_data(self.sample_bytes)
        
        # Decrypt bytes
        decrypted_data = self.encryption.decrypt_data(encrypted_data, output_format='bytes')
        
        # Verify decryption correctness
        self.assertEqual(decrypted_data, self.sample_bytes, "Decrypted bytes should match original")
    
    def test_additional_authenticated_data(self):
        """Test using additional authenticated data (AAD)"""
        aad = b"Additional authenticated data"
        
        # Encrypt with AAD
        encrypted_data = self.encryption.encrypt_data(self.sample_dict, additional_data=aad)
        
        # Check AAD is included in encrypted data
        self.assertIn('aad', encrypted_data, "Encrypted data should contain 'aad' field when AAD is provided")
        
        # Decrypt with matching AAD (should succeed)
        decrypted_data = self.encryption.decrypt_data(encrypted_data)
        self.assertEqual(decrypted_data, self.sample_dict, "Decryption with matching AAD should succeed")
        
        # Tamper with AAD
        tampered_data = encrypted_data.copy()
        tampered_data['aad'] = base64.b64encode(b"Tampered AAD").decode('utf-8')
        
        # Decryption should fail
        with self.assertRaises(Exception):
            self.encryption.decrypt_data(tampered_data)
    
    def test_tamper_resistance(self):
        """Test resistance to tampering with encrypted data"""
        # Encrypt data
        encrypted_data = self.encryption.encrypt_data(self.sample_dict)
        
        # Tamper with encrypted data
        tampered_data = encrypted_data.copy()
        ciphertext = base64.b64decode(encrypted_data['encrypted'])
        # Modify first byte of ciphertext
        tampered_ciphertext = bytes([ciphertext[0] ^ 0xFF]) + ciphertext[1:]
        tampered_data['encrypted'] = base64.b64encode(tampered_ciphertext).decode('utf-8')
        
        # Decryption should fail
        with self.assertRaises(Exception):
            self.encryption.decrypt_data(tampered_data)
    
    def test_performance_measurement(self):
        """Test performance measurement function"""
        metrics = QuantumEncryption.measure_encryption_performance(data_size=1024, iterations=5)
        
        # Check that metrics include expected fields
        expected_fields = [
            'data_size_bytes', 'iterations', 
            'avg_encryption_time_ms', 'avg_decryption_time_ms',
            'encryption_throughput_mbps', 'decryption_throughput_mbps'
        ]
        
        for field in expected_fields:
            self.assertIn(field, metrics, f"Performance metrics should include {field}")
            
        # Check that metrics have reasonable values
        self.assertEqual(metrics['data_size_bytes'], 1024, "Data size should match input")
        self.assertEqual(metrics['iterations'], 5, "Iterations should match input")
        self.assertGreater(metrics['avg_encryption_time_ms'], 0, "Encryption time should be positive")
        self.assertGreater(metrics['avg_decryption_time_ms'], 0, "Decryption time should be positive")

# Need to import these here to avoid issues with test import
import base64

if __name__ == '__main__':
    unittest.main()
