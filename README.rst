=====
Django-C3
=====

Django-C3 is a simple Django app to generate simple charts with C3.js.
With Django-C3 you can using Django template engine tags and send data in with dictionary or list python types to that and your charts are ready!

Quick start
-----------

1. Add "django_c3" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_c3',
    ]


2. Add "C3_IMPORT = False" to setting.py if you want import C3 javascript libraries by yourself.

Output example:

.. image:: screenshot.png

There is "demo" directory in github repository (a compelete django project), you can see it to see a real example.
