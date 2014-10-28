Repository used internally.

It's possible to use a [vagrant](http://vagrantup.com) machine in order to test all the things

    $ ansible-playbook playbook.yml --syntax-check
    $ ansible-playbook \
        --inventory-file=vagrant_inventory \
        --private-key=~/.vagrant.d/insecure_private_key \
        --user=root \
        --skip-tag certs \
        playbook.yml
    $ ansible-playbook \
        --inventory-file=local_inventory \
        --tag certs \
        --extra-vars @certs.yml \
        --extra-vars site=eeplab.es \
        playbook.yml 


There are several roles availables:

 - nginx
 - postgresql
 - Certificates (coming soon)

If the variable ``development`` is defined some dev options are enabled.

Getting started
---------------

If you have a project that needs to be provisioned you can use this as a submodule

    $ git submodule add https://github.com/EEP-Labs/ansible-roles-repository provision/
