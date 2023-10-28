import subprocess

# Install expect
subprocess.call(["sudo", "yum", "install", "-y", "expect"])

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

mysql_password = "Omkar@123"

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

CREATE USER 'temp'@'%' IDENTIFIED BY 'Omkar@123';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, RELOAD, PROCESS, REFERENCES, INDEX, ALTER, SHOW DATABASES, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, REPLICATION SLAVE, REPLICATION CLIENT, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, CREATE USER, EVENT, TRIGGER ON *.* TO 'temp'@'%' WITH GRANT OPTION;

alter user 'hue'@'%' IDENTIFIED WITH mysql_native_password BY 'Omkar@123';
SHOW DATABASES;
"""

# Save the MySQL commands to a file
with open("mysql_commands.sql", "w") as file:
    file.write(mysql_commands)

# Run MySQL commands
subprocess.run(["mysql", "-u", "root", "-p" + mysql_password], stdin=open('mysql_commands.sql', 'r'))

 

print("MySQL commands executed successfully.")
