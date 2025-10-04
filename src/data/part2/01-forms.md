---{
  "title": "Forms",
  "source_url": "https://fullstackopen.com/en/part2/forms",
  "crawl_timestamp": "2025-10-04T19:16:11Z",
  "checksum": "42b43a5150f732fe7e703eee1e067a93f6614146077a0bcbc063c55b8dd9e12a"
}
---[Skip to content](../part2/01-forms-course-main-content.md)
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
Forms
[a Rendering a collection, modules](../part2/01-rendering-a-collection-modules.md)
b Forms

- [Saving the notes in the component state](../part2/01-forms-saving-the-notes-in-the-component-state.md)
- [Controlled component](../part2/01-forms-controlled-component.md)
- [Filtering Displayed Elements](../part2/01-forms-filtering-displayed-elements.md)
- [Exercises 2.6.-2.10.](../part2/01-forms-exercises-2-6-2-10.md)


[c Getting data from server](../part2/01-getting-data-from-server.md)[d Altering data in server](../part2/01-altering-data-in-server.md)[e Adding styles to React app](../part2/01-adding-styles-to-react-app.md)
b
# Forms
Let's continue expanding our application by allowing users to add new notes. You can find the code for our current application
### Saving the notes in the component state
To get our page to update when new notes are added it's best to store the notes in the _App_ component's state. Let's import the

```
import { useState } from 'react'import Note from './components/Note'

const App = (props) => {  const [notes, setNotes] = useState(props.notes)
  return (
    <div>
      <h1>Notes</h1>
      <ul>
        {notes.map(note => 
          <Note key={note.id} note={note} />
        )}
      </ul>
    </div>
  )
}

export default App copy
```

The component uses the _useState_ function to initialize the piece of state stored in _notes_ with the array of notes passed in the props:

```
const App = (props) => { 
  const [notes, setNotes] = useState(props.notes) 

  // ...
}copy
```

We can also use React Developer Tools to see that this really happens:
![browser showing dev react tools window](../assets/7b2d7cd27deb036e.png)
If we wanted to start with an empty list of notes, we would set the initial value as an empty array, and since the props would not be used, we could omit the _props_ parameter from the function definition:

```
const App = () => { 
  const [notes, setNotes] = useState([]) 

  // ...
}  copy
```

Let's stick with the initial value passed in the props for the time being.
Next, let's add an HTML

```
const App = (props) => {
  const [notes, setNotes] = useState(props.notes)

  const addNote = (event) => {    event.preventDefault()    console.log('button clicked', event.target)  }
  return (
    <div>
      <h1>Notes</h1>
      <ul>
        {notes.map(note => 
          <Note key={note.id} note={note} />
        )}
      </ul>
      <form onSubmit={addNote}>        <input />        <button type="submit">save</button>      </form>       </div>
  )
}copy
```

We have added the _addNote_ function as an event handler to the form element that will be called when the form is submitted, by clicking the submit button.
We use the method discussed in [part 1](../part1/01-component-state-event-handlers-event-handling.md) for defining our event handler:

```
const addNote = (event) => {
  event.preventDefault()
  console.log('button clicked', event.target)
}copy
```

The _event_ parameter is the
The event handler immediately calls the _event.preventDefault()_ method, which prevents the default action of submitting a form. The default action would,
The target of the event stored in _event.target_ is logged to the console:
![button clicked with form object console](../assets/7b9becd58f122b52.png)
The target in this case is the form that we have defined in our component.
How do we access the data contained in the form's _input_ element?
### Controlled component
There are many ways to accomplish this; the first method we will take a look at is through the use of so-called
Let's add a new piece of state called _newNote_ for storing the user-submitted input **and** let's set it as the _input_ element's _value_ attribute:

```
const App = (props) => {
  const [notes, setNotes] = useState(props.notes)
  const [newNote, setNewNote] = useState(    'a new note...'  ) 
  const addNote = (event) => {
    event.preventDefault()
    console.log('button clicked', event.target)
  }

  return (
    <div>
      <h1>Notes</h1>
      <ul>
        {notes.map(note => 
          <Note key={note.id} note={note} />
        )}
      </ul>
      <form onSubmit={addNote}>
        <input value={newNote} />        <button type="submit">save</button>
      </form>   
    </div>
  )
}copy
```

The placeholder text stored as the initial value of the _newNote_ state appears in the _input_ element, but the input text can't be edited. The console displays a warning that gives us a clue as to what might be wrong:
![provided value to prop without onchange console error](../assets/63a7d84891bc2126.png)
Since we assigned a piece of the _App_ component's state as the _value_ attribute of the input element, the _App_ component now
To enable editing of the input element, we have to register an _event handler_ that synchronizes the changes made to the input with the component's state:

```
const App = (props) => {
  const [notes, setNotes] = useState(props.notes)
  const [newNote, setNewNote] = useState(
    'a new note...'
  ) 

  // ...

  const handleNoteChange = (event) => {    console.log(event.target.value)    setNewNote(event.target.value)  }
  return (
    <div>
      <h1>Notes</h1>
      <ul>
        {notes.map(note => 
          <Note key={note.id} note={note} />
        )}
      </ul>
      <form onSubmit={addNote}>
        <input
          value={newNote}
          onChange={handleNoteChange}        />
        <button type="submit">save</button>
      </form>   
    </div>
  )
}copy
```

We have now registered an event handler to the _onChange_ attribute of the form's _input_ element:

```
<input
  value={newNote}
  onChange={handleNoteChange}
/>copy
```

The event handler is called every time _a change occurs in the input element_. The event handler function receives the event object as its _event_ parameter:

```
const handleNoteChange = (event) => {
  console.log(event.target.value)
  setNewNote(event.target.value)
}copy
```

The _target_ property of the event object now corresponds to the controlled _input_ element, and _event.target.value_ refers to the input value of that element.
Note that we did not need to call the _event.preventDefault()_ method like we did in the _onSubmit_ event handler. This is because no default action occurs on an input change, unlike a form submission.
You can follow along in the console to see how the event handler is called:
![multiple console calls with typing text](../assets/c910659212567520.png)
You did remember to install
![state changes in react devtools shows typing too](../assets/f1d567fee5734304.png)
Now the _App_ component's _newNote_ state reflects the current value of the input, which means that we can complete the _addNote_ function for creating new notes:

```
const addNote = (event) => {
  event.preventDefault()
  const noteObject = {
    content: newNote,
    important: Math.random() < 0.5,
    id: String(notes.length + 1),
  }

  setNotes(notes.concat(noteObject))
  setNewNote('')
}copy
```

First, we create a new object for the note called _noteObject_ that will receive its content from the component's _newNote_ state. The unique identifier _id_ is generated based on the total number of notes. This method works for our application since notes are never deleted. With the help of the _Math.random()_ function, our note has a 50% chance of being marked as important.
The new note is added to the list of notes using the [part 1](../part1/01-java-script-arrays.md):

```
setNotes(notes.concat(noteObject))copy
```

The method does not mutate the original _notes_ array, but rather creates _a new copy of the array with the new item added to the end_. This is important since we must
The event handler also resets the value of the controlled input element by calling the _setNewNote_ function of the _newNote_ state:

```
setNewNote('')copy
```

You can find the code for our current application in its entirety in the _part2-2_ branch of
### Filtering Displayed Elements
Let's add some new functionality to our application that allows us to only view the important notes.
Let's add a piece of state to the _App_ component that keeps track of which notes should be displayed:

```
const App = (props) => {
  const [notes, setNotes] = useState(props.notes) 
  const [newNote, setNewNote] = useState('')
  const [showAll, setShowAll] = useState(true)  
  // ...
}copy
```

Let's change the component so that it stores a list of all the notes to be displayed in the _notesToShow_ variable. The items on the list depend on the state of the component:

```
import { useState } from 'react'
import Note from './components/Note'

const App = (props) => {
  const [notes, setNotes] = useState(props.notes)
  const [newNote, setNewNote] = useState('') 
  const [showAll, setShowAll] = useState(true)

  // ...

  const notesToShow = showAll    ? notes    : notes.filter(note => note.important === true)
  return (
    <div>
      <h1>Notes</h1>
      <ul>
        {notesToShow.map(note =>          <Note key={note.id} note={note} />
        )}
      </ul>
      // ...
    </div>
  )
}copy
```

The definition of the _notesToShow_ variable is rather compact:

```
const notesToShow = showAll
  ? notes
  : notes.filter(note => note.important === true)copy
```

The definition uses the
The operator functions as follows. If we have:

```
const result = condition ? val1 : val2copy
```

the _result_ variable will be set to the value of _val1_ if _condition_ is true. If _condition_ is false, the _result_ variable will be set to the value of _val2_.
If the value of _showAll_ is false, the _notesToShow_ variable will be assigned to a list that only contains notes that have the _important_ property set to true. Filtering is done with the help of the array

```
notes.filter(note => note.important === true)copy
```

The comparison operator is redundant, since the value of _note.important_ is either _true_ or _false_ , which means that we can simply write:

```
notes.filter(note => note.important)copy
```

We showed the comparison operator first to emphasize an important detail: in JavaScript _val1 == val2_ does not always work as expected. When performing comparisons, it's therefore safer to exclusively use _val1 === val2_. You can read more about the topic
You can test out the filtering functionality by changing the initial value of the _showAll_ state.
Next, let's add functionality that enables users to toggle the _showAll_ state of the application from the user interface.
The relevant changes are shown below:

```
import { useState } from 'react' 
import Note from './components/Note'

const App = (props) => {
  const [notes, setNotes] = useState(props.notes) 
  const [newNote, setNewNote] = useState('')
  const [showAll, setShowAll] = useState(true)

  // ...

  return (
    <div>
      <h1>Notes</h1>
      <div>        <button onClick={() => setShowAll(!showAll)}>          show {showAll ? 'important' : 'all'}        </button>      </div>      <ul>
        {notesToShow.map(note =>
          <Note key={note.id} note={note} />
        )}
      </ul>
      // ...    
    </div>
  )
}copy
```

The displayed notes (all versus important) are controlled with a button. The event handler for the button is so simple that it has been defined directly in the attribute of the button element. The event handler switches the value of _showAll_ from true to false and vice versa:

```
() => setShowAll(!showAll)copy
```

The text of the button depends on the value of the _showAll_ state:

```
show {showAll ? 'important' : 'all'}copy
```

You can find the code for our current application in its entirety in the _part2-3_ branch of
### Exercises 2.6.-2.10
In the first exercise, we will start working on an application that will be further developed in the later exercises. In related sets of exercises, it is sufficient to return the final version of your application. You may also make a separate commit after you have finished each part of the exercise set, but doing so is not required.
#### 2.6: The Phonebook Step 1
Let's create a simple phonebook. _**In this part, we will only be adding names to the phonebook.**_
Let us start by implementing the addition of a person to the phonebook.
You can use the code below as a starting point for the _App_ component of your application:

```
import { useState } from 'react'

const App = () => {
  const [persons, setPersons] = useState([
    { name: 'Arto Hellas' }
  ]) 
  const [newName, setNewName] = useState('')

  return (
    <div>
      <h2>Phonebook</h2>
      <form>
        <div>
          name: <input />
        </div>
        <div>
          <button type="submit">add</button>
        </div>
      </form>
      <h2>Numbers</h2>
      ...
    </div>
  )
}

export default Appcopy
```

The _newName_ state is meant for controlling the form input element.
Sometimes it can be useful to render state and other variables as text for debugging purposes. You can temporarily add the following element to the rendered component:

```
<div>debug: {newName}</div>copy
```

It's also important to put what we learned in the [debugging React applications](../part1/01-a-more-complex-state-debugging-react-apps.md) chapter of part one into good use. The _incredibly_ useful for tracking changes that occur in the application's state.
After finishing this exercise your application should look something like this:
![screenshot of 2.6 finished](../assets/357c56277b42a41b.png)
Note the use of the React developer tools extension in the picture above!
**NB:**

- you can use the person's name as a value of the _key_ property
- remember to prevent the default action of submitting HTML forms!


#### 2.7: The Phonebook Step 2
Prevent the user from being able to add names that already exist in the phonebook. JavaScript arrays have numerous suitable
Issue a warning with the
![browser alert: "user already exists in the phonebook"](../assets/0064bbc7966ed42d.png)
**Hint:** when you are forming strings that contain values from variables, it is recommended to use a

```
`${newName} is already added to phonebook`copy
```

If the _newName_ variable holds the value _Arto Hellas_ , the template string expression returns the string

```
`Arto Hellas is already added to phonebook`copy
```

The same could be done in a more Java-like fashion by using the plus operator:

```
newName + ' is already added to phonebook'copy
```

Using template strings is the more idiomatic option and the sign of a true JavaScript professional.
#### 2.8: The Phonebook Step 3
Expand your application by allowing users to add phone numbers to the phone book. You will need to add a second _input_ element to the form (along with its own event handler):

```
<form>
  <div>name: <input /></div>
  <div>number: <input /></div>
  <div><button type="submit">add</button></div>
</form>copy
```

At this point, the application could look something like this. The image also displays the application's state with the help of
![2.8 sample screenshot](../assets/eae43c9eb7aff40a.png)
#### 2.9*: The Phonebook Step 4
Implement a search field that can be used to filter the list of people by name:
![2.9 search field](../assets/816983ffbe8bc540.png)
You can implement the search field as an _input_ element that is placed outside the HTML form. The filtering logic shown in the image is _case insensitive_ , meaning that the search term _arto_ also returns results that contain Arto with an uppercase A.
**NB:** When you are working on new functionality, it's often useful to "hardcode" some dummy data into your application, e.g.

```
const App = () => {
  const [persons, setPersons] = useState([
    { name: 'Arto Hellas', number: '040-123456', id: 1 },
    { name: 'Ada Lovelace', number: '39-44-5323523', id: 2 },
    { name: 'Dan Abramov', number: '12-43-234345', id: 3 },
    { name: 'Mary Poppendieck', number: '39-23-6423122', id: 4 }
  ])

  // ...
}copy
```

This saves you from having to manually input data into your application for testing out your new functionality.
#### 2.10: The Phonebook Step 5
If you have implemented your application in a single component, refactor it by extracting suitable parts into new components. Maintain the application's state and all event handlers in the _App_ root component.
It is sufficient to extract _**three**_ components from the application. Good candidates for separate components are, for example, the search filter, the form for adding new people to the phonebook, a component that renders all people from the phonebook, and a component that renders a single person's details.
The application's root component could look similar to this after the refactoring. The refactored root component below only renders titles and lets the extracted components take care of the rest.

```
const App = () => {
  // ...

  return (
    <div>
      <h2>Phonebook</h2>

      <Filter ... />

      <h3>Add a new</h3>

      <PersonForm 
        ...
      />

      <h3>Numbers</h3>

      <Persons ... />
    </div>
  )
}copy
```

**NB** : You might run into problems in this exercise if you define your components "in the wrong place". Now would be a good time to rehearse the chapter [do not define a component in another component](../part1/01-a-more-complex-state-debugging-react-apps-do-not-define-components-within-components.md) from the last part.
[Part 2a **Previous part**](../part2/01-rendering-a-collection-modules.md)[Part 2c **Next part**](../part2/01-getting-data-from-server.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)
