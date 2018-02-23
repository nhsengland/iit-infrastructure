#!/bin/sh

# This script creates a backup tgz file containing the following assets:
#
# 1. Dumps from Postgres of the CKAN databases.
# 2. A copy of the SOLR data directory.
# 3. A copy of CKAN's filestore directory.

set -e

# Set some useful variables.
USER_HOME=$(eval echo "~${SUDO_USER}")
restore_dir="$USER_HOME/restored"

# Download from S3
cd "$USER_HOME" || (echo "failed to cd into user home" && exit 1)
"$USER_HOME/backup_env/bin/python" download.py "$1"
echo "Downloaded backup"

# Untar/gunzip it
rm -rf "$restore_dir"
mkdir "$restore_dir"
mv "backup-$1.tgz" "$restore_dir/"

tar xfz "$restore_dir/backup-$1.tgz" --directory="$restore_dir"
echo "Extracted backup"

# Kick some services in an appropriate way so restore isn't blocked.
sudo service apache2 stop
echo "Stopped Apache"

sudo service postgresql restart
echo "Restarted Postgres"

# Restore the databases.
sudo /usr/lib/ckan/default/bin/paster --plugin=ckan db upgrade --config=/etc/ckan/default/production.ini
echo "Upgraded database schema"

sudo /usr/lib/ckan/default/bin/paster --plugin=ckan db clean --config=/etc/ckan/default/production.ini

sudo --user=postgres pg_restore --dbname="ckan_default" --clean --if-exists "$restore_dir/ckan_default.dump"
echo "Restored database: ckan_default"
sudo --user=postgres pg_restore --dbname="datastore_default" --clean --if-exists "$restore_dir/datastore_default.dump"
echo "Restored database: datastore_default"

# Copy the filestore directory into the backup directory.
sudo cp -r "$restore_dir/default/"* /var/lib/ckan/default
# Ensure that the restored directories are read/writable by Apache
sudo chown -R www-data /var/lib/ckan/default
sudo chgrp -R www-data /var/lib/ckan/default
echo "Restored directory: /var/lib/ckan/default"

# Restart Apache
sudo service apache2 start
echo "Started Apache"

# Reindex SOLR:
/usr/lib/ckan/default/bin/paster --plugin=ckan search-index rebuild --config /etc/ckan/default/production.ini
