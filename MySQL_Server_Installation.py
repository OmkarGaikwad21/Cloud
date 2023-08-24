import subprocess

# Download MySQL repository RPM
subprocess.run(["wget", "https://dev.mysql.com/get/mysql80-community-release-el7-9.noarch.rpm"], check=True)

# Install MySQL repository
subprocess.run(["sudo", "rpm", "-ivh", "mysql80-community-release-el7-9.noarch.rpm"], check=True)

# Update repositories
subprocess.run(["sudo", "yum", "update", "-y"], check=True)

# Install MySQL Server
subprocess.run(["sudo", "yum", "install", "mysql-server", "--nogpgcheck", "-y"], check=True)

# Start MySQL service
subprocess.run(["sudo", "systemctl", "start", "mysqld"], check=True)

# Check MySQL service status
subprocess.run(["sudo", "systemctl", "status", "mysqld"], check=True)
