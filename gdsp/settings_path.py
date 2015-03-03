# Django settings for gdsp project.

from os import path

# The root directory of our project; useful for building the paths below.
PROJECT_DIRECTORY = path.abspath(path.join(path.dirname(__file__), '..'))

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = path.join(PROJECT_DIRECTORY, 'uploaded_media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = path.join(PROJECT_DIRECTORY, 'collected_static_files')

# Absolute path to the data directory (used by the tutor)
DATA_ROOT = path.join(PROJECT_DIRECTORY, 'data/')


# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Don't forget to use absolute paths, not relative paths.
    path.join(PROJECT_DIRECTORY, 'static'),
)

TEMPLATE_DIRS = (
    # Don't forget to use absolute paths, not relative paths.
    path.join(PROJECT_DIRECTORY, 'templates')
)
