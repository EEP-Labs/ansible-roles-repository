    $ vagrant up
    $ ansible-playbook         \
        --inventory-file=vagrant_inventory                \
        --private-key=~/.vagrant.d/insecure_private_key   \
        --user=root         \
        --skip-tag certs    \
        playbook.yml
    $ storm add vagrant root@127.0.0.1:2222 \
        --id_file ~/.vagrant.d/insecure_private_key --o 'identitiesonly=True' --config .ssh_provisioning_config

    $ bin/manage add-key-to-user \
        id_rsa.pub testuser vagrant    # put the wanted ssh key into the authorized_keys file to the remote side
    $ storm add test testuser@127.0.0.1:2222 \
        --id_file id_rsa --o 'identitiesonly=True' --config .ssh_provisioning_config
    $ git remote add test test:repo/   # save a remote

    $ bin/deploy test HEAD             # finally deploy