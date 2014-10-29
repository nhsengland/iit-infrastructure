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
--------------------

Simply run the following command in this directory and "it should just work" (tm)::

    ansible-playbook -i hosts site.yml --vault-pasword-file ~/.vault.txt

You will need to obtain the appropriate password through the usual channels.

If you need to deploy the website with SSL enabled (only do this if you're
deploying to data.england.nhs.uk) then remember to run::

    ansible-playbook -i hosts ssl.yml --vault-password-file ~/.vault.txt

Deploying changes to Ckanext NHSEngland
---------------------------------------

Simply run the following command in this directory and "it should just work" (tm)::

    ansible-playbook -i hosts deploy.yml --vault-password-file ~/.vault.txt


Rolling back changes to Ckanext NHSEngland
------------------------------------------

Rollbacks consist of checking out a previous version of the git repo and then restarting
Apache.

For your convenience, the handy rollback.yml playbook has been created to do just that !

You can roll back either to tags (by name), or to specific commits (by hash).

Example commandline usage:

     ansible-playbook -i hosts rollback.yml --extra-vars="tag=Alpha"
     ansible-playbook -i hosts rollback.yml --extra-vars="commit=ec8f7ae323bdfcc8baa68d669b913e4fd23fb999"

Database backup and restore
---------------------------

For the purposes of disaster recovery we need to regularly backup our database
and have a well understood mechanism for restoring the data. This is what
the backup.yml playbook is for.

The deployment playbook will deploy all the required scripts, credentials and
dependencies needed for backup and restore to occur. The basic modus operandi
is as follows for backup:

* A backup.sh script is scheduled to be run by the CRON daemon.
* This script takes a snapshot of both Postgres databases, copies the filestore, tgzips it all up and dumps it into the nhsebackups bucket on S3.
* The key for the backup is the hostname of the box from where the backup is being made.
* We use the "backupmonkey" user for this task (who has limited S3 access)
* The values stored in S3 are versioned.
* Each individual version gets moved to cold-storage after two weeks and deleted after three months (this is configured from within S3).
* Backups are scheduled to run every day at 1am.

The restore process is very simple:

* Find the backup you want to use within S3 and note the key name (it'll be something like ip-172-31-14-177)
* SSH into the new box that you want to restore the data to.
* As the ubuntu user run the restore script: ``restore.sh KEYNAME`` where KEYNAME is the name of the key you looked up earlier (e.f. ``restore.sh ip-172-31-14-177``)
* This script will grab the backup from S3, unzip it, stop Apache, restart Postgres (so pg_restore is not blocked by existing connections), use CKAN's blessed paster commands to clean then restore the main database (see http://docs.ckan.org/en/latest/maintaining/paster.html#dumping-and-loading-databases-to-from-a-file), use pg_restore to restore the datastore database (this may produce some errors that are safe to ignore), copy the filestore files back into the correct location and kick off a reindex by SOLR.

In order to ACTUALLY SET-UP SCHEDULED BACKUPS FOR AN INSTANCE you need to run
this playbook use the following command::

    ansible-playbook -i hosts backup.yml --vault-password-file ~/.vault.txt

This playbook simply uses the CRON daemon to schedule all the backup scripts
you first deployed when the new instance was created.
