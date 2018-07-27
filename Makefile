init:
	pip install -r requirements.txt

create_user_db:
	docker exec --user postgres pokepare_db /bin/sh -c "createuser pokepare -s && createdb -U pokepare pokepare"

create_cache_table:
	docker exec pokepare_py /bin/sh -c "python manage.py createcachetable" 

migrate_db:
	docker exec pokepare_py /bin/sh -c 'python manage.py migrate'

import_data:
	docker exec pokepare_py /bin/sh -c 'python manage.py import_data all'

add_images_docker:
	docker exec pokepare_py /bin/sh -c 'python manage.py add_images all'

add_images:
	python manage.py add_images all

cov_test:
	coverage run manage.py test

cov_report:
	coverage report

build:
	docker-compose build

build_no_cache:
	docker-compose build --no-cache

up:
	docker-compose up -d

up_no_d:
	docker-compose up

restart:
	docker-compose restart

collectstatic:
	docker exec pokepare_py /bin/sh -c "python manage.py collectstatic --noinput"

bash_nginx:
	docker exec -ti pokepare_nginx bash

bash_web:
	docker exec -ti pokepare_py bash

bash_db:
	docker exec -ti pokepare_db bash

npm_build:
	cd frontend
	npm run build

freeze:
	pip freeze > requirements.txt