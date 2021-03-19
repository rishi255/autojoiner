import subprocess
def run_command_windows(cmd):
	output = subprocess.Popen(["powershell", "-Command", cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	std_out, std_err = output.communicate()
	return std_out.decode('utf-8').split('\n'), std_err.decode('utf-8').split('\n')

def run_command_linux(cmd):
	# TODO check if this works
	output = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	std_out, std_err = output.communicate()
	return std_out.decode('utf-8').split('\n'), std_err.decode('utf-8').split('\n')