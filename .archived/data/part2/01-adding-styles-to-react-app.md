---{
  "title": "Adding styles to React app",
  "source_url": "https://fullstackopen.com/en/part2/adding_styles_to_react_app",
  "crawl_timestamp": "2025-10-04T19:16:06Z",
  "checksum": "a4357ced3c17758e9faf8a9a465cf27fbbc3e4810ab3dc5ea81a4e83dd06d811"
}
---[Skip to content](../part2/01-adding-styles-to-react-app-course-main-content.md)
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
Adding styles to React app
[a Rendering a collection, modules](../part2/01-rendering-a-collection-modules.md)[b Forms](../part2/01-forms.md)[c Getting data from server](../part2/01-getting-data-from-server.md)[d Altering data in server](../part2/01-altering-data-in-server.md)
e Adding styles to React app

- [Improved error message](../part2/01-adding-styles-to-react-app-improved-error-message.md)
- [Inline styles](../part2/01-adding-styles-to-react-app-inline-styles.md)
- [Exercises 2.16.-2.17.](../part2/01-adding-styles-to-react-app-exercises-2-16-2-17.md)
- [Couple of important remarks](../part2/01-adding-styles-to-react-app-couple-of-important-remarks.md)
- [Exercises 2.18.-2.20.](../part2/01-adding-styles-to-react-app-exercises-2-18-2-20.md)


e
# Adding styles to React app
The appearance of our current Notes application is quite modest. In [exercise 0.2](../part0/01-fundamentals-of-web-apps-exercises-0-1-0-6.md), the assignment was to go through Mozilla's
Let's take a look at how we can add styles to a React application. There are several different ways of doing this and we will take a look at the other methods later on. First, we will add CSS to our application the old-school way; in a single file without using a
Let's add a new _index.css_ file under the _src_ directory and then add it to the application by importing it in the _main.jsx_ file:

```
import './index.css'copy
```

Let's add the following CSS rule to the _index.css_ file:

```
h1 {
  color: green;
}copy
```

CSS rules comprise of _selectors_ and _declarations_. The selector defines which elements the rule should be applied to. The selector above is _h1_ , which will match all of the _h1_ header tags in our application.
The declaration sets the _color_ property to the value _green_.
One CSS rule can contain an arbitrary number of properties. Let's modify the previous rule to make the text cursive, by defining the font style as _italic_ :

```
h1 {
  color: green;
  font-style: italic;}copy
```

There are many ways of matching elements by using
If we wanted to target, let's say, each one of the notes with our styles, we could use the selector _li_ , as all of the notes are wrapped inside _li_ tags:

```
const Note = ({ note, toggleImportance }) => {
  const label = note.important 
    ? 'make not important' 
    : 'make important'

  return (
    <li>
      {note.content} 
      <button onClick={toggleImportance}>{label}</button>
    </li>
  )
}copy
```

Let's add the following rule to our style sheet (since my knowledge of elegant web design is close to zero, the styles don't make much sense):

```
li {
  color: grey;
  padding-top: 3px;
  font-size: 15px;
}copy
```

Using element types for defining CSS rules is slightly problematic. If our application contained other _li_ tags, the same style rule would also be applied to them.
If we want to apply our style specifically to notes, then it is better to use
In regular HTML, classes are defined as the value of the _class_ attribute:

```
<li class="note">some text...</li>copy
```

In React we have to use the _Note_ component:

```
const Note = ({ note, toggleImportance }) => {
  const label = note.important 
    ? 'make not important' 
    : 'make important'

  return (
    <li className='note'>      {note.content} 
      <button onClick={toggleImportance}>{label}</button>
    </li>
  )
}copy
```

Class selectors are defined with the _.classname_ syntax:

```
.note {
  color: grey;
  padding-top: 5px;
  font-size: 15px;
}copy
```

If you now add other _li_ elements to the application, they will not be affected by the style rule above.
### Improved error message
We previously implemented the error message that was displayed when the user tried to toggle the importance of a deleted note with the _alert_ method. Let's implement the error message as its own React component.
The component is quite simple:

```
const Notification = ({ message }) => {
  if (message === null) {
    return null
  }

  return (
    <div className='error'>
      {message}
    </div>
  )
}copy
```

If the value of the _message_ prop is _null_ , then nothing is rendered to the screen, and in other cases, the message gets rendered inside of a div element.
Let's add a new piece of state called _errorMessage_ to the _App_ component. Let's initialize it with some error message so that we can immediately test our component:

```
const App = () => {
  const [notes, setNotes] = useState([]) 
  const [newNote, setNewNote] = useState('')
  const [showAll, setShowAll] = useState(true)
  const [errorMessage, setErrorMessage] = useState('some error happened...')
  // ...

  return (
    <div>
      <h1>Notes</h1>
      <Notification message={errorMessage} />      <div>
        <button onClick={() => setShowAll(!showAll)}>
          show {showAll ? 'important' : 'all' }
        </button>
      </div>      
      // ...
    </div>
  )
}copy
```

Then let's add a style rule that suits an error message:

```
.error {
  color: red;
  background: lightgrey;
  font-size: 20px;
  border-style: solid;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 10px;
}copy
```

Now we are ready to add the logic for displaying the error message. Let's change the _toggleImportanceOf_ function in the following way:

```
  const toggleImportanceOf = id => {
    const note = notes.find(n => n.id === id)
    const changedNote = { ...note, important: !note.important }

    noteService
      .update(id, changedNote).then(returnedNote => {
        setNotes(notes.map(note => note.id !== id ? note : returnedNote))
      })
      .catch(error => {
        setErrorMessage(          `Note '${note.content}' was already removed from server`        )        setTimeout(() => {          setErrorMessage(null)        }, 5000)        setNotes(notes.filter(n => n.id !== id))
      })
  }copy
```

When the error occurs we add a descriptive error message to the _errorMessage_ state. At the same time, we start a timer, that will set the _errorMessage_ state to _null_ after five seconds.
The result looks like this:
![error removed from server screenshot from app](../assets/92d6be547be25d86.png)
The code for the current state of our application can be found in the _part2-7_ branch on
### Inline styles
React also makes it possible to write styles directly in the code as so-called
The idea behind defining inline styles is extremely simple. Any React component or element can be provided with a set of CSS properties as a JavaScript object through the
CSS rules are defined slightly differently in JavaScript than in normal CSS files. Let's say that we wanted to give some element the color green and italic font. In CSS, it would look like this:

```
{
  color: green;
  font-style: italic;
}copy
```

But as a React inline-style object it would look like this:

```
{
  color: 'green',
  fontStyle: 'italic'
}copy
```

Every CSS property is defined as a separate property of the JavaScript object. Numeric values for pixels can be simply defined as integers. One of the major differences compared to regular CSS, is that hyphenated (kebab case) CSS properties are written in camelCase.
Let's add a footer component, _Footer_ , to our application and define inline styles for it. The component is defined in the file _components/Footer.jsx_ and used in the file _App.jsx_ as follows:

```
const Footer = () => {
  const footerStyle = {
    color: 'green',
    fontStyle: 'italic'
  }

  return (
    <div style={footerStyle}>
      <br />
      <p>
        Note app, Department of Computer Science, University of Helsinki 2025
      </p>
    </div>
  )
}

export default Footercopy
```

```
import { useState, useEffect } from 'react'
import Footer from './components/Footer'import Note from './components/Note'
import Notification from './components/Notification'
import noteService from './services/notes'

const App = () => {
  // ...

  return (
    <div>
      <h1>Notes</h1>

      <Notification message={errorMessage} />

      // ...  

      <Footer />    </div>
  )
}copy
```

Inline styles come with certain limitations. For instance, so-called
Inline styles and some of the other ways of adding styles to React components go completely against the grain of old conventions. Traditionally, it has been considered best practice to entirely separate CSS from the content (HTML) and functionality (JavaScript). According to this older school of thought, the goal was to write CSS, HTML, and JavaScript into their separate files.
The philosophy of React is, in fact, the polar opposite of this. Since the separation of CSS, HTML, and JavaScript into separate files did not seem to scale well in larger applications, React bases the division of the application along the lines of its logical functional entities.
The structural units that make up the application's functional entities are React components. A React component defines the HTML for structuring the content, the JavaScript functions for determining functionality, and also the component's styling; all in one place. This is to create individual components that are as independent and reusable as possible.
The code of the final version of our application can be found in the _part2-8_ branch on
### Exercises 2.16.-2.17
#### 2.16: Phonebook step 11
Use the [improved error message](../part2/01-adding-styles-to-react-app-improved-error-message.md) example from part 2 as a guide to show a notification that lasts for a few seconds after a successful operation is executed (a person is added or a number is changed):
![successful green added screenshot](../assets/675cc21824f019f6.png)
#### 2.17*: Phonebook step 12
Open your application in two browsers. **If you delete a person in browser 1** a short while before attempting to _change the person's phone number_ in browser 2, you will get the following error messages:
![error message 404 not found when changing multiple browsers](../assets/d8ad4c24e0512d64.png)
Fix the issue according to the example shown in [promise and errors](../part2/01-altering-data-in-server-promises-and-errors.md) in part 2. Modify the example so that the user is shown a message when the operation does not succeed. The messages shown for successful and unsuccessful events should look different:
![error message shown on screen instead of in console feature add-on](../assets/c26bb7aec9fc68d0.png)
**Note** that even if you handle the exception, the first "404" error message is still printed to the console. But you should not see "Uncaught (in promise) Error".
### Couple of important remarks
At the end of this part there are a few more challenging exercises. At this stage, you can skip the exercises if they are too much of a headache, we will come back to the same themes again later. The material is worth reading through in any case.
We have done one thing in our app that is masking away a very typical source of error.
We set the state _notes_ to have initial value of an empty array:

```
const App = () => {
  const [notes, setNotes] = useState([])

  // ...
}copy
```

This is a pretty natural initial value since the notes are a set, that is, there are many notes that the state will store.
If the state were only saving "one thing", a more appropriate initial value would be _null_ denoting that there is _nothing_ in the state at the start. Let's see what happens if we use this initial value:

```
const App = () => {
  const [notes, setNotes] = useState(null)
  // ...
}copy
```

The app breaks down:
![console typerror cannot read properties of null via map from App](../assets/961c00c3bfd57d6a.png)
The error message gives the reason and location for the error. The code that caused the problems is the following:

```
  // notesToShow gets the value of notes
  const notesToShow = showAll
    ? notes
    : notes.filter(note => note.important)

  // ...

  {notesToShow.map(note =>    <Note key={note.id} note={note} />
  )}copy
```

The error message is

```
Cannot read properties of null (reading 'map')copy
```

The variable _notesToShow_ is first assigned the value of the state _notes_ and then the code tries to call method _map_ to a nonexisting object, that is, to _null_.
What is the reason for that?
The effect hook uses the function _setNotes_ to set _notes_ to have the notes that the backend is returning:

```
  useEffect(() => {
    noteService
      .getAll()
      .then(initialNotes => {
        setNotes(initialNotes)      })
  }, [])copy
```

However the problem is that the effect is executed only _after the first render_. And because _notes_ has the initial value of null:

```
const App = () => {
  const [notes, setNotes] = useState(null)
  // ...copy
```

on the first render the following code gets executed:

```
notesToShow = notes

// ...

notesToShow.map(note => ...)copy
```

and this blows up the app since we can not call method _map_ of the value _null_.
When we set _notes_ to be initially an empty array, there is no error since it is allowed to call _map_ to an empty array.
So, the initialization of the state "masked" the problem that is caused by the fact that the data is not yet fetched from the backend.
Another way to circumvent the problem is to use _conditional rendering_ and return null if the component state is not properly initialized:

```
const App = () => {
  const [notes, setNotes] = useState(null)  // ... 

  useEffect(() => {
    noteService
      .getAll()
      .then(initialNotes => {
        setNotes(initialNotes)
      })
  }, [])

  // do not render anything if notes is still null
  if (!notes) {     return null   }
  // ...
} copy
```

So on the first render, nothing is rendered. When the notes arrive from the backend, the effect used function _setNotes_ to set the value of the state _notes_. This causes the component to be rendered again, and at the second render, the notes get rendered to the screen.
The method based on conditional rendering is suitable in cases where it is impossible to define the state so that the initial rendering is possible.
The other thing that we still need to have a closer look at is the second parameter of the useEffect:

```
  useEffect(() => {
    noteService
      .getAll()
      .then(initialNotes => {
        setNotes(initialNotes)  
      })
  }, [])copy
```

The second parameter of _useEffect_ is used to _and_ when the value of the second parameter changes.
If the second parameter is an empty array _[]_ , its content never changes and the effect is only run after the first render of the component. This is exactly what we want when we are initializing the app state from the server.
However, there are situations where we want to perform the effect at other times, e.g. when the state of the component changes in a particular way.
Consider the following simple application for querying currency exchange rates from the

```
import { useState, useEffect } from 'react'
import axios from 'axios'

const App = () => {
  const [value, setValue] = useState('')
  const [rates, setRates] = useState({})
  const [currency, setCurrency] = useState(null)

  useEffect(() => {
    console.log('effect run, currency is now', currency)

    // skip if currency is not defined
    if (currency) {
      console.log('fetching exchange rates...')
      axios
        .get(`https://open.er-api.com/v6/latest/${currency}`)
        .then(response => {
          setRates(response.data.rates)
        })
    }
  }, [currency])

  const handleChange = (event) => {
    setValue(event.target.value)
  }

  const onSearch = (event) => {
    event.preventDefault()
    setCurrency(value)
  }

  return (
    <div>
      <form onSubmit={onSearch}>
        currency: <input value={value} onChange={handleChange} />
        <button type="submit">exchange rate</button>
      </form>
      <pre>
        {JSON.stringify(rates, null, 2)}
      </pre>
    </div>
  )
}

export default Appcopy
```

The user interface of the application has a form, in the input field of which the name of the desired currency is written. If the currency exists, the application renders the exchange rates of the currency to other currencies:
![browser showing currency exchange rates with eur typed and console saying fetching exchange rates](../assets/cfedb7fcc4ab87ed.png)
The application sets the name of the currency entered to the form to the state _currency_ at the moment the button is pressed.
When the _currency_ gets a new value, the application fetches its exchange rates from the API in the effect function:

```
const App = () => {
  // ...
  const [currency, setCurrency] = useState(null)

  useEffect(() => {
    console.log('effect run, currency is now', currency)

    // skip if currency is not defined
    if (currency) {
      console.log('fetching exchange rates...')
      axios
        .get(`https://open.er-api.com/v6/latest/${currency}`)
        .then(response => {
          setRates(response.data.rates)
        })
    }
  }, [currency])  // ...
}copy
```

The useEffect hook now has _[currency]_ as the second parameter. The effect function is therefore executed after the first render, and _always_ after the table as its second parameter _[currency]_ changes. That is, when the state _currency_ gets a new value, the content of the table changes and the effect function is executed.
It is natural to choose _null_ as the initial value for the variable _currency_ , because _currency_ represents a single item. The initial value _null_ indicates that there is nothing in the state yet, and it is also easy to check with a simple if statement whether a value has been assigned to the variable. The effect has the following condition

```
if (currency) { 
  // exchange rates are fetched
}copy
```

which prevents requesting the exchange rates just after the first render when the variable _currency_ still has the initial value, i.e. a _null_ value.
So if the user writes e.g. _eur_ in the search field, the application uses Axios to perform an HTTP GET request to the address _rates_ state.
When the user then enters another value in the search field, e.g. _usd_ , the effect function is executed again and the exchange rates of the new currency are requested from the API.
The way presented here for making API requests might seem a bit awkward. This particular application could have been made completely without using the useEffect, by making the API requests directly in the form submit handler function:

```
  const onSearch = (event) => {
    event.preventDefault()
    axios
      .get(`https://open.er-api.com/v6/latest/${value}`)
      .then(response => {
        setRates(response.data.rates)
      })
  }copy
```

However, there are situations where that technique would not work. For example, you _might_ encounter one such a situation in the exercise 2.20 where the use of useEffect could provide a solution. Note that this depends quite much on the approach you selected, e.g. the model solution does not use this trick.
### Exercises 2.18.-2.20
#### 2.18* Data for countries, step 1
At
The user interface is very simple. The country to be shown is found by typing a search query into the search field.
If there are too many (over 10) countries that match the query, then the user is prompted to make their query more specific:
![too many matches screenshot](../assets/014dcc16758018ab.png)
If there are ten or fewer countries, but more than one, then all countries matching the query are shown:
![matching countries in a list screenshot](../assets/d48c30289df6b371.png)
When there is only one country matching the query, then the basic data of the country (eg. capital and area), its flag and the languages spoken are shown:
![flag and additional attributes screenshot](../assets/adda63f167c7903d.png)
**NB** : It is enough that your application works for most countries. Some countries, like _Sudan_ , can be hard to support since the name of the country is part of the name of another country, _South Sudan_. You don't need to worry about these edge cases.
#### 2.19*: Data for countries, step 2
**There is still a lot to do in this part, so don't get stuck on this exercise!**
Improve on the application in the previous exercise, such that when the names of multiple countries are shown on the page there is a button next to the name of the country, which when pressed shows the view for that country:
![attach show buttons for each country feature](../assets/fa0862fb551f21a0.png)
In this exercise, it is also enough that your application works for most countries. Countries whose name appears in the name of another country, like _Sudan_ , can be ignored.
#### 2.20*: Data for countries, step 3
Add to the view showing the data of a single country, the weather report for the capital of that country. There are dozens of providers for weather data. One suggested API is
![weather report added feature](../assets/796980e058df8735.png)
If you use Open weather map,
**NB:** In some browsers (such as Firefox) the chosen API might send an error response, which indicates that HTTPS encryption is not supported, although the request URL starts with _http://_. This issue can be fixed by completing the exercise using Chrome.
**NB:** You need an api-key to use almost every weather service. Do not save the api-key to source control! Nor hardcode the api-key to your source code. Instead use an
Assuming the api-key is _54l41n3n4v41m34rv0_ , when the application is started like so:

```
export VITE_SOME_KEY=54l41n3n4v41m34rv0 && npm run dev // For Linux/macOS Bash
($env:VITE_SOME_KEY="54l41n3n4v41m34rv0") -and (npm run dev) // For Windows PowerShell
set "VITE_SOME_KEY=54l41n3n4v41m34rv0" && npm run dev // For Windows cmd.execopy
```

you can access the value of the key from the _import.meta.env_ object:

```
const api_key = import.meta.env.VITE_SOME_KEY
// variable api_key now has the value set in startupcopy
```

**NB:** To prevent accidentally leaking environment variables to the client, only variables prefixed with VITE_ are exposed to Vite.
Also remember that if you make changes to environment variables, you need to restart the development server for the changes to take effect.
This was the last exercise of this part of the course. It's time to push your code to GitHub and mark all of your finished exercises to the
[Part 2d **Previous part**](../part2/01-altering-data-in-server.md)[Part 3 **Next part**](../part3/01-part3.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)
