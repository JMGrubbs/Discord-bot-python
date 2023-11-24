import subprocess
from pydantic import BaseModel
import json


class AgentTools(BaseModel):
    workspace: str
    tools: str

    def __pydantic_fields_set__(self, workspace, tools):
        self.workspace = workspace
        self.tools = tools

    def getjson(self, json_object_string):
        try:
            json_object = json.loads(json_object_string[7:-3])
            return json_object
        except Exception as e:
            Error = str(("JSON ERROR: ", e))

        try:
            json_object = json.loads(json_object_string)
            return json_object
        except Exception as e:
            Error = str(("JSON ERROR: ", e))
        return Error

    def write_to_file(self, file_path, content):
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

    def createNewScript(self, json_object):
        # Define the code for the new Python script
        new_script_code = json_object.get("code")

        # Define the filename for the new Python script
        filename = json_object.get("filename")

        # Create the new Python script file with the provided code
        with open(self.tools + filename, "w") as file:
            file.write(new_script_code)
        return

    def run_tool(self, filename):
        result = subprocess.run(
            ["python", self.tools + filename],
            capture_output=True,
            text=True,
        )
        # Return the output of the script
        return result.stdout

    def run_scripts(self):
        result = subprocess.run(
            ["python", self.workspace + "testing.py"],
            capture_output=True,
            text=True,
        )
        # Return the output of the script
        return result.stdout

    def test_new_script(self, json_object):
        # Define the filename for the new Python script
        filename = json_object.get("filename")

        self.write
        return
