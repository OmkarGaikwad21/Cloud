import subprocess

# Stop MySQL service
subprocess.run(["sudo", "systemctl", "stop", "mysqld"], check=True)

# Start MySQL service with --skip-grant-tables
subprocess.run(["sudo", "mysqld_safe", "--skip-grant-tables", "&"], check=True)

# Update root password
subprocess.run(["mysql", "-u", "root", "-e", "ALTER USER 'root'@'localhost' IDENTIFIED BY 'Omkar@123'; FLUSH PRIVILEGES;"], check=True)

# Exit MySQL
subprocess.run(["mysql", "-u", "root", "-e", "EXIT;"], check=True)

# Stop MySQL service
subprocess.run(["sudo", "systemctl", "stop", "mysqld"], check=True)

# Start MySQL service
subprocess.run(["sudo", "systemctl", "start", "mysqld"], check=True)

# Connect to MySQL and run SQL commands
mysql_cmd = ["mysql", "-u", "root", "-pOmkar@123", "--execute"]
databases = ["scm", "hive", "hue", "rman", "navs", "navms", "oozie", "actmo", "sentry", "ranger"]

for db in databases:
    sql_commands = [
        f"CREATE DATABASE {db} DEFAULT CHARACTER SET utf8;",
        f"CREATE USER '{db}'@'%' IDENTIFIED BY 'Omkar@123';",
        f"GRANT ALL PRIVILEGES ON {db}.* TO '{db}'@'%';"
    ]
    
    for sql in sql_commands:
        subprocess.run(mysql_cmd + [sql], check=True)

# Create temp user
temp_user_sql = """CREATE USER 'temp'@'%' IDENTIFIED BY 'Omkar@123';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, RELOAD, PROCESS, REFERENCES, INDEX, ALTER, SHOW DATABASES, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, REPLICATION SLAVE, REPLICATION CLIENT, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, CREATE USER, EVENT, TRIGGER ON *.* TO 'temp'@'%' WITH GRANT OPTION;"""
subprocess.run(mysql_cmd + [temp_user_sql], check=True)

print("MySQL configured successfully!")
