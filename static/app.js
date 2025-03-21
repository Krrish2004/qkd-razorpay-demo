// QKD Razorpay Demo - Frontend JavaScript - Enhanced with Apple-like UX

// Global variables
let currentSimulation = null;
let pollingInterval = null;
const API_POLL_INTERVAL = 1000; // 1 second
let isScrolling = false;

// DOM Elements
const startDemoBtn = document.getElementById('startDemo');
const showHistoryBtn = document.getElementById('showHistory');
const configModal = document.getElementById('configModal');
const configForm = document.getElementById('configForm');
const closeModalBtn = document.querySelector('.close');
const cancelBtn = document.querySelector('.cancel');
const simulationContainer = document.getElementById('simulationContainer');
const historyContainer = document.getElementById('historyContainer');
const backToHomeBtn = document.getElementById('backToHome');
const newSimulationBtn = document.getElementById('newSimulation');
const downloadReportBtn = document.getElementById('downloadReport');

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    // Event listeners
    startDemoBtn.addEventListener('click', openConfigModal);
    showHistoryBtn.addEventListener('click', showHistory);
    closeModalBtn.addEventListener('click', closeConfigModal);
    cancelBtn.addEventListener('click', closeConfigModal);
    configForm.addEventListener('submit', startSimulation);
    backToHomeBtn.addEventListener('click', showHome);
    newSimulationBtn.addEventListener('click', openConfigModal);
    downloadReportBtn.addEventListener('click', downloadReport);

    // Enhanced scroll behavior
    initSmoothScrolling();
    
    // Add scroll animation effects
    initScrollAnimations();
    
    // Fix iOS scrolling issues
    fixIOSScrolling();

    // Fetch previous simulations
    fetchSimulationHistory();
});

// Initialize smooth scrolling behavior
function initSmoothScrolling() {
    // Add smooth scroll behavior to all internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                // Prevent multiple scroll events
                if (isScrolling) return;
                isScrolling = true;
                
                // Smooth scroll to target with easing
                scrollToElement(targetElement);
                
                // Update URL hash without jumping
                window.history.pushState(null, null, targetId);
                
                // Reset scrolling flag after animation completes
                setTimeout(() => {
                    isScrolling = false;
                }, 1000);
            }
        });
    });
}

// Scroll to element with easing
function scrollToElement(element) {
    const headerOffset = 80; // Account for fixed header
    const elementPosition = element.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
    
    window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
    });
}

// Initialize scroll-based animations
function initScrollAnimations() {
    // Detect elements that should animate on scroll
    const animatedElements = document.querySelectorAll('.card, .flow-step, .result-section');
    
    // Set initial state (if not visible)
    animatedElements.forEach(el => {
        if (!isElementInViewport(el)) {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        }
    });
    
    // Add scroll listener to animate elements as they come into view
    window.addEventListener('scroll', debounce(() => {
        animatedElements.forEach(el => {
            if (isElementInViewport(el)) {
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            }
        });
    }, 50));
}

// Fix iOS scrolling issues
function fixIOSScrolling() {
    // Detect iOS
    const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
    
    if (isIOS) {
        // Prevent elastic bouncing
        document.body.addEventListener('touchmove', function(e) {
            if (e.target === document.body) {
                e.preventDefault();
            }
        }, { passive: false });
        
        // Fix modal scrolling on iOS
        document.querySelectorAll('.modal-content').forEach(modal => {
            modal.addEventListener('touchmove', function(e) {
                e.stopPropagation();
            });
        });
    }
}

// Utility: Check if element is in viewport
function isElementInViewport(el) {
    const rect = el.getBoundingClientRect();
    return (
        rect.top <= (window.innerHeight || document.documentElement.clientHeight) * 0.9 &&
        rect.bottom >= 0
    );
}

// Utility: Debounce function for scroll events
function debounce(func, wait) {
    let timeout;
    return function() {
        const context = this;
        const args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(context, args), wait);
    };
}

// Open configuration modal with animation
function openConfigModal() {
    configModal.style.display = 'block';
    // Delay to allow opacity transition
    setTimeout(() => {
        document.querySelector('.modal-content').style.opacity = '1';
        document.querySelector('.modal-content').style.transform = 'translateY(0)';
    }, 10);
    
    // Disable body scrolling when modal is open
    document.body.style.overflow = 'hidden';
}

// Close configuration modal with animation
function closeConfigModal() {
    document.querySelector('.modal-content').style.opacity = '0';
    document.querySelector('.modal-content').style.transform = 'translateY(20px)';
    
    // Delay hiding the modal to allow animation to complete
    setTimeout(() => {
        configModal.style.display = 'none';
        // Re-enable body scrolling
        document.body.style.overflow = '';
    }, 300);
}

// Start a new simulation
function startSimulation(event) {
    event.preventDefault();
    
    // Get form data
    const formData = new FormData(document.getElementById('configForm'));
    const simulationData = {
        qubits: parseInt(formData.get('qubits')),
        error_rate: parseFloat(formData.get('error_rate')),
        eavesdropper: formData.get('eavesdropper') === 'on',
        amount: parseInt(formData.get('amount')) * 100, // Convert to paise
        fraud_model: formData.get('fraud_model'),
        fraud_sensitivity: parseFloat(formData.get('fraud_sensitivity'))
    };
    
    // Validate input
    if (isNaN(simulationData.qubits) || simulationData.qubits < 100 || simulationData.qubits > 5000) {
        showError('Number of qubits must be between 100 and 5000');
        return;
    }
    
    if (isNaN(simulationData.error_rate) || simulationData.error_rate < 0 || simulationData.error_rate > 0.2) {
        showError('Error rate must be between 0 and 0.2');
        return;
    }
    
    if (isNaN(simulationData.amount) || simulationData.amount < 10000 || simulationData.amount > 100000000) {
        showError('Amount must be between ₹100 and ₹1,000,000');
        return;
    }
    
    // Show loading state
    document.getElementById('simulationContainer').classList.remove('hidden');
    document.getElementById('statusBadge').textContent = 'Starting...';
    document.getElementById('statusBadge').className = 'status-badge';
    document.getElementById('progressBar').style.width = '0%';
    closeConfigModal();
    
    // Reset result fields
    document.getElementById('quantumKey').textContent = 'Generating...';
    document.getElementById('qkdTime').textContent = '-';
    document.getElementById('bitsUsed').textContent = '-';
    document.getElementById('baseMatchRate').textContent = '-';
    document.getElementById('resultOrderId').textContent = '-';
    document.getElementById('resultPaymentId').textContent = '-';
    document.getElementById('resultAmount').textContent = '-';
    document.getElementById('resultStatus').textContent = '-';
    document.getElementById('resultTotalTime').textContent = '-';
    document.getElementById('qkdEncryptionTime').textContent = '-';
    document.getElementById('qkdDecryptionTime').textContent = '-';
    document.getElementById('standardEncryptionTime').textContent = '-';
    document.getElementById('standardDecryptionTime').textContent = '-';
    document.getElementById('overhead').textContent = '-';
    document.getElementById('fraudModelType').textContent = '-';
    document.getElementById('fraudRiskScore').textContent = '-';
    document.getElementById('fraudThreshold').textContent = '-';
    document.getElementById('fraudConfidence').textContent = '-';
    document.getElementById('fraudRiskFactors').textContent = '-';
    document.getElementById('fraudDetectionTime').textContent = '-';
    
    // Reset flow steps
    for (let i = 1; i <= 5; i++) {
        const step = document.querySelector(`.flow-step[data-step="${i}"]`);
        step.classList.remove('active', 'completed', 'error');
        document.getElementById(`step${i}Status`).textContent = 'Pending';
    }
    
    // Hide visualization
    document.getElementById('qkdVisualization').classList.add('hidden');
    document.getElementById('visualizationPlaceholder').classList.remove('hidden');
    
    // Start the simulation
    fetch('/api/start_simulation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(simulationData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to start simulation');
        }
        return response.json();
    })
    .then(data => {
        if (data.simulation_id) {
            // Store simulation ID and start polling for updates
            document.getElementById('simulationId').textContent = `#${data.simulation_id.substring(0, 8)}`;
            startPolling(data.simulation_id);
        } else {
            showError('Invalid response from server');
        }
    })
    .catch(error => {
        showError(`Error: ${error.message}`);
    });
}

// Start polling for simulation updates
function startPolling(simulationId) {
    // Clear any existing polling
    if (pollingInterval) {
        clearInterval(pollingInterval);
    }
    
    // Set up new polling
    pollingInterval = setInterval(() => {
        fetchSimulationStatus(simulationId);
    }, API_POLL_INTERVAL);
}

// Fetch the status of a simulation
function fetchSimulationStatus(simulationId) {
    fetch(`/api/simulation/${simulationId}`)
        .then(response => response.json())
        .then(simulation => {
            updateSimulationUI(simulation);
            
            // Stop polling if simulation is complete or failed
            if (simulation.status === 'completed' || simulation.status === 'failed') {
                clearInterval(pollingInterval);
                pollingInterval = null;
            }
        })
        .catch(error => {
            console.error('Error fetching simulation status:', error);
        });
}

// Update the UI with simulation data
function updateSimulationUI(simulation) {
    // Update progress
    const progressPercent = Math.min(100, Math.round(simulation.progress * 100));
    document.getElementById('progressBar').style.width = `${progressPercent}%`;
    
    // Update status badge
    const statusBadge = document.getElementById('statusBadge');
    statusBadge.textContent = simulation.status;
    statusBadge.className = 'status-badge';
    
    if (simulation.status === 'Completed') {
        statusBadge.classList.add('success');
    } else if (simulation.status === 'Failed') {
        statusBadge.classList.add('error');
    } else if (simulation.status === 'Running') {
        // Default style is fine
    }
    
    // Update current step
    document.getElementById('currentStep').textContent = simulation.current_step || 'Initializing...';
    
    // Update flow steps
    updateFlowSteps(simulation);
    
    // Update visualization if available
    if (simulation.visualization_url && simulation.current_step_index >= 2) {
        const visualizationImg = document.getElementById('qkdVisualization');
        visualizationImg.src = simulation.visualization_url + '?t=' + new Date().getTime(); // Prevent caching
        visualizationImg.classList.remove('hidden');
        document.getElementById('visualizationPlaceholder').classList.add('hidden');
    }
    
    // Update QKD metrics
    if (simulation.qkd_metrics) {
        document.getElementById('quantumKey').textContent = 
            simulation.qkd_metrics.key ? 
            `${simulation.qkd_metrics.key.substring(0, 8)}...` : 
            'Generation failed';
        
        document.getElementById('qkdTime').textContent = 
            simulation.qkd_metrics.time ? 
            `${simulation.qkd_metrics.time.toFixed(2)}s` : 
            '-';
        
        document.getElementById('bitsUsed').textContent = 
            simulation.qkd_metrics.bits_used || '-';
        
        document.getElementById('baseMatchRate').textContent = 
            simulation.qkd_metrics.match_rate ? 
            `${(simulation.qkd_metrics.match_rate * 100).toFixed(1)}%` : 
            '-';
    }
    
    // Update transaction results
    if (simulation.transaction_results) {
        const results = simulation.transaction_results;
        
        // Transaction summary
        document.getElementById('resultOrderId').textContent = results.order_id || '-';
        document.getElementById('resultPaymentId').textContent = results.payment_id || '-';
        document.getElementById('resultAmount').textContent = results.amount ? 
            `₹${(results.amount / 100).toFixed(2)} ${results.currency}` : 
            '-';
        document.getElementById('resultStatus').textContent = results.status || '-';
        document.getElementById('resultTotalTime').textContent = results.total_time ? 
            `${results.total_time.toFixed(2)}s` : 
            '-';
        
        // Performance metrics
        document.getElementById('qkdEncryptionTime').textContent = results.encryption_time ? 
            `${results.encryption_time.toFixed(2)}ms` : 
            '-';
        document.getElementById('qkdDecryptionTime').textContent = results.decryption_time ? 
            `${results.decryption_time.toFixed(2)}ms` : 
            '-';
        document.getElementById('standardEncryptionTime').textContent = results.standard_encryption_time ? 
            `${results.standard_encryption_time.toFixed(2)}ms` : 
            '-';
        document.getElementById('standardDecryptionTime').textContent = results.standard_decryption_time ? 
            `${results.standard_decryption_time.toFixed(2)}ms` : 
            '-';
        document.getElementById('overhead').textContent = results.overhead ? 
            `${results.overhead.toFixed(1)}%` : 
            '-';
            
        // Fraud detection results
        if (results.fraud_detection) {
            const fraud = results.fraud_detection;
            document.getElementById('fraudModelType').textContent = fraud.model_type || 'Not used';
            document.getElementById('fraudRiskScore').textContent = fraud.risk_score !== undefined ? 
                `${fraud.risk_score.toFixed(3)}` : 
                '-';
            document.getElementById('fraudThreshold').textContent = fraud.threshold !== undefined ? 
                `${fraud.threshold.toFixed(3)}` : 
                '-';
            document.getElementById('fraudConfidence').textContent = fraud.confidence !== undefined ? 
                `${(fraud.confidence * 100).toFixed(1)}%` : 
                '-';
            document.getElementById('fraudRiskFactors').textContent = fraud.risk_factors && fraud.risk_factors.length > 0 ? 
                fraud.risk_factors.join(', ') : 
                'None detected';
            document.getElementById('fraudDetectionTime').textContent = fraud.analysis_time ? 
                `${fraud.analysis_time.toFixed(2)}ms` : 
                '-';
                
            // If fraudulent transaction was detected, show the status as Failed
            if (fraud.is_fraudulent) {
                document.getElementById('resultStatus').textContent = 'Failed - Fraud Detected';
                document.getElementById('resultStatus').classList.add('error-text');
            }
        }
    }
    
    // Add smooth reveal animations for updated content
    const newElements = document.querySelectorAll('.newly-updated');
    newElements.forEach(el => {
        el.classList.remove('newly-updated');
        el.style.opacity = '0';
        el.style.transform = 'translateY(10px)';
        
        // Trigger reflow
        void el.offsetWidth;
        
        // Apply animation
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        el.style.opacity = '1';
        el.style.transform = 'translateY(0)';
    });
}

// Update the flow steps based on the simulation progress
function updateFlowSteps(simulation) {
    // Clear previous states
    for (let i = 1; i <= 5; i++) {
        const step = document.querySelector(`.flow-step[data-step="${i}"]`);
        step.classList.remove('active', 'completed', 'error');
    }
    
    // Get current step index
    const currentStepIndex = simulation.current_step_index || 0;
    
    // Map API step indices to UI steps
    // 0: Initializing, 1: QKD, 2: Encryption, 3: Payment, 4: Fraud Detection, 5: Verification
    const stepMap = {
        0: { uiStep: 0, status: 'Initializing' },
        1: { uiStep: 1, status: 'Generating quantum key' },
        2: { uiStep: 2, status: 'Encrypting payment data' },
        3: { uiStep: 3, status: 'Processing payment' },
        4: { uiStep: 4, status: 'Analyzing for fraud' },
        5: { uiStep: 5, status: 'Verifying transaction' }
    };
    
    // Update each step's status
    for (let i = 1; i <= 5; i++) {
        const step = document.querySelector(`.flow-step[data-step="${i}"]`);
        const statusEl = document.getElementById(`step${i}Status`);
        
        if (i < currentStepIndex) {
            // Previous steps are completed
            step.classList.add('completed');
            statusEl.textContent = 'Completed';
        } else if (i === currentStepIndex) {
            // Current step is active
            step.classList.add('active');
            statusEl.textContent = stepMap[i]?.status || 'Processing';
        } else {
            // Future steps are pending
            statusEl.textContent = 'Pending';
        }
    }
    
    // Handle step errors
    if (simulation.step_errors) {
        for (const [stepIndex, error] of Object.entries(simulation.step_errors)) {
            const uiStep = parseInt(stepIndex) + 1; // API steps are 0-indexed
            const step = document.querySelector(`.flow-step[data-step="${uiStep}"]`);
            if (step) {
                step.classList.add('error');
                step.classList.remove('active', 'completed');
                document.getElementById(`step${uiStep}Status`).textContent = 'Failed';
            }
        }
    }
    
    // Special case for fraud detection result
    if (simulation.transaction_results && 
        simulation.transaction_results.fraud_detection && 
        simulation.transaction_results.fraud_detection.is_fraudulent) {
        
        const fraudStep = document.querySelector('.flow-step[data-step="4"]');
        if (fraudStep) {
            fraudStep.classList.add('error');
            fraudStep.classList.remove('active', 'completed');
            document.getElementById('step4Status').textContent = 'Fraud Detected';
            
            // Mark verification step as failed too
            const verificationStep = document.querySelector('.flow-step[data-step="5"]');
            if (verificationStep) {
                verificationStep.classList.add('error');
                verificationStep.classList.remove('active', 'completed');
                document.getElementById('step5Status').textContent = 'Failed';
            }
        }
    }
}

// Fetch the history of simulations
function fetchSimulationHistory() {
    fetch('/api/simulations')
        .then(response => response.json())
        .then(simulations => {
            updateHistoryTable(simulations);
        })
        .catch(error => {
            console.error('Error fetching simulation history:', error);
        });
}

// Update the history table with simulations
function updateHistoryTable(simulations) {
    const tableBody = document.getElementById('historyTableBody');
    const noHistory = document.getElementById('noHistory');
    
    // Clear existing rows
    tableBody.innerHTML = '';
    
    if (simulations.length === 0) {
        noHistory.classList.remove('hidden');
        return;
    }
    
    noHistory.classList.add('hidden');
    
    // Sort simulations by start time (newest first)
    simulations.sort((a, b) => {
        return new Date(b.started_at) - new Date(a.started_at);
    });
    
    // Add rows for each simulation
    simulations.forEach(sim => {
        const row = document.createElement('tr');
        
        // Format date
        const date = new Date(sim.started_at);
        const formattedDate = date.toLocaleString();
        
        // Format amount
        const amount = sim.config.amount / 100;
        
        // Calculate duration
        let duration = '-';
        if (sim.completion_time) {
            const startTime = new Date(sim.started_at);
            const endTime = new Date(sim.completion_time);
            const durationSec = (endTime - startTime) / 1000;
            duration = `${durationSec.toFixed(2)}s`;
        }
        
        // Status badge class
        let statusClass = '';
        if (sim.status === 'completed') {
            statusClass = 'success';
        } else if (sim.status === 'failed') {
            statusClass = 'error';
        } else if (sim.status === 'running') {
            statusClass = '';
        }
        
        row.innerHTML = `
            <td>${sim.id.substring(0, 8)}</td>
            <td>${formattedDate}</td>
            <td><span class="status-badge ${statusClass}">${sim.status}</span></td>
            <td>${duration}</td>
            <td>₹${amount}</td>
            <td><button class="view-simulation" data-id="${sim.id}">View</button></td>
        `;
        
        tableBody.appendChild(row);
    });
    
    // Add event listeners to view buttons
    const viewButtons = document.querySelectorAll('.view-simulation');
    viewButtons.forEach(button => {
        button.addEventListener('click', () => {
            const simId = button.getAttribute('data-id');
            viewSimulation(simId);
        });
    });
}

// View a specific simulation
function viewSimulation(simulationId) {
    fetch(`/api/simulation/${simulationId}`)
        .then(response => response.json())
        .then(simulation => {
            // Show simulation container
            simulationContainer.classList.remove('hidden');
            historyContainer.classList.add('hidden');
            
            // Update UI
            currentSimulation = simulationId;
            document.getElementById('simulationId').textContent = `#${simulationId.substring(0, 8)}`;
            
            updateSimulationUI(simulation);
        })
        .catch(error => {
            console.error('Error fetching simulation:', error);
            showError('Failed to load simulation: ' + error.message);
        });
}

// Show the history view
function showHistory() {
    simulationContainer.classList.add('hidden');
    historyContainer.classList.remove('hidden');
    
    // Fetch latest history
    fetchSimulationHistory();
}

// Show the home view
function showHome() {
    simulationContainer.classList.add('hidden');
    historyContainer.classList.add('hidden');
}

// Generate and download a report of the current simulation
function downloadReport() {
    if (!currentSimulation) {
        showError('No simulation data available for report');
        return;
    }
    
    fetch(`/api/simulation/${currentSimulation}`)
        .then(response => response.json())
        .then(simulation => {
            const reportContent = generateReportContent(simulation);
            const blob = new Blob([reportContent], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            
            const a = document.createElement('a');
            a.href = url;
            a.download = `qkd-razorpay-report-${simulation.id.substring(0, 8)}.txt`;
            a.click();
            
            URL.revokeObjectURL(url);
        })
        .catch(error => {
            console.error('Error generating report:', error);
            showError('Failed to generate report: ' + error.message);
        });
}

// Generate report content from simulation data
function generateReportContent(simulation) {
    // Function to format date
    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`;
    };
    
    // Get results
    const results = simulation.transaction_results || {};
    const qkdMetrics = simulation.qkd_metrics || {};
    const fraudResults = results.fraud_detection || {};
    
    // Build report content
    let content = `
    QKD-Razorpay Simulation Report
    ===============================
    
    Simulation ID: ${simulation.id}
    Date: ${formatDate(simulation.created_at)}
    Status: ${simulation.status}
    Duration: ${results.total_time ? results.total_time.toFixed(2) + 's' : 'Unknown'}
    
    Configuration
    ------------
    Number of Qubits: ${simulation.config?.qubits || 'Unknown'}
    Error Rate: ${simulation.config?.error_rate || 'Unknown'}
    Eavesdropper: ${simulation.config?.eavesdropper ? 'Enabled' : 'Disabled'}
    Amount: ₹${((simulation.config?.amount || 0) / 100).toFixed(2)} INR
    Fraud Model: ${simulation.config?.fraud_model || 'heuristic'}
    Fraud Sensitivity: ${simulation.config?.fraud_sensitivity || '0.7'}
    
    Quantum Key Distribution Results
    -------------------------------
    QKD Time: ${qkdMetrics.time ? qkdMetrics.time.toFixed(2) + 's' : 'Unknown'}
    Bits Used: ${qkdMetrics.bits_used || 'Unknown'}
    Base Match Rate: ${qkdMetrics.match_rate ? (qkdMetrics.match_rate * 100).toFixed(1) + '%' : 'Unknown'}
    
    Transaction Details
    ------------------
    Order ID: ${results.order_id || 'Unknown'}
    Payment ID: ${results.payment_id || 'Unknown'}
    Amount: ${results.amount ? '₹' + (results.amount / 100).toFixed(2) + ' ' + results.currency : 'Unknown'}
    Status: ${results.status || 'Unknown'}
    
    Fraud Detection Results
    ----------------------
    Model: ${fraudResults.model_type || 'Not used'}
    Risk Score: ${fraudResults.risk_score !== undefined ? fraudResults.risk_score.toFixed(3) : 'Unknown'}
    Threshold: ${fraudResults.threshold !== undefined ? fraudResults.threshold.toFixed(3) : 'Unknown'}
    Fraudulent: ${fraudResults.is_fraudulent ? 'Yes' : 'No'}
    Confidence: ${fraudResults.confidence !== undefined ? (fraudResults.confidence * 100).toFixed(1) + '%' : 'Unknown'}
    Analysis Time: ${fraudResults.analysis_time ? fraudResults.analysis_time.toFixed(2) + 'ms' : 'Unknown'}
    Risk Factors: ${
        (fraudResults.risk_factors && fraudResults.risk_factors.length) 
        ? '\n      - ' + fraudResults.risk_factors.join('\n      - ') 
        : 'None detected'
    }
    
    Performance Metrics
    ------------------
    QKD-based Encryption: ${results.encryption_time ? results.encryption_time.toFixed(2) + 'ms' : 'Unknown'}
    QKD-based Decryption: ${results.decryption_time ? results.decryption_time.toFixed(2) + 'ms' : 'Unknown'}
    Standard Encryption: ${results.standard_encryption_time ? results.standard_encryption_time.toFixed(2) + 'ms' : 'Unknown'}
    Standard Decryption: ${results.standard_decryption_time ? results.standard_decryption_time.toFixed(2) + 'ms' : 'Unknown'}
    QKD Overhead: ${results.overhead ? results.overhead.toFixed(1) + '%' : 'Unknown'}
    
    Notes
    -----
    This report was generated from a simulation of quantum key distribution (QKD)
    integrated with Razorpay payment processing and enhanced with AI fraud detection.
    The BB84 protocol was used for key generation.
    `;
    
    return content;
}

// Show an error message
function showError(message) {
    alert(message);
} 