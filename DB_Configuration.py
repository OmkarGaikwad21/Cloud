import subprocess

# Connect to MySQL and reset root password
mysql_reset_cmd = [
    "mysql", "-u", "root", "-pOmkar@123", "--execute", 
    "ALTER USER 'root'@'localhost' IDENTIFIED BY 'Omkar@123';"
]
subprocess.run(mysql_reset_cmd, check=True)

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
        subprocess.run(mysql_cmd + [sql], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Create temp user
temp_user_sql = """CREATE USER 'temp'@'%' IDENTIFIED BY 'Omkar@123';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, RELOAD, PROCESS, REFERENCES, INDEX, ALTER, SHOW DATABASES, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, REPLICATION SLAVE, REPLICATION CLIENT, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, CREATE USER, EVENT, TRIGGER ON *.* TO 'temp'@'%' WITH GRANT OPTION;"""
subprocess.run(mysql_cmd + [temp_user_sql], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

print("MySQL configured successfully!")
