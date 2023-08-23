import subprocess

job_list = [
    'sudo apt update',
    'sudo apt install apache2 -y'
]

for job in job_list:
    try:
        subprocess.run(job, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")

base_url = 'https://archive.cloudera.com/cdh7/7.1.7/parcels/'
target_directory = '/var/www/html/cloudera-repos/cdh7/7.1.7.0/parcels'

# Create target directory
create_directory_command = f'sudo mkdir -p {target_directory}'
try:
    subprocess.run(create_directory_command, shell=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error creating directory: {e}")

files_to_download = [
    'CDH-7.1.7-1.cdh7.1.7.p0.15945976-el7.parcel',
    'CDH-7.1.7-1.cdh7.1.7.p0.15945976-el7.parcel.sha1',
    'CDH-7.1.7-1.cdh7.1.7.p0.15945976-el7.parcel.sha256',
    'KEYTRUSTEE_SERVER-7.1.7.0-1.keytrustee7.1.7.0.p0.15945976-el7.parcel',
    'KEYTRUSTEE_SERVER-7.1.7.0-1.keytrustee7.1.7.0.p0.15945976-el7.parcel.sha',
    'KEYTRUSTEE_SERVER-7.1.7.0-1.keytrustee7.1.7.0.p0.15945976-el7.parcel.sha1',
    'manifest.json'
]

for file in files_to_download:
    download_command = f'sudo wget {base_url}/{file} -P {target_directory}'
    try:
        subprocess.run(download_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {file}: {e}")

subprocess.run(['sudo', 'systemctl', 'start', 'apache2'], check=True)
