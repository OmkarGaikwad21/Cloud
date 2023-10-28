import subprocess

# Install expect
subprocess.call(["sudo", "yum", "install", "-y", "expect"])

# Download MySQL repo RPM
subprocess.call(["wget", "https://dev.mysql.com/get/mysql80-community-release-el7-3.noarch.rpm"]) 

# Install MySQL repository
subprocess.call(["sudo", "rpm", "-ivh", "mysql80-community-release-el7-3.noarch.rpm"])

# Update repositories  
subprocess.call(["sudo", "yum", "update", "-y"])  

# Install MySQL server
subprocess.call(["sudo", "yum", "install", "mysql-server", "-y"])

# Start MySQL service
subprocess.call(["sudo", "systemctl", "start", "mysqld"])  

# Get temporary password
temp_pw = subprocess.check_output(["sudo", "grep", "'temporary password'", "/var/log/mysqld.log"]).decode().split()[-1]
print("Temporary password:", temp_pw)

# Set MySQL root password
mysql_password = "Omkar@123"  

# Create expect script to secure installation 
with open("secure_mysql.exp", "w") as f:
    f.write(f"""
spawn sudo mysql_secure_installation 
expect "Enter password for user root:"
send "{temp_pw}\r"
expect "New password:"  
send "{mysql_password}\r"
expect "Re-enter new password:"
send "{mysql_password}\r"  
expect "Change the password for root ?"
send "n\r"
expect "Remove anonymous users?"
send "Y\r"
expect "Disallow root login remotely?"  
send "Y\r"
expect "Remove test database and access to it?"
send "Y\r"
expect "Reload privilege tables now?"
send "Y\r"
expect eof
""")

subprocess.call(["expect", "./secure_mysql.exp"]) 

# Create databases and users 
db_commands = f"""
CREATE DATABASE scm CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE USER 'scm'@'%' IDENTIFIED BY '{mysql_password}';
GRANT ALL ON scm.* TO 'scm'@'%';

CREATE DATABASE hive CHARACTER SET utf8;  
CREATE USER 'hive'@'%' IDENTIFIED BY '{mysql_password}';
GRANT ALL ON hive.* TO 'hive'@'%';

CREATE DATABASE hue CHARACTER SET utf8;
CREATE USER 'hue'@'%' IDENTIFIED BY '{mysql_password}';
GRANT ALL ON hue.* TO 'hue'@'%';

CREATE DATABASE rman CHARACTER SET utf8;
CREATE USER 'rman'@'%' IDENTIFIED BY '{mysql_password}'; 
GRANT ALL ON rman.* TO 'rman'@'%';

CREATE DATABASE navs CHARACTER SET utf8;
CREATE USER 'navs'@'%' IDENTIFIED BY '{mysql_password}';
GRANT ALL ON navs.* TO 'navs'@'%';  

CREATE DATABASE navms CHARACTER SET utf8;
CREATE USER 'navms'@'%' IDENTIFIED BY '{mysql_password}';
GRANT ALL ON navms.* TO 'navms'@'%';

CREATE DATABASE oozie CHARACTER SET utf8; 
CREATE USER 'oozie'@'%' IDENTIFIED BY '{mysql_password}';
GRANT ALL ON oozie.* TO 'oozie'@'%'; 

CREATE DATABASE actmo CHARACTER SET utf8;
CREATE USER 'actmo'@'%' IDENTIFIED BY '{mysql_password}';
GRANT ALL ON actmo.* TO 'actmo'@'%';

CREATE DATABASE sentry CHARACTER SET utf8;
CREATE USER 'sentry'@'%' IDENTIFIED BY '{mysql_password}';
GRANT ALL ON sentry.* TO 'sentry'@'%';

CREATE DATABASE ranger CHARACTER SET utf8;
CREATE USER 'ranger'@'%' IDENTIFIED BY '{mysql_password}';
GRANT ALL ON ranger.* TO 'ranger'@'%'; 

CREATE USER 'temp'@'%' IDENTIFIED BY '{mysql_password}';  
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, RELOAD, PROCESS, REFERENCES, INDEX, ALTER, SHOW DATABASES, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, REPLICATION SLAVE, REPLICATION CLIENT, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, CREATE USER, EVENT, TRIGGER ON *.* TO 'temp'@'%' WITH GRANT OPTION;
"""

subprocess.run(["mysql", "-u", "root", "-p" + mysql_password], input=db_commands, encoding='utf8')

print("Databases and users created successfully!")