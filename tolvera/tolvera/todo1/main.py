import os

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
