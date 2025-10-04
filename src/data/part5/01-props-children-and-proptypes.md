---{
  "title": "props.children and proptypes",
  "source_url": "https://fullstackopen.com/en/part5/props_children_and_proptypes",
  "crawl_timestamp": "2025-10-04T19:16:44Z",
  "checksum": "07b380e785074ab5b028fb0de6db91b8569d6acded96cde4277de84bb8dc8034"
}
---[Skip to content](../part5/01-props-children-and-proptypes-course-main-content.md)
[{() => fs}](https://fullstackopen.com/en/)

- [About course](../about/01-about.md)
- [Course contents](../#course-contents/01-course-contents.md)
- [FAQ](../faq/01-faq.md)
- [Partners](../companies/01-companies.md)
- [Challenge](../challenge/01-challenge.md)
[Search from the material](../search/01-search.md)Toggle dark theme
Select languageSuomi English 中文 Español Français Português(BR)

[Fullstack](../#course-contents/01-course-contents.md)
[Part 5](../part5/01-part5.md)
props.children and proptypes
[a Login in frontend](../part5/01-login-in-frontend.md)
b props.children and proptypes

- [Displaying the login form only when appropriate](../part5/01-props-children-and-proptypes-displaying-the-login-form-only-when-appropriate.md)
- [The components children, aka. props.children](../part5/01-props-children-and-proptypes-the-components-children-aka-props-children.md)
- [State of the forms](../part5/01-props-children-and-proptypes-state-of-the-forms.md)
- [References to components with ref](../part5/01-props-children-and-proptypes-references-to-components-with-ref.md)
- [One point about components](../part5/01-props-children-and-proptypes-one-point-about-components.md)
- [The updated full stack developer's oath](../part5/01-props-children-and-proptypes-the-updated-full-stack-developers-oath.md)
- [Exercises 5.5.-5.11.](../part5/01-props-children-and-proptypes-exercises-5-5-5-11.md)
- [ESlint](../part5/01-props-children-and-proptypes-e-slint.md)
- [Exercise 5.12.](../part5/01-props-children-and-proptypes-exercise-5-12.md)


[c Testing React apps](../part5/01-testing-react-apps.md)[d End to end testing: Playwright](../part5/01-end-to-end-testing-playwright.md)[e End to end testing: Cypress](../part5/01-end-to-end-testing-cypress.md)
b
# props.children and proptypes
### Displaying the login form only when appropriate
Let's modify the application so that the login form is not displayed by default:
![browser showing log in button by default](../assets/76a04b9461d229a1.png)
The login form appears when the user presses the _login_ button:
![user at login screen about to press cancel](../assets/ebf74fac97ed39b4.png)
The user can close the login form by clicking the _cancel_ button.
Let's start by extracting the login form into its own component:

```
const LoginForm = ({
   handleSubmit,
   handleUsernameChange,
   handlePasswordChange,
   username,
   password
  }) => {
  return (
    <div>
      <h2>Login</h2>

      <form onSubmit={handleSubmit}>
        <div>
          username
          <input
            value={username}
            onChange={handleUsernameChange}
          />
        </div>
        <div>
          password
          <input
            type="password"
            value={password}
            onChange={handlePasswordChange}
          />
      </div>
        <button type="submit">login</button>
      </form>
    </div>
  )
}

export default LoginFormcopy
```

The state and all the functions related to it are defined outside of the component and are passed to the component as props.
Notice that the props are assigned to variables through _destructuring_ , which means that instead of writing:

```
const LoginForm = (props) => {
  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={props.handleSubmit}>
        <div>
          username
          <input
            value={props.username}
            onChange={props.handleChange}
            name="username"
          />
        </div>
        // ...
        <button type="submit">login</button>
      </form>
    </div>
  )
}copy
```

where the properties of the _props_ object are accessed through e.g. _props.handleSubmit_ , the properties are assigned directly to their own variables.
One fast way of implementing the functionality is to change the _loginForm_ function of the _App_ component like so:

```
const App = () => {
  const [loginVisible, setLoginVisible] = useState(false)
  // ...

  const loginForm = () => {
    const hideWhenVisible = { display: loginVisible ? 'none' : '' }
    const showWhenVisible = { display: loginVisible ? '' : 'none' }

    return (
      <div>
        <div style={hideWhenVisible}>
          <button onClick={() => setLoginVisible(true)}>log in</button>
        </div>
        <div style={showWhenVisible}>
          <LoginForm
            username={username}
            password={password}
            handleUsernameChange={({ target }) => setUsername(target.value)}
            handlePasswordChange={({ target }) => setPassword(target.value)}
            handleSubmit={handleLogin}
          />
          <button onClick={() => setLoginVisible(false)}>cancel</button>
        </div>
      </div>
    )
  }

  // ...
}copy
```

The _App_ component state now contains the boolean _loginVisible_ , which defines if the login form should be shown to the user or not.
The value of _loginVisible_ is toggled with two buttons. Both buttons have their event handlers defined directly in the component:

```
<button onClick={() => setLoginVisible(true)}>log in</button>

<button onClick={() => setLoginVisible(false)}>cancel</button>copy
```

The visibility of the component is defined by giving the component an [inline](../part2/01-adding-styles-to-react-app-inline-styles.md) style rule, where the value of the _none_ if we do not want the component to be displayed:

```
const hideWhenVisible = { display: loginVisible ? 'none' : '' }
const showWhenVisible = { display: loginVisible ? '' : 'none' }

<div style={hideWhenVisible}>
  // button
</div>

<div style={showWhenVisible}>
  // button
</div>copy
```

We are once again using the "question mark" ternary operator. If _loginVisible_ is _true_ , then the CSS rule of the component will be:

```
display: 'none';copy
```

If _loginVisible_ is _false_ , then _display_ will not receive any value related to the visibility of the component.
### The components children, aka. props.children
The code related to managing the visibility of the login form could be considered to be its own logical entity, and for this reason, it would be good to extract it from the _App_ component into a separate component.
Our goal is to implement a new _Togglable_ component that can be used in the following way:

```
<Togglable buttonLabel='login'>
  <LoginForm
    username={username}
    password={password}
    handleUsernameChange={({ target }) => setUsername(target.value)}
    handlePasswordChange={({ target }) => setPassword(target.value)}
    handleSubmit={handleLogin}
  />
</Togglable>copy
```

The way that the component is used is slightly different from our previous components. The component has both opening and closing tags that surround a _LoginForm_ component. In React terminology _LoginForm_ is a child component of _Togglable_.
We can add any React elements we want between the opening and closing tags of _Togglable_ , like this for example:

```
<Togglable buttonLabel="reveal">
  <p>this line is at start hidden</p>
  <p>also this is hidden</p>
</Togglable>copy
```

The code for the _Togglable_ component is shown below:

```
import { useState } from 'react'

const Togglable = (props) => {
  const [visible, setVisible] = useState(false)

  const hideWhenVisible = { display: visible ? 'none' : '' }
  const showWhenVisible = { display: visible ? '' : 'none' }

  const toggleVisibility = () => {
    setVisible(!visible)
  }

  return (
    <div>
      <div style={hideWhenVisible}>
        <button onClick={toggleVisibility}>{props.buttonLabel}</button>
      </div>
      <div style={showWhenVisible}>
        {props.children}
        <button onClick={toggleVisibility}>cancel</button>
      </div>
    </div>
  )
}

export default Togglablecopy
```

The new and interesting part of the code is
This time the children are rendered in the code that is used for rendering the component itself:

```
<div style={showWhenVisible}>
  {props.children}
  <button onClick={toggleVisibility}>cancel</button>
</div>copy
```

Unlike the "normal" props we've seen before, _children_ is automatically added by React and always exists. If a component is defined with an automatically closing _/ >_ tag, like this:

```
<Note
  key={note.id}
  note={note}
  toggleImportance={() => toggleImportanceOf(note.id)}
/>copy
```

Then _props.children_ is an empty array.
The _Togglable_ component is reusable and we can use it to add similar visibility toggling functionality to the form that is used for creating new notes.
Before we do that, let's extract the form for creating notes into a component:

```
const NoteForm = ({ onSubmit, handleChange, value}) => {
  return (
    <div>
      <h2>Create a new note</h2>

      <form onSubmit={onSubmit}>
        <input
          value={value}
          onChange={handleChange}
        />
        <button type="submit">save</button>
      </form>
    </div>
  )
}copy
```

Next let's define the form component inside of a _Togglable_ component:

```
<Togglable buttonLabel="new note">
  <NoteForm
    onSubmit={addNote}
    value={newNote}
    handleChange={handleNoteChange}
  />
</Togglable>copy
```

You can find the code for our current application in its entirety in the _part5-4_ branch of
### State of the forms
The state of the application currently is in the _App_ component.
React documentation says the
_Sometimes, you want the state of two components to always change together. To do it, remove state from both of them, move it to their closest common parent, and then pass it down to them via props. This is known as lifting state up, and it’s one of the most common things you will do writing React code._
If we think about the state of the forms, so for example the contents of a new note before it has been created, the _App_ component does not need it for anything. We could just as well move the state of the forms to the corresponding components.
The component for creating a new note changes like so:

```
import { useState } from 'react'

const NoteForm = ({ createNote }) => {
  const [newNote, setNewNote] = useState('')

  const addNote = (event) => {
    event.preventDefault()
    createNote({
      content: newNote,
      important: true
    })

    setNewNote('')
  }

  return (
    <div>
      <h2>Create a new note</h2>

      <form onSubmit={addNote}>
        <input
          value={newNote}
          onChange={event => setNewNote(event.target.value)}
        />
        <button type="submit">save</button>
      </form>
    </div>
  )
}

export default NoteFormcopy
```

**NOTE** At the same time, we changed the behavior of the application so that new notes are important by default, i.e. the field _important_ gets the value _true_.
The _newNote_ state variable and the event handler responsible for changing it have been moved from the _App_ component to the component responsible for the note form.
There is only one prop left, the _createNote_ function, which the form calls when a new note is created.
The _App_ component becomes simpler now that we have got rid of the _newNote_ state and its event handler. The _addNote_ function for creating new notes receives a new note as a parameter, and the function is the only prop we send to the form:

```
const App = () => {
  // ...
  const addNote = (noteObject) => {    noteService
      .create(noteObject)
      .then(returnedNote => {
        setNotes(notes.concat(returnedNote))
      })
  }
  // ...
  const noteForm = () => (
    <Togglable buttonLabel='new note'>
      <NoteForm createNote={addNote} />
    </Togglable>
  )

  // ...
}copy
```

We could do the same for the log in form, but we'll leave that for an optional exercise.
The application code can be found on _part5-5_.
### References to components with ref
Our current implementation is quite good; it has one aspect that could be improved.
After a new note is created, it would make sense to hide the new note form. Currently, the form stays visible. There is a slight problem with hiding it, the visibility is controlled with the _visible_ state variable inside of the _Togglable_ component.
One solution to this would be to move control of the Togglable component's state outside the component. However, we won't do that now, because we want the component to be responsible for its own state. So we have to find another solution, and find a mechanism to change the state of the component externally.
There are several different ways to implement access to a component's functions from outside the component, but let's use the
Let's make the following changes to the _App_ component:

```
import { useState, useEffect, useRef } from 'react'
const App = () => {
  // ...
  const noteFormRef = useRef()
  const noteForm = () => (
    <Togglable buttonLabel='new note' ref={noteFormRef}>      <NoteForm createNote={addNote} />
    </Togglable>
  )

  // ...
}copy
```

The _noteFormRef_ reference, that is assigned to the _Togglable_ component containing the creation note form. The _noteFormRef_ variable acts as a reference to the component. This hook ensures the same reference (ref) that is kept throughout re-renders of the component.
We also make the following changes to the _Togglable_ component:

```
import { useState, useImperativeHandle } from 'react'
const Togglable = (props) => {  const [visible, setVisible] = useState(false)

  const hideWhenVisible = { display: visible ? 'none' : '' }
  const showWhenVisible = { display: visible ? '' : 'none' }

  const toggleVisibility = () => {
    setVisible(!visible)
  }

  useImperativeHandle(props.ref, () => {    return { toggleVisibility }  })
  return (
    <div>
      <div style={hideWhenVisible}>
        <button onClick={toggleVisibility}>{props.buttonLabel}</button>
      </div>
      <div style={showWhenVisible}>
        {props.children}
        <button onClick={toggleVisibility}>cancel</button>
      </div>
    </div>
  )
}

export default Togglablecopy
```

The component uses the _toggleVisibility_ function available outside of the component.
We can now hide the form by calling _noteFormRef.current.toggleVisibility()_ after a new note has been created:

```
const App = () => {
  // ...
  const addNote = (noteObject) => {
    noteFormRef.current.toggleVisibility()    noteService
      .create(noteObject)
      .then(returnedNote => {     
        setNotes(notes.concat(returnedNote))
      })
  }
  // ...
}copy
```

To recap, the
This trick works for changing the state of a component, but it looks a bit unpleasant. We could have accomplished the same functionality with slightly cleaner code using "old React" class-based components. We will take a look at these class components during part 7 of the course material. So far this is the only situation where using React hooks leads to code that is not cleaner than with class components.
There are also
You can find the code for our current application in its entirety in the _part5-6_ branch of
### One point about components
When we define a component in React:

```
const Togglable = () => ...
  // ...
}copy
```

And use it like this:

```
<div>
  <Togglable buttonLabel="1" ref={togglable1}>
    first
  </Togglable>

  <Togglable buttonLabel="2" ref={togglable2}>
    second
  </Togglable>

  <Togglable buttonLabel="3" ref={togglable3}>
    third
  </Togglable>
</div>copy
```

We create _three separate instances of the component_ that all have their separate state:
![browser of three togglable components](../assets/a05d63b80496284a.png)
The _ref_ attribute is used for assigning a reference to each of the components in the variables _togglable1_ , _togglable2_ and _togglable3_.
### The updated full stack developer's oath
The number of moving parts increases. At the same time, the likelihood of ending up in a situation where we are looking for a bug in the wrong place increases. So we need to be even more systematic.
So we should once more extend our oath:
Full stack development is _extremely hard_ , that is why I will use all the possible means to make it easier

- I will have my browser developer console open all the time
- I will use the network tab of the browser dev tools to ensure that frontend and backend are communicating as I expect
- I will constantly keep an eye on the state of the server to make sure that the data sent there by the frontend is saved there as I expect
- I will keep an eye on the database: does the backend save data there in the right format
- I progress with small steps
- _when I suspect that there is a bug in the frontend, I'll make sure that the backend works as expected_
- _when I suspect that there is a bug in the backend, I'll make sure that the frontend works as expected_
- I will write lots of _console.log_ statements to make sure I understand how the code and the tests behave and to help pinpoint problems
- If my code does not work, I will not write more code. Instead, I'll start deleting it until it works or will just return to a state where everything was still working
- If a test does not pass, I'll make sure that the tested functionality works properly in the application
- When I ask for help in the course Discord channel or elsewhere I formulate my questions properly, see [here](../part0/01-general-info-how-to-get-help-in-discord.md) how to ask for help


### Exercises 5.5.-5.11
#### 5.5 Blog List Frontend, step 5
Change the form for creating blog posts so that it is only displayed when appropriate. Use functionality similar to what was shown [earlier in this part of the course material](../part5/01-props-children-and-proptypes-displaying-the-login-form-only-when-appropriate.md). If you wish to do so, you can use the _Togglable_ component defined in part 5.
By default the form is not visible
![browser showing new note button with no form](../assets/9b00d01f4d171f47.png)
It expands when button _create new blog_ is clicked
![browser showing form with create new](../assets/be3c6f18517e10a3.png)
The form hides again after a new blog is created or the _cancel_ button is pressed.
#### 5.6 Blog List Frontend, step 6
Separate the form for creating a new blog into its own component (if you have not already done so), and move all the states required for creating a new blog to this component.
The component must work like the _NoteForm_ component from the [material](../part5/01-props-children-and-proptypes-state-of-the-forms.md) of this part.
#### 5.7 Blog List Frontend, step 7
Let's add a button to each blog, which controls whether all of the details about the blog are shown or not.
Full details of the blog open when the button is clicked.
![browser showing full details of a blog with others just having view buttons](../assets/88caff38d168cc82.png)
And the details are hidden when the button is clicked again.
At this point, the _like_ button does not need to do anything.
The application shown in the picture has a bit of additional CSS to improve its appearance.
It is easy to add styles to the application as shown in part 2 using [inline](../part2/01-adding-styles-to-react-app-inline-styles.md) styles:

```
const Blog = ({ blog }) => {
  const blogStyle = {
    paddingTop: 10,
    paddingLeft: 2,
    border: 'solid',
    borderWidth: 1,
    marginBottom: 5
  }

  return (
    <div style={blogStyle}>      <div>
        {blog.title} {blog.author}
      </div>
      // ...
  </div>
)}copy
```

**NB:** Even though the functionality implemented in this part is almost identical to the functionality provided by the _Togglable_ component, it can't be used directly to achieve the desired behavior. The easiest solution would be to add a state to the blog component that controls if the details are being displayed or not.
#### 5.8: Blog List Frontend, step 8
Implement the functionality for the like button. Likes are increased by making an HTTP _PUT_ request to the unique address of the blog post in the backend.
Since the backend operation replaces the entire blog post, you will have to send all of its fields in the request body. If you wanted to add a like to the following blog post:

```
{
  _id: "5a43fde2cbd20b12a2c34e91",
  user: {
    _id: "5a43e6b6c37f3d065eaaa581",
    username: "mluukkai",
    name: "Matti Luukkainen"
  },
  likes: 0,
  author: "Joel Spolsky",
  title: "The Joel Test: 12 Steps to Better Code",
  url: "https://www.joelonsoftware.com/2000/08/09/the-joel-test-12-steps-to-better-code/"
},copy
```

You would have to make an HTTP PUT request to the address _/api/blogs/5a43fde2cbd20b12a2c34e91_ with the following request data:

```
{
  user: "5a43e6b6c37f3d065eaaa581",
  likes: 1,
  author: "Joel Spolsky",
  title: "The Joel Test: 12 Steps to Better Code",
  url: "https://www.joelonsoftware.com/2000/08/09/the-joel-test-12-steps-to-better-code/"
}copy
```

The backend has to be updated too to handle the user reference.
#### 5.9: Blog List Frontend, step 9
We notice that something is wrong. When a blog is liked in the app, the name of the user that added the blog is not shown in its details:
![browser showing missing name underneath like button](../assets/5a1d23485ed27c78.png)
When the browser is reloaded, the information of the person is displayed. This is not acceptable, find out where the problem is and make the necessary correction.
Of course, it is possible that you have already done everything correctly and the problem does not occur in your code. In that case, you can move on.
#### 5.10: Blog List Frontend, step 10
Modify the application to sort the blog posts by the number of _likes_. The Sorting can be done with the array
#### 5.11: Blog List Frontend, step 11
Add a new button for deleting blog posts. Also, implement the logic for deleting blog posts in the frontend.
Your application could look something like this:
![browser of confirmation of blog removal](../assets/053e5629eeb5742f.png)
The confirmation dialog for deleting a blog post is easy to implement with the
Show the button for deleting a blog post only if the blog post was added by the user.
### ESlint
In part 3 we configured the [ESlint](../part3/01-validation-and-es-lint-lint.md) code style tool to the backend. Let's take ESlint to use in the frontend as well.
Vite has installed ESlint to the project by default, so all that's left for us to do is define our desired configuration in the _eslint.config.js_ file.
Let's create a _eslint.config.js_ file with the following contents:

```
import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'

export default [
  { ignores: ['dist'] },
  {
    files: ['**/*.{js,jsx}'],
    languageOptions: {
      ecmaVersion: 2020,
      globals: globals.browser,
      parserOptions: {
        ecmaVersion: 'latest',
        ecmaFeatures: { jsx: true },
        sourceType: 'module'
      }
    },
    plugins: {
      'react-hooks': reactHooks,
      'react-refresh': reactRefresh
    },
    rules: {
      ...js.configs.recommended.rules,
      ...reactHooks.configs.recommended.rules,
      'no-unused-vars': ['error', { varsIgnorePattern: '^[A-Z_]' }],
      'react-refresh/only-export-components': [
        'warn',
        { allowConstantExport: true }
      ],      indent: ['error', 2],      'linebreak-style': ['error', 'unix'],      quotes: ['error', 'single'],      semi: ['error', 'never'],      eqeqeq: 'error',      'no-trailing-spaces': 'error',      'object-curly-spacing': ['error', 'always'],      'arrow-spacing': ['error', { before: true, after: true }],      'no-console': 'off'    }
  }
]copy
```

NOTE: If you are using Visual Studio Code together with ESLint plugin, you might need to add a workspace setting for it to work. If you are seeing _Failed to load plugin react: Cannot find module 'eslint-plugin-react'_ additional configuration is needed. Adding the following line to settings.json may help:

```
"eslint.workingDirectories": [{ "mode": "auto" }]copy
```

See
As usual, you can perform the linting either from the command line with the command

```
npm run lintcopy
```

or using the editor's Eslint plugin.
You can find the code for our current application in its entirety in the _part5-7_ branch of
### Exercise 5.12
#### 5.12: Blog List Frontend, step 12
Add ESlint to the project. Define the configuration according to your liking. Fix all of the linter errors.
Vite has installed ESlint to the project by default, so all that's left for you to do is define your desired configuration in the _eslint.config.js_ file.
[Part 5a **Previous part**](../part5/01-login-in-frontend.md)[Part 5c **Next part**](../part5/01-testing-react-apps.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)
