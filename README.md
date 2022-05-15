# STRUCTURE OF THE PROJECT
For each directory, refer to the `README.md` in each directory for more information.

## [`backend`](backend/)
Contains the code in backend to provide the API. The code is written in python with the use of FastAPI library.

## [`frontend`](frontend/)
Contains the code in frontend. The code is written in javascript with the use of ReactJS library.

## [`documentation`](documentation/)
Contains the documentation of the project.

## [`thesis`](thesis/)
Contains the thesis, which discuss about the idea of project in advance.

---


# FOR DEVELOPMENT
Follow the instruction in section **FOR DEVELOPMENT** in [`backend/README.md`](backend/README.md) and [`frontend/README.md`](frontend/README.md).


---


# FOR USING WITH DOCKER
Follow the instruction in section **FOR USING WITH DOCKER** in [`backend/README.md`](backend/README.md) and [`frontend/README.md`](frontend/README.md).  
To run the app, open the terminal in the current directory and run the following command

```sh
docker-compose -f docker-compose.product.yml up
```

In the first time run the app, we must run the migration. Run the following command in the terminal:

```sh
docker exec -it fastapi-app python -m ORM.migration.migration