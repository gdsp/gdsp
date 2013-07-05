# gDSP – an online course in DSP ear training

## South database migrations

This project uses [South][south] migrations for database management. South
allows you to make changes to the database without dealing with raw SQL. The
workflow is as follows:

1. Make some change to a model which affects the database, e.g. add a field.
2. Create a migration for this change. If the change was made to a model in the
   `core` application, this is achieved by running:

        ./manage.py schemamigration core --auto

   If it's the first migration for an app, replace `--auto` with `--initial`.
3. Run the migration. In the case of the `core` application, this means
   running:

        ./manage.py migrate core

   To run the migrations for all installed apps, including third party ones
   such as `taggit`, simply run:

        ./manage.py migrate

**Note**: You need to run `./manage syncdb` once when you first set up the
project to prepare the database for South.

## SASS and Compass for stylesheets

The CSS for this project is generated from stylesheets written in [SASS][sass]
using the [Compass][compass] framework. Compass is a Ruby application which can
be installed using [RubyGems][rubygems] by running:

        [sudo] gem install compass

(At the time of writing, this will install `compass-0.12.2` and its dependencies
`sass`, `chunky_png` and `fssm`.)

To have Compass pick up on changes to SASS files when they're saved, navigate
into the `compass` directory and run:

        compass watch

For a one-off compilation, run:

        compass compile

from the same directory. Both will generate CSS from the files present in
`compass/sass` and write to files in `static/css` in accordance with the
settings in `compass/config.rb`.

## Python packages

The Python packages required by this project are listed in the file
`requirements.txt`. Assuming [pip][pip] is present, these packages can be
installed with:

        pip install -r requirements.txt

The file `requirements_dev.txt` includes all of `requirements.txt` as well as
packages that should only be installed in a development environment. Similarly,
`requirements_prod.txt` includes packages only needed in a production
environment. Both of these can be passed to `pip install` in the same way as
`requirements.txt`.

Using a [virtualenv][virtualenv] environment is a good idea, both in
development and production, as it allows you to maintain several different
Python environments on one system, as well as install packages without root
privileges. When using virtualenv with Apache and mod\_wsgi, [remember to set
the WSGIPythonPath][wsgipythonpath] or to [pass the right path to
WSGIDaemonProcess][wsgidaemonprocess].

## Configuration in a production environment

For security reasons, the database configuration and `SECRET_KEY` of the
project are kept out of Git. These settings, along with other configuration
variables which differ from development to production, are defined in the file
`gdsp/settings_prod.py`. In production, this file needs to be present and the
environment variable `DJANGO_PRODUCTION` needs to be set to a value which is
truthy in Python, e.g. `1`.

## Updating the application in production

Updating the running application is a simple matter of following these steps
from the root directory of the project:

1. Fetch the updated code:

        git pull origin master

2. If you have added any Python packages (third party applications or
   libraries), these need to be installed. Assuming that you've added these
   packages to either `requirements.txt` or `requirements_prod.txt`, that you
   are using `virtualenv` and that the `virtualenv` environment is kept in a
   directory `.virtualenv` in your project root, this is achieved like so:

        # Enter virtualenv; this assumes you are running bash.
        source .virtualenv/bin/activate

        # Install the packages. requirements_prod.txt includes all of
        # requirements.txt, so packages listed there will also be installed.
        pip install -r requirements_prod.txt

        # Leave virtualenv (if you want to).
        deactivate

3. If you have added any static files (CSS, JavaScript, images etc.), you need
   to collect these into the directory whence static files are served:

        # Enter virtualenv if you haven't already.
        source .virtualenv/bin/activate

        ./manage.py collectstatic

4. If you have made any changes to the database schema, i.e. you have added
   South migrations, you need to run these migrations:

        # Enter virtualenv if you haven't already.
        source .virtualenv/bin/activate

        ./manage.py migrate

5. Now restart the application. Assuming you are running Apache with mod\_wsgi
   in daemon mode, simply `touch` the WSGI application script:

        touch gdsp/wsgi.py

[south]: http://south.aeracode.org/ "South migration tool"
[sass]: http://sass-lang.com/ "SASS stylesheet language"
[compass]: http://compass-style.org/ "Compass framework"
[rubygems]: http://rubygems.org/ "RubyGems package manager"
[pip]: http://www.pip-installer.org/ "pip package manager"
[virtualenv]: http://www.virtualenv.org/ "virtualenv environment manager"
[wsgipythonpath]: https://docs.djangoproject.com/en/1.5/howto/deployment/wsgi/modwsgi/#using-a-virtualenv "Django documentation"
[wsgidaemonprocess]: https://docs.djangoproject.com/en/1.5/howto/deployment/wsgi/modwsgi/#using-mod-wsgi-daemon-mode "Django documentation"
