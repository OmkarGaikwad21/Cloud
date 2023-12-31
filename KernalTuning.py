import subprocess

# List of commands to execute
job_list = [
    "sudo yum update -y",
    "sudo yum install nano httpd zip unzip -y",
    "sudo yum install krb5-workstation krb5-libs -y",
    
   
    "sudo wget https://bitbucket.org/omkargaikwad21/cdp-cloud-files/raw/master/jdk-8u181-linux-x64.rpm",
    "sudo rpm -ivh jdk-8u181-linux-x64.rpm",
    "java -version",
    
    
    "wget https://raw.githubusercontent.com/OmkarGaikwad21/Cloud/main/pre-req-files/check-pre-req.sh",
    "wget https://raw.githubusercontent.com/OmkarGaikwad21/Cloud/main/pre-req-files/disable_iptables.sh",
    "wget https://raw.githubusercontent.com/OmkarGaikwad21/Cloud/main/pre-req-files/disable_ipv6.sh",
    "wget https://raw.githubusercontent.com/OmkarGaikwad21/Cloud/main/pre-req-files/disable_selinux.sh",
    "wget https://raw.githubusercontent.com/OmkarGaikwad21/Cloud/main/pre-req-files/disable_thp.sh",
    "wget https://raw.githubusercontent.com/OmkarGaikwad21/Cloud/main/pre-req-files/install_lzo.sh",
    "wget https://raw.githubusercontent.com/OmkarGaikwad21/Cloud/main/pre-req-files/install_nscd.sh",
    "wget https://raw.githubusercontent.com/OmkarGaikwad21/Cloud/main/pre-req-files/install_ntp.sh",
    "wget https://raw.githubusercontent.com/OmkarGaikwad21/Cloud/main/pre-req-files/install_tools.sh",
    "wget https://raw.githubusercontent.com/OmkarGaikwad21/Cloud/main/pre-req-files/remove_tuned.sh",
    "wget https://raw.githubusercontent.com/OmkarGaikwad21/Cloud/main/pre-req-files/tune_kernel.sh",
    "wget https://raw.githubusercontent.com/OmkarGaikwad21/Cloud/main/pre-req-files/sssd.conf",
    "wget https://raw.githubusercontent.com/OmkarGaikwad21/Cloud/main/pre-req-files/nscd.conf",
   
    
    
    "sudo sh disable_iptables.sh",
    "sudo sh disable_ipv6.sh",
    "sudo sh disable_selinux.sh",
    "sudo sh disable_thp.sh",
    "sudo sh install_lzo.sh",
    "sudo sh install_nscd.sh",
    "sudo sh install_ntp.sh",
    "sudo sh install_tools.sh",
    "sudo sh remove_tuned.sh",
    "sudo sh tune_kernel.sh",
    "sudo yum install bind-utils -y",
    
    
    "sudo service postfix stop",
    "sudo postfix set-permissions",
    "sudo service postfix start",
    
    
    "echo 'vm.swappiness=1' | sudo tee -a /etc/sysctl.conf",
    "sudo sysctl -p",
    
    
    "sudo yum install sssd -y",
    "sudo mv sssd.conf /etc/sssd/",
    "sudo chown root:root /etc/sssd/sssd.conf",
    "sudo chmod 600 /etc/sssd/sssd.conf",
    "sudo chkconfig sssd on",
    "sudo service sssd start",
    "sudo authconfig --enablesssdauth --enablesssd --updateall",
    "sudo mv nscd.conf /etc/",
    
    
    "wget https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-5.1.48.tar.gz",
    "tar zxvf mysql-connector-java-5.1.48.tar.gz",
    "sudo mkdir -p /usr/share/java/",
    "sudo cp mysql-connector-java-5.1.48/mysql-connector-java-5.1.48-bin.jar /usr/share/java/mysql-connector-java.jar",
    
    
    "echo -e 'StrictHostKeyChecking no\nUserKnownHostsFile=/dev/null' >> ~/.ssh/config",
    "ssh-keygen -t rsa -P '' -f $HOME/.ssh/id_rsa",
    "cat $HOME/.ssh/id_rsa.pub >> $HOME/.ssh/authorized_keys",
    "sudo chmod 600 ~/.ssh/config",
    
    
    "sudo sh check-pre-req.sh"

    
]

# Execute each command
for job in job_list:
    subprocess.call(job, shell=True)
