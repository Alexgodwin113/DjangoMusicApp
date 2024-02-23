MyMusic Maestro
===============

Instructions for marking
------------------------

Write here any extra instructions or notes for marking.

Put any extra requirements in requirements.txt.

Structure
---------

Project structure is as follows:
1. /MyMusicMaestro -- configuration directory for project
2. /templates -- project-wide shared templates
3. /static -- project-wide shared static resources
4. /locale -- project-wide string localisation
5. /media -- user-uploaded file directory
6. /app_pages -- pages sub-app for public pages, e.g., landing page, help page, about page
7. /app_album_viewer -- viewer/editor sub-app for album management functionality

The sub-apps have the following nested structure:
1. /app_NAME/locale/ -- translations specific to the sub-app
2. /app_NAME/migrations/ -- migrations specific to the sub-app, if applicable
3. /app_NAME/templates/ -- view templates specific to the sub-app
4. /app_NAME/[apps,urls,models,views,tests,admin].py -- Django setup and code for each sub-app


Credits
-------

Album icons from Openclipart.
