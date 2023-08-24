import subprocess

# Update package repository and install Apache
subprocess.run(["sudo", "apt", "update"])
subprocess.run(["sudo", "apt", "install", "apache2", "-y"])

# Create necessary directories
subprocess.run(["sudo", "mkdir", "-p", "/var/www/html/cloudera-repos/cm7/"])

# Download and extract CM repository
subprocess.run(["sudo", "wget", "https://archive.cloudera.com/cm7/7.4.4/repo-as-tarball/cm7.4.4-redhat7.tar.gz"])
subprocess.run(["sudo", "tar", "-xzvf", "cm7.4.4-redhat7.tar.gz", "-C", "/var/www/html/cloudera-repos/cm7/"])

# Download CDH parcels and files
subprocess.run(["sudo", "mkdir", "-p", "/var/www/html/cloudera-repos/cdh7/7.1.7.0/parcels"])
parcel_urls = [
    "https://archive.cloudera.com/cdh7/7.1.7/parcels/CDH-7.1.7-1.cdh7.1.7.p0.15945976-el7.parcel",
    "https://archive.cloudera.com/cdh7/7.1.7/parcels/CDH-7.1.7-1.cdh7.1.7.p0.15945976-el7.parcel.sha1",
    "https://archive.cloudera.com/cdh7/7.1.7/parcels/CDH-7.1.7-1.cdh7.1.7.p0.15945976-el7.parcel.sha256",
    "https://archive.cloudera.com/cdh7/7.1.7/parcels/KEYTRUSTEE_SERVER-7.1.7.0-1.keytrustee7.1.7.0.p0.15945976-el7.parcel",
    "https://archive.cloudera.com/cdh7/7.1.7/parcels/KEYTRUSTEE_SERVER-7.1.7.0-1.keytrustee7.1.7.0.p0.15945976-el7.parcel.sha",
    "https://archive.cloudera.com/cdh7/7.1.7/parcels/KEYTRUSTEE_SERVER-7.1.7.0-1.keytrustee7.1.7.0.p0.15945976-el7.parcel.sha1",
    "https://archive.cloudera.com/cdh7/7.1.7/parcels/manifest.json"
]

for url in parcel_urls:
    subprocess.run(["sudo", "wget", url, "-P", "/var/www/html/cloudera-repos/cdh7/7.1.7.0/parcels"])

# Start Apache service
subprocess.run(["sudo", "systemctl", "start", "apache2"])

print("Cloudera setup completed.")
