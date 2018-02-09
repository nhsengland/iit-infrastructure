Ansible Playbooks
=================

This directory contains Ansible (http://www.ansible.com/home) playbooks for
various sysop-y type "stuff".

Setup
-----

You need to have Ansible installed. Make sure it is a recent (>2.4) version or you will encounter
errors running the deb module.

The cleanest way to do this is with `pipsi <https://github.com/mitsuhiko/pipsi>`.  Full ansible docs here: http://docs.ansible.com/index.html

Make sure you create/update the hosts file to something like the following::

    [webservers]
    data.england.nhs.uk

    [dbservers]
    data.england.nhs.uk

    [solr]
    data.england.nhs.uk

    [publishomatic]
    data.endlang.nhs.uk

(Replace with the appropriate hostname[s] - look in hosts.example for hints)

Please ensure you have the correct keys (pem) for the instances you hope to manage.

Deploying
---------

Make sure you have the Ansible vault password in the .vault.txt file (available via the usual channels).

Simply run the following command in this directory and "it should just work" (tm) to install a test instance::

    ansible-playbook hosts deploy_test.yml --vault-password-file .vault.txt

This brings up an empty "basic" CKAN instance with NHSEngland branding.

If you want to deploy a "full" production type instance with all the bells and whistles, you need to type::

    ansible-playbook hosts deploy_prod.yml --vault-password-file .vault.txt

If you just want to deploy publish-o-matic then you need to run::

    ansible-playbook hosts deploy_publishomatic.yml --vault-password-file .vault.txt

Configuring publishomatic
-------------------------

For PoM to work correctly, it needs some settings in the .dc.ini file that it generates from ./config/dc.ini
In particular, it uses the following values from the group_vars/all file::

    {{ staging_url }} - The CKAN URL
    {{ staging_apikey }} - The CKAN API Key
    {{ AWS_SECRET_ACCESS_KEY }} and  {{ AWS_ACCESS_KEY_ID }}

To populate the config/dms.ini file it uses::

    {{publishomatic_notify_to}} - The recipient address for the nightly email.


Deploying changes to Ckanext NHSEngland
---------------------------------------

Simply run the following command in this directory and "it should just work" (tm)::

    ansible-playbook hosts update.yml --vault-password-file .vault.txt


Rolling back changes to Ckanext NHSEngland
------------------------------------------

Rollbacks consist of checking out a previous version of the git repo and then restarting Apache.

For your convenience, the handy rollback.yml playbook has been created to do just that!

You can roll back either to tags (by name), or to specific commits (by hash).

Example commandline usage::

     ansible-playbook hosts rollback.yml --extra-vars="tag=Alpha" --vault-password-file .vault.txt
     ansible-playbook hosts rollback.yml --extra-vars="commit=ec8f7ae323bdfcc8baa68d669b913e4fd23fb999" --vault-password-file .vault.txt

Database backup and restore
---------------------------

For the purposes of disaster recovery we need to regularly backup our database
and have a well understood mechanism for restoring the data. This is what
the backup.yml playbook is for.

Both the test and production playbooks will deploy all the required scripts, credentials and dependencies needed for backup and restore to occur. The prod playbook schedules the daily backup. The basic modus operandi is as follows for backup:

* A backup.sh script is scheduled to be run by the CRON daemon.
* This script takes a snapshot of both Postgres databases, copies the filestore, tgzips it all up and dumps it into the nhsebackups bucket on S3.
* The key for the backup is the hostname of the box from where the backup is being made.
* We use the "backupmonkey" user for this task (who has limited S3 access)
* The values stored in S3 are versioned.
* Each individual version gets moved to cold-storage after two weeks and deleted after three months (this is configured from within S3).
* Backups are scheduled to run every day at 1am.

The restore process is very simple:

* Find the backup you want to use (They will be named after the EC2 Private DNS IP Address) within S3 and note the key name (it'll be something like ip-172-31-14-177)
* SSH into the new box that you want to restore the data to.
* As the ubuntu user run the restore script: ``restore.sh KEYNAME`` where KEYNAME is the name of the key you looked up earlier (e.g. ``restore.sh ip-172-31-14-177``)
* This script will grab the backup from S3, unzip it, stop Apache, restart Postgres (so pg_restore is not blocked by existing connections), use CKAN's blessed paster commands to clean then restore the main database (see http://docs.ckan.org/en/latest/maintaining/paster.html#dumping-and-loading-databases-to-from-a-file), use pg_restore to restore the datastore database (this may produce some errors that are safe to ignore), copy the filestore files back into the correct location and kick off a reindex by SOLR.
