# FOR DEVELOPMENT

## Config the app

### In `app_config.py`
Set the following variables to the corresponding database you have:
* `database`: the name of database management system, e.g. postgresql
* `host`: the host name, e.g. localhost, 127.0.0.1
* `port`: the port for communicating with database, e.g. 5432 for postgresql
* `user_name`: the username for using the database
* `password`: the password for the username
* `database_name`: the name of the database in database management system

Comment the section for using with docker and the api_root_path.

### In `main.py`
Comment the line with the `api_root_path`.

## Run the API
Open the terminal in the current directory and run the following command:
```sh
python main.py
```
To run the migration, run the following command:
```sh
python -m ORM.migration.migration
```


---


# FOR USING THE APP WITH DOCKER
Open the `app_config.py` and comment the section for development and the api_root_path.  
Next, open the `main.py` and uncomment the line for using the api_root_path.  


---


# STRUCTURE OF `backend`

## [`ORM/`](ORM/)
Contains all the code to deal with database using [SQLAlchemy](https://www.sqlalchemy.org/).

### [`ORM/Base.py`](ORM/Base.py)
Declare the `Base` class, which is inherited by all Object Relational Mapper (ORM) class defined in `/ORM.Model.py`.

### [`/ORM/engine.py`](ORM/engine.py)
Declare the engine for the use of session. More information in [Engine Configuration](https://docs.sqlalchemy.org/en/14/core/engines.html).

### [`/ORM/Model.py`](ORM/Model.py)
Contains all ORM class definitions.

### [`/ORM/Model_description.py`](ORM/Model_description.py)
The description of all ORM classes and the relationship with other ORM.

### [`/ORM/migration/`](ORM/migration/) 
Contains the file for seeding data and data migration.

### [`/ORM/Commiter.py`](ORM/Commiter.py) 
Define the commiter using for create the commit for each transition in the system.

---

## [`controller/`](controller/)

### [`controller/BaseController.py`](controller/BaseController.py)
Contains the base class for other controller to inherit. For each model, there is a correspond controller for handling the logic of the each request. Refer to the file for more information.

---

## [`authentication/`](authentication/)

### [`authentication/login.py`](authentication/login.py)
Is the file for handling the login of user. It's will check the username and password provided by the user, create the access token and return the access token and token type in the response body as follow:
```json
{
    'access_token': <access_token_value>,
    'token_type': bearer
}
```
The client consuming this API should store the access token and token type somewhere e.g. Local Storage, in order to get authenticated in the next request. The request is authenticated only when it contain the header:
```http
Authorization: Bearer <access_token_value>
```

### [`authentication/registration.py`](authentication/registration.py)
Is the file for handling registration of a new user.

### [`authentication/authorization/auth_checker.py`](authentication/authorization/auth_checker.py)
Is the file for checking the authorization of authenticated user. The object created from `AuthorizationChecker` class will check in correspond with the schema provided by [`pydantic_models/Schema.py`](pydantic_models/Schema.py) whether:
* The user is an admin, which we call **require_admin** authorization
* The user is an owner of a resource instance, which we call **require_ownership** authorization.

To check when the `AuthorizationChecker` will check these two authorization, refer to class `Config` in each schema class in [`pydantic_models/Schema.py`](pydantic_models/Schema.py).

---

## [`pydantic_models/`](pydantic_models/)

### [`pydantic_models/Schema.py`](pydantic_models/Schema.py)
Contains all schema definitions for validating the request and filter the response. Refer to the file for more information.

---

## [`routes/`](routes/)

### [`routes/resource_registry.py`](routes/resource_registry.py)
Define which resource should be used to generate endpoints.

### [`routes/pof_generator.py`](routes/pof_generator.py)
Path Operation Function (POF) Generator contains 6 methods, which will generate 6 endpoints for each resource. Refer to the file for more information.

### [`routes/all_routes.py`](routes/all_routes.py)
Is where the `POFGenerator` will generate endpoints for each resource defined in [`routes/resource_registry`](routes/resource_registry).

### [`routes/special_routes.py`](routes/special_routes.py)
The routes, which do not follow 6 generic endpoint, but quite helpful for frontend to get all the needed data in a single request.

### [`routes/dependencies/`](routes/dependencies/)
Define dependencies for endpoints. View [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/) for more information.

The [`routes/dependencies/oauth2_scheme.py`](routes/dependencies/oauth2_scheme.py) defines the authentication scheme. More information in [Security - First Steps](https://fastapi.tiangolo.com/tutorial/security/first-steps/)

The [`routes/dependencies/user.py`](routes/dependencies/user.py) define the dependencies for authenticating user and get the current user if the access token is valid.

The [`routes/dependencies/db.py`](routes/dependencies/db.py) yield a new session for each request. The session will be created for each request and is closed after the response is sent.

---

## [`utils/`](utils/)

### [`utils/markdown_table_from_schema.py`](utils/markdown_table_from_schema.py)
Create the table in markdown language for schemas for POST and PATCH request in [`pydantic_models/Schema.py`](pydantic_models/Schema.py). The table will be shown in the interactive document to give the information about parameters in a request body of a POST or a PATCH request.