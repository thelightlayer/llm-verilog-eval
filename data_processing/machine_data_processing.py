import os
import json
import re

# Function to create files based on the given conditions
def create_files_from_jsonl(jsonl_file):
    # Read the JSONL file
    with open(jsonl_file, 'r') as file:
        data = file.readlines()

    # Process each JSON object in the file
    for num, line in enumerate(data, start=1):
        # Format num to be three digits long
        num_str = f"{num:03}"

        # Parse the JSON object
        json_obj = json.loads(line)

        # Extract required fields
        task_id = json_obj.get("task_id", "unknown")
        prompt = json_obj.get("prompt", "").replace("module top_module", "module TopModule")
        prompt_ref = json_obj.get("prompt", "").replace("module top_module", "module reference_module")
        canonical_solution = json_obj.get("canonical_solution", "").replace("module top_module", "module TopModule")
        test = json_obj.get("test", "").replace("top_module top_module1", "TopModule top_module1")
        detail_description = json_obj.get("detail_description", "")
        updated_test = remove_reference_module_definition(test)

        # Create file names and content
        file_name_ifc = f"Prob{num_str}_{task_id}_ifc.txt"
        file_name_prompt = f"Prob{num_str}_{task_id}_prompt.txt"
        file_name_ref = f"Prob{num_str}_{task_id}_ref.sv"
        file_name_test = f"Prob{num_str}_{task_id}_test.sv"

        path = "dataset_machine/"

        content_ifc = prompt
        content_prompt = f"{detail_description}\n\n{prompt}"
        content_ref = f"{prompt_ref}{canonical_solution}"
        content_test = updated_test
        

        # Write content to respective files
        with open(path+file_name_ifc, 'w') as f_ifc:
            f_ifc.write(content_ifc)

        with open(path+file_name_prompt, 'w') as f_prompt:
            f_prompt.write(content_prompt)

        with open(path+file_name_ref, 'w') as f_ref:
            f_ref.write(content_ref)

        with open(path+file_name_test, 'w') as f_test:
            f_test.write(content_test)

        print(f"Files created for task_id: {task_id}, num: {num_str}")



def remove_reference_module_definition(content):
    # Split the content into lines
    lines = content.splitlines()

    # Remove the module definition
    inside_reference_module = False
    updated_lines = []
    for line in lines:
        # Detect the start of the reference_module definition
        if re.match(r'\s*module\s+reference_module\b', line):
            inside_reference_module = True
        # Detect the end of the module definition
        if inside_reference_module and re.match(r'\s*endmodule\b', line):
            inside_reference_module = False
            continue  # Skip the endmodule line
        # Skip lines inside the reference_module definition
        if not inside_reference_module:
            updated_lines.append(line)

    return "\n".join(updated_lines)



# Specify the path to the verilogeval-machine.jsonl file
jsonl_file_path = "verilogeval-machine.jsonl"

# Call the function to process the JSONL file and create files
create_files_from_jsonl(jsonl_file_path)


#-------------------------------------------------------------------------
# Output file for the list of problem filenames
#-------------------------------------------------------------------------

# Directory containing the dataset files
dataset_dir = "dataset_machine"

# Output file for the list of problem filenames
output_file = "problems.txt"

# Collect all filenames in the dataset directory
file_names = sorted(os.listdir(dataset_dir))

# Open the output file for writing
with open(output_file, "w") as f:
    for file_name in file_names:
        # Remove the file extension
        base_name = os.path.splitext(file_name)[0]
        
        # Remove the "_ref" suffix if it exists
        if base_name.endswith("_ref"):
            base_name = base_name[:-4]
        
            # Write the modified base name to the output file
            f.write(base_name + "\n")

