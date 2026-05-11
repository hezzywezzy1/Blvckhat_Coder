"""Forgeloop Deployer - Full Virtual Linux Desktop Access"""

import time
from typing import Dict, Any, Optional
from e2b import Sandbox

class Deployer:
    """Handles all virtual desktop execution with full access"""

    def __init__(self, api_key: str, persistent: bool = True, memory_gb: int = 8):
        self.api_key = api_key
        self.persistent = persistent
        self.memory_gb = memory_gb
        self.sandbox: Optional[Sandbox] = None
        self.sandbox_id: Optional[str] = None
        self.is_ready = False

    def connect(self) -> bool:
        """Connect to E2B virtual desktop"""
        try:
            self.sandbox = Sandbox(api_key=self.api_key)
            if self.persistent and self.sandbox_id:
                self.sandbox.connect(sandbox_id=self.sandbox_id)
            else:
                self.sandbox_id = self.sandbox.create(template="ubuntu", memory_gb=self.memory_gb)
                self.sandbox.connect(sandbox_id=self.sandbox_id)
            self.is_ready = True
            return True
        except Exception as e:
            print(f"[ERROR] Deployer connection failed: {e}")
            return False

    def execute(self, code: str, language: str = "python", timeout: int = 60) -> Dict[str, Any]:
        """Execute code in virtual desktop"""
        if not self.is_ready:
            self.connect()

        try:
            if language == "python":
                return self._exec_python(code, timeout)
            elif language == "bash":
                return self._exec_bash(code, timeout)
            else:
                return self._exec_bash(code, timeout)
        except Exception as e:
            return {"success": False, "error": str(e), "output": "", "time": 0}

    def _exec_python(self, code: str, timeout: int) -> Dict[str, Any]:
        """Execute Python code"""
        start = time.time()
        temp_file = "/tmp/forgeloop_script.py"
        self.sandbox.run(f"cat > {temp_file} << 'EOF'\n{code}\nEOF")
        result = self.sandbox.run(f"python3 {temp_file}", timeout=timeout)
        return {
            "success": result.exit_code == 0,
            "output": result.stdout,
            "error": result.stderr,
            "time": time.time() - start,
            "language": "python"
        }

    def _exec_bash(self, command: str, timeout: int) -> Dict[str, Any]:
        """Execute bash command"""
        start = time.time()
        result = self.sandbox.run(command, timeout=timeout)
        return {
            "success": result.exit_code == 0,
            "output": result.stdout,
            "error": result.stderr,
            "time": time.time() - start,
            "language": "bash"
        }

    def browse(self, url: str, timeout: int = 30) -> Dict[str, Any]:
        """Browse web in virtual desktop"""
        result = self.sandbox.run(
            f"curl -s -L -A 'Forgeloop/1.0' {url} | head -c 10000",
            timeout=timeout
        )
        return {
            "success": result.exit_code == 0,
            "output": result.stdout,
            "error": result.stderr,
            "time": timeout,
            "url": url
        }

    def upload(self, local_path: str, remote_path: str) -> bool:
        """Upload file to virtual desktop"""
        try:
            with open(local_path, 'r') as f:
                content = f.read()
            cmd = f"cat > {remote_path} << 'EOF'\n{content}\nEOF"
            result = self.sandbox.run(cmd)
            return result.exit_code == 0
        except:
            return False

    def download(self, remote_path: str) -> Optional[str]:
        """Download file from virtual desktop"""
        try:
            result = self.sandbox.run(f"cat {remote_path}")
            return result.stdout if result.exit_code == 0 else None
        except:
            return None

    def get_telemetry(self) -> Dict[str, Any]:
        """Get system telemetry"""
        cpu = self.sandbox.run("top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\\([0-9.]*\\)%* id.*/\\1/' | awk '{print 100 - $1}'")
        mem = self.sandbox.run("free -m | awk 'NR==2{printf \"%.2f%%\", $3*100/$2 }'")
        disk = self.sandbox.run("df -h | awk '$NF==\"/\"{printf \"%s\", $5}'")
        return {
            "cpu": float(cpu.stdout.strip()) if cpu.stdout.strip() else 0,
            "memory": float(mem.stdout.strip().rstrip('%')) if mem.stdout.strip() else 0,
            "disk": disk.stdout.strip() if disk.stdout.strip() else "0%"
        }

    def disconnect(self):
        """Disconnect from virtual desktop"""
        if self.sandbox:
            try:
                self.sandbox.close()
            except:
                pass
        self.is_ready = False
