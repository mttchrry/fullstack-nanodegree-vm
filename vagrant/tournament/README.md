# Tournament tracker with PostgreSQL database. 

In order to get started, follow the instructions at https://www.udacity.com/wiki/ud197/install-vagrant for installing VirtualBox and Vagrant, but USE THIS PARENT DIRECTORY instead of forking the git directory and cloning.  Then once you have the ssh open and logged in from this parent directory, run, in order, the following:

psql
\i tournament.psql 
\q
python tournement_test.py

That should show you the output of all the test running successfully.  Furthermore you can play around with the tables afterwards by using the standard psql commands. 