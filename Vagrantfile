# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.box = "generic/rocky8"
  config.vm.box_download_insecure = true
  config.vbguest.installer_options = { allow_kernel_upgrade: true }

  if Vagrant.has_plugin?("vagrant-vbguest") then
    config.vbguest.auto_update = false
  end

  config.vm.provider "virtualbox" do |v|
	  v.customize ["modifyvm", :id, "--memory", "8192"]
  end

  config.vm.synced_folder "./", "/vagrant"
  config.vm.synced_folder "~/.aws", "/home/vagrant/.aws"
  #config.vm.synced_folder "C:/Users/Walter.Deignan/GitHub/aws-serverless-s3-antivirus/aws-serverless-s3-antivirus", "/antivirus"

  config.vm.network :forwarded_port, guest: 8000, host: 8000
  config.vm.network :forwarded_port, guest: 8443, host: 8443
  config.vm.network "private_network", ip: "192.168.56.30"

  config.vm.provision "shell", inline: <<-SHELL

  #yum -y update
  systemctl stop firewalld
  systemctl disable firewalld

  dnf check-update
  dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
  dnf install -y docker-ce docker-ce-cli containerd.io

  yum -y install dos2unix
	curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
	chmod +x /usr/local/bin/docker-compose

	systemctl enable docker
	systemctl start docker
  usermod -aG docker vagrant

  yum -y install zip
  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
  unzip awscliv2.zip
  ./aws/install

  curl -L https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip -o aws-sam-cli-linux-x86_64.zip
  unzip aws-sam-cli-linux-x86_64.zip -d sam-installation
  ./sam-installation/install

  echo "export AWS_DEFAULT_PROFILE=cred_proc" >> /home/vagrant/.bashrc
  SHELL
end
