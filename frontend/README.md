# FOR DEVELOPMENT
## Config the app
Open the file [`src/config.js`](src/config.js) set the `domain` to the domain name of the api for example:
```js
const domain = 'http://www.localhost:8000'
```
## Run the app
Open the terminal in the current directory and run the following command:
```sh
npm start
```


---


# FOR USING WITH DOCKER
Open the file [`src/config.js`](src/config.js) set the `domain` as following:
```js
const domain = `http://localhost/api`
```


---


# STRUCTURE OF `frontend`
The `frontend` is created by the command:
```sh
npm create-react-app frontend
```
Therefore the directory has the structure of a react app. The main directory for development is the directory [`src/`](src) and its structure is described as follow:

## [`src/components/`](src/components/)
Contains all components for creating the frontend

## [`src/controllers/`](src/controllers/)
Contains the controller classes for communicating with the backend

## [`src/custom_hooks/`](src/custom_hooks/)
Contains the custom hooks for using with the pages and components

## [`src/pages/`](src/pages/)
Contains page component of the frontend. Each page component is a page in the frontend

## [`src/utils/`](src/utils/)
Contain the utilities function e.g. drawing the graf by using CytoscapeJS library, formatting date,...