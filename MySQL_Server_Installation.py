import subprocess

# Check if the MySQL repository package is already installed
check_installed_cmd = ["rpm", "-q", "mysql80-community-release-el7-9.noarch"]
try:
    subprocess.run(check_installed_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("MySQL repository package is already installed.")
except subprocess.CalledProcessError:
    print("MySQL repository package is not installed. Proceeding with installation...")
    # Install MySQL repository package
    install_cmd = ["sudo", "rpm", "-ivh", "mysql80-community-release-el7-9.noarch.rpm"]
    try:
        subprocess.run(install_cmd, check=True)
        print("MySQL repository package installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing MySQL repository package: {e}")
        exit(1)

# Update and install MySQL Server
update_cmd = ["sudo", "yum", "update", "-y"]
install_mysql_cmd = ["sudo", "yum", "install", "mysql-server", "--nogpgcheck", "-y"]

for cmd in [update_cmd, install_mysql_cmd]:
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {cmd}\nError message: {e}")
        exit(1)

# Start MySQL service
start_mysql_cmd = ["sudo", "systemctl", "start", "mysqld"]
try:
    subprocess.run(start_mysql_cmd, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error starting MySQL service: {e}")
    exit(1)

# Get temporary password
get_temp_pwd_cmd = ["sudo", "grep", "'temporary password'", "/var/log/mysqld.log"]
try:
    result = subprocess.run(get_temp_pwd_cmd, stdout=subprocess.PIPE, text=True)
    temp_password = result.stdout.split()[-1]
    print(f"Temporary password: {temp_password}")
except subprocess.CalledProcessError as e:
    print(f"Error getting temporary password: {e}")
    exit(1)

# Secure MySQL installation
secure_install_cmd = [
    "sudo", "mysql_secure_installation",
    "-p" + temp_password,
    "-e", "Omkar@123",
    "-e", "Omkar@123",
    "-e", "n",
    "-e", "Y", "-e", "Y", "-e", "n", "-e", "Y"
]
try:
    subprocess.run(secure_install_cmd, check=True)
    print("MySQL secure installation completed successfully!")
except subprocess.CalledProcessError as e:
    print(f"Error running secure installation: {e}")
    exit(1)
