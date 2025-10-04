---{
  "title": "Login in frontend",
  "source_url": "https://fullstackopen.com/en/part5/login_in_frontend",
  "crawl_timestamp": "2025-10-04T19:16:42Z",
  "checksum": "8c7b1a29f7e86aa60e73ddeb7d9c85d5c3bca57935105d436809b47a3820d5e6"
}
---[Skip to content](../part5/01-login-in-frontend-course-main-content.md)
[{() => fs}](https://fullstackopen.com/en/)
  * [About course](../about/01-about.md)
  * [Course contents](../#course-contents/01-course-contents.md)
  * [FAQ](../faq/01-faq.md)
  * [Partners](../companies/01-companies.md)
  * [Challenge](../challenge/01-challenge.md)
[Search from the material](../search/01-search.md)Toggle dark theme
Select languageSuomi English 中文 Español Français Português(BR) 

[Fullstack](../#course-contents/01-course-contents.md)
[Part 5](../part5/01-part5.md)
Login in frontend
a Login in frontend
  * [Adding a Login Form](../part5/01-login-in-frontend-adding-a-login-form.md)
  * [Adding Logic to the Login Form](../part5/01-login-in-frontend-adding-logic-to-the-login-form.md)
  * [Conditional Rendering of the Login Form](../part5/01-login-in-frontend-conditional-rendering-of-the-login-form.md)
  * [Note on Using the Label Element](../part5/01-login-in-frontend-note-on-using-the-label-element.md)
  * [Creating new notes](../part5/01-login-in-frontend-creating-new-notes.md)
  * [Saving the token to the browser's local storage](../part5/01-login-in-frontend-saving-the-token-to-the-browsers-local-storage.md)
  * [Exercises 5.1.-5.4.](../part5/01-login-in-frontend-exercises-5-1-5-4.md)
  * [A note on using local storage](../part5/01-login-in-frontend-a-note-on-using-local-storage.md)


[b props.children and proptypes](../part5/01-props-children-and-proptypes.md)[c Testing React apps](../part5/01-testing-react-apps.md)[d End to end testing: Playwright](../part5/01-end-to-end-testing-playwright.md)[e End to end testing: Cypress](../part5/01-end-to-end-testing-cypress.md)
a
# Login in frontend
In the last two parts, we have mainly concentrated on the backend. The frontend that we developed in [part 2](../part2/01-part2.md) does not yet support the user management we implemented to the backend in part 4.
At the moment the frontend shows existing notes and lets users change the state of a note from important to not important and vice versa. New notes cannot be added anymore because of the changes made to the backend in part 4: the backend now expects that a token verifying a user's identity is sent with the new note.
We'll now implement a part of the required user management functionality in the frontend. Let's begin with the user login. Throughout this part, we will assume that new users will not be added from the frontend.
### Adding a Login Form
A login form has now been added to the top of the page:
![browser showing user login for notes](../assets/f8eb1c317a05d55f.png)
The code of the _App_ component now looks as follows:
```
const App = () => {
  const [notes, setNotes] = useState([]) 
  const [newNote, setNewNote] = useState('')
  const [showAll, setShowAll] = useState(true)
  const [errorMessage, setErrorMessage] = useState(null)
  const [username, setUsername] = useState('')   const [password, setPassword] = useState('') 
  useEffect(() => {
    noteService
      .getAll().then(initialNotes => {
        setNotes(initialNotes)
      })
  }, [])

  // ...

  const handleLogin = (event) => {    event.preventDefault()    console.log('logging in with', username, password)  }
  return (
    <div>
      <h1>Notes</h1>
      <Notification message={errorMessage} />
      
      <h2>Login</h2>      <form onSubmit={handleLogin}>        <div>          <label>            username            <input              type="text"              value={username}              onChange={({ target }) => setUsername(target.value)}            />          </label>        </div>        <div>          <label>            password            <input              type="password"              value={password}              onChange={({ target }) => setPassword(target.value)}            />          </label>        </div>        <button type="submit">login</button>      </form>
      // ...
    </div>
  )
}

export default Appcopy
```

The current application code can be found on _part5-1_. If you clone the repo, don't forget to run _npm install_ before attempting to run the frontend.
The frontend will not display any notes if it's not connected to the backend. You can start the backend with _npm run dev_ in its folder from Part 4. This will run the backend on port 3001. While that is active, in a separate terminal window you can start the frontend with _npm run dev_ , and now you can see the notes that are saved in your MongoDB database from Part 4.
Keep this in mind from now on.
The login form is handled the same way we handled forms in [part 2](../part2/01-forms.md). The app state has fields for _username_ and _password_ to store the data from the form. The form fields have event handlers, which synchronize changes in the field to the state of the _App_ component. The event handlers are simple: An object is given to them as a parameter, and they destructure the field _target_ from the object and save its value to the state.
```
({ target }) => setUsername(target.value)copy
```

The method _handleLogin_ , which is responsible for handling the data in the form, is yet to be implemented.
### Adding Logic to the Login Form
Logging in is done by sending an HTTP POST request to the server address _api/login_. Let's separate the code responsible for this request into its own module, to file _services/login.js_.
We'll use _async/await_ syntax instead of promises for the HTTP request:
```
import axios from 'axios'
const baseUrl = '/api/login'

const login = async credentials => {
  const response = await axios.post(baseUrl, credentials)
  return response.data
}

export default { login }copy
```

The method for handling the login can be implemented as follows:
```
import loginService from './services/login'
const App = () => {
  // ...
  const [username, setUsername] = useState('') 
  const [password, setPassword] = useState('') 
  const [user, setUser] = useState(null)
  // ...

  const handleLogin = async event => {    event.preventDefault()
    
    try {      const user = await loginService.login({ username, password })      setUser(user)      setUsername('')      setPassword('')    } catch {      setErrorMessage('wrong credentials')      setTimeout(() => {        setErrorMessage(null)      }, 5000)    }  }

  // ...
}copy
```

If the login is successful, the form fields are emptied _and_ the server response (including a _token_ and the user details) is saved to the _user_ field of the application's state.
If the login fails or running the function _loginService.login_ results in an error, the user is notified.
### Conditional Rendering of the Login Form
The user is not notified about a successful login in any way. Let's modify the application to show the login form only _if the user is not logged-in_ , so when _user === null_. The form for adding new notes is shown only if the _user is logged-in_ , so when _user_ state contains the user's details.
Let's add two helper functions to the _App_ component for generating the forms:
```
const App = () => {
  // ...

  const loginForm = () => (
    <form onSubmit={handleLogin}>
      <div>
        <label>
          username
          <input
            type="text"
            value={username}
            onChange={({ target }) => setUsername(target.value)}
          />
        </label>
      </div>
      <div>
        <label>
          password
          <input
            type="password"
            value={password}
            onChange={({ target }) => setPassword(target.value)}
          />
        </label>
      </div>
      <button type="submit">login</button>
    </form>
  )

  const noteForm = () => (
    <form onSubmit={addNote}>
      <input value={newNote} onChange={handleNoteChange} />
      <button type="submit">save</button>
    </form>
  )

  return (
    // ...
  )
}copy
```

and conditionally render them:
```
const App = () => {
  // ...

  const loginForm = () => (
    // ...
  )

  const noteForm = () => (
    // ...
  )

  return (
    <div>
      <h1>Notes</h1>
      <Notification message={errorMessage} />

      {!user && loginForm()}      {user && noteForm()}
      <div>
        <button onClick={() => setShowAll(!showAll)}>
          show {showAll ? 'important' : 'all'}
        </button>
      </div>
      <ul>
        {notesToShow.map(note => (
          <Note
            key={note.id}
            note={note}
            toggleImportance={() => toggleImportanceOf(note.id)}
          />
        ))}
      </ul>

      <Footer />
    </div>
  )
}copy
```

A slightly odd looking, but commonly used 
```
{!user && loginForm()}copy
```

If the first statement evaluates to false or is 
Let's do one more modification. If the user is logged in, their name is shown on the screen:
```
return (
  <div>
    <h1>Notes</h1>
    <Notification message={errorMessage} />

    {!user && loginForm()}
    {user && (      <div>        <p>{user.name} logged in</p>        {noteForm()}      </div>    )}
    <div>
      <button onClick={() => setShowAll(!showAll)}>
    // ...copy
```

The solution isn't perfect, but we'll leave it like this for now.
Our main component _App_ is at the moment way too large. The changes we did now are a clear sign that the forms should be refactored into their own components. However, we will leave that for an optional exercise.
The current application code can be found on _part5-2_.
### Note on Using the Label Element
We used the _input_ fields in the login form. The _input_ field for the username is placed inside the corresponding _label_ element:
```
<div>
  <label>
    username
    <input
      type="text"
      value={username}
      onChange={({ target }) => setUsername(target.value)}
    />
  </label>
</div>
// ...copy
```

Why did we implement the form this way? Visually, the same result could be achieved with simpler code, without a separate _label_ element:
```
<div>
  username
  <input
    type="text"
    value={username}
    onChange={({ target }) => setUsername(target.value)}
  />
</div>
// ...copy
```

The _label_ element is used in forms to describe and name _input_ fields. It provides a description for the input field, helping the user understand what information should be entered into each field. This description is programmatically linked to the corresponding input field, improving the form's accessibility. 
This way, screen readers can read the field's name to the user when the input field is selected, and clicking on the label's text automatically focuses on the correct input field. Using the _label_ element with _input_ fields is always recommended, even if the same visual result could be achieved without it.
There are _label_ to an _input_ element. The easiest method is to place the _input_ element inside the corresponding _label_ element, as demonstrated in this material. This automatically associates the _label_ with the correct input field, requiring no additional configuration.
### Creating new notes
The token returned with a successful login is saved to the application's state - the _user_ 's field _token_ :
```
const handleLogin = async (event) => {
  event.preventDefault()
  try {
    const user = await loginService.login({
      username, password,
    })

    setUser(user)    setUsername('')
    setPassword('')
  } catch (exception) {
    // ...
  }
}copy
```

Let's fix creating new notes so it works with the backend. This means adding the token of the logged-in user to the Authorization header of the HTTP request.
The _noteService_ module changes like so:
```
import axios from 'axios'
const baseUrl = '/api/notes'

let token = null
const setToken = newToken => {  token = `Bearer ${newToken}`}
const getAll = () => {
  const request = axios.get(baseUrl)
  return request.then(response => response.data)
}

const create = async newObject => {
  const config = {    headers: { Authorization: token }  }
  const response = await axios.post(baseUrl, newObject, config)  return response.data
}

const update = (id, newObject) => {
  const request = axios.put(`${ baseUrl }/${id}`, newObject)
  return request.then(response => response.data)
}

export default { getAll, create, update, setToken }copy
```

The noteService module contains a private variable called _token_. Its value can be changed with the _setToken_ function, which is exported by the module. _create_ , now with async/await syntax, sets the token to the _Authorization_ header. The header is given to axios as the third parameter of the _post_ method.
The event handler responsible for login must be changed to call the method `noteService.setToken(user.token)` with a successful login:
```
const handleLogin = async (event) => {
  event.preventDefault()

  try {
    const user = await loginService.login({ username, password })
    noteService.setToken(user.token)    setUser(user)
    setUsername('')
    setPassword('')
  } catch {
    // ...
  }
}copy
```

And now adding new notes works again!
### Saving the token to the browser's local storage
Our application has a small flaw: if the browser is refreshed (eg. pressing F5), the user's login information disappears.
This problem is easily solved by saving the login details to 
It is very easy to use. A _value_ corresponding to a certain _key_ is saved to the database with the method 
```
window.localStorage.setItem('name', 'juha tauriainen')copy
```

saves the string given as the second parameter as the value of the key _name_.
The value of a key can be found with the method 
```
window.localStorage.getItem('name')copy
```

while 
Values in the local storage are persisted even when the page is re-rendered. The storage is 
Let's extend our application so that it saves the details of a logged-in user to the local storage.
Values saved to the storage are _JSON.stringify_. Correspondingly, when a JSON object is read from the local storage, it has to be parsed back to JavaScript with _JSON.parse_.
Changes to the login method are as follows:
```
  const handleLogin = async (event) => {
    event.preventDefault()
    try {
      const user = await loginService.login({ username, password })

      window.localStorage.setItem(        'loggedNoteappUser', JSON.stringify(user)      )       noteService.setToken(user.token)
      setUser(user)
      setUsername('')
      setPassword('')
    } catch (exception) {
      // ...
    }
  }copy
```

The details of a logged-in user are now saved to the local storage, and they can be viewed on the console (by typing _window.localStorage_ in it):
![browser showing user data in console saved in local storage](../assets/cff10c7d46c274ff.png)
You can also inspect the local storage using the developer tools. On Chrome, go to the _Application_ tab and select _Local Storage_ (more details _Storage_ tab and select _Local Storage_ (details 
We still have to modify our application so that when we enter the page, the application checks if user details of a logged-in user can already be found on the local storage. If they are there, the details are saved to the state of the application and to _noteService_.
The right way to do this is with an [part 2](../part2/01-getting-data-from-server-effect-hooks.md), and used to fetch notes from the server.
We can have multiple effect hooks, so let's create a second one to handle the first loading of the page:
```
const App = () => {
  const [notes, setNotes] = useState([])
  const [newNote, setNewNote] = useState('')
  const [showAll, setShowAll] = useState(true)
  const [errorMessage, setErrorMessage] = useState(null)
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [user, setUser] = useState(null)

  useEffect(() => {
    noteService.getAll().then(initialNotes => {
      setNotes(initialNotes)
    })
  }, [])
  
  useEffect(() => {    const loggedUserJSON = window.localStorage.getItem('loggedNoteappUser')    if (loggedUserJSON) {      const user = JSON.parse(loggedUserJSON)      setUser(user)      noteService.setToken(user.token)    }  }, [])
  // ...
}copy
```

The empty array as the parameter of the effect ensures that the effect is executed only when the component is rendered 
Now a user stays logged in to the application forever. We should probably add a _logout_ functionality, which removes the login details from the local storage. We will however leave it as an exercise.
It's possible to log out a user using the console, and that is enough for now. You can log out with the command:
```
window.localStorage.removeItem('loggedNoteappUser')copy
```

or with the command which empties _localstorage_ completely:
```
window.localStorage.clear()copy
```

The current application code can be found on _part5-3_.
### Exercises 5.1.-5.4.
We will now create a frontend for the blog list backend we created in the last part. You can use [part 3](../part3/01-deploying-app-to-internet-proxy.md).
It is enough to submit your finished solution. You can commit after each exercise, but that is not necessary.
The first few exercises revise everything we have learned about React so far. They can be challenging, especially if your backend is incomplete. It might be best to use the backend that we marked as the answer for part 4.
While doing the exercises, remember all of the debugging methods we have talked about, especially keeping an eye on the console.
**Warning:** If you notice you are mixing in the _async/await_ and _then_ commands, it's 99.9% certain you are doing something wrong. Use either or, never both.
#### 5.1: Blog List Frontend, step 1
Clone the application from 
```
git clone https://github.com/fullstack-hy2020/bloglist-frontendcopy
```

_Remove the git configuration of the cloned application_
```
cd bloglist-frontend   // go to cloned repository
rm -rf .gitcopy
```

The application is started the usual way, but you have to install its dependencies first:
```
npm install
npm run devcopy
```

Implement login functionality to the frontend. The token returned with a successful login is saved to the application's state _user_.
If a user is not logged in, _only_ the login form is visible.
![browser showing visible login form only](../assets/8f199cc9540fd7a2.png)
If the user is logged-in, the name of the user and a list of blogs is shown.
![browser showing blogs and who is logged in](../assets/168e94f027cbc9f4.png)
User details of the logged-in user do not have to be saved to the local storage yet.
**NB** You can implement the conditional rendering of the login form like this for example:
```
  if (user === null) {
    return (
      <div>
        <h2>Log in to application</h2>
        <form>
          //...
        </form>
      </div>
    )
  }

  return (
    <div>
      <h2>blogs</h2>
      {blogs.map(blog =>
        <Blog key={blog.id} blog={blog} />
      )}
    </div>
  )
}copy
```

#### 5.2: Blog List Frontend, step 2
Make the login 'permanent' by using the local storage. Also, implement a way to log out.
![browser showing logout button after logging in](../assets/c80be348a0e3282b.png)
Ensure the browser does not remember the details of the user after logging out.
#### 5.3: Blog List Frontend, step 3
Expand your application to allow a logged-in user to add new blogs:
![browser showing new blog form](../assets/c917e335c1e2d37a.png)
#### 5.4: Blog List Frontend, step 4
Implement notifications that inform the user about successful and unsuccessful operations at the top of the page. For example, when a new blog is added, the following notification can be shown:
![browser showing successful operation notification](../assets/2ce35e3917b13ae7.png)
Failed login can show the following notification:
![browser showing failed login attempt notification](../assets/3cb6a934a051a740.png)
The notifications must be visible for a few seconds. It is not compulsory to add colors.
### A note on using local storage
At the [end](../part4/01-token-authentication-problems-of-token-based-authentication.md) of the last part, we mentioned that the challenge of token-based authentication is how to cope with the situation when the API access of the token holder to the API needs to be revoked.
There are two solutions to the problem. The first one is to limit the validity period of a token. This forces the user to re-login to the app once the token has expired. The other approach is to save the validity information of each token to the backend database. This solution is often called a _server-side session_.
No matter how the validity of tokens is checked and ensured, saving a token in the local storage might contain a security risk if the application has a security vulnerability that allows 
If one wants to play safe, the best option is to not store a token in local storage. This might be an option in situations where leaking a token might have tragic consequences.
It has been suggested that the identity of a signed-in user should be saved as 
However, it is good to notice that even the use of httpOnly cookies does not guarantee anything. It has even been suggested that httpOnly cookies are 
So no matter the used solution the most important thing is to 
[ Part 4 **Previous part** ](../part4/01-part4.md)[ Part 5b **Next part** ](../part5/01-props-children-and-proptypes.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)