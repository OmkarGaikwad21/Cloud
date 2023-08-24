import subprocess

# Step 1: Download and install MySQL repository
subprocess.run(["wget", "https://dev.mysql.com/get/mysql80-community-release-el7-9.noarch.rpm"], check=True)
subprocess.run(["sudo", "rpm", "-ivh", "mysql80-community-release-el7-9.noarch.rpm"], check=True)

# Step 2: Update and install MySQL Server
subprocess.run(["sudo", "yum", "update", "-y"], check=True)
subprocess.run(["sudo", "yum", "install", "mysql-server", "--nogpgcheck", "-y"], check=True)

# Step 3: Start MySQL service
subprocess.run(["sudo", "systemctl", "start", "mysqld"], check=True)

# Step 4: Display MySQL service status
subprocess.run(["sudo", "systemctl", "status", "mysqld"], check=True)

# Step 5: Get temporary password
result = subprocess.run(["sudo", "grep", "temporary password", "/var/log/mysqld.log"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
temp_password = result.stdout.split()[-1]

# Step 6: Secure MySQL installation
secure_install_cmd = f"echo -e 'Omkar@123\\nOmkar@123\\n{temp_password}\\nn\\nY\\nY\\nn\\nY' | sudo mysql_secure_installation"
subprocess.run(secure_install_cmd, shell=True, check=True)

print("MySQL setup completed!")
