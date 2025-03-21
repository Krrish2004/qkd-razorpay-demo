// QKD Razorpay Demo - Frontend JavaScript

// Global variables
let currentSimulation = null;
let pollingInterval = null;
const API_POLL_INTERVAL = 1000; // 1 second

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

    // Fetch previous simulations
    fetchSimulationHistory();
});

// Open configuration modal
function openConfigModal() {
    configModal.style.display = 'block';
}

// Close configuration modal
function closeConfigModal() {
    configModal.style.display = 'none';
}

// Start a new simulation
function startSimulation(event) {
    event.preventDefault();
    
    // Get form data
    const formData = new FormData(configForm);
    const config = {
        qubits: parseInt(formData.get('qubits')),
        error_rate: parseFloat(formData.get('error_rate')),
        eavesdropper: formData.get('eavesdropper') === 'on',
        amount: parseInt(formData.get('amount')) * 100 // Convert to paise
    };
    
    // Close the modal
    closeConfigModal();
    
    // Show simulation container
    simulationContainer.classList.remove('hidden');
    historyContainer.classList.add('hidden');
    
    // Reset UI
    document.getElementById('simulationId').textContent = 'Starting...';
    document.getElementById('statusBadge').textContent = 'Initializing';
    document.getElementById('statusBadge').className = 'status-badge';
    document.getElementById('currentStep').textContent = 'Initializing simulation...';
    document.getElementById('progressBar').style.width = '0%';
    document.getElementById('quantumKey').textContent = 'Generating...';
    document.getElementById('qkdTime').textContent = '-';
    document.getElementById('bitsUsed').textContent = '-';
    document.getElementById('baseMatchRate').textContent = '-';
    document.getElementById('qkdVisualization').classList.add('hidden');
    document.getElementById('visualizationPlaceholder').classList.remove('hidden');
    
    // Reset step statuses
    for (let i = 1; i <= 4; i++) {
        document.getElementById(`step${i}Status`).textContent = 'Pending';
        document.querySelector(`.flow-step[data-step="${i}"]`).className = 'flow-step';
    }
    
    // Reset results section
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
    
    // Start the simulation by calling the API
    fetch('/api/start_simulation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(config)
    })
    .then(response => response.json())
    .then(data => {
        if (data.simulation_id) {
            // Store the simulation ID
            currentSimulation = data.simulation_id;
            document.getElementById('simulationId').textContent = `#${currentSimulation.substring(0, 8)}`;
            
            // Start polling for updates
            startPolling(currentSimulation);
        } else {
            showError('Failed to start simulation');
        }
    })
    .catch(error => {
        console.error('Error starting simulation:', error);
        showError('Failed to start simulation: ' + error.message);
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
    // Update progress bar and status
    document.getElementById('progressBar').style.width = `${simulation.progress}%`;
    document.getElementById('currentStep').textContent = simulation.current_step;
    
    // Update status badge
    const statusBadge = document.getElementById('statusBadge');
    statusBadge.textContent = simulation.status.charAt(0).toUpperCase() + simulation.status.slice(1);
    
    // Add appropriate class to status badge
    if (simulation.status === 'completed') {
        statusBadge.className = 'status-badge success';
    } else if (simulation.status === 'failed') {
        statusBadge.className = 'status-badge error';
    } else if (simulation.status === 'running') {
        statusBadge.className = 'status-badge';
    }
    
    // Update flow steps based on progress
    updateFlowSteps(simulation);
    
    // Update QKD metrics if available
    if (simulation.quantum_key) {
        document.getElementById('quantumKey').textContent = 
            `${simulation.quantum_key.substring(0, 8)}...${simulation.quantum_key.substring(simulation.quantum_key.length - 8)}`;
    }
    
    if (simulation.qkd_time) {
        document.getElementById('qkdTime').textContent = `${simulation.qkd_time.toFixed(2)} seconds`;
    }
    
    if (simulation.bit_count) {
        document.getElementById('bitsUsed').textContent = simulation.bit_count;
    }
    
    if (simulation.base_match_rate) {
        document.getElementById('baseMatchRate').textContent = `${(simulation.base_match_rate * 100).toFixed(2)}%`;
    }
    
    // Update visualization if available
    if (simulation.visualization_url && document.getElementById('qkdVisualization').classList.contains('hidden')) {
        const visImg = document.getElementById('qkdVisualization');
        visImg.src = simulation.visualization_url;
        visImg.onload = () => {
            document.getElementById('visualizationPlaceholder').classList.add('hidden');
            visImg.classList.remove('hidden');
        };
    }
    
    // Update results section for completed simulations
    if (simulation.status === 'completed') {
        document.getElementById('resultOrderId').textContent = simulation.order_id || '-';
        document.getElementById('resultPaymentId').textContent = simulation.payment_id || '-';
        
        if (simulation.payment_details && simulation.payment_details.amount) {
            const amount = simulation.payment_details.amount / 100;
            const currency = simulation.payment_details.currency || 'INR';
            document.getElementById('resultAmount').textContent = `${amount} ${currency}`;
        }
        
        document.getElementById('resultStatus').textContent = simulation.payment_details?.status || 'Success';
        document.getElementById('resultTotalTime').textContent = `${simulation.total_time.toFixed(2)} seconds`;
        
        // Performance metrics
        if (simulation.encryption_time) {
            document.getElementById('qkdEncryptionTime').textContent = `${(simulation.encryption_time * 1000).toFixed(2)} ms`;
        }
        
        if (simulation.decryption_time) {
            document.getElementById('qkdDecryptionTime').textContent = `${(simulation.decryption_time * 1000).toFixed(2)} ms`;
        }
        
        if (simulation.standard_encryption_time) {
            document.getElementById('standardEncryptionTime').textContent = `${simulation.standard_encryption_time.toFixed(2)} ms`;
        }
        
        if (simulation.standard_decryption_time) {
            document.getElementById('standardDecryptionTime').textContent = `${simulation.standard_decryption_time.toFixed(2)} ms`;
        }
        
        if (simulation.encryption_overhead && simulation.decryption_overhead) {
            document.getElementById('overhead').textContent = 
                `+${simulation.encryption_overhead.toFixed(2)}% (enc), +${simulation.decryption_overhead.toFixed(2)}% (dec)`;
        }
    }
    
    // Show error message if simulation failed
    if (simulation.status === 'failed' && simulation.error) {
        showError(`Simulation failed: ${simulation.error}`);
    }
}

// Update the flow steps based on the simulation progress
function updateFlowSteps(simulation) {
    // Reset all steps
    for (let i = 1; i <= 4; i++) {
        document.querySelector(`.flow-step[data-step="${i}"]`).className = 'flow-step';
        document.getElementById(`step${i}Status`).textContent = 'Pending';
    }
    
    // Determine active and completed steps based on progress
    let activeStep = 0;
    
    if (simulation.progress >= 10 && simulation.progress < 30) {
        // QKD step
        activeStep = 1;
        document.getElementById('step1Status').textContent = 'In Progress';
    } else if (simulation.progress >= 30 && simulation.progress < 60) {
        // Encryption step
        activeStep = 2;
        document.getElementById('step1Status').textContent = 'Completed';
        document.getElementById('step2Status').textContent = 'In Progress';
    } else if (simulation.progress >= 60 && simulation.progress < 90) {
        // Razorpay order step
        activeStep = 3;
        document.getElementById('step1Status').textContent = 'Completed';
        document.getElementById('step2Status').textContent = 'Completed';
        document.getElementById('step3Status').textContent = 'In Progress';
    } else if (simulation.progress >= 90) {
        // Verification step
        activeStep = 4;
        document.getElementById('step1Status').textContent = 'Completed';
        document.getElementById('step2Status').textContent = 'Completed';
        document.getElementById('step3Status').textContent = 'Completed';
        document.getElementById('step4Status').textContent = 'In Progress';
    }
    
    // Mark steps as active or completed
    for (let i = 1; i <= 4; i++) {
        const stepElement = document.querySelector(`.flow-step[data-step="${i}"]`);
        
        if (i < activeStep) {
            // Completed steps
            stepElement.classList.add('completed');
        } else if (i === activeStep) {
            // Active step
            stepElement.classList.add('active');
        }
    }
    
    // If simulation is completed, mark all steps as completed
    if (simulation.status === 'completed') {
        for (let i = 1; i <= 4; i++) {
            document.querySelector(`.flow-step[data-step="${i}"]`).className = 'flow-step completed';
            document.getElementById(`step${i}Status`).textContent = 'Completed';
        }
    }
    
    // If simulation failed, mark the active step as error
    if (simulation.status === 'failed') {
        document.querySelector(`.flow-step[data-step="${activeStep}"]`).classList.add('error');
        document.getElementById(`step${activeStep}Status`).textContent = 'Failed';
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
    const lines = [
        "Quantum Key Distribution (QKD) for Razorpay Security - Simulation Report",
        "=======================================================================",
        "",
        `Simulation ID: ${simulation.id}`,
        `Started At: ${new Date(simulation.started_at).toLocaleString()}`,
        `Status: ${simulation.status}`,
        "",
        "Configuration:",
        `- Qubits: ${simulation.config.n_bits}`,
        `- Error Rate: ${simulation.config.error_rate}`,
        `- Eavesdropper: ${simulation.config.eavesdropper ? 'Yes' : 'No'}`,
        `- Amount: ₹${simulation.config.amount / 100}`,
        "",
        "QKD Results:",
        `- Quantum Key: ${simulation.quantum_key || 'N/A'}`,
        `- QKD Time: ${simulation.qkd_time ? simulation.qkd_time.toFixed(2) + ' seconds' : 'N/A'}`,
        `- Bits Used: ${simulation.bit_count || 'N/A'}`,
        `- Base Match Rate: ${simulation.base_match_rate ? (simulation.base_match_rate * 100).toFixed(2) + '%' : 'N/A'}`,
        "",
        "Transaction Details:",
        `- Order ID: ${simulation.order_id || 'N/A'}`,
        `- Payment ID: ${simulation.payment_id || 'N/A'}`,
        `- Amount: ${simulation.payment_details?.amount ? simulation.payment_details.amount / 100 + ' ' + (simulation.payment_details.currency || 'INR') : 'N/A'}`,
        `- Status: ${simulation.payment_details?.status || 'N/A'}`,
        `- Total Time: ${simulation.total_time ? simulation.total_time.toFixed(2) + ' seconds' : 'N/A'}`,
        "",
        "Performance Metrics:",
        `- QKD-based Encryption: ${simulation.encryption_time ? (simulation.encryption_time * 1000).toFixed(2) + ' ms' : 'N/A'}`,
        `- QKD-based Decryption: ${simulation.decryption_time ? (simulation.decryption_time * 1000).toFixed(2) + ' ms' : 'N/A'}`,
        `- Standard Encryption: ${simulation.standard_encryption_time ? simulation.standard_encryption_time.toFixed(2) + ' ms' : 'N/A'}`,
        `- Standard Decryption: ${simulation.standard_decryption_time ? simulation.standard_decryption_time.toFixed(2) + ' ms' : 'N/A'}`,
        `- Encryption Overhead: ${simulation.encryption_overhead ? simulation.encryption_overhead.toFixed(2) + '%' : 'N/A'}`,
        `- Decryption Overhead: ${simulation.decryption_overhead ? simulation.decryption_overhead.toFixed(2) + '%' : 'N/A'}`,
        "",
        "Steps Timeline:",
    ];
    
    // Add steps timeline
    if (simulation.steps && simulation.steps.length > 0) {
        simulation.steps.forEach(step => {
            const time = new Date(step.timestamp).toLocaleTimeString();
            lines.push(`- ${time}: ${step.name} (${step.progress}%)`);
        });
    } else {
        lines.push("No steps data available");
    }
    
    // Add error information if applicable
    if (simulation.status === 'failed' && simulation.error) {
        lines.push("");
        lines.push("Error Information:");
        lines.push(`- ${simulation.error}`);
    }
    
    // Add footer
    lines.push("");
    lines.push("Generated at: " + new Date().toLocaleString());
    lines.push("QKD-Razorpay Demo - A System Engineering Project");
    
    return lines.join('\n');
}

// Show an error message
function showError(message) {
    alert(message);
} 