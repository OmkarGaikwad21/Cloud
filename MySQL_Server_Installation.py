import subprocess
import re

# Download MySQL repository RPM
subprocess.run(["wget", "https://dev.mysql.com/get/mysql80-community-release-el7-9.noarch.rpm"], check=True)

# Install MySQL repository
subprocess.run(["sudo", "rpm", "-ivh", "mysql80-community-release-el7-9.noarch.rpm"], check=True)

# Update repositories
subprocess.run(["sudo", "yum", "update", "-y"], check=True)

# Install MySQL Server
subprocess.run(["sudo", "yum", "install", "mysql-server", "-y"], check=True)

# Start MySQL service
subprocess.run(["sudo", "systemctl", "start", "mysqld"], check=True)

# Check MySQL service status
subprocess.run(["sudo", "systemctl", "status", "mysqld"], check=True)

# Get temporary password from the MySQL log
try:
    result = subprocess.run(["sudo", "grep", "A temporary password is generated", "/var/log/mysqld.log"],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
    temp_password = re.search(r"root@localhost: (.+)$", result.stdout, re.MULTILINE).group(1)
except subprocess.CalledProcessError:
    print("Error: Unable to extract temporary password from the log.")
    exit(1)
except AttributeError:
    print("Error: Temporary password not found in the log.")
    exit(1)

# Secure MySQL installation
secure_install_cmd = (
    "echo -e 'Y\\n" + temp_password + "\\nOmkar@123\\nOmkar@123\\nn\\nY\\nY\\nn\\nY' | "
    "sudo mysql_secure_installation"
)
subprocess.run(secure_install_cmd, shell=True, check=True)

print("MySQL setup completed!")
