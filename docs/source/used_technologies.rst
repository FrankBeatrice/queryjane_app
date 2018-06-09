Used technologies and requirements
==================================

QueryJane is a web application developed with `Python <https://www.python.org/>`_, using the web framework `Django <https://www.djangoproject.com/>`_.

The project is configured with `Docker <https://docker.com/>`_, that allows to setup a local enviroment to run the project in a very easy way.

The process to install the following packages is described in the next section, with the help of Docker.
The system prerequisites for properly configuring the project are:

============
Python:3.6.0
============

Python is an interpreted high-level programming language for general-purpose programming (`Taken from Wikipedia <https://en.wikipedia.org/wiki/Python_(programming_language)>`_).

Python is the main backend programming language, all the application logic has been implemented with Python.

===========
Postgis:9.6
===========

PostgreSQL, often simply Postgres, is an object-relational database management system (ORDBMS) with an emphasis on extensibility and standards compliance. (`Taken from Wikipedia <https://en.wikipedia.org/wiki/PostgreSQL>`_).

Postgres is the used database engine. In order to extend the application funcionalities for the future, we have installed and configured `PostGIS <https://postgis.net/>`_, a Postgres extension to manage spatial queries that supports geographic data.

===========
Redis:4.0.8
===========

Redis is an open-source in-memory database project implementing a distributed, in-memory key-value store with optional durability. Redis supports different kinds of abstract data structures, such as strings, lists, maps, sets, sorted sets, hyperloglogs, bitmaps and spatial indexes (`Taken from Wikipedia <https://en.wikipedia.org/wiki/Redis>`_).

The application executes second level tasks. For this reason we are using Redis, to temporarily store the information required to execute these tasks.

=============
LibSass:3.4.4
=============

Sass is the used stylesheet language. In this application we are using the `LibSass wrapper <https://sass-lang.com/libsass>`_, that allows to compile locally the stylesheets. `SASS C <https://github.com/sass/sassc>`_ is required to run the compiler locally.

==========
Gulp:3.9.1
==========


`Gulp.js <https://gulpjs.com/>`_  is a build system that allows to automate common development tasks. We are using it to minify JavaScript and CSS code and to compress images. `Node <https://nodejs.org/es/>`_ and 
`npm <https://www.npmjs.com/>`_ are prerequisites to run Gulp properly.

==========
Yarn:1.7.0
==========

`yarn <https://yarnpkg.com/lang/en/>`_ is used to install in a very easy way all the Javscript and CSS packages.


===============
Python packages
===============

The Required Python packages are listed in the `requirements.txt <https://github.com/augustakingfoundation/queryjane_app/blob/master/requirements.txt>`_ file. These are the necessary packages to development all the application functionalities:

Framework Web
-------------
Django==1.11.4

Python Libraries
----------------

* psycopg2==2.6.2
* Pillow==3.3.1
* huey==1.6.1
* boto3==1.4.6
* twython==3.6.0
* pygeoip==0.3.2
* Sphinx==1.7.5
* social-auth-app-django==2.1.0

Django libraries
----------------

* django-widget-tweaks==1.4.1
* django-storages==1.6.5
* django-extensions==1.7.4
* django-countries==4.6.2
* django-redis-cache==1.7.1
* django-model-utils==3.1.1

All these packages are easily installed and configured by using docker, and this is explained in the next section.
