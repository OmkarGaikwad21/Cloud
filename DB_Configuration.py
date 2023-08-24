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
    f"echo -e 'Omkar@123\\nOmkar@123\\n{temp_password}\\n{sql_commands_str}' "
    "| sudo mysql_secure_installation"
)
subprocess.run(secure_install_cmd, shell=True, check=True)

# Create databases and users
databases = [
    ("scm", "Omkar@123"),
    ("hive", "Omkar@123"),
    ("hue", "Omkar@123"),
    ("rman", "Omkar@123"),
    ("navs", "Omkar@123"),
    ("navms", "Omkar@123"),
    ("oozie", "Omkar@123"),
    ("actmo", "Omkar@123"),
    ("sentry", "Omkar@123"),
    ("ranger", "Omkar@123"),
]

for db, password in databases:
    sql = f"""
        CREATE DATABASE {db} DEFAULT CHARACTER SET utf8;
        CREATE USER '{db}'@'%' IDENTIFIED BY '{password}';
        GRANT ALL PRIVILEGES ON {db}.* TO '{db}'@'%';
    """
    subprocess.run(f"echo '{sql}' | sudo mysql -u root -pOmkar@123", shell=True, check=True)

# Create temp user
temp_sql = """
    CREATE USER 'temp'@'%' IDENTIFIED BY 'Omkar@123';
    GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, RELOAD, PROCESS, REFERENCES, INDEX, ALTER, SHOW DATABASES, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, REPLICATION SLAVE, REPLICATION CLIENT, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, CREATE USER, EVENT, TRIGGER ON *.* TO 'temp'@'%' WITH GRANT OPTION;
"""
subprocess.run(f"echo '{temp_sql}' | sudo mysql -u root -pOmkar@123", shell=True, check=True)

print("MySQL setup completed!")
