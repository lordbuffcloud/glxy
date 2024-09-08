import subprocess

class CodeTool:
    def __init__(self):
        pass

    def execute_code(self, code):
        try:
            # Execute the code in a subprocess
            result = subprocess.run(['python', '-c', code], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                return f"Code executed successfully. Output:\n{result.stdout}"
            else:
                return f"Code execution failed. Error:\n{result.stderr}"
        except subprocess.TimeoutExpired:
            return "Code execution timed out."
        except Exception as e:
            return f"An error occurred: {str(e)}"