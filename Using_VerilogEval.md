# Using VerilogEval to Evaluate Closed-Source LLMs
<!-- TOC -->

- [Using VerilogEval to Evaluate Closed-Source LLMs](#using-verilogeval-to-evaluate-closed-source-llms)
    - [1. VerilogEval Project File Structure](#1-verilogeval-project-file-structure)
    - [2. Root Directory: /home/gcp01/verilog-eval](#2-root-directory-homegcp01verilog-eval)
        - [2.1. build//](#21-build)
        - [2.2. dataset_code-complete-iccad2023//](#22-dataset_code-complete-iccad2023)
        - [2.3. dataset_spec-to-rtl//](#23-dataset_spec-to-rtl)
        - [2.4. scripts//](#24-scripts)
        - [2.5. .gitignoree](#25-gitignoree)
        - [2.6. configuree](#26-configuree)
        - [2.7. configure.acc](#27-configureacc)
        - [2.8. count_failures.pyy](#28-count_failurespyy)
        - [2.9. environment.ymll](#29-environmentymll)
        - [2.10. key_config.jsonn](#210-key_configjsonn)
        - [2.11. LICENSEE](#211-licensee)
        - [2.12. Makefile.inn](#212-makefileinn)
        - [2.13. pass_rate_to_csv.pyy](#213-pass_rate_to_csvpyy)
        - [2.14. README.mdd](#214-readmemdd)
        - [2.15. GCP_VerilogEval_Guide.mdd](#215-gcp_verilogeval_guidemdd)
- [Getting Started](#getting-started)
- [✅ Conda Environment Clone Guide](#-conda-environment-clone-guide)
    - [1. Step 1: Create the Environment on the Target Machine](#1-step-1-create-the-environment-on-the-target-machine)
    - [2. Step 2: Activate the New Environment](#2-step-2-activate-the-new-environment)
- [✅ Usag Evaluation Tool](#-usag-evaluation-tool)
    - [1. Example Execution](#1-example-execution)
- [✅ How to Add a New LLM to VerilogEval](#-how-to-add-a-new-llm-to-verilogeval)
    - [1. Step-by-step Guide to Add a New LLM](#1-step-by-step-guide-to-add-a-new-llm)
        - [1.1. Update the Model Lists in sv-generatee](#11-update-the-model-lists-in-sv-generatee)
        - [1.2. Add Model Aliases Optional](#12-add-model-aliases-optional)
        - [1.3. Implement the Model Integration](#13-implement-the-model-integration)
        - [1.4. Update the API Key Configuration](#14-update-the-api-key-configuration)
        - [1.5. Running Full Evaluation](#15-running-full-evaluation)
    - [2. 📝 Example : Adding the Anthropic Claude Modell](#2--example--adding-the-anthropic-claude-modell)
- [Tracking Spending](#tracking-spending)
        - [1. GPT-4o OpenAI](#1-gpt-4o-openai)
        - [2. GPT-o1-mini OpenAI CoT](#2-gpt-o1-mini-openai-cot)
        - [3. Claude 3.5 Sonnet Anthropic AI](#3-claude-35-sonnet-anthropic-ai)
        - [4. Claude 3.7 Sonnet Anthropic AI](#4-claude-37-sonnet-anthropic-ai)
        - [5. Perplexity Perplexity AI](#5-perplexity-perplexity-ai)

<!-- /TOC -->
## 1. VerilogEval Project File Structure

```
/home/gcp01/verilog-eval/
├── build/
├── dataset_code-complete-iccad2023/
├── dataset_spec-to-rtl/
├── scripts/
├── .gitignore
├── configure
├── configure.ac
├── count_failures.py
├── environment.yml
├── key_config.json
├── LICENSE
├── Makefile.in
├── pass_rate_to_csv.py
├── README.md
└── VerilogEval_Guide.md
```


## 2. Root Directory: /home/gcp01/verilog-eval`

### 2.1. build//`
- **Description**: Directory for build outputs.

### 2.2. dataset_code-complete-iccad2023//`
- **Description**: Directory containing datasets for the `code-complete-iccad2023` task.

### 2.3. dataset_spec-to-rtl//`
- **Description**: Directory containing datasets for the `spec-to-rtl` task.

### 2.4. scripts//`
- **Description**: Directory containing scripts for various tasks.
  - **sv-generate**: Main script for generating Verilog code from prompts.
    - **Description**: This script processes command-line arguments, loads the API key from a configuration file, and interacts with various models to generate Verilog code.

### 2.5. .gitignoree`
- **Description**: Git configuration file to specify untracked files to ignore.

### 2.6. configuree`
- **Description**: Script to configure the build environment.

### 2.7. configure.acc`
- **Description**: Autoconf script for generating the `configure` script.

### 2.8. count_failures.pyy`
- **Description**: Python script to count failures in the evaluation results.

### 2.9. environment.ymll`
- **Description**: Conda environment configuration file.

### 2.10. key_config.jsonn`
- **Description**: Configuration file containing the API key for OpenAI.

### 2.11. LICENSEE`
- **Description**: License file for the project.

### 2.12. Makefile.inn`
- **Description**: Input file for `make` to generate the `Makefile`.

### 2.13. pass_rate_to_csv.pyy`
- **Description**: Python script to convert pass rates to CSV format.

### 2.14. README.mdd`
- **Description**: Readme file containing an overview and instructions for the project.

### 2.15. GCP_VerilogEval_Guide.mdd`
- **Description**: Guide for setting up and using the VerilogEval environment.


<br><br><br>

# Getting Started

<br>

# ✅ Conda Environment Clone Guide


This guide explains how to clone a Conda environment from one machine to another.



## 1. Step 1: Create the Environment on the Target Machine


On the target machine, create the environment using the exported YAML file:

```bash
conda env create -f ../gcp01/environment.yml
```



## 2. Step 2: Activate the New Environment

Once created, activate the cloned environment:

```bash
conda activate your_environment_name
```

<br>


> **_Export the Environment from the Source Machine:_**  
On the source machine, activate the environment you want to clone and export it to a YAML file:  
$conda activate your_environment_name  
$conda env export > environment.yml

<br><br>

# ✅ Usag Evaluation Tool

```bash
# Create a build directory
mkdir -p build/
cd build/

# Configure the evaluation
/home/gcp01/verilog-eval/configure --with-task=$task --with-model=$model --with-examples=$shots --with-samples=$samples --with-temperature=$temperature --with-top-p=$top_p

# Run the evaluation
make
```

Where:
- `$task` - can be `code-complete-iccad2023` or `spec-to-rtl`
- `$model` - is a model from those listed in `scripts/sv-generate`
- `$shots` - is the number of in-context learning examples (0-4)
- `$samples` - is the number of samples to collect per problem
- `$temperature` - and `$top_p` control the model's generation parameters

For faster evaluation, use `make -j4` to run 4 worker processes in parallel.

## 1. Example Execution

Here's an example of running the evaluation with specific parameters:

```bash
mkdir -p build/
cd build/

/home/gcp01/verilog-eval/configure \
--with-task=code-complete-iccad2023 \
--with-model=gpt-4o \
--with-examples=0 \
--with-samples=10 \
--with-temperature=0.5 \

# Run the make utility with up to 4 jobs in parallel
make -j4
```

<br><br>

# ✅ How to Add a New LLM to VerilogEval

VerilogEval supports multiple LLM providers, including OpenAI and NVIDIA models. Adding a new model requires updating the sv-generate script and potentially implementing new API integrations.

## 1. Step-by-step Guide to Add a New LLM

### 1.1. Update the Model Lists in sv-generatee`
Locate the model list definitions in the `sv-generate` script (around line 80-100):

```python
# ...existing code...

# Add your model to the appropriate list or create a new list
openai_models = [
  "gpt-3.5-turbo",
  "gpt-4",
  "gpt-4-turbo",
  "gpt-4o",
  # Add new OpenAI models here
]

nim_chat_models = [
  "ai-llama2-70b",
  "ai-llama3-70b",
  # ...existing models...
  # Add new NVIDIA models here
]

# Create a new list for your provider if needed
your_provider_models = [
  "your-model-name",
  # Add other models from your provider
]

# Update manual_models if needed
manual_models = [
  'manual-rtl-coder',
  # Add new manual evaluation models here
]
```

### 1.2. Add Model Aliases (Optional)
If your model has alternative names or shorthand versions, add them to the `model_aliases` dictionary:

```python
# ...existing code...

model_aliases = {
  "gpt3.5-turbo" : "gpt-3.5-turbo",
  # ...existing aliases...
  "your-model-alias" : "your-model-name",
}

```


### 1.3. Implement the Model Integration
In the `sv-generate` `main()` function, locate the section where LLM interfaces are initialized and add your model:

around line 253
```python
# ...existing code...

# Add your model to the model checking condition
if model not in openai_models + nim_chat_models + your_provider_models + manual_models:
  print("")
  print(f"ERROR: Unknown model {model}")
  print("")
  return

# ...existing code...
```

around line 362
```python
# Query the LLM

# Add integration code for your provider
if model in openai_models:
  llm = ChatOpenAI(
    # ...existing parameters...
  )
elif model in nim_chat_models:
  llm = ChatNVIDIA(
    # ...existing parameters...
  )
elif model in your_provider_models:
  # Import required libraries at the top of the file
  # from your_provider_library import YourProviderAPI
  
  llm = YourProviderAPI(
    model       = model,
    temperature = temperature,
    top_p       = top_p,
    max_tokens  = max_tokens,
    api_key     = config['your_provider_api_key'],  # Add this to key_config.json
  )
elif model in manual_models:
  # ...existing code...
else:
  # should never reach here
  return

```

### 1.4. Update the API Key Configuration
Add your provider's API key to the `key_config.json` file:


```json
{
  "openai_api_key": "your-openai-key-here",
  "your_provider_api_key": "your-provider-key-here"
}
```

### 1.5. Running Full Evaluation 
Once tested, you can run a full evaluation using the configure script:

```bash
mkdir -p build/
cd build/

/home/gcp01/verilog-eval/configure \
--with-task=code-complete-iccad2023 \
--with-model=your-model-name \
--with-examples=0 \
--with-samples=10 \
--with-temperature=0.5

make -j4

```
<br><br>

## 2. 📝 Example : Adding the Anthropic Claude Modell`

`key_config.json`

```json
{
  "openai_api_key": "your-openai-key-here",
  "anthropic_api_key": "xxxxxxxxxxxx"
}
```
<br>

`sv-generate`  
 
 around line 253

```python

# Add to imports
from langchain_anthropic import ChatAnthropic

# Add to model lists
anthropic_models = [
  "claude-3-opus-20240229",
  "claude-3-sonnet-20240229",
  "claude-3-haiku-20240307"
]
 ```

 around line 362

 
 ```python
# In main()
elif model in anthropic_models:
  llm = ChatAnthropic(
    model       = model,
    temperature = temperature,
    top_p       = top_p,
    max_tokens  = max_tokens,
    api_key     = config['anthropic_api_key'],
  )

  ```

  Be sure to add the necessary dependencies to your environment:

  ```bash
  pip install langchain-anthropic
  ```

<br><br>

# Tracking Spending

Add your LLM to the spending record section to track evaluation costs:

### 1. GPT-4o (OpenAI)
- 0-shot : 
  ```text 
  pass_rate             =      61.67  
  pass_rate(old)        =      72.44  
  avg_gini_simpson_idx  =       0.21  
  total_prompt_tokens   =     412010  
  total_resp_tokens     =     235823  
  total_tokens          =     647833  
  avg_tokens_per_prompt =     264.11  
  avg_tokens_per_resp   =     151.17  
  avg_tokens_per_query  =     415.28  
  total_cost            =       3.38 USD
  used_time             =         40 min
  date                  = 2025.03.19
  ```

- 2-shot :   

  ```text
  pass_rate             =      62.24
  pass_rate(old)        =      71.15
  avg_gini_simpson_idx  =       0.20
  total_prompt_tokens   =     975170
  total_resp_tokens     =     225844
  total_tokens          =    1201014
  avg_tokens_per_prompt =     625.11
  avg_tokens_per_resp   =     144.77
  avg_tokens_per_query  =     769.88
  total_cost            =       4.63 USD
  used_time             =         45 min
  date                  = 2025.03.19   
  ```

### 2. GPT-o1-mini (OpenAI) CoT 
- 0-shot :

  ```text
  pass_rate             =      60.90
  pass_rate(old)        =      76.85
  avg_gini_simpson_idx  =       0.23
  total_prompt_tokens   =     435600
  total_resp_tokens     =    1576654
  total_tokens          =    2012254
  avg_tokens_per_prompt =     279.23
  avg_tokens_per_resp   =    1010.68
  avg_tokens_per_query  =    1289.91
  total_cost            =       8.51 USD
  used_time             =        4.0 hr
  date                  = 2025.03.25   
  ```

- 2-shot : 

  ```text
  pass_rate             =      62.12
  pass_rate(old)        =      75.64
  avg_gini_simpson_idx  =       0.21
  total_prompt_tokens   =    1053360
  total_resp_tokens     =    1855147
  total_tokens          =    2908507
  avg_tokens_per_prompt =     675.23
  avg_tokens_per_resp   =    1189.20
  avg_tokens_per_query  =    1864.43
  total_cost            =       8.51 USD
  used_time             =        5.0 hr   
  date                  = 2025.03.25
  ```


### 3. Claude 3.5 Sonnet (Anthropic AI)
- claude-3-5-sonnet-20241022
- 0-shot : 

  ```text 
  pass_rate             =      64.87
  pass_rate(old)        =      75.00
  avg_gini_simpson_idx  =       0.14
  total_prompt_tokens   =     364578
  total_resp_tokens     =     254158
  total_tokens          =     618736
  avg_tokens_per_prompt =     233.70
  avg_tokens_per_resp   =     162.92
  avg_tokens_per_query  =     396.63
  total_cost            =       4.91 USD
  used_time             =        6.5 hr   
  date                  = 2025.03.28
  ```

- 2-shot : 

  ```text 
  pass_rate             =      23.85
  pass_rate(old)        =      50.00
  avg_gini_simpson_idx  =       0.22
  total_prompt_tokens   =     947093
  total_resp_tokens     =     282962
  total_tokens          =    1230055
  avg_tokens_per_prompt =     607.11
  avg_tokens_per_resp   =     181.39
  avg_tokens_per_query  =     788.50
  total_cost            =       7.09 USD
  used_time             =        8.0 hr   
  date                  = 2025.03.28
  ```

### 4. Claude 3.7 Sonnet (Anthropic AI)
- claude-3-7-sonnet-20250219
- 0-shot : 

  ```text 
  pass_rate             =      53.01
  pass_rate(old)        =      73.08
  avg_gini_simpson_idx  =       0.21
  total_prompt_tokens   =     364970
  total_resp_tokens     =     222836
  total_tokens          =     587806
  avg_tokens_per_prompt =     233.96
  avg_tokens_per_resp   =     142.84
  avg_tokens_per_query  =     376.80
  total_cost            =       4.44 USD
  used_time             =        6.0 hr   
  date                  = 2025.04.01
  ```

- 2-shot : 

  ```text 
  pass_rate             =      35.38
  pass_rate(old)        =      57.69
  avg_gini_simpson_idx  =       0.25
  total_prompt_tokens   =     947640
  total_resp_tokens     =     165911
  total_tokens          =    1113551
  avg_tokens_per_prompt =     607.46
  avg_tokens_per_resp   =     106.35
  avg_tokens_per_query  =     713.81
  total_cost            =       5.33 USD
  used_time             =        5.5 hr   
  date                  = 2025.04.01
  ```

### 4. Perplexity (Perplexity AI)
- Offline Model

- 0-shot : 

  ```text 
  pass_rate             =      53.91
  pass_rate(old)        =      62.82
  avg_gini_simpson_idx  =       0.09
  total_prompt_tokens   =     386080
  total_resp_tokens     =    2149235
  total_tokens          =    2535315
  avg_tokens_per_prompt =     247.49
  avg_tokens_per_resp   =    1377.71
  avg_tokens_per_query  =    1625.20
  total_cost            =      17.97 USD
  used_time             =         10 hr   
  date                  = 2025.03.28
  ```

- 2-shot : 

  ```text 
  pass_rate             =      42.50
  pass_rate(old)        =      64.10
  avg_gini_simpson_idx  =       0.19
  total_prompt_tokens   =     969520
  total_resp_tokens     =    2277794
  total_tokens          =    3247314
  avg_tokens_per_prompt =     621.49
  avg_tokens_per_resp   =    1460.12
  avg_tokens_per_query  =    2081.61
  total_cost            =      20.16 USD
  used_time             =         11 hr   
  date                  = 2025.03.28
  ```
