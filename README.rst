RSS feed parser
===============

Installation
------------

Create Python 3.6 environment and do the following:

.. code:: bash

    $ pip install -r requirements.txt

Running
-------

.. code:: bash

    $ make migrate # Run database migrations.
    $ make super # Create superuser.
    $ make # Run Django HTTP server.

Also you must to run Celery on the separate shell:

.. code:: bash

    $ make celery

Usage
-----

1. Open admin panel.
2. Add "Feed source" with any RSS URL you want (for instance: https://feeds.feedburner.com/PythonInsider).
3. Check this "Feed source" and click on "Parse selected feed sources" action.
