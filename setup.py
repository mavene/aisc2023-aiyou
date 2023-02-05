import subprocess

subprocess.run(["pipenv", "shell"])
subprocess.run(["pipenv", "install", "-r", "requirements.txt"])
subprocess.run(["flask", "run"])