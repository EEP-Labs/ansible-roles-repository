Installation
============

This repository can be used in any project involving some machine configuration actions.

First of all, you can use ``git submodule`` to put the code into a ``provisioning/`` directory
with the following command

    $ git submodule add https://github.com/EEP-Labs/ansible-roles-repository provision/

After that you can copy the ``vagrant`` and ansible configuration files

    $ cp provision/{Vagrantfile,ansible_vagrant_inventory,ansible_vagrant_variables} .

and edit them to fit your taste.