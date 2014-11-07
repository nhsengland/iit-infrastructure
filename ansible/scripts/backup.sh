#!/bin/sh

# This script creates a backup tgz file containing the following assets:
#
# 1. Dumps from Postgres of the CKAN databases.
# 2. A copy of the SOLR data directory.
# 3. A copy of CKAN's filestore directory.

# Set some useful variables.
USER_HOME=$(eval echo ~${SUDO_USER})
backup_dir="$USER_HOME/backup"
hostname=$(hostname -s)
date=`date '+%Y-%m-%d_%H-%M-%S'`
filename="$date-$hostname.tgz"
backup_target="$USER_HOME/$filename"

# Clean up and ensure the script is in a good state.
sudo rm -rf $backup_dir
rm *.tgz
mkdir -p "$backup_dir"

# Use pg_dump on the databases.
/usr/lib/ckan/default/bin/paster --plugin=ckan db dump -c /etc/ckan/default/production.ini "$backup_dir/ckan_default.sql"
sudo su - postgres -c "pg_dump datastore_default" > "$backup_dir/datastore_default.sql"
sudo su - postgres -c "pg_dump -Fc datastore_default" > "$backup_dir/datastore_default.dump"

# Copy the filestore directory into the backup directory. This will contain any
# newly uploaded data-source assets (it's just an extra source of safety in
# case the S3 push at the end fails).
sudo cp -r /var/lib/ckan/default "$backup_dir/default"

# Create the tgz
cd $backup_dir
tar cfz $backup_target .

# Upload to S3
cd $USER_HOME
python upload.py $backup_target

# Push any new data-source assets to S3
sudo /usr/lib/ckan/default/bin/paster --plugin=ckanext-s3archive s3archive archive -c /etc/ckan/default/production.ini
