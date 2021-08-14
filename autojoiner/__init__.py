import subprocess
import platform
import sys


def run_command_windows(cmd):
    cmd = cmd.split()
    output = subprocess.Popen(
        ["powershell", "-Command"] + cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    std_out, std_err = output.communicate()
    std_out, std_err = std_out.decode("utf-8").split("\n"), std_err.decode(
        "utf-8"
    ).split("\n")

    return std_out, std_err


def run_command_linux(cmd):
    cmd = cmd.split()
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    std_out, std_err = output.communicate()
    std_out, std_err = std_out.decode("utf-8").split("\n"), std_err.decode(
        "utf-8"
    ).split("\n")

    return std_out, std_err


def main(command):
    if platform.system() == "Windows":
        return run_command_windows(command)
    else:
        return run_command_linux(command)


if __name__ == "__main__":
    ## testing run_command_linux
    command = sys.argv[1]
    std_out, std_err = main(command)

    for i in std_out:
        print(i)
