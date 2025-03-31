import typer
import os
from pathlib import Path
from typing import Optional
from datetime import datetime

app = typer.Typer(help="Sketchbook CLI: Create and manage your sketchbooks")

@app.command()
def create(
    name: str = typer.Argument(..., help="Name of the sketchbook folder"),
    path: Optional[Path] = typer.Option(
        None, "--path", "-p", help="Path where sketchbook should be created"
    ),
    template: bool = typer.Option(
        True, "--template", "-t", help="Create sketchbook with template files (default: True)"
    )
):
    """
    Create a new sketchbook folder with optional templates.
    """
    # Set default path to current directory if not specified
    if path is None:
        path = Path.cwd()
    
    # Create full path for the sketchbook
    sketchbook_path = path / name
    
    try:
        # Create the main sketchbook directory
        sketchbook_path.mkdir(parents=True, exist_ok=False)
        typer.echo(f"Created sketchbook folder: {sketchbook_path}")
        
        # Create default structure if template is enabled
        if template:
            # Create subdirectories
            (sketchbook_path / "sketches").mkdir()
            (sketchbook_path / "README.md").touch()
            
            
            # Create a README file
            readme_path = sketchbook_path / "README.md"
            with open(readme_path, "w") as f:
                f.write(f"# {name} Sketchbook\n\n")
                f.write(f"Created on: {datetime.now().strftime('%Y-%m-%d')}\n\n")
                f.write("## Structure\n\n")
                f.write("- **sketches/**: Store your sketch files here\n")
                f.write("- **main.py**: Main script to run sketches\n")             
            # Create main.py file
            main_py_path = sketchbook_path / "main.py"
            with open(main_py_path, "w") as f:
                data = '''import os

SKETCH_DIR = "sketches"

def list_sketches():
    """List available sketches."""
    return [f for f in os.listdir(SKETCH_DIR) if f.endswith(".py")]

if __name__ == "__main__":
    sketches = list_sketches()
    
    if not sketches:
        print("⚠️ No sketches found! Add some in the 'sketches/' folder.")
    else:
        print("Available Sketches:")
        for idx, sketch in enumerate(sketches, 1):
            print(f"{idx}. {sketch}")
        
        choice = input("Enter the sketch number to run: ")
        
        try:
            sketch_file = sketches[int(choice) - 1]
            sketch_path = os.path.join(SKETCH_DIR, sketch_file)
            exec(open(sketch_path).read())  # Runs selected sketch
        except (IndexError, ValueError):
            print("Invalid choice. Exiting.")
'''
                f.write(data)
            
            # Create pyproject.toml file
            pyproject_path = sketchbook_path / "pyproject.toml"
            with open(pyproject_path, "w") as f:
                f.write("""[tool.poetry]
name = "tolvera"
version = "0.1.0"
description = "A creative coding environment inspired by Arduino and Processing."
authors = ["Ayush Goyal <your-email@example.com>"]
license = "MIT"

[tool.poetry.dependencies]
python = "^3.8"
pygame = "^2.5.2"
numpy = "^1.26.4"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
""")
            
            typer.echo(f"Created template structure with directories, README, main.py, and pyproject.toml")
    
    except FileExistsError:
        typer.echo(f"Error: Sketchbook '{name}' already exists at {path}", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"Error creating sketchbook: {str(e)}", err=True)
        raise typer.Exit(code=1)

@app.command()
def list(
    path: Optional[Path] = typer.Option(
        None, "--path", "-p", help="Path to look for sketchbooks"
    )
):
    """
    List all sketchbooks in the given directory.
    """
    # Set default path to current directory if not specified
    if path is None:
        path = Path.cwd()
    
    try:
        # Get all directories in the path
        sketchbooks = [d for d in path.iterdir() if d.is_dir()]
        
        if not sketchbooks:
            typer.echo(f"No sketchbooks found in {path}")
            return
        
        typer.echo(f"Found {len(sketchbooks)} sketchbook(s) in {path}:")
        for idx, sketchbook in enumerate(sketchbooks, 1):
            typer.echo(f"{idx}. {sketchbook.name}")
    
    except Exception as e:
        typer.echo(f"Error listing sketchbooks: {str(e)}", err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
