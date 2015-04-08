VM_MEMORY = "1024"
VM_CPU = 1
VM_NAME = "firethoughts"
VAGRANT_COMMAND = ARGV[0]

Vagrant.require_version ">=1.6.0"
Vagrant.configure("2") do |config|

    config.vm.hostname = VM_NAME
    # if VAGRANT_COMMAND == "ssh"
    #  config.ssh.username = "firethoughts"
    # end
    config.vm.post_up_message = "Welcome to firethoughts VM. Please 'vagrant ssh' to continue.."

    config.vm.provision :shell, :path => "provision/shell/ubuntu.sh"
    config.vm.provision :puppet do |provision|
        provision.manifests_path ="provision/puppet/manifests"
        provision.manifest_file = "site.pp"
        provision.module_path = "provision/puppet/modules"
    end
    config.vm.synced_folder "project/", "/var/www/www.firethoughts.mu", owner:"www-data", group: "www-data"
    #config.vm.synced_folder "project/client/", "/var/www", owner:"www-data", group:"www-data"

    config.vm.define "local", primary: true do |local|
        local.vm.provider "virtualbox" do |provider, override|
            if Vagrant.has_plugin?("vagrant-cachier")
                override.cache.scope = :box
            end
            provider.name = VM_NAME
            provider.gui = false
            provider.customize ["modifyvm", :id, "--memory", VM_MEMORY]
            provider.customize ["modifyvm", :id, "--cpus", VM_CPU]
			provider.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
            provider.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
            provider.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root", "1"]

            override.vm.box = "ubuntu/trusty64"
            override.vm.box_url = "https://vagrantcloud.com/ubuntu/trusty64"
            override.vm.network :forwarded_port, guest: 3000, host: 3000, auto_correct:true # client app
            override.vm.network :forwarded_port, guest: 4000, host: 4000, auto_correct:true # admin app
            override.vm.network :forwarded_port, guest: 5000, host: 5000, auto_correct:true # server api
            override.vm.network :forwarded_port, guest: 6379, host: 6379, auto_correct:true # redis
            override.vm.network :forwarded_port, guest: 9200, host: 9200, auto_correct:true # elasticsearch
            override.vm.network :forwarded_port, guest: 27017, host: 27017, auto_correct:true # mongodb

            # override.vm.network :private_network, ip: '10.11.12.13'
        end
    end
    config.vm.define "production", autostart: false do |production|
        production.vm.provider :digital_ocean do |provider, override|
            override.ssh.private_key_path = "~/.ssh/id_rsa"
            override.vm.box = "digital_ocean"
            override.vm.box_url = "https://github.com/smdahlen/vagrant-digitalocean/raw/master/box/digital_ocean.box"
            provider.token = "xxxxxx"
            provider.image = "14.04 x64"
            provider.size = "1gb"
            provider.region = "lon1"
            provider.backups_enabled = true
        end
    end
    config.vm.define "lxc", autostart: false do |lxc|
        lxc.vm.provider :lxc do |provider, override|
            provider.container_name = VM_NAME
            override.vm.box = "fgrehm/trusty64-lxc"
            override.vm.network :forwarded_port, guest: 3000, host: 3000, auto_correct:true # client app
            override.vm.network :forwarded_port, guest: 4000, host: 4000, auto_correct:true # admin app
            override.vm.network :forwarded_port, guest: 5000, host: 5000, auto_correct:true # server api
            override.vm.network :forwarded_port, guest: 6379, host: 6379, auto_correct:true # redis
            override.vm.network :forwarded_port, guest: 9200, host: 9200, auto_correct:true # elasticsearch
            override.vm.network :forwarded_port, guest: 27017, host: 27017, auto_correct:true # mongodb
        end
    end
end
