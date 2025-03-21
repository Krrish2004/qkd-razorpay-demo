#!/usr/bin/env python3
"""
Unit tests for QKD module
"""

import unittest
import os
import sys
import numpy as np

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qkd_module import QKDSimulator

class TestQKDModule(unittest.TestCase):
    """Test cases for QKD Module"""
    
    def test_qkd_initialization(self):
        """Test QKD simulator initialization"""
        qkd = QKDSimulator(n_bits=100, error_rate=0.05, eavesdropper=True)
        
        self.assertEqual(qkd.n_bits, 100, "Number of bits should be set to 100")
        self.assertEqual(qkd.error_rate, 0.05, "Error rate should be set to 0.05")
        self.assertTrue(qkd.eavesdropper, "Eavesdropper should be enabled")
        
    def test_key_generation_success(self):
        """Test successful key generation"""
        qkd = QKDSimulator(n_bits=500, error_rate=0.0, eavesdropper=False)
        success, key = qkd.generate_quantum_keys(key_length=16)
        
        self.assertTrue(success, "Key generation should succeed with no errors and no eavesdropper")
        self.assertIsNotNone(key, "Key should not be None")
        self.assertEqual(len(key), 16, "Key length should be 16 bytes")
        
    def test_key_generation_with_errors(self):
        """Test key generation with channel errors"""
        qkd = QKDSimulator(n_bits=500, error_rate=0.05, eavesdropper=False)
        success, key = qkd.generate_quantum_keys(key_length=16)
        
        self.assertTrue(success, "Key generation should succeed with moderate error rate")
        self.assertIsNotNone(key, "Key should not be None")
        
    def test_key_generation_with_eavesdropper(self):
        """Test key generation with an eavesdropper"""
        qkd = QKDSimulator(n_bits=500, error_rate=0.0, eavesdropper=True)
        # With eavesdropper, the error rate should be high enough to detect tampering
        # But in some cases, Eve might get lucky and introduce minimal errors
        # So we run the test multiple times
        failures = 0
        for _ in range(3):
            success, key = qkd.generate_quantum_keys(key_length=16)
            if not success:
                failures += 1
                
        # We expect at least one failure due to eavesdropper detection
        self.assertGreater(failures, 0, "Eavesdropper should be detected in at least one test")
        
    def test_key_bit_count(self):
        """Test that bit_count is properly tracked"""
        qkd = QKDSimulator(n_bits=500, error_rate=0.0, eavesdropper=False)
        success, key = qkd.generate_quantum_keys(key_length=16)
        
        self.assertGreater(qkd.bit_count, 0, "Bit count should be greater than 0")
        self.assertLessEqual(qkd.bit_count, 500, "Bit count should be less than or equal to n_bits")
        
    def test_bits_to_bytes_conversion(self):
        """Test bit array to bytes conversion"""
        qkd = QKDSimulator()
        
        # Test with a known bit pattern
        bits = [1, 0, 1, 0, 1, 0, 1, 0]  # 0xAA in binary
        bytes_result = qkd._bits_to_bytes(bits)
        self.assertEqual(bytes_result, b'\xaa', "Bit conversion should yield 0xAA")
        
        # Test with a bit pattern that requires padding
        bits = [1, 1, 1, 1]  # Should be padded to 0xF0
        bytes_result = qkd._bits_to_bytes(bits)
        self.assertEqual(bytes_result, b'\xf0', "Bit conversion with padding should yield 0xF0")
        
    def test_quantum_transmission(self):
        """Test the quantum transmission simulation"""
        qkd = QKDSimulator(n_bits=100, error_rate=0.0, eavesdropper=False)
        
        # Set up Alice's bits and bases
        qkd.alice_bits = np.random.randint(0, 2, qkd.n_bits)
        qkd.alice_bases = np.random.randint(0, 2, qkd.n_bits)
        qkd.bob_bases = qkd.alice_bases.copy()  # Same bases for perfect correlation
        
        # Perform quantum transmission
        qkd.bob_results = qkd._simulate_quantum_transmission()
        
        # With same bases and no noise, results should match
        matching_bits = sum(qkd.alice_bits[i] == qkd.bob_results[i] for i in range(qkd.n_bits))
        self.assertEqual(matching_bits, qkd.n_bits, 
                         "With same bases and no noise, all bits should match")
        
    def test_visualization(self):
        """Test the visualization function"""
        qkd = QKDSimulator(n_bits=40)
        success, _ = qkd.generate_quantum_keys()
        
        # Visualization should return a matplotlib figure
        figure = qkd.visualize_protocol()
        self.assertIsNotNone(figure, "Visualization should return a figure object")

if __name__ == '__main__':
    unittest.main()
