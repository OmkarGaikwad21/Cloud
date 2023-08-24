import subprocess

# Step 1: Download MySQL repository
subprocess.run(["wget", "https://dev.mysql.com/get/mysql80-community-release-el7-9.noarch.rpm"], check=True)

# Step 2: Install MySQL repository (only if the older version is not installed)
try:
    subprocess.run(["sudo", "rpm", "-ivh", "mysql80-community-release-el7-9.noarch.rpm"], check=True)
except subprocess.CalledProcessError as e:
    if "is already installed" not in e.stderr:
        raise

# Step 3: Update packages
subprocess.run(["sudo", "yum", "update", "-y"], check=True)

# Step 4: Install MySQL Server
subprocess.run(["sudo", "yum", "install", "mysql-server", "--nogpgcheck", "-y"], check=True)

# Step 5: Start MySQL service
subprocess.run(["sudo", "systemctl", "start", "mysqld"], check=True)

# Step 6: Check MySQL service status
subprocess.run(["sudo", "systemctl", "status", "mysqld"], check=True)

# Step 7: Get temporary password
result = subprocess.run(["sudo", "grep", "'temporary password'", "/var/log/mysqld.log"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
temp_password = result.stdout.split()[-1]

# Step 8: Secure MySQL installation
secure_install_cmd = (
    "echo -e 'Omkar@123\\nOmkar@123\\n{}\\nn\\nY\\nY\\nn\\nY' | "
    "sudo mysql_secure_installation".format(temp_password)
)
subprocess.run(secure_install_cmd, shell=True, check=True)

print("MySQL setup completed!")
