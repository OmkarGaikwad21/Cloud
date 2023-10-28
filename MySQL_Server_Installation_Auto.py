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

# Install MySQL server without GPG checks
run_command("sudo yum install mysql-server --nogpgcheck -y", "Failed to install MySQL server.")

# Start MySQL service and get temporary password
run_command("sudo service mysqld start", "Failed to start MySQL service.")
run_command("sudo service mysqld restart", "Failed to restart MySQL service.")
temp_password = subprocess.check_output(["sudo", "grep", "temporary password", "/var/log/mysqld.log"]).decode('utf-8').split(': ')[-1].strip()

print("Temporary password:", temp_password)

# Create an expect script to change MySQL root password
expect_change_password_script = f"""spawn mysql -u root -p

expect "Enter password:"
send "{temp_password}\\r"

expect "mysql>"
send "ALTER USER 'root'@'localhost' IDENTIFIED BY 'New_Password';\\r"

expect "mysql>"
send "\\r"

expect eof
"""

with open("change_mysql_password.exp", 'w') as f:
    f.write(expect_change_password_script)

# Run the expect script to change the MySQL root password
run_command("expect ./change_mysql_password.exp", "Failed to change MySQL root password.")

# MySQL database and user creation commands (replace 'New_Password' and add more as needed)
mysql_commands = """
SHOW DATABASES;
CREATE DATABASE scm DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
CREATE USER 'scm'@'%' IDENTIFIED BY 'New_Password';
GRANT ALL PRIVILEGES ON scm.* TO 'scm'@'%';

CREATE DATABASE hive DEFAULT CHARACTER SET utf8;
CREATE USER 'hive'@'%' IDENTIFIED BY 'New_Password'; 
GRANT ALL PRIVILEGES ON hive.* TO 'hive'@'%';

CREATE DATABASE hue DEFAULT CHARACTER SET utf8;
CREATE USER 'hue'@'%' IDENTIFIED BY 'New_Password';
GRANT ALL PRIVILEGES ON hue.* TO 'hue'@'%';

CREATE DATABASE rman DEFAULT CHARACTER SET utf8;
CREATE USER 'rman'@'%' IDENTIFIED BY 'Omkar@123';
GRANT ALL PRIVILEGES ON rman.* TO 'rman'@'%';

CREATE DATABASE navs DEFAULT CHARACTER SET utf8; 
CREATE USER 'navs'@'%' IDENTIFIED BY 'Omkar@123';
GRANT ALL PRIVILEGES ON navs.* TO 'navs'@'%';

CREATE DATABASE navms DEFAULT CHARACTER SET utf8;
CREATE USER 'navms'@'%' IDENTIFIED BY 'Omkar@123';  
GRANT ALL PRIVILEGES ON navms.* TO 'navms'@'%';

CREATE DATABASE oozie DEFAULT CHARACTER SET utf8;
CREATE USER 'oozie'@'%' IDENTIFIED BY 'Omkar@123';
GRANT ALL PRIVILEGES ON oozie.* TO 'oozie'@'%';

CREATE DATABASE actmo DEFAULT CHARACTER SET utf8;
CREATE USER 'actmo'@'%' IDENTIFIED BY 'Omkar@123'; 
GRANT ALL PRIVILEGES ON actmo.* TO 'actmo'@'%';

CREATE DATABASE sentry DEFAULT CHARACTER SET utf8;
CREATE USER 'sentry'@'%' IDENTIFIED BY 'Omkar@123';
GRANT ALL PRIVILEGES ON sentry.* TO 'sentry'@'%';

CREATE DATABASE ranger DEFAULT CHARACTER SET utf8;
CREATE USER 'ranger'@'%' IDENTIFIED BY 'Omkar@123';
GRANT ALL PRIVILEGES ON ranger.* TO 'ranger'@'%';

SHOW DATABASES;
"""

with open("mysql_commands.sql", "w") as file:
    file.write(mysql_commands)

# Run MySQL commands
run_command(f"mysql -u root -pNew_Password < mysql_commands.sql", "Failed to execute MySQL commands.")

print("MySQL commands executed successfully.")
