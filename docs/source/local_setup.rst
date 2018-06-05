Local setup
===========

We are using `Docker <https://docker.com/>`_  to isolate the development environment to have a single and stable operating system and libraries.


============
Installation
============

*Follow these steps located in the project root folder in a terminal.*

Generate a *local_settings.py* file by running the following command:

``$ test ! -e app/local_settings.py && cp app/test/local_settings.py.j2 app/local_settings.py``

This command will generate a file with *.py* extension inside the *app/* folder. The content of this file is taken from `local_settings.py.j2 <https://github.com/augustakingfoundation/queryjane_app/blob/master/app/test/local_settings.py.j2>`_.

With docker `installed <https://docs.docker.com/install/>`_ and running, execute the following command:

``$ docker-compose build``


===========================
Running the project locally
===========================

Execute the following command to start the Docker container and enable the project locally:

``$ docker-compose up``

Now, you will be able to view the application homepage by visiting **localhost:8000** in a browser.


========
Database
========

Since Docker does not come with database contents, you migth need to populate your database manually.

After adding some data, you can generate a database backup by running the following command:

``$ docker exec -t -u postgres queryjaneapp_db_1 pg_dumpall -c > dump.sql``


And to restore the database backup, run the following commands:

``$ docker exec queryjaneapp_db_1 psql --dbname=postgres --username=postgres --command="DROP SCHEMA public CASCADE;CREATE SCHEMA public;"``

``$ docker exec queryjaneapp_db_1 pg_restore dump.sql --dbname=postgres --username=postgres --no-owner``

You can connect to the database shell using this command:

``$ docker exec -it queryjaneapp_db_1 psql --dbname=postgres --username=postgres``
