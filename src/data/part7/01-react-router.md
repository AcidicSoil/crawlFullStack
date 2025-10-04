---{
  "title": "React Router",
  "source_url": "https://fullstackopen.com/en/part7/react_router",
  "crawl_timestamp": "2025-10-04T19:17:04Z",
  "checksum": "479c2dfc576cdf9f8cdfeca9b3b69e581c00137c4c936c182ba8918ad3ccae29"
}
---[Skip to content](../part7/01-react-router-course-main-content.md)
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
React Router
a React Router

- [Application navigation structure](../part7/01-react-router-application-navigation-structure.md)
- [React Router](../part7/01-react-router-react-router.md)
- [Parameterized route](../part7/01-react-router-parameterized-route.md)
- [useNavigate](../part7/01-react-router-use-navigate.md)
- [Redirect](../part7/01-react-router-redirect.md)
- [Parameterized route revisited](../part7/01-react-router-parameterized-route-revisited.md)
- [Exercises 7.1.-7.3.](../part7/01-react-router-exercises-7-1-7-3.md)


[b Custom hooks](../part7/01-custom-hooks.md)[c More about styles](../part7/01-more-about-styles.md)[d Webpack](../part7/01-webpack.md)[e Class components, Miscellaneous](../part7/01-class-components-miscellaneous.md)[f Exercises: extending the bloglist](../part7/01-exercises-extending-the-bloglist.md)
a
# React Router
The exercises in this seventh part of the course differ a bit from the ones before. In this and the next chapter, as usual, there are [exercises related to the theory of the chapter](../part7/01-react-router-exercises-7-1-7-3.md).
In addition to the exercises in this and the next chapter, there are a series of exercises in which we'll be revising what we've learned during the whole course, by expanding the BlogList application, which we worked on during parts 4 and 5.
### Application navigation structure
Following part 6, we return to React without Redux.
It is very common for web applications to have a navigation bar, which enables switching the view of the application.
Our app could have a main page
![browser showing notes app with home nav link](../assets/51fdafd1b8206742.png)
and separate pages for showing information on notes and users:
![browser showing notes app with notes nav link](../assets/95a8e98a65114c5d.png)
In an [old school web app](../part0/01-fundamentals-of-web-apps-traditional-web-applications.md), changing the page shown by the application would be accomplished by the browser making an HTTP GET request to the server and rendering the HTML representing the view that was returned.
In single-page apps, we are, in reality, always on the same page. The Javascript code run by the browser creates an illusion of different "pages". If HTTP requests are made when switching views, they are only for fetching JSON-formatted data, which the new view might require for it to be shown.
The navigation bar and an application containing multiple views are very easy to implement using React.
Here is one way:

```
import { useState }  from 'react'
import ReactDOM from 'react-dom/client'

const Home = () => (
  <div> <h2>TKTL notes app</h2> </div>
)

const Notes = () => (
  <div> <h2>Notes</h2> </div>
)

const Users = () => (
  <div> <h2>Users</h2> </div>
)

const App = () => {
  const [page, setPage] = useState('home')

  const toPage = (page) => (event) => {
    event.preventDefault()
    setPage(page)
  }

  const content = () => {
    if (page === 'home') {
      return <Home />
    } else if (page === 'notes') {
      return <Notes />
    } else if (page === 'users') {
      return <Users />
    }
  }

  const padding = {
    padding: 5
  }

  return (
    <div>
      <div>
        <a href="" onClick={toPage('home')} style={padding}>
          home
        </a>
        <a href="" onClick={toPage('notes')} style={padding}>
          notes
        </a>
        <a href="" onClick={toPage('users')} style={padding}>
          users
        </a>
      </div>

      {content()}
    </div>
  )
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />)copy
```

Each view is implemented as its own component. We store the view component information in the application state called _page_. This information tells us which component, representing a view, should be shown below the menu bar.
However, the method is not very optimal. As we can see from the pictures, the address stays the same even though at times we are in different views. Each view should preferably have its own address, e.g. to make bookmarking possible. The _back_ button doesn't work as expected for our application either, meaning that _back_ doesn't move you to the previously displayed view of the application, but somewhere completely different. If the application were to grow even bigger and we wanted to, for example, add separate views for each user and note, then this self-made _routing_ , which means the navigation management of the application, would get overly complicated.
### React Router
Luckily, React has the
Let's change the above application to use React Router. First, we install React Router with the command:

```
npm install react-router-domcopy
```

The routing provided by React Router is enabled by changing the application as follows:

```
import {
  BrowserRouter as Router,
  Routes, Route, Link
} from 'react-router-dom'

const App = () => {

  const padding = {
    padding: 5
  }

  return (
    <Router>
      <div>
        <Link style={padding} to="/">home</Link>
        <Link style={padding} to="/notes">notes</Link>
        <Link style={padding} to="/users">users</Link>
      </div>

      <Routes>
        <Route path="/notes" element={<Notes />} />
        <Route path="/users" element={<Users />} />
        <Route path="/" element={<Home />} />
      </Routes>

      <div>
        <i>Note app, Department of Computer Science 2024</i>
      </div>
    </Router>
  )
}copy
```

Routing, or the conditional rendering of components _based on the URL_ in the browser, is used by placing components as children of the _Router_ component, meaning inside _Router_ tags.
Notice that, even though the component is referred to by the name _Router_ , we are talking about

```
import {
  BrowserRouter as Router,  Routes, Route, Link
} from 'react-router-dom'copy
```

According to the
> _BrowserRouter_ is a _Router_ that uses the HTML5 history API (pushState, replaceState and the popState event) to keep your UI in sync with the URL.
Normally the browser loads a new page when the URL in the address bar changes. However, with the help of the _BrowserRouter_ enables us to use the URL in the address bar of the browser for internal "routing" in a React application. So, even if the URL in the address bar changes, the content of the page is only manipulated using Javascript, and the browser will not load new content from the server. Using the back and forward actions, as well as making bookmarks, is still logical like on a traditional web page.
Inside the router, we define _links_ that modify the address bar with the help of the

```
<Link to="/notes">notes</Link>copy
```

creates a link in the application with the text _notes_ , which when clicked changes the URL in the address bar to _/notes_.
Components rendered based on the URL of the browser are defined with the help of the component

```
<Route path="/notes" element={<Notes />} />copy
```

defines that, if the browser address is _/notes_ , we render the _Notes_ component.
We wrap the components to be rendered based on the URL with a

```
<Routes>
  <Route path="/notes" element={<Notes />} />
  <Route path="/users" element={<Users />} />
  <Route path="/" element={<Home />} />
</Routes>copy
```

The Routes works by rendering the first component whose _path_ matches the URL in the browser's address bar.
### Parameterized route
Let's examine a slightly modified version from the previous example. The complete code for the updated example can be found
The application now contains five different views whose display is controlled by the router. In addition to the components from the previous example (_Home_ , _Notes_ and _Users_), we have _Login_ representing the login view and _Note_ representing the view of a single note.
_Home_ and _Users_ are unchanged from the previous exercise. _Notes_ is a bit more complicated. It renders the list of notes passed to it as props in such a way that the name of each note is clickable.
![notes app showing notes are clickable](../assets/62b3ad9ba8e8902f.png)
The ability to click a name is implemented with the component _Link_ , and clicking the name of a note whose id is 3 would trigger an event that changes the address of the browser into _notes/3_ :

```
const Notes = ({notes}) => (
  <div>
    <h2>Notes</h2>
    <ul>
      {notes.map(note =>
        <li key={note.id}>
          <Link to={`/notes/${note.id}`}>{note.content}</Link>        </li>
      )}
    </ul>
  </div>
)copy
```

We define parameterized URLs in the routing of the _App_ component as follows:

```
<Router>
  // ...

  <Routes>
    <Route path="/notes/:id" element={<Note notes={notes} />} />    <Route path="/notes" element={<Notes notes={notes} />} />   
    <Route path="/users" element={user ? <Users /> : <Navigate replace to="/login" />} />
    <Route path="/login" element={<Login onLogin={login} />} />
    <Route path="/" element={<Home />} />      
  </Routes>
</Router>copy
```

We define the route rendering a specific note "express style" by marking the parameter with a colon - _:id_

```
<Route path="/notes/:id" element={<Note notes={notes} />} />copy
```

When a browser navigates to the URL for a specific note, for example, _/notes/3_ , we render the _Note_ component:

```
import {
  // ...
  useParams} from 'react-router-dom'

const Note = ({ notes }) => {
  const id = useParams().id  const note = notes.find(n => n.id === Number(id)) 
  return (
    <div>
      <h2>{note.content}</h2>
      <div>{note.user}</div>
      <div><strong>{note.important ? 'important' : ''}</strong></div>
    </div>
  )
}copy
```

The _Note_ component receives all of the notes as props _notes_ , and it can access the URL parameter (the id of the note to be displayed) with the
### useNavigate
We have also implemented a simple login function in our application. If a user is logged in, information about a logged-in user is saved to the _user_ field of the state of the _App_ component.
The option to navigate to the _Login_ view is rendered conditionally in the menu.

```
<Router>
  <div>
    <Link style={padding} to="/">home</Link>
    <Link style={padding} to="/notes">notes</Link>
    <Link style={padding} to="/users">users</Link>
    {user      ? <em>{user} logged in</em>      : <Link style={padding} to="/login">login</Link>    }  </div>

  // ...
</Router>copy
```

So if the user is already logged in, instead of displaying the link _Login_ , we show its username:
![browser notes app showing username logged in](../assets/137327a075f37125.png)
The code of the component handling the login functionality is as follows:

```
import {
  // ...
  useNavigate} from 'react-router-dom'

const Login = (props) => {
  const navigate = useNavigate()
  const onSubmit = (event) => {
    event.preventDefault()
    props.onLogin('mluukkai')
    navigate('/')  }

  return (
    <div>
      <h2>login</h2>
      <form onSubmit={onSubmit}>
        <div>
          username: <input />
        </div>
        <div>
          password: <input type='password' />
        </div>
        <button type="submit">login</button>
      </form>
    </div>
  )
}copy
```

What is interesting about this component is the use of the
With user login, we call _navigate('/')_ which causes the browser's URL to change to _/_ and the application renders the corresponding component _Home_.
Both [rules](../part1/01-rules-of-hooks.md) to using hook functions.
### Redirect
There is one more interesting detail about the _Users_ route:

```
<Route path="/users" element={user ? <Users /> : <Navigate replace to="/login" />} />copy
```

If a user isn't logged in, the _Users_ component is not rendered. Instead, the user is _redirected_ using the component

```
<Navigate replace to="/login" />copy
```

In reality, it would perhaps be better to not even show links in the navigation bar requiring login if the user is not logged into the application.
Here is the _App_ component in its entirety:

```
const App = () => {
  const [notes, setNotes] = useState([
    // ...
  ])

  const [user, setUser] = useState(null) 

  const login = (user) => {
    setUser(user)
  }

  const padding = {
    padding: 5
  }

  return (
    <div>
      <Router>
        <div>
          <Link style={padding} to="/">home</Link>
          <Link style={padding} to="/notes">notes</Link>
          <Link style={padding} to="/users">users</Link>
          {user
            ? <em>{user} logged in</em>
            : <Link style={padding} to="/login">login</Link>
          }
        </div>

        <Routes>
          <Route path="/notes/:id" element={<Note notes={notes} />} />  
          <Route path="/notes" element={<Notes notes={notes} />} />   
          <Route path="/users" element={user ? <Users /> : <Navigate replace to="/login" />} />
          <Route path="/login" element={<Login onLogin={login} />} />
          <Route path="/" element={<Home />} />      
        </Routes>
      </Router>      
      <footer>
        <br />
        <em>Note app, Department of Computer Science 2024</em>
      </footer>
    </div>
  )
}copy
```

We define an element common for modern web apps called _footer_ , which defines the part at the bottom of the screen, outside of the _Router_ , so that it is shown regardless of the component shown in the routed part of the application.
### Parameterized route revisited
Our application has a flaw. The _Note_ component receives all of the notes, even though it only displays the one whose id matches the URL parameter:

```
const Note = ({ notes }) => { 
  const id = useParams().id
  const note = notes.find(n => n.id === Number(id))
  // ...
}copy
```

Would it be possible to modify the application so that the _Note_ component receives only the note that it should display?

```
const Note = ({ note }) => {
  return (
    <div>
      <h2>{note.content}</h2>
      <div>{note.user}</div>
      <div><strong>{note.important ? 'important' : ''}</strong></div>
    </div>
  )
}copy
```

One way to do this would be to use React Router's _App_ component.
It is not possible to use the _useMatch_ hook in the component which defines the routed part of the application. Let's move the use of the _Router_ components from _App_ :

```
ReactDOM.createRoot(document.getElementById('root')).render(
  <Router>    <App />
  </Router>)copy
```

The _App_ component becomes:

```
import {
  // ...
  useMatch} from 'react-router-dom'

const App = () => {
  // ...

  const match = useMatch('/notes/:id')  const note = match     ? notes.find(note => note.id === Number(match.params.id))    : null
  return (
    <div>
      <div>
        <Link style={padding} to="/">home</Link>
        // ...
      </div>

      <Routes>
        <Route path="/notes/:id" element={<Note note={note} />} />        <Route path="/notes" element={<Notes notes={notes} />} />   
        <Route path="/users" element={user ? <Users /> : <Navigate replace to="/login" />} />
        <Route path="/login" element={<Login onLogin={login} />} />
        <Route path="/" element={<Home />} />      
      </Routes>   

      <div>
        <em>Note app, Department of Computer Science 2024</em>
      </div>
    </div>
  )
}  copy
```

Every time the component is rendered, so practically every time the browser's URL changes, the following command is executed:

```
const match = useMatch('/notes/:id')copy
```

If the URL matches _/notes/:id_ , the match variable will contain an object from which we can access the parameterized part of the path, the id of the note to be displayed, and we can then fetch the correct note to display.

```
const note = match 
  ? notes.find(note => note.id === Number(match.params.id))
  : nullcopy
```

The completed code can be found
### Exercises 7.1.-7.3
Let's return to working with anecdotes. Use the redux-free anecdote app found in the repository
If you clone the project into an existing git repository, remember to _delete the git configuration of the cloned application:_

```
cd routed-anecdotes   // go first to directory of the cloned repository
rm -rf .gitcopy
```

The application starts the usual way, but first, you need to install its dependencies:

```
npm install
npm run devcopy
```

#### 7.1: Routed Anecdotes, step 1
Add React Router to the application so that by clicking links in the _Menu_ component the view can be changed.
At the root of the application, meaning the path _/_ , show the list of anecdotes:
![browser at baseURL showing anecdotes and footer](../assets/67bad19e2298c244.png)
The _Footer_ component should always be visible at the bottom.
The creation of a new anecdote should happen e.g. in the path _create_ :
![browser anecdotes /create shows create form](../assets/31de9195b0d237fb.png)
#### 7.2: Routed Anecdotes, step 2
Implement a view for showing a single anecdote:
![browser /anecdotes/number showing single anecdote](../assets/76de36c9324ced0e.png)
Navigating to the page showing the single anecdote is done by clicking the name of that anecdote:
![browser showing previous link that was clicked](../assets/8ac9c9cdb9a8aae2.png)
#### 7.3: Routed Anecdotes, step3
The default functionality of the creation form is quite confusing because nothing seems to be happening after creating a new anecdote using the form.
Improve the functionality such that after creating a new anecdote the application transitions automatically to showing the view for all anecdotes _and_ the user is shown a notification informing them of this successful creation for the next five seconds:
![browser anecdotes showing success message for adding anecdote](../assets/cc64a18d72c304c4.png)
[Part 6 **Previous part**](../part6/01-part6.md)[Part 7b **Next part**](../part7/01-custom-hooks.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)
