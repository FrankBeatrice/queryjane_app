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

With this command, the installation of the following packages is executed:

Packages included in the `Dockerfile <https://github.com/augustakingfoundation/queryjane_app/blob/master/Dockerfile>`_ (System requirements).

* Python:3.6.0
* Postgis:9.6
* Redis:4.0.8
* LibSass:3.4.4
* Gulp:3.9.1
* Yarn:1.7.0

Packages included in the `requirements.txt <https://github.com/augustakingfoundation/queryjane_app/blob/master/requirements.txt>`_ file (Python requirements).

* Django==1.11.4
* psycopg2==2.6.2
* Pillow==3.3.1
* huey==1.6.1
* boto3==1.4.6
* twython==3.6.0
* pygeoip==0.3.2
* Sphinx==1.7.5
* social-auth-app-django==2.1.0
* django-widget-tweaks==1.4.1
* django-storages==1.6.5
* django-extensions==1.7.4
* django-countries==4.6.2
* django-redis-cache==1.7.1
* django-model-utils==3.1.1

If there is a change in the *requirements.txt* file, the ``docker-compose build`` must be executed.


===========================
Running the project locally
===========================

Execute the following command to start the Docker container and enable the project locally:

``$ docker-compose up``

Now, you will be able to view the application homepage by visiting **localhost:8000** in a browser.

every time we execute this command, the tasks described in the `docker_compose.yml <https://github.com/augustakingfoundation/queryjane_app/blob/master/docker-compose.yml>`_ file will be executed:

1. Run the local server with the command:

``$ ./manage.py runserver 0.0.0.0:8000``

2. Enable Postgres and Redis services.

3. Check for Javascript and CSS requirements running the command:

``$ yarn install``

4. Run Gulp, to compress statics files with the command:

``$ gulp``

5. Run database migrations with the command:

``$ ./manage.py migrate --noinput``


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
