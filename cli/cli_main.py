import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))
from datetime import datetime
from utils.output_handler import OutputHandler

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich import box
from rich.markdown import Markdown

from utils.logger import setup_logger
from utils.file_handler import FileHandler
from engine.lexer import Lexer
from engine.exceptions import SQLError

console = Console()
logger = setup_logger()

# ---------------- UI SCREENS ---------------- #

ASCII_BANNER = r"""
  _____  ____   _      __      __ _ _ _           
 / ____|/ __ \ | |     \ \    / /| | | |          
| (___ | |  | || |      \ \/\/ / | | | |          
 \___ \| |  | || |       \_/\_/  | | | |          
 ____) | |__| || |___               | | |___       
|_____/ \____/ |_____|             |_|_____|      
"""

WELCOME_TEXT = """
Welcome to [bold cyan]SQL Validator[/bold cyan]!

This CLI tool lets you:
- Validate your SQL queries
- Debug and inspect token streams
- Use an interactive SQL shell

Lightweight • Fast • Developer Friendly
"""

def show_welcome():
    console.clear()
    console.print(f"[bold bright_magenta]{ASCII_BANNER}[/bold bright_magenta]")
    console.print(Panel.fit(Markdown(WELCOME_TEXT), border_style="cyan"))


def show_menu():
    menu_table = Table(title="[bold yellow]Main Menu[/bold yellow]", box=box.DOUBLE_EDGE, border_style="magenta")
    menu_table.add_column("Option", justify="center", style="bright_cyan", no_wrap=True)
    menu_table.add_column("Action", justify="left", style="bright_white")

    menu_table.add_row("1", "Validate SQL from text")
    menu_table.add_row("2", "Validate SQL from file")
    menu_table.add_row("3", "Interactive SQL shell")
    menu_table.add_row("4", "Validate multiple queries from file and Generate output files")



    console.print(menu_table)


def show_tokens(tokens):
    table = Table(title="Token Stream", box=box.ROUNDED)
    table.add_column("#", justify="right", style="cyan")
    table.add_column("Token", style="magenta")
    table.add_column("Value", style="green")

    for i, token in enumerate(tokens, start=1):
        table.add_row(str(i), token.type.name, str(token.value))

    console.print(table)
    console.print(Panel.fit("[bold green]✔ Lexing Successful[/bold green]", border_style="green"))


def show_error(err: SQLError):
    console.print(Panel.fit(
        f"[bold red]SQL ERROR[/bold red]\n\n"
        f"Message : {err.msg}\n"
        f"Location : Line {err.line}, Column {err.column}\n"
        f"Hint : {err.detail}",
        border_style="red"
    ))

# ---------------- CORE ENGINE CALL ---------------- #

def run_lexer(source_input: str):
    raw_sql = FileHandler.read(source_input)
    if not raw_sql:
        console.print(Panel.fit("[bold red]Failed to read input[/bold red]", border_style="red"))
        return

    lexer = Lexer(raw_sql)
    tokens = []

    while True:
        token = lexer.get_next_token()

        if isinstance(token, SQLError):
            show_error(token)
            return

        tokens.append(token)

        if token.type.name == "EOF":
            break

    show_tokens(tokens)

# ---------------- MENU ACTIONS ---------------- #

def validate_from_text():
    console.print(Panel.fit("Paste your SQL query below:", border_style="cyan"))
    query = Prompt.ask("SQL")
    run_lexer(query)


def validate_from_file():
    console.print(Panel.fit("Enter file path (.txt or .json):", border_style="cyan"))
    path = Prompt.ask("Path")
    run_lexer(path)


def interactive_shell():
    console.print(Panel.fit("[bold cyan]Interactive SQL Shell[/bold cyan]\nType 'exit' to quit", border_style="cyan"))
    while True:
        query = Prompt.ask("SQL >")
        if query.lower() in ["exit", "quit"]:
            break
        run_lexer(query)



def batch_validate_file():
    console.print(Panel.fit("[bold cyan]Batch SQL Validation[/bold cyan]", border_style="cyan"))
    
    # Input file
    path = Prompt.ask("Enter input file path (.txt or .json)")
    raw_content = FileHandler.read(path)
    if not raw_content:
        console.print("[bold red]Failed to read input file[/bold red]")
        return

    # Extract filename without extension for output naming
    base_name = Path(path).stem

    # Output format
    console.print("Select output format: txt / json / csv / all")
    out_format = Prompt.ask("Format", choices=["txt", "json", "csv", "all"], default="all")

    # Prepare results storage
    results = []
    errors = []

    # Determine queries
    if isinstance(raw_content, str):
        # txt file, one query per line
        queries = [q.strip() for q in raw_content.splitlines() if q.strip()]
    elif isinstance(raw_content, dict):
        # json file, expect "queries" key
        queries = raw_content.get("queries", [])

    # Process each query
    for idx, query in enumerate(queries, start=1):
        lexer = Lexer(query)
        tokens = []

        while True:
            token = lexer.get_next_token()
            if isinstance(token, SQLError):
                errors.append({
                    "query_index": idx,
                    "query": query,
                    "message": token.msg,
                    "line": token.line,
                    "column": token.column,
                    "hint": token.detail
                })
                break
            tokens.append({"type": token.type.name, "value": token.value})
            if token.type.name == "EOF":
                break
        
        if tokens:
            results.append({
                "query_index": idx,
                "query": query,
                "tokens": tokens
            })

    # Save files using input filename as base
    if out_format in ["txt", "all"]:
        OutputHandler.save_txt(f"{base_name}_results.txt",
                               "\n\n".join([f"Query {r['query_index']}:\n{r['query']}\nTokens: {r['tokens']}" for r in results]))
        OutputHandler.save_txt(f"{base_name}_errors.txt",
                               "\n\n".join([f"Query {e['query_index']}:\n{e['query']}\nError: {e['message']}\nLocation: Line {e['line']}, Col {e['column']}\nHint: {e['hint']}" for e in errors]))
    
    if out_format in ["json", "all"]:
        OutputHandler.save_json(f"{base_name}_results.json", results)
        OutputHandler.save_json(f"{base_name}_errors.json", errors)

    if out_format in ["csv", "all"]:
        # Flatten tokens/errors for CSV
        flat_results = []
        for r in results:
            for t in r["tokens"]:
                flat_results.append({"query_index": r["query_index"], "query": r["query"], "token_type": t["type"], "token_value": t["value"]})
        OutputHandler.save_csv(f"{base_name}_results.csv", flat_results)

        flat_errors = []
        for e in errors:
            flat_errors.append({"query_index": e["query_index"], "query": e["query"], "message": e["message"], "line": e["line"], "column": e["column"], "hint": e["hint"]})
        OutputHandler.save_csv(f"{base_name}_errors.csv", flat_errors)

    console.print(Panel.fit(f"[bold green]Batch processing completed![/bold green]\nResults and errors saved in output folder with base name '{base_name}'", border_style="green"))


# ---------------- MAIN APP LOOP ---------------- #

def main():
    show_welcome()

    while True:
        show_menu()
        choice = Prompt.ask("Select option", choices=["1","2","3","4","5"])

        if choice == "1":
            validate_from_text()
        elif choice == "2":
            validate_from_file()
        elif choice == "3":
            interactive_shell()
        elif choice == "4":
            batch_validate_file()
        elif choice == "5":
            console.print(Panel.fit("[bold green]Goodbye 👋[/bold green]", border_style="green"))
            break  # <<< THIS IS THE KEY: stop the loop

        input("\nPress Enter to return to menu...")
        show_welcome()



if __name__ == "__main__":
    main()