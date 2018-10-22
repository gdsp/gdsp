The GDSP project code is release under GNU GPLv3. See LICENSE.TXT for details.

An attempt to document the gdsp project source code (work in progress)
======================================================================

1. Folders with code
--------------------

accounts: 
The Django project for user accounts and authorization (log in/out)

compass: 
Contains the layout file in .scss format that generates the css files when running compass and also a corresponding ruby config file.
* The file sass/application.scss is the main file for layout definitions

core:
The main Django project containing models, views and templates.

data:
The system subfolder Contains the Csound include files and some audio used to generate listening tests

gdsp:
The main project containing the basic settings.py and urls.py

pages:
Django project containing the static pages only (Home and About)

templates:
Contains some template files for the tutor and for admin

tutor:
The Django project for the automated tutor with code for tests. The subfolder modular contains python/csound code for generating tests


2. Folders with data
--------------------

Collected_static_files: 
Static files collected by the "manage.py collectstatic" command

static:
This is where static files are placed (images, javascripts, auto-generated css files, etc.)

uploaded_media:
Folder holding all data uploaded as project data (topic images, etc.)


3. Admin
--------

In file core/admin.py:

LessonAdmin:
* Inlines: TopicInline
* Forms: TopicInlineForm 
* Templates: admin/core/inline_topic.html
* Customizations: Ordering and "excluded content"-checkboxes

TopicAdmin:
* Inlines: BaseTopicElementInline (ordering!), ImageElementInline, etc.
* Templates: admin/core/inline_basetopicelement.html (BaseTopicElementInline)
* Customizations: Ordering (BaseTopicElementInline)

4. Template dependencies
------------------------

In folder templates:

base.html --> links to style template css/application.css
* Defines the top menu and some Java tools
* Also layout of login/out

In folder core/templates:

/core/base.html --> extends base.html
* Many Java tools (soundmanager, inlineplayer, mathjax)

/core/lessons/base.html --> extends /core/base.html
* Layout for the lesson sidebar

/core/lessons/index.html --> extends /core/lessons/base.html
* Called from LessonsListView
* Shows a bulleted list of lessons in the main window 

/core/lessons/lesson.html --> extends /core/lessons/base.html
* Called from LessonDetailView

/core/topics/index.html --> extends /core/base.html
* Called from TopicsListView

/core/topics/topic.html --> extends /core/base.html
* Called from TopicDetailView
