Fabric
======

[Doc](http://docs.fabfile.org/)

Fabric uses internally a re-implementation of the [SSH with ``paramiko``](http://docs.fabfile.org/en/latest/usage/ssh.html)
so be aware of some behaviours not expected.

    $ fab -H localhost -a -f provisioning/fabric/fabfile.py my_task
    [localhost] Executing task 'my_task'
    [localhost] run: /bin/bash -l -c "ls /var/www"
    [localhost] Login password for 'eeplabs': 
    [localhost] out: ls: impossibile accedere a /var/www: File o directory non esistente
    [localhost] out:

In order to test with Vagrant

    $ fab --no_agent \
        -H 127.0.0.1 \
        -i ~/.vagrant.d/insecure_private_key  \
        --user vagrant \
        --port 2222 \
        -f provisioning/fabric/fabfile.py \
        release

There are available three commands

 - ``release`` that deploy a revision in the remote side
 - ``dump_db_snapshot`` download a dump of the current remote database
 - ``load_db_snapshot`` download and load into the local database the remote one