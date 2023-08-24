import subprocess
import sys

def main():

  # Install MySQL
  subprocess.run("wget https://dev.mysql.com/get/mysql80-community-release-el7-9.noarch.rpm", shell=True, check=True)
  subprocess.run("sudo rpm -ivh mysql80-community-release-el7-9.noarch.rpm", shell=True, check=True) 
  subprocess.run("sudo yum update -y", shell=True, check=True)
  subprocess.run("sudo yum install mysql-server -y", shell=True, check=True)
  subprocess.run("sudo systemctl start mysqld", shell=True, check=True)

  # Get temp password
  result = subprocess.run("sudo grep 'temporary password' /var/log/mysqld.log", shell=True, capture_output=True, text=True)
  temp_password = result.stdout.split()[3]
  print(f"Temporary password: {temp_password}")

  # Secure MySQL installation
  sql_commands = [
    "SET PASSWORD = 'Omkar@123';",
    "ALTER USER 'root'@'localhost' PASSWORD EXPIRE NEVER;", 
    "drop database if exists test;",
    "flush privileges;"
  ]
  subprocess.run("echo '\n".join(sql_commands) + f"' | mysql -u root -p{temp_password}", shell=True, check=True)

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

if __name__ == "__main__":
  main()
