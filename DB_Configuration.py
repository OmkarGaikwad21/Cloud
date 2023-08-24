import subprocess

# Check if MySQL is running, start if not running
result = subprocess.run("systemctl status mysqld | grep 'active (running)'", shell=True)
if result.returncode != 0:
    subprocess.run("sudo systemctl start mysqld", shell=True, check=True)

# Get temporary password
result = subprocess.check_output("sudo grep 'temporary password' /var/log/mysqld.log", shell=True)  
temp_password = result.decode().strip().split()[-1]

# Secure installation
subprocess.run(f"mysql -u root -p{temp_password} -e 'ALTER USER \\'root\\'@\\'localhost\\' IDENTIFIED BY \\'Omkar@123\\';'", shell=True, check=True)

# Create databases and users
databases = ["scm", "hive", "hue", "rman", "navs", "navms", "oozie", "actmo", "sentry", "ranger"]

for db in databases:
  sql = f"CREATE DATABASE {db} DEFAULT CHARACTER SET utf8; CREATE USER '{db}'@'%' IDENTIFIED BY 'Omkar@123'; GRANT ALL PRIVILEGES ON {db}.* TO '{db}'@'%';"
  subprocess.run(f"mysql -u root -p{temp_password} -e '{sql}'", shell=True, check=True)

# Create temp user 
temp_user_sql = """CREATE USER 'temp'@'%' IDENTIFIED BY 'Omkar@123';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, RELOAD, PROCESS, REFERENCES, INDEX, ALTER, SHOW DATABASES, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, REPLICATION SLAVE, REPLICATION CLIENT, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, CREATE USER, EVENT, TRIGGER ON *.* TO 'temp'@'%' WITH GRANT OPTION;"""
subprocess.run(f"mysql -u root -p{temp_password} -e '{temp_user_sql}'", shell=True, check=True)

print("MySQL configuration completed!")
