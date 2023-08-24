import subprocess
import sys

# Configure Cloudera Manager repo
with open('/etc/yum.repos.d/cloudera-manager.repo', 'w') as f:
  f.write("""
[cloudera-manager]
name=Cloudera Manager
baseurl=http://your_repo_privateIP/cloudera-repos/cm7/cm7.4.4/
gpgkey =http://your_repo_privateIP/cloudera-repos/cm7/cm7.4.4/RPM-GPG-KEY-cloudera
gpgcheck = 0
""")

# Install Cloudera Manager
subprocess.run("sudo yum clean all", shell=True, check=True)
subprocess.run("sudo yum makecache", shell=True, check=True)
subprocess.run("sudo yum install cloudera-manager-daemons cloudera-manager-agent cloudera-manager-server -y", shell=True, check=True)

# Prepare database 
db_host = "your_db_host_privateIP_of_DNS" 
db_name = "scm"
db_user = "scm"
db_password = "Omkar@123"

subprocess.run(f"sudo /opt/cloudera/cm/schema/scm_prepare_database.sh mysql -h {db_host} {db_name} {db_user} {db_password}", shell=True, check=True)

# Start Cloudera Manager
subprocess.run("sudo systemctl start cloudera-scm-server", shell=True, check=True)
subprocess.run("sudo systemctl enable cloudera-scm-server", shell=True, check=True)
subprocess.run("sudo tail -f /var/log/cloudera-scm-server/cloudera-scm-server.log", shell=True)

print("Cloudera Manager installed and configured!")
