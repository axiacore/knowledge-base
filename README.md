# Knowledge Base

[![Code Climate](https://codeclimate.com/github/Axiacore/knowledge-base/badges/gpa.svg)](https://codeclimate.com/github/Axiacore/knowledge-base)

Knowledge Base written in Django.

Copy `local_settings.py.template` to `local_settings.py` and fill in your
information. Have in mind that `SITE_URL` should be the url where you are
hosting this project, and `ALLOWED_DOMAINS` should be the domains of the emails 
that are allowed to login and view private articles.

![](https://s3.amazonaws.com/uploads.hipchat.com/50553/714369/WlN0IzjIc3cMqJc/screenshot.png)

## Running

Just do:

```bash
$ docker-compose up
```

## Commands

Running gulp to have livereload on templates and frontend files:

```bash
$ docker exec -it knowledgebase_web_1 gulp
```

To run any command on the app container you can do:

```bash
$ docker exec -it knowledgebase_web_1 python manage.py createsuperuser
$ docker exec -it knowledgebase_web_1 python manage.py shell_plus
$ docker exec -it knowledgebase_web_1 python manage.py test --failfast
$ docker exec -it knowledgebase_web_1 bash
```

## Upgrade packages

To upgrade packages version run:

```bash
$ docker exec -it knowledgebase_web_1 piprot --latest --verbatim
```

## Update translation strings

```bash
$ docker exec -it knowledgebase_web_1 django-admin makemessages -l es_CO
$ docker exec -it knowledgebase_web_1 django-admin compilemessages
```

## Improve

Check out the project licence and report issues or fork this project at
https://github.com/Axiacore/knowledge-base
