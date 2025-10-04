---{
  "title": "Node.js and Express",
  "source_url": "https://fullstackopen.com/en/part3/node_js_and_express",
  "crawl_timestamp": "2025-10-04T19:16:19Z",
  "checksum": "1b6c78a126b3fd2187a57224e95d9ca13a9b97087c23825868f30aa6691bf4a4"
}
---[Skip to content](../part3/01-node-js-and-express-course-main-content.md)
[{() => fs}](https://fullstackopen.com/en/)
  * [About course](../about/01-about.md)
  * [Course contents](../#course-contents/01-course-contents.md)
  * [FAQ](../faq/01-faq.md)
  * [Partners](../companies/01-companies.md)
  * [Challenge](../challenge/01-challenge.md)
[Search from the material](../search/01-search.md)Toggle dark theme
Select languageSuomi English 中文 Español Français Português(BR) 

[Fullstack](../#course-contents/01-course-contents.md)
[Part 3](../part3/01-part3.md)
Node.js and Express
a Node.js and Express
  * [Simple web server](../part3/01-node-js-and-express-simple-web-server.md)
  * [Express](../part3/01-node-js-and-express-express.md)
  * [Web and Express](../part3/01-node-js-and-express-web-and-express.md)
  * [Automatic Change Tracking](../part3/01-node-js-and-express-automatic-change-tracking.md)
  * [REST](../part3/01-node-js-and-express-rest.md)
  * [Fetching a single resource](../part3/01-node-js-and-express-fetching-a-single-resource.md)
  * [Deleting resources](../part3/01-node-js-and-express-deleting-resources.md)
  * [Postman](../part3/01-node-js-and-express-postman.md)
  * [The Visual Studio Code REST client](../part3/01-node-js-and-express-the-visual-studio-code-rest-client.md)
  * [The WebStorm HTTP Client](../part3/01-node-js-and-express-the-web-storm-http-client.md)
  * [Receiving data](../part3/01-node-js-and-express-receiving-data.md)
  * [Exercises 3.1.-3.6.](../part3/01-node-js-and-express-exercises-3-1-3-6.md)
  * [About HTTP request types](../part3/01-node-js-and-express-about-http-request-types.md)
  * [Middleware](../part3/01-node-js-and-express-middleware.md)
  * [Exercises 3.7.-3.8.](../part3/01-node-js-and-express-exercises-3-7-3-8.md)


[b Deploying app to internet](../part3/01-deploying-app-to-internet.md)[c Saving data to MongoDB](../part3/01-saving-data-to-mongo-db.md)[d Validation and ESLint](../part3/01-validation-and-es-lint.md)
a
# Node.js and Express
In this part, our focus shifts towards the backend: that is, towards implementing functionality on the server side of the stack.
We will be building our backend on top of 
This course material was written with version _v22.3.0_ of Node.js. Please make sure that your version of Node is at least as new as the version used in the material (you can check the version by running _node -v_ in the command line).
As mentioned in [part 1](../part1/01-java-script.md), browsers don't yet support the newest features of JavaScript, and that is why the code running in the browser must be _transpiled_ with e.g. 
Our goal is to implement a backend that will work with the notes application from [part 2](../part2/01-part2.md). However, let's start with the basics by implementing a classic "hello world" application.
**Notice** that the applications and exercises in this part are not all React applications, and we will not use the _create vite@latest -- --template react_ utility for initializing the project for this application.
We had already mentioned [npm](../part2/01-getting-data-from-server-npm.md) back in part 2, which is a tool used for managing JavaScript packages. In fact, npm originates from the Node ecosystem.
Let's navigate to an appropriate directory, and create a new template for our application with the _npm init_ command. We will answer the questions presented by the utility, and the result will be an automatically generated _package.json_ file at the root of the project that contains information about the project.
```
{
  "name": "backend",
  "version": "0.0.1",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "author": "Matti Luukkainen",
  "license": "MIT"
}copy
```

The file defines, for instance, that the entry point of the application is the _index.js_ file.
Let's make a small change to the _scripts_ object by adding a new script command.
```
{
  // ...
  "scripts": {
    "start": "node index.js",    "test": "echo \"Error: no test specified\" && exit 1"
  },
  // ...
}copy
```

Next, let's create the first version of our application by adding an _index.js_ file to the root of the project with the following code:
```
console.log('hello world')copy
```

We can run the program directly with Node from the command line:
```
node index.jscopy
```

Or we can run it as an 
```
npm startcopy
```

The _start_ npm script works because we defined it in the _package.json_ file:
```
{
  // ...
  "scripts": {
    "start": "node index.js",
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  // ...
}copy
```

Even though the execution of the project works when it is started by calling _node index.js_ from the command line, it's customary for npm projects to execute such tasks as npm scripts.
By default, the _package.json_ file also defines another commonly used npm script called _npm test_. Since our project does not yet have a testing library, the _npm test_ command simply executes the following command:
```
echo "Error: no test specified" && exit 1copy
```

### Simple web server
Let's change the application into a web server by editing the _index.js_ file as follows:
```
const http = require('http')

const app = http.createServer((request, response) => {
  response.writeHead(200, { 'Content-Type': 'text/plain' })
  response.end('Hello World')
})

const PORT = 3001
app.listen(PORT)
console.log(`Server running on port ${PORT}`)copy
```

Once the application is running, the following message is printed in the console:
```
Server running on port 3001copy
```

We can open our humble application in the browser by visiting the address 
![hello world screen capture](../assets/3e9709fbbd7297a9.png)
The server works the same way regardless of the latter part of the URL. Also the address 
**NB** If port 3001 is already in use by some other application, then starting the server will result in the following error message:
```
➜  hello npm start

> hello@1.0.0 start /Users/mluukkai/opetus/_2019fullstack-code/part3/hello
> node index.js

Server running on port 3001
events.js:167
      throw er; // Unhandled 'error' event
      ^

Error: listen EADDRINUSE :::3001
    at Server.setupListenHandle [as _listen2] (net.js:1330:14)
    at listenInCluster (net.js:1378:12)copy
```

You have two options. Either shut down the application using port 3001 (the JSON Server in the last part of the material was using port 3001), or use a different port for this application.
Let's take a closer look at the first line of the code:
```
const http = require('http')copy
```

In the first row, the application imports Node's built-in 
```
import http from 'http'copy
```

These days, code that runs in the browser uses ES6 modules. Modules are defined with an 
Node.js uses 
CommonJS modules function almost exactly like ES6 modules, at least as far as our needs in this course are concerned.
The next chunk in our code looks like this:
```
const app = http.createServer((request, response) => {
  response.writeHead(200, { 'Content-Type': 'text/plain' })
  response.end('Hello World')
})copy
```

The code uses the _createServer_ method of the _event handler_ is registered to the server that is called _every time_ an HTTP request is made to the server's address 
The request is responded to with the status code 200, with the _Content-Type_ header set to _text/plain_ , and the content of the site to be returned set to _Hello World_.
The last rows bind the http server assigned to the _app_ variable, to listen to HTTP requests sent to port 3001:
```
const PORT = 3001
app.listen(PORT)
console.log(`Server running on port ${PORT}`)copy
```

The primary purpose of the backend server in this course is to offer raw data in JSON format to the frontend. For this reason, let's immediately change our server to return a hardcoded list of notes in the JSON format:
```
const http = require('http')

let notes = [  {    id: "1",    content: "HTML is easy",    important: true  },  {    id: "2",    content: "Browser can execute only JavaScript",    important: false  },  {    id: "3",    content: "GET and POST are the most important methods of HTTP protocol",    important: true  }]const app = http.createServer((request, response) => {  response.writeHead(200, { 'Content-Type': 'application/json' })  response.end(JSON.stringify(notes))})
const PORT = 3001
app.listen(PORT)
console.log(`Server running on port ${PORT}`)copy
```

Let's restart the server (you can shut the server down by pressing _Ctrl+C_ in the console) and let's refresh the browser.
The _application/json_ value in the _Content-Type_ header informs the receiver that the data is in the JSON format. The _notes_ array gets transformed into JSON formatted string with the _JSON.stringify(notes)_ method. This is necessary because the response.end() method expects a string or a buffer to send as the response body.
When we open the browser, the displayed format is exactly the same as in [part 2](../part2/01-getting-data-from-server.md) where we used 
![formatted JSON notes data](../assets/5852fa3ba64f40b7.png)
### Express
Implementing our server code directly with Node's built-in 
Many libraries have been developed to ease server-side development with Node, by offering a more pleasing interface to work with the built-in http module. These libraries aim to provide a better abstraction for general use cases we usually require to build a backend server. By far the most popular library intended for this purpose is 
Let's take Express into use by defining it as a project dependency with the command:
```
npm install expresscopy
```

The dependency is also added to our _package.json_ file:
```
{
  // ...
  "dependencies": {
    "express": "^5.1.0"
  }
}copy
```

The source code for the dependency is installed in the _node_modules_ directory located at the root of the project. In addition to Express, you can find a great number of other dependencies in the directory:
![ls command listing of dependencies in directory](../assets/c3a17a96f2a2f1e9.png)
These are the dependencies of the Express library and the dependencies of all of its dependencies, and so forth. These are called the 
Version 5.1.0 of Express was installed in our project. What does the caret in front of the version number in _package.json_ mean?
```
"express": "^5.1.0"copy
```

The versioning model used in npm is called 
The caret in the front of _^5.1.0_ means that if and when the dependencies of a project are updated, the version of Express that is installed will be at least _5.1.0_. However, the installed version of Express can also have a larger _patch_ number (the last number), or a larger _minor_ number (the middle number). The major version of the library indicated by the first _major_ number must be the same.
We can update the dependencies of the project with the command:
```
npm updatecopy
```

Likewise, if we start working on the project on another computer, we can install all up-to-date dependencies of the project defined in _package.json_ by running this next command in the project's root directory:
```
npm installcopy
```

If the _major_ number of a dependency does not change, then the newer versions should be 
### Web and Express
Let's get back to our application and make the following changes:
```
const express = require('express')
const app = express()

let notes = [
  ...
]

app.get('/', (request, response) => {
  response.send('<h1>Hello World!</h1>')
})

app.get('/api/notes', (request, response) => {
  response.json(notes)
})

const PORT = 3001
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`)
})copy
```

To get the new version of our application into use, first we have to restart it.
The application did not change a whole lot. Right at the beginning of our code, we're importing _express_ , which this time is a _function_ that is used to create an Express application stored in the _app_ variable:
```
const express = require('express')
const app = express()copy
```

Next, we define two _routes_ to the application. The first one defines an event handler that is used to handle HTTP GET requests made to the application's _/_ root:
```
app.get('/', (request, response) => {
  response.send('<h1>Hello World!</h1>')
})copy
```

The event handler function accepts two parameters. The first 
In our code, the request is answered by using the _response_ object. Calling the method makes the server respond to the HTTP request by sending a response containing the string `<h1>Hello World!</h1>` that was passed to the _send_ method. Since the parameter is a string, Express automatically sets the value of the _Content-Type_ header to be _text/html_. The status code of the response defaults to 200.
We can verify this from the _Network_ tab in developer tools:
![network tab in dev tools](../assets/9f4ca3b485aa07b8.png)
The second route defines an event handler that handles HTTP GET requests made to the _notes_ path of the application:
```
app.get('/api/notes', (request, response) => {
  response.json(notes)
})copy
```

The request is responded to with the _response_ object. Calling the method will send the **notes** array that was passed to it as a JSON formatted string. Express automatically sets the _Content-Type_ header with the appropriate value of _application/json_.
![api/notes gives the formatted JSON data again](../assets/b83b00a4df3a38c7.png)
Next, let's take a quick look at the data sent in JSON format.
In the earlier version where we were only using Node, we had to transform the data into the JSON formatted string with the _JSON.stringify_ method:
```
response.end(JSON.stringify(notes))copy
```

With Express, this is no longer required, because this transformation happens automatically.
It's worth noting that _notes_.
The experiment shown below illustrates this point:
![node terminal demonstrating json is of type string](../assets/7d6835ce67bfd7d3.png)
The experiment above was done in the interactive _node_ in the command line. The repl is particularly useful for testing how commands work while you're writing application code. I highly recommend this!
### Automatic Change Tracking
If we change the application's code, we first need to stop the application from the console (_ctrl_ + _c_) and then restart it for the changes to take effect. Restarting feels cumbersome compared to React's smooth workflow, where the browser automatically updates when the code changes.
You can make the server track our changes by starting it with the _--watch_ option:
```
node --watch index.jscopy
```

Now, changes to the application's code will cause the server to restart automatically. Note that although the server restarts automatically, you still need to refresh the browser. Unlike with React, we do not have, nor could we have, a hot reload functionality that updates the browser in this scenario (where we return JSON data).
Let's define a custom _npm script_ in the _package.json_ file to start the development server:
```
{
  // ..
  "scripts": {
    "start": "node index.js",
    "dev": "node --watch index.js",    "test": "echo \"Error: no test specified\" && exit 1"
  },
  // ..
}copy
```

We can now start the server in development mode with the command
```
npm run devcopy
```

Unlike when running the _start_ or _test_ scripts, the command must include _run_. 
### REST
Let's expand our application so that it provides the same RESTful HTTP API as 
Representational State Transfer, aka REST, was introduced in 2000 in Roy Fielding's 
We are not going to dig into Fielding's definition of REST or spend time pondering about what is and isn't RESTful. Instead, we take a more 
We mentioned in the [previous part](../part2/01-altering-data-in-server-rest.md) that singular things, like notes in the case of our application, are called _resources_ in RESTful thinking. Every resource has an associated URL which is the resource's unique address.
One convention for creating unique addresses is to combine the name of the resource type with the resource's unique identifier.
Let's assume that the root URL of our service is _www.example.com/api_.
If we define the resource type of note to be _notes_ , then the address of a note resource with the identifier 10, has the unique address _www.example.com/api/notes/10_.
The URL for the entire collection of all note resources is _www.example.com/api/notes_.
We can execute different operations on resources. The operation to be executed is defined by the HTTP _verb_ :
URL | verb | functionality  
---|---|---  
notes/10 | GET | fetches a single resource  
notes | GET | fetches all resources in the collection  
notes | POST | creates a new resource based on the request data  
notes/10 | DELETE | removes the identified resource  
notes/10 | PUT | replaces the entire identified resource with the request data  
notes/10 | PATCH | replaces a part of the identified resource with the request data  
|  |   
This is how we manage to roughly define what REST refers to as a 
This way of interpreting REST falls under the 
In some places (see e.g. 
### Fetching a single resource
Let's expand our application so that it offers a REST interface for operating on individual notes. First, let's create a 
The unique address we will use for an individual note is of the form _notes/10_ , where the number at the end refers to the note's unique id number.
We can define 
```
app.get('/api/notes/:id', (request, response) => {
  const id = request.params.id
  const note = notes.find(note => note.id === id)
  response.json(note)
})copy
```

Now `app.get('/api/notes/:id', ...)` will handle all HTTP GET requests that are of the form _/api/notes/SOMETHING_ , where _SOMETHING_ is an arbitrary string.
The _id_ parameter in the route of a request can be accessed through the 
```
const id = request.params.idcopy
```

The now familiar _find_ method of arrays is used to find the note with an id that matches the parameter. The note is then returned to the sender of the request.
We can now test our application by going to 
![api/notes/1 gives a single note as JSON](../assets/55cc134fce863507.png)
However, there's another problem with our application.
If we search for a note with an id that does not exist, the server responds with:
![network tools showing 200 and content-length 0](../assets/15e48e3784fb4e82.png)
The HTTP status code that is returned is 200, which means that the response succeeded. There is no data sent back with the response, since the value of the _content-length_ header is 0, and the same can be verified from the browser.
The reason for this behavior is that the _note_ variable is set to _undefined_ if no matching note is found. The situation needs to be handled on the server in a better way. If no note is found, the server should respond with the status code 
Let's make the following change to our code:
```
app.get('/api/notes/:id', (request, response) => {
  const id = request.params.id
  const note = notes.find(note => note.id === id)
  
  if (note) {    response.json(note)  } else {    response.status(404).end()  }})copy
```

Since no data is attached to the response, we use the 
The if-condition leverages the fact that all JavaScript objects are _undefined_ is 
Our application works and sends the error status code if no note is found. However, the application doesn't return anything to show to the user, like web applications normally do when we visit a page that does not exist. We do not need to display anything in the browser because REST APIs are interfaces that are intended for programmatic use, and the error status code is all that is needed.
Anyway, it's possible to give a clue about the reason for sending a 404 error by 
### Deleting resources
Next, let's implement a route for deleting resources. Deletion happens by making an HTTP DELETE request to the URL of the resource:
```
app.delete('/api/notes/:id', (request, response) => {
  const id = request.params.id
  notes = notes.filter(note => note.id !== id)

  response.status(204).end()
})copy
```

If deleting the resource is successful, meaning that the note exists and is removed, we respond to the request with the status code 
There's no consensus on what status code should be returned to a DELETE request if the resource does not exist. The only two options are 204 and 404. For the sake of simplicity, our application will respond with 204 in both cases.
### Postman
So how do we test the delete operation? HTTP GET requests are easy to make from the browser. We could write some JavaScript for testing deletion, but writing test code is not always the best solution in every situation.
Many tools exist for making the testing of backends easier. One of these is a command line program 
Let's install the Postman desktop client 
![postman screenshot on api/notes/2](../assets/4d335017fca6099b.png) NB: Postman is also available on VS Code which can be downloaded from the Extension tab on the left -> search for Postman -> First result (Verified Publisher) -> Install You will then see an extra icon added on the activity bar below the extensions tab. Once you log in, you can follow the steps below 
Using Postman is quite easy in this situation. It's enough to define the URL and then select the correct request type (DELETE).
The backend server appears to respond correctly. By making an HTTP GET request to 
Because the notes in the application are only saved to memory, the list of notes will return to its original state when we restart the application.
### The Visual Studio Code REST client
If you use Visual Studio Code, you can use the VS Code 
Once the plugin is installed, using it is very simple. We make a directory at the root of the application named _requests_. We save all the REST client requests in the directory as files that end with the _.rest_ extension.
Let's create a new _get_all_notes.rest_ file and define the request that fetches all notes.
![get all notes rest file with get request on notes](../assets/61de9528795c86c6.png)
By clicking the _Send Request_ text, the REST client will execute the HTTP request and the response from the server is opened in the editor.
![response from vs code from get request](../assets/c6b584cece69a936.png)
### The WebStorm HTTP Client
If you use _IntelliJ WebStorm_ instead, you can use a similar procedure with its built-in HTTP Client. Create a new file with extension `.rest` and the editor will display your options to create and run your requests. You can learn more about it by following 
### Receiving data
Next, let's make it possible to add new notes to the server. Adding a note happens by making an HTTP POST request to the address 
To access the data easily, we need the help of the Express _app.use(express.json())_.
Let's activate the json-parser and implement an initial handler for dealing with the HTTP POST requests:
```
const express = require('express')
const app = express()

app.use(express.json())
//...

app.post('/api/notes', (request, response) => {  const note = request.body  console.log(note)  response.json(note)})copy
```

The event handler function can access the data from the _body_ property of the _request_ object.
Without the json-parser, the _body_ property would be undefined. The json-parser takes the JSON data of a request, transforms it into a JavaScript object and then attaches it to the _body_ property of the _request_ object before the route handler is called.
For the time being, the application does not do anything with the received data besides printing it to the console and sending it back in the response.
Before we implement the rest of the application logic, let's verify with Postman that the data is in fact received by the server. In addition to defining the URL and request type in Postman, we also have to define the data sent in the _body_ :
![postman post on api/notes with post content](../assets/ba1530bc4ab8f1ef.png)
The application prints the data that we sent in the request to the console:
![terminal printing content provided in postman](../assets/a3cba3a400905a85.png)
**NOTE:** When programming the backend, _keep the console running the application visible at all times_. The development server will restart if changes are made to the code, so by monitoring the console, you will immediately notice if there is an error in the application's code:
![console error about SyntaxError](../assets/eab07ab85c3d3bd8.png)
Similarly, it is useful to check the console to make sure that the backend behaves as we expect it to in different situations, like when we send data with an HTTP POST request. Naturally, it's a good idea to add lots of _console.log_ commands to the code while the application is still being developed.
A potential cause for issues is an incorrectly set _Content-Type_ header in requests. This can happen with Postman if the type of body is not defined correctly:
![postman having text as content-type](../assets/91566873ec162a97.png)
The _Content-Type_ header is set to _text/plain_ :
![postman showing headers and content-type as text/plain](../assets/27b0d78b779ad445.png)
The server appears to only receive an empty object:
![console output showing empty curly braces](../assets/71457ee685577ff8.png)
The server will not be able to parse the data correctly without the correct value in the header. It won't even try to guess the format of the data since there's a _Content-Types_.
If you are using VS Code, then you should install the REST client from the previous chapter _now, if you haven't already_. The POST request can be sent with the REST client like this:
![sample post request in vscode with JSON data](../assets/44961789d81929ec.png)
We created a new _create_note.rest_ file for the request. The request is formatted according to the 
One benefit that the REST client has over Postman is that the requests are handily available at the root of the project repository, and they can be distributed to everyone in the development team. You can also add multiple requests in the same file using `###` separators:
```
GET http://localhost:3001/api/notes/

###
POST http://localhost:3001/api/notes/ HTTP/1.1
content-type: application/json

{
    "name": "sample",
    "time": "Wed, 21 Oct 2015 18:27:50 GMT"
}copy
```

Postman also allows users to save requests, but the situation can get quite chaotic especially when you're working on multiple unrelated projects.
> **Important sidenote**
> Sometimes when you're debugging, you may want to find out what headers have been set in the HTTP request. One way of accomplishing this is through the _request_ object, that can be used for getting the value of a single header. The _request_ object also has the _headers_ property, that contains all of the headers of a specific request.
> Problems can occur with the VS REST client if you accidentally add an empty line between the top row and the row specifying the HTTP headers. In this situation, the REST client interprets this to mean that all headers are left empty, which leads to the backend server not knowing that the data it has received is in the JSON format.
> You will be able to spot this missing _Content-Type_ header if at some point in your code you print all of the request headers with the _console.log(request.headers)_ command.
Let's return to the application. Once we know that the application receives data correctly, it's time to finalize the handling of the request:
```
app.post('/api/notes', (request, response) => {
  const maxId = notes.length > 0
    ? Math.max(...notes.map(n => Number(n.id))) 
    : 0

  const note = request.body
  note.id = String(maxId + 1)

  notes = notes.concat(note)

  response.json(note)
})copy
```

We need a unique id for the note. First, we find out the largest id number in the current list and assign it to the _maxId_ variable. The id of the new note is then defined as _maxId + 1_ as a string. This method is not recommended, but we will live with it for now as we will replace it soon enough.
The current version still has the problem that the HTTP POST request can be used to add objects with arbitrary properties. Let's improve the application by defining that the _content_ property may not be empty. The _important_ property will be given a default value of false. All other properties are discarded:
```
const generateId = () => {
  const maxId = notes.length > 0
    ? Math.max(...notes.map(n => Number(n.id)))
    : 0
  return String(maxId + 1)
}

app.post('/api/notes', (request, response) => {
  const body = request.body

  if (!body.content) {
    return response.status(400).json({ 
      error: 'content missing' 
    })
  }

  const note = {
    content: body.content,
    important: body.important || false,
    id: generateId(),
  }

  notes = notes.concat(note)

  response.json(note)
})copy
```

The logic for generating the new id number for notes has been extracted into a separate _generateId_ function.
If the received data is missing a value for the _content_ property, the server will respond to the request with the status code 
```
if (!body.content) {
  return response.status(400).json({ 
    error: 'content missing' 
  })
}copy
```

Notice that calling return is crucial because otherwise the code will execute to the very end and the malformed note gets saved to the application.
If the content property has a value, the note will be based on the received data. If the _important_ property is missing, we will default the value to _false_. The default value is currently generated in a rather odd-looking way:
```
important: body.important || false,copy
```

If the data saved in the _body_ variable has the _important_ property, the expression will evaluate its value and convert it to a boolean value. If the property does not exist, then the expression will evaluate to false which is defined on the right-hand side of the vertical lines.
> To be exact, when the _important_ property is _false_ , then the _body.important || false_ expression will in fact return the _false_ from the right-hand side...
You can find the code for our current application in its entirety in the _part3-1_ branch of 
![GitHub screenshot of branch 3-1](../assets/20a7627ec436b113.png)
If you clone the project, run the _npm install_ command before starting the application with _npm start_ or _npm run dev_.
One more thing before we move on to the exercises. The function for generating IDs looks currently like this:
```
const generateId = () => {
  const maxId = notes.length > 0
    ? Math.max(...notes.map(n => Number(n.id)))
    : 0
  return String(maxId + 1)
}copy
```

The function body contains a row that looks a bit intriguing:
```
Math.max(...notes.map(n => Number(n.id)))copy
```

What exactly is happening in that line of code? _notes.map(n = > n.id)_ creates a new array that contains all the ids of the notes in number form. _notes.map(n = > Number(n.id))_ is an _array_ so it can't directly be given as a parameter to _Math.max_. The array can be transformed into individual numbers by using the "three dot" _..._.
### Exercises 3.1.-3.6.
**NB:** Because this is not a frontend project and we are not working with React, the application **is not created** with create vite@latest -- --template react. You initialize this project with the _npm init_ command that was demonstrated earlier in this part of the material.
**NB:** Because the "node_modules" is created using "npm init", it will not be excluded when you are trying to add your code to git using "git add .", therefore please create a file called ".gitignore" and write "node_modules" so that git ignores it everytime you try to add, commit or push to a remote repo. 
**Strong recommendation:** When you are working on backend code, always keep an eye on what's going on in the terminal that is running your application.
#### 3.1: Phonebook backend step 1
Implement a Node application that returns a hardcoded list of phonebook entries from the address 
Data:
```
[
    { 
      "id": "1",
      "name": "Arto Hellas", 
      "number": "040-123456"
    },
    { 
      "id": "2",
      "name": "Ada Lovelace", 
      "number": "39-44-5323523"
    },
    { 
      "id": "3",
      "name": "Dan Abramov", 
      "number": "12-43-234345"
    },
    { 
      "id": "4",
      "name": "Mary Poppendieck", 
      "number": "39-23-6423122"
    }
]copy
```

Output in the browser after GET request:
![JSON data of 4 people in browser from api/persons](../assets/887e6b17062ec5c4.png)
Notice that the forward slash in the route _api/persons_ is not a special character, and is just like any other character in the string.
The application must be started with the command _npm start_.
The application must also offer an _npm run dev_ command that will run the application and restart the server whenever changes are made and saved to a file in the source code.
#### 3.2: Phonebook backend step 2
Implement a page at the address 
![Screenshot for 3.2](../assets/6c7dd97f14feb25a.png)
The page has to show the time that the request was received and how many entries are in the phonebook at the time of processing the request.
#### 3.3: Phonebook backend step 3
Implement the functionality for displaying the information for a single phonebook entry. The url for getting the data for a person with the id 5 should be 
If an entry for the given id is not found, the server has to respond with the appropriate status code.
#### 3.4: Phonebook backend step 4
Implement functionality that makes it possible to delete a single phonebook entry by making an HTTP DELETE request to the unique URL of that phonebook entry.
Test that your functionality works with either Postman or the Visual Studio Code REST client.
#### 3.5: Phonebook backend step 5
Expand the backend so that new phonebook entries can be added by making HTTP POST requests to the address 
Generate a new id for the phonebook entry with the 
#### 3.6: Phonebook backend step 6
Implement error handling for creating new entries. The request is not allowed to succeed, if:
  * The name or number is missing
  * The name already exists in the phonebook


Respond to requests like these with the appropriate status code, and also send back information that explains the reason for the error, e.g.:
```
{ error: 'name must be unique' }copy
```

### About HTTP request types
**safety** and **idempotency**.
The HTTP GET request should be _safe_ :
> _In particular, the convention has been established that the GET and HEAD methods SHOULD NOT have the significance of taking an action other than retrieval. These methods ought to be considered "safe"._
Safety means that the executing request must not cause any _side effects_ on the server. By side effects, we mean that the state of the database must not change as a result of the request, and the response must only return data that already exists on the server.
Nothing can ever guarantee that a GET request is _safe_ , this is just a recommendation that is defined in the HTTP standard. By adhering to RESTful principles in our API, GET requests are always used in a way that they are _safe_.
The HTTP standard also defines the request type 
All HTTP requests except POST should be _idempotent_ :
> _Methods can also have the property of "idempotence" in that (aside from error or expiration issues) the side-effects of N > 0 identical requests is the same as for a single request. The methods GET, HEAD, PUT and DELETE share this property_
This means that if a request does generate side effects, then the result should be the same regardless of how many times the request is sent.
If we make an HTTP PUT request to the URL _/api/notes/10_ and with the request we send the data _{ content: "no side effects!", important: true }_ , the result is the same regardless of how many times the request is sent.
Like _safety_ for the GET request, _idempotence_ is also just a recommendation in the HTTP standard and not something that can be guaranteed simply based on the request type. However, when our API adheres to RESTful principles, then GET, HEAD, PUT, and DELETE requests are used in such a way that they are idempotent.
POST is the only HTTP request type that is neither _safe_ nor _idempotent_. If we send 5 different HTTP POST requests to _/api/notes_ with a body of _{content: "many same", important: true}_ , the resulting 5 notes on the server will all have the same content.
### Middleware
The Express 
Middleware are functions that can be used for handling _request_ and _response_ objects.
The json-parser we used earlier takes the raw data from the requests that are stored in the _request_ object, parses it into a JavaScript object and assigns it to the _request_ object as a new property _body_.
In practice, you can use several middlewares at the same time. When you have more than one, they're executed one by one in the order that they were listed in the application code.
Let's implement our own middleware that prints information about every request that is sent to the server.
Middleware is a function that receives three parameters:
```
const requestLogger = (request, response, next) => {
  console.log('Method:', request.method)
  console.log('Path:  ', request.path)
  console.log('Body:  ', request.body)
  console.log('---')
  next()
}copy
```

At the end of the function body, the _next_ function that was passed as a parameter is called. The _next_ function yields control to the next middleware.
Middleware is used like this:
```
app.use(requestLogger)copy
```

Remember, middleware functions are called in the order that they're encountered by the JavaScript engine. Notice that _json-parser_ is listed before _requestLogger_ , because otherwise _request.body_ will not be initialized when the logger is executed!
Middleware functions have to be used before routes when we want them to be executed by the route event handlers. Sometimes, we want to use middleware functions after routes. We do this when the middleware functions are only called if no route handler processes the HTTP request.
Let's add the following middleware after our routes. This middleware will be used for catching requests made to non-existent routes. For these requests, the middleware will return an error message in the JSON format.
```
const unknownEndpoint = (request, response) => {
  response.status(404).send({ error: 'unknown endpoint' })
}

app.use(unknownEndpoint)copy
```

You can find the code for our current application in its entirety in the _part3-2_ branch of 
### Exercises 3.7.-3.8.
#### 3.7: Phonebook backend step 7
Add the _tiny_ configuration.
The documentation for Morgan is not the best, and you may have to spend some time figuring out how to configure it correctly. However, most documentation in the world falls under the same category, so it's good to learn to decipher and interpret cryptic documentation in any case.
Morgan is installed just like all other libraries with the _npm install_ command. Taking morgan into use happens the same way as configuring any other middleware by using the _app.use_ command.
#### 3.8*: Phonebook backend step 8
Configure morgan so that it also shows the data sent in HTTP POST requests:
![terminal showing post data being sent](../assets/d5602c6a5067d1ec.png)
Note that logging data even in the console can be dangerous since it can contain sensitive data and may violate local privacy law (e.g. GDPR in EU) or business-standard. In this exercise, you don't have to worry about privacy issues, but in practice, try not to log any sensitive data.
This exercise can be quite challenging, even though the solution does not require a lot of code.
This exercise can be completed in a few different ways. One of the possible solutions utilizes these two techniques:
[ Part 2 **Previous part** ](../part2/01-part2.md)[ Part 3b **Next part** ](../part3/01-deploying-app-to-internet.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)