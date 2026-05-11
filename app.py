#!/usr/bin/env python3
"""
Forgeloop - CLI Interface
The main entry point with the gangster ASCII mascot
"""

import os
import sys
import asyncio
import logging
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box

# Load environment
load_dotenv()
sys.path.insert(0, str(Path(__file__).parent))

from config import get_config
from deployer import Deployer
from memory import PatternMemory
from loop import Forgeloop

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

console = Console()

# =============================================================================
# ASCII ART - THE GANGSTER MASCOT
# =============================================================================

def get_ascii_art() -> str:
    """Get the Forgeloop ASCII art"""
    return r"""
     ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄
    ███░░░░░░░███ ███░░░░░░░███ ███░░░░░░░███ ███░░░░░░░███
    ███░░████░░███ ███░░█████░░███ ███░░█████░░███ ███░░█████░░███
    ███░░░░░░░███ ███░░░░░░░███ ███░░░░░░░███ ███░░░░░░░███
    ███░░█████░░███ ███████░░█████ ███████░░█████ ███████░░█████
    ███░░░░░░░███ ███░░░░░░░███ ███░░░░░░░███ ███░░░░░░░███
    ███░░████░░███ ███░░█████░░███ ███░░█████░░███ ███░░█████░░███
    ███████░░█████ ███████░░█████ ███████░░█████ ███████░░█████

    ████████████████████████████████████████████████████████████████
    ████████████████████████████████████████████████████████████
    ████████████████████████████████████████████████████████
    ███████████████████████████████████████████████████████
    ██████████████████████████████████████████████████████

    ███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ███░░▄▄▄▄▄░░▄▄▄▄▄░░▄▄▄▄▄░░▄▄▄▄▄░░███░░▄▄▄▄▄░░▄▄▄▄▄░░▄▄▄▄▄░░
    ███░░░░░░░░░░░░░░░░░░░░░░░░░███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ███░░░░░░░░░░░░░░░░░░░░░░░░░███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ███░░▄▄▄▄▄░░▄▄▄▄▄░░▄▄▄▄▄░░▄▄▄▄▄░░███░░▄▄▄▄▄░░▄▄▄▄▄░░▄▄▄▄▄░░
    ███░░░░░░░░░░░░░░░░░░░░░░░░░███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ███░░▄▄▄▄▄░░▄▄▄▄▄░░▄▄▄▄▄░░▄▄▄▄▄░░███░░▄▄▄▄▄░░▄▄▄▄▄░░▄▄▄▄▄░░

    ██████████████████████████████████████████████████████████
    """

def get_mascot() -> str:
    """Get the Forgeloop mascot"""
    return r"""
       ▄▄▄▄▄
      ███░░███
      ███░░███
      ███████
       █████
        ███
    """

# =============================================================================
# FORGELOOP CLI
# =============================================================================

class ForgeloopCLI:
    """Command Line Interface for Forgeloop"""

    def __init__(self):
        self.config = get_config()
        self.deployer = Deployer(
            api_key=self.config["E2B_API_KEY"],
            persistent=self.config["E2B_PERSISTENT"],
            memory_gb=self.config["E2B_MEMORY_GB"]
        )
        self.memory = PatternMemory()
        self.loop = Forgeloop(
            deployer=self.deployer,
            memory=self.memory,
            config=self.config
        )
        self.is_running = False

    def print_header(self):
        """Print the Forgeloop header"""
        if self.config.get("SHOW_ASCII", True):
            console.print(Panel(
                get_ascii_art(),
                title="[bold red]FORGELOOP[/bold red]",
                subtitle="The Mythic Forging Loop",
                border_style="red",
                box=box.DOUBLE
            ))
        console.print("\n[bold white]🔥 FORGELOOP: WHERE CODE BECOMES POWERFUL 🔥[/bold white]\n")

    def print_mascot(self, message: str = ""):
        """Print the mascot with a message"""
        mascot = get_mascot()
        if message:
            console.print(f"{mascot}  [bold]{message}[/bold]")
        else:
            console.print(mascot)

    def interactive_mode(self):
        """Start interactive CLI mode"""
        self.print_header()

        if not self.deployer.connect():
            console.print("[red]✗ Failed to connect to virtual desktop. Check your E2B API key.[/red]")
            return

        console.print("[bold green]Connected to virtual desktop. Type 'help' for commands, 'exit' to quit.[/bold green]\n")

        self.is_running = True

        while self.is_running:
            try:
                # Get user input
                user_input = console.input("[bold red]forgeloop> [/bold red]").strip()

                if not user_input:
                    continue

                # Handle special commands
                if user_input.lower() in ['exit', 'quit', 'q']:
                    console.print("[yellow]Shutting down Forgeloop...[/yellow]")
                    self.deployer.disconnect()
                    self.is_running = False
                    break

                if user_input.lower() in ['help', '?']:
                    self.print_help()
                    continue

                if user_input.lower() in ['clear', 'cls']:
                    console.clear()
                    self.print_header()
                    continue

                if user_input.lower().startswith('mode '):
                    # Mode switching would go here if we had modes
                    console.print("[yellow]Mode switching not yet implemented[/yellow]")
                    continue

                # Process command through the loop
                asyncio.run(self.process_command(user_input))

            except KeyboardInterrupt:
                console.print("\n[yellow]Use 'exit' to quit[/yellow]")
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
                logger.error(f"Command processing error: {e}", exc_info=True)

    async def process_command(self, command: str):
        """Process a user command through the Mythic Forging Loop"""
        console.print(f"\n[bold cyan][INCEPT][/bold cyan] Processing: {command}")

        try:
            # Execute the full loop
            result = await self.loop.execute(command)

            # Display results
            self.display_result(result)

        except Exception as e:
            console.print(f"[red]✗ Loop execution failed: {e}[/red]")
            logger.error(f"Loop execution error: {e}", exc_info=True)

    def display_result(self, result: Dict[str, Any]):
        """Display the result of a command execution"""
        if not result:
            return

        # Display phases
        for phase_name, phase_data in result.get("phases", {}).items():
            if phase_name.startswith("forge"):
                console.print(f"\n[bold yellow][{phase_name.upper()}][/bold yellow]")
                if "code" in phase_data:
                    console.print(Panel(
                        phase_data["code"][:500] + ("..." if len(phase_data["code"]) > 500 else ""),
                        title="[Generated Code]",
                        border_style="yellow",
                        box=box.ROUNDED
                    ))

            elif phase_name.startswith("refinery"):
                console.print(f"\n[bold blue][{phase_name.upper()}][/bold blue]")
                if "optimized_code" in phase_data:
                    console.print(f"Optimization Score: {phase_data.get('optimization_score', 0):.1f}/100")

            elif phase_name.startswith("deploy"):
                console.print(f"\n[bold green][{phase_name.upper()}][/bold green]")

            elif phase_name.startswith("observe"):
                console.print(f"\n[bold magenta][{phase_name.upper()}][/bold magenta]")
                if "observations" in phase_data:
                    obs = phase_data["observations"]
                    console.print(f"Success: {'[green]✓[/green]' if obs['success'] else '[red]✗[/red]'}")
                    console.print(f"Execution Time: {obs['execution_time']:.2f}s")
                    if obs["output_length"] > 0:
                        console.print(f"Output Length: {obs['output_length']} chars")

        # Display best solution
        if result.get("best_solution"):
            best = result["best_solution"]
            console.print("\n[bold white][BEST SOLUTION][/bold white]")
            console.print(Panel(
                best.get("code", "")[:1000],
                title=f"[Solution for: {best.get('intent', 'unknown')}]",
                border_style="white",
                box=box.DOUBLE
            ))

            # Display execution results
            if "execution" in best:
                exec_result = best["execution"]
                if exec_result.get("output"):
                    console.print("\n[bold green][OUTPUT][/bold green]")
                    console.print(Panel(
                        exec_result["output"][:2000],
                        border_style="green",
                        box=box.ROUNDED
                    ))
                if exec_result.get("error"):
                    console.print("\n[bold red][ERROR][/bold red]")
                    console.print(Panel(
                        exec_result["error"][:1000],
                        border_style="red",
                        box=box.ROUNDED
                    ))

        # Display recommendations
        if result.get("best_solution", {}).get("recommendations"):
            console.print("\n[bold cyan][RECOMMENDATIONS][/bold cyan]")
            for i, rec in enumerate(result["best_solution"]["recommendations"], 1):
                console.print(f"  {i}. {rec}")

        # Display telemetry
        if result.get("telemetry"):
            tele = result["telemetry"]
            console.print(f"\n[dim][TELEMETRY] CPU: {tele.get('cpu', 0):.1f}% | Memory: {tele.get('memory', 0):.1f}% | Disk: {tele.get('disk', '0%')}[/dim]")

        console.print()

    def print_help(self):
        """Print help information"""
        help_text = """
[bold]FORGELOOP COMMANDS[/bold]

[cyan]General:[/cyan]
  help, ?          Show this help message
  exit, quit, q    Exit Forgeloop
  clear, cls       Clear the screen

[red]Network:[/red]
  scan <target>              Run nmap scan
  scan <target> --ports <range>  Custom port range
  scan <target> --aggressive    Aggressive scan

[yellow]Exploitation:[/yellow]
  exploit reverse_shell --lhost <ip> --lport <port>  Create reverse shell
  exploit bind_shell --bind_ip <ip> --bind_port <port>  Create bind shell
  metasploit <module>         Run Metasploit module

[green]Financial:[/green]
  generate cc --count <n>     Generate credit card numbers
  generate cc --bank <type>   Specify bank type (visa, mastercard, amex)
  test bypass <url>           Test payment gateway bypass

[blue]Web:[/blue]
  audit <url>                 Audit website
  audit <url> --type sqli     Test for SQL injection
  audit <url> --type xss      Test for XSS

[magenta]Code:[/magenta]
  code <language>             Generate code in language
  run <command>               Execute command directly

[white]System:[/white]
  telemetry                   Show system telemetry
  patterns                    Show stored patterns
"""
        console.print(Panel(
            Text.from_markup(help_text),
            title="[bold]COMMAND REFERENCE[/bold]",
            border_style="white",
            box=box.DOUBLE
        ))

    def run_single_command(self, command: str):
        """Run a single command and exit"""
        self.print_header()

        if not self.deployer.connect():
            console.print("[red]✗ Failed to connect to virtual desktop[/red]")
            sys.exit(1)

        asyncio.run(self.process_command(command))
        self.deployer.disconnect()

# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    """Main entry point"""
    cli = ForgeloopCLI()

    # Check for command-line arguments
    if len(sys.argv) > 1:
        # Run single command
        cli.run_single_command(" ".join(sys.argv[1:]))
    else:
        # Interactive mode
        cli.interactive_mode()

if __name__ == "__main__":
    main()
