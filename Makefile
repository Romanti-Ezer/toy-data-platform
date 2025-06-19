DBT_IMAGE = movies_transform
DBT_TARGET ?= dev
NETWORK = platform-net

build: 
	docker build -t $(DBT_IMAGE) dbt/

dbt-shell:
	docker run --rm -v $(PWD)/dbt/$(DBT_IMAGE):/usr/app/$(DBT_IMAGE) \
	    -e DBT_TARGET=$(DBT_TARGET) \
	    -e DBT_TARGET_PATH=target/$(DBT_TARGET) \
	    -p 8082:8082 \
	    --env-file $(PWD)/dbt/.env \
		--network $(NETWORK) \
		-w /usr/app/$(DBT_IMAGE) -it $(DBT_IMAGE) \
		bash

docs-generate:
	docker run --rm \
	  -v $(PWD)/dbt/$(DBT_IMAGE):/usr/app/$(DBT_IMAGE) \
	  --env-file $(PWD)/dbt/.env \
	  -e DBT_TARGET=$(DBT_TARGET) \
	  --network $(NETWORK) \
	  -w /usr/app/$(DBT_IMAGE) \
	  $(DBT_IMAGE) \
	  dbt docs generate

docs: docs-generate
	docker run --rm \
	  -v $(PWD)/dbt/$(DBT_IMAGE):/usr/app/$(DBT_IMAGE) \
	  --env-file $(PWD)/dbt/.env \
	  -e DBT_TARGET=$(DBT_TARGET) \
	  -p 8082:8082 \
	  --network $(NETWORK) \
	  -w /usr/app/$(DBT_IMAGE)/target \
	  -it $(DBT_IMAGE) \
	  python3 -m http.server 8082