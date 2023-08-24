import subprocess

import subprocess

# Step 1: Download MySQL repository configuration files
subprocess.run(["wget", "https://raw.githubusercontent.com/OmkarGaikwad21/Cloud/main/mysql-community.repo"], check=True)
subprocess.run(["wget", "https://raw.githubusercontent.com/OmkarGaikwad21/Cloud/main/mysql-community-source.repo"], check=True)

# Step 2: Move downloaded files to the correct location
subprocess.run(["sudo", "mv", "mysql-community.repo", "/etc/yum.repos.d/"], check=True)
subprocess.run(["sudo", "mv", "mysql-community-source.repo", "/etc/yum.repos.d/"], check=True)

# Step 3: Update packages
subprocess.run(["sudo", "yum", "update", "-y"], check=True)

# Rest of the script remains the same...


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
