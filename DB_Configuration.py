import subprocess

# Install MySQL
subprocess.run("wget https://dev.mysql.com/get/mysql80-community-release-el7-9.noarch.rpm", shell=True, check=True)
subprocess.run("sudo rpm -ivh mysql80-community-release-el7-9.noarch.rpm", shell=True, check=True)
subprocess.run("sudo yum update -y", shell=True, check=True)
subprocess.run("sudo yum install mysql-server -y", shell=True, check=True)
subprocess.run("sudo systemctl start mysqld", shell=True, check=True)

# Get temporary password
result = subprocess.run("sudo grep 'temporary password' /var/log/mysqld.log", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
temp_password = result.stdout.split()[3]

# Secure MySQL installation
sql_commands = [
    "y",  # Remove anonymous users
    "Y",  # Disallow root login remotely
    "n",  # Remove test database and access it
    "Y",  # Reload privilege tables
]
sql_commands_str = "\n".join(sql_commands)

secure_install_cmd = (
    "echo -e 'Omkar@123\\nOmkar@123\\n{temp_password}\\n' '{sql_commands_str}' | sudo mysql_secure_installation"
)
subprocess.run(secure_install_cmd, shell=True, check=True, env={"temp_password": temp_password, "sql_commands_str": sql_commands_str})

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
