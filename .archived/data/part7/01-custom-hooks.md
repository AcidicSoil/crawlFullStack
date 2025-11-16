---{
  "title": "Custom hooks",
  "source_url": "https://fullstackopen.com/en/part7/custom_hooks",
  "crawl_timestamp": "2025-10-04T19:16:56Z",
  "checksum": "236d690507f9727f1ceed6bcfb81fa9f7ce5fc5c902043af68b669e8b5630dc5"
}
---[Skip to content](../part7/01-custom-hooks-course-main-content.md)
[{() => fs}](https://fullstackopen.com/en/)

- [About course](../about/01-about.md)
- [Course contents](../#course-contents/01-course-contents.md)
- [FAQ](../faq/01-faq.md)
- [Partners](../companies/01-companies.md)
- [Challenge](../challenge/01-challenge.md)
[Search from the material](../search/01-search.md)Toggle dark theme
Select languageSuomi English 中文 Español Français Português(BR)

[Fullstack](../#course-contents/01-course-contents.md)
[Part 7](../part7/01-part7.md)
Custom hooks
[a React Router](../part7/01-react-router.md)
b Custom hooks

- [Hooks](../part7/01-custom-hooks-hooks.md)
- [Custom hooks](../part7/01-custom-hooks-custom-hooks.md)
- [Spread attributes](../part7/01-custom-hooks-spread-attributes.md)
- [More about hooks](../part7/01-custom-hooks-more-about-hooks.md)
- [Exercises 7.4.-7.8.](../part7/01-custom-hooks-exercises-7-4-7-8.md)


[c More about styles](../part7/01-more-about-styles.md)[d Webpack](../part7/01-webpack.md)[e Class components, Miscellaneous](../part7/01-class-components-miscellaneous.md)[f Exercises: extending the bloglist](../part7/01-exercises-extending-the-bloglist.md)
b
# Custom hooks
### Hooks
React offers 15 different
In [part 5](../part5/01-props-children-and-proptypes-references-to-components-with-ref.md) we used the [part 6](../part6/01-react-query-use-reducer-and-the-context.md) we used
Within the last couple of years, many React libraries have begun to offer hook-based APIs. [In part 6](../part6/01-flux-architecture-and-redux.md) we used the
The [previous part](../part7/01-react-router.md) is also partially hook-based. Its hooks can be used to access URL parameters and the _navigation_ object, which allows for manipulating the browser URL programmatically.
As mentioned in [part 1](../part1/01-a-more-complex-state-debugging-react-apps-rules-of-hooks.md), hooks are not normal functions, and when using these we have to adhere to certain
**Don’t call Hooks inside loops, conditions, or nested functions.** Instead, always use Hooks at the top level of your React function.
**You can only call Hooks while React is rendering a function component:**

- Call them at the top level in the body of a function component.
- Call them at the top level in the body of a custom Hook.


There's an existing
![vscode error useState being called conditionally](../assets/f00a0d1570f0c69b.png)
### Custom hooks
React offers the option to create
> _Building your own Hooks lets you extract component logic into reusable functions._
Custom hooks are regular JavaScript functions that can use any other hooks, as long as they adhere to the [rules of hooks](../part1/01-a-more-complex-state-debugging-react-apps-rules-of-hooks.md). Additionally, the name of custom hooks must start with the word _use_.
We implemented a counter application in [part 1](../part1/01-component-state-event-handlers-event-handling.md) that can have its value incremented, decremented, or reset. The code of the application is as follows:

```
import { useState } from 'react'
const App = () => {
  const [counter, setCounter] = useState(0)

  return (
    <div>
      <div>{counter}</div>
      <button onClick={() => setCounter(counter + 1)}>
        plus
      </button>
      <button onClick={() => setCounter(counter - 1)}>
        minus
      </button>      
      <button onClick={() => setCounter(0)}>
        zero
      </button>
    </div>
  )
}copy
```

Let's extract the counter logic into a custom hook. The code for the hook is as follows:

```
const useCounter = () => {
  const [value, setValue] = useState(0)

  const increase = () => {
    setValue(value + 1)
  }

  const decrease = () => {
    setValue(value - 1)
  }

  const zero = () => {
    setValue(0)
  }

  return {
    value, 
    increase,
    decrease,
    zero
  }
}copy
```

Our custom hook uses the _useState_ hook internally to create its state. The hook returns an object, the properties of which include the value of the counter as well as functions for manipulating the value.
React components can use the hook as shown below:

```
const App = () => {
  const counter = useCounter()

  return (
    <div>
      <div>{counter.value}</div>
      <button onClick={counter.increase}>
        plus
      </button>
      <button onClick={counter.decrease}>
        minus
      </button>      
      <button onClick={counter.zero}>
        zero
      </button>
    </div>
  )
}copy
```

By doing this we can extract the state of the _App_ component and its manipulation entirely into the _useCounter_ hook. Managing the counter state and logic is now the responsibility of the custom hook.
The same hook could be _reused_ in the application that was keeping track of the number of clicks made to the left and right buttons:

```
const App = () => {
  const left = useCounter()
  const right = useCounter()

  return (
    <div>
      {left.value}
      <button onClick={left.increase}>
        left
      </button>
      <button onClick={right.increase}>
        right
      </button>
      {right.value}
    </div>
  )
}copy
```

The application creates _two_ completely separate counters. The first one is assigned to the variable _left_ and the other to the variable _right_.
Dealing with forms in React is somewhat tricky. The following application presents the user with a form that requires him to input their name, birthday, and height:

```
const App = () => {
  const [name, setName] = useState('')
  const [born, setBorn] = useState('')
  const [height, setHeight] = useState('')

  return (
    <div>
      <form>
        name: 
        <input
          type='text'
          value={name}
          onChange={(event) => setName(event.target.value)} 
        /> 
        <br/> 
        birthdate:
        <input
          type='date'
          value={born}
          onChange={(event) => setBorn(event.target.value)}
        />
        <br /> 
        height:
        <input
          type='number'
          value={height}
          onChange={(event) => setHeight(event.target.value)}
        />
      </form>
      <div>
        {name} {born} {height} 
      </div>
    </div>
  )
}copy
```

Every field of the form has its own state. To keep the state of the form synchronized with the data provided by the user, we have to register an appropriate _onChange_ handler for each of the _input_ elements.
Let's define our own custom _useField_ hook that simplifies the state management of the form:

```
const useField = (type) => {
  const [value, setValue] = useState('')

  const onChange = (event) => {
    setValue(event.target.value)
  }

  return {
    type,
    value,
    onChange
  }
}copy
```

The hook function receives the type of the input field as a parameter. It returns all of the attributes required by the _input_ : its type, value and the onChange handler.
The hook can be used in the following way:

```
const App = () => {
  const name = useField('text')
  // ...

  return (
    <div>
      <form>
        <input
          type={name.type}
          value={name.value}
          onChange={name.onChange} 
        /> 
        // ...
      </form>
    </div>
  )
}copy
```

### Spread attributes
We could simplify things a bit further. Since the _name_ object has exactly all of the attributes that the _input_ element expects to receive as props, we can pass the props to the element using the

```
<input {...name} /> copy
```

As the

```
<Greeting firstName='Arto' lastName='Hellas' />

const person = {
  firstName: 'Arto',
  lastName: 'Hellas'
}

<Greeting {...person} />copy
```

The application gets simplified into the following format:

```
const App = () => {
  const name = useField('text')
  const born = useField('date')
  const height = useField('number')

  return (
    <div>
      <form>
        name: 
        <input  {...name} /> 
        <br/> 
        birthdate:
        <input {...born} />
        <br /> 
        height:
        <input {...height} />
      </form>
      <div>
        {name.value} {born.value} {height.value}
      </div>
    </div>
  )
}copy
```

Dealing with forms is greatly simplified when the unpleasant nitty-gritty details related to synchronizing the state of the form are encapsulated inside our custom hook.
Custom hooks are not only a tool for reusing code; they also provide a better way for dividing it into smaller modular parts.
### More about hooks
The internet is starting to fill up with more and more helpful material related to hooks. The following sources are worth checking out:
### Exercises 7.4.-7.8
We'll continue with the app from the [exercises](../part7/01-react-router-exercises-7-1-7-3.md) of the [react router](../part7/01-react-router.md) chapter.
#### 7.4: Anecdotes and Hooks step 1
Simplify the anecdote creation form of your application with the _useField_ custom hook we defined earlier.
One natural place to save the custom hooks of your application is in the _/src/hooks/index.js_ file.
If you use the

```
import { useState } from 'react'

export const useField = (type) => {  const [value, setValue] = useState('')

  const onChange = (event) => {
    setValue(event.target.value)
  }

  return {
    type,
    value,
    onChange
  }
}

// modules can have several named exports
export const useAnotherHook = () => {  // ...
}copy
```

Then

```
import  { useField } from './hooks'

const App = () => {
  // ...
  const username = useField('text')
  // ...
}copy
```

#### 7.5: Anecdotes and Hooks step 2
Add a button to the form that you can use to clear all the input fields:
![browser anecdotes with reset button](../assets/8e97bccc992bdfc9.png)
Expand the functionality of the _useField_ hook so that it offers a new _reset_ operation for clearing the field.
Depending on your solution, you may see the following warning in your console:
![devtools console warning invalid value for reset prop](../assets/389d0c6d85fb2dd6.png)
We will return to this warning in the next exercise.
#### 7.6: Anecdotes and Hooks step 3
If your solution did not cause a warning to appear in the console, you have already finished this exercise.
If you see the _Invalid value for prop `reset` on <input> tag_ warning in the console, make the necessary changes to get rid of it.
The reason for this warning is that after making the changes to your application, the following expression:

```
<input {...content}/>copy
```

Essentially, is the same as this:

```
<input
  value={content.value} 
  type={content.type}
  onChange={content.onChange}
  reset={content.reset}/>copy
```

The _input_ element should not be given a _reset_ attribute.
One simple fix would be to not use the spread syntax and write all of the forms like this:

```
<input
  value={username.value} 
  type={username.type}
  onChange={username.onChange}
/>copy
```

If we were to do this, we would lose much of the benefit provided by the _useField_ hook. Instead, come up with a solution that fixes the issue, but is still easy to use with the spread syntax.
#### 7.7: Country hook
Let's return to exercises [2.18-2.20](../part2/01-adding-styles-to-react-app-exercises-2-18-2-20.md).
Use the code from
The application can be used to search for a country's details from the service in
![browser displaying country details](../assets/4d0f322270e8ccb5.png)
If no country is found, a message is displayed to the user:
![browser showing country not found](../assets/38add80b7375ad88.png)
The application is otherwise complete, but in this exercise, you have to implement a custom hook _useCountry_ , which can be used to search for the details of the country given to the hook as a parameter.
Use the API endpoint _useEffect_ hook within your custom hook.
Note that in this exercise it is essential to use useEffect's [part 2](../part2/01-adding-styles-to-react-app-couple-of-important-remarks.md) for more info how the second parameter could be used.
#### 7.8: Ultimate Hooks
The code of the application responsible for communicating with the backend of the note application of the previous parts looks like this:

```
import axios from 'axios'
const baseUrl = '/api/notes'

let token = null

const setToken = newToken => {
  token = `bearer ${newToken}`
}

const getAll = async () => {
  const response = await axios.get(baseUrl)
  return response.data
}

const create = async newObject => {
  const config = {
    headers: { Authorization: token },
  }

  const response = await axios.post(baseUrl, newObject, config)
  return response.data
}

const update = async (id, newObject) => {
  const response = await axios.put(`${ baseUrl }/${id}`, newObject)
  return response.data
}

export default { getAll, create, update, setToken }copy
```

We notice that the code is in no way specific to the fact that our application deals with notes. Excluding the value of the _baseUrl_ variable, the same code could be reused in the blog post application for dealing with the communication with the backend.
Extract the code for communicating with the backend into its own _useResource_ hook. It is sufficient to implement fetching all resources and creating a new resource.
You can do the exercise in the project found in the _App_ component for the project is the following:

```
const App = () => {
  const content = useField('text')
  const name = useField('text')
  const number = useField('text')

  const [notes, noteService] = useResource('http://localhost:3005/notes')
  const [persons, personService] = useResource('http://localhost:3005/persons')

  const handleNoteSubmit = (event) => {
    event.preventDefault()
    noteService.create({ content: content.value })
  }
 
  const handlePersonSubmit = (event) => {
    event.preventDefault()
    personService.create({ name: name.value, number: number.value})
  }

  return (
    <div>
      <h2>notes</h2>
      <form onSubmit={handleNoteSubmit}>
        <input {...content} />
        <button>create</button>
      </form>
      {notes.map(n => <p key={n.id}>{n.content}</p>)}

      <h2>persons</h2>
      <form onSubmit={handlePersonSubmit}>
        name <input {...name} /> <br/>
        number <input {...number} />
        <button>create</button>
      </form>
      {persons.map(n => <p key={n.id}>{n.name} {n.number}</p>)}
    </div>
  )
}copy
```

The _useResource_ custom hook returns an array of two items just like the state hooks. The first item of the array contains all of the individual resources and the second item of the array is an object that can be used for manipulating the resource collection, like creating new ones.
If you implement the hook correctly, it can be used for both notes and persons (start the server with the _npm run server_ command at port 3005).
![browser showing notes and persons](../assets/87a25a319d316d0b.png)
[Part 7a **Previous part**](../part7/01-react-router.md)[Part 7c **Next part**](../part7/01-more-about-styles.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)
