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
**Handlers** can be triggered by tasks. The principal tool is ``ansible-playbook`` that reading a playbook
executes the necessary tasks.

First of all the tool used to connect is ``SSH``, the host to which connect to is indicated into the ``inventory`` file.


The default inventory is ``/etc/ansible/hosts`` but you can pass another with the ``--inventory-file`` parameter; the inventory
can store alias, variable, etc. There are also a lot of
[variables](http://docs.ansible.com/intro_inventory.html#list-of-behavioral-inventory-parameters) used by ansible itself.

It's possible also to launch ansible without playbook if you want to execute a single module, like the following

    $ ansible -i <inventory> all -m setup --tree /tmp/facts

In the official documentation there is [more](http://docs.ansible.com/intro_adhoc.html).

Generally the form of usage is

    $ ansible-playbook         \
        --inventory-file=vagrant_inventory                \
        --private-key=~/.vagrant.d/insecure_private_key   \
        --user=root         \
        --skip-tag certs    \
        playbook.yml

Template
--------

The configuration is described using ``YAML`` file, and internally are parsed using the [Jinja2](http://jinja.pocoo.org/)
template system.

Roles
-----

Since we want to reuse configuration across projects (that is the aim of this project) we are using the **roles**.

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