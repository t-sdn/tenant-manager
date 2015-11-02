Tenant Manager
==============

Simple tenant manager for smoke testing.


Installation and Usage
----------------------

.. code-block:: console

   # Using pip for global installation.
   $ pip install --user -r requirements.txt

   # Using virtualenv.
   $ virtualenv venv
   $ source venv/bin/activate
   $ pip install -r requirements.txt

   # Using virtualenvwrapper.
   $ mkvirtualenv tenant-manager -a .
   $ pip install -r requirements.txt

   # Now, you can run it with uwsgi.
   # But before you run, set environment.
   $ export INTERFACE=ethX
   $ uwsgi uwsgi.ini

And you can open http://localhost:5000/ on your browser.
