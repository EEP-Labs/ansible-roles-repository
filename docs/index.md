It's important to maintain a set of reusable tools and conventions to deploy web application and stuff, like
directory structure, database permissions, user home directory and web server configuration.

The procedures are categorized as follow

 - Server configuration: exist a lot of tools to do that, we have chosen [Ansible](http://ansible.com) since it's written in Python
and does not require to install nothing server side but Python itself. There are some drawbacks in this tool
but up to now has done its job. If you want a little introduction there is a page [here](ansible.md)

- Deploy procedure: we have chosen [Fabric](fabric.md) 

Convention
----------

There are at least three configurations in a normal development:

 * local, using [Vagrant](vagrant.md)
 * staging, used for pre-release
 * production, where shit happens

In our deployment configuration with ansible, the inventory file is named like

    ansible_<configuration>_inventory

and the variables file is named

    ansible_<configuraton>_variables

The vagrant version of these files is included in this repository since it should be equal across every project.

For each of this file you have to indicate at least the following ansible variables

 * ``ansible_ssh_host``
 * ``ansible_ssh_private_key``
 * ``ansible_ssh_user`` equal to ``root``

A project will contain this repository and its roles as a submodule in a directory named ``provision/``
(see [here](installation.md) for some notes about this)
and all the file described for the configuration will be placed inside it.

Usage
-----

In the ``bin/`` directory exists the ``manage`` script that help to configure the machines
 
    (provisioning dir) $ bin/manage provision <configuration>
    (main project dir) $ git remote add vagrant example:repo/
    (main project dir) $ provision/bin/deploy vagrant HEAD

Directories structure
---------------------

The structure is

    app-rev  <--- this here will be recreated each time
    app      <--- this is a symbolic link to the actual app's directory
    logs
    media
    static
    repo <--- optional
    .conf
    .virtualenv

TODO
----
    $ storm add vagrant root@127.0.0.1:2222 \
        --id_file ~/.vagrant.d/insecure_private_key --o 'identitiesonly=True' --config .ssh_provisioning_config

    $ bin/manage add-key-to-user \
        id_rsa.pub testuser vagrant    # put the wanted ssh key into the authorized_keys file to the remote side
    $ storm add test testuser@127.0.0.1:2222 \
        --id_file id_rsa --o 'identitiesonly=True' --config .ssh_provisioning_config