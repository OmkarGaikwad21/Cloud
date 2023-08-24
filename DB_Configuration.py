import subprocess

# Clean up existing MySQL packages and repositories
subprocess.run("sudo yum remove mysql80-community-release", shell=True, check=True)
subprocess.run("sudo yum clean all", shell=True, check=True)

# Download the correct MySQL package
mysql_package_url = "https://dev.mysql.com/get/mysql80-community-release-el7-10.noarch.rpm"
subprocess.run(f"wget {mysql_package_url}", shell=True, check=True)

# Install the MySQL package
subprocess.run("sudo rpm -ivh mysql80-community-release-el7-10.noarch.rpm", shell=True, check=True)

# Update the system
subprocess.run("sudo yum update -y", shell=True, check=True)

# Install MySQL Server
subprocess.run("sudo yum install mysql-server -y", shell=True, check=True)
subprocess.run("sudo systemctl start mysqld", shell=True, check=True)

# Get temporary password
result = subprocess.run("sudo grep 'temporary password' /var/log/mysqld.log", shell=True, capture_output=True, check=True)
temp_password = result.stdout.decode('utf-8').split()[3]

# Secure MySQL installation
sql_commands = [f"{temp_password}", "Omkar@123", "Omkar@123", "n", "Y", "Y", "n", "Y"]
subprocess.run("echo '{}' | sudo mysql_secure_installation".format('\\n'.join(sql_commands)), shell=True, check=True)

# Create databases and users
databases = ["scm", "hive", "hue", "rman", "navs", "navms", "oozie", "actmo", 
             "sentry", "ranger"]

for db in databases:
    sql = f"""
        CREATE DATABASE {db} DEFAULT CHARACTER SET utf8;
        CREATE USER '{db}'@'%' IDENTIFIED BY 'Omkar@123';
        GRANT ALL PRIVILEGES ON {db}.* TO '{db}'@'%';
    """
    subprocess.run(f"echo '{sql}' | mysql -u root -pOmkar@123", shell=True, check=True)

# Create temp user  
subprocess.run("echo 'CREATE USER temp@'%' IDENTIFIED BY 'Omkar@123'; GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, RELOAD, PROCESS, REFERENCES, INDEX, ALTER, SHOW DATABASES, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, REPLICATION SLAVE, REPLICATION CLIENT, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, CREATE USER, EVENT, TRIGGER ON *.* TO 'temp'@'%' WITH GRANT OPTION;' | mysql -u root -pOmkar@123", shell=True, check=True)

print("MySQL setup completed!")
