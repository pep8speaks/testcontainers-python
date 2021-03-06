Database containers
===================

Allows to spin up docker database images such as MySQL, PostgreSQL, MariaDB and Oracle XE.

MySQL example
-------------

::

    def test_docker_run_mysql():
        config = MySqlContainer('mysql:5.7.17')
        with config as mysql:
            e = sqlalchemy.create_engine(mysql.get_connection_url())
            result = e.execute("select version()")
            for row in result:
                assert row[0] == '5.7.17'

It will spin up MySQL version 5.7. Then you can connect to database with credentials passed in constructor or just

call ``get_connection_url()`` method which returns sqlalchemy compatible url in format ``dialect+driver://username:password@host:port/database``.

PostgresSQL
-----------

Example of PostgresSQL database usage:

::

    def test_docker_run_postgress():
        postgres_container = PostgresContainer("postgres:9.5")
        with postgres_container as postgres:
            e = sqlalchemy.create_engine(postgres.get_connection_url())
            result = e.execute("select version()")
            for row in result:
                print("server version:", row[0])

Connection set by using raw python ``psycopg2`` driver for Postgres.

MariaDB
-------

Maria DB is a fork of MySQL database, so the only difference with MySQL is the name of Docker container.

::

    def test_docker_run_mariadb():
        mariadb_container = MariaDbContainer("mariadb:latest")
        with mariadb_container as mariadb:
            e = sqlalchemy.create_engine(mariadb.get_connection_url())
            result = e.execute("select version()")
            for row in result:
                assert row[0] == '10.1.22-MariaDB-1~jessie'

Oracle XE
---------

::

    oracle = OracleDbContainer()

    with oracle:
        e = sqlalchemy.create_engine(mysql.get_connection_url())
        result = e.execute("select 1 from dual")

It uses **https://hub.docker.com/r/wnameless/oracle-xe-11g/** docker image.

Connection detail for Oracle DB.

::

    hostname: localhost
    port: 49161
    sid: xe
    username: system
    password: oracle

Generic Database containers
---------------------------

Generally you are able to run any database container, but you need to configure it yourself.

Mongo example:

::

    def test_docker_generic_db():
        mongo_container = DockerContainer("mongo:latest")
        mongo_container.expose_port(27017, 27017)

        with mongo_container:
            @wait_container_is_ready()
            def connect():
                return MongoClient("mongodb://{}:{}".format(mongo_container.get_container_host_ip(),
                                                        mongo_container.get_exposed_port(27017)))

            db = connect().primer
            result = db.restaurants.insert_one(
                {
                    "address": {
                        "street": "2 Avenue",
                        "zipcode": "10075",
                        "building": "1480",
                        "coord": [-73.9557413, 40.7720266]
                    },
                    "borough": "Manhattan",
                    "cuisine": "Italian",
                    "name": "Vella",
                    "restaurant_id": "41704620"
                }
            )
            print(result.inserted_id)
            cursor = db.restaurants.find({"borough": "Manhattan"})
            for document in cursor:
                print(document)

