---{
  "title": "Component state, event handlers",
  "source_url": "https://fullstackopen.com/en/part1/component_state_event_handlers",
  "crawl_timestamp": "2025-10-04T19:15:36Z",
  "checksum": "46bfb9860994d17db781b2314c6998e00ee3d3e67af10a69fa57b59e47ee81ec"
}
---[Skip to content](../part1/01-component-state-event-handlers-course-main-content.md)
[{() => fs}](https://fullstackopen.com/en/)
  * [About course](../about/01-about.md)
  * [Course contents](../#course-contents/01-course-contents.md)
  * [FAQ](../faq/01-faq.md)
  * [Partners](../companies/01-companies.md)
  * [Challenge](../challenge/01-challenge.md)
[Search from the material](../search/01-search.md)Toggle dark theme
Select languageSuomi English 中文 Español Français Português(BR) 

[Fullstack](../#course-contents/01-course-contents.md)
[Part 1](../part1/01-part1.md)
Component state, event handlers
[a Introduction to React](../part1/01-introduction-to-react.md)[b JavaScript](../part1/01-java-script.md)
c Component state, event handlers
  * [Component helper functions](../part1/01-component-state-event-handlers-component-helper-functions.md)
  * [Destructuring](../part1/01-component-state-event-handlers-destructuring.md)
  * [Page re-rendering](../part1/01-component-state-event-handlers-page-re-rendering.md)
  * [Stateful component](../part1/01-component-state-event-handlers-stateful-component.md)
  * [Event handling](../part1/01-component-state-event-handlers-event-handling.md)
  * [An event handler is a function](../part1/01-component-state-event-handlers-an-event-handler-is-a-function.md)
  * [Passing state - to child components](../part1/01-component-state-event-handlers-passing-state-to-child-components.md)
  * [Changes in state cause re-rendering](../part1/01-component-state-event-handlers-changes-in-state-cause-re-rendering.md)
  * [Refactoring the components](../part1/01-component-state-event-handlers-refactoring-the-components.md)


[d A more complex state, debugging React apps](../part1/01-a-more-complex-state-debugging-react-apps.md)
c
# Component state, event handlers
Let's go back to working with React.
We start with a new example:
```
const Hello = (props) => {
  return (
    <div>
      <p>
        Hello {props.name}, you are {props.age} years old
      </p>
    </div>
  )
}

const App = () => {
  const name = 'Peter'
  const age = 10

  return (
    <div>
      <h1>Greetings</h1>
      <Hello name="Maya" age={26 + 10} />
      <Hello name={name} age={age} />
    </div>
  )
}copy
```

### Component helper functions
Let's expand our _Hello_ component so that it guesses the year of birth of the person being greeted:
```
const Hello = (props) => {
  const bornYear = () => {    const yearNow = new Date().getFullYear()    return yearNow - props.age  }
  return (
    <div>
      <p>
        Hello {props.name}, you are {props.age} years old
      </p>
      <p>So you were probably born in {bornYear()}</p>    </div>
  )
}copy
```

The logic for guessing the year of birth is encapsulated within a function of its own, which is invoked when the component is rendered.
The person's age does not need to be explicitly passed as a parameter to this function because the function can directly access all the props provided to the component.
If we examine the current code, we notice that the helper function is defined within another function that determines the component's behavior. In Java programming, defining a function within another function can be complex and is uncommon. However, in JavaScript, defining functions within functions is a common and efficient practice.
### Destructuring
Before we move forward, we will take a look at a small but useful feature of the JavaScript language that was added in the ES6 specification, that allows us to 
In our previous code, we had to reference the data passed to our component as _props.name_ and _props.age_. Of these two expressions, we had to repeat _props.age_ twice in our code.
Since _props_ is an object
```
props = {
  name: 'Arto Hellas',
  age: 35,
}copy
```

we can streamline our component by assigning the values of the properties directly into two variables _name_ and _age_ which we can then use in our code:
```
const Hello = (props) => {
  const name = props.name  const age = props.age
  const bornYear = () => new Date().getFullYear() - age
  return (
    <div>
      <p>Hello {name}, you are {age} years old</p>      <p>So you were probably born in {bornYear()}</p>
    </div>
  )
}copy
```

Note that we've also utilized the more compact syntax for arrow functions when defining the _bornYear_ function. As mentioned earlier, if an arrow function consists of a single expression, then the function body does not need to be written inside of curly braces. In this more compact form, the function simply returns the result of the single expression.
To recap, the two function definitions shown below are equivalent:
```
const bornYear = () => new Date().getFullYear() - age

const bornYear = () => {
  return new Date().getFullYear() - age
}copy
```

Destructuring makes the assignment of variables even easier since we can use it to extract and gather the values of an object's properties into separate variables:
```
const Hello = (props) => {
  const { name, age } = props  const bornYear = () => new Date().getFullYear() - age

  return (
    <div>
      <p>Hello {name}, you are {age} years old</p>
      <p>So you were probably born in {bornYear()}</p>
    </div>
  )
}copy
```

When the object that we are destructuring has the values
```
props = {
  name: 'Arto Hellas',
  age: 35,
}copy
```

the expression _const { name, age } = props_ assigns the values 'Arto Hellas' to _name_ and 35 to _age_.
We can take destructuring a step further:
```
const Hello = ({ name, age }) => {  const bornYear = () => new Date().getFullYear() - age

  return (
    <div>
      <p>
        Hello {name}, you are {age} years old
      </p>
      <p>So you were probably born in {bornYear()}</p>
    </div>
  )
}copy
```

The props that are passed to the component are now directly destructured into the variables, _name_ and _age_.
This means that instead of assigning the entire props object into a variable called _props_ and then assigning its properties to the variables _name_ and _age_
```
const Hello = (props) => {
  const { name, age } = propscopy
```

we assign the values of the properties directly to variables by destructuring the props object that is passed to the component function as a parameter:
```
const Hello = ({ name, age }) => {copy
```

### Page re-rendering
Up to this point, our applications have been static — their appearance remains unchanged after the initial rendering. But what if we wanted to create a counter that increases in value, either over time or when a button is clicked?
Let's start with the following. File _App.jsx_ becomes:
```
const App = (props) => {
  const {counter} = props
  return (
    <div>{counter}</div>
  )
}

export default Appcopy
```

And file _main.jsx_ becomes:
```
import ReactDOM from 'react-dom/client'

import App from './App'

let counter = 1

ReactDOM.createRoot(document.getElementById('root')).render(
  <App counter={counter} />
)copy
```

The App component is given the value of the counter via the _counter_ prop. This component renders the value to the screen. What happens when the value of _counter_ changes? Even if we were to add the following
```
counter += 1copy
```

the component won't re-render. We can get the component to re-render by calling the _render_ method a second time, e.g. in the following way:
```
let counter = 1

const root = ReactDOM.createRoot(document.getElementById('root'))

const refresh = () => {
  root.render(
    <App counter={counter} />
  )
}

refresh()
counter += 1
refresh()
counter += 1
refresh()copy
```

The re-rendering command has been wrapped inside of the _refresh_ function to cut down on the amount of copy-pasted code.
Now the component _renders three times_ , first with the value 1, then 2, and finally 3. However, values 1 and 2 are displayed on the screen for such a short amount of time that they can't be noticed.
We can implement slightly more interesting functionality by re-rendering and incrementing the counter every second by using 
```
setInterval(() => {
  refresh()
  counter += 1
}, 1000)copy
```

Making repeated calls to the _render_ method is not the recommended way to re-render components. Next, we'll introduce a better way of accomplishing this effect.
### Stateful component
All of our components up till now have been simple in the sense that they have not contained any state that could change during the lifecycle of the component.
Next, let's add state to our application's _App_ component with the help of React's 
We will change the application as follows. _main.jsx_ goes back to:
```
import ReactDOM from 'react-dom/client'

import App from './App'

ReactDOM.createRoot(document.getElementById('root')).render(<App />)copy
```

and _App.jsx_ changes to the following:
```
import { useState } from 'react'
const App = () => {
  const [ counter, setCounter ] = useState(0)
  setTimeout(    () => setCounter(counter + 1),    1000  )
  return (
    <div>{counter}</div>
  )
}

export default Appcopy
```

In the first row, the file imports the _useState_ function:
```
import { useState } from 'react'copy
```

The function body that defines the component begins with the function call:
```
const [ counter, setCounter ] = useState(0)copy
```

The function call adds _state_ to the component and renders it initialized with the value zero. The function returns an array that contains two items. We assign the items to the variables _counter_ and _setCounter_ by using the destructuring assignment syntax shown earlier.
The _counter_ variable is assigned the initial value of _state_ , which is zero. The variable _setCounter_ is assigned a function that will be used to _modify the state_.
The application calls the 
```
setTimeout(
  () => setCounter(counter + 1),
  1000
)copy
```

The function passed as the first parameter to the _setTimeout_ function is invoked one second after calling the _setTimeout_ function
```
() => setCounter(counter + 1)copy
```

When the state modifying function _setCounter_ is called, _React re-renders the component_ which means that the function body of the component function gets re-executed:
```
() => {
  const [ counter, setCounter ] = useState(0)

  setTimeout(
    () => setCounter(counter + 1),
    1000
  )

  return (
    <div>{counter}</div>
  )
}copy
```

The second time the component function is executed it calls the _useState_ function and returns the new value of the state: 1. Executing the function body again also makes a new function call to _setTimeout_ , which executes the one-second timeout and increments the _counter_ state again. Because the value of the _counter_ variable is 1, incrementing the value by 1 is essentially the same as an expression setting the value of _counter_ to 2.
```
() => setCounter(2)copy
```

Meanwhile, the old value of _counter_ - "1" - is rendered to the screen.
Every time the _setCounter_ modifies the state it causes the component to re-render. The value of the state will be incremented again after one second, and this will continue to repeat for as long as the application is running.
If the component doesn't render when you think it should, or if it renders at the "wrong time", you can debug the application by logging the values of the component's variables to the console. If we make the following additions to our code:
```
const App = () => {
  const [ counter, setCounter ] = useState(0)

  setTimeout(
    () => setCounter(counter + 1),
    1000
  )

  console.log('rendering...', counter)
  return (
    <div>{counter}</div>
  )
}copy
```

It's easy to follow and track the calls made to the _App_ component's render function:
![screenshot of rendering log on dev tools](../assets/ccffd337b4a9a3bf.png)
Was your browser console open? If it wasn't, then promise that this was the last time you need to be reminded about it.
### Event handling
We have already mentioned the _event handlers_ that are registered to be called when specific events occur a few times in [part 0](../part0/01-part0.md). A user's interaction with the different elements of a web page can cause a collection of various kinds of events to be triggered.
Let's change the application so that increasing the counter happens when a user clicks a button, which is implemented with the 
Button elements support so-called _mouse event_.
In React, _click_ event happens like this:
```
const App = () => {
  const [ counter, setCounter ] = useState(0)

  const handleClick = () => {    console.log('clicked')  }
  return (
    <div>
      <div>{counter}</div>
      <button onClick={handleClick}>        plus      </button>    </div>
  )
}copy
```

We set the value of the button's _onClick_ attribute to be a reference to the _handleClick_ function defined in the code.
Now every click of the _plus_ button causes the _handleClick_ function to be called, meaning that every click event will log a _clicked_ message to the browser console.
The event handler function can also be defined directly in the value assignment of the onClick-attribute:
```
const App = () => {
  const [ counter, setCounter ] = useState(0)

  return (
    <div>
      <div>{counter}</div>
      <button onClick={() => console.log('clicked')}>        plus
      </button>
    </div>
  )
}copy
```

By changing the event handler to the following form
```
<button onClick={() => setCounter(counter + 1)}>
  plus
</button>copy
```

we achieve the desired behavior, meaning that the value of _counter_ is increased by one _and_ the component gets re-rendered.
Let's also add a button for resetting the counter:
```
const App = () => {
  const [ counter, setCounter ] = useState(0)

  return (
    <div>
      <div>{counter}</div>
      <button onClick={() => setCounter(counter + 1)}>
        plus
      </button>
      <button onClick={() => setCounter(0)}>         zero      </button>    </div>
  )
}copy
```

Our application is now ready!
### An event handler is a function
We define the event handlers for our buttons where we declare their _onClick_ attributes:
```
<button onClick={() => setCounter(counter + 1)}> 
  plus
</button>copy
```

What if we tried to define the event handlers in a simpler form?
```
<button onClick={setCounter(counter + 1)}> 
  plus
</button>copy
```

This would completely break our application:
![screenshot of re-renders error](../assets/73f3c922859ef532.png)
What's going on? An event handler is supposed to be either a _function_ or a _function reference_ , and when we write:
```
<button onClick={setCounter(counter + 1)}>copy
```

the event handler is actually a _function call_. In many situations this is ok, but not in this particular situation. In the beginning, the value of the _counter_ variable is 0. When React renders the component for the first time, it executes the function call _setCounter(0+1)_ , and changes the value of the component's state to 1. This will cause the component to be re-rendered, React will execute the setCounter function call again, and the state will change leading to another re-render...
Let's define the event handlers like we did before:
```
<button onClick={() => setCounter(counter + 1)}> 
  plus
</button>copy
```

Now the button's attribute which defines what happens when the button is clicked - _onClick_ - has the value _() = > setCounter(counter + 1)_. The setCounter function is called only when a user clicks the button.
Usually defining event handlers within JSX-templates is not a good idea. Here it's ok, because our event handlers are so simple.
Let's separate the event handlers into separate functions anyway:
```
const App = () => {
  const [ counter, setCounter ] = useState(0)

  const increaseByOne = () => setCounter(counter + 1)  const setToZero = () => setCounter(0)
  return (
    <div>
      <div>{counter}</div>
      <button onClick={increaseByOne}>        plus
      </button>
      <button onClick={setToZero}>        zero
      </button>
    </div>
  )
}copy
```

Here, the event handlers have been defined correctly. The value of the _onClick_ attribute is a variable containing a reference to a function:
```
<button onClick={increaseByOne}> 
  plus
</button>copy
```

### Passing state - to child components
It's recommended to write React components that are small and reusable across the application and even across projects. Let's refactor our application so that it's composed of three smaller components, one component for displaying the counter and two components for buttons.
Let's first implement a _Display_ component that's responsible for displaying the value of the counter.
One best practice in React is to 
> _Often, several components need to reflect the same changing data. We recommend lifting the shared state up to their closest common ancestor._
So let's place the application's state in the _App_ component and pass it down to the _Display_ component through _props_ :
```
const Display = (props) => {
  return (
    <div>{props.counter}</div>
  )
}copy
```

Using the component is straightforward, as we only need to pass the state of the _counter_ to it:
```
const App = () => {
  const [ counter, setCounter ] = useState(0)

  const increaseByOne = () => setCounter(counter + 1)
  const setToZero = () => setCounter(0)

  return (
    <div>
      <Display counter={counter}/>      <button onClick={increaseByOne}>
        plus
      </button>
      <button onClick={setToZero}> 
        zero
      </button>
    </div>
  )
}copy
```

Everything still works. When the buttons are clicked and the _App_ gets re-rendered, all of its children including the _Display_ component are also re-rendered.
Next, let's make a _Button_ component for the buttons of our application. We have to pass the event handler as well as the title of the button through the component's props:
```
const Button = (props) => {
  return (
    <button onClick={props.onClick}>
      {props.text}
    </button>
  )
}copy
```

Our _App_ component now looks like this:
```
const App = () => {
  const [ counter, setCounter ] = useState(0)

  const increaseByOne = () => setCounter(counter + 1)
  const decreaseByOne = () => setCounter(counter - 1)  const setToZero = () => setCounter(0)

  return (
    <div>
      <Display counter={counter}/>
      <Button        onClick={increaseByOne}        text='plus'      />      <Button        onClick={setToZero}        text='zero'      />           <Button        onClick={decreaseByOne}        text='minus'      />               </div>
  )
}copy
```

Since we now have an easily reusable _Button_ component, we've also implemented new functionality into our application by adding a button that can be used to decrement the counter.
The event handler is passed to the _Button_ component through the _onClick_ prop. When creating your own components, you can theoretically choose the prop name freely. However, our naming choice for the event handler was not entirely arbitrary.
React's own official _onSomething_ names for props which take functions which handle events and _handleSomething_ for the actual function definitions which handle those events."
### Changes in state cause re-rendering
Let's go over the main principles of how an application works once more.
When the application starts, the code in _App_ is executed. This code uses a _counter_. This component contains the _Display_ component - which displays the counter's value, 0 - and three _Button_ components. The buttons all have event handlers, which are used to change the state of the counter.
When one of the buttons is clicked, the event handler is executed. The event handler changes the state of the _App_ component with the _setCounter_ function. **Calling a function that changes the state causes the component to re-render.**
So, if a user clicks the _plus_ button, the button's event handler changes the value of _counter_ to 1, and the _App_ component is re-rendered. This causes its subcomponents _Display_ and _Button_ to also be re-rendered. _Display_ receives the new value of the counter, 1, as props. The _Button_ components receive event handlers which can be used to change the state of the counter.
To be sure to understand how the program works, let us add some _console.log_ statements to it
```
const App = () => {
  const [counter, setCounter] = useState(0)
  console.log('rendering with counter value', counter)
  const increaseByOne = () => {
    console.log('increasing, value before', counter)    setCounter(counter + 1)
  }

  const decreaseByOne = () => { 
    console.log('decreasing, value before', counter)    setCounter(counter - 1)
  }

  const setToZero = () => {
    console.log('resetting to zero, value before', counter)    setCounter(0)
  }

  return (
    <div>
      <Display counter={counter} />
      <Button onClick={increaseByOne} text="plus" />
      <Button onClick={setToZero} text="zero" />
      <Button onClick={decreaseByOne} text="minus" />
    </div>
  )
} copy
```

Let us now see what gets rendered to the console when the buttons plus, zero and minus are pressed:
![browser showing console with rendering values highlighted](../assets/24352e26096626cc.png)
Do not ever try to guess what your code does. It is just better to use _console.log_ and _see with your own eyes_ what it does.
### Refactoring the components
The component displaying the value of the counter is as follows:
```
const Display = (props) => {
  return (
    <div>{props.counter}</div>
  )
}copy
```

The component only uses the _counter_ field of its _props_. This means we can simplify the component by using [destructuring](../part1/01-component-state-event-handlers-destructuring.md), like so:
```
const Display = ({ counter }) => {
  return (
    <div>{counter}</div>
  )
}copy
```

The function defining the component contains only the return statement, so we can define the function using the more compact form of arrow functions:
```
const Display = ({ counter }) => <div>{counter}</div>copy
```

We can simplify the Button component as well.
```
const Button = (props) => {
  return (
    <button onClick={props.onClick}>
      {props.text}
    </button>
  )
}copy
```

We can use destructuring to get only the required fields from _props_ , and use the more compact form of arrow functions:
```
const Button = ({ onClick, text }) => <button onClick={onClick}>{text}</button>copy
```

This approach works because the component contains only a single return statement, making it possible to use the concise arrow function syntax.
[ Part 1b **Previous part** ](../part1/01-java-script.md)[ Part 1d **Next part** ](../part1/01-a-more-complex-state-debugging-react-apps.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)