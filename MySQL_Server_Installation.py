import subprocess

# Download MySQL repository RPM
subprocess.call(["wget", "https://dev.mysql.com/get/mysql80-community-release-el7-9.noarch.rpm"])

# Install MySQL repository 
subprocess.call(["sudo", "rpm", "-ivh", "mysql80-community-release-el7-9.noarch.rpm"])

# Update repositories
subprocess.call(["sudo", "yum", "update", "-y"])

# Install MySQL server
subprocess.call(["sudo", "yum", "install", "mysql-server", "--nogpgcheck", "-y"])

# Start MySQL service
subprocess.call(["sudo", "service", "mysqld", "start"]) 

# Restart to generate new temporary password
subprocess.call(["sudo", "service", "mysqld", "restart"])

# Get temporary password
temp_password = subprocess.check_output(["sudo", "grep", "temporary password", "/var/log/mysqld.log"]).decode('utf-8').split(': ')[-1].strip()

print("Temporary password: ", temp_password)  

# Install expect
subprocess.call(["sudo", "yum", "install", "-y", "expect"])

# Create an expect script
expect_script = f"""spawn sudo mysql_secure_installation

expect "*Enter password for user root:*"
send "{temp_password}\\r"

expect "*New password:*"
send "Omkar@123\\r"

expect "*Re-enter new password:*"
send "Omkar@123\\r"

expect "*Change the password for root ? ((Press y|Y for Yes, any other key for No) :*"
send "n\\r"

expect "*Remove anonymous users? ((Press y|Y for Yes, any other key for No) :*"
send "Y\\r"

expect "*Disallow root login remotely? ((Press y|Y for Yes, any other key for No) :*"
send "Y\\r"

expect "*Remove test database and access to it? ((Press y|Y for Yes, any other key for No) :*"
send "n\\r"

expect "*Reload privilege tables now? ((Press y|Y for Yes, any other key for No) :*"
send "Y\\r"

expect eof"""

with open("secure_mysql.exp", 'w') as f:
    f.write(expect_script)

# Run expect script
subprocess.call(["expect", "./secure_mysql.exp"])

