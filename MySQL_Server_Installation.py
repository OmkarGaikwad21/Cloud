import os

# Download the MySQL repository
os.system('wget https://dev.mysql.com/get/mysql80-community-release-el7-9.noarch.rpm')

# Install the repository
os.system('sudo rpm -ivh mysql80-community-release-el7-9.noarch.rpm')

# Update the system
os.system('sudo yum update -y')

# Install MySQL Server
os.system('sudo yum install mysql-server --nogpgcheck -y')

# Start the MySQL service
os.system('sudo systemctl start mysqld')

# Check the status of the MySQL service
os.system('sudo systemctl status mysqld')

# Get the temporary password from the log file
with os.popen("sudo grep 'temporary password' /var/log/mysqld.log") as temp_pass:
    temp_password = temp_pass.read().split()[-1]

# Run the secure installation script
os.system(f"sudo mysql_secure_installation <<EOF\n{temp_password}\nOmkar@123\nOmkar@123\nn\nY\nY\nn\nY\nEOF")
