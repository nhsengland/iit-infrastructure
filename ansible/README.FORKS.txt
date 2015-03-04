
0.  Install Ansible, and clone this repository.
0.1 Obtain the relevant .pem and vault password files

1. Edit hosts file to set the following varialbes: 

[webservers]
52.16.151.114

[dbservers]
52.16.151.114

[solr]
52.16.151.114

2. Edit the forks.yml to point at the correct branch.

3. From this directory, run the command: 

   ansible-playbook -i hosts hebe.yml --vault-password-file vault.txt

4. Repeat steps 1-3 as often as needed.

5. There is no step 5

6. Profit.
