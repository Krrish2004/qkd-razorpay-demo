#!/usr/bin/env python3
"""
Run script for QKD-Razorpay Demo
Provides options to run either CLI or web version
"""

import os
import sys
import argparse
import subprocess

def print_banner():
    """Print a fancy banner for the application"""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ██████╗ ██╗  ██╗██████╗     ██████╗  █████╗ ███████╗ ██████╗ ██████╗ ██████╗  █████╗ ██╗   ██╗   ║
║  ██╔═══██╗██║ ██╔╝██╔══██╗    ██╔══██╗██╔══██╗╚══███╔╝██╔═══██╗██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝   ║
║  ██║   ██║█████╔╝ ██║  ██║    ██████╔╝███████║  ███╔╝ ██║   ██║██████╔╝██████╔╝███████║ ╚████╔╝    ║
║  ██║▄▄ ██║██╔═██╗ ██║  ██║    ██╔══██╗██╔══██║ ███╔╝  ██║   ██║██╔══██╗██╔═══╝ ██╔══██║  ╚██╔╝     ║
║  ╚██████╔╝██║  ██╗██████╔╝    ██║  ██║██║  ██║███████╗╚██████╔╝██║  ██║██║     ██║  ██║   ██║      ║
║   ╚══▀▀═╝ ╚═╝  ╚═╝╚═════╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝   ╚═╝      ║
║                                                               ║
║       Quantum Key Distribution for Razorpay Security          ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Check if all dependencies are installed"""
    try:
        # Check if Python modules can be imported
        import qiskit
        import flask
        import matplotlib
        import numpy
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please install required dependencies:")
        print("  For Python 3.8-3.12: pip install -r requirements.txt")
        print("  For Python 3.13+:    pip install -r requirements-flexible.txt")
        return False

def run_cli(args):
    """Run the command-line version of the application"""
    print("\nStarting command-line QKD-Razorpay demo...")
    
    # Construct the command
    cmd = ["python", "main.py"]
    
    # Add arguments if provided
    if args.qubits:
        cmd.extend(["--qubits", str(args.qubits)])
    if args.error_rate:
        cmd.extend(["--error-rate", str(args.error_rate)])
    if args.eavesdropper:
        cmd.append("--eavesdropper")
    if args.amount:
        cmd.extend(["--amount", str(args.amount)])
    if args.no_visualize:
        cmd.append("--no-visualize")
    
    # Run the command
    try:
        process = subprocess.run(cmd, check=True)
        return process.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Error running CLI demo: {e}")
        return False

def run_web(args):
    """Run the web version of the application"""
    print("\nStarting web-based QKD-Razorpay demo...")
    print(f"Server will run on http://localhost:{args.port}")
    print("Press Ctrl+C to stop the server")
    
    # Set port as environment variable
    os.environ["FLASK_RUN_PORT"] = str(args.port)
    
    # Construct the command
    cmd = ["python", "app.py"]
    
    # Run the command
    try:
        process = subprocess.run(cmd, check=True)
        return process.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Error running web demo: {e}")
        return False
    except KeyboardInterrupt:
        print("\nServer stopped")
        return True

def parse_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="QKD-Razorpay Demo - Quantum Key Distribution for Razorpay Security"
    )
    
    # Mode selection
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "--cli", action="store_true",
        help="Run command-line version of the demo"
    )
    mode_group.add_argument(
        "--web", action="store_true",
        help="Run web-based version of the demo"
    )
    
    # CLI demo arguments
    cli_group = parser.add_argument_group("CLI demo options")
    cli_group.add_argument(
        "--qubits", type=int,
        help="Number of qubits for QKD (default: 1000)"
    )
    cli_group.add_argument(
        "--error-rate", type=float,
        help="Simulated quantum channel error rate (default: 0.01)"
    )
    cli_group.add_argument(
        "--eavesdropper", action="store_true",
        help="Simulate an eavesdropper in the quantum channel"
    )
    cli_group.add_argument(
        "--amount", type=int,
        help="Transaction amount in paise (default: 50000 = ₹500.00)"
    )
    cli_group.add_argument(
        "--no-visualize", action="store_true",
        help="Skip QKD visualization"
    )
    
    # Web demo arguments
    web_group = parser.add_argument_group("Web demo options")
    web_group.add_argument(
        "--port", type=int, default=5000,
        help="Port to run the web server on (default: 5000)"
    )
    
    return parser.parse_args()

def main():
    """Main entry point"""
    # Print banner
    print_banner()
    
    # Parse arguments
    args = parse_args()
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    # Run selected mode
    if args.cli:
        success = run_cli(args)
    elif args.web:
        success = run_web(args)
    else:
        print("No mode selected. Use --cli or --web")
        return 1
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 