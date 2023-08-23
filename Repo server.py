import subprocess

job_list = [
    'sudo apt update',
    'sudo apt install apache2 -y',
    'sudo mkdir -p /var/www/html/cloudera-repos/cm7/',
    'wget https://archive.cloudera.com/cm7/7.4.4/repo-as-tarball/cm7.4.4-redhat7.tar.gz',
    'sudo tar -xzvf cm7.4.4-redhat7.tar.gz -C /var/www/html/cloudera-repos/cm7/',
    'sudo mkdir -p /var/www/html/cloudera-repos/cdh7/7.1.7.0/parcels',
    'cd /var/www/html/cloudera-repos/cdh7/7.1.7.0/parcels',
    'sudo wget https://archive.cloudera.com/cdh7/7.1.7/parcels/CDH-7.1.7-1.cdh7.1.7.p0.15945976-el7.parcel',
    'sudo wget https://archive.cloudera.com/cdh7/7.1.7/parcels/CDH-7.1.7-1.cdh7.1.7.p0.15945976-el7.parcel.sha1',
    'sudo wget https://archive.cloudera.com/cdh7/7.1.7/parcels/CDH-7.1.7-1.cdh7.1.7.p0.15945976-el7.parcel.sha256',
    'sudo wget https://archive.cloudera.com/cdh7/7.1.7/parcels/KEYTRUSTEE_SERVER-7.1.7.0-1.keytrustee7.1.7.0.p0.15945976-el7.parcel',
    'sudo wget https://archive.cloudera.com/cdh7/7.1.7/parcels/KEYTRUSTEE_SERVER-7.1.7.0-1.keytrustee7.1.7.0.p0.15945976-el7.parcel.sha',
    'sudo wget https://archive.cloudera.com/cdh7/7.1.7/parcels/KEYTRUSTEE_SERVER-7.1.7.0-1.keytrustee7.1.7.0.p0.15945976-el7.parcel.sha1',
    'sudo wget https://archive.cloudera.com/cdh7/7.1.7/parcels/manifest.json',
    'cd ~',  # Change back to home directory
    'sudo systemctl start apache2'
]

for job in job_list:
    try:
        subprocess.run(job, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
