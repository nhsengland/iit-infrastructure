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
cd "$USER_HOME"
python download.py "$1"

# Untar/gunzip it
rm -rf "$restore_dir"
mkdir "$restore_dir"
mv "backup-$1.tgz" "$restore_dir/"

tar xfz "$restore_dir/backup-$1.tgz" --directory="$restore_dir"

# Kick some services in an appropriate way so restore isn't blocked.
sudo service apache2 stop
sudo service postgresql restart

# Restore the databases.
sudo /usr/lib/ckan/default/bin/paster --plugin=ckan db clean -c /etc/ckan/default/production.ini
sudo /usr/lib/ckan/default/bin/paster --plugin=ckan db load -c /etc/ckan/default/production.ini "$restore_dir/ckan_default.sql"
sudo --user=postgres pg_restore --dbname="datastore_default" --clean --if-exists "$restore_dir/datastore_default.dump"

# Copy the filestore directory into the backup directory.
sudo cp -r "$restore_dir/default/"* /var/lib/ckan/default
# Ensure that the restored directories are read/writable by Apache
sudo chown -R www-data /var/lib/ckan/default
sudo chgrp -R www-data /var/lib/ckan/default

# Restart Apache
sudo service apache2 start

# Reindex SOLR:
/usr/lib/ckan/default/bin/paster --plugin=ckan user list -c /etc/ckan/default/production.ini search-index rebuild
