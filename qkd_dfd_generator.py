#!/usr/bin/env python3
"""
QKD-Razorpay Data Flow Diagram Generator

This script generates TikZ code for multiple levels of data flow diagrams (DFDs)
for the Quantum Key Distribution (QKD) - Razorpay integration project.

The generated TikZ code can be directly included in a LaTeX document for
creating professional data flow diagrams at different levels of abstraction.

Usage:
    python qkd_dfd_generator.py [options]

Options:
    --level0     Generate only Level 0 (Context) DFD
    --level1     Generate only Level 1 DFD
    --level2-qkd Generate only Level 2 DFD for QKD Module
    --level2-enc Generate only Level 2 DFD for Encryption Module
    --level2-rzp Generate only Level 2 DFD for Razorpay Integration
    --level2-web Generate only Level 2 DFD for Web Interface
    --all        Generate all diagrams (default)
    --a4         Optimize for A4 paper size (default)
    --scale=NUM  Set custom scale factor for diagrams (default depends on --a4)
    --output=FILE Write output to FILE instead of stdout
    --help       Show this help message and exit

Without any options, all diagrams will be generated and printed to stdout.
"""

import sys
import argparse

def generate_level0_dfd(scale=0.75):
    """Generate a Level 0 (Context) Data Flow Diagram
    
    Args:
        scale (float): Scale factor for the diagram (for A4 paper)
    """
    output = f"""
% Level 0 (Context) Data Flow Diagram
\\begin{{figure}}[H]
\\centering
\\begin{{tikzpicture}}[
    scale={scale},
    transform shape,
    node distance=3.5cm,
    entity/.style={{rectangle, draw, minimum width=2cm, minimum height=1cm, text centered}},
    process/.style={{circle, draw, minimum width=3cm, minimum height=3cm, text centered}},
    arrow/.style={{thick,->,>=stealth}}
]
    % External entities
    \\node (user) [entity] {{User}};
    \\node (razorpay) [entity, right=7cm of user] {{Razorpay API}};
    
    % Main process
    \\node (system) [process, below=2cm of user, xshift=3.5cm] {{QKD-Razorpay\\\\System}};
    
    % Data flows
    \\draw [arrow] (user) -- node[text width=2cm, midway, above, align=center] {{Configuration\\\\Parameters}} (system);
    \\draw [arrow] (system) -- node[text width=2cm, midway, below, align=center] {{Visualization\\\\Results}} (user);
    
    \\draw [arrow] (system) -- node[text width=2cm, midway, above, align=center] {{Payment\\\\Orders}} (razorpay);
    \\draw [arrow] (razorpay) -- node[text width=2cm, midway, below, align=center] {{Transaction\\\\Data}} (system);

\\end{{tikzpicture}}
\\caption{{Level 0 (Context) Data Flow Diagram showing the QKD-Razorpay system and its external entities}}
\\label{{fig:dfd_level0}}
\\end{{figure}}
"""
    return output

def generate_level1_dfd(scale=0.7):
    """Generate a Level 1 Data Flow Diagram
    
    Args:
        scale (float): Scale factor for the diagram (for A4 paper)
    """
    output = f"""
% Level 1 Data Flow Diagram
\\begin{{figure}}[H]
\\centering
\\begin{{tikzpicture}}[
    scale={scale},
    transform shape,
    node distance=2.7cm,
    entity/.style={{rectangle, draw, minimum width=2cm, minimum height=1cm, text centered}},
    process/.style={{circle, draw, minimum width=2.3cm, minimum height=2.3cm, text centered}},
    datastore/.style={{rectangle, draw, minimum width=2.3cm, text centered, inner sep=8pt}},
    arrow/.style={{thick,->,>=stealth}}
]
    % External entities
    \\node (user) [entity] {{User}};
    \\node (razorpay) [entity, right=13cm of user] {{Razorpay API}};
    
    % Processes
    \\node (web) [process, below=2cm of user, xshift=2cm] {{1.0\\\\Web\\\\Interface}};
    \\node (qkd) [process, right=2.8cm of web] {{2.0\\\\QKD\\\\Module}};
    \\node (encryption) [process, right=2.8cm of qkd] {{3.0\\\\Encryption\\\\Module}};
    \\node (razorpay_int) [process, right=2.8cm of encryption] {{4.0\\\\Razorpay\\\\Integration}};
    
    % Data stores
    \\node (sim_results) [datastore, below=1.8cm of qkd] {{D1: Simulation Results}};
    \\node (keys) [datastore, below=1.8cm of encryption] {{D2: Quantum Keys}};
    
    % Data flows
    \\draw [arrow] (user) -- node[text width=1.8cm, midway, above, sloped, align=center] {{Simulation\\\\Parameters}} (web);
    \\draw [arrow] (web) -- node[text width=1.8cm, midway, above, sloped, align=center] {{QKD\\\\Configuration}} (qkd);
    \\draw [arrow] (qkd) -- node[text width=1.8cm, midway, above, sloped, align=center] {{Quantum\\\\Keys}} (encryption);
    \\draw [arrow] (encryption) -- node[text width=1.8cm, midway, above, sloped, align=center] {{Encrypted\\\\Data}} (razorpay_int);
    \\draw [arrow] (razorpay_int) -- node[text width=1.8cm, midway, above, sloped, align=center] {{Payment\\\\Orders}} (razorpay);
    \\draw [arrow] (razorpay) -- node[text width=1.8cm, midway, above, sloped, align=center] {{Transaction\\\\Data}} (razorpay_int);
    
    % Data store flows
    \\draw [arrow] (qkd) -- node[text width=1.8cm, midway, right, align=center] {{Store\\\\Results}} (sim_results);
    \\draw [arrow] (sim_results) -- node[text width=1.8cm, midway, left, align=center] {{Retrieve\\\\Metrics}} (web);
    
    \\draw [arrow] (qkd) -- node[text width=1.8cm, midway, above, sloped, align=center] {{Store\\\\Keys}} (keys);
    \\draw [arrow] (keys) -- node[text width=1.8cm, midway, above, sloped, align=center] {{Retrieve\\\\Keys}} (encryption);
    
    % Return flows
    \\draw [arrow] (razorpay_int) to[bend right=40] node[text width=1.8cm, midway, below, align=center] {{Payment\\\\Status}} (web);
    \\draw [arrow] (web) to[bend right=40] node[text width=1.8cm, midway, below, align=center] {{Visualization\\\\Results}} (user);

\\end{{tikzpicture}}
\\caption{{Level 1 Data Flow Diagram showing the main processes in the QKD-Razorpay system}}
\\label{{fig:dfd_level1}}
\\end{{figure}}
"""
    return output

def generate_level2_qkd_dfd(scale=0.75):
    """Generate a Level 2 Data Flow Diagram for the QKD Module
    
    Args:
        scale (float): Scale factor for the diagram (for A4 paper)
    """
    output = f"""
% Level 2 Data Flow Diagram for QKD Module
\\begin{{figure}}[H]
\\centering
\\begin{{tikzpicture}}[
    scale={scale},
    transform shape,
    node distance=2.7cm,
    process/.style={{circle, draw, minimum width=2cm, minimum height=2cm, text centered}},
    datastore/.style={{rectangle, draw, minimum width=2.3cm, text centered, inner sep=8pt}},
    arrow/.style={{thick,->,>=stealth}}
]
    % Processes
    \\node (p1) [process] {{2.1\\\\Qubit\\\\Preparation}};
    \\node (p2) [process, right=2.7cm of p1] {{2.2\\\\Quantum\\\\Transmission}};
    \\node (p3) [process, right=2.7cm of p2] {{2.3\\\\Base\\\\Comparison}};
    \\node (p4) [process, below=2.7cm of p2] {{2.4\\\\Error\\\\Detection}};
    \\node (p5) [process, left=2.7cm of p4] {{2.5\\\\Key\\\\Extraction}};
    
    % Data stores
    \\node (d1) [datastore, above=1.8cm of p1] {{D1.1: Alice's Bits \\& Bases}};
    \\node (d2) [datastore, above=1.8cm of p2] {{D1.2: Bob's Bases \\& Results}};
    \\node (d3) [datastore, above=1.8cm of p3] {{D1.3: Matched Bases}};
    \\node (d4) [datastore, below=1.5cm of p5] {{D2: Final Quantum Key}};
    
    % Data flows
    \\draw [arrow] (p1) -- node[text width=2.2cm, midway, above, align=center] {{Quantum\\\\States}} (p2);
    \\draw [arrow] (p2) -- node[text width=2.2cm, midway, above, align=center] {{Measurement\\\\Results}} (p3);
    \\draw [arrow] (p3) -- node[text width=2.2cm, midway, right, align=center] {{Base Matching\\\\Statistics}} (p4);
    \\draw [arrow] (p4) -- node[text width=2.2cm, midway, above, align=center] {{Error Rate\\\\Analysis}} (p5);
    
    % Data store flows
    \\draw [arrow] (p1) -- node[text width=1.8cm, midway, left, align=center] {{Random\\\\Bits \\& Bases}} (d1);
    \\draw [arrow] (p2) -- node[text width=1.8cm, midway, right, align=center] {{Measurement\\\\Data}} (d2);
    \\draw [arrow] (p3) -- node[text width=1.8cm, midway, right, align=center] {{Matched\\\\Indices}} (d3);
    
    \\draw [arrow] (d1) -- node[text width=1.8cm, midway, above, sloped, align=center] {{Alice's\\\\Data}} (p3);
    \\draw [arrow] (d2) -- node[text width=1.8cm, midway, above, sloped, align=center] {{Bob's\\\\Data}} (p3);
    \\draw [arrow] (d3) -- node[text width=1.8cm, midway, above, sloped, align=center] {{Matching\\\\Data}} (p4);
    \\draw [arrow] (d3) -- node[text width=1.8cm, midway, below, sloped, align=center] {{Matching\\\\Data}} (p5);
    
    \\draw [arrow] (p5) -- node[text width=1.8cm, midway, right, align=center] {{Secure\\\\Key}} (d4);
    
    % External input/output arrows
    \\draw [arrow, dashed] (-2,0) -- node[text width=1.8cm, midway, above, align=center] {{Config\\\\Parameters}} (p1);
    \\draw [arrow, dashed] (d4) -- node[text width=1.8cm, midway, below, align=center] {{Key to\\\\Encryption Module}} ($(d4) + (3,0)$);

\\end{{tikzpicture}}
\\caption{{Level 2 Data Flow Diagram for the QKD Module (Process 2.0) showing the BB84 protocol implementation}}
\\label{{fig:dfd_level2_qkd}}
\\end{{figure}}
"""
    return output

def generate_level2_encryption_dfd(scale=0.75):
    """Generate a Level 2 Data Flow Diagram for the Encryption Module
    
    Args:
        scale (float): Scale factor for the diagram (for A4 paper)
    """
    output = f"""
% Level 2 Data Flow Diagram for Encryption Module
\\begin{{figure}}[H]
\\centering
\\begin{{tikzpicture}}[
    scale={scale},
    transform shape,
    node distance=2.7cm,
    process/.style={{circle, draw, minimum width=2cm, minimum height=2cm, text centered}},
    datastore/.style={{rectangle, draw, minimum width=2.3cm, text centered, inner sep=8pt}},
    arrow/.style={{thick,->,>=stealth}}
]
    % Processes
    \\node (p1) [process] {{3.1\\\\Key\\\\Derivation}};
    \\node (p2) [process, right=3.5cm of p1] {{3.2\\\\AES-GCM\\\\Encryption}};
    \\node (p3) [process, below=2.7cm of p1] {{3.3\\\\Data\\\\Formatting}};
    \\node (p4) [process, right=3.5cm of p3] {{3.4\\\\Decryption\\\\Process}};
    
    % Data stores
    \\node (d1) [datastore, above=1.8cm of p1] {{D2.1: Quantum Keys}};
    \\node (d2) [datastore, above=1.8cm of p2] {{D2.2: Derived Keys}};
    \\node (d3) [datastore, below=1.8cm of p3] {{D2.3: Encrypted Data}};
    
    % Data flows
    \\draw [arrow] (p1) -- node[text width=2.2cm, midway, above, align=center] {{Derived\\\\Keys}} (p2);
    \\draw [arrow] (p2) -- node[text width=2.2cm, midway, right, align=center] {{Encrypted\\\\Payload}} (p3);
    \\draw [arrow] (p3) -- node[text width=2.2cm, midway, above, align=center] {{Formatted\\\\Data}} (p4);
    
    % Data store flows
    \\draw [arrow] (d1) -- node[text width=1.8cm, midway, left, align=center] {{Raw\\\\Key}} (p1);
    \\draw [arrow] (p1) -- node[text width=1.8cm, midway, right, align=center] {{Store\\\\Key}} (d2);
    \\draw [arrow] (d2) -- node[text width=1.8cm, midway, right, align=center] {{Retrieve\\\\Key}} (p2);
    \\draw [arrow] (p2) -- node[text width=1.8cm, midway, right, align=center] {{Store\\\\Ciphertext}} (d3);
    \\draw [arrow] (d3) -- node[text width=1.8cm, midway, left, align=center] {{Retrieve\\\\Ciphertext}} (p3);
    \\draw [arrow] (d2) -- node[text width=1.8cm, midway, above, sloped, align=center] {{Retrieval for\\\\Decryption}} (p4);
    
    % External input/output arrows
    \\draw [arrow, dashed] (-2,1) -- node[text width=1.8cm, midway, above, align=center] {{Quantum\\\\Key}} (p1);
    \\draw [arrow, dashed] (0,-3) -- node[text width=1.8cm, midway, left, align=center] {{Payment\\\\Data}} (p3);
    \\draw [arrow, dashed] (p2) -- node[text width=1.8cm, midway, above, align=center] {{To Razorpay\\\\Integration}} ($(p2) + (3.5,0)$);
    \\draw [arrow, dashed] (p4) -- node[text width=1.8cm, midway, right, align=center] {{Decrypted\\\\Data}} ($(p4) + (0,-2)$);

\\end{{tikzpicture}}
\\caption{{Level 2 Data Flow Diagram for the Encryption Module (Process 3.0) showing how payment data is secured}}
\\label{{fig:dfd_level2_encryption}}
\\end{{figure}}
"""
    return output

def generate_level2_razorpay_dfd(scale=0.75):
    """Generate a Level 2 Data Flow Diagram for the Razorpay Integration Module
    
    Args:
        scale (float): Scale factor for the diagram (for A4 paper)
    """
    output = f"""
% Level 2 Data Flow Diagram for Razorpay Integration
\\begin{{figure}}[H]
\\centering
\\begin{{tikzpicture}}[
    scale={scale},
    transform shape,
    node distance=2.7cm,
    process/.style={{circle, draw, minimum width=2cm, minimum height=2cm, text centered}},
    datastore/.style={{rectangle, draw, minimum width=2.3cm, text centered, inner sep=8pt}},
    entity/.style={{rectangle, draw, minimum width=2cm, minimum height=1cm, text centered}},
    arrow/.style={{thick,->,>=stealth}}
]
    % External entity
    \\node (razorpay) [entity] {{Razorpay API}};
    
    % Processes
    \\node (p1) [process, below=2.5cm of razorpay] {{4.1\\\\Order\\\\Creation}};
    \\node (p2) [process, left=3.5cm of p1] {{4.2\\\\Payment\\\\Link Gen}};
    \\node (p3) [process, below=2.7cm of p1] {{4.3\\\\Payment\\\\Verification}};
    \\node (p4) [process, left=3.5cm of p3] {{4.4\\\\Transaction\\\\Management}};
    
    % Data stores
    \\node (d1) [datastore, below=1.5cm of p2] {{D3.1: Order Data}};
    \\node (d2) [datastore, right=1.8cm of d1] {{D3.2: Payment Data}};
    
    % Data flows
    \\draw [arrow] (p1) -- node[text width=2.2cm, midway, above, align=center] {{Order\\\\Details}} (p2);
    \\draw [arrow] (p1) -- node[text width=2.2cm, midway, right, align=center] {{Order\\\\ID}} (p3);
    \\draw [arrow] (p3) -- node[text width=2.2cm, midway, above, align=center] {{Verification\\\\Result}} (p4);
    
    % External entity flows
    \\draw [arrow] (p1) -- node[text width=1.8cm, midway, right, align=center] {{Create\\\\Order}} (razorpay);
    \\draw [arrow] (razorpay) -- node[text width=1.8cm, midway, left, align=center] {{Order\\\\Response}} (p1);
    \\draw [arrow] (p3) -- node[text width=2.2cm, midway, below, sloped, align=center] {{Verify\\\\Signature}} (razorpay);
    \\draw [arrow] (razorpay) -- node[text width=2.2cm, midway, above, sloped, align=center] {{Signature\\\\Validity}} (p3);
    
    % Data store flows
    \\draw [arrow] (p1) -- node[text width=1.8cm, midway, above, sloped, align=center] {{Store\\\\Order}} (d1);
    \\draw [arrow] (p3) -- node[text width=1.8cm, midway, below, sloped, align=center] {{Store\\\\Payment}} (d2);
    \\draw [arrow] (d1) -- node[text width=1.8cm, midway, left, align=center] {{Order\\\\Info}} (p4);
    \\draw [arrow] (d2) -- node[text width=1.8cm, midway, above, sloped, align=center] {{Payment\\\\Info}} (p4);
    
    % External input/output arrows
    \\draw [arrow, dashed] (-4.5,0) -- node[text width=1.8cm, midway, above, align=center] {{Encrypted\\\\Data}} (p2);
    \\draw [arrow, dashed] (p4) -- node[text width=1.8cm, midway, left, align=center] {{Transaction\\\\Result}} ($(p4) + (0,-2)$);
    \\draw [arrow, dashed] (p2) -- node[text width=2.2cm, midway, above, align=center] {{Payment\\\\Link}} ($(p2) + (-2.7,0)$);

\\end{{tikzpicture}}
\\caption{{Level 2 Data Flow Diagram for the Razorpay Integration Module (Process 4.0)}}
\\label{{fig:dfd_level2_razorpay}}
\\end{{figure}}
"""
    return output

def generate_level2_web_dfd(scale=0.75):
    """Generate a Level 2 Data Flow Diagram for the Web Interface Module
    
    Args:
        scale (float): Scale factor for the diagram (for A4 paper)
    """
    output = f"""
% Level 2 Data Flow Diagram for Web Interface
\\begin{{figure}}[H]
\\centering
\\begin{{tikzpicture}}[
    scale={scale},
    transform shape,
    node distance=2.7cm,
    process/.style={{circle, draw, minimum width=2cm, minimum height=2cm, text centered}},
    datastore/.style={{rectangle, draw, minimum width=2.3cm, text centered, inner sep=8pt}},
    entity/.style={{rectangle, draw, minimum width=2cm, minimum height=1cm, text centered}},
    arrow/.style={{thick,->,>=stealth}}
]
    % External entity
    \\node (user) [entity] {{User}};
    
    % Processes
    \\node (p1) [process, below=2.2cm of user] {{1.1\\\\Configuration\\\\Handler}};
    \\node (p2) [process, right=3.5cm of p1] {{1.2\\\\Simulation\\\\Controller}};
    \\node (p3) [process, below=2.7cm of p1] {{1.3\\\\Visualization\\\\Generator}};
    \\node (p4) [process, right=3.5cm of p3] {{1.4\\\\Result\\\\Presenter}};
    
    % Data stores
    \\node (d1) [datastore, below=1.5cm of p2] {{D4.1: Simulation Status}};
    \\node (d2) [datastore, right=1.8cm of d1] {{D4.2: Visualization Data}};
    
    % Data flows
    \\draw [arrow] (p1) -- node[text width=2.2cm, midway, above, align=center] {{Simulation\\\\Parameters}} (p2);
    \\draw [arrow] (p2) -- node[text width=2.2cm, midway, left, align=center] {{Simulation\\\\Data}} (p3);
    \\draw [arrow] (p3) -- node[text width=2.2cm, midway, above, align=center] {{Visual\\\\Output}} (p4);
    
    % External entity flows
    \\draw [arrow] (user) -- node[text width=1.8cm, midway, left, align=center] {{User\\\\Input}} (p1);
    \\draw [arrow] (p4) -- node[text width=1.8cm, midway, right, align=center] {{Display\\\\Results}} (user);
    
    % Data store flows
    \\draw [arrow] (p2) -- node[text width=1.8cm, midway, right, align=center] {{Store\\\\Status}} (d1);
    \\draw [arrow] (p3) -- node[text width=1.8cm, midway, below, sloped, align=center] {{Store\\\\Visuals}} (d2);
    \\draw [arrow] (d1) -- node[text width=1.8cm, midway, above, sloped, align=center] {{Status\\\\Data}} (p4);
    \\draw [arrow] (d2) -- node[text width=1.8cm, midway, right, align=center] {{Visual\\\\Data}} (p4);
    
    % External input/output arrows
    \\draw [arrow, dashed] (p2) -- node[text width=1.8cm, midway, above, align=center] {{To QKD\\\\Module}} ($(p2) + (2.7,0)$);
    \\draw [arrow, dashed] ($(p4) + (2.7,0)$) -- node[text width=1.8cm, midway, above, align=center] {{From Other\\\\Modules}} (p4);

\\end{{tikzpicture}}
\\caption{{Level 2 Data Flow Diagram for the Web Interface Module (Process 1.0)}}
\\label{{fig:dfd_level2_web}}
\\end{{figure}}
"""
    return output

def generate_a4_layout_preamble():
    """Generate additional LaTeX code to help with A4 page layout"""
    output = """
% A4 Page Layout Settings
% Add these to your LaTeX document preamble for better A4 page layout with diagrams

\\usepackage[a4paper, margin=2.5cm]{geometry}  % Set margins for A4 paper
\\usepackage{float}                           % For better figure placement
\\floatstyle{boxed}                           % Optional: Add boxes around figures
\\restylefloat{figure}

% For multi-page diagrams, consider adding:
\\usepackage{pdflscape}                       % For landscape pages
% \\usepackage{afterpage}                       % For isolated landscape pages

% To ensure diagrams fit properly, consider adding:
\\renewcommand{\\floatpagefraction}{0.85}      % Require fuller float pages
\\renewcommand{\\textfraction}{0.1}           % Allow more space to floats
"""
    return output

def generate_latex_preamble():
    """Generate LaTeX preamble with required packages"""
    output = """
% Required LaTeX packages for Data Flow Diagrams
% Add these to your LaTeX document preamble if not already included

\\usepackage{tikz}
\\usepackage{float}
\\usetikzlibrary{arrows,shapes,positioning,calc}

% The following DFD styles can be added to your document preamble for consistent styling
\\tikzset{
    entity/.style={rectangle, draw, minimum width=2cm, minimum height=1cm, text centered},
    process/.style={circle, draw, minimum width=2.5cm, minimum height=2.5cm, text centered},
    datastore/.style={rectangle, draw, minimum width=2.5cm, text centered, inner sep=8pt},
    arrow/.style={thick,->,>=stealth}
}
"""
    return output

def generate_usage_instructions():
    """Generate usage instructions for the LaTeX diagrams"""
    output = """
% -------------------------------------------------------------
% USAGE INSTRUCTIONS
% -------------------------------------------------------------
% 
% 1. Add the required packages to your LaTeX document preamble:
%    \\usepackage{tikz}
%    \\usepackage{float}
%    \\usetikzlibrary{arrows,shapes,positioning,calc}
% 
% 2. For A4 paper optimization, add:
%    \\usepackage[a4paper, margin=2.5cm]{geometry}
%
% 3. Copy the desired diagram code into your document where you want it to appear
% 
% 4. Make sure your document class supports figures and captions
% 
% 5. Compile your LaTeX document with pdfLaTeX or similar
% 
% Note: These diagrams work best with:
%  - IEEE conference class (IEEEtran) 
%  - Article class
%  - Report class
% 
% To adjust diagram sizes:
%  - Modify the scale parameter in the tikzpicture environment
%  - Adjust the 'minimum width' and 'minimum height' parameters
%  - Change node distances in the 'node distance=' parameter
%
% If diagrams still don't fit properly on A4:
%  - Try landscape orientation for specific diagrams:
%    \\begin{landscape}
%      [diagram code here]
%    \\end{landscape}
% -------------------------------------------------------------
"""
    return output

def main():
    """Main function to parse command line arguments and generate diagrams"""
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Generate TikZ code for Data Flow Diagrams (DFDs) for QKD-Razorpay project'
    )
    parser.add_argument('--level0', action='store_true', help='Generate only Level 0 DFD')
    parser.add_argument('--level1', action='store_true', help='Generate only Level 1 DFD')
    parser.add_argument('--level2-qkd', action='store_true', help='Generate only Level 2 DFD for QKD Module')
    parser.add_argument('--level2-enc', action='store_true', help='Generate only Level 2 DFD for Encryption Module')
    parser.add_argument('--level2-rzp', action='store_true', help='Generate only Level 2 DFD for Razorpay Integration')
    parser.add_argument('--level2-web', action='store_true', help='Generate only Level 2 DFD for Web Interface')
    parser.add_argument('--all', action='store_true', help='Generate all diagrams')
    parser.add_argument('--a4', action='store_true', help='Optimize for A4 paper size', default=True)
    parser.add_argument('--scale', type=float, help='Set custom scale factor for diagrams')
    parser.add_argument('--output', metavar='FILE', help='Write output to FILE instead of stdout')
    parser.add_argument('--preamble', action='store_true', help='Include LaTeX preamble code')
    parser.add_argument('--a4-layout', action='store_true', help='Include A4 layout optimization code')
    parser.add_argument('--instructions', action='store_true', help='Include usage instructions')
    
    # Parse arguments
    args = parser.parse_args()

    # If no specific diagram is requested, generate all
    generate_all = (not any([args.level0, args.level1, args.level2_qkd, 
                             args.level2_enc, args.level2_rzp, args.level2_web])
                    or args.all)
                    
    # Determine scale factor
    scale = args.scale if args.scale is not None else (0.75 if args.a4 else 1.0)

    # Output file handling
    if args.output:
        output_file = open(args.output, 'w')
    else:
        output_file = sys.stdout

    # Write header
    output_file.write("% QKD-Razorpay Data Flow Diagrams\n")
    output_file.write(f"% Generated by qkd_dfd_generator.py (optimized for {'A4 paper' if args.a4 else 'standard paper'}, scale={scale})\n\n")

    # Generate preamble if requested
    if args.preamble:
        output_file.write(generate_latex_preamble())
        output_file.write("\n")
        
    # Generate A4 layout optimization if requested
    if args.a4_layout:
        output_file.write(generate_a4_layout_preamble())
        output_file.write("\n")

    # Generate diagrams based on arguments
    if args.level0 or generate_all:
        output_file.write(generate_level0_dfd(scale=scale))
        output_file.write("\n")
    
    if args.level1 or generate_all:
        output_file.write(generate_level1_dfd(scale=scale))
        output_file.write("\n")
    
    if args.level2_qkd or generate_all:
        output_file.write(generate_level2_qkd_dfd(scale=scale))
        output_file.write("\n")
    
    if args.level2_enc or generate_all:
        output_file.write(generate_level2_encryption_dfd(scale=scale))
        output_file.write("\n")
    
    if args.level2_rzp or generate_all:
        output_file.write(generate_level2_razorpay_dfd(scale=scale))
        output_file.write("\n")
    
    if args.level2_web or generate_all:
        output_file.write(generate_level2_web_dfd(scale=scale))
        output_file.write("\n")

    # Generate usage instructions if requested
    if args.instructions:
        output_file.write(generate_usage_instructions())
        output_file.write("\n")

    # Close output file if not stdout
    if args.output:
        output_file.close()
        print(f"Generated diagrams written to {args.output}")
        if args.a4:
            print(f"Diagrams optimized for A4 paper with scale factor {scale}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 