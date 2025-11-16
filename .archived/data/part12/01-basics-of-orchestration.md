---{
  "title": "Basics of Orchestration",
  "source_url": "https://fullstackopen.com/en/part12/basics_of_orchestration",
  "crawl_timestamp": "2025-10-04T19:15:55Z",
  "checksum": "bc006858b803be176a4f3f771906338972d70d7c4be65632d5d2b244be87d797"
}
---[Skip to content](../part12/01-basics-of-orchestration-course-main-content.md)
[{() => fs}](https://fullstackopen.com/en/)

- [About course](../about/01-about.md)
- [Course contents](../#course-contents/01-course-contents.md)
- [FAQ](../faq/01-faq.md)
- [Partners](../companies/01-companies.md)
- [Challenge](../challenge/01-challenge.md)
[Search from the material](../search/01-search.md)Toggle dark theme
Select languageSuomi English 中文 Español Français Português(BR)

[Fullstack](../#course-contents/01-course-contents.md)
[Part 12](../part12/01-part12.md)
Basics of Orchestration
[a Introduction to Containers](../part12/01-introduction-to-containers.md)[b Building and configuring environments](../part12/01-building-and-configuring-environments.md)
c Basics of Orchestration

- [React in container](../part12/01-basics-of-orchestration-react-in-container.md)
- [Using multiple stages](../part12/01-basics-of-orchestration-using-multiple-stages.md)
- [Exercises 12.13 - 12.14.](../part12/01-basics-of-orchestration-exercises-12-13-12-14.md)
- [Development in containers](../part12/01-basics-of-orchestration-development-in-containers.md)
- [Exercise 12.15](../part12/01-basics-of-orchestration-exercise-12-15.md)
- [Communication between containers in a Docker network](../part12/01-basics-of-orchestration-communication-between-containers-in-a-docker-network.md)
- [Exercise 12.16](../part12/01-basics-of-orchestration-exercise-12-16.md)
- [Communications between containers in a more ambitious environment](../part12/01-basics-of-orchestration-communications-between-containers-in-a-more-ambitious-environment.md)
- [Exercises 12.17. - 12.19.](../part12/01-basics-of-orchestration-exercises-12-17-12-19.md)
- [Tools for Production](../part12/01-basics-of-orchestration-tools-for-production.md)
- [Exercises 12.20.-12.22.](../part12/01-basics-of-orchestration-exercises-12-20-12-22.md)
- [Submitting exercises and getting the credits](../part12/01-basics-of-orchestration-submitting-exercises-and-getting-the-credits.md)


c
# Basics of Orchestration
The part was updated 21th Mar 2024: Create react app was replaced with Vite in the todo-frontend.
If you started the part before the update, you can see
We have now a basic understanding of Docker and can use it to easily set up eg. a database for our app. Let us now move our focus to the frontend.
### React in container
Let's create and containerize a React application next. We start with the usual steps:

```
npm create vite@latest hello-front -- --template react
cd hello-front
npm installcopy
```

The next step is to turn the JavaScript code and CSS, into production-ready static files. Vite already has _build_ as an npm script so let's use that:

```
$ npm run build
  ...

  Creating an optimized production build...
  ...
  The build folder is ready to be deployed.
  ...copy
```

Great! The final step is figuring out a way to use a server to serve the static files. As you may know, we could use

```
FROM node:20

WORKDIR /usr/src/app

COPY . .

RUN npm ci

RUN npm run buildcopy
```

That looks about right. Let's build it and see if we are on the right track. Our goal is to have the build succeed without errors. Then we will use bash to check inside of the container to see if the files are there.

```
$ docker build . -t hello-front
 => [4/5] RUN npm ci                  
 => [5/5] RUN npm run 
 ...             
 => => naming to docker.io/library/hello-front

$ docker run -it hello-front bash

root@98fa9483ee85:/usr/src/app# ls
  Dockerfile  README.md  dist  index.html  node_modules  package-lock.json  package.json public src  vite.config.js

root@98fa9483ee85:/usr/src/app# ls dist
  assets index.html  vite.svgcopy
```

A valid option for serving static files now that we already have Node in the container is

```
root@98fa9483ee85:/usr/src/app# npm install -g serve

  added 89 packages in 2s

root@98fa9483ee85:/usr/src/app# serve dist

   ┌────────────────────────────────────────┐
   │                                        │
   │   Serving!                             │
   │                                        │
   │   - Local:    http://localhost:3000    │
   │   - Network:  http://172.17.0.2:3000   │
   │                                        │
   └────────────────────────────────────────┘copy
```

Great! Let's ctrl+c to exit out and then add those to our Dockerfile.
The installation of serve turns into a RUN in the Dockerfile. This way the dependency is installed during the build process. The command to serve the _dist_ directory will become the command to start the container:

```
FROM node:20

WORKDIR /usr/src/app

COPY . .

RUN npm ci

RUN npm run build

RUN npm install -g serve
CMD ["serve", "dist"]copy
```

Our CMD now includes square brackets and as a result, we now use the _exec form_ of CMD. There are actually **three** different forms for CMD, out of which the exec form is preferred. Read the
When we now build the image with _docker build . -t hello-front_ and run it with _docker run -p 5001:3000 hello-front_ , the app will be available in
### Using multiple stages
While serve is a _valid_ option, we can do better. A good goal is to create Docker images so that they do not contain anything irrelevant. With a minimal number of dependencies, images are less likely to break or become vulnerable over time.
With multi-stage builds, a tried and true solution like
Let's use the previous Dockerfile but change the FROM to include the name of the stage:

```
# The first FROM is now a stage called build-stage
FROM node:20 AS build-stage 
WORKDIR /usr/src/app

COPY . .

RUN npm ci

RUN npm run build

# This is a new stage, everything before this is gone, except for the files that we want to COPY
FROM nginx:1.25-alpine
# COPY the directory dist from the build-stage to /usr/share/nginx/html
# The target location here was found from the Docker hub page
COPY --from=build-stage /usr/src/app/dist /usr/share/nginx/htmlcopy
```

We have also declared _another stage_ , where only the relevant files of the first stage (the _dist_ directory, that contains the static content) are copied.
After we build it again, the image is ready to serve the static content. The default port will be 80 for Nginx, so something like _-p 8000:80_ will work, so the parameters of the RUN command need to be changed a bit.
Multi-stage builds also include some internal optimizations that may affect your builds. As an example, multi-stage builds skip stages that are not used. If we wish to use a stage to replace a part of a build pipeline, like testing or notifications, we must pass **some** data to the following stages. In some cases this is justified: copy the code from the testing stage to the build stage. This ensures that you are building the tested code.
### Exercises 12.13 - 12.14
#### Exercise 12.13: Todo application frontend
Finally, we get to the todo-frontend. View the todo-app/todo-frontend and read through the README.
Start by running the frontend outside the container and ensure that it works with the backend.
Containerize the application by creating _todo-app/todo-frontend/Dockerfile_ and use the _VITE_BACKEND_URL_ to the application and run it with the backend. The backend should still be running outside a container.
**Note** that you need to set _VITE_BACKEND_URL_ before building the frontend, otherwise, it does not get defined in the code!
#### Exercise 12.14: Testing during the build process
One interesting possibility that utilizing multi-stage builds gives us, is to use a separate build stage for _all testing_ to be done during the building of an image, but there may be _some_ containerization-related tests where it might be worth considering.
Extract a component _Todo_ that represents a single todo. Write a test for the new component and add running the tests into the build process.
You can add a new build stage for the test if you wish to do so. If you do so, remember to read the last paragraph before exercise 12.13 again!
### Development in containers
Let's move the whole todo application development to a container. There are a few reasons why you would want to do that:

- To keep the environment similar between development and production to avoid bugs that appear only in the production environment
- To avoid differences between developers and their personal environments that lead to difficulties in application development
- To help new team members hop in by having them install container runtime - and requiring nothing else.


These all are great reasons. The tradeoff is that we may encounter some unconventional behavior when we aren't running the applications like we are used to. We will need to do at least two things to move the application to a container:

- Start the application in development mode
- Access the files with VS Code


Let's start with the frontend. Since the Dockerfile will be significantly different from the production Dockerfile let's create a new one called _dev.Dockerfile_.
**Note** we shall use the name _dev.Dockerfile_ for development configurations and _Dockerfile_ otherwise.
Starting Vite in development mode should be easy. Let's start with the following:

```
FROM node:20

WORKDIR /usr/src/app

COPY . .

# Change npm ci to npm install since we are going to be in development mode
RUN npm install

# npm run dev is the command to start the application in development mode
CMD ["npm", "run", "dev", "--", "--host"]copy
```

> Note the extra parameters _-- --host_ in the _CMD_. Those are needed to expose the development server to be visible outside the Docker network. By default the development server is exposed only to localhost, and despite we access the frontend still using the localhost address, it is in reality attached to the Docker network.
During build the flag _-f_ will be used to tell which file to use, it would otherwise default to Dockerfile, so the following command will build the image:

```
docker build -f ./dev.Dockerfile -t hello-front-dev .copy
```

Vite will be served in port 5173, so you can test that it works by running a container with that port published.
The second task, accessing the files with VSCode, is not yet taken care of. There are at least two ways of doing this:

- Volumes, the same thing we used to preserve data with the database


Let's go over the latter since that will work with other editors as well. Let's do a trial run with the flag _-v_ , and if that works, then we will move the configuration to a docker-compose file. To use the _-v_ , we will need to tell it the current directory. The command _pwd_ should output the path to the current directory for us. Let's try this with _echo $(pwd)_ in the command line. We can use that as the left side for _-v_ to map the current directory to the inside of the container or we can use the full directory path.

```
$ docker run -p 5173:5173 -v "$(pwd):/usr/src/app/" hello-front-dev
> todo-vite@0.0.0 dev
> vite --host

  VITE v5.1.6  ready in 130 mscopy
```

Now we can edit the file _src/App.jsx_ , and the changes should be hot-loaded to the browser!
If you have a Mac with M1/M2 processor, the above command fails. In the error message, we notice the following:

```
Error: Cannot find module @rollup/rollup-linux-arm64-gnucopy
```

The problem is the library _node_modules_ from the host machine directory where the _@rollup/rollup-darwin-arm64_ (the version suitable Mac M1/M2) is installed, so the right version of the library for the container _@rollup/rollup-linux-arm64-gnu_ is not found.
There are several ways to fix the problem. Let's use the perhaps simplest one. Start the container with bash as the command, and run the _npm install_ inside the container:

```
$ docker run -it -v "$(pwd):/usr/src/app/" front-dev bash
root@b83e9040b91d:/usr/src/app# npm installcopy
```

Now both versions of the library rollup are installed and the container works!
Next, let's move the config to the file _docker-compose.dev.yml_. This file should be at the root of the project as well:

```
services:
  app:
    image: hello-front-dev
    build:
      context: . # The context will pick this directory as the "build context"
      dockerfile: dev.Dockerfile # This will simply tell which dockerfile to read
    volumes:
      - ./:/usr/src/app # The path can be relative, so ./ is enough to say "the same location as the docker-compose.yml"
    ports:
      - 5173:5173
    container_name: hello-front-dev # This will name the container hello-front-devcopy
```

With this configuration, _docker compose -f docker-compose.dev.yml up_ can run the application in development mode. You don't even need Node installed to develop it!
**Note** we shall use the name _docker-compose.dev.yml_ for development environment compose files, and the default name _docker-compose.yml_ otherwise.
Installing new dependencies is a headache for a development setup like this. One of the better options is to install the new dependency **inside** the container. So instead of doing e.g. _npm install axios_ , you have to do it in the running container e.g. _docker exec hello-front-dev npm install axios_ , or add it to the package.json and run _docker build_ again.
### Exercise 12.15
#### Exercise 12.15: Set up a frontend development environment
Create _todo-frontend/docker-compose.dev.yml_ and use volumes to enable the development of the todo-frontend while it is running _inside_ a container.
### Communication between containers in a Docker network
The Docker Compose tool sets up a network between the containers and includes a DNS to easily connect two containers. Let's add a new service to the Docker Compose and we shall see how the network and DNS work.
Busybox can help us to debug our configurations. So if you get lost in the later exercises of this section, you should use Busybox to find out what works and what doesn't. Let's use it to explore what was just said. That the containers are inside a network and you can easily connect between them. Busybox can be added to the mix by changing _docker-compose.dev.yml_ to:

```
services:
  app:
    image: hello-front-dev
    build:
      context: .
      dockerfile: dev.Dockerfile
    volumes:
      - ./:/usr/src/app
    ports:
      - 5173:5173
    container_name: hello-front-dev
  debug-helper:    image: busyboxcopy
```

The Busybox container won't have any process running inside so we can not _exec_ in there. Because of that, the output of _docker compose up_ will also look like this:

```
$ docker compose -f docker-compose.dev.yml up                                                                                    0.0s
Attaching to front-dev, debug-helper-1
debug-helper-1 exited with code 0
front-dev       |
front-dev       | > todo-vite@0.0.0 dev
front-dev       | > vite --host
front-dev       |
front-dev       |
front-dev       |   VITE v5.2.2  ready in 153 mscopy
```

This is expected as it's just a toolbox. Let's use it to send a request to hello-front-dev and see how the DNS works. While the hello-front-dev is running, we can do the request with
With Docker Compose we can use _docker compose run SERVICE COMMAND_ to run a service with a specific command. Command wget requires the flag _-O_ with _-_ to output the response to the stdout:

```
$ docker compose -f docker-compose.dev.yml run debug-helper wget -O - http://app:5173

Connecting to app:5173 (192.168.240.3:5173)
writing to stdout
<!doctype html>
<html lang="en">
  <head>
    <script type="module">
      ...copy
```

The URL is the interesting part here. We simply said to connect to port 5173 of the service _app_. _app_ is the name of the service specified in the _docker-compose.dev.yml_ file:

```
services:
  app:    image: hello-front-dev
    build:
      context: .
      dockerfile: dev.Dockerfile
    volumes:
      - ./:/usr/src/app
    ports:
      - 5173:5173    container_name: hello-front-devcopy
```

The port used is the port from which the application is available in that container, also specified in the _docker-compose.dev.yml_. The port does not need to be published for other services in the same network to be able to connect to it. The "ports" in the docker-compose file are only for external access.
Let's change the port configuration in the _docker-compose.dev.yml_ to emphasize this:

```
services:
  app:
    image: hello-front-dev
    build:
      context: .
      dockerfile: dev.Dockerfile
    volumes:
      - ./:/usr/src/app
    ports:
      - 3210:5173    container_name: hello-front-dev
  debug-helper:
    image: busyboxcopy
```

With _docker compose up_ the application is available in _host machine_ , but the command

```
docker compose  -f docker-compose.dev.yml run debug-helper wget -O - http://app:5173copy
```

works still since the port is still 5173 within the docker network.
The below image illustrates what happens. The command _docker compose run_ asks debug-helper to send the request within the network. While the browser in the host machine sends the request from outside of the network.
![fullstack content](../assets/d75733a78a79638f.png)
Now that you know how easy it is to find other services in the _docker-compose.yml_ and we have nothing to debug we can remove the debug-helper and revert the ports to 5173:5173 in our compose file.
### Exercise 12.16
#### Exercise 12.16: Run todo-backend in a development container
Use volumes and Nodemon to enable the development of the todo app backend while it is running _inside_ a container. Create a _todo-backend/dev.Dockerfile_ and edit the _todo-backend/docker-compose.dev.yml_.
You will also need to rethink the connections between backend and MongoDB / Redis. Thankfully Docker Compose can include environment variables that will be passed to the application:

```
services:
  server:
    image: ...
    volumes:
      - ...
    ports:
      - ...
    environment: 
      - REDIS_URL=redisurl_here
      - MONGO_URL=mongourl_herecopy
```

The URLs are purposefully wrong, you will need to set the correct values. Remember to _look all the time what happens in the console_. If and when things blow up, the error messages hint at what might be broken.
Here is a possibly helpful image illustrating the connections within the docker network:
![diagram of connection between browser, backend, mongo and redis](../assets/813fd55e4e0d5252.png)
### Communications between containers in a more ambitious environment
Next, we will configure a
> _A reverse proxy is a type of proxy server that retrieves resources on behalf of a client from one or more servers. These resources are then returned to the client, appearing as if they originated from the reverse proxy server itself._
So in our case, the reverse proxy will be the single point of entry to our application, and the final goal will be to set both the React frontend and the Express backend behind the reverse proxy.
There are multiple different options for a reverse proxy implementation, such as Traefik, Caddy, Nginx, and Apache (ordered by initial release from newer to older).
Our pick is
Let us now put the _hello-frontend_ behind the reverse proxy.
Create a file _nginx.dev.conf_ in the project root and take the following template as a starting point. We will need to do minor edits to have our application running:

```
# events is required, but defaults are ok
events { }

# A http server, listening at port 80
http {
  server {
    listen 80;

    # Requests starting with root (/) are handled
    location / {
      # The following 3 lines are required for the hot loading to work (websocket).
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection 'upgrade';
      
      # Requests are directed to http://localhost:5173
      proxy_pass http://localhost:5173;
    }
  }
}copy
```

**Note** we are using the familiar naming convention also for Nginx, _nginx.dev.conf_ for development configurations, and the default name _nginx.conf_ otherwise.
Next, create an Nginx service in the _docker-compose.dev.yml_ file. Add a volume as instructed in the Docker Hub page where the right side is _:/etc/nginx/nginx.conf:ro_ , the final ro declares that the volume will be _read-only_ :

```
services:
  app:
    # ...
  nginx:
    image: nginx:1.20.1
    volumes:
      - ./nginx.dev.conf:/etc/nginx/nginx.conf:ro
    ports:
      - 8080:80
    container_name: reverse-proxy
    depends_on:
      - app # wait for the frontend container to be startedcopy
```

with that added, we can run _docker compose -f docker-compose.dev.yml up_ and see what happens.

```
$ docker container ls
CONTAINER ID   IMAGE            COMMAND  PORTS                   NAMES
a02ae58f3e8d   nginx:1.20.1     ...      0.0.0.0:8080->80/tcp    reverse-proxy
5ee0284566b4   hello-front-dev  ...      0.0.0.0:5173->5173/tcp  hello-front-devcopy
```

Connecting to
This is because directing requests to
Let's test this by going inside the Nginx container and using curl to send a request to the application itself. In our usage curl is similar to wget, but won't need any flags.

```
$ docker exec -it reverse-proxy bash  

root@374f9e62bfa8:\# curl http://localhost:80
  <html>
  <head><title>502 Bad Gateway</title></head>
  ...copy
```

To help us, Docker Compose has set up a network when we ran _docker compose up_. It has also added all of the containers mentioned in the _docker-compose.dev.yml_ to the network. A DNS makes sure we can find the other containers in the network. The containers are each given two names: the service name and the container name and both can be used to communicate with a container.
Since we are inside the container, we can also test the DNS! Let's curl the service name (app) in port 5173

```
root@374f9e62bfa8:\# curl http://app:5173
<!doctype html>
<html lang="en">
  <head>
    <script type="module" src="/@vite/client"></script>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Vite + React</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>copy
```

That is it! Let's replace the proxy_pass address in nginx.dev.conf with that one.
One more thing: we added an option _nginx_ container is not started before the frontend container _app_ is started:

```
services:
  app:
    # ...
  nginx:
    image: nginx:1.20.1
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      - 8080:80
    container_name: reverse-proxy
    depends_on:      - appcopy
```

If we do not enforce the starting order with _depends_on_ there a risk that Nginx fails on startup since it tries to resolve all DNS names that are referred in the config file:

```
http {
  server {
    listen 80;

    location / {
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection 'upgrade';
      
      proxy_pass http://app:5173;    }
  }
}copy
```

Note that _depends_on_ does not guarantee that the service in the depended container is ready for action, it just ensures that the container has been started (and the corresponding entry is added to DNS). If a service needs to wait another service to become ready before the startup,
### Exercises 12.17. - 12.19
#### Exercise 12.17: Set up an Nginx reverse proxy server in front of todo-frontend
We are going to put the Nginx server in front of both todo-frontend and todo-backend. Let's start by creating a new docker-compose file _todo-app/docker-compose.dev.yml_ and _todo-app/nginx.dev.conf_.

```
todo-app
├── todo-frontend
├── todo-backend
├── nginx.dev.conf└── docker-compose.dev.ymlcopy
```

Add the services Nginx and the todo-frontend built with _todo-app/todo-frontend/dev.Dockerfile_ into the _todo-app/docker-compose.dev.yml_.
![connection diagram between browser, nginx, express and frontend](../assets/f4f6852086cbbead.png)
In this and the following exercises you **do not** need to support the build option, that is, the command:

```
docker compose -f docker-compose.dev.yml up --buildcopy
```

It is enough to build the frontend and backend at their own repositories.
#### Exercise 12.18: Configure the Nginx server to be in front of todo-backend
Add the service todo-backend to the docker-compose file _todo-app/docker-compose.dev.yml_ in development mode.
Add a new location to the _nginx.dev.conf_ file, so that requests to _/api_ are proxied to the backend. Something like this should do the trick:

```
  server {
    listen 80;

    # Requests starting with root (/) are handled
    location / {
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection 'upgrade';
      
      proxy_pass ...
    }

    # Requests starting with /api/ are handled
    location /api/ {
      proxy_pass ...
    }
  }copy
```

The _proxy_pass_ directive has an interesting feature with a trailing slash. As we are using the path _/api_ for location but the backend application only answers in paths _/_ or _/todos_ we will want the _/api_ to be removed from the request. In other words, even though the browser will send a GET request to _/api/todos/1_ we want the Nginx to proxy the request to _/todos/1_. Do this by adding a trailing slash _/_ to the URL at the end of _proxy_pass_.
This is a
![comments about forgetting to use the trailing slash](../assets/5bc14d3edd911b8d.png)
This illustrates what we are looking for and may be helpful if you are having trouble:
![diagram of calling / and /api in action](../assets/0fc19fe93294a329.png)
#### Exercise 12.19: Connect the services, todo-frontend with todo-backend
> In this exercise, submit the entire development environment, including both Express and React applications, dev.Dockerfiles and docker-compose.dev.yml.
Finally, it is time to put all the pieces together. Before starting, it is essential to understand _where_ the React app is actually run. The above diagram might give the impression that React app is run in the container but it is totally wrong.
It is just the _React app source code_ that is in the container. When the browser hits the address
![diagram showing that the react code is sent to the browser for its execution](../assets/636c453aca339f3e.png)
Next, the browser starts executing the React app, and all the requests it makes to the backend should be done through the Nginx reverse proxy:
![diagram showing requests made from the browser to /api of nginx and the proxy in action proxying the request to /todos](../assets/3ea8741728e62b3e.png)
The frontend container is actually only accessed on the first request that gets the React app source code to the browser.
Now set up your app to work as depicted in the above figure. Make sure that the todo-frontend works with todo-backend. It will require changes to the _VITE_BACKEND_URL_ environmental variable in the frontend.
Make sure that the development environment is now fully functional, that is:

- all features of the todo app work
- you can edit the source files _and_ the changes take effect by reloading the app
- frontend should access the backend through Nginx, so the requests should be done to

![network tab of the browser developer tools showing that the url request includes 8080/api/todos](../assets/cf09003f7fbba95a.png)
Note that your app should work even if no

```
services:
  app:
    image: todo-front-dev
    volumes:
      - ./todo-frontend/:/usr/src/app
    # no ports here!

  server:
      image: todo-back-dev
      volumes:
        - ./todo-backend/:/usr/src/app
      environment: 
        - ...
      # no ports here!

  nginx:
    image: nginx:1.20.1
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      - 8080:80 # this is needed
    container_name: reverse-proxy
    depends_on:
      - appcopy
```

We just need to expose the Nginx port to the host machine since the access to the backend and frontend is proxied to the right container port by Nginx. Because Nginx, frontend and backend are defined in the same Docker compose configuration, Docker puts those to the same
### Tools for Production
Containers are fun tools to use in development, but the best use case for them is in the production environment. There are many more powerful tools than Docker Compose to run containers in production.
Heavyweight container orchestration tools like
If you are interested in learning more in-depth about containers come to the
### Exercises 12.20.-12.22
#### Exercise 12.20
Create a production _todo-app/docker-compose.yml_ file with all of the services, Nginx, todo-backend, todo-frontend, MongoDB and Redis. Use Dockerfiles instead of _dev.Dockerfiles_ and make sure to start the applications in production mode.
Please use the following structure for this exercise:

```
todo-app
├── todo-frontend
├── todo-backend
├── nginx.dev.conf
├── docker-compose.dev.yml
├── nginx.conf└── docker-compose.ymlcopy
```

#### Exercise 12.21
Create a similar containerized development environment of one of _your own_ full stack apps that you have created during the course or in your free time. You should structure the app in your submission repository as follows:

```
└── my-app
    ├── frontend
    |    └── dev.Dockerfile
    ├── backend
    |    └── dev.Dockerfile
    ├── nginx.dev.conf
    └── docker-compose.dev.ymlcopy
```

#### Exercise 12.22
Finish this part by creating a containerized _production setup_ of your own full stack app. Structure the app in your submission repository as follows:

```
└── my-app
    ├── frontend
    |    ├── dev.Dockerfile
    |    └── Dockerfile
    ├── backend
    |    └── dev.Dockerfile
    |    └── Dockerfile
    ├── nginx.dev.conf
    ├── nginx.conf
    ├── docker-compose.dev.yml
    └── docker-compose.ymlcopy
```

### Submitting exercises and getting the credits
This was the last exercise in this section. It's time to push your code to GitHub and mark all of your finished exercises to the
Exercises of this part are submitted just like in the previous parts, but unlike parts 0 to 7, the submission goes to an own _all the exercises_ to pass this part!
Once you have completed the exercises and want to get the credits, let us know through the exercise submission system that you have completed the course:
![Submissions](../assets/770a7d941952a2f6.png)
**Note** that you need a registration to the corresponding course part for getting the credits registered, see [here](../part0/01-general-info-parts-and-completion.md) for more information.
You can download the certificate for completing this part by clicking one of the flag icons. The flag icon corresponds to the certificate's language.
[Part 12b **Previous part**](../part12/01-building-and-configuring-environments.md)[Part 13 **Next part**](../part13/01-part13.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)
