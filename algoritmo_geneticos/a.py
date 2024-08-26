import subprocess

def check_graphviz():
    try:
        result = subprocess.run(['dot', '-V'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print(result.stdout.decode())
    except FileNotFoundError:
        print("Graphviz not found. Make sure it's installed and added to PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

check_graphviz()
