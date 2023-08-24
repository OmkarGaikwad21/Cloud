import subprocess

# Uninstall existing mysql80-community-release
subprocess.run("sudo rpm -e mysql80-community-release", shell=True)

# Download and install v9 release package
subprocess.run("wget https://dev.mysql.com/get/mysql80-community-release-el7-9.noarch.rpm", shell=True, check=True)
subprocess.run("sudo rpm -ivh mysql80-community-release-el7-9.noarch.rpm", shell=True, check=True)

# Update packages
subprocess.run("sudo yum update -y", shell=True, check=True)  

# Install MySQL server
subprocess.run("sudo yum install mysql-server -y", shell=True, check=True)

# Start MySQL service
subprocess.run("sudo systemctl start mysqld", shell=True, check=True)

# Get temporary root password
result = subprocess.run("sudo grep 'temporary password' /var/log/mysqld.log", shell=True, capture_output=True, text=True)
temp_password = result.stdout.split()[3]

# Secure MySQL installation
sql_commands = [
  f"ALTER USER 'root'@'localhost' IDENTIFIED BY 'Omkar@123';",
  "ALTER USER 'root'@'localhost' PASSWORD EXPIRE NEVER;",
  "DROP DATABASE IF EXISTS test;", 
  "FLUSH PRIVILEGES;"
]
subprocess.run("echo '\n'.join(sql_commands) + f' | mysql -u root -p{temp_password}"', shell=True, check=True)

# Create databases and users 
databases = ["scm", "hive", "hue", "rman", "navs", "navms", "oozie", "actmo", "sentry", "ranger"]

for db in databases:
  sql = f"CREATE DATABASE {db} DEFAULT CHARACTER SET utf8;"
  subprocess.run(f"echo '{sql}' | mysql -u root -pOmkar@123", shell=True, check=True)

  sql = f"CREATE USER '{db}'@'%' IDENTIFIED BY 'Omkar@123';"
  subprocess.run(f"echo '{sql}' | mysql -u root -pOmkar@123", shell=True, check=True)

  sql = f"GRANT ALL PRIVILEGES ON {db}.* TO '{db}'@'%';"
  subprocess.run(f"echo '{sql}' | mysql -u root -pOmkar@123", shell=True, check=True)

# Create temp user  
temp_user_sql = """
  CREATE USER 'temp'@'%' IDENTIFIED BY 'Omkar@123';
  GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, RELOAD, PROCESS, REFERENCES, INDEX, ALTER, SHOW DATABASES, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, REPLICATION SLAVE, REPLICATION CLIENT, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, CREATE USER, EVENT, TRIGGER ON *.* TO 'temp'@'%' WITH GRANT OPTION;
"""
subprocess.run(f"echo '{temp_user_sql}' | mysql -u root -pOmkar@123", shell=True, check=True)

print("MySQL setup completed!")
