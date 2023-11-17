import subprocess
import json

# File name provided by the user
file_name = input("Enter the file name: ")

# Run the provided file and capture the output
try:
    result = subprocess.check_output(["python", file_name], universal_newlines=True)
    output = result.strip()
except subprocess.CalledProcessError as e:
    output = e.output.strip()

# Return the output as a JSON object
print(json.dumps({"output": output}))
