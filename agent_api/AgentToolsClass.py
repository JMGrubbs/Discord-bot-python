import subprocess
from pydantic import BaseModel
import json


class AgentTools(BaseModel):
    workspace: str
    creations: str

    def __pydantic_fields_set__(self, workspace, creations):
        self.workspace = workspace
        self.creations = creations

    def getjson(string):
        json_object = None
        Error = None
        try:
            json_object = json.loads(string[7:-3])
            return json_object
        except Exception as e:
            Error = str(("JSON ERROR: ", e))

        try:
            json_object = json.loads(string)
            return json_object
        except Exception as e:
            Error = str(("JSON ERROR: ", e))
        return Error

    def write_to_file(file_path, content):
        try:
            with open(file_path, "w") as file:
                file.write(content)
            print(f"Successfully wrote content to {file_path}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def read_file(self, file_path):
        try:
            with open(file_path, "r") as file:
                file_contents = file.read()
                print("File Contents:")
                print(file_contents)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def createNewScript(json_object):
        # Define the code for the new Python script
        new_script_code = json_object.get("code")

        # Define the filename for the new Python script
        filename = json_object.get("filename")

        # Create the new Python script file with the provided code
        with open("tools/creations/" + filename, "w") as file:
            file.write(new_script_code)

        return "tools/creations/" + filename

    def run_scripts(self, json_object):
        result = subprocess.run(
            ["python", "tools/creations/" + json_object.get("filename")],
            capture_output=True,
            text=True,
        )
        # Return the output of the script
        return result.stdout
