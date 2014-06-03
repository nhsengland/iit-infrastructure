"""
Upload some data to CKAN
"""
import datetime
import sys

import ckanapi
import dataconverters
import ffs

API_KEY = 'f3caf96d-ca74-4353-9eb0-6b446718d43d'

dev = ckanapi.RemoteCKAN('http://localhost:5000', apikey=API_KEY)
GP_ADDRS = 'https://indicators.ic.nhs.uk/download/GP%20Practice%20data/summaries/demography/Practice%20Addresses%20Final.xls'
TMP = ffs.Path.newdir()

def update_gp_addresses():
    packages = dev.action.package_list()
    print 'Making sure Package exists'
    if 'gp-practice-addresses' not in packages:
        dev.action.package_create(name='gp-practice-addresses', title='Locations of GP Practices')

    with TMP:
        print 'Converting Excel Spreadsheet'
        dataconverters.dataconvert(GP_ADDRS, 'gp.addresses.csv')
        csvfile = TMP/'gp.addresses.csv'

        with csvfile.open('r') as upload:
            print 'Creating Resource'
            resource = dev.action.resource_create(package_id='gp-practice-addresses',
                                       upload=upload,
                                       format='csv',
                                       name=datetime.datetime.now().strftime('%d-%m-%y-%H-%S'))
        with csvfile.csv() as csv:
            print 'Preparing data for datastore'
            fieldnames = csv.next()
            fields = [{"id": n, "type": "text"} for n in fieldnames]
            records = []
            for row in csv:
                records.append(dict(zip(fieldnames, row)))

            print 'Uploading to datastore'
            dev.action.datastore_create(
                force=True,
                resource_id=resource['id'],
                fields=fields,
                records=records
                )

    return 0

if __name__ == '__main__':
    sys.exit(update_gp_addresses())
