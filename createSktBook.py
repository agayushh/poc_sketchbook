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
        False, "--template", "-t", help="Create sketchbook with template files"
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
            (sketchbook_path / "main.py").touch()
            (sketchbook_path / "README.md").touch()
            
            # Create a README file
            readme_path = sketchbook_path / "README.md"
            with open(readme_path, "w") as f:
                f.write(f"# {name} Sketchbook\n\n")
                f.write(f"Created on: {datetime.now().strftime('%Y-%m-%d')}\n\n")
                f.write("## Structure\n\n")
                f.write("- **sketches/**: Store your sketch files here\n")
                f.write("- **main.py**: This works as the entry point for sketchbook\n")
               
            
            typer.echo(f" Created template with main.py and README")
    
    except FileExistsError:
        typer.echo(f" Error: Sketchbook '{name}' already exists at {path}", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f" Error creating sketchbook: {str(e)}", err=True)
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
        typer.echo(f" Error listing sketchbooks: {str(e)}", err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()