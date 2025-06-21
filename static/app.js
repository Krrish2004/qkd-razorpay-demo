// QKD Razorpay Demo - Modern Frontend JavaScript with Tailwind CSS

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

// New history-related elements
const refreshHistoryBtn = document.getElementById('refreshHistory');
const exportHistoryBtn = document.getElementById('exportHistory');
const backToHomeFromHistoryBtn = document.getElementById('backToHomeFromHistory');
const startFirstSimulationBtn = document.getElementById('startFirstSimulation');

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

    // History-related event listeners
    if (refreshHistoryBtn) refreshHistoryBtn.addEventListener('click', fetchSimulationHistory);
    if (exportHistoryBtn) exportHistoryBtn.addEventListener('click', exportHistoryData);
    if (backToHomeFromHistoryBtn) backToHomeFromHistoryBtn.addEventListener('click', showHome);
    if (startFirstSimulationBtn) startFirstSimulationBtn.addEventListener('click', openConfigModal);

    // Close modal when clicking outside
    configModal.addEventListener('click', (e) => {
        if (e.target === configModal) {
            closeConfigModal();
        }
    });

    // Enhanced animations
    initScrollAnimations();
    
    // Add dark mode support
    initDarkMode();
    
    // Add enhanced form interactions
    initFormEnhancements();

    // Fetch previous simulations
    fetchSimulationHistory();
});

// Initialize dark mode support
function initDarkMode() {
    // Check for saved theme preference or default to light
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        document.documentElement.classList.add('dark');
    }
    
    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('theme')) {
            if (e.matches) {
                document.documentElement.classList.add('dark');
            } else {
                document.documentElement.classList.remove('dark');
            }
        }
    });
}

// Initialize enhanced form interactions
function initFormEnhancements() {
    // Sensitivity slider with visual feedback
    const sensitivitySlider = document.getElementById('fraudSensitivity');
    const sensitivityValue = document.getElementById('sensitivityValue');
    
    if (sensitivitySlider && sensitivityValue) {
        sensitivitySlider.addEventListener('input', function() {
            const value = parseFloat(this.value);
            sensitivityValue.textContent = value;
            
            // Update color based on sensitivity level
            sensitivityValue.className = 'text-sm font-medium px-2 py-1 rounded-lg transition-colors';
            if (value < 0.4) {
                sensitivityValue.className += ' bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200';
            } else if (value < 0.7) {
                sensitivityValue.className += ' bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200';
            } else {
                sensitivityValue.className += ' bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200';
            }
        });
        
        // Trigger initial update
        sensitivitySlider.dispatchEvent(new Event('input'));
    }
    
    // Enhanced form validation
    const numberInputs = document.querySelectorAll('input[type="number"]');
    numberInputs.forEach(input => {
        input.addEventListener('input', function() {
            const value = parseFloat(this.value);
            const min = parseFloat(this.getAttribute('min'));
            const max = parseFloat(this.getAttribute('max'));
            
            this.classList.remove('border-red-500', 'border-green-500');
            
            if (value < min || value > max || isNaN(value)) {
                this.classList.add('border-red-500');
            } else {
                this.classList.add('border-green-500');
            }
        });
    });
}

// Initialize scroll-based animations
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements that should animate
    document.querySelectorAll('[class*="animate-"]').forEach(el => {
        observer.observe(el);
    });
}

// Open configuration modal with enhanced animation
function openConfigModal() {
    configModal.classList.remove('hidden');
    configModal.classList.add('flex');
    
    // Add entrance animation
    const modalContent = configModal.querySelector('div > div');
    modalContent.style.transform = 'scale(0.9) translateY(20px)';
    modalContent.style.opacity = '0';
    
    // Animate in
    setTimeout(() => {
        modalContent.style.transform = 'scale(1) translateY(0)';
        modalContent.style.opacity = '1';
        modalContent.style.transition = 'all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)';
    }, 10);
    
    // Disable body scrolling
    document.body.style.overflow = 'hidden';
}

// Close configuration modal with enhanced animation
function closeConfigModal() {
    const modalContent = configModal.querySelector('div > div');
    
    // Animate out
    modalContent.style.transform = 'scale(0.9) translateY(20px)';
    modalContent.style.opacity = '0';
    modalContent.style.transition = 'all 0.2s ease-in';
    
    setTimeout(() => {
        configModal.classList.add('hidden');
        configModal.classList.remove('flex');
        document.body.style.overflow = '';
    }, 200);
}

// Start a new simulation with enhanced validation
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
    
    // Enhanced validation
    const errors = [];
    
    if (isNaN(simulationData.qubits) || simulationData.qubits < 100 || simulationData.qubits > 5000) {
        errors.push('Number of qubits must be between 100 and 5000');
    }
    
    if (isNaN(simulationData.error_rate) || simulationData.error_rate < 0 || simulationData.error_rate > 0.2) {
        errors.push('Error rate must be between 0 and 0.2');
    }
    
    if (isNaN(simulationData.amount) || simulationData.amount < 10000 || simulationData.amount > 100000000) {
        errors.push('Amount must be between ₹100 and ₹1,000,000');
    }
    
    if (errors.length > 0) {
        showError(errors.join('<br>'));
        return;
    }
    
    // Show loading state
    const submitBtn = document.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Starting...';
    submitBtn.disabled = true;
    
    // Start simulation
    fetch('/api/start_simulation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(simulationData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            currentSimulation = data.simulation_id;
            closeConfigModal();
            showSimulationContainer();
            startPolling(data.simulation_id);
            
            // Show success message
            showSuccess('Simulation started successfully!');
            
            // Scroll to simulation container
            setTimeout(() => {
                simulationContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 300);
        } else {
            showError(data.error || 'Failed to start simulation');
        }
    })
    .catch(error => {
        console.error('Error starting simulation:', error);
        showError('Failed to start simulation. Please check your connection and try again.');
    })
    .finally(() => {
        // Reset button state
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    });
}

// Show simulation container with animation
function showSimulationContainer() {
    simulationContainer.classList.remove('hidden');
    simulationContainer.classList.add('animate-fade-in');
    
    // Initialize progress bar
    const progressBar = document.getElementById('progressBar');
    progressBar.style.width = '0%';
    
    // Reset all step statuses
    for (let i = 1; i <= 5; i++) {
        updateStepStatus(i, 'pending');
    }
}

// Start polling for simulation updates
function startPolling(simulationId) {
    if (pollingInterval) {
        clearInterval(pollingInterval);
    }
    
    pollingInterval = setInterval(() => {
        fetchSimulationStatus(simulationId);
    }, API_POLL_INTERVAL);
    
    // Initial fetch
    fetchSimulationStatus(simulationId);
}

// Fetch simulation status
function fetchSimulationStatus(simulationId) {
    fetch(`/api/simulation/${simulationId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateSimulationUI(data.simulation);
                
                if (data.simulation.status === 'completed' || data.simulation.status === 'failed') {
                    clearInterval(pollingInterval);
                    pollingInterval = null;
                }
            } else {
                console.error('Error fetching simulation status:', data.error);
            }
        })
        .catch(error => {
            console.error('Error fetching simulation status:', error);
        });
}

// Update simulation UI with modern styling
function updateSimulationUI(simulation) {
    // Update simulation ID
    const shortId = simulation.id ? simulation.id.substring(0, 8) : 'Unknown';
    document.getElementById('simulationId').textContent = `#${shortId}`;
    
    // Update status badge
    updateStatusBadge(simulation.status);
    
    // Update progress bar
    updateProgress(simulation.progress || 0);
    
    // Update current step
    document.getElementById('currentStep').textContent = simulation.current_step || 'Initializing...';
    
    // Update flow steps
    updateFlowSteps(simulation);
    
    // Update QKD visualization
    if (simulation.qkd_visualization) {
        const img = document.getElementById('qkdVisualization');
        const placeholder = document.getElementById('visualizationPlaceholder');
        
        img.src = simulation.qkd_visualization + '?t=' + Date.now();
        img.classList.remove('hidden');
        placeholder.classList.add('hidden');
    }
    
    // Update metrics from QKD metrics or direct fields
    const qkdMetrics = simulation.qkd_metrics || {};
    
    if (qkdMetrics.time || simulation.qkd_time) {
        const time = qkdMetrics.time || simulation.qkd_time;
        document.getElementById('qkdTime').textContent = typeof time === 'number' ? 
            (time > 1 ? `${time.toFixed(2)}s` : `${(time * 1000).toFixed(0)}ms`) : 
            time;
    }
    
    if (qkdMetrics.bits_used || simulation.bit_count) {
        document.getElementById('bitsUsed').textContent = qkdMetrics.bits_used || simulation.bit_count;
    }
    
    if (qkdMetrics.key || simulation.quantum_key) {
        const key = qkdMetrics.key || simulation.quantum_key;
        const keyDisplay = key && key.length > 32 ? 
            key.substring(0, 32) + '...' : 
            key || 'Generating...';
        document.getElementById('quantumKey').textContent = keyDisplay;
    }
    
    // Update results if completed
    if (simulation.status === 'completed' && simulation.transaction_results) {
        updateResults(simulation.transaction_results);
    }
}

// Update status badge with modern styling
function updateStatusBadge(status) {
    const badge = document.getElementById('statusBadge');
    badge.className = 'px-4 py-2 rounded-full text-sm font-semibold transition-all duration-300';
    
    switch(status) {
        case 'running':
            badge.className += ' bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 animate-pulse';
            badge.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Running';
            break;
        case 'completed':
            badge.className += ' bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200';
            badge.innerHTML = '<i class="fas fa-check mr-2"></i>Completed';
            break;
        case 'failed':
            badge.className += ' bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200';
            badge.innerHTML = '<i class="fas fa-times mr-2"></i>Failed';
            break;
        default:
            badge.className += ' bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200';
            badge.innerHTML = '<i class="fas fa-clock mr-2"></i>Initializing';
    }
}

// Update progress bar with smooth animation
function updateProgress(progress) {
    const progressBar = document.getElementById('progressBar');
    progressBar.style.width = progress + '%';
    
    // Change gradient based on progress
    if (progress === 100) {
        progressBar.style.background = 'linear-gradient(to right, #22c55e, #16a34a)';
    } else if (progress > 50) {
        progressBar.style.background = 'linear-gradient(to right, #0ea5e9, #22c55e)';
    } else {
        progressBar.style.background = 'linear-gradient(to right, #0ea5e9, #3b82f6)';
    }
}

// Update flow steps with enhanced animations
function updateFlowSteps(simulation) {
    const stepMappings = {
        'Initializing': 1,
        'Running quantum key distribution': 1,
        'Generating QKD visualization': 1,
        'QKD completed': 1,
        'Preparing payment data': 2,
        'Encrypting payment data': 2,
        'Creating Razorpay order': 3,
        'Creating payment link': 3,
        'Simulating payment completion': 3,
        'Analyzing transaction for fraud': 4,
        'Verifying payment': 5,
        'Transaction completed': 5
    };
    
    const currentStepIndex = stepMappings[simulation.current_step] || 0;
    
    // Update step statuses
    for (let i = 1; i <= 5; i++) {
        if (i < currentStepIndex) {
            updateStepStatus(i, 'completed');
        } else if (i === currentStepIndex) {
            updateStepStatus(i, 'active');
        } else {
            updateStepStatus(i, 'pending');
        }
    }
    
    // Handle errors
    if (simulation.status === 'failed') {
        updateStepStatus(currentStepIndex, 'error');
    }
}

// Update step status with modern styling
function updateStepStatus(stepIndex, status) {
    const step = document.querySelector(`[data-step="${stepIndex}"]`);
    if (!step) return;
    
    const icon = step.querySelector('div:first-child');
    const statusEl = step.querySelector('[id$="Status"]');
    
    // Reset classes
    step.className = 'flow-step flex items-center space-x-4 p-4 rounded-2xl transition-all duration-500';
    
    switch(status) {
        case 'active':
            step.className += ' bg-blue-50 dark:bg-blue-900/20 border-2 border-blue-200 dark:border-blue-800 transform scale-105';
            icon.className = icon.className.replace(/bg-\w+-\d+/, 'bg-blue-200 dark:bg-blue-800 animate-pulse');
            statusEl.textContent = 'In Progress';
            statusEl.className = 'text-xs text-blue-600 dark:text-blue-400 font-semibold mt-1';
            break;
        case 'completed':
            step.className += ' bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800';
            icon.className = icon.className.replace(/bg-\w+-\d+/, 'bg-green-200 dark:bg-green-800');
            statusEl.textContent = 'Completed';
            statusEl.className = 'text-xs text-green-600 dark:text-green-400 font-semibold mt-1';
            break;
        case 'error':
            step.className += ' bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800';
            icon.className = icon.className.replace(/bg-\w+-\d+/, 'bg-red-200 dark:bg-red-800');
            statusEl.textContent = 'Failed';
            statusEl.className = 'text-xs text-red-600 dark:text-red-400 font-semibold mt-1';
            break;
        default:
            step.className += ' bg-gray-50 dark:bg-gray-700';
            statusEl.textContent = 'Pending';
            statusEl.className = 'text-xs text-gray-500 dark:text-gray-400 mt-1';
    }
}

// Update results section
function updateResults(results) {
    // Transaction Summary
    document.getElementById('resultOrderId').textContent = results.order_id || '-';
    document.getElementById('resultPaymentId').textContent = results.payment_id || '-';
    document.getElementById('resultAmount').textContent = results.amount ? `₹${results.amount / 100}` : '-';
    
    // Status badge
    const statusBadge = document.getElementById('resultStatus');
    if (results.status) {
        statusBadge.textContent = results.status;
        statusBadge.className = 'px-3 py-1 rounded-full text-xs font-semibold';
        
        if (results.status === 'Success') {
            statusBadge.className += ' bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200';
        } else {
            statusBadge.className += ' bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200';
        }
    }
    
    // Performance Metrics
    const qkdTime = results.qkd_time || results.total_time;
    document.getElementById('perfQkdTime').textContent = qkdTime ? 
        (qkdTime > 1 ? `${qkdTime.toFixed(2)}s` : `${(qkdTime * 1000).toFixed(0)}ms`) : '-';
    
    document.getElementById('perfEncryption').textContent = results.encryption_time ? 
        `${results.encryption_time.toFixed(2)}ms` : '-';
    
    const fraudScore = results.fraud_detection?.risk_score;
    document.getElementById('perfFraudScore').textContent = fraudScore ? 
        `${(fraudScore * 100).toFixed(1)}%` : '-';
    
    document.getElementById('perfTotalTime').textContent = results.total_time ? 
        `${results.total_time.toFixed(2)}s` : '-';
}

// Show history with enhanced animations
function showHistory() {
    // Hide other containers with animation
    const heroSection = document.querySelector('section');
    const simContainer = document.getElementById('simulationContainer');
    
    if (heroSection) {
        heroSection.style.opacity = '0';
        heroSection.style.transform = 'translateY(-20px)';
        setTimeout(() => heroSection.classList.add('hidden'), 300);
    }
    
    if (simContainer) {
        simContainer.classList.add('hidden');
    }
    
    // Show history container with animation
    historyContainer.classList.remove('hidden');
    historyContainer.style.opacity = '0';
    historyContainer.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
        historyContainer.style.opacity = '1';
        historyContainer.style.transform = 'translateY(0)';
        historyContainer.style.transition = 'all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1)';
    }, 50);
    
    // Fetch fresh history data
    fetchSimulationHistory();
}

// Show error notification
function showError(message) {
    showNotification(message, 'error');
}

// Show success notification
function showSuccess(message) {
    showNotification(message, 'success');
}

// Show notification with modern styling
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 z-50 p-4 rounded-2xl shadow-lg max-w-sm transform translate-x-full transition-all duration-300`;
    
    // Set styling based on type
    switch(type) {
        case 'error':
            notification.className += ' bg-red-50 dark:bg-red-900 border border-red-200 dark:border-red-800 text-red-800 dark:text-red-200';
            notification.innerHTML = `<i class="fas fa-exclamation-circle mr-2"></i>${message}`;
            break;
        case 'success':
            notification.className += ' bg-green-50 dark:bg-green-900 border border-green-200 dark:border-green-800 text-green-800 dark:text-green-200';
            notification.innerHTML = `<i class="fas fa-check-circle mr-2"></i>${message}`;
            break;
        default:
            notification.className += ' bg-blue-50 dark:bg-blue-900 border border-blue-200 dark:border-blue-800 text-blue-800 dark:text-blue-200';
            notification.innerHTML = `<i class="fas fa-info-circle mr-2"></i>${message}`;
    }
    
    // Add to DOM
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(full)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 5000);
}

// Utility functions
function formatTime(ms) {
    if (ms < 1000) return `${ms}ms`;
    const seconds = (ms / 1000).toFixed(1);
    return `${seconds}s`;
}

function formatKey(key) {
    if (!key) return '-';
    return key.length > 32 ? key.substring(0, 32) + '...' : key;
}

// Fetch the history of simulations with improved error handling
function fetchSimulationHistory() {
    // Show loading state
    const tableBody = document.getElementById('historyTableBody');
    const noHistory = document.getElementById('noHistory');
    
    if (tableBody) {
        tableBody.innerHTML = '<tr><td colspan="8" class="px-6 py-4 text-center text-gray-500 dark:text-gray-400"><i class="fas fa-spinner fa-spin mr-2"></i>Loading history...</td></tr>';
    }
    
    fetch('/api/simulations')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateHistoryTable(data.simulations);
                
                // Show count in notification
                if (data.count > 0) {
                    showNotification(`Loaded ${data.count} simulation${data.count !== 1 ? 's' : ''}`, 'success');
                }
            } else {
                throw new Error(data.error || 'Failed to fetch simulation history');
            }
        })
        .catch(error => {
            console.error('Error fetching simulation history:', error);
            showError('Failed to load simulation history: ' + error.message);
            
            // Show error state
            if (tableBody) {
                tableBody.innerHTML = '<tr><td colspan="8" class="px-6 py-4 text-center text-red-500 dark:text-red-400"><i class="fas fa-exclamation-triangle mr-2"></i>Failed to load history</td></tr>';
            }
        });
}

// Update the history table with simulations - Enhanced version
function updateHistoryTable(simulations) {
    const tableBody = document.getElementById('historyTableBody');
    const noHistory = document.getElementById('noHistory');
    
    // Clear existing rows
    tableBody.innerHTML = '';
    
    if (!simulations || simulations.length === 0) {
        noHistory.classList.remove('hidden');
        return;
    }
    
    noHistory.classList.add('hidden');
    
    // Sort simulations by start time (newest first)
    simulations.sort((a, b) => {
        return new Date(b.started_at) - new Date(a.started_at);
    });
    
    // Add rows for each simulation
    simulations.forEach((sim, index) => {
        const row = document.createElement('tr');
        row.className = 'hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-200';
        
        // Format date
        const date = new Date(sim.started_at);
        const formattedDate = date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'});
        
        // Format amount
        const amount = sim.config ? (sim.config.amount / 100) : 0;
        
        // Calculate duration
        let duration = '-';
        if (sim.completion_time) {
            const startTime = new Date(sim.started_at);
            const endTime = new Date(sim.completion_time);
            const durationSec = (endTime - startTime) / 1000;
            duration = `${durationSec.toFixed(1)}s`;
        } else if (sim.status === 'running') {
            duration = 'Running...';
        }
        
        // Get fraud score
        const fraudScore = sim.transaction_results?.fraud_detection?.risk_score;
        const fraudDisplay = fraudScore ? `${(fraudScore * 100).toFixed(1)}%` : '-';
        
        // Status badge styling
        let statusBadge = '';
        switch(sim.status) {
            case 'completed':
                statusBadge = '<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200"><i class="fas fa-check-circle mr-1"></i>Completed</span>';
                break;
            case 'failed':
                statusBadge = '<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200"><i class="fas fa-times-circle mr-1"></i>Failed</span>';
                break;
            case 'running':
                statusBadge = '<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200 animate-pulse"><i class="fas fa-spinner fa-spin mr-1"></i>Running</span>';
                break;
            default:
                statusBadge = '<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200">Unknown</span>';
        }
        
        row.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-mono text-gray-900 dark:text-white">#${sim.id.substring(0, 8)}</div>
                <div class="text-xs text-gray-500 dark:text-gray-400 sm:hidden">${formattedDate}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap hidden sm:table-cell">
                <div class="text-sm text-gray-900 dark:text-white">${formattedDate}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                ${statusBadge}
                <div class="text-xs text-gray-500 dark:text-gray-400 md:hidden mt-1">${duration}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap hidden md:table-cell">
                <div class="text-sm text-gray-900 dark:text-white">${duration}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-semibold text-cyber-600 dark:text-cyber-400">₹${amount.toFixed(2)}</div>
                <div class="text-xs text-gray-500 dark:text-gray-400 lg:hidden">
                    ${sim.config ? sim.config.qubits : '-'} qubits • ${fraudDisplay} fraud
                </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap hidden lg:table-cell">
                <div class="text-sm text-gray-900 dark:text-white">${sim.config ? sim.config.qubits : '-'}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap hidden lg:table-cell">
                <div class="text-sm text-gray-900 dark:text-white">${fraudDisplay}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button class="view-simulation bg-gradient-to-r from-quantum-500 to-cyber-500 text-white px-3 py-1.5 rounded-lg text-xs font-medium hover:from-quantum-600 hover:to-cyber-600 transition-all duration-200 transform hover:scale-105" data-id="${sim.id}">
                    <i class="fas fa-eye mr-1"></i>View
                </button>
            </td>
        `;
        
        // Add staggered animation
        row.style.opacity = '0';
        row.style.transform = 'translateY(20px)';
        setTimeout(() => {
            row.style.opacity = '1';
            row.style.transform = 'translateY(0)';
            row.style.transition = 'all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1)';
        }, index * 100);
        
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

// View a specific simulation with enhanced navigation
function viewSimulation(simulationId) {
    fetch(`/api/simulation/${simulationId}`)
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                throw new Error(data.error || 'Failed to fetch simulation');
            }
            
            const simulation = data.simulation;
            
            // Hide history container with animation
            historyContainer.style.opacity = '0';
            historyContainer.style.transform = 'translateY(-20px)';
            setTimeout(() => historyContainer.classList.add('hidden'), 300);
            
            // Show simulation container with animation
            setTimeout(() => {
                showSimulationContainer();
                currentSimulation = simulationId;
                
                // Update simulation ID display
                const simIdElement = document.getElementById('simulationId');
                if (simIdElement) {
                    simIdElement.textContent = `#${simulationId.substring(0, 8)}`;
                }
                
                updateSimulationUI(simulation);
                
                // If simulation is completed, show all results immediately
                if (simulation.status === 'completed') {
                    updateProgress(100);
                    updateStatusBadge('completed');
                    updateFlowSteps(simulation);
                    if (simulation.transaction_results) {
                        updateResults(simulation.transaction_results);
                    }
                } else if (simulation.status === 'running') {
                    // Start polling for running simulations
                    startPolling(simulationId);
                }
            }, 350);
        })
        .catch(error => {
            console.error('Error fetching simulation:', error);
            showError('Failed to load simulation: ' + error.message);
        });
}

// Show the home view with enhanced animations
function showHome() {
    // Hide other containers
    simulationContainer.classList.add('hidden');
    historyContainer.classList.add('hidden');
    
    // Show hero section
    const heroSection = document.querySelector('section');
    if (heroSection) {
        heroSection.classList.remove('hidden');
        heroSection.style.opacity = '0';
        heroSection.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            heroSection.style.opacity = '1';
            heroSection.style.transform = 'translateY(0)';
            heroSection.style.transition = 'all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1)';
        }, 50);
    }
    
    // Clear any active simulation polling
    if (pollingInterval) {
        clearInterval(pollingInterval);
        pollingInterval = null;
    }
    
    currentSimulation = null;
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

// Export history data as CSV
function exportHistoryData() {
    fetch('/api/simulations')
        .then(response => response.json())
        .then(data => {
            const simulations = data.success ? data.simulations : data;
            
            if (!simulations || simulations.length === 0) {
                showNotification('No simulation data to export', 'info');
                return;
            }
            
            // Create CSV content
            const headers = [
                'Simulation ID',
                'Started',
                'Completed',
                'Status',
                'Duration (seconds)',
                'Amount (INR)',
                'Qubits',
                'Error Rate',
                'Eavesdropper',
                'Fraud Model',
                'Fraud Sensitivity',
                'Fraud Score',
                'QKD Time (ms)',
                'Encryption Time (ms)',
                'Total Time (seconds)'
            ];
            
            let csvContent = headers.join(',') + '\n';
            
            simulations.forEach(sim => {
                const startTime = new Date(sim.started_at);
                const completionTime = sim.completion_time ? new Date(sim.completion_time) : null;
                const duration = completionTime ? (completionTime - startTime) / 1000 : '';
                
                const row = [
                    sim.id,
                    sim.started_at,
                    sim.completion_time || '',
                    sim.status,
                    duration,
                    sim.config ? (sim.config.amount / 100) : '',
                    sim.config ? sim.config.qubits : '',
                    sim.config ? sim.config.error_rate : '',
                    sim.config ? (sim.config.eavesdropper ? 'Yes' : 'No') : '',
                    sim.config ? sim.config.fraud_model : '',
                    sim.config ? sim.config.fraud_sensitivity : '',
                    sim.transaction_results?.fraud_detection?.risk_score || '',
                    sim.qkd_metrics?.time ? (sim.qkd_metrics.time * 1000) : '',
                    sim.transaction_results?.encryption_time || '',
                    sim.transaction_results?.total_time || ''
                ];
                
                // Escape commas and quotes in data
                const escapedRow = row.map(field => {
                    const stringField = String(field);
                    if (stringField.includes(',') || stringField.includes('"')) {
                        return '"' + stringField.replace(/"/g, '""') + '"';
                    }
                    return stringField;
                });
                
                csvContent += escapedRow.join(',') + '\n';
            });
            
            // Create and trigger download
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement('a');
            const url = URL.createObjectURL(blob);
            link.setAttribute('href', url);
            link.setAttribute('download', `qkd-simulation-history-${new Date().toISOString().split('T')[0]}.csv`);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            showSuccess('History exported successfully!');
        })
        .catch(error => {
            console.error('Error exporting history:', error);
            showError('Failed to export history: ' + error.message);
        });
} 