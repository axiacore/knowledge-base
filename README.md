# Knowledge Base

Knowledge Base written in Django.

## Running

Just do:

    $ docker-compose up


## Commands

Running gulp to have livereload on templates and frontend files:

    $ docker exec -it knowledgebase_web_1 gulp

To run any command on the app container you can do:

    $ docker exec -it knowledgebase_web_1 python manage.py createsuperuser
    $ docker exec -it knowledgebase_web_1 python manage.py shell_plus
    $ docker exec -it knowledgebase_web_1 python manage.py test --failfast
    $ docker exec -it knowledgebase_web_1 bash


## Upgrade packages

To upgrade packages version run:

    $ docker exec -it knowledgebase_web_1 piprot --latest --verbatim


## Update translation strings

    $ docker exec -it knowledgebase_web_1 django-admin makemessages -l es_CO
    $ docker exec -it knowledgebase_web_1 django-admin compilemessages
