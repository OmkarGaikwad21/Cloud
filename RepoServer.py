from subprocess import call

job_list = [
'sudo apt update',
'sudo apt install apache2 -y',

'wget https://archive.cloudera.com/cm7/7.4.4/repo-as-tarball/cm7.4.4-redhat7.tar.gz',

'wget https://archive.cloudera.com/cdh7/7.1.7/parcels/CDH-7.1.7-1.cdh7.1.7.p0.15945976-el7.parcel',
'wget https://archive.cloudera.com/cdh7/7.1.7/parcels/CDH-7.1.7-1.cdh7.1.7.p0.15945976-el7.parcel.sha1',
'wget https://archive.cloudera.com/cdh7/7.1.7/parcels/CDH-7.1.7-1.cdh7.1.7.p0.15945976-el7.parcel.sha256',
'wget https://archive.cloudera.com/cdh7/7.1.7/parcels/KEYTRUSTEE_SERVER-7.1.7.0-1.keytrustee7.1.7.0.p0.15945976-el7.parcel',
'wget https://archive.cloudera.com/cdh7/7.1.7/parcels/KEYTRUSTEE_SERVER-7.1.7.0-1.keytrustee7.1.7.0.p0.15945976-el7.parcel.sha',
'wget https://archive.cloudera.com/cdh7/7.1.7/parcels/KEYTRUSTEE_SERVER-7.1.7.0-1.keytrustee7.1.7.0.p0.15945976-el7.parcel.sha1',
'wget https://archive.cloudera.com/cdh7/7.1.7/parcels/KEYTRUSTEE_SERVER-7.1.7.0-1.keytrustee7.1.7.0.p0.15945976-el7.parcel.sha256',
'wget https://archive.cloudera.com/cdh7/7.1.7/parcels/manifest.json',

'sudo mkdir -p /var/www/html/cloudera-repos/cdh7/7.1.7.0/parcels/',
'sudo mkdir -p /var/www/html/cloudera-repos/cm7/',

'sudo mv CDH-7.1.7-1.cdh7.1.7.p0.15945976-el7.parcel* /var/www/html/cloudera-repos/cdh7/7.1.7.0/parcels ',
'sudo mv KEYTRUSTEE_SERVER-7.1.7.0-1.keytrustee7.1.7.0.p0.15945976-el7.parcel* /var/www/html/cloudera-repos/cdh7/7.1.7.0/parcels ',
'sudo mv manifest.json /var/www/html/cloudera-repos/cdh7/7.1.7.0/parcels ',

'sudo tar -xzvf cm7.4.4-redhat7.tar.gz -C /var/www/html/cloudera-repos/cm7/',

]

for job in job_list:
    call(job, shell=True)
