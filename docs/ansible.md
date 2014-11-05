Ansible
=======

Installation
------------

From source

    $ git clone https://github.com/ansible/ansible.git && cd ansible
    $ make deb
    # dpkg -i ../ansible_XXX.deb

or from the package manager

    # apt-get install ansible

Usage
-----

``Ansible`` is based on **playbook**: **Playbook** contains **Plays** contains **Tasks** calls **Modules**,
**Handlers** can be triggered by tasks.

First of all the tool used to connect is ``SSH``, the host to which connect to is indicated into the ``inventory`` file.

The default is ``/etc/ansible/hosts`` but you can pass another with the ``--inventory-file`` parameter; the inventory
can store alias, variable, etc. There are also a lot of
[variables](http://docs.ansible.com/intro_inventory.html#list-of-behavioral-inventory-parameters) used by ansible itself.

Vagrant
-------

In order to provision with it

```ruby
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "provisioning/playbook.yml"
    #ansible.verbose  = 'vvvv'
    ansible.extra_vars = {
        ansible_ssh_user: 'root',
        db_user: "astauser",
        db_name: "astadb",
        db_password: "asta"
    }
  end
```