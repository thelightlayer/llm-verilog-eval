# Using VerilogEval to Evaluate Closed-Source LLMs
<!-- TOC -->

- [Using VerilogEval to Evaluate Closed-Source LLMs](#using-verilogeval-to-evaluate-closed-source-llms)
    - [1. VerilogEval Project File Structure](#1-verilogeval-project-file-structure)
    - [2. Root Directory: /home/gcp01/verilog-eval](#2-root-directory-homegcp01verilog-eval)
        - [2.1. build](#21-build)
        - [2.2. dataset_code-complete-iccad2023](#22-dataset_code-complete-iccad2023)
        - [2.3. dataset_spec-to-rtl](#23-dataset_spec-to-rtl)
        - [2.4. scripts](#24-scripts)
        - [2.5. .gitignore](#25-gitignore)
        - [2.6. configure](#26-configure)
        - [2.7. configure.ac](#27-configureac)
        - [2.8. count_failures.py](#28-count_failurespy)
        - [2.9. environment.yml](#29-environmentyml)
        - [2.10. key_config.json](#210-key_configjson)
        - [2.11. LICENSE](#211-license)
        - [2.12. Makefile.in](#212-makefilein)
        - [2.13. pass_rate_to_csv.py](#213-pass_rate_to_csvpy)
        - [2.14. README.md](#214-readmemd)
        - [2.15. GCP_VerilogEval_Guide.md](#215-gcp_verilogeval_guidemd)
- [Getting Started](#getting-started)
- [✅ Conda Environment Clone Guide](#-conda-environment-clone-guide)
    - [1. Step 1: Create the Environment on the Target Machine](#1-step-1-create-the-environment-on-the-target-machine)
    - [2. Step 2: Activate the New Environment](#2-step-2-activate-the-new-environment)
- [✅ Usag Evaluation Tool](#-usag-evaluation-tool)
    - [1. Example Execution](#1-example-execution)
- [✅ How to Add a New LLM to VerilogEval](#-how-to-add-a-new-llm-to-verilogeval)
    - [1. Step-by-step Guide to Add a New LLM](#1-step-by-step-guide-to-add-a-new-llm)
        - [1.1. Update the Model Lists in sv-generate](#11-update-the-model-lists-in-sv-generate)
        - [1.2. Add Model Aliases Optional](#12-add-model-aliases-optional)
        - [1.3. Implement the Model Integration](#13-implement-the-model-integration)
        - [1.4. Update the API Key Configuration](#14-update-the-api-key-configuration)
        - [1.5. Running Full Evaluation](#15-running-full-evaluation)
    - [2. 📝 Example : Adding the Anthropic Claude Model](#2--example--adding-the-anthropic-claude-model)

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


## 2. Root Directory: /home/gcp01/verilog-eval

### 2.1. build
- **Description**: Directory for build outputs.

### 2.2. dataset_code-complete-iccad2023
- **Description**: Directory containing datasets for the `code-complete-iccad2023` task.

### 2.3. dataset_spec-to-rtl
- **Description**: Directory containing datasets for the `spec-to-rtl` task.

### 2.4. scripts
- **Description**: Directory containing scripts for various tasks.
  - **sv-generate**: Main script for generating Verilog code from prompts.
    - **Description**: This script processes command-line arguments, loads the API key from a configuration file, and interacts with various models to generate Verilog code.

### 2.5. .gitignore
- **Description**: Git configuration file to specify untracked files to ignore.

### 2.6. configure
- **Description**: Script to configure the build environment.

### 2.7. configure.ac
- **Description**: Autoconf script for generating the `configure` script.

### 2.8. count_failures.py
- **Description**: Python script to count failures in the evaluation results.

### 2.9. environment.yml
- **Description**: Conda environment configuration file.

### 2.10. key_config.json
- **Description**: Configuration file containing the API key for OpenAI.

### 2.11. LICENSE
- **Description**: License file for the project.

### 2.12. Makefile.in
- **Description**: Input file for `make` to generate the `Makefile`.

### 2.13. pass_rate_to_csv.py
- **Description**: Python script to convert pass rates to CSV format.

### 2.14. README.md
- **Description**: Readme file containing an overview and instructions for the project.

### 2.15. GCP_VerilogEval_Guide.md
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

### 1.1. Update the Model Lists in sv-generate`
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

## 2. 📝 Example : Adding the Anthropic Claude Model`

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
