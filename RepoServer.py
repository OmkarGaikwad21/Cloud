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
cm_directory = '/var/www/html/cloudera-repos/cm7/'
cdh_directory = '/var/www/html/cloudera-repos/cdh7/7.1.7.0/parcels'

# Create target directories
create_cm_directory_command = f'sudo mkdir -p {cm_directory}'
create_cdh_directory_command = f'sudo mkdir -p {cdh_directory}'
try:
    subprocess.run(create_cm_directory_command, shell=True, check=True)
    subprocess.run(create_cdh_directory_command, shell=True, check=True)
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
    download_command = f'sudo wget {base_url}/{file} -P {cdh_directory}'
    try:
        subprocess.run(download_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {file}: {e}")

# Download cm file
cm_file_url = 'https://archive.cloudera.com/cm7/7.4.4/repo-as-tarball/cm7.4.4-redhat7.tar.gz'
download_cm_command = f'sudo wget {cm_file_url} -P {cm_directory}'
try:
    subprocess.run(download_cm_command, shell=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error downloading CM file: {e}")

# Extract cm file
extract_cm_command = f'sudo tar -xzvf {cm_directory}cm7.4.4-redhat7.tar.gz -C {cm_directory}'
try:
    subprocess.run(extract_cm_command, shell=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error extracting CM file: {e}")

subprocess.run(['sudo', 'systemctl', 'start', 'apache2'], check=True)
