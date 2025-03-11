DBT_IMAGE = movies_transform
DBT_TARGET ?= dev
NETWORK = platform-net

build: 
	docker build -t $(DBT_IMAGE) dbt/

dbt-shell:
	docker run --rm -v $(PWD)/dbt/$(DBT_IMAGE):/usr/app/$(DBT_IMAGE) \
	    -e DBT_TARGET=$(DBT_TARGET) \
	    -e DBT_TARGET_PATH=target/$(DBT_TARGET) \
	    --env-file $(PWD)/dbt/.env \
		--network $(NETWORK) \
		-w /usr/app/$(DBT_IMAGE) -it $(DBT_IMAGE) \
		bash

docs:
	docker run --rm -v $(PWD)/dbt/$(DBT_IMAGE):/usr/app/$(DBT_IMAGE) \
	    -e DBT_TARGET=$(DBT_TARGET) \
	    -e DBT_TARGET_PATH=target/$(DBT_TARGET) \
	    --env-file $(PWD)/dbt/.env \
	    --network $(NETWORK) \
	    -w /usr/app/$(DBT_IMAGE) \
	    -it $(DBT_IMAGE) \
		bash -c "dbt docs generate && dbt docs serve --port 8080 --no-browser"
