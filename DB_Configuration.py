import subprocess

# Install MySQL
subprocess.run("wget https://dev.mysql.com/get/mysql80-community-release-el7-9.noarch.rpm", shell=True, check=True)
subprocess.run("sudo rpm -ivh mysql80-community-release-el7-9.noarch.rpm", shell=True, check=True)
subprocess.run("sudo yum update -y", shell=True, check=True)
subprocess.run("sudo yum install mysql-server -y", shell=True, check=True)
subprocess.run("sudo systemctl start mysqld", shell=True, check=True)

# Get temporary password
result = subprocess.run("sudo grep 'temporary password' /var/log/mysqld.log", shell=True, stdout=subprocess.PIPE, check=True)
temp_password = result.stdout.decode('utf-8').split()[3]

# Secure MySQL installation
sql_commands = [
    f"{temp_password}",
    "Omkar@123", "Omkar@123", "n", "Y", "Y", "n", "Y"
]
subprocess.run("echo '{}' | sudo mysql_secure_installation".format('\\n'.join(sql_commands)), shell=True, check=True)

# Create databases and users
databases_and_users = [
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
    ("temp", "Omkar@123")
]

for db, password in databases_and_users:
    sql = f"""
        CREATE DATABASE {db} DEFAULT CHARACTER SET utf8;
        CREATE USER '{db}'@'%' IDENTIFIED BY '{password}';
        GRANT ALL PRIVILEGES ON {db}.* TO '{db}'@'%';
    """
    subprocess.run(f"echo '{sql}' | mysql -u root -pOmkar@123", shell=True, check=True)

print("MySQL setup and configuration completed!")
