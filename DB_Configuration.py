import subprocess


# Reset root password 
mysql_cmd = ["mysqladmin", "-u", "root", "--skip-grant-tables", "password", "Omkar@123"]
subprocess.run(mysql_cmd, check=True)

# Connect to MySQL and run SQL
mysql_cmd = ["mysql", "-u", "root", "-pOmkar@123"]

# Create databases
databases = ["scm", "hive", "hue", "rman", "navs", "navms", "oozie", "actmo", "sentry", "ranger"]
for db in databases:
  sql = f"CREATE DATABASE {db} DEFAULT CHARACTER SET utf8;" 
  subprocess.Popen(mysql_cmd, stdin=subprocess.PIPE).communicate(sql.encode())  

  sql = f"CREATE USER '{db}'@'%' IDENTIFIED BY 'Omkar@123';"
  subprocess.Popen(mysql_cmd, stdin=subprocess.PIPE).communicate(sql.encode())

  sql = f"GRANT ALL PRIVILEGES ON {db}.* TO '{db}'@'%';"
  subprocess.Popen(mysql_cmd, stdin=subprocess.PIPE).communicate(sql.encode())

# Create temp user  
sql = """CREATE USER 'temp'@'%' IDENTIFIED BY 'Omkar@123';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, RELOAD, PROCESS, REFERENCES, INDEX, ALTER, SHOW DATABASES, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, REPLICATION SLAVE, REPLICATION CLIENT, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, CREATE USER, EVENT, TRIGGER ON *.* TO 'temp'@'%' WITH GRANT OPTION;"""
subprocess.Popen(mysql_cmd, stdin=subprocess.PIPE).communicate(sql.encode())

print("MySQL configured!")
