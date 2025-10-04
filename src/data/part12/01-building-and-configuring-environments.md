---{
  "title": "Building and configuring environments",
  "source_url": "https://fullstackopen.com/en/part12/building_and_configuring_environments",
  "crawl_timestamp": "2025-10-04T19:15:57Z",
  "checksum": "644090ef8940c83644d436152125bfe4824e98e776d3879e3968e6d1919e8eb1"
}
---[Skip to content](../part12/01-building-and-configuring-environments-course-main-content.md)
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
Building and configuring environments
[a Introduction to Containers](../part12/01-introduction-to-containers.md)
b Building and configuring environments

- [Dockerfile](../part12/01-building-and-configuring-environments-dockerfile.md)
- [More meaningful image](../part12/01-building-and-configuring-environments-more-meaningful-image.md)
- [Exercise 12.5.](../part12/01-building-and-configuring-environments-exercise-12-5.md)
- [Using Docker compose](../part12/01-building-and-configuring-environments-using-docker-compose.md)
- [Exercise 12.6.](../part12/01-building-and-configuring-environments-exercise-12-6.md)
- [Utilizing containers in development](../part12/01-building-and-configuring-environments-utilizing-containers-in-development.md)
- [Bind mount and initializing the database](../part12/01-building-and-configuring-environments-bind-mount-and-initializing-the-database.md)
- [Still problems?](../part12/01-building-and-configuring-environments-still-problems.md)
- [Persisting data with volumes](../part12/01-building-and-configuring-environments-persisting-data-with-volumes.md)
- [Exercise 12.7.](../part12/01-building-and-configuring-environments-exercise-12-7.md)
- [Debugging issues in containers](../part12/01-building-and-configuring-environments-debugging-issues-in-containers.md)
- [Exercise 12.8.](../part12/01-building-and-configuring-environments-exercise-12-8.md)
- [Redis](../part12/01-building-and-configuring-environments-redis.md)
- [Exercises 12.9. - 12.11.](../part12/01-building-and-configuring-environments-exercises-12-9-12-11.md)
- [Persisting data with Redis](../part12/01-building-and-configuring-environments-persisting-data-with-redis.md)
- [Exercise 12.12.](../part12/01-building-and-configuring-environments-exercise-12-12.md)


[c Basics of Orchestration](../part12/01-basics-of-orchestration.md)
b
# Building and configuring environments
The part was updated 21th Mar 2024: Create react app was replaced with Vite in the todo-frontend.
If you started the part before the update, you can see
In the previous section, we used two different base images: ubuntu and node, and did some manual work to get a simple "Hello, World!" running. The tools and commands we learned during that process will be helpful. In this section, we will learn how to build images and configure environments for our applications. We will start with a regular Express/Node.js backend and build on top of that with other services, including a MongoDB database.
### Dockerfile
Instead of modifying a container by copying files inside, we can create a new image that contains the "Hello, World!" application. The tool for this is the Dockerfile. Dockerfile is a simple text file that contains all of the instructions for creating an image. Let's create an example Dockerfile from the "Hello, World!" application.
If you did not already, create a directory on your machine and create a file called _Dockerfile_ inside that directory. Let's also put an _index.js_ containing _console.log('Hello, World!')_ next to the Dockerfile. Your directory structure should look like this:

```
├── index.js
└── Dockerfilecopy
```

inside that Dockerfile we will tell the image three things:

- Use the
- Include the index.js file inside the image, so we don't need to manually copy it into the container
- When we run a container from the image, use Node to execute the index.js file.


The wishes above will translate into a basic Dockerfile. The best location to place this file is usually at the root of the project.
The resulting _Dockerfile_ looks like this:

```
FROM node:20

WORKDIR /usr/src/app

COPY ./index.js ./index.js

CMD node index.jscopy
```

FROM instruction will tell Docker that the base for the image should be node:20. COPY instruction will copy the file _index.js_ from the host machine to the file with the same name in the image. CMD instruction tells what happens when _docker run_ is used. CMD is the default command that can then be overwritten with the argument given after the image name. See _docker run --help_ if you forgot.
The WORKDIR instruction was slipped in to ensure we don't interfere with the contents of the image. It will guarantee all of the following commands will have _/usr/src/app_ set as the working directory. If the directory doesn't exist in the base image, it will be automatically created.
If we do not specify a WORKDIR, we risk overwriting important files by accident. If you check the root (_/_) of the node:20 image with _docker run node:20 ls_ , you can notice all of the directories and files that are already included in the image.
Now we can use the command _docker build_ to build an image based on the Dockerfile. Let's spice up the command with one additional flag: _-t_ , this will help us name the image:

```
$ docker build -t fs-hello-world . 
[+] Building 3.9s (8/8) FINISHED
...copy
```

So the result is "Docker please build with tag (you may think of the tag as the name of the resulting image.) _fs-hello-world_ the Dockerfile in this directory". You can point to any Dockerfile, but in our case, a simple dot will mean the Dockerfile is in _this_ directory. That is why the command ends with a period. After the build is finished, you can run it with _docker run fs-hello-world_ :

```
$ docker run fs-hello-world
Hello, Worldcopy
```

As images are just files, they can be moved around, downloaded and deleted. You can list the images you have locally with _docker image ls_ , delete them with _docker image rm_. See what other command you have available with _docker image --help_.
One more thing: before it was mentioned that the default command, defined by the CMD in the Dockerfile, can be overwritten if needed. We could e.g. open a bash session to the container and observe it's content:

```
$ docker run -it fs-hello-world bash
root@2932e32dbc09:/usr/src/app# ls
index.js
root@2932e32dbc09:/usr/src/app#copy
```

### More meaningful image
Moving an Express server to a container should be as simple as moving the "Hello, World!" application inside a container. The only difference is that there are more files. Thankfully _COPY_ instruction can handle all that. Let's delete the index.js and create a new Express server. Lets use

```
$ npx express-generator
  ...
  
  install dependencies:
    $ npm install

  run the app:
    $ DEBUG=playground:* npm startcopy
```

First, let's run the application to get an idea of what we just created. Note that the command to run the application may be different from you, my directory was called playground.

```
$ npm install
$ DEBUG=playground:* npm start
  playground:server Listening on port 3000 +0mscopy
```

Great, so now we can navigate to
Containerizing that should be relatively easy based on the previous example.

- Use node as base
- Set working directory so we don't interfere with the contents of the base image
- Copy ALL of the files in this directory to the image
- Start with DEBUG=playground:* npm start


Let's place the following Dockerfile at the root of the project:

```
FROM node:20

WORKDIR /usr/src/app

COPY . .

CMD DEBUG=playground:* npm startcopy
```

Let's build the image from the Dockerfile and then run it:

```
docker build -t express-server .
docker run -p 3123:3000 express-servercopy
```

The _-p_ flag in the run command will inform Docker that a port from the host machine should be opened and directed to a port in the container. The format is _-p host-port:application-port_.
The application is now running! Let's test it by sending a GET request to
> If yours doesn't work, skip to the next section. There is an explanation why it may not work even if you followed the steps correctly.
Shutting the app down is a headache at the moment. Use another terminal and _docker kill_ command to kill the application. The _docker kill_ will send a kill signal (SIGKILL) to the application to force it to shut down. It needs the name or the id of the container as an argument.
By the way, when using the id as the argument, the beginning of the ID is enough for Docker to know which container we mean.

```
$ docker container ls
  CONTAINER ID   IMAGE            COMMAND                  CREATED         STATUS         PORTS                                       NAMES
  48096ca3ffec   express-server   "docker-entrypoint.s…"   9 seconds ago   Up 6 seconds   0.0.0.0:3123->3000/tcp, :::3123->3000/tcp   infallible_booth

$ docker kill 48
  48copy
```

In the future, let's use the same port on both sides of _-p_. Just so we don't have to remember which one we happened to choose.
#### Fixing potential issues we created by copy-pasting
There are a few steps we need to change to create a more comprehensive Dockerfile. It may even be that the above example doesn't work in all cases because we skipped an important step.
When we ran npm install on our machine, in some cases the **Node package manager** may install operating system specific dependencies during the install step. We may accidentally move non-functional parts to the image with the COPY instruction. This can easily happen if we copy the _node_modules_ directory into the image.
This is a critical thing to keep in mind when we build our images. It's best to do most things, such as to run _npm install_ during the build process _inside the container_ rather than doing those prior to building. The easy rule of thumb is to only copy files that you would push to GitHub. Build artifacts or dependencies should not be copied since those can be installed during the build process.
We can use _.dockerignore_ to solve the problem. The file .dockerignore is very similar to .gitignore, you can use that to prevent unwanted files from being copied to your image. The file should be placed next to the Dockerfile. Here is a possible content of a _.dockerignore_

```
.dockerignore
.gitignore
node_modules
Dockerfilecopy
```

However, in our case, the .dockerignore isn't the only thing required. We will need to install the dependencies during the build step. The _Dockerfile_ changes to:

```
FROM node:20

WORKDIR /usr/src/app

COPY . .

RUN npm install
CMD DEBUG=playground:* npm startcopy
```

The npm install can be risky. Instead of using npm install, npm offers a much better tool for installing dependencies, the _ci_ command.
Differences between ci and install:

- install may update the package-lock.json
- install may install a different version of a dependency if you have ^ or ~ in the version of the dependency.
- ci will delete the node_modules folder before installing anything
- ci will follow the package-lock.json and does not alter any files


So in short: _ci_ creates reliable builds, while _install_ is the one to use when you want to install new dependencies.
As we are not installing anything new during the build step, and we don't want the versions to suddenly change, we will use _ci_ :

```
FROM node:20

WORKDIR /usr/src/app

COPY . .

RUN npm ci
CMD DEBUG=playground:* npm startcopy
```

Even better, we can use _npm ci --omit=dev_ to not waste time installing development dependencies.
> As you noticed in the comparison list; npm ci will delete the node_modules folder so creating the .dockerignore did not matter. However, .dockerignore is an amazing tool when you want to optimize your build process. We will talk briefly about these optimizations later.
Now the Dockerfile should work again, try it with _docker build -t express-server . && docker run -p 3123:3000 express-server_
> Note that we are here chaining two bash commands with &&. We could get (nearly) the same effect by running both commands separately. When chaining commands with && if one command fails, the next ones in the chain will not be executed.
We set an environment variable _DEBUG=playground:*_ during CMD for the npm start. However, with Dockerfiles we could also use the instruction ENV to set environment variables. Let's do that:

```
FROM node:20

WORKDIR /usr/src/app

COPY . .

RUN npm ci 

ENV DEBUG=playground:*
CMD npm startcopy
```

> _If you're wondering what the DEBUG environment variable does, read_
#### Dockerfile best practices
There are 2 rules of thumb you should follow when creating images:

- Try to create as **secure** of an image as possible
- Try to create as **small** of an image as possible


Smaller images are more secure by having less attack surface area, and also move faster in deployment pipelines.
Snyk has a great list of the 10 best practices for Node/Express containerization. Read those
One big carelessness we have left is running the application as root instead of using a user with lower privileges. Let's do a final fix to the Dockerfile:

```
FROM node:20
  
WORKDIR /usr/src/app

COPY --chown=node:node . .
RUN npm ci 

ENV DEBUG=playground:*
  
USER node
CMD npm startcopy
```

### Exercise 12.5
#### Exercise 12.5: Containerizing a Node application
The repository that you cloned or copied in the [first exercise](../part12/01-introduction-to-containers-exercise-12-1.md) contains a todo-app. See the todo-app/todo-backend and read through the README. We will not touch the todo-frontend yet.

- Step 1. Containerize the todo-backend by creating a _todo-app/todo-backend/Dockerfile_ and building an image.
- Step 2. Run the todo-backend image with the correct ports open. Make sure the visit counter increases when used through a browser in


Tip: Run the application outside of a container to examine it before starting to containerize.
### Using Docker compose
In the previous section, we created an Express server, knowing that it will run in port 3123, and used the commands _docker build -t express-server . && docker run -p 3123:3000 express-server_ to run it. This already looks like something you would need to put into a script to remember. Fortunately, Docker offers us a better solution.
Now we can turn the previous spell into a yaml file. The best part about yaml files is that you can save these to a Git repository!
Create the file **docker-compose.yml** and place it at the root of the project, next to the Dockerfile. This time we will use the same port for host and container. The file content is:

```
services:
  app:                    # The name of the service, can be anything
    image: express-server # Declares which image to use
    build: .              # Declares where to build if image is not found
    ports:                # Declares the ports to publish
      - 3000:3000copy
```

The meaning of each line is explained as a comment. If you want to see the full specification see the
Now we can use _docker compose up_ to build and run the application. If we want to rebuild the images we can use _docker compose up --build_.
You can also run the application in the background with _docker compose up -d_ (_-d_ for detached) and close it with _docker compose down_.
> _Note that some older Docker versions (especially in Windows) do not support the command _docker compose_. One way to circumvent this problem is to _docker-compose_ that works mostly similarly to _docker compose_. However, the preferable fix is to update the Docker to a more recent version._
Creating files like _docker-compose.yml_ that _declare_ what you want instead of script files that you need to run in a specific order / a specific number of times is often a great practice.
### Exercise 12.6
#### Exercise 12.6: Docker compose
Create a _todo-app/todo-backend/docker-compose.yml_ file that works with the Node application from the previous exercise.
The visit counter is the only feature that is required to be working.
### Utilizing containers in development
When you are developing software, containerization can be used in various ways to improve your quality of life. One of the most useful cases is by bypassing the need to install and configure tools twice.
It may not be the best option to move your entire development environment into a container, but if that's what you want it's certainly possible. We will revisit this idea at the end of this part. But until then, _run the Node application itself outside of containers_.
The application we met in the previous exercises uses MongoDB. Let's explore
Create a new yaml called _todo-app/todo-backend/docker-compose.dev.yml_ that looks like following:

```
services:
  mongo:
    image: mongo
    ports:
      - 3456:27017
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: example
      MONGO_INITDB_DATABASE: the_databasecopy
```

The meaning of the two first environment variables defined above is explained on the Docker Hub page:
> _These variables, used in conjunction, create a new user and set that user's password. This user is created in the admin authentication database and given the role of root, which is a "superuser" role._
The last environment variable _MONGO_INITDB_DATABASE_ will tell MongoDB to create a database with that name.
You can use _-f_ flag to specify a _file_ to run the Docker Compose command with e.g.

```
docker compose -f docker-compose.dev.yml upcopy
```

Now that we may have multiple compose files, it's useful.
Next, start the MongoDB with _docker compose -f docker-compose.dev.yml up -d_. With _-d_ it will run it in the background. You can view the output logs with _docker compose -f docker-compose.dev.yml logs -f_. There the _-f_ will ensure we _follow_ the logs.
As said previously, currently we **do not** want to run the Node application inside a container. Developing while the application itself is inside a container is a challenge. We will explore that option later in this part.
Run the good old _npm install_ first on your machine to set up the Node application. Then start the application with the relevant environment variable. You can modify the code to set them as the defaults or use the .env file. There is no hurt in putting these keys to GitHub since they are only used in your local development environment. I'll just throw them in with the _npm run dev_ to help you copy-paste.

```
MONGO_URL=mongodb://localhost:3456/the_database npm run devcopy
```

This won't be enough; we need to create a user to be authorized inside of the container. The url

```
[nodemon] 2.0.12
[nodemon] to restart at any time, enter `rs`
[nodemon] watching path(s): *.*
[nodemon] watching extensions: js,mjs,json
[nodemon] starting `node ./bin/www`
/Users/mluukkai/dev/fs-ci-lokakuu/repo/todo-app/todo-backend/node_modules/mongodb/lib/cmap/connection.js:272
          callback(new MongoError(document));
                   ^
MongoError: command find requires authentication
    at MessageStream.messageHandler (/Users/mluukkai/dev/fs-ci-lokakuu/repo/todo-app/todo-backend/node_modules/mongodb/lib/cmap/connection.js:272:20)copy
```

### Bind mount and initializing the database
In the
The exercise project has a file _todo-app/todo-backend/mongo/mongo-init.js_ with contents:

```
db.createUser({
  user: 'the_username',
  pwd: 'the_password',
  roles: [
    {
      role: 'dbOwner',
      db: 'the_database',
    },
  ],
});

db.createCollection('todos');

db.todos.insert({ text: 'Write code', done: true });
db.todos.insert({ text: 'Learn about containers', done: false });copy
```

This file will initialize the database with a user and a few todos. Next, we need to get it inside the container at startup.
We could create a new image FROM mongo and COPY the file inside, or we can use a _mongo-init.js_ to the container. Let's do the latter.
Bind mount is the act of binding a file (or directory) on the host machine to a file (or directory) in the container. A bind mount is done by adding a _-v_ flag with _container run_. The syntax is _-v FILE-IN-HOST:FILE-IN-CONTAINER_. Since we already learned about Docker Compose let's skip that. The bind mount is declared under key _volumes_ in _docker-compose.dev.yml_. Otherwise the format is the same, first host and then container:

```
  mongo:
    image: mongo
    ports:
     - 3456:27017
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: example
      MONGO_INITDB_DATABASE: the_database
    volumes:       - ./mongo/mongo-init.js:/docker-entrypoint-initdb.d/mongo-init.jscopy
```

The result of the bind mount is that the file _mongo-init.js_ in the mongo folder of the host machine is the same as the _mongo-init.js_ file in the container's /docker-entrypoint-initdb.d directory. Changes to either file will be available in the other. We don't need to make any changes during runtime. But this will be the key to software development in containers.
Run _docker compose -f docker-compose.dev.yml down --volumes_ to ensure that nothing is left and start from a clean slate with _docker compose -f docker-compose.dev.yml up_ to initialize the database.
If you see an error like this:

```
mongo_database | failed to load: /docker-entrypoint-initdb.d/mongo-init.js
mongo_database | exiting with code -3copy
```

you may have a read permission problem. They are not uncommon when dealing with volumes. In the above case, you can use _chmod a+r mongo-init.js_ , which will give everyone read access to that file. Be careful when using _chmod_ since granting more privileges can be a security issue. Use the _chmod_ only on the mongo-init.js on your computer.
Now starting the Express application with the correct environment variable should work:

```
MONGO_URL=mongodb://the_username:the_password@localhost:3456/the_database npm run devcopy
```

Let's check that the _should_ use Postman to test the basic functionality of the app, such as adding or deleting a todo.
### Still problems
For some reason, the initialization of Mongo has caused problems for many.
If the app does not work and you still end up with the following error:

```
/Users/mluukkai/dev/fs-ci-lokakuu/repo/todo-app/todo-backend/node_modules/mongodb/lib/cmap/connection.js:272
          callback(new MongoError(document));
                   ^
MongoError: command find requires authentication
    at MessageStream.messageHandler (/Users/mluukkai/dev/fs-ci-lokakuu/repo/todo-app/todo-backend/node_modules/mongodb/lib/cmap/connection.js:272:20)copy
```

run these commands:

```
docker compose -f docker-compose.dev.yml down --volumes
docker image rm mongocopy
```

After these, try to start Mongo again.
If the problem persists, let us drop the idea of a volume altogether and copy the initialization script to a custom image. Create the following _Dockerfile_ to the directory _todo-app/todo-backend/mongo_ :

```
FROM mongo

COPY ./mongo-init.js /docker-entrypoint-initdb.d/copy
```

Build it to an image with the command:

```
docker build -t initialized-mongo .copy
```

Now change the _docker-compose.dev.yml_ file to use the new image:

```
  mongo:
    image: initialized-mongo    ports:
     - 3456:27017
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: example
      MONGO_INITDB_DATABASE: the_databasecopy
```

Now the app should finally work.
### Persisting data with volumes
By default, database containers are not going to preserve our data. When you close the database container you _may or may not_ be able to get the data back.
> Mongo is actually a rare case in which the container indeed does preserve the data. This happens, since the developers who made the Docker image for Mongo have defined a volume to be used.
There are two distinct methods to store the data:

- Declaring a location in your filesystem (called
- Letting Docker decide where to store the data (


The first choice is preferable in most cases whenever one _really_ needs to avoid the data being deleted.
Let's see both in action with Docker compose. Let us start with _bind mount:_

```
services:
  mongo:
    image: mongo
    ports:
     - 3456:27017
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: example
      MONGO_INITDB_DATABASE: the_database
    volumes:
      - ./mongo/mongo-init.js:/docker-entrypoint-initdb.d/mongo-init.js
      - ./mongo_data:/data/dbcopy
```

The above will create a directory called _mongo_data_ to your local filesystem and map it into the container as _/data/db_. This means the data in _/data/db_ is stored outside of the container but still accessible by the container! Just remember to add the directory to .gitignore.
A similar outcome can be achieved with a _named volume:_

```
services:
  mongo:
    image: mongo
    ports:
     - 3456:27017
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: example
      MONGO_INITDB_DATABASE: the_database
    volumes:
      - ./mongo/mongo-init.js:/docker-entrypoint-initdb.d/mongo-init.js
      - mongo_data:/data/db
volumes:  mongo_data:copy
```

Now the volume is created and managed by Docker. After starting the application (_docker compose -f docker-compose.dev.yml up_) you can list the volumes with _docker volume ls_ , inspect one of them with _docker volume inspect_ and even delete them with _docker volume rm_ :

```
$ docker volume ls
DRIVER    VOLUME NAME
local     todo-backend_mongo_data
$ docker volume inspect todo-backend_mongo_data
[
    {
        "CreatedAt": "2024-19-03T12:52:11Z",
        "Driver": "local",
        "Labels": {
            "com.docker.compose.project": "todo-backend",
            "com.docker.compose.version": "1.29.2",
            "com.docker.compose.volume": "mongo_data"
        },
        "Mountpoint": "/var/lib/docker/volumes/todo-backend_mongo_data/_data",
        "Name": "todo-backend_mongo_data",
        "Options": null,
        "Scope": "local"
    }
]copy
```

The named volume is still stored in your local filesystem but figuring out _where_ may not be as trivial as with the previous option.
### Exercise 12.7
#### Exercise 12.7: Little bit of MongoDB coding
Note that this exercise assumes that you have done all the configurations made in the material after exercise 12.5. You should still run the todo-app backend _outside a container_ ; just the MongoDB is containerized for now.
The todo application has no proper implementation of routes for getting one todo (GET _/todos/:id_) and updating one todo (PUT _/todos/:id_). Fix the code.
### Debugging issues in containers
> _When coding, you most likely end up in a situation where everything is broken._
>
> - Matti Luukkainen
When developing with containers, we need to learn new tools for debugging, since we can not just "console.log" everything. When code has a bug, you may often be in a state where at least something works, so you can work forward from that. Configuration most often is in either of two states: 1. working or 2. broken. We will go over a few tools that can help when your application is in the latter state.
When developing software, you can safely progress step by step, all the time verifying that what you have coded behaves as expected. Often, this is not the case when doing configurations. The configuration you may be writing can be broken until the moment it is finished. So when you write a long docker-compose.yml or Dockerfile and it does not work, you need to take a moment and think about the various ways you could confirm something is working.
_Question Everything_ is still applicable here. As said in [part 3](../part3/01-saving-data-to-mongo-db.md): The key is to be systematic. Since the problem can exist anywhere, _you must question everything_ , and eliminate all possible sources of error one by one.
For myself, the most valuable method of debugging is stopping and thinking about what I'm trying to accomplish instead of just bashing my head at the problem. Often there is a simple, alternate, solution or quick google search that will get me moving forward.

#### exec
The Docker command
Let's start a web server in the background and do a little bit of debugging to get it running and displaying the message "Hello, exec!" in our browser. Let's choose

```
docker container run -d nginxcopy
```

Ok, now the questions are:

- Where should we go with our browser?
- Is it even running?


We know how to answer the latter: by listing the running containers.

```
$ docker container ls
CONTAINER ID   IMAGE   COMMAND  CREATED     STATUS    PORTS     NAMES
3f831a57b7cc   nginx   ...      3 sec ago   Up 2 sec  80/tcp    keen_darwincopy
```

Yes! We got the first question answered as well. It seems to listen on port 80, as seen on the output above.
Let's shut it down and restart with the _-p_ flag to have our browser access it.

```
docker container stop keen_darwin
docker container rm keen_darwin

docker container run -d -p 8080:80 nginxcopy
```

> _**Editor's note_** when doing development, it is **essential** to constantly follow the container logs. I'm usually not running containers in a detached mode (that is with -d) since it requires a bit of an extra effort to open the logs. _
> _When I'm 100% sure that everything works... no, when I'm 200% sure, then I might relax a bit and start the containers in detached mode. Until everything again falls apart and it is time to open the logs again._
Let's look at the app by going to _-it_ will ensure that we can interact with the container:

```
$ docker container ls
CONTAINER ID   IMAGE     COMMAND  PORTS                  NAMES
7edcb36aff08   nginx     ...      0.0.0.0:8080->80/tcp   wonderful_ramanujan

$ docker exec -it wonderful_ramanujan bash
root@7edcb36aff08:/#copy
```

Now that we are in, we need to find the faulty file and replace it. Quick Google tells us that file itself is _/usr/share/nginx/html/index.html_.
Let's move to the directory and delete the file

```
root@7edcb36aff08:/# cd /usr/share/nginx/html/
root@7edcb36aff08:/# rm index.htmlcopy
```

Now, if we go to

```
root@7edcb36aff08:/# echo "Hello, exec!" > index.htmlcopy
```

Refresh the page, and our message is displayed! Now we know how exec can be used to interact with the containers. Remember that all of the changes are lost when the container is deleted. To preserve the changes, you must use _commit_ just as we did in [previous section](../part12/01-introduction-to-containers-other-docker-commands.md).
### Exercise 12.8
#### Exercise 12.8: Mongo command-line interface
> Use _script_ to record what you do, save the file as script-answers/exercise12_8.txt
While the MongoDB from the previous exercise is running, access the database with the Mongo command-line interface (CLI). You can do that using docker exec. Then add a new todo using the CLI.
The command to open CLI when inside the container is _mongosh_
The Mongo CLI will require the username and password flags to authenticate correctly. Flags _-u root -p example_ should work, the values are from the _docker-compose.dev.yml_.

- Step 1: Run MongoDB
- Step 2: Use _docker exec_ to get inside the container
- Step 3: Open Mongo CLI


When you have connected to the Mongo CLI you can ask it to show the DBs inside:

```
> show dbs
admin         0.000GB
config         0.000GB
local         0.000GB
the_database  0.000GBcopy
```

To access the correct database:

```
> use the_databasecopy
```

And finally to find out the collections:

```
> show collections
todoscopy
```

We can now access the data in those collections:

```
> db.todos.find({})
[
  {
    _id: ObjectId("633c270ba211aa5f7931f078"),
    text: 'Write code',
    done: false
  },
  {
    _id: ObjectId("633c270ba211aa5f7931f079"),
    text: 'Learn about containers',
    done: false
  }
]copy
```

Insert one new todo with the text: "Increase the number of tools in my tool belt" with the status done as _false_. Consult the
Ensure that you see the new todo both in the Express app and when querying from Mongo CLI.
### Redis
_key_ that was attached to the data (the _value_).
By default, Redis works _in-memory_ , which means that it does not store data persistently.
An excellent use case for Redis is to use it as a cache. Caches are often used to store data that is otherwise slow to fetch and save until it's no longer valid. After the cache becomes invalid, you would then fetch the data again and store it in the cache.
Redis has nothing to do with containers. But since we are already able to add _any_ 3rd party service to your applications, why not learn about a new one?
### Exercises 12.9. - 12.11
#### Exercise 12.9: Set up Redis for the project
The Express server has already been configured to use Redis, and it is only missing the _REDIS_URL_ environment variable. The application will use that environment variable to connect to the Redis. Read through the _todo-app/todo-backend/docker-compose.dev.yml_ by defining another service after mongo:

```
services:
  mongo:
    ...
  redis:
    ???copy
```

Since the Docker Hub page doesn't have all the info, we can use Google to aid us. The default port for Redis is found by doing so:
![google search result for "default port for redis" is 6379](../assets/2a9ddc7879ac306c.png)
We won't have any idea if the configuration works unless we try it. The application will not start using Redis by itself, that shall happen in the next exercise.
Once Redis is configured and started, restart the backend and give it the _REDIS_URL_ , which has the form _redis://host:port_

```
REDIS_URL=insert-redis-url-here MONGO_URL=mongodb://the_username:the_password@localhost:3456/the_database npm run devcopy
```

You can now test the configuration by adding the line

```
const redis = require('../redis')copy
```

to the Express server e.g. in the file _routes/index.js_. If nothing happens, the configuration is done right. If not, the server crashes:

```
events.js:291
      throw er; // Unhandled 'error' event
      ^

Error: Redis connection to localhost:637 failed - connect ECONNREFUSED 127.0.0.1:6379
    at TCPConnectWrap.afterConnect [as oncomplete] (net.js:1144:16)
Emitted 'error' event on RedisClient instance at:
    at RedisClient.on_error (/Users/mluukkai/opetus/docker-fs/container-app/express-app/node_modules/redis/index.js:342:14)
    at Socket.<anonymous> (/Users/mluukkai/opetus/docker-fs/container-app/express-app/node_modules/redis/index.js:223:14)
    at Socket.emit (events.js:314:20)
    at emitErrorNT (internal/streams/destroy.js:100:8)
    at emitErrorCloseNT (internal/streams/destroy.js:68:3)
    at processTicksAndRejections (internal/process/task_queues.js:80:21) {
  errno: -61,
  code: 'ECONNREFUSED',
  syscall: 'connect',
  address: '127.0.0.1',
  port: 6379
}
[nodemon] app crashed - waiting for file changes before starting...copy
```

#### Exercise 12.10
The project already has

- setAsync function takes in key and value, using the key to store the value.
- getAsync function takes in a key and returns the value in a promise.


Implement a todo counter that saves the number of created todos to Redis:

- Step 1: Whenever a request is sent to add a todo, increment the counter by one.
- Step 2: Create a GET /statistics endpoint where you can ask for the usage metadata. The format should be the following JSON:


```
{
  "added_todos": 0
}copy
```

#### Exercise 12.11
> Use _script_ to record what you do, save the file as script-answers/exercise12_11.txt
If the application does not behave as expected, direct access to the database may be beneficial in pinpointing problems. Let us try out how

- Go to the Redis container with _docker exec_ and open the redis-cli.
- Find the key you used with
- Check the value of the key with the command
- Set the value of the counter to 9001, find the right command from
- Make sure that the new value works by refreshing the page
- Create a new todo with Postman and ensure from redis-cli that the counter has increased accordingly
- Delete the key from the cli and ensure that the counter works when new todos are added


### Persisting data with Redis
In the previous section, it was mentioned that _by default_ Redis does not persist the data. However, the persistence is easy to toggle on. We only need to start the Redis with a different command, as instructed by the

```
services:
  redis:
    # Everything else
    command: ['redis-server', '--appendonly', 'yes'] # Overwrite the CMD
    volumes: # Declare the volume
      - ./redis_data:/datacopy
```

The data will now be persisted to the directory _redis_data_ of the host machine. Remember to add the directory to .gitignore!
#### Other functionality of Redis
In addition to the GET, SET and DEL operations on keys and values, Redis can do also quite a lot more. It can for example automatically expire keys, which is a very useful feature when Redis is used as a cache.
Redis can also be used to implement the so-called _message broker_ between two or more services. Some of the services are _publishing_ messages by sending those to Redis, which on arrival of a message, informs the parties that have _subscribed_ to those messages.
### Exercise 12.12
#### Exercise 12.12: Persisting data in Redis
Check that the data is not persisted by default, after running:

```
docker compose -f docker-compose.dev.yml down
docker compose -f docker-compose.dev.yml upcopy
```

the counter value is reset to 0.
Then create a volume for Redis data (by modifying _todo-app/todo-backend/docker-compose.dev.yml_) and make sure that the data survives after running:

```
docker compose -f docker-compose.dev.yml down
docker compose -f docker-compose.dev.yml upcopy
```

[Part 12a **Previous part**](../part12/01-introduction-to-containers.md)[Part 12c **Next part**](../part12/01-basics-of-orchestration.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)
