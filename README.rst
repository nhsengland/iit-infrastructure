IIT Infrastructure
==================

Infrastructure, scripts, deployment, other for the NHSE IIT project

Setup
-----

pip install -r requirements.txt
ansible-galaxy install -r ansible/requirements.yml


Deployment
----------

Ansible is your friend. See ./ansible .

(We're assuming you're deploying to the recommended Ubuntu 12.04 release on AWS as the ubuntu user.)

Localization && Internationalization
------------------------------------

Unlike the OED [1], NHS England's style guidelines suggest that iz(e|a) is an incorrect verb ending for English.

In order to change these, and also to rename "Organizations" to "Publishers", we have translated CKAN.

The translation ckan.(mo|po) files are stored in the NHS England CKANext and checked into source control whenever a change is made.

We then change the CKAN internationalization directory setting to be our NHS England CKANext, which activates the translation.

In order to make this documentation comply with the NHS England style guide, please run the following command:

    perl -p -i -e 's/iz(?=a|e)/is/g' ./README.rst

[1] http://www.oxforddictionaries.com/words/ize-ise-or-yse
