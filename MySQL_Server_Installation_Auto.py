import subprocess

def run_command(command, error_msg):
    try:
        subprocess.check_call(command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {error_msg}")
        print(e.output.decode('utf-8'))
        exit(1)

# Install expect and MySQL repository
run_command("sudo yum install -y expect", "Failed to install 'expect'.")
run_command("wget https://dev.mysql.com/get/mysql80-community-release-el7-9.noarch.rpm", "Failed to download MySQL repository RPM.")
run_command("sudo rpm -ivh mysql80-community-release-el7-9.noarch.rpm", "Failed to install MySQL repository.")
run_command("sudo yum update -y", "Failed to update repositories.")

# Install MySQL server
run_command("sudo yum install mysql-server --nogpgcheck -y", "Failed to install MySQL server.")

# Start MySQL service and get temporary password
run_command("sudo service mysqld start", "Failed to start MySQL service.")
run_command("sudo service mysqld restart", "Failed to restart MySQL service.")
temp_password = subprocess.check_output(["sudo", "grep", "temporary password", "/var/log/mysqld.log"]).decode('utf-8').split(': ')[-1].strip()

print("Temporary password:", temp_password)

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
run_command("expect ./secure_mysql.exp", "Failed to run the expect script.")

# Configure 'hue' user with native authentication
run_command("mysql -u root -p{temp_password} -e \"ALTER USER 'hue'@'%' IDENTIFIED WITH mysql_native_password BY 'Omkar@123';\"", "Failed to configure 'hue' user.")

# Create databases and users
mysql_commands = """
SHOW DATABASES;
CREATE DATABASE scm DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
CREATE USER 'scm'@'%' IDENTIFIED BY 'Omkar@123';
GRANT ALL PRIVILEGES ON scm.* TO 'scm'@'%';

CREATE DATABASE hive DEFAULT CHARACTER SET utf8;
CREATE USER 'hive'@'%' IDENTIFIED BY 'Omkar@123'; 
GRANT ALL PRIVILEGES ON hive.* TO 'hive'@'%';

CREATE DATABASE hue DEFAULT CHARACTER SET utf8;
CREATE USER 'hue'@'%' IDENTIFIED BY 'Omkar@123';
GRANT ALL PRIVILEGES ON hue.* TO 'hue'@'%';

# Add more database and user creation commands here...

SHOW DATABASES;
"""

with open("mysql_commands.sql", "w") as file:
    file.write(mysql_commands)

# Run MySQL commands
run_command(f"mysql -u root -pOmkar@123 < mysql_commands.sql", "Failed to execute MySQL commands.")

print("MySQL commands executed successfully.")
