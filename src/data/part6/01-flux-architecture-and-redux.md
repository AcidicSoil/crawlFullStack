---{
  "title": "Flux-architecture and Redux",
  "source_url": "https://fullstackopen.com/en/part6/flux_architecture_and_redux",
  "crawl_timestamp": "2025-10-04T19:16:47Z",
  "checksum": "52d44386bd7fe9c2db21f80699bff58357465e15426426b288a381d52b184481"
}
---[Skip to content](../part6/01-flux-architecture-and-redux-course-main-content.md)
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
Flux-architecture and Redux
a Flux-architecture and Redux
  * [Flux-architecture](../part6/01-flux-architecture-and-redux-flux-architecture.md)
  * [Redux](../part6/01-flux-architecture-and-redux-redux.md)
  * [A note about the use of createStore](../part6/01-flux-architecture-and-redux-a-note-about-the-use-of-create-store.md)
  * [Redux-notes](../part6/01-flux-architecture-and-redux-redux-notes.md)
  * [Pure functions, immutable](../part6/01-flux-architecture-and-redux-pure-functions-immutable.md)
  * [Array spread syntax](../part6/01-flux-architecture-and-redux-array-spread-syntax.md)
  * [Exercises 6.1.-6.2.](../part6/01-flux-architecture-and-redux-exercises-6-1-6-2.md)
  * [Uncontrolled form](../part6/01-flux-architecture-and-redux-uncontrolled-form.md)
  * [Action creators](../part6/01-flux-architecture-and-redux-action-creators.md)
  * [Forwarding Redux Store to various components](../part6/01-flux-architecture-and-redux-forwarding-redux-store-to-various-components.md)
  * [More components](../part6/01-flux-architecture-and-redux-more-components.md)
  * [Exercises 6.3.-6.8.](../part6/01-flux-architecture-and-redux-exercises-6-3-6-8.md)


[b Many reducers](../part6/01-many-reducers.md)[c Communicating with server in a Redux application](../part6/01-communicating-with-server-in-a-redux-application.md)[d React Query, useReducer and the context](../part6/01-react-query-use-reducer-and-the-context.md)
a
# Flux-architecture and Redux
So far, we have followed the state management conventions recommended by React. We have placed the state and the functions for handling it in the 
### Flux-architecture
Already years ago Facebook developed the _stores_. State in the store is not changed directly, but with different _actions_.
When an action changes the state of the store, the views are rerendered:
![diagram action->dispatcher->store->view](../assets/0bb7d27aede4a659.png)
If some action on the application, for example pushing a button, causes the need to change the state, the change is made with an action. This causes re-rendering the view again:
![same diagram as above but with action looping back](../assets/b355a5bd56d17988.png)
Flux offers a standard way for how and where the application's state is kept and how it is modified.
### Redux
Facebook has an implementation for Flux, but we will be using the 
We will get to know Redux by implementing a counter application yet again:
![browser counter application](../assets/e80657c8e8da427e.png)
Create a new Vite application and install redux with the command
```
npm install reduxcopy
```

As in Flux, in Redux the state is also stored in a 
The whole state of the application is stored in _one_ JavaScript object in the store. Because our application only needs the value of the counter, we will save it straight to the store. If the state was more complicated, different things in the state would be saved as separate fields of the object.
The state of the store is changed with _type_ of the action. Our application needs for example the following action:
```
{
  type: 'INCREMENT'
}copy
```

If there is data involved with the action, other fields can be declared as needed. However, our counting app is so simple that the actions are fine with just the type field.
The impact of the action to the state of the application is defined using a _returns_ a new state.
Let's now define a reducer for our application at _main.jsx_. The file initially looks like this:
```
const counterReducer = (state, action) => {
  if (action.type === 'INCREMENT') {
    return state + 1
  } else if (action.type === 'DECREMENT') {
    return state - 1
  } else if (action.type === 'ZERO') {
    return 0
  }

  return state
}copy
```

The first parameter is the _state_ in the store. The reducer returns a _new state_ based on the _action_ type. So, e.g. when the type of Action is _INCREMENT_ , the state gets the old value plus one. If the type of Action is _ZERO_ the new value of state is zero.
Let's change the code a bit. We have used if-else statements to respond to an action and change the state. However, the 
Let's also define a _state_. Now the reducer works even if the store state has not been primed yet.
```
const counterReducer = (state = 0, action) => {  switch (action.type) {
    case 'INCREMENT':
      return state + 1
    case 'DECREMENT':
      return state - 1
    case 'ZERO':
      return 0
    default: // if none of the above matches, code comes here
      return state
  }
}copy
```

The reducer is never supposed to be called directly from the application's code. It is only given as a parameter to the _createStore_ function which creates the store:
```
import { createStore } from 'redux'
const counterReducer = (state = 0, action) => {
  // ...
}

const store = createStore(counterReducer)copy
```

The store now uses the reducer to handle _actions_ , which are _dispatched_ or 'sent' to the store with its 
```
store.dispatch({ type: 'INCREMENT' })copy
```

You can find out the state of the store using the method 
For example the following code:
```
const store = createStore(counterReducer)
console.log(store.getState())
store.dispatch({ type: 'INCREMENT' })
store.dispatch({ type: 'INCREMENT' })
store.dispatch({ type: 'INCREMENT' })
console.log(store.getState())
store.dispatch({ type: 'ZERO' })
store.dispatch({ type: 'DECREMENT' })
console.log(store.getState())copy
```

would print the following to the console
```
0
3
-1copy
```

because at first, the state of the store is 0. After three _INCREMENT_ actions the state is 3. In the end, after the _ZERO_ and _DECREMENT_ actions, the state is -1.
The third important method that the store has is 
If, for example, we would add the following function to subscribe, _every change in the store_ would be printed to the console.
```
store.subscribe(() => {
  const storeNow = store.getState()
  console.log(storeNow)
})copy
```

so the code
```
const store = createStore(counterReducer)

store.subscribe(() => {
  const storeNow = store.getState()
  console.log(storeNow)
})

store.dispatch({ type: 'INCREMENT' })
store.dispatch({ type: 'INCREMENT' })
store.dispatch({ type: 'INCREMENT' })
store.dispatch({ type: 'ZERO' })
store.dispatch({ type: 'DECREMENT' })copy
```

would cause the following to be printed
```
1
2
3
0
-1copy
```

The code of our counter application is the following. All of the code has been written in the same file (_main.jsx_), so _store_ is directly available for the React code. We will get to know better ways to structure React/Redux code later.
```
import React from 'react'
import ReactDOM from 'react-dom/client'

import { createStore } from 'redux'

const counterReducer = (state = 0, action) => {
  switch (action.type) {
    case 'INCREMENT':
      return state + 1
    case 'DECREMENT':
      return state - 1
    case 'ZERO':
      return 0
    default:
      return state
  }
}

const store = createStore(counterReducer)

const App = () => {
  return (
    <div>
      <div>
        {store.getState()}
      </div>
      <button 
        onClick={e => store.dispatch({ type: 'INCREMENT' })}
      >
        plus
      </button>
      <button
        onClick={e => store.dispatch({ type: 'DECREMENT' })}
      >
        minus
      </button>
      <button 
        onClick={e => store.dispatch({ type: 'ZERO' })}
      >
        zero
      </button>
    </div>
  )
}

const root = ReactDOM.createRoot(document.getElementById('root'))

const renderApp = () => {
  root.render(<App />)
}

renderApp()
store.subscribe(renderApp)copy
```

There are a few notable things in the code. _App_ renders the value of the counter by asking it from the store with the method _store.getState()_. The action handlers of the buttons _dispatch_ the right actions to the store.
When the state in the store is changed, React is not able to automatically re-render the application. Thus we have registered a function _renderApp_ , which renders the whole app, to listen for changes in the store with the _store.subscribe_ method. Note that we have to immediately call the _renderApp_ method. Without the call, the first rendering of the app would never happen.
### A note about the use of createStore
The most observant will notice that the name of the function createStore is overlined. If you move the mouse over the name, an explanation will appear
![vscode error showing createStore deprecated, use configureStore instead](../assets/84c532aba5adda47.png)
The full explanation is as follows
> _We recommend using the configureStore method of the @reduxjs/toolkit package, which replaces createStore._
> _Redux Toolkit is our recommended approach for writing Redux logic today, including store setup, reducers, data fetching, and more._
> _For more details, please read this Redux docs page:_
> _configureStore from Redux Toolkit is an improved version of createStore that simplifies setup and helps avoid common bugs._
> _You should not be using the redux core package by itself today, except for learning purposes. The createStore method from the core redux package will not be removed, but we encourage all users to migrate to using Redux Toolkit for all Redux code._
So, instead of the function _createStore_ , it is recommended to use the slightly more "advanced" function _configureStore_ , and we will also use it when we have achieved the basic functionality of Redux.
Side note: _createStore_ is defined as "deprecated", which usually means that the feature will be removed in some newer version of the library. The explanation above and this _createStore_ will not be removed, and it has been given the status _deprecated_ , perhaps with slightly incorrect reasons. So the function is not obsolete, but today there is a more preferable, new way to do almost the same thing.
### Redux-notes
We aim to modify our note application to use Redux for state management. However, let's first cover a few key concepts through a simplified note application.
The first version of our application is the following
```
const noteReducer = (state = [], action) => {
  if (action.type === 'NEW_NOTE') {
    state.push(action.payload)
    return state
  }

  return state
}

const store = createStore(noteReducer)

store.dispatch({
  type: 'NEW_NOTE',
  payload: {
    content: 'the app state is in redux store',
    important: true,
    id: 1
  }
})

store.dispatch({
  type: 'NEW_NOTE',
  payload: {
    content: 'state changes are made with actions',
    important: false,
    id: 2
  }
})

const App = () => {
  return(
    <div>
      <ul>
        {store.getState().map(note=>
          <li key={note.id}>
            {note.content} <strong>{note.important ? 'important' : ''}</strong>
          </li>
        )}
        </ul>
    </div>
  )
}
export default noteReducer;copy
```

So far the application does not have the functionality for adding new notes, although it is possible to do so by dispatching _NEW_NOTE_ actions.
Now the actions have a type and a field _payload_ , which contains the note to be added:
```
{
  type: 'NEW_NOTE',
  payload: {
    content: 'state changes are made with actions',
    important: false,
    id: 2
  }
}copy
```

The choice of the field name is not random. The general convention is that actions have exactly two fields, _type_ telling the type and _payload_ containing the data included with the Action.
### Pure functions, immutable
The initial version of the reducer is very simple:
```
const noteReducer = (state = [], action) => {
  if (action.type === 'NEW_NOTE') {
    state.push(action.payload)
    return state
  }

  return state
}copy
```

The state is now an Array. _NEW_NOTE_ -type actions cause a new note to be added to the state with the 
The application seems to be working, but the reducer we have declared is bad. It breaks the 
Pure functions are such, that they _do not cause any side effects_ and they must always return the same response when called with the same parameters.
We added a new note to the state with the method _state.push(action.payload)_ which _changes_ the state of the state-object. This is not allowed. The problem is easily solved by using the _new array_ , which contains all the elements of the old array and the new element:
```
const noteReducer = (state = [], action) => {
  if (action.type === 'NEW_NOTE') {
    return state.concat(action.payload)  }

  return state
}copy
```

A reducer state must be composed of _replaced with a new, changed, object_. This is exactly what we did with the new reducer: the old array is replaced with the new one.
Let's expand our reducer so that it can handle the change of a note's importance:
```
{
  type: 'TOGGLE_IMPORTANCE',
  payload: {
    id: 2
  }
}copy
```

Since we do not have any code which uses this functionality yet, we are expanding the reducer in the 'test-driven' way. Let's start by creating a test for handling the action _NEW_NOTE_.
We have to first configure the 
```
npm install --save-dev jest @babel/preset-env @babel/preset-react eslint-plugin-jestcopy
```

Next we'll create the file _.babelrc_ , with the following content:
```
{
  "presets": [
    "@babel/preset-env",
    ["@babel/preset-react", { "runtime": "automatic" }]
  ]
}copy
```

Let us expand _package.json_ with a script for running the tests:
```
{
  // ...
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "lint": "eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview",
    "test": "jest"  },
  // ...
}copy
```

And finally, _.eslintrc.cjs_ needs to be altered as follows:
```
module.exports = {
  root: true,
  env: { 
    browser: true,
    es2020: true,
    "jest/globals": true  },
  // ...
}copy
```

To make testing easier, we'll first move the reducer's code to its own module, to the file _src/reducers/noteReducer.js_. We'll also add the library 
```
npm install --save-dev deep-freezecopy
```

The test, which we define in file _src/reducers/noteReducer.test.js_ , has the following content:
```
import noteReducer from './noteReducer'
import deepFreeze from 'deep-freeze'

describe('noteReducer', () => {
  test('returns new state with action NEW_NOTE', () => {
    const state = []
    const action = {
      type: 'NEW_NOTE',
      payload: {
        content: 'the app state is in redux store',
        important: true,
        id: 1
      }
    }

    deepFreeze(state)
    const newState = noteReducer(state, action)

    expect(newState).toHaveLength(1)
    expect(newState).toContainEqual(action.payload)
  })
})copy
```

Run the test with _npm test_. The _deepFreeze(state)_ command ensures that the reducer does not change the state of the store given to it as a parameter. If the reducer uses the _push_ command to manipulate the state, the test will not pass
![terminal showing test failure and error about not using array.push](../assets/68035f97f82a2896.png)
Now we'll create a test for the _TOGGLE_IMPORTANCE_ action:
```
test('returns new state with action TOGGLE_IMPORTANCE', () => {
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
    type: 'TOGGLE_IMPORTANCE',
    payload: {
      id: 2
    }
  }

  deepFreeze(state)
  const newState = noteReducer(state, action)

  expect(newState).toHaveLength(2)

  expect(newState).toContainEqual(state[0])

  expect(newState).toContainEqual({
    content: 'state changes are made with actions',
    important: true,
    id: 2
  })
})copy
```

So the following action
```
{
  type: 'TOGGLE_IMPORTANCE',
  payload: {
    id: 2
  }
}copy
```

has to change the importance of the note with the id 2.
The reducer is expanded as follows
```
const noteReducer = (state = [], action) => {
  switch(action.type) {
    case 'NEW_NOTE':
      return state.concat(action.payload)
    case 'TOGGLE_IMPORTANCE': {
      const id = action.payload.id
      const noteToChange = state.find(n => n.id === id)
      const changedNote = { 
        ...noteToChange, 
        important: !noteToChange.important 
      }
      return state.map(note =>
        note.id !== id ? note : changedNote 
      )
     }
    default:
      return state
  }
}copy
```

We create a copy of the note whose importance has changed with the syntax [familiar from part 2](../part2/01-altering-data-in-server-changing-the-importance-of-notes.md), and replace the state with a new state containing all the notes which have not changed and the copy of the changed note _changedNote_.
Let's recap what goes on in the code. First, we search for a specific note object, the importance of which we want to change:
```
const noteToChange = state.find(n => n.id === id)copy
```

then we create a new object, which is a _copy_ of the original note, only the value of the _important_ field has been changed to the opposite of what it was:
```
const changedNote = { 
  ...noteToChange, 
  important: !noteToChange.important 
}copy
```

A new state is then returned. We create it by taking all of the notes from the old state except for the desired note, which we replace with its slightly altered copy:
```
state.map(note =>
  note.id !== id ? note : changedNote 
)copy
```

### Array spread syntax
Because we now have quite good tests for the reducer, we can refactor the code safely.
Adding a new note creates the state returned from the Array's _concat_ function. Let's take a look at how we can achieve the same by using the JavaScript 
```
const noteReducer = (state = [], action) => {
  switch(action.type) {
    case 'NEW_NOTE':
      return [...state, action.payload]    case 'TOGGLE_IMPORTANCE':
      // ...
    default:
    return state
  }
}copy
```

The spread -syntax works as follows. If we declare
```
const numbers = [1, 2, 3]copy
```

`...numbers` breaks the array up into individual elements, which can be placed in another array.
```
[...numbers, 4, 5]copy
```

and the result is an array _[1, 2, 3, 4, 5]_.
If we would have placed the array to another array without the spread
```
[numbers, 4, 5]copy
```

the result would have been _[ [1, 2, 3], 4, 5]_.
When we take elements from an array by _gather_ the rest of the elements:
```
const numbers = [1, 2, 3, 4, 5, 6]

const [first, second, ...rest] = numbers

console.log(first)     // prints 1
console.log(second)   // prints 2
console.log(rest)     // prints [3, 4, 5, 6]copy
```

### Exercises 6.1.-6.2.
Let's make a simplified version of the unicafe exercise from part 1. Let's handle the state management with Redux.
You can take the code from this repository 
_Start by removing the git configuration of the cloned repository, and by installing dependencies_
```
cd unicafe-redux   // go to the directory of cloned repository
rm -rf .git
npm installcopy
```

#### 6.1: Unicafe Revisited, step 1
Before implementing the functionality of the UI, let's implement the functionality required by the store.
We have to save the number of each kind of feedback to the store, so the form of the state in the store is:
```
{
  good: 5,
  ok: 4,
  bad: 2
}copy
```

The project has the following base for a reducer:
```
const initialState = {
  good: 0,
  ok: 0,
  bad: 0
}

const counterReducer = (state = initialState, action) => {
  console.log(action)
  switch (action.type) {
    case 'GOOD':
      return state
    case 'OK':
      return state
    case 'BAD':
      return state
    case 'ZERO':
      return state
    default: return state
  }

}

export default counterReducercopy
```

and a base for its tests
```
import deepFreeze from 'deep-freeze'
import counterReducer from './reducer'

describe('unicafe reducer', () => {
  const initialState = {
    good: 0,
    ok: 0,
    bad: 0
  }

  test('should return a proper initial state when called with undefined state', () => {
    const state = {}
    const action = {
      type: 'DO_NOTHING'
    }

    const newState = counterReducer(undefined, action)
    expect(newState).toEqual(initialState)
  })

  test('good is incremented', () => {
    const action = {
      type: 'GOOD'
    }
    const state = initialState

    deepFreeze(state)
    const newState = counterReducer(state, action)
    expect(newState).toEqual({
      good: 1,
      ok: 0,
      bad: 0
    })
  })
})copy
```

**Implement the reducer and its tests.**
In the tests, make sure that the reducer is an _immutable function_ with the _deep-freeze_ library. Ensure that the provided first test passes, because Redux expects that the reducer returns the original state when it is called with a first parameter - which represents the previous _state_ - with the value _undefined_.
Start by expanding the reducer so that both tests pass. Then add the rest of the tests, and finally the functionality that they are testing.
A good model for the reducer is the [redux-notes](../part6/01-flux-architecture-and-redux-pure-functions-immutable.md) example above.
#### 6.2: Unicafe Revisited, step2
Now implement the actual functionality of the application.
Your application can have a modest appearance, nothing else is needed but buttons and the number of reviews for each type:
![browser showing good bad ok buttons](../assets/568e984dbcc82c0b.png)
### Uncontrolled form
Let's add the functionality for adding new notes and changing their importance:
```
const generateId = () =>  Number((Math.random() * 1000000).toFixed(0))
const App = () => {
  const addNote = (event) => {    event.preventDefault()    const content = event.target.note.value    event.target.note.value = ''    store.dispatch({      type: 'NEW_NOTE',      payload: {        content,        important: false,        id: generateId()      }    })  }
  const toggleImportance = (id) => {    store.dispatch({      type: 'TOGGLE_IMPORTANCE',      payload: { id }    })  }
  return (
    <div>
      <form onSubmit={addNote}>        <input name="note" />         <button type="submit">add</button>      </form>      <ul>
        {store.getState().map(note =>
          <li
            key={note.id} 
            onClick={() => toggleImportance(note.id)}          >
            {note.content} <strong>{note.important ? 'important' : ''}</strong>
          </li>
        )}
      </ul>
    </div>
  )
}copy
```

The implementation of both functionalities is straightforward. It is noteworthy that we _have not_ bound the state of the form fields to the state of the _App_ component like we have previously done. React calls this kind of form 
> Uncontrolled forms have certain limitations (for example, dynamic error messages or disabling the submit button based on input are not possible). However they are suitable for our current needs.
You can read more about uncontrolled forms 
The method for adding new notes is simple, it just dispatches the action for adding notes:
```
addNote = (event) => {
  event.preventDefault()
  const content = event.target.note.value  event.target.note.value = ''
  store.dispatch({
    type: 'NEW_NOTE',
    payload: {
      content,
      important: false,
      id: generateId()
    }
  })
}copy
```

We can get the content of the new note straight from the form field. Because the field has a name, we can access the content via the event object _event.target.note.value_. 
```
<form onSubmit={addNote}>
  <input name="note" />  <button type="submit">add</button>
</form>copy
```

A note's importance can be changed by clicking its name. The event handler is very simple:
```
toggleImportance = (id) => {
  store.dispatch({
    type: 'TOGGLE_IMPORTANCE',
    payload: { id }
  })
}copy
```

### Action creators
We begin to notice that, even in applications as simple as ours, using Redux can simplify the frontend code. However, we can do a lot better.
React components don't need to know the Redux action types and forms. Let's separate creating actions into separate functions:
```
const createNote = (content) => {
  return {
    type: 'NEW_NOTE',
    payload: {
      content,
      important: false,
      id: generateId()
    }
  }
}

const toggleImportanceOf = (id) => {
  return {
    type: 'TOGGLE_IMPORTANCE',
    payload: { id }
  }
}copy
```

Functions that create actions are called 
The _App_ component does not have to know anything about the inner representation of the actions anymore, it just gets the right action by calling the creator function:
```
const App = () => {
  const addNote = (event) => {
    event.preventDefault()
    const content = event.target.note.value
    event.target.note.value = ''
    store.dispatch(createNote(content))    
  }
  
  const toggleImportance = (id) => {
    store.dispatch(toggleImportanceOf(id))  }

  // ...
}copy
```

### Forwarding Redux Store to various components
Aside from the reducer, our application is in one file. This is of course not sensible, and we should separate _App_ into its module.
Now the question is, how can the _App_ access the store after the move? And more broadly, when a component is composed of many smaller components, there must be a way for all of the components to access the store. There are multiple ways to share the Redux store with the components. First, we will look into the newest, and possibly the easiest way, which is using the 
First, we install react-redux
```
npm install react-reduxcopy
```

Next, we move the _App_ component into its own file _App.jsx_. Let's see how this affects the rest of the application files.
_main.jsx_ becomes:
```
import React from 'react'
import ReactDOM from 'react-dom/client'
import { createStore } from 'redux'
import { Provider } from 'react-redux'
import App from './App'
import noteReducer from './reducers/noteReducer'

const store = createStore(noteReducer)

ReactDOM.createRoot(document.getElementById('root')).render(
  <Provider store={store}>    <App />
  </Provider>)copy
```

Note, that the application is now defined as a child of a _store_.
Defining the action creators has been moved to the file _reducers/noteReducer.js_ where the reducer is defined. That file looks like this:
```
const noteReducer = (state = [], action) => {
  // ...
}

const generateId = () =>
  Number((Math.random() * 1000000).toFixed(0))

export const createNote = (content) => {  return {
    type: 'NEW_NOTE',
    payload: {
      content,
      important: false,
      id: generateId()
    }
  }
}

export const toggleImportanceOf = (id) => {  return {
    type: 'TOGGLE_IMPORTANCE',
    payload: { id }
  }
}

export default noteReducercopy
```

Previously, if the application had many components which needed the store, the _App_ component had to pass _store_ as props to all of those components (known as prop drilling). Now with the _store_ Provider wrapping the _App_ component, the _store_ is directly accessible to all components within the _App_ component without explicitly being passed as props.
The module now has multiple 
The reducer function is still returned with the _export default_ command, so the reducer can be imported the usual way:
```
import noteReducer from './reducers/noteReducer'copy
```

A module can have only _one default export_ , but multiple "normal" exports
```
export const createNote = (content) => {
  // ...
}

export const toggleImportanceOf = (id) => { 
  // ...
}copy
```

Normally (not as defaults) exported functions can be imported with the curly brace syntax:
```
import { createNote } from '../../reducers/noteReducer'copy
```

Code for the _App_ component
```
import { createNote, toggleImportanceOf } from './reducers/noteReducer'import { useSelector, useDispatch } from 'react-redux'
const App = () => {
  const dispatch = useDispatch()  const notes = useSelector(state => state)
  const addNote = (event) => {
    event.preventDefault()
    const content = event.target.note.value
    event.target.note.value = ''
    dispatch(createNote(content))  }

  const toggleImportance = (id) => {
    dispatch(toggleImportanceOf(id))  }

  return (
    <div>
      <form onSubmit={addNote}>
        <input name="note" /> 
        <button type="submit">add</button>
      </form>
      <ul>
        {notes.map(note =>          <li
            key={note.id} 
            onClick={() => toggleImportance(note.id)}
          >
            {note.content} <strong>{note.important ? 'important' : ''}</strong>
          </li>
        )}
      </ul>
    </div>
  )
}

export default Appcopy
```

There are a few things to note in the code. Previously the code dispatched actions by calling the dispatch method of the Redux store:
```
store.dispatch({
  type: 'TOGGLE_IMPORTANCE',
  payload: { id }
})copy
```

Now it does it with the _dispatch_ function from the 
```
import { useSelector, useDispatch } from 'react-redux'
const App = () => {
  const dispatch = useDispatch()  // ...

  const toggleImportance = (id) => {
    dispatch(toggleImportanceOf(id))  }

  // ...
}copy
```

The _useDispatch_ hook provides any React component access to the dispatch function of the Redux store defined in _main.jsx_. This allows all components to make changes to the state of the Redux store.
The component can access the notes stored in the store with the 
```
import { useSelector, useDispatch } from 'react-redux'
const App = () => {
  // ...
  const notes = useSelector(state => state)  // ...
}copy
```

_useSelector_ receives a function as a parameter. The function either searches for or selects data from the Redux store. Here we need all of the notes, so our selector function returns the whole state:
```
state => statecopy
```

which is a shorthand for:
```
(state) => {
  return state
}copy
```

Usually, selector functions are a bit more interesting and return only selected parts of the contents of the Redux store. We could for example return only notes marked as important:
```
const importantNotes = useSelector(state => state.filter(note => note.important))  copy
```

The current version of the application can be found on _part6-0_.
### More components
Let's separate creating a new note into a component.
```
import { useDispatch } from 'react-redux'import { createNote } from '../reducers/noteReducer'
const NewNote = () => {
  const dispatch = useDispatch()
  const addNote = (event) => {
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
}

export default NewNotecopy
```

Unlike in the React code we did without Redux, the event handler for changing the state of the app (which now lives in Redux) has been moved away from the _App_ to a child component. The logic for changing the state in Redux is still neatly separated from the whole React part of the application.
We'll also separate the list of notes and displaying a single note into their own components (which will both be placed in the _Notes.jsx_ file ):
```
import { useDispatch, useSelector } from 'react-redux'import { toggleImportanceOf } from '../reducers/noteReducer'
const Note = ({ note, handleClick }) => {
  return(
    <li onClick={handleClick}>
      {note.content} 
      <strong> {note.important ? 'important' : ''}</strong>
    </li>
  )
}

const Notes = () => {
  const dispatch = useDispatch()  const notes = useSelector(state => state)
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
}

export default Notescopy
```

The logic for changing the importance of a note is now in the component managing the list of notes.
There is not much code left in _App_ :
```
const App = () => {

  return (
    <div>
      <NewNote />
      <Notes />
    </div>
  )
}copy
```

_Note_ , responsible for rendering a single note, is very simple and is not aware that the event handler it gets as props dispatches an action. These kinds of components are called 
_Notes_ , on the other hand, is a _Note_ components do and coordinates the configuration of _presentational_ components, that is, the _Note_ s.
The code of the Redux application can be found on _part6-1_.
### Exercises 6.3.-6.8.
Let's make a new version of the anecdote voting application from part 1. Take the project from this repository 
If you clone the project into an existing git repository, _remove the git configuration of the cloned application:_
```
cd redux-anecdotes  // go to the cloned repository
rm -rf .gitcopy
```

The application can be started as usual, but you have to install the dependencies first:
```
npm install
npm run devcopy
```

After completing these exercises, your application should look like this:
![browser showing anecdotes and vote buttons](../assets/97fd505f54423cb1.png)
#### 6.3: Anecdotes, step 1
Implement the functionality for voting anecdotes. The number of votes must be saved to a Redux store.
#### 6.4: Anecdotes, step 2
Implement the functionality for adding new anecdotes.
You can keep the form uncontrolled like we did [earlier](../part6/01-flux-architecture-and-redux-uncontrolled-form.md).
#### 6.5: Anecdotes, step 3
Make sure that the anecdotes are ordered by the number of votes.
#### 6.6: Anecdotes, step 4
If you haven't done so already, separate the creation of action-objects to _src/reducers/anecdoteReducer.js_ file, so do what we have been doing since the chapter [action creators](../part6/01-flux-architecture-and-redux-action-creators.md).
#### 6.7: Anecdotes, step 5
Separate the creation of new anecdotes into a component called _AnecdoteForm_. Move all logic for creating a new anecdote into this new component.
#### 6.8: Anecdotes, step 6
Separate the rendering of the anecdote list into a component called _AnecdoteList_. Move all logic related to voting for an anecdote to this new component.
Now the _App_ component should look like this:
```
import AnecdoteForm from './components/AnecdoteForm'
import AnecdoteList from './components/AnecdoteList'

const App = () => {
  return (
    <div>
      <h2>Anecdotes</h2>
      <AnecdoteList />
      <AnecdoteForm />
    </div>
  )
}

export default Appcopy
```

[ Part 5 **Previous part** ](../part5/01-part5.md)[ Part 6b **Next part** ](../part6/01-many-reducers.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)