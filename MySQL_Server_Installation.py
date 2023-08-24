import subprocess
import re
import os

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

# Reset MySQL root password
reset_password_script = f"""
ALTER USER 'root'@'localhost' IDENTIFIED BY 'Omkar@123';
FLUSH PRIVILEGES;
"""

reset_password_cmd = "sudo mysql"
subprocess.run(["echo", reset_password_script, "|", reset_password_cmd], shell=True, check=True, executable="/bin/bash")

print("MySQL root password reset completed!")

# Secure MySQL installation
secure_install_script = f"""
Y
n
n
n
n
n
"""

secure_install_cmd = "sudo mysql_secure_installation"
subprocess.run(["echo", secure_install_script, "|", secure_install_cmd], shell=True, check=True, executable="/bin/bash")

print("MySQL setup completed!")
