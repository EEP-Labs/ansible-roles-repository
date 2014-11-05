Vagrant
=======

Vagrant is a fundamental tool for creating reproducible environment; it's written in Ruby and can be installed
with ``apt``

    # apt-get install vagrant

After installed you should have the ``vagrant`` executable available that is a toolbox with the following
commands:

```
$ vagrant
Usage: vagrant [options] <command> [<args>]

    -v, --version                    Print the version and exit.
    -h, --help                       Print this help.

Common commands:
     box             manages boxes: installation, removal, etc.
     connect         connect to a remotely shared Vagrant environment
     destroy         stops and deletes all traces of the vagrant machine
     global-status   outputs status Vagrant environments for this user
     halt            stops the vagrant machine
     help            shows the help for a subcommand
     init            initializes a new Vagrant environment by creating a Vagrantfile
     login           log in to Vagrant Cloud
     package         packages a running vagrant environment into a box
     plugin          manages plugins: install, uninstall, update, etc.
     provision       provisions the vagrant machine
     rdp             connects to machine via RDP
     reload          restarts vagrant machine, loads new Vagrantfile configuration
     resume          resume a suspended vagrant machine
     share           share your Vagrant environment with anyone in the world
     ssh             connects to machine via SSH
     ssh-config      outputs OpenSSH valid configuration to connect to the machine
     status          outputs status of the vagrant machine
     suspend         suspends the machine
     up              starts and provisions the vagrant environment
     version         prints current and latest Vagrant version

For help on any individual command run `vagrant COMMAND -h`

Additional subcommands are available, but are either more advanced
or not commonly used. To see all subcommands, run the command
`vagrant list-commands`.
```
Usually a command acts in its own installation, the configuration for an installation is represented by a file
named ``Vagrantfile`` containing at least the box type and probably some network settings. It's possible to initialize
 one using the ``init`` subcommand.

After that ``vagrant up`` should launch the virtual machine.

Getting Started
---------------

From the project root is possible to launch a Debian machine with two
configurated network interfaces:

    $ vagrant up
    ==> default: Checking if box 'puphpet/debian75-x64' is up to date...
    ==> default: Clearing any previously set forwarded ports...
    ==> default: Clearing any previously set network interfaces...
    ==> default: Preparing network interfaces based on configuration...
        default: Adapter 1: nat
        default: Adapter 2: hostonly
    ==> default: Forwarding ports...
        default: 22 => 2222 (adapter 1)
    ==> default: Booting VM...
    ==> default: Waiting for machine to boot. This may take a few minutes...
        default: SSH address: 127.0.0.1:2222
        default: SSH username: vagrant
        default: SSH auth method: private key
        default: Warning: Connection timeout. Retrying...
    ==> default: Machine booted and ready!
    ==> default: Checking for guest additions in VM...
    ==> default: Configuring and enabling network interfaces...
    ==> default: Mounting shared folders...
        default: /vagrant => /path/to/project/root/
    ==> default: Machine already provisioned. Run `vagrant provision` or use the `--provision`
    ==> default: to force provisioning. Provisioners marked to run always will still run.

The box is provisioned with a simple script that copy the vagrant key into the ``authorized_keys``
of the ``root`` user so to make more easy using ansible after.

To provisioning this machine you have already some preconfigured files ready to use, you have only to do

    $ bin/manage provision vagrant