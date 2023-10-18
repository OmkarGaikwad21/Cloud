import subprocess
import os

# Specify the full path to the AWS CLI executable
aws_cli_path = "/usr/local/bin/aws"  # Replace with the correct path if necessary

# Check if AWS CLI is installed
if not subprocess.run([f"command -v {aws_cli_path} >/dev/null 2>&1"], shell=True).returncode == 0:
    # Install AWS CLI if it's not installed
    subprocess.run(["sudo", "pip3", "install", "awscli"], shell=False, check=True)
    # Get the path to the AWS CLI executable
    aws_cli_path = subprocess.check_output(["which", "aws"], shell=False).strip()

# Set AWS configuration environment variables
os.environ["AWS_ACCESS_KEY_ID"] = "AKIATZ2MTC63MJSPDCRD"
os.environ["AWS_SECRET_ACCESS_KEY"] = "6U58VkVg4qjAG3Vgjukbwba4nulO6CRWYU6y8xiJ"
os.environ["AWS_DEFAULT_REGION"] = "ap-south-1"
os.environ["AWS_DEFAULT_OUTPUT"] = "json"  # Set your desired output format here

# Configure AWS CLI without user interaction
subprocess.run([f"{aws_cli_path}", "configure", "set", "aws_access_key_id", os.environ['AWS_ACCESS_KEY_ID']], shell=False, check=True)
subprocess.run([f"{aws_cli_path}", "configure", "set", "aws_secret_access_key", os.environ['AWS_SECRET_ACCESS_KEY']], shell=False, check=True)
subprocess.run([f"{aws_cli_path}", "configure", "set", "default.region", os.environ['AWS_DEFAULT_REGION']], shell=False, check=True)
subprocess.run([f"{aws_cli_path}", "configure", "set", "default.output", os.environ['AWS_DEFAULT_OUTPUT']], shell=False, check=True)

# Get the private IP of the "repo" instance
repo_private_ip = subprocess.check_output([aws_cli_path, "ec2", "describe-instances", "--filters", "Name=tag:Name,Values=Repo", "--query", "Reservations[0].Instances[0].PrivateIpAddress", "--output", "text"], shell=False).strip()

# Get the private DNS of the "database" instance
db_private_dns = subprocess.check_output([aws_cli_path, "ec2", "describe-instances", "--filters", "Name=tag:Name,Values=Database", "--query", "Reservations[0].Instances[0].PrivateDnsName", "--output", "text"], shell=False).strip()

# Correct the formatting of the private IP
repo_private_ip = repo_private_ip.decode().strip("b")

# Configure Cloudera Manager repo
repo_content = f"""
[cloudera-manager]
name=Cloudera Manager
baseurl=http://{repo_private_ip}/cloudera-repos/cm7/cm7.4.4/
gpgkey =http://{repo_private_ip}/cloudera-repos/cm7/cm7.4.4/RPM-GPG-KEY-cloudera
gpgcheck = 0
"""

# Save repo configuration
with open('/etc/yum.repos.d/cloudera-manager.repo', 'w') as f:
    f.write(repo_content)

# Install Cloudera Manager
subprocess.run(["sudo", "yum", "clean", "all"], shell=False, check=True)
subprocess.run(["sudo", "yum", "makecache"], shell=False, check=True)
subprocess.run(["sudo", "yum", "install", "cloudera-manager-daemons", "cloudera-manager-agent", "cloudera-manager-server", "-y"], shell=False, check=True)

# Prepare database
db_name = "scm"
db_user = "scm"
db_password = "Omkar@123"


subprocess.run(["sudo", "/opt/cloudera/cm/schema/scm_prepare_database.sh", "mysql", "-h", db_private_dns.decode(), db_name, db_user, db_password], shell=False, check=True)

# Start Cloudera Manager
subprocess.run(["sudo", "systemctl", "start", "cloudera-scm-server"], shell=False, check=True)
subprocess.run(["sudo", "systemctl", "enable", "cloudera-scm-server"], shell=False, check=True)

print("Cloudera Manager installed and configured!")

# Tail the Cloudera Manager server log
subprocess.run(["sudo", "tail", "-f", "/var/log/cloudera-scm-server/cloudera-scm-server.log"])