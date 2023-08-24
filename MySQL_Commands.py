import subprocess

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

SHOW DATABASES;
"""

# Save the MySQL commands to a file
with open("mysql_commands.sql", "w") as file:
    file.write(mysql_commands)

# Run MySQL commands
subprocess.run(["mysql", "-u", "root", "-p" + mysql_password, "-e", "source mysql_commands.sql"])

print("MySQL commands executed successfully.")

