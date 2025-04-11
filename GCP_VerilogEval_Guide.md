# VerilogEval Environment Setup Guide for GCP VM


<!-- TOC -->

- [VerilogEval Environment Setup Guide for GCP VM](#verilogeval-environment-setup-guide-for-gcp-vm)
    - [1. Overview](#1-overview)
    - [2. Prerequisites](#2-prerequisites)
        - [2.1. Required Components:](#21-required-components)
    - [3. Step 1: Install Conda if not already installed](#3-step-1-install-conda-if-not-already-installed)
    - [4. Step 2: Create and Activate Python Environment](#4-step-2-create-and-activate-python-environment)
    - [5. Step 3: Install Build Dependencies](#5-step-3-install-build-dependencies)
    - [6. Step 4: Install Icarus Verilog iverilog](#6-step-4-install-icarus-verilog-iverilog)
    - [7. Step 5: Install Required Python Packages](#7-step-5-install-required-python-packages)
    - [8. Step 6: Verify Installation](#8-step-6-verify-installation)
    - [9. Step 7: Clone the VerilogEval Repository](#9-step-7-clone-the-verilogeval-repository)
    - [10. Step 8: Run the Evaluation Harness](#10-step-8-run-the-evaluation-harness)
    - [11. Example Execution](#11-example-execution)
    - [12. Troubleshooting](#12-troubleshooting)
        - [12.1. Common Issues and Solutions](#121-common-issues-and-solutions)
    - [13. Notes](#13-notes)

<!-- /TOC -->



## Overview

VerilogEval is an evaluation harness for testing large language models on Verilog code generation tasks. It requires specific versions of tools and dependencies to function correctly.

## Prerequisites

### Required Components:
- Python 3.11
- Conda (for managing Python environments)
- iverilog v12 (not v13)
- Build tools (gcc, g++, make)
- Various development tools (autoconf, gperf, flex, bison)

## Step 1: Install Conda (if not already installed)

```bash
# Download Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh

# Run the installer
bash ~/miniconda.sh

# Follow the prompts and initialize Miniconda when asked
# After installation, refresh your current shell
source ~/.bashrc

# Verify the installation
conda --version
```

## Step 2: Create and Activate Python Environment

```bash
# Create a new conda environment with Python 3.11
conda create -n codex python=3.11

# Activate the environment
conda activate codex
```

## Step 3: Install Build Dependencies

```bash
# Install required development tools
sudo apt-get update
sudo apt-get install -y build-essential g++ autoconf gperf flex bison
```

**Common Issue:** Missing C++ compiler
- Error: `configure: error: C++ preprocessor "/lib/cpp" fails sanity check`
- Solution: Install build-essential and g++ packages

## Step 4: Install Icarus Verilog (iverilog)

```bash
# Clone repository and build from source
git clone https://github.com/steveicarus/iverilog.git
cd iverilog
git checkout v12-branch
sh ./autoconf.sh
./configure
make -j4
sudo make install
```

**Common Issues:**
- Missing autoconf or gperf: Install with `sudo apt-get install autoconf gperf`
- Permission denied during installation: Use `sudo make install` instead of just `make install`
- Failed clone attempt: If a previous attempt failed, remove the directory with `rm -rf iverilog` before trying again

## Step 5: Install Required Python Packages

```bash
pip install langchain langchain-openai langchain-nvidia-ai-endpoints langchain-community
```

## Step 6: Verify Installation

Verify the installations:

```bash
# Check Python version
python --version  # Should output Python 3.11.x

# Check iverilog version
iverilog -v  # Should output Icarus Verilog version 12.x
```

## Step 7: Clone the VerilogEval Repository

```bash
git clone https://github.com/NVlabs/verilog-eval.git
cd verilog-eval
```

## Step 8: Run the Evaluation Harness

```bash
# Create a build directory
mkdir -p build/
cd build/

# Configure the evaluation
../configure --with-task=$task --with-model=$model --with-examples=$shots --with-samples=$samples --with-temperature=$temperature --with-top-p=$top_p

# Run the evaluation
make
```

Where:
- `$task` can be `code-complete-iccad2023` or `spec-to-rtl`
- `$model` is a model from those listed in `scripts/sv-generate`
- `$shots` is the number of in-context learning examples (0-4)
- `$samples` is the number of samples to collect per problem
- `$temperature` and `$top_p` control the model's generation parameters

For faster evaluation, use `make -j4` to run 4 worker processes in parallel.

## Example Execution

Here's an example of running the evaluation with specific parameters:

```bash
mkdir -p build/
cd build/

../configure --with-task=spec-to-rtl --with-model=gpt-4o --with-examples=2 --with-samples=5 --with-temperature=0.8 --with-top-p=0.95

# Run the make utility with up to 4 jobs in parallel
make -j4
```

## Troubleshooting

### Common Issues and Solutions

1. **Missing Dependencies**
   - Error: 
   
      Various build errors during iverilog compilation
   - Solution: 
   
      Ensure all required development packages are installed with:

     ```bash
     sudo apt-get install -y build-essential g++ autoconf gperf flex bison
     ```

2. **Python Package Issues**
   - Error: 
   
      `ImportError: No module named 'langchain'`

   - Solution: 
   
      Ensure you've activated the conda environment and installed all required packages:
     ```bash
     conda activate codex
     pip install langchain langchain-openai langchain-nvidia-ai-endpoints
     ```

3. **iverilog Version Mismatch**
   - Error: 
   
      Unexpected behavior or errors when running the evaluation.

   - Solution: 
   
      Verify you're using iverilog v12:

     ```bash
     iverilog -v
     ```
     If not v12, uninstall the current version and follow Step 4 again

4. **API Keys Required for Models**
   - Error: 
   
      Authentication errors when trying to use language models.
      
   - Solution: 
   
      Ensure you have the appropriate API keys set in your environment variables
     
      file : key_config.json
     ```json
      {
        "openai_api_key": "xxxxxxxx",
        "other_key": "xxxxxxxx"
      }
     ```

5. **Fix for the Makefile**
   - Error: 
   
      An error occurred while executing the make command.

   - Solution: 
   
      Here is an example of how your Makefile might look after adding the SHELL specification:

        ```bash
          # Use bash for shell commands
          SHELL := /bin/bash
          .SHELLFLAGS := -e -o pipefail -c
          
          # ...existing code...
          
          # Test verilog samples
          $(1)_sv_iv_test_bins = \
            $$(patsubst %.sv, %, $$($(1)_sv_samples))
          
          $(1)_sv_iv_test_logs = \
            $$(patsubst %.sv, %-sv-iv-test.log, $$($(1)_sv_samples))
          
          $$($(1)_sv_iv_test_logs) : %-sv-iv-test.log : %.sv $(1)_test.sv $(1)_ref.sv
              @$$(ECHO)  Testing $$(notdir $$*) with iverilog
              -$$(QUIET) $(IVERILOG_COMPILE) -o $$* $$^ \
                         $(REDIRECT_LOG) $$*-sv-iv-test.log
              -$$(QUIET) timeout 30 ./$$* $(REDIRECT_APPEND_LOG) $$@; \
                       if [[ $$? == 124 ]]; then    \
                         echo "TIMEOUT" $(REDIRECT_APPEND_LOG) $$@; \
                       fi
          
          # ...existing code...
        ```

  

## Notes

- iverilog v13 (development release) is not supported
- When cloning the original VerilogEval 1.0 harness, checkout Git branch "release/1.0.0"
- The main branch contains the improved VerilogEvalV2 harness
- For the latest instructions and information, refer to the official VerilogEval repository


By following this guide, you should be able to successfully set up the VerilogEval environment and run the evaluation harness.
