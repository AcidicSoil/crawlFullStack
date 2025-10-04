---{
  "title": "Many reducers",
  "source_url": "https://fullstackopen.com/en/part6/many_reducers",
  "crawl_timestamp": "2025-10-04T19:16:50Z",
  "checksum": "c9dfcd71d625a10cf46e232d769029f826512045e2b083b503bec08779f048e8"
}
---[Skip to content](../part6/01-many-reducers-course-main-content.md)
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
Many reducers
[a Flux-architecture and Redux](../part6/01-flux-architecture-and-redux.md)
b Many reducers
  * [Store with complex state](../part6/01-many-reducers-store-with-complex-state.md)
  * [Combined reducers](../part6/01-many-reducers-combined-reducers.md)
  * [Finishing the filters](../part6/01-many-reducers-finishing-the-filters.md)
  * [Exercise 6.9](../part6/01-many-reducers-exercise-6-9.md)
  * [Redux Toolkit](../part6/01-many-reducers-redux-toolkit.md)
  * [Redux Toolkit and console.log](../part6/01-many-reducers-redux-toolkit-and-console-log.md)
  * [Redux DevTools](../part6/01-many-reducers-redux-dev-tools.md)
  * [Exercises 6.10.-6.13.](../part6/01-many-reducers-exercises-6-10-6-13.md)


[c Communicating with server in a Redux application](../part6/01-communicating-with-server-in-a-redux-application.md)[d React Query, useReducer and the context](../part6/01-react-query-use-reducer-and-the-context.md)
b
# Many reducers
Let's continue our work with the simplified [Redux version](../part6/01-flux-architecture-and-redux-redux-notes.md) of our notes application.
To ease our development, let's change our reducer so that the store gets initialized with a state that contains a couple of notes:
```
const initialState = [
  {
    content: 'reducer defines how redux store works',
    important: true,
    id: 1,
  },
  {
    content: 'state of store can contain any data',
    important: false,
    id: 2,
  },
]

const noteReducer = (state = initialState, action) => {
  // ...
}

// ...
export default noteReducercopy
```

### Store with complex state
Let's implement filtering for the notes that are displayed to the user. The user interface for the filters will be implemented with 
![browser with important/not radio buttons and list](../assets/bb3eca31d384fb34.png)
Let's start with a very simple and straightforward implementation:
```
import NewNote from './components/NewNote'
import Notes from './components/Notes'

const App = () => {
  const filterSelected = (value) => {    console.log(value)  }
  return (
    <div>
      <NewNote />
      <div>        all          <input type="radio" name="filter"          onChange={() => filterSelected('ALL')} />        important    <input type="radio" name="filter"          onChange={() => filterSelected('IMPORTANT')} />        nonimportant <input type="radio" name="filter"          onChange={() => filterSelected('NONIMPORTANT')} />      </div>      <Notes />
    </div>
  )
}copy
```

Since the _name_ attribute of all the radio buttons is the same, they form a _button group_ where only one option can be selected.
The buttons have a change handler that currently only prints the string associated with the clicked button to the console.
In the following section, we will implement filtering by storing both the notes as well as _the value of the filter_ in the redux store. When we are finished, we would like the state of the store to look like this:
```
{
  notes: [
    { content: 'reducer defines how redux store works', important: true, id: 1},
    { content: 'state of store can contain any data', important: false, id: 2}
  ],
  filter: 'IMPORTANT'
}copy
```

Only the array of notes was stored in the state of the previous implementation of our application. In the new implementation, the state object has two properties, _notes_ that contains the array of notes and _filter_ that contains a string indicating which notes should be displayed to the user.
### Combined reducers
We could modify our current reducer to deal with the new shape of the state. However, a better solution in this situation is to define a new separate reducer for the state of the filter:
```
const filterReducer = (state = 'ALL', action) => {
  switch (action.type) {
    case 'SET_FILTER':
      return action.payload
    default:
      return state
  }
}copy
```

The actions for changing the state of the filter look like this:
```
{
  type: 'SET_FILTER',
  payload: 'IMPORTANT'
}copy
```

Let's also create a new _action creator_ function. We will write its code in a new _src/reducers/filterReducer.js_ module:
```
const filterReducer = (state = 'ALL', action) => {
  // ...
}

export const filterChange = filter => {
  return {
    type: 'SET_FILTER',
    payload: filter,
  }
}

export default filterReducercopy
```

We can create the actual reducer for our application by combining the two existing reducers with the 
Let's define the combined reducer in the _main.jsx_ file:
```
import ReactDOM from 'react-dom/client'
import { createStore, combineReducers } from 'redux'import { Provider } from 'react-redux' 
import App from './App'

import noteReducer from './reducers/noteReducer'
import filterReducer from './reducers/filterReducer'
const reducer = combineReducers({  notes: noteReducer,  filter: filterReducer})
const store = createStore(reducer)
console.log(store.getState())

/*
ReactDOM.createRoot(document.getElementById('root')).render(
  <Provider store={store}>
    <App />
  </Provider>
)*/

ReactDOM.createRoot(document.getElementById('root')).render(
  <Provider store={store}>
    <div />
  </Provider>
)copy
```

Since our application breaks completely at this point, we render an empty _div_ element instead of the _App_ component.
The state of the store gets printed to the console:
![devtools console showing notes array data](../assets/acafe8967880a390.png)
As we can see from the output, the store has the exact shape we wanted it to!
Let's take a closer look at how the combined reducer is created:
```
const reducer = combineReducers({
  notes: noteReducer,
  filter: filterReducer,
})copy
```

The state of the store defined by the reducer above is an object with two properties: _notes_ and _filter_. The value of the _notes_ property is defined by the _noteReducer_ , which does not have to deal with the other properties of the state. Likewise, the _filter_ property is managed by the _filterReducer_.
Before we make more changes to the code, let's take a look at how different actions change the state of the store defined by the combined reducer. Let's add the following to the _main.jsx_ file:
```
import { createNote } from './reducers/noteReducer'
import { filterChange } from './reducers/filterReducer'
//...
store.subscribe(() => console.log(store.getState()))
store.dispatch(filterChange('IMPORTANT'))
store.dispatch(createNote('combineReducers forms one reducer from many simple reducers'))copy
```

By simulating the creation of a note and changing the state of the filter in this fashion, the state of the store gets logged to the console after every change that is made to the store:
![devtools console output showing notes filter and new note](../assets/8f0fc3e36ead4e8d.png)
At this point, it is good to become aware of a tiny but important detail. If we add a console log statement _to the beginning of both reducers_ :
```
const filterReducer = (state = 'ALL', action) => {
  console.log('ACTION: ', action)
  // ...
}copy
```

Based on the console output one might get the impression that every action gets duplicated:
![devtools console output showing duplicated actions in note and filter reducers](../assets/4fb20c6cbf22bbba.png)
Is there a bug in our code? No. The combined reducer works in such a way that every _action_ gets handled in _every_ part of the combined reducer, or in other words, every reducer "listens" to all of the dispatched actions and does something with them if it has been instructed to do so. Typically only one reducer is interested in any given action, but there are situations where multiple reducers change their respective parts of the state based on the same action.
### Finishing the filters
Let's finish the application so that it uses the combined reducer. We start by changing the rendering of the application and hooking up the store to the application in the _main.jsx_ file:
```
ReactDOM.createRoot(document.getElementById('root')).render(
  <Provider store={store}>
    <App />
  </Provider>
)copy
```

Next, let's fix a bug that is caused by the code expecting the application store to be an array of notes:
![browser TypeError: notes.map is not a function](../assets/898ff5385a2c674a.png)
It's an easy fix. Because the notes are in the store's field _notes_ , we only have to make a little change to the selector function:
```
const Notes = () => {
  const dispatch = useDispatch()
  const notes = useSelector(state => state.notes)
  return(
    <ul>
      {notes.map(note =>
        <Note
          key={note.id}
          note={note}
          handleClick={() => 
            dispatch(toggleImportanceOf(note.id))
          }
        />
      )}
    </ul>
  )
}copy
```

Previously the selector function returned the whole state of the store:
```
const notes = useSelector(state => state)copy
```

And now it returns only its field _notes_
```
const notes = useSelector(state => state.notes)copy
```

Let's extract the visibility filter into its own _src/components/VisibilityFilter.jsx_ component:
```
import { filterChange } from '../reducers/filterReducer'
import { useDispatch } from 'react-redux'

const VisibilityFilter = (props) => {
  const dispatch = useDispatch()

  return (
    <div>
      all    
      <input 
        type="radio" 
        name="filter" 
        onChange={() => dispatch(filterChange('ALL'))}
      />
      important   
      <input
        type="radio"
        name="filter"
        onChange={() => dispatch(filterChange('IMPORTANT'))}
      />
      nonimportant 
      <input
        type="radio"
        name="filter"
        onChange={() => dispatch(filterChange('NONIMPORTANT'))}
      />
    </div>
  )
}

export default VisibilityFiltercopy
```

With the new component, _App_ can be simplified as follows:
```
import Notes from './components/Notes'
import NewNote from './components/NewNote'
import VisibilityFilter from './components/VisibilityFilter'

const App = () => {
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

The implementation is rather straightforward. Clicking the different radio buttons changes the state of the store's _filter_ property.
Let's change the _Notes_ component to incorporate the filter:
```
const Notes = () => {
  const dispatch = useDispatch()
  const notes = useSelector(state => {    if ( state.filter === 'ALL' ) {      return state.notes    }    return state.filter  === 'IMPORTANT'       ? state.notes.filter(note => note.important)      : state.notes.filter(note => !note.important)  })
  return(
    <ul>
      {notes.map(note =>
        <Note
          key={note.id}
          note={note}
          handleClick={() => 
            dispatch(toggleImportanceOf(note.id))
          }
        />
      )}
    </ul>
  )
}copy
```

We only make changes to the selector function, which used to be
```
useSelector(state => state.notes)copy
```

Let's simplify the selector by destructuring the fields from the state it receives as a parameter:
```
const notes = useSelector(({ filter, notes }) => {
  if ( filter === 'ALL' ) {
    return notes
  }
  return filter  === 'IMPORTANT' 
    ? notes.filter(note => note.important)
    : notes.filter(note => !note.important)
})copy
```

There is a slight cosmetic flaw in our application. Even though the filter is set to _ALL_ by default, the associated radio button is not selected. Naturally, this issue can be fixed, but since this is an unpleasant but ultimately harmless bug we will save the fix for later.
The current version of the application can be found on _part6-2_.
### Exercise 6.9
#### 6.9 Better Anecdotes, step 7
Implement filtering for the anecdotes that are displayed to the user.
![browser showing filtering of anecdotes](../assets/27788cd9dd389b36.png)
Store the state of the filter in the redux store. It is recommended to create a new reducer, action creators, and a combined reducer for the store using the _combineReducers_ function.
Create a new _Filter_ component for displaying the filter. You can use the following code as a template for the component:
```
const Filter = () => {
  const handleChange = (event) => {
    // input-field value is in variable event.target.value
  }
  const style = {
    marginBottom: 10
  }

  return (
    <div style={style}>
      filter <input onChange={handleChange} />
    </div>
  )
}

export default Filtercopy
```

### Redux Toolkit
As we have seen so far, Redux's configuration and state management implementation requires quite a lot of effort. This is manifested for example in the reducer and action creator-related code which has somewhat repetitive boilerplate code. 
Let's start using Redux Toolkit in our application by refactoring the existing code. First, we will need to install the library:
```
npm install @reduxjs/toolkitcopy
```

Next, open the _main.jsx_ file which currently creates the Redux store. Instead of Redux's _createStore_ function, let's create the store using Redux Toolkit's 
```
import ReactDOM from 'react-dom/client'
import { Provider } from 'react-redux'
import { configureStore } from '@reduxjs/toolkit'import App from './App'

import noteReducer from './reducers/noteReducer'
import filterReducer from './reducers/filterReducer'

const store = configureStore({  reducer: {    notes: noteReducer,    filter: filterReducer  }})
console.log(store.getState())

ReactDOM.createRoot(document.getElementById('root')).render(
  <Provider store={store}>
    <App />
  </Provider>
)copy
```

We already got rid of a few lines of code, now we don't need the _combineReducers_ function to create the store's reducer. We will soon see that the _configureStore_ function has many additional benefits such as the effortless integration of development tools and many commonly used libraries without the need for additional configuration.
Let's move on to refactoring the reducers, which brings forth the benefits of the Redux Toolkit. With Redux Toolkit, we can easily create reducer and related action creators using the _createSlice_ function to refactor the reducer and action creators in the _reducers/noteReducer.js_ file in the following manner:
```
import { createSlice } from '@reduxjs/toolkit'
const initialState = [
  {
    content: 'reducer defines how redux store works',
    important: true,
    id: 1,
  },
  {
    content: 'state of store can contain any data',
    important: false,
    id: 2,
  },
]

const generateId = () =>
  Number((Math.random() * 1000000).toFixed(0))

const noteSlice = createSlice({  name: 'notes',  initialState,  reducers: {    createNote(state, action) {      const content = action.payload      state.push({        content,        important: false,        id: generateId(),      })    },    toggleImportanceOf(state, action) {      const id = action.payload      const noteToChange = state.find(n => n.id === id)      const changedNote = {         ...noteToChange,         important: !noteToChange.important       }      return state.map(note =>        note.id !== id ? note : changedNote       )         }  },})export const {createNote,toggleImportanceOf} = noteSlice.actionsexport default noteSlice.reducercopy
```

The _createSlice_ function's _name_ parameter defines the prefix which is used in the action's type values. For example, the _createNote_ action defined later will have the type value of _notes/createNote_. It is a good practice to give the parameter a value which is unique among the reducers. This way there won't be unexpected collisions between the application's action type values. The _initialState_ parameter defines the reducer's initial state. The _reducers_ parameter takes the reducer itself as an object, of which functions handle state changes caused by certain actions. Note that the _action.payload_ in the function contains the argument provided by calling the action creator:
```
dispatch(createNote('Redux Toolkit is awesome!'))copy
```

This dispatch call is equivalent to dispatching the following object:
```
dispatch({ type: 'notes/createNote', payload: 'Redux Toolkit is awesome!' })copy
```

If you followed closely, you might have noticed that inside the _createNote_ action, there seems to happen something that violates the reducers' immutability principle mentioned earlier:
```
createNote(state, action) {
  const content = action.payload

  state.push({
    content,
    important: false,
    id: generateId(),
  })
}copy
```

We are mutating _state_ argument's array by calling the _push_ method instead of returning a new instance of the array. What's this all about?
Redux Toolkit utilizes the _createSlice_ function, which makes it possible to mutate the _state_ argument inside the reducer. Immer uses the mutated state to produce a new, immutable state and thus the state changes remain immutable. Note that _state_ can be changed without "mutating" it, as we have done with the _toggleImportanceOf_ action. In this case, the function directly _returns_ the new state. Nevertheless mutating the state will often come in handy especially when a complex state needs to be updated.
The _createSlice_ function returns an object containing the reducer as well as the action creators defined by the _reducers_ parameter. The reducer can be accessed by the _noteSlice.reducer_ property, whereas the action creators by the _noteSlice.actions_ property. We can produce the file's exports in the following way:
```
const noteSlice = createSlice(/* ... */)

export const { createNote, toggleImportanceOf } = noteSlice.actionsexport default noteSlice.reducercopy
```

The imports in other files will work just as they did before:
```
import noteReducer, { createNote, toggleImportanceOf } from './reducers/noteReducer'copy
```

We need to alter the action type names in the tests due to the conventions of ReduxToolkit:
```
import noteReducer from './noteReducer'
import deepFreeze from 'deep-freeze'

describe('noteReducer', () => {
  test('returns new state with action notes/createNote', () => {
    const state = []
    const action = {
      type: 'notes/createNote',      payload: 'the app state is in redux store',    }

    deepFreeze(state)
    const newState = noteReducer(state, action)

    expect(newState).toHaveLength(1)
    expect(newState.map(s => s.content)).toContainEqual(action.payload)  })

  test('returns new state with action notes/toggleImportanceOf', () => {
    const state = [
      {
        content: 'the app state is in redux store',
        important: true,
        id: 1
      },
      {
        content: 'state changes are made with actions',
        important: false,
        id: 2
      }]
  
    const action = {
      type: 'notes/toggleImportanceOf',      payload: 2    }
  
    deepFreeze(state)
    const newState = noteReducer(state, action)
  
    expect(newState).toHaveLength(2)
  
    expect(newState).toContainEqual(state[0])
  
    expect(newState).toContainEqual({
      content: 'state changes are made with actions',
      important: true,
      id: 2
    })
  })
})copy
```

### Redux Toolkit and console.log
As we have learned, console.log is an extremely powerful tool; it often saves us from trouble.
Let's try to print the state of the Redux Store to the console in the middle of the reducer created with the function createSlice:
```
const noteSlice = createSlice({
  name: 'notes',
  initialState,
  reducers: {
    // ...
    toggleImportanceOf(state, action) {
      const id = action.payload

      const noteToChange = state.find(n => n.id === id)

      const changedNote = { 
        ...noteToChange, 
        important: !noteToChange.important 
      }

      console.log(state)
      return state.map(note =>
        note.id !== id ? note : changedNote 
      )     
    }
  },
})copy
```

The following is printed to the console
![devtools console showing Handler,Target as null but IsRevoked as true](../assets/5f37df31b19f3a3b.png)
The output is interesting but not very useful. This is about the previously mentioned Immer library used by the Redux Toolkit internally to save the state of the Store.
The status can be converted to a human-readable format by using the 
Let's update the imports to include the "current" function from the immer library:
```
import { createSlice, current } from '@reduxjs/toolkit'copy
```

Then we update the console.log function call:
```
console.log(current(state))copy
```

Console output is now human readable
![dev tools showing array of 2 notes](../assets/22c74d8401ffae5f.png)
### Redux DevTools
_configureStore_ function, no additional configuration is needed for Redux DevTools to work.
Once the addon is installed, clicking the _Redux_ tab in the browser's developer tools, the Redux DevTools should open:
![browser with redux addon in devtools](../assets/8a3c1fd408d53beb.png)
You can inspect how dispatching a certain action changes the state by clicking the action:
![devtools inspecting state tree in redux](../assets/d417498832b45387.png)
It is also possible to dispatch actions to the store using the development tools:
![devtools redux dispatching createNote with payload](../assets/511044087a85c8f5.png)
You can find the code for our current application in its entirety in the _part6-3_ branch of 
### Exercises 6.10.-6.13.
Let's continue working on the anecdote application using Redux that we started in exercise 6.3.
#### 6.10 Better Anecdotes, step 8
Install Redux Toolkit for the project. Move the Redux store creation into the file _store.js_ and use Redux Toolkit's _configureStore_ to create the store.
Change the definition of the _filter reducer and action creators_ to use the Redux Toolkit's _createSlice_ function.
Also, start using Redux DevTools to debug the application's state easier.
#### 6.11 Better Anecdotes, step 9
Change also the definition of the _anecdote reducer and action creators_ to use the Redux Toolkit's _createSlice_ function.
Implementation note: when you use the Redux Toolkit to return the initial state of anecdotes, it will be immutable, so you will need to make a copy of it to sort the anecdotes, or you will encounter the error "TypeError: Cannot assign to read only property". You can use the spread syntax to make a copy of the array. Instead of:
```
anecdotes.sort()copy
```

Write:
```
[...anecdotes].sort()copy
```

#### 6.12 Better Anecdotes, step 10
The application has a ready-made body for the _Notification_ component:
```
const Notification = () => {
  const style = {
    border: 'solid',
    padding: 10,
    borderWidth: 1
  }
  return (
    <div style={style}>
      render here notification...
    </div>
  )
}

export default Notificationcopy
```

Extend the component so that it renders the message stored in the Redux store, making the component take the following form:
```
import { useSelector } from 'react-redux'
const Notification = () => {
  const notification = useSelector(/* something here */)  const style = {
    border: 'solid',
    padding: 10,
    borderWidth: 1
  }
  return (
    <div style={style}>
      {notification}    </div>
  )
}copy
```

You will have to make changes to the application's existing reducer. Create a separate reducer for the new functionality by using the Redux Toolkit's _createSlice_ function.
The application does not have to use the _Notification_ component intelligently at this point in the exercises. It is enough for the application to display the initial value set for the message in the _notificationReducer_.
#### 6.13 Better Anecdotes, step 11
Extend the application so that it uses the _Notification_ component to display a message for five seconds when the user votes for an anecdote or creates a new anecdote:
![browser showing message of having voted](../assets/77d5cf9e5462c0e1.png)
It's recommended to create separate 
[ Part 6a **Previous part** ](../part6/01-flux-architecture-and-redux.md)[ Part 6c **Next part** ](../part6/01-communicating-with-server-in-a-redux-application.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)