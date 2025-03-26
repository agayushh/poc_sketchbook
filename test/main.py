import os
import json
import subprocess
from tag_manager import load_tags, add_tags, remove_tags, get_metadata_path

SKETCH_DIR = "sketches"

def list_sketches():
    """List available sketches."""
    sketches = [f for f in os.listdir(SKETCH_DIR) if f.endswith(".py")]
    
    if not sketches:
        print("⚠️ No sketches found! Add some in the 'sketches/' folder.")
        return []
    
    print("\n📜 Available Sketches:\n")
    for idx, sketch in enumerate(sketches, 1):
        tags = load_tags(sketch)
        tag_display = f"({', '.join(tags)})" if tags else "(No Tags)"
        print(f"{idx}. {sketch} {tag_display}")
    
    return sketches

def get_sketch_args(tags):
    """Prompt user for arguments based on the tags."""
    if not tags:
        return {}

    kwargs = {}
    print("\n🔹 Enter values for the following arguments (press Enter to skip):")

    if "cv" in tags:
        kwargs["cv"] = input("cv (True/False): ").strip() or "False"
        kwargs["camera"] = input("camera (True/False): ").strip() or "False"
        kwargs["device"] = input("device (int): ").strip() or "0"
        kwargs["hands"] = input("hands (True/False): ").strip() or "False"

    if "physics" in tags:
        kwargs["gravity"] = input("gravity (float): ").strip() or "9.8"
        kwargs["friction"] = input("friction (float): ").strip() or "0.1"

    if "AI" in tags:
        kwargs["model"] = input("model (string): ").strip() or "default_model"

    return kwargs

if __name__ == "__main__":
    sketches = list_sketches()
    
    if not sketches:
        exit()

    choice = input("\n🎨 Enter the sketch number to run: ").strip()
    
    try:
        sketch_file = sketches[int(choice) - 1]
        tags = load_tags(sketch_file)

        if not tags:
            print("\n⚠️ No tags found for this sketch.")
            add_tag_choice = input("Would you like to add tags? (yes/no): ").strip().lower()
            if add_tag_choice == "yes":
                add_tags(sketch_file)
                tags = load_tags(sketch_file)  # Reload tags after adding

        # Ask for kwargs if there are tags
        use_kwargs = input("\n🔹 Do you want to enter arguments? (yes/no): ").strip().lower()
        kwargs = get_sketch_args(tags) if use_kwargs == "yes" else {}

        # Construct argument string
        args_str = " ".join(f"--{key} {value}" for key, value in kwargs.items())
        command = f"python {os.path.join(SKETCH_DIR, sketch_file)} {args_str}"

        print(f"\n🚀 Running: {command}")
        subprocess.run(command, shell=True)

    except (IndexError, ValueError):
        print("❌ Invalid choice or file does not exist.")
