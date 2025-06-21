# 🔐 Quantum Key Distribution (QKD) for Razorpay Integration

[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-krrishchoudhary109%2Fqkd--razorpay--demo-blue?logo=docker)](https://hub.docker.com/r/krrishchoudhary109/qkd-razorpay-demo)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green?logo=python)](https://python.org)
[![Qiskit](https://img.shields.io/badge/Qiskit-Latest-purple?logo=qiskit)](https://qiskit.org)
[![Flask](https://img.shields.io/badge/Flask-Web%20App-red?logo=flask)](https://flask.palletsprojects.com)

A cutting-edge demonstration of **Quantum Key Distribution (BB84 protocol)** integrated with **Razorpay payment processing**, featuring **AI-powered fraud detection** and a **modern web interface**. This project showcases quantum-secured financial transactions with real-time visualizations and comprehensive security analysis.

## 🚀 Quick Start with Docker

**The fastest way to run this project:**

```bash
docker run -p 5000:5000 krrishchoudhary109/qkd-razorpay-demo:latest
```

Then open: **http://localhost:5000**

## ✨ Key Features

- 🔐 **Quantum Key Distribution** - BB84 protocol implementation with Qiskit
- 💳 **Razorpay Integration** - Real payment processing simulation
- 🤖 **AI Fraud Detection** - Quantum-enhanced machine learning models
- 🎨 **Modern UI** - Tailwind CSS with dark mode and animations
- 📊 **Real-time Visualization** - Interactive quantum state monitoring
- 📱 **Responsive Design** - Mobile-first approach with glass morphism
- 📈 **Performance Analytics** - Quantum vs classical encryption comparison
- 🔒 **Security Analysis** - Advanced eavesdropping detection
- 📋 **Transaction History** - Complete audit trail with export functionality
- 🎯 **Interactive Presentation** - Built-in demo mode

## 🌟 What Makes This Special

This project demonstrates:
- **Real-world quantum cryptography** applications in fintech
- **Integration of quantum computing** with modern web technologies
- **AI-enhanced security** using quantum-classical hybrid approaches
- **Production-ready containerization** with Docker
- **Modern DevOps practices** with comprehensive deployment options

## 🐳 Deployment Options

### Option 1: Docker Hub (Recommended)

```bash
# Pull and run the latest image
docker pull krrishchoudhary109/qkd-razorpay-demo:latest
docker run -p 5000:5000 krrishchoudhary109/qkd-razorpay-demo:latest
```

### Option 2: Docker Compose (Production)

```bash
git clone <your-repository>
cd qkd-razorpay-demo
docker compose up
```

Access at: **http://localhost** (with Nginx reverse proxy)

### Option 3: Local Development

```bash
git clone <your-repository>
cd qkd-razorpay-demo

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-flexible.txt

# Run the application
python app.py
```

## 🏗️ Project Architecture

```
qkd-razorpay-demo/
├── 🐳 Docker Configuration
│   ├── Dockerfile              # Multi-stage build with Python 3.12
│   ├── docker-compose.yml      # Production setup with Nginx
│   ├── nginx.conf              # Reverse proxy configuration
│   └── docker-helper.sh        # Management scripts
│
├── 🌐 Web Application
│   ├── app.py                  # Flask backend with REST API
│   ├── templates/
│   │   ├── index.html          # Modern Tailwind CSS interface
│   │   └── presentation.html   # Interactive demo mode
│   └── static/
│       ├── app.js              # ES6+ frontend with animations
│       └── *.png               # Generated visualizations
│
├── ⚛️ Quantum Modules
│   ├── qkd_module.py           # BB84 protocol implementation
│   ├── encryption.py           # Quantum-secured encryption
│   └── fraud_detection.py      # AI-powered security analysis
│
├── 💳 Payment Integration
│   └── razorpay_api.py         # Razorpay API integration
│
├── 🤖 AI Models
│   ├── models/
│   │   ├── feature_scaler.joblib
│   │   └── simple_nn_model.pth
│   └── research_paper/         # Academic documentation
│
└── 🧪 Testing & Documentation
    ├── tests/                  # Comprehensive test suite
    ├── DOCKER_README.md        # Docker deployment guide
    └── requirements-flexible.txt
```

## 🎯 Usage Examples

### Web Interface Features

1. **🔐 Start QKD Simulation**
   - Configure quantum parameters (qubits, error rates)
   - Real-time BB84 protocol visualization
   - Eavesdropping detection alerts

2. **💳 Payment Processing**
   - Razorpay order creation and processing
   - Quantum-secured transaction data
   - Payment verification and completion

3. **🤖 Fraud Analysis**
   - AI-powered risk assessment
   - Quantum-enhanced detection algorithms
   - Confidence scoring and recommendations

4. **📊 Performance Monitoring**
   - Quantum vs classical encryption comparison
   - Real-time metrics and analytics
   - Transaction history and export

### Command Line Interface

```bash
# Basic quantum simulation
python main.py --qubits 500 --error-rate 0.01

# Test eavesdropper detection
python main.py --qubits 500 --eavesdropper

# Custom payment amount
python main.py --amount 100000 --qubits 1000
```

## 🔬 Technical Deep Dive

### Quantum Key Distribution (BB84)
- **Quantum State Preparation**: Random bit and basis selection
- **Quantum Channel Simulation**: Noise and decoherence modeling
- **Eavesdropping Detection**: Statistical analysis of error rates
- **Key Distillation**: Privacy amplification and error correction

### AI Fraud Detection
- **Heuristic Analysis**: Rule-based risk assessment
- **Machine Learning**: Neural network classification
- **Quantum Enhancement**: Quantum-classical hybrid algorithms

### Security Features
- **Quantum-Resistant Encryption**: AES-GCM with quantum keys
- **Perfect Forward Secrecy**: New keys for each transaction
- **Tamper Detection**: Real-time security monitoring
- **Audit Trail**: Complete transaction logging

## 📊 Performance Benchmarks

| Metric | Quantum-Secured | Standard | Quantum Advantage |
|--------|----------------|----------|-------------------|
| **Key Security** | Information-theoretic | Computational | ✅ Provably secure |
| **Eavesdrop Detection** | Guaranteed | None | ✅ Physics-based |
| **Key Generation** | ~1.14s (500 qubits) | ~1ms | ⚠️ Setup overhead |
| **Encryption Speed** | ~53ms | ~45ms | ⚠️ 19% slower |
| **Future-Proof** | Quantum-resistant | Vulnerable to quantum | ✅ Post-quantum ready |

## 🛠️ Development Setup

### Prerequisites
- **Docker** (recommended) or **Python 3.8+**
- **Git** for cloning
- **Modern browser** for web interface

### Environment Variables
```bash
# Optional: Real Razorpay credentials
RAZORPAY_KEY_ID=your_key_id
RAZORPAY_KEY_SECRET=your_key_secret

# Default: Uses test mode with dummy credentials
```

### Testing
```bash
# Run all tests
python -m unittest discover -s tests

# Specific test modules
python -m unittest tests.test_qkd
python -m unittest tests.test_encryption
python -m unittest tests.test_fraud_detection
```

## 🌐 Live Demo

**Docker Hub Repository**: https://hub.docker.com/r/krrishchoudhary109/qkd-razorpay-demo

**Quick Demo Commands**:
```bash
# Pull latest version
docker pull krrishchoudhary109/qkd-razorpay-demo:latest

# Run with port mapping
docker run -p 5000:5000 krrishchoudhary109/qkd-razorpay-demo:latest

# Background execution
docker run -d -p 5000:5000 --name qkd-demo krrishchoudhary109/qkd-razorpay-demo:latest
```

## 🎓 Educational Value

This project is perfect for:
- **Quantum Computing Education** - Hands-on BB84 protocol implementation
- **Fintech Innovation** - Real-world quantum cryptography applications
- **Web Development** - Modern full-stack architecture
- **DevOps Practices** - Containerization and deployment
- **AI/ML Integration** - Quantum-enhanced machine learning

## 🤝 Contributing

We welcome contributions! Areas for enhancement:
- Additional quantum protocols (E91, SARG04)
- Advanced fraud detection algorithms
- Mobile app development
- Performance optimizations
- Documentation improvements

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Qiskit** - IBM's quantum computing framework
- **Razorpay** - Payment processing platform
- **Tailwind CSS** - Modern utility-first CSS framework
- **Flask** - Lightweight web framework
- **Docker** - Containerization platform

## 📞 Support

- **Docker Hub**: https://hub.docker.com/r/krrishchoudhary109/qkd-razorpay-demo
- **Issues**: Create an issue in the repository
- **Documentation**: Check the `research_paper/` directory for technical details

---

**⭐ Star this repository if you found it helpful!**

*Built with ❤️ for the quantum computing and fintech communities*
