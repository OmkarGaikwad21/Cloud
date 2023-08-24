import subprocess

# Stop the MySQL service
subprocess.run("sudo systemctl stop mysqld", shell=True, check=True)

# Start the MySQL service with --skip-grant-tables option
subprocess.run("sudo systemctl set-environment MYSQLD_OPTS='--skip-grant-tables'", shell=True, check=True)
subprocess.run("sudo systemctl start mysqld", shell=True, check=True)

# Update root password
mysql_reset_cmd = [
    "mysql", "-u", "root", "--execute", 
    "ALTER USER 'root'@'localhost' IDENTIFIED BY 'Omkar@123';"
]
subprocess.run(mysql_reset_cmd, check=True)

# Stop the MySQL service
subprocess.run("sudo systemctl stop mysqld", shell=True, check=True)

# Clear the MySQL service environment variable
subprocess.run("sudo systemctl unset-environment MYSQLD_OPTS", shell=True, check=True)

# Start the MySQL service
subprocess.run("sudo systemctl start mysqld", shell=True, check=True)

print("Root password reset successfully!")
