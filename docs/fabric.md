Fabric
======

[Doc](http://docs.fabfile.org/)

    $ fab -H localhost -a -f provisioning/fabric/fabfile.py my_task
    [localhost] Executing task 'my_task'
    [localhost] run: /bin/bash -l -c "ls /var/www"
    [localhost] Login password for 'eeplabs': 
    [localhost] out: ls: impossibile accedere a /var/www: File o directory non esistente
    [localhost] out: