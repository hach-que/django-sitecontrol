import subprocess

def run(user, command, cwd):
    return subprocess.Popen([
            "sudo",
            "-u",
            user,
            "/bin/bash",
            "-l",
            "-c",
            command],
        stdin=None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
        cwd=cwd)

