init:
	pip install -r requirements.txt

create_user_db:
	docker exec --user postgres pokepare_db /bin/sh -c "createuser pokepare -s && createdb -U pokepare pokepare"

migrate_db:
	docker exec pokepare_py /bin/sh -c 'python manage.py migrate'

feed_db:
	docker exec pokepare_py /bin/sh -c 'python db_feeding.py'

cov_test:
	docker exec pokepare_py /bin/sh -c 'coverage run manage.py test'

cov_report:
	docker exec pokepare_py /bin/sh -c 'coverage report'

build:
	docker-compose build

build-no-cache:
	docker-compose build --no-cache

up:
	docker-compose up -d

up-no-d:
	docker-compose up

restart:
	docker-compose restart

collectstatic:
	docker exec pokepare_py /bin/sh -c "python manage.py collectstatic --noinput"

shell-nginx:
	docker exec -ti pokepare_nginx bash

shell-web:
	docker exec -ti pokepare_py bash

shell-db:
	docker exec -ti pokepare_db bash