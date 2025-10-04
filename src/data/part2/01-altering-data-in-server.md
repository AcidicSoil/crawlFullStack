---{
  "title": "Altering data in server",
  "source_url": "https://fullstackopen.com/en/part2/altering_data_in_server",
  "crawl_timestamp": "2025-10-04T19:16:08Z",
  "checksum": "b4d4d2f8d9ea6df110d7be6f919dc6f70944ff91ecf2255553204f696b37ea16"
}
---[Skip to content](../part2/01-altering-data-in-server-course-main-content.md)
[{() => fs}](https://fullstackopen.com/en/)
  * [About course](../about/01-about.md)
  * [Course contents](../#course-contents/01-course-contents.md)
  * [FAQ](../faq/01-faq.md)
  * [Partners](../companies/01-companies.md)
  * [Challenge](../challenge/01-challenge.md)
[Search from the material](../search/01-search.md)Toggle dark theme
Select languageSuomi English 中文 Español Français Português(BR) 

[Fullstack](../#course-contents/01-course-contents.md)
[Part 2](../part2/01-part2.md)
Altering data in server
[a Rendering a collection, modules](../part2/01-rendering-a-collection-modules.md)[b Forms](../part2/01-forms.md)[c Getting data from server](../part2/01-getting-data-from-server.md)
d Altering data in server
  * [REST](../part2/01-altering-data-in-server-rest.md)
  * [Sending Data to the Server](../part2/01-altering-data-in-server-sending-data-to-the-server.md)
  * [Changing the Importance of Notes](../part2/01-altering-data-in-server-changing-the-importance-of-notes.md)
  * [Extracting Communication with the Backend into a Separate Module](../part2/01-altering-data-in-server-extracting-communication-with-the-backend-into-a-separate-module.md)
  * [Cleaner Syntax for Defining Object Literals](../part2/01-altering-data-in-server-cleaner-syntax-for-defining-object-literals.md)
  * [Promises and Errors](../part2/01-altering-data-in-server-promises-and-errors.md)
  * [Full stack developer's oath](../part2/01-altering-data-in-server-full-stack-developers-oath.md)
  * [Exercises 2.12.-2.15.](../part2/01-altering-data-in-server-exercises-2-12-2-15.md)


[e Adding styles to React app](../part2/01-adding-styles-to-react-app.md)
d
# Altering data in server
When creating notes in our application, we would naturally want to store them in some backend server. The 
> _Get a full fake REST API with zero coding in less than 30 seconds (seriously)_
The json-server does not exactly match the description provided by the textbook 
We will take a closer look at REST in the [next part](../part3/01-part3.md) of the course. But it's important to familiarize ourselves at this point with some of the 
### REST
In REST terminology, we refer to individual data objects, such as the notes in our application, as _resources_. Every resource has a unique address associated with it - its URL. According to a general convention used by json-server, we would be able to locate an individual note at the resource URL _notes/3_ , where 3 is the id of the resource. The _notes_ URL, on the other hand, would point to a resource collection containing all the notes.
Resources are fetched from the server with HTTP GET requests. For instance, an HTTP GET request to the URL _notes/3_ will return the note that has the id number 3. An HTTP GET request to the _notes_ URL would return a list of all notes.
Creating a new resource for storing a note is done by making an HTTP POST request to the _notes_ URL according to the REST convention that the json-server adheres to. The data for the new note resource is sent in the _body_ of the request.
json-server requires all data to be sent in JSON format. What this means in practice is that the data must be a correctly formatted string and that the request must contain the _Content-Type_ request header with the value _application/json_.
### Sending Data to the Server
Let's make the following changes to the event handler responsible for creating a new note:
```
const addNote = event => {
  event.preventDefault()
  const noteObject = {
    content: newNote,
    important: Math.random() < 0.5,
  }

  axios    .post('http://localhost:3001/notes', noteObject)    .then(response => {      console.log(response)    })}copy
```

We create a new object for the note but omit the _id_ property since it's better to let the server generate ids for our resources.
The object is sent to the server using the axios _post_ method. The registered event handler logs the response that is sent back from the server to the console.
When we try to create a new note, the following output pops up in the console:
![data json output in console](../assets/d0d628dfe547e528.png)
The newly created note resource is stored in the value of the _data_ property of the _response_ object.
Quite often it is useful to inspect HTTP requests in the _Network_ tab of Chrome developer tools, which was used heavily at the beginning of [part 0](../part0/01-fundamentals-of-web-apps-http-get.md).
We can use the inspector to check that the headers sent in the POST request are what we expected them to be:
![dev tools header shows 201 created for localhost:3001/notes](../assets/5062c160ed772225.png)
Since the data we sent in the POST request was a JavaScript object, axios automatically knew to set the appropriate _application/json_ value for the _Content-Type_ header.
The tab _payload_ can be used to check the request data:
![devtools payload tab shows content and important fields from above](../assets/f0eb234eb167eabf.png)
Also the tab _response_ is useful, it shows what was the data the server responded with:
![devtools response tab shows same content as payload but with id field too](../assets/efc8edcde75c8975.png)
The new note is not rendered to the screen yet. This is because we did not update the state of the _App_ component when we created it. Let's fix this:
```
const addNote = event => {
  event.preventDefault()
  const noteObject = {
    content: newNote,
    important: Math.random() > 0.5,
  }

  axios
    .post('http://localhost:3001/notes', noteObject)
    .then(response => {
      setNotes(notes.concat(response.data))      setNewNote('')    })
}copy
```

The new note returned by the backend server is added to the list of notes in our application's state in the customary way of using the _setNotes_ function and then resetting the note creation form. An [important detail](../part1/01-a-more-complex-state-debugging-react-apps-handling-arrays.md) to remember is that the _concat_ method does not change the component's original state, but instead creates a new copy of the list.
Once the data returned by the server starts to have an effect on the behavior of our web applications, we are immediately faced with a whole new set of challenges arising from, for instance, the asynchronicity of communication. This necessitates new debugging strategies, console logging and other means of debugging become increasingly more important. We must also develop a sufficient understanding of the principles of both the JavaScript runtime and React components. Guessing won't be enough.
It's beneficial to inspect the state of the backend server, e.g. through the browser:
![JSON data output from backend](../assets/12c4425ee33113e3.png)
This makes it possible to verify that all the data we intended to send was actually received by the server.
In the next part of the course, we will learn to implement our own logic in the backend. We will then take a closer look at tools like 
The code for the current state of our application can be found in the _part2-5_ branch on 
### Changing the Importance of Notes
Let's add a button to every note that can be used for toggling its importance.
We make the following changes to the _Note_ component:
```
const Note = ({ note, toggleImportance }) => {
  const label = note.important
    ? 'make not important' : 'make important'

  return (
    <li>
      {note.content} 
      <button onClick={toggleImportance}>{label}</button>
    </li>
  )
}copy
```

We add a button to the component and assign its event handler as the _toggleImportance_ function passed in the component's props.
The _App_ component defines an initial version of the _toggleImportanceOf_ event handler function and passes it to every _Note_ component:
```
const App = () => {
  const [notes, setNotes] = useState([]) 
  const [newNote, setNewNote] = useState('')
  const [showAll, setShowAll] = useState(true)

  // ...

  const toggleImportanceOf = (id) => {    console.log('importance of ' + id + ' needs to be toggled')  }
  // ...

  return (
    <div>
      <h1>Notes</h1>
      <div>
        <button onClick={() => setShowAll(!showAll)}>
          show {showAll ? 'important' : 'all' }
        </button>
      </div>      
      <ul>
        {notesToShow.map(note => 
          <Note
            key={note.id}
            note={note} 
            toggleImportance={() => toggleImportanceOf(note.id)}          />
        )}
      </ul>
      // ...
    </div>
  )
}copy
```

Notice how every note receives its own _unique_ event handler function since the _id_ of every note is unique.
E.g., if _note.id_ is 3, the event handler function returned by _toggleImportance(note.id)_ will be:
```
() => { console.log('importance of 3 needs to be toggled') }copy
```

A short reminder here. The string printed by the event handler is defined in a Java-like manner by adding the strings:
```
console.log('importance of ' + id + ' needs to be toggled')copy
```

The 
```
console.log(`importance of ${id} needs to be toggled`)copy
```

We can now use the "dollar-bracket"-syntax to add parts to the string that will evaluate JavaScript expressions, e.g. the value of a variable. Note that we use backticks in template strings instead of quotation marks used in regular JavaScript strings.
Individual notes stored in the json-server backend can be modified in two different ways by making HTTP requests to the note's unique URL. We can either _replace_ the entire note with an HTTP PUT request or only change some of the note's properties with an HTTP PATCH request.
The final form of the event handler function is the following:
```
const toggleImportanceOf = id => {
  const url = `http://localhost:3001/notes/${id}`
  const note = notes.find(n => n.id === id)
  const changedNote = { ...note, important: !note.important }

  axios.put(url, changedNote).then(response => {
    setNotes(notes.map(note => note.id === id ? response.data : note))
  })
}copy
```

Almost every line of code in the function body contains important details. The first line defines the unique URL for each note resource based on its id.
The array _note_ variable.
After this, we create a _new object_ that is an exact copy of the old note, apart from the important property that has the value flipped (from true to false or from false to true).
The code for creating the new object that uses the 
```
const changedNote = { ...note, important: !note.important }copy
```

In practice, _{ ...note }_ creates a new object with copies of all the properties from the _note_ object. When we add properties inside the curly braces after the spread object, e.g. _{ ...note, important: true }_ , then the value of the _important_ property of the new object will be _true_. In our example, the _important_ property gets the negation of its previous value in the original object.
There are a few things to point out. Why did we make a copy of the note object we wanted to modify when the following code also appears to work?
```
const note = notes.find(n => n.id === id)
note.important = !note.important

axios.put(url, note).then(response => {
  // ...copy
```

This is not recommended because the variable _note_ is a reference to an item in the _notes_ array in the component's state, and as we recall we must 
It's also worth noting that the new object _changedNote_ is only a so-called 
The new note is then sent with a PUT request to the backend where it will replace the old object.
The callback function sets the component's _notes_ state to a new array that contains all the items from the previous _notes_ array, except for the old note which is replaced by the updated version of it returned by the server:
```
axios.put(url, changedNote).then(response => {
  setNotes(notes.map(note => note.id === id ? response.data : note))
})copy
```

This is accomplished with the _map_ method:
```
notes.map(note => note.id === id ? response.data : note)copy
```

The map method creates a new array by mapping every item from the old array into an item in the new array. In our example, the new array is created conditionally so that if _note.id === id_ is true; the note object returned by the server is added to the array. If the condition is false, then we simply copy the item from the old array into the new array instead.
This _map_ trick may seem a bit strange at first, but it's worth spending some time wrapping your head around it. We will be using this method many times throughout the course.
### Extracting Communication with the Backend into a Separate Module
The _App_ component has become somewhat bloated after adding the code for communicating with the backend server. In the spirit of the [module](../part2/01-rendering-a-collection-modules-refactoring-modules.md).
Let's create a _src/services_ directory and add a file there called _notes.js_ :
```
import axios from 'axios'
const baseUrl = 'http://localhost:3001/notes'

const getAll = () => {
  return axios.get(baseUrl)
}

const create = newObject => {
  return axios.post(baseUrl, newObject)
}

const update = (id, newObject) => {
  return axios.put(`${baseUrl}/${id}`, newObject)
}

export default { 
  getAll: getAll, 
  create: create, 
  update: update 
}copy
```

The module returns an object that has three functions (_getAll_ , _create_ , and _update_) as its properties that deal with notes. The functions directly return the promises returned by the axios methods.
The _App_ component uses _import_ to get access to the module:
```
import noteService from './services/notes'
const App = () => {copy
```

The functions of the module can be used directly with the imported variable _noteService_ as follows:
```
const App = () => {
  // ...

  useEffect(() => {
    noteService      .getAll()      .then(response => {        setNotes(response.data)      })  }, [])

  const toggleImportanceOf = id => {
    const note = notes.find(n => n.id === id)
    const changedNote = { ...note, important: !note.important }

    noteService      .update(id, changedNote)      .then(response => {        setNotes(notes.map(note => note.id === id ? response.data : note))      })  }

  const addNote = (event) => {
    event.preventDefault()
    const noteObject = {
      content: newNote,
      important: Math.random() > 0.5
    }

    noteService      .create(noteObject)      .then(response => {        setNotes(notes.concat(response.data))        setNewNote('')      })  }

  // ...
}

export default Appcopy
```

We could take our implementation a step further. When the _App_ component uses the functions, it receives an object that contains the entire response for the HTTP request:
```
noteService
  .getAll()
  .then(response => {
    setNotes(response.data)
  })copy
```

The _App_ component only uses the _response.data_ property of the response object.
The module would be much nicer to use if, instead of the entire HTTP response, we would only get the response data. Using the module would then look like this:
```
noteService
  .getAll()
  .then(initialNotes => {
    setNotes(initialNotes)
  })copy
```

We can achieve this by changing the code in the module as follows (the current code contains some copy-paste, but we will tolerate that for now):
```
import axios from 'axios'
const baseUrl = 'http://localhost:3001/notes'

const getAll = () => {
  const request = axios.get(baseUrl)
  return request.then(response => response.data)
}

const create = newObject => {
  const request = axios.post(baseUrl, newObject)
  return request.then(response => response.data)
}

const update = (id, newObject) => {
  const request = axios.put(`${baseUrl}/${id}`, newObject)
  return request.then(response => response.data)
}

export default { 
  getAll: getAll, 
  create: create, 
  update: update 
}copy
```

We no longer return the promise returned by axios directly. Instead, we assign the promise to the _request_ variable and call its _then_ method:
```
const getAll = () => {
  const request = axios.get(baseUrl)
  return request.then(response => response.data)
}copy
```

The last row in our function is simply a more compact expression of the same code as shown below:
```
const getAll = () => {
  const request = axios.get(baseUrl)
  return request.then(response => {    return response.data  })}copy
```

The modified _getAll_ function still returns a promise, as the _then_ method of a promise also 
After defining the parameter of the _then_ method to directly return _response.data_ , we have gotten the _getAll_ function to work like we wanted it to. When the HTTP request is successful, the promise returns the data sent back in the response from the backend.
We have to update the _App_ component to work with the changes made to our module. We have to fix the callback functions given as parameters to the _noteService_ object's methods so that they use the directly returned response data:
```
const App = () => {
  // ...

  useEffect(() => {
    noteService
      .getAll()
      .then(initialNotes => {        setNotes(initialNotes)      })
  }, [])

  const toggleImportanceOf = id => {
    const note = notes.find(n => n.id === id)
    const changedNote = { ...note, important: !note.important }

    noteService
      .update(id, changedNote)
      .then(returnedNote => {        setNotes(notes.map(note => note.id === id ? returnedNote : note))      })
  }

  const addNote = (event) => {
    event.preventDefault()
    const noteObject = {
      content: newNote,
      important: Math.random() > 0.5
    }

    noteService
      .create(noteObject)
      .then(returnedNote => {        setNotes(notes.concat(returnedNote))        setNewNote('')
      })
  }

  // ...
}copy
```

This is all quite complicated and attempting to explain it may just make it harder to understand. The internet is full of material discussing the topic, such as 
The "Async and performance" book from the 
Promises are central to modern JavaScript development and it is highly recommended to invest a reasonable amount of time into understanding them.
### Cleaner Syntax for Defining Object Literals
The module defining note-related services currently exports an object with the properties _getAll_ , _create_ , and _update_ that are assigned to functions for handling notes.
The module definition was:
```
import axios from 'axios'
const baseUrl = 'http://localhost:3001/notes'

const getAll = () => {
  const request = axios.get(baseUrl)
  return request.then(response => response.data)
}

const create = newObject => {
  const request = axios.post(baseUrl, newObject)
  return request.then(response => response.data)
}

const update = (id, newObject) => {
  const request = axios.put(`${baseUrl}/${id}`, newObject)
  return request.then(response => response.data)
}

export default { 
  getAll: getAll, 
  create: create, 
  update: update 
}copy
```

The module exports the following, rather peculiar looking, object:
```
{ 
  getAll: getAll, 
  create: create, 
  update: update 
}copy
```

The labels to the left of the colon in the object definition are the _keys_ of the object, whereas the ones to the right of it are _variables_ that are defined inside the module.
Since the names of the keys and the assigned variables are the same, we can write the object definition with a more compact syntax:
```
{ 
  getAll, 
  create, 
  update 
}copy
```

As a result, the module definition gets simplified into the following form:
```
import axios from 'axios'
const baseUrl = 'http://localhost:3001/notes'

const getAll = () => {
  const request = axios.get(baseUrl)
  return request.then(response => response.data)
}

const create = newObject => {
  const request = axios.post(baseUrl, newObject)
  return request.then(response => response.data)
}

const update = (id, newObject) => {
  const request = axios.put(`${baseUrl}/${id}`, newObject)
  return request.then(response => response.data)
}

export default { getAll, create, update }copy
```

In defining the object using this shorter notation, we make use of a 
To demonstrate this feature, let's consider a situation where we have the following values assigned to variables:
```
const name = 'Leevi'
const age = 0copy
```

In older versions of JavaScript we had to define an object like this:
```
const person = {
  name: name,
  age: age
}copy
```

However, since both the property fields and the variable names in the object are the same, it's enough to simply write the following in ES6 JavaScript:
```
const person = { name, age }copy
```

The result is identical for both expressions. They both create an object with a _name_ property with the value _Leevi_ and an _age_ property with the value _0_.
### Promises and Errors
If our application allowed users to delete notes, we could end up in a situation where a user tries to change the importance of a note that has already been deleted from the system.
Let's simulate this situation by making the _getAll_ function of the note service return a "hardcoded" note that does not actually exist on the backend server:
```
const getAll = () => {
  const request = axios.get(baseUrl)
  const nonExisting = {
    id: 10000,
    content: 'This note is not saved to server',
    important: true,
  }
  return request.then(response => response.data.concat(nonExisting))
}copy
```

When we try to change the importance of the hardcoded note, we see the following error message in the console. The error says that the backend server responded to our HTTP PUT request with a status code 404 _not found_.
![404 not found error in dev tools](../assets/3ea8aa9a4558bd74.png)
The application should be able to handle these types of error situations gracefully. Users won't be able to tell that an error has occurred unless they happen to have their console open. The only way the error can be seen in the application is that clicking the button does not affect the note's importance.
We had [previously](../part2/01-getting-data-from-server-axios-and-promises.md) mentioned that a promise can be in one of three different states. When an axios HTTP request fails, the associated promise is _rejected_. Our current code does not handle this rejection in any way.
The rejection of a promise is _then_ method with a second callback function, which is called in the situation where the promise is rejected.
The more common way of adding a handler for rejected promises is to use the 
In practice, the error handler for rejected promises is defined like this:
```
axios
  .get('http://example.com/probably_will_fail')
  .then(response => {
    console.log('success!')
  })
  .catch(error => {
    console.log('fail')
  })copy
```

If the request fails, the event handler registered with the _catch_ method gets called.
The _catch_ method is often utilized by placing it deeper within the promise chain.
When multiple _.then_ methods are chained together, we are in fact creating a 
```
axios
  .get('http://...')
  .then(response => response.data)
  .then(data => {
    // ...
  })copy
```

The _catch_ method can be used to define a handler function at the end of a promise chain, which is called once any promise in the chain throws an error and the promise becomes _rejected_.
```
axios
  .get('http://...')
  .then(response => response.data)
  .then(data => {
    // ...
  })
  .catch(error => {
    console.log('fail')
  })copy
```

Let's take advantage of this feature. We will place our application's error handler in the _App_ component:
```
const toggleImportanceOf = id => {
  const note = notes.find(n => n.id === id)
  const changedNote = { ...note, important: !note.important }

  noteService
    .update(id, changedNote).then(returnedNote => {
      setNotes(notes.map(note => note.id === id ? returnedNote : note))
    })
    .catch(error => {      alert(        `the note '${note.content}' was already deleted from server`      )      setNotes(notes.filter(n => n.id !== id))    })}copy
```

The error message is displayed to the user with the trusty old 
Removing an already deleted note from the application's state is done with the array 
```
notes.filter(n => n.id !== id)copy
```

It's probably not a good idea to use alert in more serious React applications. We will soon learn a more advanced way of displaying messages and notifications to users. There are situations, however, where a simple, battle-tested method like _alert_ can function as a starting point. A more advanced method could always be added in later, given that there's time and energy for it.
The code for the current state of our application can be found in the _part2-6_ branch on 
### Full stack developer's oath
It is again time for the exercises. The complexity of our app is now increasing since besides just taking care of the React components in the frontend, we also have a backend that is persisting the application data.
To cope with the increasing complexity we should extend the web developer's oath to a _Full stack developer's oath_ , which reminds us to make sure that the communication between frontend and backend happens as expected.
So here is the updated oath:
Full stack development is _extremely hard_ , that is why I will use all the possible means to make it easier
  * I will have my browser developer console open all the time
  * _I will use the network tab of the browser dev tools to ensure that frontend and backend are communicating as I expect_
  * _I will constantly keep an eye on the state of the server to make sure that the data sent there by the frontend is saved there as I expect_
  * I will progress with small steps
  * I will write lots of _console.log_ statements to make sure I understand how the code behaves and to help pinpoint problems
  * If my code does not work, I will not write more code. Instead, I start deleting the code until it works or just return to a state when everything was still working
  * When I ask for help in the course Discord channel or elsewhere I formulate my questions properly, see [here](../part0/01-general-info-how-to-get-help-in-discord.md) how to ask for help


### Exercises 2.12.-2.15.
#### 2.12: The Phonebook step 7
Let's return to our phonebook application.
Currently, the numbers that are added to the phonebook are not saved to a backend server. Fix this situation.
#### 2.13: The Phonebook step 8
Extract the code that handles the communication with the backend into its own module by following the example shown earlier in this part of the course material.
#### 2.14: The Phonebook step 9
Make it possible for users to delete entries from the phonebook. The deletion can be done through a dedicated button for each person in the phonebook list. You can confirm the action from the user by using the 
![2.17 window confirm feature screeshot](../assets/55f986fade124d77.png)
The associated resource for a person in the backend can be deleted by making an HTTP DELETE request to the resource's URL. If we are deleting e.g. a person who has the _id_ 2, we would have to make an HTTP DELETE request to the URL _localhost:3001/persons/2_. No data is sent with the request.
You can make an HTTP DELETE request with the 
**NB:** You can't use the name _delete_ for a variable because it's a reserved word in JavaScript. E.g. the following is not possible:
```
// use some other name for variable!
const delete = (id) => {
  // ...
}copy
```

#### 2.15*: The Phonebook step 10
_Why is there an asterisk in the exercise? See[here](../part0/01-general-info-taking-the-course.md) for the explanation._
Change the functionality so that if a number is added to an already existing user, the new number will replace the old number. It's recommended to use the HTTP PUT method for updating the phone number.
If the person's information is already in the phonebook, the application can ask the user to confirm the action:
![2.18 screenshot alert confirmation](../assets/4dd0224e4b3b3eb5.png)
[ Part 2c **Previous part** ](../part2/01-getting-data-from-server.md)[ Part 2e **Next part** ](../part2/01-adding-styles-to-react-app.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)