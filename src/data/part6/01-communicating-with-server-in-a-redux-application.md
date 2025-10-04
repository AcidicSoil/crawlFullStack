---{
  "title": "Communicating with server in a Redux application",
  "source_url": "https://fullstackopen.com/en/part6/communicating_with_server_in_a_redux_application",
  "crawl_timestamp": "2025-10-04T19:16:45Z",
  "checksum": "b0da0c467e79b636a241366a54905ae0f44476f79780f82b8b00098772e503ea"
}
---[Skip to content](../part6/01-communicating-with-server-in-a-redux-application-course-main-content.md)
[{() => fs}](https://fullstackopen.com/en/)
  * [About course](../about/01-about.md)
  * [Course contents](../#course-contents/01-course-contents.md)
  * [FAQ](../faq/01-faq.md)
  * [Partners](../companies/01-companies.md)
  * [Challenge](../challenge/01-challenge.md)
[Search from the material](../search/01-search.md)Toggle dark theme
Select languageSuomi English 中文 Español Français Português(BR) 

[Fullstack](../#course-contents/01-course-contents.md)
[Part 6](../part6/01-part6.md)
Communicating with server in a Redux application
[a Flux-architecture and Redux](../part6/01-flux-architecture-and-redux.md)[b Many reducers](../part6/01-many-reducers.md)
c Communicating with server in a Redux application
  * [Getting data from the backend](../part6/01-communicating-with-server-in-a-redux-application-getting-data-from-the-backend.md)
  * [Sending data to the backend](../part6/01-communicating-with-server-in-a-redux-application-sending-data-to-the-backend.md)
  * [Exercises 6.14.-6.15.](../part6/01-communicating-with-server-in-a-redux-application-exercises-6-14-6-15.md)
  * [Asynchronous actions and Redux Thunk](../part6/01-communicating-with-server-in-a-redux-application-asynchronous-actions-and-redux-thunk.md)
  * [Exercises 6.16.-6.19.](../part6/01-communicating-with-server-in-a-redux-application-exercises-6-16-6-19.md)


[d React Query, useReducer and the context](../part6/01-react-query-use-reducer-and-the-context.md)
c
# Communicating with server in a Redux application
Let's expand the application so that the notes are stored in the backend. We'll use [json-server](../part2/01-getting-data-from-server.md), familiar from part 2.
The initial state of the database is stored in the file _db.json_ , which is placed in the root of the project:
```
{
  "notes": [
    {
      "content": "the app state is in redux store",
      "important": true,
      "id": 1
    },
    {
      "content": "state changes are made with actions",
      "important": false,
      "id": 2
    }
  ]
}copy
```

We'll install json-server for the project:
```
npm install json-server --save-devcopy
```

and add the following line to the _scripts_ part of the file _package.json_
```
"scripts": {
  "server": "json-server -p3001 --watch db.json",
  // ...
}copy
```

Now let's launch json-server with the command _npm run server_.
### Getting data from the backend
Next, we'll create a method into the file _services/notes.js_ , which uses _axios_ to fetch data from the backend
```
import axios from 'axios'

const baseUrl = 'http://localhost:3001/notes'

const getAll = async () => {
  const response = await axios.get(baseUrl)
  return response.data
}

export default { getAll }copy
```

We'll add axios to the project
```
npm install axioscopy
```

We'll change the initialization of the state in _noteReducer_ , so that by default there are no notes:
```
const noteSlice = createSlice({
  name: 'notes',
  initialState: [],  // ...
})copy
```

Let's also add a new action _appendNote_ for adding a note object:
```
const noteSlice = createSlice({
  name: 'notes',
  initialState: [],
  reducers: {
    createNote(state, action) {
      const content = action.payload

      state.push({
        content,
        important: false,
        id: generateId(),
      })
    },
    toggleImportanceOf(state, action) {
      const id = action.payload

      const noteToChange = state.find(n => n.id === id)

      const changedNote = { 
        ...noteToChange, 
        important: !noteToChange.important 
      }

      return state.map(note =>
        note.id !== id ? note : changedNote 
      )     
    },
    appendNote(state, action) {      state.push(action.payload)    }  },
})

export const { createNote, toggleImportanceOf, appendNote } = noteSlice.actions
export default noteSlice.reducercopy
```

A quick way to initialize the notes state based on the data received from the server is to fetch the notes in the _main.jsx_ file and dispatch an action using the _appendNote_ action creator for each individual note object:
```
// ...
import noteService from './services/notes'import noteReducer, { appendNote } from './reducers/noteReducer'
const store = configureStore({
  reducer: {
    notes: noteReducer,
    filter: filterReducer,
  }
})

noteService.getAll().then(notes =>  notes.forEach(note => {    store.dispatch(appendNote(note))  }))
// ...copy
```

Dispatching multiple actions seems a bit impractical. Let's add an action creator _setNotes_ which can be used to directly replace the notes array. We'll get the action creator from the _createSlice_ function by implementing the _setNotes_ action:
```
// ...

const noteSlice = createSlice({
  name: 'notes',
  initialState: [],
  reducers: {
    createNote(state, action) {
      const content = action.payload

      state.push({
        content,
        important: false,
        id: generateId(),
      })
    },
    toggleImportanceOf(state, action) {
      const id = action.payload

      const noteToChange = state.find(n => n.id === id)

      const changedNote = { 
        ...noteToChange, 
        important: !noteToChange.important 
      }

      return state.map(note =>
        note.id !== id ? note : changedNote 
      )     
    },
    appendNote(state, action) {
      state.push(action.payload)
    },
    setNotes(state, action) {      return action.payload    }  },
})

export const { createNote, toggleImportanceOf, appendNote, setNotes } = noteSlice.actions
export default noteSlice.reducercopy
```

Now, the code in the _main.jsx_ file looks a lot better:
```
// ...
import noteService from './services/notes'
import noteReducer, { setNotes } from './reducers/noteReducer'
const store = configureStore({
  reducer: {
    notes: noteReducer,
    filter: filterReducer,
  }
})

noteService.getAll().then(notes =>
  store.dispatch(setNotes(notes)))copy
```

> **NB:** Why didn't we use await in place of promises and event handlers (registered to _then_ -methods)?
> Await only works inside _async_ functions, and the code in _main.jsx_ is not inside a function, so due to the simple nature of the operation, we'll abstain from using _async_ this time.
We do, however, decide to move the initialization of the notes into the _App_ component, and, as usual, when fetching data from a server, we'll use the _effect hook_.
```
import { useEffect } from 'react'import NewNote from './components/NewNote'
import Notes from './components/Notes'
import VisibilityFilter from './components/VisibilityFilter'
import noteService from './services/notes'import { setNotes } from './reducers/noteReducer'import { useDispatch } from 'react-redux'
const App = () => {
  const dispatch = useDispatch()  useEffect(() => {    noteService      .getAll().then(notes => dispatch(setNotes(notes)))  }, [])
  return (
    <div>
      <NewNote />
      <VisibilityFilter />
      <Notes />
    </div>
  )
}

export default Appcopy
```

### Sending data to the backend
We can do the same thing when it comes to creating a new note. Let's expand the code communicating with the server as follows:
```
const baseUrl = 'http://localhost:3001/notes'

const getAll = async () => {
  const response = await axios.get(baseUrl)
  return response.data
}

const createNew = async (content) => {  const object = { content, important: false }  const response = await axios.post(baseUrl, object)  return response.data}
export default {
  getAll,
  createNew,}copy
```

The method _addNote_ of the component _NewNote_ changes slightly:
```
import { useDispatch } from 'react-redux'
import { createNote } from '../reducers/noteReducer'
import noteService from '../services/notes'
const NewNote = (props) => {
  const dispatch = useDispatch()
  
  const addNote = async (event) => {    event.preventDefault()
    const content = event.target.note.value
    event.target.note.value = ''
    const newNote = await noteService.createNew(content)    dispatch(createNote(newNote))  }

  return (
    <form onSubmit={addNote}>
      <input name="note" />
      <button type="submit">add</button>
    </form>
  )
}

export default NewNotecopy
```

Because the backend generates ids for the notes, we'll change the action creator _createNote_ in the file _noteReducer.js_ accordingly:
```
const noteSlice = createSlice({
  name: 'notes',
  initialState: [],
  reducers: {
    createNote(state, action) {
      state.push(action.payload)    },
    // ..
  },
})copy
```

Changing the importance of notes could be implemented using the same principle, by making an asynchronous method call to the server and then dispatching an appropriate action.
The current state of the code for the application can be found on _part6-3_.
### Exercises 6.14.-6.15.
#### 6.14 Anecdotes and the Backend, step 1
When the application launches, fetch the anecdotes from the backend implemented using json-server.
As the initial backend data, you can use, e.g. 
#### 6.15 Anecdotes and the Backend, step 2
Modify the creation of new anecdotes, so that the anecdotes are stored in the backend.
### Asynchronous actions and Redux Thunk
Our approach is quite good, but it is not great that the communication with the server happens inside the functions of the components. It would be better if the communication could be abstracted away from the components so that they don't have to do anything else but call the appropriate _action creator_. As an example, _App_ would initialize the state of the application as follows:
```
const App = () => {
  const dispatch = useDispatch()

  useEffect(() => {
    dispatch(initializeNotes())  
  }, []) 

  // ...
}copy
```

and _NewNote_ would create a new note as follows:
```
const NewNote = () => {
  const dispatch = useDispatch()
  
  const addNote = async (event) => {
    event.preventDefault()
    const content = event.target.note.value
    event.target.note.value = ''
    dispatch(createNote(content))
  }

  // ...
}copy
```

In this implementation, both components would dispatch an action without the need to know about the communication with the server that happens behind the scenes. These kinds of _async actions_ can be implemented using the _configureStore_ function.
With Redux Thunk it is possible to implement _action creators_ which return a function instead of an object. The function receives Redux store's _dispatch_ and _getState_ methods as parameters. This allows for example implementations of asynchronous action creators, which first wait for the completion of a certain asynchronous operation and after that dispatch some action, which changes the store's state.
We can define an action creator _initializeNotes_ which initializes the notes based on the data received from the server:
```
// ...
import noteService from '../services/notes'
const noteSlice = createSlice(/* ... */)

export const { createNote, toggleImportanceOf, setNotes, appendNote } = noteSlice.actions

export const initializeNotes = () => {  return async dispatch => {    const notes = await noteService.getAll()    dispatch(setNotes(notes))  }}
export default noteSlice.reducercopy
```

In the inner function, meaning the _asynchronous action_ , the operation first fetches all the notes from the server and then _dispatches_ the _setNotes_ action, which adds them to the store.
The component _App_ can now be defined as follows:
```
// ...
import { initializeNotes } from './reducers/noteReducer'
const App = () => {
  const dispatch = useDispatch()

  useEffect(() => {    dispatch(initializeNotes())   }, []) 
  return (
    <div>
      <NewNote />
      <VisibilityFilter />
      <Notes />
    </div>
  )
}copy
```

The solution is elegant. The initialization logic for the notes has been completely separated from the React component.
Next, let's replace the _createNote_ action creator created by the _createSlice_ function with an asynchronous action creator:
```
// ...
import noteService from '../services/notes'

const noteSlice = createSlice({
  name: 'notes',
  initialState: [],
  reducers: {
    toggleImportanceOf(state, action) {
      const id = action.payload

      const noteToChange = state.find(n => n.id === id)

      const changedNote = { 
        ...noteToChange, 
        important: !noteToChange.important 
      }

      return state.map(note =>
        note.id !== id ? note : changedNote 
      )     
    },
    appendNote(state, action) {
      state.push(action.payload)
    },
    setNotes(state, action) {
      return action.payload
    }
    // createNote definition removed from here!
  },
})

export const { toggleImportanceOf, appendNote, setNotes } = noteSlice.actions
export const initializeNotes = () => {
  return async dispatch => {
    const notes = await noteService.getAll()
    dispatch(setNotes(notes))
  }
}

export const createNote = content => {  return async dispatch => {    const newNote = await noteService.createNew(content)    dispatch(appendNote(newNote))  }}
export default noteSlice.reducercopy
```

The principle here is the same: first, an asynchronous operation is executed, after which the action changing the state of the store is _dispatched_.
The component _NewNote_ changes as follows:
```
// ...
import { createNote } from '../reducers/noteReducer'
const NewNote = () => {
  const dispatch = useDispatch()
  
  const addNote = async (event) => {
    event.preventDefault()
    const content = event.target.note.value
    event.target.note.value = ''
    dispatch(createNote(content))  }

  return (
    <form onSubmit={addNote}>
      <input name="note" />
      <button type="submit">add</button>
    </form>
  )
}copy
```

Finally, let's clean up the _main.jsx_ file a bit by moving the code related to the creation of the Redux store into its own, _store.js_ file:
```
import { configureStore } from '@reduxjs/toolkit'

import noteReducer from './reducers/noteReducer'
import filterReducer from './reducers/filterReducer'

const store = configureStore({
  reducer: {
    notes: noteReducer,
    filter: filterReducer
  }
})

export default storecopy
```

After the changes, the content of the _main.jsx_ is the following:
```
import React from 'react'
import ReactDOM from 'react-dom/client'
import { Provider } from 'react-redux' 
import store from './store'import App from './App'

ReactDOM.createRoot(document.getElementById('root')).render(
  <Provider store={store}>
    <App />
  </Provider>
)copy
```

The current state of the code for the application can be found on _part6-5_.
Redux Toolkit offers a multitude of tools to simplify asynchronous state management. Suitable tools for this use case are for example the 
### Exercises 6.16.-6.19.
#### 6.16 Anecdotes and the Backend, step 3
Modify the initialization of the Redux store to happen using asynchronous action creators, which are made possible by the Redux Thunk library.
#### 6.17 Anecdotes and the Backend, step 4
Also modify the creation of a new anecdote to happen using asynchronous action creators, made possible by the Redux Thunk library.
#### 6.18 Anecdotes and the Backend, step 5
Voting does not yet save changes to the backend. Fix the situation with the help of the Redux Thunk library.
#### 6.19 Anecdotes and the Backend, step 6
The creation of notifications is still a bit tedious since one has to do two actions and use the _setTimeout_ function:
```
dispatch(setNotification(`new anecdote '${content}'`))
setTimeout(() => {
  dispatch(clearNotification())
}, 5000)copy
```

Make an action creator, which enables one to provide the notification as follows:
```
dispatch(setNotification(`you voted '${anecdote.content}'`, 10))copy
```

The first parameter is the text to be rendered and the second parameter is the time to display the notification given in seconds.
Implement the use of this improved notification in your application.
[ Part 6b **Previous part** ](../part6/01-many-reducers.md)[ Part 6d **Next part** ](../part6/01-react-query-use-reducer-and-the-context.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)