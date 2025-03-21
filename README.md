# Quantum Key Distribution (QKD) for Razorpay Integration

This project demonstrates the use of Quantum Key Distribution (BB84 protocol) for securing payment transactions with Razorpay. It includes both a command-line implementation and a web-based visual interface with Apple-like design aesthetics and AI-powered fraud detection.

## Project Structure

```
.
├── main.py              # Command-line implementation of QKD-Razorpay demo
├── app.py               # Flask web application for web-based interface
├── run.py               # Launcher script for both CLI and web versions
├── qkd_module.py        # Implementation of BB84 protocol using Qiskit
├── encryption.py        # Encryption module using quantum-generated keys
├── razorpay_api.py      # Razorpay integration module
├── fraud_detection.py   # AI-powered fraud detection module
├── static/              # Static files for web interface
│   ├── style.css        # CSS styling with Apple-like aesthetics
│   └── app.js           # Frontend JavaScript with enhanced UX
├── templates/           # HTML templates
│   └── index.html       # Main web interface
├── tests/               # Unit and integration tests
│   ├── test_qkd.py      # Tests for QKD module
│   ├── test_encryption.py # Tests for encryption module
│   └── test_razorpay.py # Tests for Razorpay integration
├── requirements.txt     # Python dependencies (exact versions)
└── requirements-flexible.txt  # Python dependencies with flexible versions
```

## Prerequisites

- Python 3.8 or higher (including Python 3.13)
- Git (to clone the repository)
- Virtual environment tool (recommended)

## Step-by-Step Installation Guide

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/qkd-razorpay-demo.git
cd qkd-razorpay-demo
```

### 2. Set Up a Virtual Environment (Strongly Recommended)

#### For Unix/macOS:
```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

#### For Windows:
```cmd
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate
```

### 3. Install Dependencies

Depending on your Python version:

#### For Python 3.8-3.12:
```bash
pip install -r requirements.txt
```

#### For Python 3.13+:
```bash
pip install -r requirements-flexible.txt
```

### 4. Make run.py Executable (Unix/macOS only)

```bash
chmod +x run.py
```

### 5. Set Up Environment Variables (Optional)

Create a `.env` file in the project root with your Razorpay API keys:

```bash
echo "RAZORPAY_KEY_ID=your_test_key_id" > .env
echo "RAZORPAY_KEY_SECRET=your_test_key_secret" >> .env
```

Note: If you don't have Razorpay keys, the system will use dummy keys in test mode.

## Running the Demo

### Web Interface (Recommended for Visualization)

```bash
# From the project root directory (qkd-razorpay-demo)
./run.py --web
```

Then open your browser and navigate to:
```
http://localhost:5000
```

If you encounter permission issues with run.py, use:
```bash
python run.py --web
```

### Command-line Demo

```bash
# Basic demo with default settings
./run.py --cli

# Custom configuration
./run.py --cli --qubits 500 --error-rate 0.02 --amount 100000
```

## Running Tests

The project includes comprehensive unit tests for the QKD module, encryption, and Razorpay integration. To run the tests:

### Running All Tests

```bash
# From the project root directory
python -m unittest discover -s tests
```

### Running Specific Test Modules

```bash
# Test QKD module only
python -m unittest tests.test_qkd

# Test encryption module only
python -m unittest tests.test_encryption

# Test Razorpay integration only
python -m unittest tests.test_razorpay
```

### Debugging Failed Tests
If tests fail due to missing dependencies, ensure you've installed all requirements:

```bash
pip install -r requirements-flexible.txt
```

For Python 3.13+ users, some packages may require additional build tools. If you encounter build errors, try:

```bash
pip install setuptools wheel
pip install -r requirements-flexible.txt
```

## Frontend Enhancements

The web interface has been redesigned with Apple-like aesthetics and improved user experience:

### Design Improvements
- Modern color palette with Apple-inspired colors and typography
- Responsive design that works well on desktop and mobile devices
- Enhanced visual hierarchy and information architecture
- Smooth animations and transitions between states
- Dark mode support using CSS variables

### UX Enhancements
- Fixed scrolling issues with smooth scrolling behavior
- Improved modal interaction and form elements
- Enhanced visualization of transaction flow
- Added scroll-based animations for content
- Optimized performance with debounced events
- Fixed iOS-specific scrolling and display issues

### Fraud Detection Feature
- New fraud detection settings in the configuration form
- AI-powered transaction analysis with three model types:
  - Heuristic (Rule-based)
  - Machine Learning
  - Quantum-enhanced
- Adjustable sensitivity slider for fraud detection
- Detailed fraud analysis results with risk factors

## Troubleshooting Common Issues

1. **"No such file or directory: ./run.py"**
   - Make sure you are in the project root directory (qkd-razorpay-demo)
   - Try using `python run.py --web` instead

2. **"Missing dependency: No module named 'qiskit'"**
   - Ensure you've activated your virtual environment
   - Re-run the dependency installation: `pip install -r requirements-flexible.txt`

3. **Matplotlib Visualization Errors**
   - These are automatically handled in the web version with proper backend settings

4. **"QKD key generation failed" or "Error rate too high"**
   - This can happen especially when the eavesdropper simulation is enabled
   - Try again with a lower error rate or disable the eavesdropper option
   - Alternatively, use larger qubit counts for more reliable key generation

5. **Flask Address Already In Use**
   - Change the port: `./run.py --web --port 5001`

6. **Port 5000 Not Accessible**
   - Try accessing http://127.0.0.1:5000 instead of localhost

7. **Display Issues on Mobile Devices**
   - The interface is now responsive but some complex visualizations may require landscape orientation
   - Use a modern browser for the best experience

## Web Interface Usage Guide

1. **Start the application** using the instructions above
2. Open your browser and navigate to http://localhost:5000
3. Click on "Start New Simulation" to configure your QKD simulation
4. Adjust parameters in the configuration modal:
   - **Number of Qubits**: More qubits provide more security but slower simulation (1000 recommended)
   - **Error Rate**: Simulates quantum channel noise (0.01 recommended)
   - **Eavesdropper**: Simulate an attacker intercepting the quantum channel (optional)
   - **Payment Amount**: Set the payment amount in rupees
   - **Fraud Detection Settings**:
     - **AI Model Type**: Choose between Heuristic, Machine Learning, or Quantum-enhanced
     - **Detection Sensitivity**: Adjust how strictly the system flags suspicious transactions
5. Click "Start Simulation" to begin the quantum-secured transaction process
6. Watch the visualization of the quantum key distribution and transaction flow
7. View detailed results and metrics after the simulation completes
8. Use "New Simulation" to start over or "View History" to see past simulations

## Quantum Key Distribution (QKD) Process

This demo implements the BB84 QKD protocol, which involves:

1. **Qubit Preparation**: Alice prepares qubits in random states (Z or X basis)
2. **Quantum Transmission**: Qubits are transmitted through a quantum channel
3. **Measurement**: Bob measures each qubit in a randomly chosen basis
4. **Basis Reconciliation**: Alice and Bob compare their basis choices (but not measurement results)
5. **Key Extraction**: Bits where bases match are kept as the raw key
6. **Error Estimation**: Some bits are sacrificed to detect eavesdropping
7. **Privacy Amplification**: A hash function is used to generate the final key

## API Documentation

The web application exposes the following API endpoints:

### Start a new simulation
```
POST /api/start_simulation
```
**Body:**
```json
{
  "qubits": 1000,
  "error_rate": 0.01,
  "eavesdropper": false,
  "amount": 50000,
  "fraud_model": "heuristic",
  "fraud_sensitivity": 0.7
}
```

### Get simulation status
```
GET /api/simulation/{simulation_id}
```

### Get all simulations
```
GET /api/simulations
```

### Get visualization URL
```
GET /api/visualization/{simulation_id}
```

## API Compatibility Note

The code has been updated to work with the latest Qiskit API. Key changes include:

1. Importing `Aer` from `qiskit_aer` instead of directly from `qiskit`
2. Using `BackendSampler` from `qiskit.primitives` instead of `execute`
3. Adapting result processing to work with the new Sampler-based approach

## Security Notice

This is a demonstration project and should not be used for actual production payments. The implementation simplifies certain aspects of both QKD and payment processing for educational purposes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
