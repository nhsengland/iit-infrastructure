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
