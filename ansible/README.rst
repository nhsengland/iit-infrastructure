Ansible Playbooks
=================

This directory contains Ansible (http://www.ansible.com/home) playbooks for
various sysop-y type "stuff".

Setup
-----

You need to have Ansible installed. I simply created a virtualenv and pip installed ansible. Full docs here: http://docs.ansible.com/index.html

Make sure you create/update the hosts file to something like the following::

    [webservers]
    ec2-11-111-11-11.us-west-2.compute.amazonaws.com

    [dbservers]
    ec2-11-111-11-11.us-west-2.compute.amazonaws.com

    [solr]
    ec2-11-111-11-11.us-west-2.compute.amazonaws.com

(Replace with the appropriate hostname[s] - look in hosts.example for hints)

Please ensure you have the correct keys (pem) for the instances you hope to manage.

Deploying a new site
-----

Simply run the following command in this directory and "it should just work" (tm)::

    ansible-playbook -i hosts site.yml

Deploying changes to Ckanext NHSEngland
----------------------------------------

Simply run the following command in this directory and "it should just work" (tm)::

    ansible-playbook -i hosts deploy.yml


Rolling back changes to Ckanext NHSEngland
------------------------------------------

Rollbacks consist of checking out a previous version of the git repo and then restarting
Apache.

For your convenience, the handy rollback.yml playbook has been created to do just that !

You can roll back either to tags (by name), or to specific commits (by hash).

Example commandline usage:

     ansible-playbook -i hosts rollback.yml --extra-vars="tag=Alpha"
     ansible-playbook -i hosts rollback.yml --extra-vars="commit=ec8f7ae323bdfcc8baa68d669b913e4fd23fb999"
