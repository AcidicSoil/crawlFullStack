---{
  "title": "Getting data from server",
  "source_url": "https://fullstackopen.com/en/part2/getting_data_from_server",
  "crawl_timestamp": "2025-10-04T19:16:13Z",
  "checksum": "d8a172a630127a53a033240ed1029f6077d3ca286f42d4a79a6980255ca67648"
}
---[Skip to content](../part2/01-getting-data-from-server-course-main-content.md)
[{() => fs}](https://fullstackopen.com/en/)

- [About course](../about/01-about.md)
- [Course contents](../#course-contents/01-course-contents.md)
- [FAQ](../faq/01-faq.md)
- [Partners](../companies/01-companies.md)
- [Challenge](../challenge/01-challenge.md)
[Search from the material](../search/01-search.md)Toggle dark theme
Select languageSuomi English 中文 Español Français Português(BR)

[Fullstack](../#course-contents/01-course-contents.md)
[Part 2](../part2/01-part2.md)
Getting data from server
[a Rendering a collection, modules](../part2/01-rendering-a-collection-modules.md)[b Forms](../part2/01-forms.md)
c Getting data from server

- [The browser as a runtime environment](../part2/01-getting-data-from-server-the-browser-as-a-runtime-environment.md)
- [npm](../part2/01-getting-data-from-server-npm.md)
- [Axios and promises](../part2/01-getting-data-from-server-axios-and-promises.md)
- [Effect-hooks](../part2/01-getting-data-from-server-effect-hooks.md)
- [The development runtime environment](../part2/01-getting-data-from-server-the-development-runtime-environment.md)
- [Exercise 2.11.](../part2/01-getting-data-from-server-exercise-2-11.md)


[d Altering data in server](../part2/01-altering-data-in-server.md)[e Adding styles to React app](../part2/01-adding-styles-to-react-app.md)
c
# Getting data from server
For a while now we have only been working on "frontend", i.e. client-side (browser) functionality. We will begin working on "backend", i.e. server-side functionality in the [third part](../part3/01-part3.md) of this course. Nonetheless, we will now take a step in that direction by familiarizing ourselves with how the code executing in the browser communicates with the backend.
Let's use a tool meant to be used during software development called
Create a file named _db.json_ in the root directory of the previous _notes_ project with the following content:

```
{
  "notes": [
    {
      "id": "1",
      "content": "HTML is easy",
      "important": true
    },
    {
      "id": "2",
      "content": "Browser can execute only JavaScript",
      "important": false
    },
    {
      "id": "3",
      "content": "GET and POST are the most important methods of HTTP protocol",
      "important": true
    }
  ]
}copy
```

You can start the JSON Server without a separate installation by running the following _npx_ command in the root directory of the application:

```
npx json-server --port 3001 db.jsoncopy
```

The JSON Server starts running on port 3000 by default, but we will now define an alternate port 3001. Let's navigate to the address
![notes on json format in the browser at localhost:3001/notes](../assets/012b56cda8843601.png)
If your browser doesn't have a way to format the display of JSON-data, then install an appropriate plugin, e.g.
Going forward, the idea will be to save the notes to the server, which in this case means saving them to the json-server. The React code fetches the notes from the server and renders them to the screen. Whenever a new note is added to the application, the React code also sends it to the server to make the new note persist in "memory".
json-server stores all the data in the _db.json_ file, which resides on the server. In the real world, data would be stored in some kind of database. However, json-server is a handy tool that enables the use of server-side functionality in the development phase without the need to program any of it.
We will get familiar with the principles of implementing server-side functionality in more detail in [part 3](../part3/01-part3.md) of this course.
### The browser as a runtime environment
Our first task is fetching the already existing notes to our React application from the address
In the part0 [example project](../part0/01-fundamentals-of-web-apps-running-application-logic-on-the-browser.md), we already learned a way to fetch data from a server using JavaScript. The code in the example was fetching the data using
The use of XHR is no longer recommended, and browsers already widely support the
As a reminder from part0 (which one should _remember to not use_ without a pressing reason), data was fetched using XHR in the following way:

```
const xhttp = new XMLHttpRequest()

xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    const data = JSON.parse(this.responseText)
    // handle the response that is saved in variable data
  }
}

xhttp.open('GET', '/data.json', true)
xhttp.send()copy
```

Right at the beginning, we register an _event handler_ to the _xhttp_ object representing the HTTP request, which will be called by the JavaScript runtime whenever the state of the _xhttp_ object changes. If the change in state means that the response to the request has arrived, then the data is handled accordingly.
It is worth noting that the code in the event handler is defined before the request is sent to the server. Despite this, the code within the event handler will be executed at a later point in time. Therefore, the code does not execute synchronously "from top to bottom", but does so _asynchronously_. JavaScript calls the event handler that was registered for the request at some point.
A synchronous way of making requests that's common in Java programming, for instance, would play out as follows (NB, this is not actually working Java code):

```
HTTPRequest request = new HTTPRequest();

String url = "https://studies.cs.helsinki.fi/exampleapp/data.json";
List<Note> notes = request.get(url);

notes.forEach(m => {
  System.out.println(m.content);
});copy
```

In Java, the code executes line by line and stops to wait for the HTTP request, which means waiting for the command _request.get(...)_ to finish. The data returned by the command, in this case the notes, are then stored in a variable, and we begin manipulating the data in the desired manner.
In contrast, JavaScript engines, or runtime environments follow the
When an asynchronous operation is completed, or, more specifically, at some point after its completion, the JavaScript engine calls the event handlers registered to the operation.
Currently, JavaScript engines are _single-threaded_ , which means that they cannot execute code in parallel. As a result, it is a requirement in practice to use a non-blocking model for executing IO operations. Otherwise, the browser would "freeze" during, for instance, the fetching of data from a server.
Another consequence of this single-threaded nature of JavaScript engines is that if some code execution takes up a lot of time, the browser will get stuck for the duration of the execution. If we added the following code at the top of our application:

```
setTimeout(() => {
  console.log('loop..')
  let i = 0
  while (i < 50000000000) {
    i++
  }
  console.log('end')
}, 5000)copy
```

everything would work normally for 5 seconds. However, when the function defined as the parameter for _setTimeout_ is run, the browser will be stuck for the duration of the execution of the long loop. Even the browser tab cannot be closed during the execution of the loop, at least not in Chrome.
For the browser to remain _responsive_ , i.e., to be able to continuously react to user operations with sufficient speed, the code logic needs to be such that no single computation can take too long.
There is a host of additional material on the subject to be found on the internet. One particularly clear presentation of the topic is the keynote by Philip Roberts called
In today's browsers, it is possible to run parallelized code with the help of so-called
### npm
Let's get back to the topic of fetching data from the server.
We could use the previously mentioned promise-based function
That being said, we will be using the _npm packages_ , to React projects.
Nowadays, practically all JavaScript projects are defined using the node package manager, aka _package.json_ file located at the root of the project:

```
{
  "name": "part2-notes-frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "lint": "eslint .",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@eslint/js": "^9.17.0",
    "@types/react": "^18.3.18",
    "@types/react-dom": "^18.3.5",
    "@vitejs/plugin-react": "^4.3.4",
    "eslint": "^9.17.0",
    "eslint-plugin-react": "^7.37.2",
    "eslint-plugin-react-hooks": "^5.0.0",
    "eslint-plugin-react-refresh": "^0.4.16",
    "globals": "^15.14.0",
    "vite": "^6.0.5"
  }
}copy
```

At this point, the _dependencies_ part is of most interest to us as it defines what _dependencies_ , or external libraries, the project has.
We now want to use axios. Theoretically, we could define the library directly in the _package.json_ file, but it is better to install it from the command line.

```
npm install axioscopy
```

**NB _npm_ -commands should always be run in the project root directory**, which is where the _package.json_ file can be found.
Axios is now included among the other dependencies:

```
{
  "name": "part2-notes-frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "lint": "eslint .",
    "preview": "vite preview"
  },
  "dependencies": {
    "axios": "^1.7.9",    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  // ...
}copy
```

In addition to adding axios to the dependencies, the _npm install_ command also _downloaded_ the library code. As with other dependencies, the code can be found in the _node_modules_ directory located in the root. As one might have noticed, _node_modules_ contains a fair amount of interesting stuff.
Let's make another addition. Install _json-server_ as a development dependency (only used during development) by executing the command:

```
npm install json-server --save-devcopy
```

and making a small addition to the _scripts_ part of the _package.json_ file:

```
{
  // ... 
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "lint": "eslint .",
    "preview": "vite preview",
    "server": "json-server -p 3001 db.json"  },
}copy
```

We can now conveniently, without parameter definitions, start the json-server from the project root directory with the command:

```
npm run servercopy
```

We will get more familiar with the _npm_ tool in the [third part of the course](../part3/01-part3.md).
**NB** The previously started json-server must be terminated before starting a new one; otherwise, there will be trouble:
![cannot bind to port 3001 error](../assets/5efc7233ff663edb.png)
The red print in the error message informs us about the issue:
_Cannot bind to port 3001. Please specify another port number either through --port argument or through the json-server.json configuration file_
As we can see, the application is not able to bind itself to the
We used the command _npm install_ twice, but with slight differences:

```
npm install axios
npm install json-server --save-devcopy
```

There is a fine difference in the parameters. _axios_ is installed as a runtime dependency of the application because the execution of the program requires the existence of the library. On the other hand, _json-server_ was installed as a development dependency (_--save-dev_), since the program itself doesn't require it. It is used for assistance during software development. There will be more on different dependencies in the next part of the course.
### Axios and promises
Now we are ready to use Axios. Going forward, json-server is assumed to be running on port 3001.
NB: To run json-server and your react app simultaneously, you may need to use two terminal windows. One to keep json-server running and the other to run our React application.
The library can be brought into use the same way other libraries, i.e., by using an appropriate _import_ statement.
Add the following to the file _main.jsx_ :

```
import axios from 'axios'

const promise = axios.get('http://localhost:3001/notes')
console.log(promise)

const promise2 = axios.get('http://localhost:3001/foobar')
console.log(promise2)copy
```

If you open
![promises printed to console](../assets/9cac821bbe7b27da.png)
Axios' method _get_ returns a
The documentation on Mozilla's site states the following about promises:
> _A Promise is an object representing the eventual completion or failure of an asynchronous operation._
In other words, a promise is an object that represents an asynchronous operation. A promise can have three distinct states:

- The promise is _pending_ : It means that the asynchronous operation corresponding to the promise has not yet finished and the final value is not available yet.
- The promise is _fulfilled_ : It means that the operation has been completed and the final value is available, which generally is a successful operation.
- The promise is _rejected_ : It means that an error prevented the final value from being determined, which generally represents a failed operation.


There are many details related to promises, but understanding these three states is sufficient for us for now. If you want, you can read more about promises in
The first promise in our example is _fulfilled_ , representing a successful _axios.get('_ request. The second one, however, is _rejected_ , and the console tells us the reason. It looks like we were trying to make an HTTP GET request to a non-existent address.
If, and when, we want to access the result of the operation represented by the promise, we must register an event handler to the promise. This is achieved using the method _then_ :

```
const promise = axios.get('http://localhost:3001/notes')

promise.then(response => {
  console.log(response)
})copy
```

The following is printed to the console:
![json object data printed to console](../assets/66a1b25971fddeaf.png)
The JavaScript runtime environment calls the callback function registered by the _then_ method providing it with a _response_ object as a parameter. The _response_ object contains all the essential data related to the response of an HTTP GET request, which would include the returned _data_ , _status code_ , and _headers_.
Storing the promise object in a variable is generally unnecessary, and it's instead common to chain the _then_ method call to the axios method call, so that it follows it directly:

```
axios.get('http://localhost:3001/notes').then(response => {
  const notes = response.data
  console.log(notes)
})copy
```

The callback function now takes the data contained within the response, stores it in a variable, and prints the notes to the console.
A more readable way to format _chained_ method calls is to place each call on its own line:

```
axios
  .get('http://localhost:3001/notes')
  .then(response => {
    const notes = response.data
    console.log(notes)
  })copy
```

The data returned by the server is plain text, basically just one long string. The axios library is still able to parse the data into a JavaScript array, since the server has specified that the data format is _application/json; charset=utf-8_ (see the previous image) using the _content-type_ header.
We can finally begin using the data fetched from the server.
Let's try and request the notes from our local server and render them, initially as the App component. Please note that this approach has many issues, as we're rendering the entire _App_ component only when we successfully retrieve a response:

```
import ReactDOM from 'react-dom/client'
import axios from 'axios'
import App from './App'

axios.get('http://localhost:3001/notes').then(response => {
  const notes = response.data
  ReactDOM.createRoot(document.getElementById('root')).render(<App notes={notes} />)
})copy
```

This method could be acceptable in some circumstances, but it's somewhat problematic. Let's instead move the fetching of the data into the _App_ component.
What's not immediately obvious, however, is where the command _axios.get_ should be placed within the component.
### Effect-hooks
We have already used _functional components_. Version 16.8.0 also introduces
> _Effects let a component connect to and synchronize with external systems._ _This includes dealing with network, browser DOM, animations, widgets written using a different UI library, and other non-React code._
As such, effect hooks are precisely the right tool to use when fetching data from a server.
Let's remove the fetching of data from _main.jsx_. Since we're going to be retrieving the notes from the server, there is no longer a need to pass data as props to the _App_ component. So _main.jsx_ can be simplified to:

```
import ReactDOM from "react-dom/client";
import App from "./App";

ReactDOM.createRoot(document.getElementById("root")).render(<App />);copy
```

The _App_ component changes as follows:

```
import { useState, useEffect } from 'react'import axios from 'axios'import Note from './components/Note'

const App = () => {  const [notes, setNotes] = useState([])  const [newNote, setNewNote] = useState('')
  const [showAll, setShowAll] = useState(true)

  useEffect(() => {    console.log('effect')    axios      .get('http://localhost:3001/notes')      .then(response => {        console.log('promise fulfilled')        setNotes(response.data)      })  }, [])  console.log('render', notes.length, 'notes')
  // ...
}copy
```

We have also added a few helpful prints, which clarify the progression of the execution.
This is printed to the console:

```
render 0 notes
effect
promise fulfilled
render 3 notescopy
```

First, the body of the function defining the component is executed and the component is rendered for the first time. At this point _render 0 notes_ is printed, meaning data hasn't been fetched from the server yet.
The following function, or effect in React parlance:

```
() => {
  console.log('effect')
  axios
    .get('http://localhost:3001/notes')
    .then(response => {
      console.log('promise fulfilled')
      setNotes(response.data)
    })
}copy
```

is executed immediately after rendering. The execution of the function results in _effect_ being printed to the console, and the command _axios.get_ initiates the fetching of data from the server as well as registers the following function as an _event handler_ for the operation:

```
response => {
  console.log('promise fulfilled')
  setNotes(response.data)
})copy
```

When data arrives from the server, the JavaScript runtime calls the function registered as the event handler, which prints _promise fulfilled_ to the console and stores the notes received from the server into the state using the function _setNotes(response.data)_.
As always, a call to a state-updating function triggers the re-rendering of the component. As a result, _render 3 notes_ is printed to the console, and the notes fetched from the server are rendered to the screen.
Finally, let's take a look at the definition of the effect hook as a whole:

```
useEffect(() => {
  console.log('effect')
  axios
    .get('http://localhost:3001/notes').then(response => {
      console.log('promise fulfilled')
      setNotes(response.data)
    })
}, [])copy
```

Let's rewrite the code a bit differently.

```
const hook = () => {
  console.log('effect')
  axios
    .get('http://localhost:3001/notes')
    .then(response => {
      console.log('promise fulfilled')
      setNotes(response.data)
    })
}

useEffect(hook, [])copy
```

Now we can see more clearly that the function _two parameters_. The first is a function, the _effect_ itself. According to the documentation:
> _By default, effects run after every completed render, but you can choose to fire it only when certain values have changed._
So by default, the effect is _always_ run after the component has been rendered. In our case, however, we only want to execute the effect along with the first render.
The second parameter of _useEffect_ is used to _[]_ , then the effect is only run along with the first render of the component.
There are many possible use cases for an effect hook other than fetching data from the server. However, this use is sufficient for us, for now.
Think back to the sequence of events we just discussed. Which parts of the code are run? In what order? How often? Understanding the order of events is critical!
Note that we could have also written the code for the effect function this way:

```
useEffect(() => {
  console.log('effect')

  const eventHandler = response => {
    console.log('promise fulfilled')
    setNotes(response.data)
  }

  const promise = axios.get('http://localhost:3001/notes')
  promise.then(eventHandler)
}, [])copy
```

A reference to an event handler function is assigned to the variable _eventHandler_. The promise returned by the _get_ method of Axios is stored in the variable _promise_. The registration of the callback happens by giving the _eventHandler_ variable, referring to the event-handler function, as an argument to the _then_ method of the promise. It isn't usually necessary to assign functions and promises to variables, and a more compact way of representing things, as seen below, is sufficient.

```
useEffect(() => {
  console.log('effect')
  axios
    .get('http://localhost:3001/notes')
    .then(response => {
      console.log('promise fulfilled')
      setNotes(response.data)
    })
}, [])copy
```

We still have a problem with our application. When adding new notes, they are not stored on the server.
The code for the application, as described so far, can be found in full on _part2-4_.
### The development runtime environment
The configuration for the whole application has steadily grown more complex. Let's review what happens and where. The following image describes the makeup of the application
![diagram of composition of react app](../assets/c6877d57978df9b1.png)
The JavaScript code making up our React application is run in the browser. The browser gets the JavaScript from the _React dev server_ , which is the application that runs after running the command _npm run dev_. The dev-server transforms the JavaScript into a format understood by the browser. Among other things, it stitches together JavaScript from different files into one file. We'll discuss the dev-server in more detail in part 7 of the course.
The React application running in the browser fetches the JSON formatted data from _json-server_ running on port 3001 on the machine. The server we query the data from - _json-server_ - gets its data from the file _db.json_.
At this point in development, all the parts of the application happen to reside on the software developer's machine, otherwise known as localhost. The situation changes when the application is deployed to the internet. We will do this in part 3.
### Exercise 2.11
#### 2.11: The Phonebook Step 6
We continue with developing the phonebook. Store the initial state of the application in the file _db.json_ , which should be placed in the root of the project.

```
{
  "persons":[
    { 
      "name": "Arto Hellas", 
      "number": "040-123456",
      "id": "1"
    },
    { 
      "name": "Ada Lovelace", 
      "number": "39-44-5323523",
      "id": "2"
    },
    { 
      "name": "Dan Abramov", 
      "number": "12-43-234345",
      "id": "3"
    },
    { 
      "name": "Mary Poppendieck", 
      "number": "39-23-6423122",
      "id": "4"
    }
  ]
}copy
```

Start json-server on port 3001 and make sure that the server returns the list of people by going to the address
If you receive the following error message:

```
events.js:182
      throw er; // Unhandled 'error' event
      ^

Error: listen EADDRINUSE 0.0.0.0:3001
    at Object._errnoException (util.js:1019:11)
    at _exceptionWithHostPort (util.js:1041:20)copy
```

it means that port 3001 is already in use by another application, e.g. in use by an already running json-server. Close the other application, or change the port in case that doesn't work.
Modify the application such that the initial state of the data is fetched from the server using the _axios_ -library. Complete the fetching with an
[Part 2b **Previous part**](../part2/01-forms.md)[Part 2d **Next part**](../part2/01-altering-data-in-server.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)
