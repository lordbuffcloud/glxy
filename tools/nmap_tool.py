import subprocess
import shlex
import re

class NmapTool:
    def __init__(self, timeout=60):
        self.timeout = timeout

    def validate_target(self, target):
        """Validate the target to ensure it's a valid IP or domain."""
        ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        domain_pattern = re.compile(r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.[A-Za-z]{2,6}$")
        
        if ip_pattern.match(target) or domain_pattern.match(target):
            return True
        else:
            return False

    def run_scan(self, target, scan_type="-sS -sV"):
        """Run the Nmap scan with the specified scan type."""
        # Validate the target before running the scan
        if not self.validate_target(target):
            return f"Invalid target: {target}. Please provide a valid IP or domain."

        nmap_command = f"nmap {scan_type} {target}"
        try:
            result = subprocess.run(shlex.split(nmap_command), capture_output=True, timeout=self.timeout)
            output = result.stdout.decode()
            return output if output else "No output from Nmap."
        except subprocess.TimeoutExpired:
            return f"Nmap scan timed out after {self.timeout} seconds."
        except Exception as e:
            return f"An error occurred during Nmap execution: {str(e)}"

