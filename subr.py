import subprocess
p = subprocess.check_output(["ls", "-l"])
print((str(p).split("\n)")))
