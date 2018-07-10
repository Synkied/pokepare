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