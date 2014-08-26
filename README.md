Repository used internally.

It's possible to use a [vagrant](http://vagrantup.com) machine in order to test all the things

    $ ansible-playbook playbook.yml --check-syntax
    $ ansible-playbook \
        --inventory-file=vagrant_inventory \
        --private-key=~/.vagrant.d/insecure_private_key \
        --user=root \
        playbook.yml


There are several roles availables:

 - nginx
 - postgresql (coming soon)
 - Certificates (coming soon)
