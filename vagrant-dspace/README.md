Vagrant + DSpace = vagrant-dspace [![Build Status](https://secure.travis-ci.org/DSpace/vagrant-dspace.png?branch=master)](https://travis-ci.org/DSpace/vagrant-dspace)
=================================

[Vagrant](http://vagrantup.com) can be used to spin up a temporary Virtual Machine (VM) in a variety of providers ([VirtualBox](http://www.virtualbox.org), [VMWare](http://www.vmware.com/), [Amazon AWS](http://aws.amazon.com/), etc).

Simply put, 'vagrant-dspace' uses Vagrant and [Puppet](http://puppetlabs.com/) to auto-install latest DSpace on the VM provider of your choice (though so far we've mostly tested with VirtualBox).

Some example use cases for 'vagrant-dspace':
* Lets you easily install the latest version of DSpace on a Virtual Machine in order to try it out or test upgrades, etc.
* Lets you easily setup an offline/local copy of DSpace for demos at conferences or similar.
* Lets you quickly setup a DSpace development environment on a Virtual Machine. You'd need to install your IDE of choice, but besides that, everything else is installed for you.
* Vagrant VMs are "throwaway". Can easily destroy the VM and recreate at will for testing purposes or as needs arise (e.g. `vagrant destroy; vagrant up`)

This work began as a collaborative project between [tdonohue](https://github.com/tdonohue/) and [hardyoyo](https://github.com/hardyoyo/),
but has now been more broadly accepted.

_BIG WARNING: THIS IS STILL A WORK IN PROGRESS. YOUR MILEAGE MAY VARY. NEVER USE THIS IN PRODUCTION._


Table of Contents
-----------------

1. [How it Works](#how-it-works)
2. [Requirements - The prerequisites you need](#requirements)
3. [Getting Started - How to install and run 'vagrant-dspace'](#getting-started)
4. [What will you get? - What does the end result look like?](#what-will-you-get)
5. [Usage Tips - How to perform common activities in this environment](#usage-tips)
6. [How to Tweak Things to your Liking? - Tips on customizing the 'vagrant-dspace' install process](#how-to-tweak-things-to-your-liking)
7. [Vagrant Plugin Recommendations - Other plugins you may wish to consider installing](#vagrant-plugin-recommendations)
8. [Don't Miss These Really Cool Things You Can Do with Vagrant](#dont-miss-these-really-cool-things-you-can-do-with-vagrant)
9. [What's Next?](#whats-next)
10. [Reporting Bugs / Requesting Enhancements](#reporting-bugs--requesting-enhancements)
11. [License](#license)

How it Works
------------

'vagrant-dspace' does all of the following for you:

* Spins up an Ubuntu 16.04 LTS virtual machine using Vagrant
* Uses [puppet-dspace](https://github.com/DSpace/puppet-dspace) module to install:
    * Base prerequisities for DSpace development (Java, Maven, Ant, Git)
    * PostgreSQL 9.5 (via the [puppetlabs/postgresql](http://forge.puppetlabs.com/puppetlabs/postgresql) module)
    * Tomcat 7 (via the [puppetlabs/tomcat](https://forge.puppetlabs.com/puppetlabs/tomcat))
        * NOTE: currently using Tomcat 7 because of [DS-3142](https://jira.duraspace.org/browse/DS-3142) which is caused by Tomcat 8.0.32 (the 8.x version currently in use by Ubuntu 16.04)
    * DSpace (`master` by default)
* Sets up SSH Forwarding, so that you can use your local SSH key(s) on the VM (for development with GitHub)
* Syncs your local Git settings (name and email from local .gitconfig) to VM (for development with GitHub)
* Optionally sets up "sync folder", so that `~/dspace-src` on the VM is synced to `[vagrant-dspace]/dspace-src` on your host machine. This allows for IDE-based development. But, it's disabled by default (as it has slow performance)

Most of the magic happens in our [`Vagrantfile`](https://github.com/DSpace/vagrant-dspace/blob/master/Vagrantfile) which tells vagrant how to setup the VM.

However, the Puppet modules are all installed using [librarian-puppet](http://librarian-puppet.com/), see our [`Puppetfile`](https://github.com/DSpace/vagrant-dspace/blob/master/Puppetfile).

**If you want to help, please do.** We'd prefer solutions using [Puppet](https://puppetlabs.com/).

Requirements
------------

* [Virtualization support must be enabled](http://www.howtogeek.com/213795/how-to-enable-intel-vt-x-in-your-computers-bios-or-uefi-firmware/), if you have a BIOS-based computer (aka a PC).
* [Vagrant](http://vagrantup.com/) version 1.8.3 or above.
* [VirtualBox](https://www.virtualbox.org/)
* (Optional) A GitHub account with an associated SSH key. This is NOT required, but if you plan to do development on 'vagrant-dspace' and/or create Pull Requests, it is recommended. If you have a local [SSH agent](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/) running (or [Pageant/PuTTY](http://www.putty.org/) on Windows), Vagrant will attempt to automatically forward your local SSH key(s) to the VM, so that you will be able to immediately interact with GitHub via SSH on the VM. However, if you are *not* running a key agent, and your SSH key has a passphrase, Vagrant will *not* prompt you to enter a password, it will simply fail to run all the provisioning processes. We urge you to consider running a key agent with your SSH key, it will make your life so much more simple.
 * *WARNING:* If you are using an SSH key, we highly recommend that you use an RSA key. The base OS we use, Ubuntu 16.04LTS, uses OpenSSH 7.0, which [*disallows* DSA keys by default](http://viryagroup.com/what-we-do/our-blog-posts/hosting-and-linux-server-managment-blog/ssh-keys-failing-in-ubuntu-16-04-xenial-with-permission-denied-publickey). You can of course work around this, but OpenSSH made this choice for a reason, you will probably be happier in the long run if you switch to an RSA key.


Getting Started
--------------------------

**WINDOWS INSTRUCTIONS:** [detailed step-by-step installation instructions for setting up Vagrant-DSpace on Windows](https://github.com/DSpace/vagrant-dspace/blob/master/docs/WINDOWS_INSTRUCTIONS.md) can be found in the `docs` folder.

1. Install all required software (see above). Linux users take note: the versions of Vagrant and Virtualbox in your distribution's package manager are probably not current enough. Download and manually install the most recent version from [Vagrant](http://vagrantup.com) and [VirtualBox](https://www.virtualbox.org/). It will be OK. Both of these projects move quickly, and the distro managers have a hard time keeping up.
2. Clone a copy of 'vagrant-dspace' to your local computer (via Git)
   * `git clone git@github.com:DSpace/vagrant-dspace.git`
   * If you don't have Git installed locally, you should be able to simply download the [latest 'vagrant-dspace' from GitHub (as a ZIP)](https://github.com/DSpace/vagrant-dspace/archive/master.zip)
4. `cd [vagrant-dspace]/`
5. `vagrant up`
   * Wait for ~15 minutes while Vagrant & Puppet do all the heavy lifting of cloning GitHub & building & installing DSpace.
   * There may be times that vagrant will appear to "stall" for several minutes (especially during the Maven build of DSpace). But, don't worry.
6. Once complete, visit `http://localhost:8080/xmlui/` or `http://localhost:8080/jspui/` in your local web browser to see if it worked! _More info below on what to expect._
   * If you already have something running locally on port 8080, vagrant-dspace will attempt to use the next available port between 8081 and 8100. The default port is also configurable by creating a `config/local.yaml` (see below for more details)

Once complete, you'll have a fresh Ubuntu VM that you can SSH into by simply typing `vagrant ssh`. Since SSH Forwarding is enabled, that Ubuntu VM should have access to your local SSH keys, which allows you to immediately use Git/GitHub.

***
**NOTE:** sometimes when `vagrant up` finishes running, you will see a message like this:

```
Booting VM...
SSH connection was refused! This usually happens if the VM failed to
boot properly. Some steps to try to fix this: First, try reloading your
VM with 'vagrant reload', since a simple restart sometimes fixes things.
If that doesn't work, destroy your VM and recreate it with a 'vagrant destroy'
followed by a 'vagrant up'. If that doesn't work, contact a Vagrant
maintainer (support channels listed on the website) for more assistance.
```

This is normal, the VM just took a while longer to boot than Vagrant wanted to wait. Don't lose hope, you can still run `vagrant ssh` and very likely the machine will be ready for you. Especially if you've wandered off during the `vagrant up` command.
***

What will you get?
------------------

* A running instance of [DSpace 'master'](https://github.com/DSpace/DSpace), on top of latest PostgreSQL and Tomcat (and using Java OpenJDK 8 by default)
   * You can visit this instance at `http://localhost:8080/xmlui/` or `http://localhost:8080/jspui/` from your local web browser
       * If you install and configure the [Landrush plugin](https://github.com/phinze/landrush) for Vagrant, you can instead visit http://dspace.vagrant.dev:8080/xmlui/ or http://dspace.vagrant.dev:8080/jspui/
   * An initial Administrator account is also auto-created (this account can be tweaked in a `config/local.yaml` file, see below)
       * Default Login: `dspacedemo+admin@gmail.com` , Default Pwd: 'vagrant'
* DSpace GitHub cloned (at `~/dspace-src/`) and Java/Maven/Ant/Git installed.
   * If `sync_src_to_host=true` in your `config/local.yaml`, then this VM directory will also be synce to `[vagrant-dspace]/dspace-src` on your host machine.  
* All "out of the box" DSpace webapps running out of `~/dspace/webapps/`. The full DSpace installation is at `~/dspace/`.
* Tomcat instance installed
   * Includes [PSI Probe](http://code.google.com/p/psi-probe/) running at `http://localhost:8080/probe/`
       * PSI Probe Login: 'dspace', Pwd: 'dspace'
* Enough to get you started with developing/building/using DSpace (or debug issues with the DSpace build process, if any pop up)
   * Though you may wish to install your IDE of choice.
* A very handy playground for testing multiple-machine configurations of DSpace, and software that might utilize DSpace as a service

If you want to destroy the VM at anytime (and start fresh again), just run `vagrant destroy`.
No worries, you can always recreate a new VM from scratch with another `vagrant up`.

As you develop with 'vagrant-dspace', from time to time you may want to run a `vagrant destroy` cycle (followed by a fresh `vagrant up`), just to confirm that the Vagrant setup is still doing exactly what you want it to do.
This cleans out any old experiments and starts fresh with a new base image. If you're just using vagrant-dspace for dspace development, this isn't advice for you.
But, if you're working on contributing back to vagrant-dspace, do try this from time to time, just to sanity-check your Vagrant and Puppet scripts.

Usage Tips
------------

Here's some common activities which you may wish to perform in `vagrant-dspace`:

* **Restarting Tomcat**
   * `sudo service tomcat7 restart`
* **Restarting PostgreSQL**
   * `sudo service postgresql restart`
* **Connecting to DSpace PostgreSQL database**
   * `psql -h localhost -U dspace dspace`  (Password is "dspace")
* **Rebuilding / Redeploying DSpace**
   * `cd ~/dspace-src/`  (Move into source directory)
   * `mvn clean package` (Rebuild/Recompile DSpace)
   * `cd dspace/target/dspace-installer` (Move into the newly built installer directory)
   * `ant update`   (Redeploy changes to ~/dspace/)
   * `sudo service tomcat7 restart` (Reboot Tomcat)


How to Tweak Things to your Liking?
-----------------------------------

### local.yaml - Your local settings go here!

If you look at the `config` folder, there are a few files you'll be interested in. The first is `default.yaml`, it's a YAML configuration file (which is loaded by Vagrantfile to configure Vagrant, as well as loaded by Hiera to configure Puppet). You may copy this file to one named `local.yaml`. Any changes to `local.yaml` will override the defaults set in the `default.yaml` file. The `local.yaml` file is ignored in `.gitignore`, so you won't accidentally commit it. Here are the basic options (see the `default.yaml` for more):

* `vm_name` - Name of the Virtual Machine to create (default is usually fine)
* `vm_memory` - Specify the amount of memory to give this VM (2GB by default)
* `vm_cpu_max` - Limit the amount of local CPU this VM can access (off by default)
* `ip_address` - Local IP address to assign to the VM
* `port` - Local port this VM should use for Tomcat (port 8080 by default)
* `db_port` - Local port where VM's PostgreSQL database will be accessible (port 5432 by default). This lets you manage the VM database locally via tools like pgAdminIII, and debug code in your local IDE while using the VM database for "test" data.
* `sync_src_to_host` - Whether or not to auto-sync the `~/dspace-src/` folder on the VM to the `[vagrant-dspace]/dspace-src/` folder on your host machine. By default this is false as the sync folder currently is often slow. But, if you want to work in a local IDE, you probably will want this to be set to "true".
* `dspace::git_repo` - it would be a good idea to point this to your own fork of DSpace. By default this is a GitHub SSH URL. But, if vagrant-dspace is unable to connect to GitHub via SSH, this will be dynamically changed to a GitHub HTTPS URL.
* `dspace::git_branch` - if you're constantly working on another brach than master, you can change it here
* `dspace::admin_firstname` - you may want to change this to something more memorable than the demo DSpace user
* `dspace::admin_lastname` - ditto
* `dspace::admin_email` - likewise
* `dspace::admin_passwd` - you probably have a preferred password
* `dspace::admin_language` - and you may have a language preference, you can set it here
* `dspace::mvn_params` - add other maven prameters here (this is added to the Vagrant user's profile, so these options are always on whenever you run mvn as the Vagrant user)
* `dspace::handle_prefix` - Handle prefix to use for the DSpace in your VM (Default=`123456789`). This is handy to set if you want to auto-load content using `local-bootstrap.sh` (see below).
* `dspace::catalina_opts` - the default CATALINA_OPTS setting for Tomcat. This allows you to tweak the amount of memory available to Tomcat (1GB by default)

### local-bootstrap.sh - You can script your own tweaks/customizations!

In the `config` folder, you will also find a file called `local-bootstrap.sh.example`. If you copy that file to `local-bootstrap.sh` and edit it to your liking (it is well-commented) you'll be able to customize your git clone folder to your liking (turning on the color.ui, always pull using rebase, set an upstream github repository, add the ability to fetch pull requests from upstream), as well as automatically batch-load content (an example using AIPs is included, but you're welcome to script whatever you need here... if you come up with something interesting, please consider sharing it with the community).

`local-bootstrap.sh` is a "shell provisioner" for Vagrant, and our [`Vagrantfile`](https://github.com/DSpace/vagrant-dspace/blob/master/Vagrantfile) is configured to run it, if it is present in the `config` folder. If you have a fork of vagrant-dSpace for your own repository management, you may add another shell provisioner, to maintain your own workgroup's customs and configurations. You may find an example of this in the [Vagrant-MOspace](https://github.com/umlso/vagrant-mospace/blob/master/config/mospace-bootstrap.sh) repository.

### apt-spy-2-bootstrap.sh - You can override the default apt-spy-2-bootstrap.sh script

Apt-spy2 is used to locate a nearby apt repository mirror, which should help speed up the startup of your VM (as packages should download more quickly).

The default `apt-spy-2-bootstraph.sh` script can be copied to the `config` folder and modified to reflect your preferences. This can potentially speed up provisiong of new machines by allowing you to tweak the `apt-spy2` commands to better fit your typical work conditions. We of course recommend using the default, especially if you do not know for sure where your travels may take you next. But, you are free to tinker with this script as you see fit.

### maven_settings.xml - Tips on tweaking Maven

If you've copied the example `local-bootstrap.sh` file, you may create a `config/dotfiles` folder, and place a file called `maven_settings.xml` in it, that file will be copied to `/home/vagrant/.m2/settings.xml` every time the `local-bootstrap.sh` provisioner is run. This will allow you to further customize your Maven builds. One handy (though somewhat dangerous) thing to add to your `settings.xml` file is the following profile:
```
  <profile>
    <id>sign</id>
    <activation>
      <activeByDefault>true</activeByDefault>
    </activation>
    <properties>
      <gpg.passphrase>add-your-passphrase-here-if-you-dare</gpg.passphrase>
    </properties>
  </profile>
```

NOTE: any file in `config/dotfiles` is ignored by Git, so you won't accidentally commit it. But, still, putting your GPG passphrase in a plain text file might be viewed by some as foolish. If you elect to not add this profile, and you DO want to sign an artifact created by Maven using GPG, you'll need to enter your GPG passphrase quickly and consistently. Choose your poison.

### vim and .vimrc - Tips on using/tweaking VIM

Another optional `config/dotfiles` folder which is copied (if it exists) by the example `local-bootstrap.sh` shell provisioner is `config/dotfiles/vimrc` (/home/vagrant/.vimrc) and `config/dotfiles/vim` (/home/vagrant/.vim). Populating these will allow you to customize (Vim)[http://www.vim.org/] to your heart's content.

Vagrant Plugin Recommendations
-------------------------------
Vagrant has a robust community of plugin developers, and some of the plugins are quite nice. [Installing a Vagrant plugin](https://www.vagrantup.com/docs/plugins/usage.html) is simple.

The following Vagrant plugin is *required*, if you use the default [ubuntu/xenial](https://app.vagrantup.com/ubuntu/boxes/xenial64) base box (in other words, if you don't change the default, you'll *need* this plugin).

* [Vagrant-Disksize](https://github.com/sprotheroe/vagrant-disksize) - may not be required if you use another base box, but we've tested it and confirmed it works with the ubuntu/xenial base box.


The following Vagrant plugins are not required, but they do make using Vagrant and vagrant-dspace more enjoyable.

* [Vagrant-VBGuest](https://github.com/dotless-de/vagrant-vbguest) - *Highly Recommended for VirtualBox* as it keeps VirtualBox Guest Additions up to date
  * `vagrant plugin install vagrant-vbguest`
* [Vagrant-Cachier](https://github.com/fgrehm/vagrant-cachier) - Caches packages between VMs. (Project now unmaintained, see URL)
* [Vagrant-Hostsupdater](https://github.com/cogitatio/vagrant-hostsupdater)
* [Vagrant-Proxyconf](https://github.com/tmatilai/vagrant-proxyconf/)
* [Vagrant-VBox-Snapshot](https://github.com/dergachev/vagrant-vbox-snapshot/)
* [Vagrant-Notify](https://github.com/fgrehm/vagrant-notify)

Don't miss these really cool things you can do with Vagrant
-----------------------------------------------------------
* [Vagrant Share](http://docs.vagrantup.com/v2/share/) requires a free login on [HashiCorp's Atlas](https://atlas.hashicorp.com/), allows you to share your Vagrant environment with anyone in the world, enabling collaboration directly in your Vagrant environment in almost any network environment. It can be used to demo functionality (or bugs) with other developers, and can even enable a sort of pair programming. OK, maybe not really, but you can at least collaborate more than before.

What's Next?
------------

Here are a few things we'd like to explore in future version of vagrant-dspace:

* use a CentOS base machine, and make all Puppet provisioning modules compatible with a Yum-based package manager. The current vagrant-dspace project relies on a package only available on Debian-based systems. We'd really like to avoid that dependency in the future.
* Oracle database version?
* [Multi-machine](http://docs.vagrantup.com/v2/multi-machine/index.html) configuration, to demonstrate proper configuration of multi-machine installations of DSpace. One possibility would be to set up a separate Elastic Search or Solr box, and send usage statistics to that external box. Another possibility would be to explore using an alternate UI based on the REST-API. We recommend that you use the Land Rush Vagrant plugin if you're serrious about exploring a multi-machine Vagrant setup.

Reporting Bugs / Requesting Enhancements
----------------------------------------

Bugs / Issues or requests for enhancements can be reported via the [DSpace Issue Tracker](https://jira.duraspace.org/browse/DS). _Please select the "vagrant-dspace" component when creating your ticket in the issue tracker._

We also encourage you to submit Pull Requests with any recommended changes/fixes. As it is, the `vagrant-dspace` project is really just a labor of love, and we can use help in making it better.

License
--------

This work is licensed under the [DSpace BSD 3-Clause License](http://www.dspace.org/license/), which is just a standard [BSD 3-Clause License](http://opensource.org/licenses/BSD-3-Clause).
