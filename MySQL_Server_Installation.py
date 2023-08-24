import subprocess

# Install MySQL repository
subprocess.run("wget https://dev.mysql.com/get/mysql80-community-release-el7-9.noarch.rpm", shell=True, check=True)
subprocess.run("sudo rpm -ivh mysql80-community-release-el7-9.noarch.rpm", shell=True, check=True)

# Update and install MySQL Server
subprocess.run("sudo yum update -y", shell=True, check=True)
subprocess.run("sudo yum install mysql-server --nogpgcheck -y", shell=True, check=True)
subprocess.run("sudo systemctl start mysqld", shell=True, check=True)

# Get temporary password
result = subprocess.run("sudo grep 'temporary password' /var/log/mysqld.log", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
temp_password = result.stdout.split()[-1]

# Secure MySQL installation
secure_install_cmd = (
    f"echo -e 'Omkar@123\\nOmkar@123\\n{temp_password}\\nY\\nY\\nY\\nn\\nY' | "
    f"sudo mysql_secure_installation"
)
subprocess.run(secure_install_cmd, shell=True, check=True)

print("MySQL setup completed!")
