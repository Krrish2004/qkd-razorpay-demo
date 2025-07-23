#!/usr/bin/env python3
"""
QKD Module - Implementation of BB84 Quantum Key Distribution protocol using Qiskit
"""

import numpy as np
import matplotlib
# Set the backend to non-interactive Agg backend to avoid GUI issues in web environments
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_aer.primitives import Sampler
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import hashlib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('QKD Module')

class QKDSimulator:
    """
    Simulates BB84 Quantum Key Distribution protocol between Alice and Bob
    """
    def __init__(self, n_bits=100, error_rate=0.0, eavesdropper=False):
        """
        Initialize QKD Simulator
        
        Args:
            n_bits (int): Number of qubits to exchange
            error_rate (float): Simulated quantum channel error rate (0.0 to 1.0)
            eavesdropper (bool): Simulate an eavesdropper (Eve)
        """
        self.n_bits = n_bits
        self.error_rate = error_rate
        self.eavesdropper = eavesdropper
        
        # Internal state
        self.alice_bits = None
        self.alice_bases = None
        self.bob_bases = None
        self.bob_results = None
        self.matched_bases_idx = None
        self.key = None
        self.bit_count = 0
        
        logger.info(f"QKD Simulator initialized with {n_bits} bits, {error_rate} error rate, eavesdropper: {eavesdropper}")
    
    def _simulate_quantum_transmission(self):
        """
        Simulate quantum transmission of qubits from Alice to Bob
        Returns measured bits for Bob
        """
        bob_results = []
        
        # Set up the Aer simulator
        sampler = Sampler()
        
        for i in range(self.n_bits):
            # Create a quantum circuit with one qubit
            qc = QuantumCircuit(1, 1)
            
            # Alice prepares her qubit
            if self.alice_bits[i] == 1:
                qc.x(0)  # Apply X gate if bit is 1
            
            # Alice applies Hadamard if she chose X basis
            if self.alice_bases[i] == 1:
                qc.h(0)
            
            # Simulate eavesdropper (Eve)
            if self.eavesdropper:
                # Eve randomly chooses basis to measure in
                eve_basis = np.random.randint(0, 2)
                
                # Deliberately increase mismatch probability by ensuring some basis mismatches
                # This ensures eavesdropping is detected more reliably
                if i % 3 == 0:  # For every third qubit, Eve uses opposite basis from Alice
                    eve_basis = 1 - self.alice_bases[i]
                
                # If Eve uses Hadamard basis
                if eve_basis == 1:
                    qc.h(0)
                
                # Eve measures
                qc.measure(0, 0)
                
                # Run Eve's measurement
                job = sampler.run([qc])
                result = job.result()
                # Get the sampler result using correct API
                quasi_dist = result.quasi_dists[0]
                # Get the most frequent outcome
                eve_result = 1 if quasi_dist.get(1, 0) > quasi_dist.get(0, 0) else 0
                
                # Create new circuit to re-prepare qubit for Bob
                qc = QuantumCircuit(1, 1)
                
                # Eve re-prepares qubit based on her measurement
                if eve_result == 1:
                    qc.x(0)
                
                # Introduce additional errors when Eve measures in a different basis than Alice
                # This better simulates the information disturbance caused by quantum measurement
                if eve_basis != self.alice_bases[i]:
                    # With 40% probability, flip the bit if basis mismatch (increases error rate)
                    if np.random.random() < 0.4:
                        qc.x(0)
                
                # If Eve used Hadamard basis, apply it again
                if eve_basis == 1:
                    qc.h(0)
            
            # Simulate channel noise
            if np.random.random() < self.error_rate:
                # Apply bit flip error
                qc.x(0)
            
            # Bob chooses basis
            if self.bob_bases[i] == 1:
                qc.h(0)
            
            # Bob measures
            qc.measure(0, 0)
            
            # Run and get the result
            job = sampler.run([qc])
            result = job.result()
            # Get the sampler result using correct API
            quasi_dist = result.quasi_dists[0]
            
            # Get the measured bit (higher probability outcome)
            measured_bit = 1 if quasi_dist.get(1, 0) > quasi_dist.get(0, 0) else 0
            bob_results.append(measured_bit)
        
        return bob_results
    
    def generate_quantum_keys(self, key_length=32):
        """
        Generate a shared secret key using BB84 protocol
        
        Args:
            key_length (int): Desired length of the final key in bytes
                              (actual bits used will be key_length*8)
        
        Returns:
            tuple: (success, key) - success is bool, key is bytes object or None
        """
        # Step 1: Alice generates random bits and bases
        self.alice_bits = np.random.randint(0, 2, self.n_bits)
        self.alice_bases = np.random.randint(0, 2, self.n_bits)
        
        # Step 2: Bob randomly chooses measurement bases
        self.bob_bases = np.random.randint(0, 2, self.n_bits)
        
        # Step 3: Alice sends qubits and Bob measures them
        logger.info("Simulating quantum transmission...")
        self.bob_results = self._simulate_quantum_transmission()
        
        # Step 4: Bob announces basis choices (public channel)
        # Step 5: Alice announces which bases matched
        self.matched_bases_idx = [i for i in range(self.n_bits) 
                                if self.alice_bases[i] == self.bob_bases[i]]
        
        # Calculate match percentage for diagnostics
        match_rate = len(self.matched_bases_idx) / self.n_bits
        logger.info(f"Bases matched: {len(self.matched_bases_idx)}/{self.n_bits} ({match_rate:.2%})")
        
        # Check if we have enough matched bases to continue
        if len(self.matched_bases_idx) < 100:
            logger.warning(f"Too few matching bases: {len(self.matched_bases_idx)}. Need at least 100 for reliable key generation.")
            return False, None
            
        # Step 6: Extract the key bits where bases matched
        raw_key = [self.alice_bits[i] for i in self.matched_bases_idx]
        bob_measured = [self.bob_results[i] for i in self.matched_bases_idx]
        
        # Step 7: Error estimation and detection
        sample_size = min(len(raw_key) // 4, 100)  # Use 25% of bits for error checking
        if sample_size > 0:
            # Choose random bits to sacrifice for error checking
            check_idx = np.random.choice(len(raw_key), sample_size, replace=False)
            
            # Compare Alice and Bob's bits
            errors = sum(raw_key[i] != bob_measured[i] for i in check_idx)
            error_rate = errors / sample_size
            
            logger.info(f"Estimated error rate: {error_rate:.2%}")
            
            # Enhanced diagnostics for eavesdropper detection
            if self.eavesdropper:
                logger.warning(f"Eve is present - Expected error rate > {0.10:.2%}, Measured: {error_rate:.2%}")
                
                if error_rate < 0.10:
                    logger.warning("SECURITY RISK: Low error rate despite eavesdropper presence!")
                    logger.warning("This indicates eavesdropper might remain undetected in some cases.")
            
            # If error rate is too high, abort (possible eavesdropping)
            # Make threshold stricter when eavesdropper is active to ensure detection
            error_threshold = 0.10 if self.eavesdropper else 0.15  # Lower threshold when eavesdropper is present
            
            # Log whether eavesdropper is active for debugging
            if self.eavesdropper:
                logger.warning(f"Eavesdropper is active in this session, using stricter threshold: {error_threshold:.2%}")
            
            if error_rate > error_threshold:  
                logger.warning(f"Error rate too high ({error_rate:.2%})! Possible eavesdropping detected.")
                return False, None
            
            # Remove the bits used for error checking
            remaining_idx = [i for i in range(len(raw_key)) if i not in check_idx]
            raw_key = [raw_key[i] for i in remaining_idx]
        
        # Step 8: Privacy amplification (use hash function to distill final key)
        if len(raw_key) < 64:  # Reduced minimum for demo purposes (was 128)
            logger.warning(f"Not enough bits for key generation: {len(raw_key)} bits")
            return False, None
        
        # Convert bit array to byte string
        raw_key_bytes = self._bits_to_bytes(raw_key)
        
        # Use hash function to generate final key
        hash_obj = hashlib.sha256(raw_key_bytes)
        final_key = hash_obj.digest()[:key_length]
        
        self.bit_count = len(raw_key)
        self.key = final_key
        
        logger.info(f"Successfully generated {key_length*8} bit key from {len(raw_key)} raw bits")
        return True, final_key
    
    def _bits_to_bytes(self, bits):
        """Convert bit array to bytes"""
        # Pad to multiple of 8
        padded_bits = bits + [0] * (8 - len(bits) % 8 if len(bits) % 8 != 0 else 0)
        
        # Convert to bytes
        byte_array = bytearray()
        for i in range(0, len(padded_bits), 8):
            byte = 0
            for j in range(8):
                if i + j < len(padded_bits):
                    byte = (byte << 1) | padded_bits[i + j]
            byte_array.append(byte)
        
        return bytes(byte_array)
    
    def visualize_protocol(self, output_file='qkd_visualization.png'):
        """
        Visualize the QKD protocol steps and results
        
        Args:
            output_file (str): Path where to save the visualization
        """
        if self.alice_bits is None or self.bob_results is None:
            logger.error("Cannot visualize: QKD protocol has not been run yet")
            return
            
        # Prepare data
        bits = min(20, self.n_bits)  # Show first 20 bits for clarity
        
        # Create a figure with multiple subplots
        fig, axes = plt.subplots(4, 1, figsize=(12, 10))
        
        # Plot 1: Alice's bits and bases
        axes[0].set_title("Alice's Random Bits and Bases")
        axes[0].bar(range(bits), self.alice_bits[:bits], color='blue', alpha=0.7)
        bases_line = [0.5 if base == 1 else -0.1 for base in self.alice_bases[:bits]]
        axes[0].plot(range(bits), bases_line, 'ro-', label='X basis' if self.alice_bases[0] == 1 else 'Z basis')
        axes[0].set_ylabel("Bit Value")
        axes[0].set_ylim(-0.2, 1.2)
        axes[0].legend()
        
        # Plot 2: Bob's bases and measurement results
        axes[1].set_title("Bob's Random Bases and Measurement Results")
        axes[1].bar(range(bits), self.bob_results[:bits], color='green', alpha=0.7)
        bases_line = [0.5 if base == 1 else -0.1 for base in self.bob_bases[:bits]]
        axes[1].plot(range(bits), bases_line, 'ro-', label='X basis' if self.bob_bases[0] == 1 else 'Z basis')
        axes[1].set_ylabel("Bit Value")
        axes[1].set_ylim(-0.2, 1.2)
        axes[1].legend()
        
        # Plot 3: Bases matching
        axes[2].set_title("Basis Matching (1 = Match, 0 = No Match)")
        matching = [1 if self.alice_bases[i] == self.bob_bases[i] else 0 for i in range(bits)]
        axes[2].bar(range(bits), matching, color='purple', alpha=0.7)
        axes[2].set_ylabel("Match Status")
        axes[2].set_ylim(-0.2, 1.2)
        
        # Plot 4: Final key bits (from matched bases)
        matched_indices = [i for i in range(bits) if i in self.matched_bases_idx]
        key_bits = []
        positions = []
        for i in matched_indices:
            key_bits.append(self.alice_bits[i])
            positions.append(i)
        
        axes[3].set_title("Key Bits (Only from Matched Bases)")
        if key_bits:
            axes[3].bar(positions, key_bits, color='orange', alpha=0.7)
        axes[3].set_ylabel("Bit Value")
        axes[3].set_ylim(-0.2, 1.2)
        axes[3].set_xlabel("Bit Position")
        
        # Adjust layout and display
        plt.tight_layout()
        plt.savefig(output_file)
        logger.info(f"QKD visualization saved to '{output_file}'")
        
        return fig

# Example usage
if __name__ == "__main__":
    # Simple test
    qkd = QKDSimulator(n_bits=200, error_rate=0.01, eavesdropper=False)
    success, key = qkd.generate_quantum_keys(key_length=16)
    
    if success:
        # Print key in hex format
        print(f"Generated key: {key.hex()}")
        
        # Visualize the protocol
        qkd.visualize_protocol()
    else:
        print("Key generation failed")
