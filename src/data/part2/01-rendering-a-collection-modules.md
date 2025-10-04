---{
  "title": "Rendering a collection, modules",
  "source_url": "https://fullstackopen.com/en/part2/rendering_a_collection_modules",
  "crawl_timestamp": "2025-10-04T19:16:15Z",
  "checksum": "8ad5a2c701ded5b4de5b993949e7e490d1b6d121a46a74af190d90134b1b8daf"
}
---[Skip to content](../part2/01-rendering-a-collection-modules-course-main-content.md)
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
Rendering a collection, modules
a Rendering a collection, modules
  * [console.log](../part2/01-rendering-a-collection-modules-console-log.md)
  * [Protip: Visual Studio Code snippets](../part2/01-rendering-a-collection-modules-protip-visual-studio-code-snippets.md)
  * [JavaScript Arrays](../part2/01-rendering-a-collection-modules-java-script-arrays.md)
  * [Event Handlers Revisited](../part2/01-rendering-a-collection-modules-event-handlers-revisited.md)
  * [Rendering Collections](../part2/01-rendering-a-collection-modules-rendering-collections.md)
  * [Key-attribute](../part2/01-rendering-a-collection-modules-key-attribute.md)
  * [Map](../part2/01-rendering-a-collection-modules-map.md)
  * [Anti-pattern: Array Indexes as Keys](../part2/01-rendering-a-collection-modules-anti-pattern-array-indexes-as-keys.md)
  * [Refactoring Modules](../part2/01-rendering-a-collection-modules-refactoring-modules.md)
  * [When the Application Breaks](../part2/01-rendering-a-collection-modules-when-the-application-breaks.md)
  * [Web developer's oath](../part2/01-rendering-a-collection-modules-web-developers-oath.md)
  * [Exercises 2.1.-2.5.](../part2/01-rendering-a-collection-modules-exercises-2-1-2-5.md)


[b Forms](../part2/01-forms.md)[c Getting data from server](../part2/01-getting-data-from-server.md)[d Altering data in server](../part2/01-altering-data-in-server.md)[e Adding styles to React app](../part2/01-adding-styles-to-react-app.md)
a
# Rendering a collection, modules
Before starting a new part, let's recap some of the topics that proved difficult last year.
### console.log
**_What's the difference between an experienced JavaScript programmer and a rookie? The experienced one uses console.log 10-100 times more._**
Paradoxically, this seems to be true even though a rookie programmer would need _console.log_ (or any debugging method) more than an experienced one.
When something does not work, don't just guess what's wrong. Instead, log or use some other way of debugging.
**NB** As explained in part 1, when you use the command _console.log_ for debugging, don't concatenate things 'the Java way' with a plus. Instead of writing:
```
console.log('props value is ' + props)copy
```

separate the things to be printed with a comma:
```
console.log('props value is', props)copy
```

If you concatenate an object with a string and log it to the console (like in our first example), the result will be pretty useless:
```
props value is [object Object]copy
```

On the contrary, when you pass objects as distinct arguments separated by commas to _console.log_ , like in our second example above, the content of the object is printed to the developer console as strings that are insightful. If necessary, read more about [debugging React applications](../part1/01-a-more-complex-state-debugging-react-apps-debugging-react-applications.md).
### Protip: Visual Studio Code snippets
With Visual Studio Code it's easy to create 'snippets', i.e., shortcuts for quickly generating commonly re-used portions of code, much like how 'sout' works in Netbeans.
Instructions for creating snippets can be found 
Useful, ready-made snippets can also be found as VS Code plugins, in the 
The most important snippet is the one for the _console.log()_ command, for example, _clog_. This can be created like so:
```
{
  "console.log": {
    "prefix": "clog",
    "body": [
      "console.log('$1')",
    ],
    "description": "Log output to console"
  }
}copy
```

Debugging your code using _console.log()_ is so common that Visual Studio Code has that snippet built in. To use it, type _log_ and hit Tab to autocomplete. More fully featured _console.log()_ snippet extensions can be found in the 
### JavaScript Arrays
From here on out, we will be using the functional programming operators of the JavaScript _find_ , _filter_ , and _map_ - all of the time.
If operating arrays with functional operators feels foreign to you, it is worth watching at least the first three parts of the YouTube video series 
### Event Handlers Revisited
Based on last year's course, event handling has proved to be difficult.
It's worth reading the revision chapter at the end of the previous part - [event handlers revisited](../part1/01-a-more-complex-state-debugging-react-apps-event-handling-revisited.md) - if it feels like your own knowledge on the topic needs some brushing up.
Passing event handlers to the child components of the _App_ component has raised some questions. A small revision on the topic can be found [here](../part1/01-a-more-complex-state-debugging-react-apps-passing-event-handlers-to-child-components.md).
### Rendering Collections
Now, we will build the frontend, or the user interface (the part users see in their browser), using React, similar to the example application from [part 0](../part0/01-part0.md).
Let's start with the following (the file _App.jsx_):
```
const App = (props) => {
  const { notes } = props

  return (
    <div>
      <h1>Notes</h1>
      <ul>
        <li>{notes[0].content}</li>
        <li>{notes[1].content}</li>
        <li>{notes[2].content}</li>
      </ul>
    </div>
  )
}

export default Appcopy
```

The file _main.jsx_ looks like this:
```
import ReactDOM from 'react-dom/client'
import App from './App'

const notes = [
  {
    id: 1,
    content: 'HTML is easy',
    important: true
  },
  {
    id: 2,
    content: 'Browser can execute only JavaScript',
    important: false
  },
  {
    id: 3,
    content: 'GET and POST are the most important methods of HTTP protocol',
    important: true
  }
]

ReactDOM.createRoot(document.getElementById('root')).render(
  <App notes={notes} />
)copy
```

Every note contains its textual content, a _boolean_ value for marking whether the note has been categorized as important or not, and also a unique _id_.
The example above works due to the fact that there are exactly three notes in the array.
A single note is rendered by accessing the objects in the array by referring to a hard-coded index number:
```
<li>{notes[1].content}</li>copy
```

This is, of course, not practical. We can improve on this by generating React elements from the array objects using the 
```
notes.map(note => <li>{note.content}</li>)copy
```

The result is an array of _li_ elements.
```
[
  <li>HTML is easy</li>,
  <li>Browser can execute only JavaScript</li>,
  <li>GET and POST are the most important methods of HTTP protocol</li>,
]copy
```

Which can then be placed inside _ul_ tags:
```
const App = (props) => {
  const { notes } = props

  return (
    <div>
      <h1>Notes</h1>
      <ul>        {notes.map(note => <li>{note.content}</li>)}      </ul>    </div>
  )
}copy
```

Because the code generating the _li_ tags is JavaScript, it must be wrapped in curly braces in a JSX template just like all other JavaScript code.
We will also make the code more readable by separating the arrow function's declaration across multiple lines:
```
const App = (props) => {
  const { notes } = props

  return (
    <div>
      <h1>Notes</h1>
      <ul>
        {notes.map(note => 
          <li>            {note.content}          </li>        )}
      </ul>
    </div>
  )
}copy
```

### Key-attribute
Even though the application seems to be working, there is a nasty warning in the console:
![unique key prop console error](../assets/da0e784e70c1376d.png)
As the linked _map_ method, must each have a unique key value: an attribute called _key_.
Let's add the keys:
```
const App = (props) => {
  const { notes } = props

  return (
    <div>
      <h1>Notes</h1>
      <ul>
        {notes.map(note => 
          <li key={note.id}>            {note.content}
          </li>
        )}
      </ul>
    </div>
  )
}copy
```

And the error message disappears.
React uses the key attributes of objects in an array to determine how to update the view generated by a component when the component is re-rendered. More about this is in the 
### Map
Understanding how the array method 
The application contains an array called _notes_ :
```
const notes = [
  {
    id: 1,
    content: 'HTML is easy',
    important: true
  },
  {
    id: 2,
    content: 'Browser can execute only JavaScript',
    important: false
  },
  {
    id: 3,
    content: 'GET and POST are the most important methods of HTTP protocol',
    important: true
  }
]copy
```

Let's pause for a moment and examine how _map_ works.
If the following code is added to, let's say, the end of the file:
```
const result = notes.map(note => note.id)
console.log(result)copy
```

_[1, 2, 3]_ will be printed to the console. _map_ always creates a new array, the elements of which have been created from the elements of the original array by _mapping_ : using the function given as a parameter to the _map_ method. 
The function is
```
note => note.idcopy
```

Which is an arrow function written in compact form. The full form would be:
```
(note) => {
  return note.id
}copy
```

The function gets a note object as a parameter and _returns_ the value of its _id_ field.
Changing the command to:
```
const result = notes.map(note => note.content)copy
```

will give you an array containing the contents of the notes.
This is already pretty close to the React code we used:
```
notes.map(note =>
  <li key={note.id}>
    {note.content}
  </li>
)copy
```

which generates an _li_ tag containing the contents of the note from each note object.
Because the function parameter passed to the _map_ method - 
```
note => <li key={note.id}>{note.content}</li>copy
```

- is used to create view elements, the value of the variable must be rendered inside curly braces. Try to see what happens if the braces are removed.
The use of curly braces will cause some pain in the beginning, but you will get used to them soon enough. The visual feedback from React is immediate.
### Anti-pattern: Array Indexes as Keys
We could have made the error message on our console disappear by using the array indexes as keys. The indexes can be retrieved by passing a second parameter to the callback function of the _map_ method: 
```
notes.map((note, i) => ...)copy
```

When called like this, _i_ is assigned the value of the index of the position in the array where the note resides.
As such, one way to define the row generation without getting errors is:
```
<ul>
  {notes.map((note, i) => 
    <li key={i}>
      {note.content}
    </li>
  )}
</ul>copy
```

This is, however, **not recommended** and can create undesired problems even if it seems to be working just fine.
Read more about this in 
### Refactoring Modules
Let's tidy the code up a bit. We are only interested in the field _notes_ of the props, so let's retrieve that directly using 
```
const App = ({ notes }) => {  return (
    <div>
      <h1>Notes</h1>
      <ul>
        {notes.map(note => 
          <li key={note.id}>
            {note.content}
          </li>
        )}
      </ul>
    </div>
  )
}copy
```

If you have forgotten what destructuring means and how it works, please review the [section on destructuring](../part1/01-component-state-event-handlers-destructuring.md).
We'll separate displaying a single note into its own component _Note_ :
```
const Note = ({ note }) => {  return (    <li>{note.content}</li>  )}
const App = ({ notes }) => {
  return (
    <div>
      <h1>Notes</h1>
      <ul>
        {notes.map(note =>           <Note key={note.id} note={note} />        )}      </ul>
    </div>
  )
}copy
```

Note that the _key_ attribute must now be defined for the _Note_ components, and not for the _li_ tags like before.
A whole React application can be written in a single file. Although that is, of course, not very practical. Common practice is to declare each component in its own file as an _ES6-module_.
We have been using modules the whole time. The first few lines of the file _main.jsx_ :
```
import ReactDOM from "react-dom/client"
import App from "./App"copy
```

_react-dom/client_ is placed into the variable _ReactDOM_ , and the module that defines the main component of the app is placed into the variable _App_
Let's move our _Note_ component into its own module.
In smaller applications, components are usually placed in a directory called _components_ , which is in turn placed within the _src_ directory. The convention is to name the file after the component.
Now, we'll create a directory called _components_ for our application and place a file named _Note.jsx_ inside. The contents of the file are as follows:
```
const Note = ({ note }) => {
  return <li>{note.content}</li>
}

export default Notecopy
```

The last line of the module _Note_.
Now the file that is using the component - _App.jsx_ - can 
```
import Note from './components/Note'
const App = ({ notes }) => {
  // ...
}copy
```

The component exported by the module is now available for use in the variable _Note_ , just as it was earlier.
Note that when importing our own components, their location must be given _in relation to the importing file_ :
```
'./components/Note'copy
```

The period - _._ - in the beginning refers to the current directory, so the module's location is a file called _Note.jsx_ in the _components_ sub-directory of the current directory. The filename extension _.jsx_ can be omitted.
Modules have plenty of other uses other than enabling component declarations to be separated into their own files. We will get back to them later in this course.
The current code of the application can be found on 
Note that the _main_ branch of the repository contains the code for a later version of the application. The current code is in the branch 
![GitHub branch screenshot](../assets/b8ae52b4a5d80e1c.png)
If you clone the project, run the command _npm install_ before starting the application with _npm run dev_.
### When the Application Breaks
Early in your programming career (and even after 30 years of coding like yours truly), what often happens is that the application just completely breaks down. This is even more so the case with dynamically typed languages, such as JavaScript, where the compiler does not check the data type. For instance, function variables or return values.
A "React explosion" can, for example, look like this:
![react sample error](../assets/e9d4a31130a8c55c.png)
In these situations, your best way out is the _console.log_ method.
The piece of code causing the explosion is this:
```
const Course = ({ course }) => (
  <div>
    <Header course={course} />
  </div>
)

const App = () => {
  const course = {
    // ...
  }

  return (
    <div>
      <Course course={course} />
    </div>
  )
}copy
```

We'll hone in on the reason for the breakdown by adding _console.log_ commands to the code. Because the first thing to be rendered is the _App_ component, it's worth putting the first _console.log_ there:
```
const App = () => {
  const course = {
    // ...
  }

  console.log('App works...')
  return (
    // ..
  )
}copy
```

To see the printing in the console, we must scroll up over the long red wall of errors.
![initial printing of the console](../assets/d48f3792871c6ea5.png)
When one thing is found to be working, it's time to log deeper. If the component has been declared as a single statement or a function without a return, it makes printing to the console harder.
```
const Course = ({ course }) => (
  <div>
    <Header course={course} />
  </div>
)copy
```

The component should be changed to its longer form for us to add the printing:
```
const Course = ({ course }) => { 
  console.log(course)  return (
    <div>
      <Header course={course} />
    </div>
  )
}copy
```

Quite often the root of the problem is that the props are expected to be of a different type, or called with a different name than they actually have, and destructuring fails as a result. The problem often begins to solve itself when destructuring is removed and we see what the _props_ contain.
```
const Course = (props) => {  console.log(props)  const { course } = props
  return (
    <div>
      <Header course={course} />
    </div>
  )
}copy
```

If the problem has still not been resolved, sadly there isn't much to do apart from continuing to bug-hunt by sprinkling more _console.log_ statements around your code. 
I added this chapter to the material after the model answer for the next question exploded completely (due to props being of the wrong type), and I had to debug it using _console.log_.
### Web developer's oath
Before the exercises, let me remind what you promised at the end of the previous part.
Programming is hard, that is why I will use all the possible means to make it easier
  * I will have my browser developer console open all the time
  * I progress with small steps
  * I will write lots of _console.log_ statements to make sure I understand how the code behaves and to help pinpoint problems
  * If my code does not work, I will not write more code. Instead, I start deleting the code until it works or just return to a state when everything was still working
  * When I ask for help in the course Discord channel or elsewhere I formulate my questions properly, see [here](../part0/01-general-info-how-to-get-help-in-discord.md) how to ask for help


### Exercises 2.1.-2.5.
The exercises are submitted via GitHub, and by marking the exercises as done in the 
You can submit all of the exercises into the same repository, or use multiple different repositories. If you submit exercises from different parts into the same repository, name your directories well.
The exercises are submitted **One part at a time**. When you have submitted the exercises for a part, you can no longer submit any missed exercises for that part.
Note that this part has more exercises than the ones before, so _do not submit_ until you have done all the exercises from this part you want to submit.
#### 2.1: Course information step 6
Let's finish the code for rendering course contents from exercises 1.1 - 1.5. You can start with the code from the model answers. The model answers for part 1 can be found by going to the _my submissions_ at the top, and in the row corresponding to part 1 under the _solutions_ column clicking on _show_. To see the solution to the _course info_ exercise, click on _App.jsx_ under _courseinfo_.
**Note that if you copy a project from one place to another, you might have to delete the _node_modules_ directory and install the dependencies again with the command _npm install_ before you can start the application.**
Generally, it's not recommended that you copy a project's whole contents and/or add the _node_modules_ directory to the version control system.
Let's change the _App_ component like so:
```
const App = () => {
  const course = {
    id: 1,
    name: 'Half Stack application development',
    parts: [
      {
        name: 'Fundamentals of React',
        exercises: 10,
        id: 1
      },
      {
        name: 'Using props to pass data',
        exercises: 7,
        id: 2
      },
      {
        name: 'State of a component',
        exercises: 14,
        id: 3
      }
    ]
  }

  return <Course course={course} />
}

export default Appcopy
```

Define a component responsible for formatting a single course called _Course_.
The component structure of the application can be, for example, the following:
```
App
  Course
    Header
    Content
      Part
      Part
      ...copy
```

Hence, the _Course_ component contains the components defined in the previous part, which are responsible for rendering the course name and its parts.
The rendered page can, for example, look as follows:
![half stack application screenshot](../assets/47ff62d4ec9c2c86.png)
You don't need the sum of the exercises yet.
The application must work _regardless of the number of parts a course has_ , so make sure the application works if you add or remove parts of a course.
Ensure that the console shows no errors!
#### 2.2: Course information step 7
Show also the sum of the exercises of the course.
![sum of exercises added feature](../assets/2503262c534490df.png)
#### 2.3*: Course information step 8
If you haven't done so already, calculate the sum of exercises with the array method 
**Pro tip:** when your code looks as follows:
```
const total = 
  parts.reduce((s, p) => someMagicHere)copy
```

and does not work, it's worth it to use _console.log_ , which requires the arrow function to be written in its longer form:
```
const total = parts.reduce((s, p) => {
  console.log('what is happening', s, p)
  return someMagicHere 
})copy
```

**Not working? :** Use your search engine to look up how _reduce_ is used in an **Object Array**.
#### 2.4: Course information step 9
Let's extend our application to allow for an _arbitrary number_ of courses:
```
const App = () => {
  const courses = [
    {
      name: 'Half Stack application development',
      id: 1,
      parts: [
        {
          name: 'Fundamentals of React',
          exercises: 10,
          id: 1
        },
        {
          name: 'Using props to pass data',
          exercises: 7,
          id: 2
        },
        {
          name: 'State of a component',
          exercises: 14,
          id: 3
        },
        {
          name: 'Redux',
          exercises: 11,
          id: 4
        }
      ]
    }, 
    {
      name: 'Node.js',
      id: 2,
      parts: [
        {
          name: 'Routing',
          exercises: 3,
          id: 1
        },
        {
          name: 'Middlewares',
          exercises: 7,
          id: 2
        }
      ]
    }
  ]

  return (
    <div>
      // ...
    </div>
  )
}copy
```

The application can, for example, look like this:
![arbitrary number of courses feature add-on](../assets/d9913a59d85b0683.png)
#### 2.5: Separate module step 10
Declare the _Course_ component as a separate module, which is imported by the _App_ component. You can include all subcomponents of the course in the same module.
[ Part 1 **Previous part** ](../part1/01-part1.md)[ Part 2b **Next part** ](../part2/01-forms.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)