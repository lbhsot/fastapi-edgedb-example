# FastAPI with EdgeDB Example Project

This is an example backend project using [fastapi](https://fastapi.tiangolo.com/) and [edgedb](https://www.edgedb.com/)

## Requirements

* [poetry](https://python-poetry.org/docs/#installation)
* [edgedb](https://www.edgedb.com/)

## Instructions

Clone the repository:

```bash
git clone https://github.com/lbhsot/fastapi-edgedb-example.git
cd fastapi-edgedb-example
```
Assuming our edgedb instance named `test_instance`

Edgedb DSN
```bash
echo "DB_DSN = test_instance" > .env
```

Setup edgedb 
```bash
edgedb project init
edgedb -I test_instance migrate
```
[Docs](https://www.edgedb.com/docs/cli/edgedb_project#edgedb-project-init) about `edgedb project init`

Install dependencies
```bash
poetry install
```

Run the server
```bash
poetry run uvicorn fastapi_edgedb_example.asgi:app --reload --host 0.0.0.0
```

Now you can visit [http://localhost:8000/ping](http://localhost:8000/ping) to check the result
