#!/usr/bin/env python3
import pandas as pd
import os

# Create output directory if it doesn't exist
OUTPUT_DIR = 'tables'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Function to generate table with proper LaTeX formatting
def create_table(data, columns, caption, label, column_format):
    """Create a LaTeX table with the given data and formatting"""
    output = []
    output.append("\\begin{table}[!htb]")
    output.append("\\centering")
    output.append("\\small")
    output.append("\\begin{tabular}{" + column_format + "}")
    output.append("\\hline")
    
    # Header row with colored cells
    header_row = []
    for col in columns:
        header_row.append(f"\\cellcolor{{lightblue!30}}\\textbf{{{col}}}")
    output.append(" & ".join(header_row) + " \\\\")
    output.append("\\hline")
    
    # Data rows
    for row in data:
        output.append(" & ".join([str(cell) for cell in row]) + " \\\\")
        output.append("\\hline")
    
    output.append("\\end{tabular}")
    output.append(f"\\caption{{{caption}}}")
    output.append(f"\\label{{{label}}}")
    output.append("\\end{table}")
    
    return "\n".join(output)

# 1. QKD Performance Analysis Table
def generate_qkd_performance_table():
    """Generate QKD Performance Analysis Table"""
    columns = ["Qubits", "Error Rate", "Eavesdropper", "Success Rate", "Avg. Time (s)"]
    data = [
        [500, 0.01, "No", "98\\%", 0.87],
        [1000, 0.01, "No", "97\\%", 1.52],
        [1000, 0.05, "No", "92\\%", 1.54],
        [1000, 0.01, "Yes", "64\\%", 1.67],
        [1000, 0.05, "Yes", "28\\%", 1.71],
        [2000, 0.01, "No", "95\\%", 2.88]
    ]
    
    latex_table = create_table(
        data,
        columns,
        "QKD Performance under Various Conditions",
        "tab:qkd_performance",
        "|c|c|c|c|c|"
    )
    
    with open(f"{OUTPUT_DIR}/qkd_performance.tex", "w") as f:
        f.write(latex_table)
    
    return latex_table

# 2. Feature Engineering Table
def generate_feature_table():
    """Generate Feature Set Table for Neural Network"""
    columns = ["Feature Type", "Description", "Implementation"]
    data = [
        ["Transaction Amount", "Raw monetary value of the transaction", "Min-Max scaled"],
        ["Account Balances", "Original and destination account balances", "Min-Max scaled"],
        ["Derived Features", "\\texttt{amount\\_deducted} and \\texttt{amount\\_credited} calculations", "Computed dynamically"],
        ["Transaction Type", "Mapped from Razorpay payment methods to PaySim transaction types", "One-hot encoded"],
        ["Previous Transactions", "Count and total value of previous transactions", "Exponentially weighted"],
        ["Transaction Velocity", "Rate of transactions over time", "Time-windowed aggregation"],
        ["Transaction Pattern", "Sequence of transaction types and amounts", "LSTM features"]
    ]
    
    latex_table = create_table(
        data,
        columns,
        "Feature Set Used by the Neural Network Fraud Detection Model",
        "table:features",
        "|p{2.8cm}|p{7cm}|p{2.8cm}|"
    )
    
    with open(f"{OUTPUT_DIR}/feature_set.tex", "w") as f:
        f.write(latex_table)
    
    return latex_table

# 3. Payment Method Mapping Table
def generate_payment_mapping_table():
    """Generate Payment Method Mapping Table"""
    columns = ["Razorpay Method", "Mapped Type", "Risk Profile"]
    data = [
        ["Credit Card", "PAYMENT", "Medium-High: Sensitive to fraud"],
        ["Debit Card", "PAYMENT", "Medium: Less risky than credit cards"],
        ["UPI", "CASH\\_IN", "Low-Medium: Fast settlement reduces risk"],
        ["Net Banking", "TRANSFER", "Medium: Bank verification adds security"],
        ["Wallets", "CASH\\_IN", "Low: Typically smaller amounts"],
        ["EMI", "PAYMENT", "High: Extended payment timeline"],
        ["NEFT/RTGS", "TRANSFER", "Medium-High: Large transaction amounts"]
    ]
    
    latex_table = create_table(
        data,
        columns,
        "Mapping from Razorpay Payment Methods to Transaction Types",
        "table:razorpay_mapping",
        "|p{3.5cm}|p{3.5cm}|p{5.5cm}|"
    )
    
    with open(f"{OUTPUT_DIR}/payment_mapping.tex", "w") as f:
        f.write(latex_table)
    
    return latex_table

# 4. Model Comparison Tables
def generate_model_comparison_table():
    """Generate Model Comparison Table"""
    columns = ["Model", "Accuracy", "Precision", "Recall", "F1 Score"]
    data = [
        ["Baseline (Rules-based)", "0.923", "0.892", "0.854", "0.873"],
        ["Neural Network", "0.967", "0.947", "0.932", "0.939"],
        ["QKD-Enhanced Model", "\\textbf{0.982}", "\\textbf{0.975}", "\\textbf{0.968}", "\\textbf{0.971}"]
    ]
    
    latex_table = create_table(
        data,
        columns,
        "Performance Comparison of Fraud Detection Models",
        "table:performance",
        "|p{3.5cm}|c|c|c|c|"
    )
    
    with open(f"{OUTPUT_DIR}/model_comparison.tex", "w") as f:
        f.write(latex_table)
    
    return latex_table

# 5. Fraud Performance Table
def generate_fraud_performance_table():
    """Generate Extended Model Performance Table"""
    columns = ["Model Type", "Accuracy", "Precision", "Recall", "F1 Score", "AUC"]
    data = [
        ["Heuristic", "0.912", "0.276", "0.082", "0.125", "0.652"],
        ["Neural Network (4-layer)", "0.945", "0.344", "0.110", "0.167", "0.710"],
        ["Quantum-enhanced", "0.958", "0.412", "0.134", "0.202", "0.732"]
    ]
    
    latex_table = create_table(
        data,
        columns,
        "Fraud Detection Model Performance Comparison with Latest Metrics",
        "tab:fraud_performance_latest",
        "|c|c|c|c|c|c|"
    )
    
    with open(f"{OUTPUT_DIR}/fraud_performance.tex", "w") as f:
        f.write(latex_table)
    
    return latex_table

# 6. Neural Network Layers Table
def generate_nn_layers_table():
    """Generate Neural Network Layer Architecture Table"""
    columns = ["Layer", "Neurons", "Activation", "Feature Extraction"]
    data = [
        ["Input Layer", "16", "--", "Raw and derived transaction features"],
        ["Hidden Layer 1", "128", "ReLU", "Basic pattern detection"],
        ["Hidden Layer 2", "64", "ReLU", "Complex correlations"],
        ["Hidden Layer 3", "32", "Tanh", "Risk factor analysis"],
        ["Output Layer", "1", "Sigmoid", "Fraud probability"]
    ]
    
    latex_table = create_table(
        data,
        columns,
        "Neural Network Layer Architecture",
        "tab:nn_layers",
        "|c|c|c|p{4.5cm}|"
    )
    
    with open(f"{OUTPUT_DIR}/nn_layers.tex", "w") as f:
        f.write(latex_table)
    
    return latex_table

# 7. Requirements Table
def generate_requirements_table():
    """Generate Requirements and Features Table"""
    columns = ["Requirement", "Description"]
    data = [
        ["Quantum Security Integration", "Implement BB84 protocol for quantum key distribution with error detection and correction"],
        ["Fraud Detection", "Neural network model for identifying fraudulent transactions with >95\\% accuracy"],
        ["Real-time Processing", "Process transactions with latency under 500ms including quantum key generation"],
        ["Scalability", "Handle up to 1000 TPS with linear scaling for additional nodes"],
        ["Visualization", "Interactive dashboard for transaction monitoring and security audit"],
        ["Compliance", "Maintain audit trails and comply with PCI-DSS requirements"]
    ]
    
    latex_table = create_table(
        data,
        columns,
        "Requirements and Features",
        "tab:requirements",
        "|p{4cm}|p{8cm}|"
    )
    
    with open(f"{OUTPUT_DIR}/requirements.tex", "w") as f:
        f.write(latex_table)
    
    return latex_table

# 8. Technical Specifications Table
def generate_tech_specs_table():
    """Generate Technical Specifications Table"""
    columns = ["Component", "Specification"]
    data = [
        ["QKD Module", "BB84 protocol implementation with 1000 qubits per key, 128-bit final key length"],
        ["Encryption Module", "AES-256-GCM for authenticated encryption with quantum-derived keys"],
        ["Fraud Detection Module", "4-layer neural network with 16-128-64-32-1 architecture, trained on PaySim dataset"],
        ["Razorpay Integration", "REST API integration with Razorpay v2.0 endpoints, OAuth 2.0 authentication"],
        ["User Interface", "React-based dashboard with real-time transaction monitoring and alerts"]
    ]
    
    latex_table = create_table(
        data,
        columns,
        "Technical Specifications",
        "tab:tech_spec",
        "|p{4cm}|p{8cm}|"
    )
    
    with open(f"{OUTPUT_DIR}/tech_specs.tex", "w") as f:
        f.write(latex_table)
    
    return latex_table

# Generate all tables and create a combined file
def generate_all_tables():
    """Generate all tables and compile them into a single file"""
    tables = [
        generate_qkd_performance_table(),
        generate_feature_table(),
        generate_payment_mapping_table(),
        generate_model_comparison_table(),
        generate_fraud_performance_table(),
        generate_nn_layers_table(),
        generate_requirements_table(),
        generate_tech_specs_table()
    ]
    
    with open("all_tables.tex", "w") as f:
        f.write("% Auto-generated tables with improved formatting\n\n")
        for table in tables:
            f.write(table)
            f.write("\n\n\\FloatBarrier\n\n")

    print("Generated all tables in the 'tables' directory and combined them in 'all_tables.tex'")
    print("To include these tables in your LaTeX document, you can:")
    print("1. Use the tables individually by including them with \\input{tables/table_name.tex}")
    print("2. Include all tables at once with \\input{all_tables.tex}")

if __name__ == "__main__":
    generate_all_tables() 