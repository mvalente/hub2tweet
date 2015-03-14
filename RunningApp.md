How to run the app:

Check it out.

Figure out where dev\_appserver.py lives:

$ which dev\_appserver.py

which should give you the full path, something like:
/usr/local/bin/dev\_appserver.py

Use python2.5 to run it in the directory you checked out (note the period for current workind directory).

$ python2.5 /usr/local/bin/dev\_appserver.py .

Then visit http://localhost:8080


To get OAuth configured, you have to visit /admin/oauth\_config and put in your Twitter OAuth token and secret.