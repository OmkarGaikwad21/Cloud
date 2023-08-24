import subprocess

# Download MySQL repository RPM
subprocess.run(["wget", "https://dev.mysql.com/get/mysql80-community-release-el7-9.noarch.rpm"], check=True)

# Install MySQL repository
subprocess.run(["sudo", "rpm", "-ivh", "mysql80-community-release-el7-9.noarch.rpm"], check=True)

# Update and install MySQL Server
subprocess.run(["sudo", "yum", "update", "-y"], check=True)
subprocess.run(["sudo", "yum", "install", "mysql-server", "--nogpgcheck", "-y"], check=True)

# Start MySQL service
subprocess.run(["sudo", "systemctl", "start", "mysqld"], check=True)

# Check MySQL service status
subprocess.run(["sudo", "systemctl", "status", "mysqld"], check=True)

# Get temporary password
result = subprocess.run(["sudo", "grep", "'temporary password'", "/var/log/mysqld.log"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
temp_password = result.stdout.split()[-1]

# Secure MySQL installation
secure_install_cmd = (
    f"echo -e 'Omkar@123\\nOmkar@123\\n{temp_password}\\nn\\nY\\nY\\nn\\nY' | "
    f"sudo mysql_secure_installation"
)
subprocess.run(secure_install_cmd, shell=True, check=True)

print("MySQL setup completed!")
