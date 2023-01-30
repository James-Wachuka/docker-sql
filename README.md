#### docker-sql
This is part of data engineering zoomcamp week one module. Integrating postgres and docker and creating a script to ingest csv data into the database

####  postgres & pg-admin
1. using a bridge network
create a network pg-network for the two containers

use ``` docker network create pg-network```

```
postgres container
docker run -it \
  -e POSTGRES_USER="root"\
  -e POSTGRES_PASSWORD="root"\
  -e POSTGRES_DB="ny_taxi"\
  -v ${pwd}/ny_taxi_postgres_data:/var/lib/postgresql/data\
  -p 5432:5432\
  --network=pg-network\
  --name pg-database\
  postgres:13
```
pgadmin container
```
docker run -it \
   -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
   -e PGADMIN_DEFAULT_PASSWORD="root" \
   -p 8080:80 \
   --network=pg-network\
   --name pgadmin\
   dpage/pgadmin4
```
2. Using docker-compose file
we can create a service that runs postgres and pgadmin to avoid having to create network.

#### ingestion script
```wget``` is used to download the data and save in a csv file. We then build an image from the ingestion script in order to use with postgres & pgadmin containers, using the docker file.

We pass the following arguments when running the ingestion script in docker

```
docker run -it \
  --network=pg-network \ # the bridge network
  test_ingest:001 \ #name of the image
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \ 
    --url=http://127.0.0.1:8000/yellow_tripdata_2019-01.csv # data url
    ```



