---{
  "title": "More about styles",
  "source_url": "https://fullstackopen.com/en/part7/more_about_styles",
  "crawl_timestamp": "2025-10-04T19:17:01Z",
  "checksum": "54cf52f1b5a712fe971776d8b13f672515c3e43d8ed1f480964c5334ab500e20"
}
---[Skip to content](../part7/01-more-about-styles-course-main-content.md)
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
More about styles
[a React Router](../part7/01-react-router.md)[b Custom hooks](../part7/01-custom-hooks.md)
c More about styles

- [Ready-made UI libraries](../part7/01-more-about-styles-ready-made-ui-libraries.md)
- [React Bootstrap](../part7/01-more-about-styles-react-bootstrap.md)
- [Material UI](../part7/01-more-about-styles-material-ui.md)
- [Closing thoughts](../part7/01-more-about-styles-closing-thoughts.md)
- [Other UI frameworks](../part7/01-more-about-styles-other-ui-frameworks.md)
- [Styled components](../part7/01-more-about-styles-styled-components.md)
- [Exercises](../part7/01-more-about-styles-exercises.md)


[d Webpack](../part7/01-webpack.md)[e Class components, Miscellaneous](../part7/01-class-components-miscellaneous.md)[f Exercises: extending the bloglist](../part7/01-exercises-extending-the-bloglist.md)
c
# More about styles
In part 2, we examined two different ways of adding styles to our application: the old-school [single CSS](../part2/01-adding-styles-to-react-app.md) file and [inline styles](../part2/01-adding-styles-to-react-app-inline-styles.md). In this part, we will take a look at a few other ways.
### Ready-made UI libraries
One approach to defining styles for an application is to use a ready-made "UI framework".
One of the first widely popular UI frameworks was the
Many UI frameworks provide developers of web applications with ready-made themes and "components" like buttons, menus, and tables. We write components in quotes because, in this context, we are not talking about React components. Usually, UI frameworks are used by including the CSS stylesheets and JavaScript code of the framework in the application.
Many UI frameworks have React-friendly versions where the framework's "components" have been transformed into React components. There are a few different React versions of Bootstrap like
Next, we will take a closer look at two UI frameworks, Bootstrap and [React Router](../part7/01-react-router.md) section of the course material.
### React Bootstrap
Let's start by taking a look at Bootstrap with the help of the
Let's install the package with the command:

```
npm install react-bootstrapcopy
```

Then let's add a _head_ tag in the _public/index.html_ file of the application:

```
<head>
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
    integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM"
    crossorigin="anonymous"
  />
  // ...
</head>copy
```

When we reload the application, we notice that it already looks a bit more stylish:
![browser notes app with bootstrap](../assets/e9c2d7e8b497d882.png)
In Bootstrap, all of the contents of the application are typically rendered inside a _div_ element of the application the _container_ class attribute:

```
const App = () => {
  // ...

  return (
    <div className="container">      // ...
    </div>
  )
}copy
```

We notice that this already affected the appearance of the application. The content is no longer as close to the edges of the browser as it was earlier:
![browser notes app with margin spacing](../assets/903949ca8cb7d2d7.png)
#### Tables
Next, let's make some changes to the _Notes_ component so that it renders the list of notes as a

```
const Notes = ({ notes }) => (
  <div>
    <h2>Notes</h2>
    <Table striped>      <tbody>
        {notes.map(note =>
          <tr key={note.id}>
            <td>
              <Link to={`/notes/${note.id}`}>
                {note.content}
              </Link>
            </td>
            <td>
              {note.user}
            </td>
          </tr>
        )}
      </tbody>
    </Table>
  </div>
)copy
```

The appearance of the application is quite stylish:
![browser notes tab with built-in table](../assets/d7d9a6e94ff4d201.png)
Notice that the React Bootstrap components have to be imported separately from the library as shown below:

```
import { Table } from 'react-bootstrap'copy
```

#### Forms
Let's improve the form in the _Login_ view with the help of Bootstrap
React Bootstrap provides built-in

```
let Login = (props) => {
  // ...
  return (
    <div>
      <h2>login</h2>
      <Form onSubmit={onSubmit}>
        <Form.Group>
          <Form.Label>username:</Form.Label>
          <Form.Control
            type="text"
            name="username"
          />
        </Form.Group>
        <Form.Group>
          <Form.Label>password:</Form.Label>
          <Form.Control
            type="password"
          />
        </Form.Group>
        <Button variant="primary" type="submit">
          login
        </Button>
      </Form>
    </div>
  )
}copy
```

The number of components we need to import increases:

```
import { Table, Form, Button } from 'react-bootstrap'copy
```

After switching over to the Bootstrap form, our improved application looks like this:
![browser notes app with bootstrap login](../assets/1ee596a88c70c754.png)
#### Notification
Now that the login form is in better shape, let's take a look at improving our application's notifications:
![browser notes app with bootstrap notification](../assets/44c967063f25a77a.png)
Let's add a message for the notification when a user logs into the application. We will store it in the _message_ variable in the _App_ component's state:

```
const App = () => {
  const [notes, setNotes] = useState([
    // ...
  ])

  const [user, setUser] = useState(null)
  const [message, setMessage] = useState(null)
  const login = (user) => {
    setUser(user)
    setMessage(`welcome ${user}`)    setTimeout(() => {      setMessage(null)    }, 10000)  }
  // ...
}copy
```

We will render the message as a Bootstrap

```
<div className="container">
  {(message &&    <Alert variant="success">      {message}    </Alert>  )}  // ...
</div>copy
```

#### Navigation structure
Lastly, let's alter the application's navigation menu to use Bootstrap's

```
<Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
  <Navbar.Toggle aria-controls="responsive-navbar-nav" />
  <Navbar.Collapse id="responsive-navbar-nav">
    <Nav className="me-auto">
      <Nav.Link href="#" as="span">
        <Link style={padding} to="/">home</Link>
      </Nav.Link>
      <Nav.Link href="#" as="span">
        <Link style={padding} to="/notes">notes</Link>
      </Nav.Link>
      <Nav.Link href="#" as="span">
        <Link style={padding} to="/users">users</Link>
      </Nav.Link>
      <Nav.Link href="#" as="span">
        {user
          ? <em style={padding}>{user} logged in</em>
          : <Link style={padding} to="/login">login</Link>
        }
      </Nav.Link>
    </Nav>
  </Navbar.Collapse>
</Navbar>copy
```

The resulting layout has a very clean and pleasing appearance:
![browser notes app bootstrap black navigation bar](../assets/17da3f3b174e8519.png)
If the viewport of the browser is narrowed, we notice that the menu "collapses" and it can be expanded by clicking the "hamburger" button:
![browser notes app with hamburger menu](../assets/daee17829853588c.png)
Bootstrap and a large majority of existing UI frameworks produce
Chrome's developer tools make it possible to simulate using our application in the browser of different mobile clients:
![chrome devtools with mobile browser preview of notes app](../assets/8b2dba6ae7f26ecf.png)
You can find the complete code for the application
### Material UI
As our second example, we will look into the
Install the library with the command

```
npm install @mui/material @emotion/react @emotion/styledcopy
```

Now let's use MaterialUI to do the same modifications to the code we did earlier with Bootstrap.
Render the contents of the whole application within a

```
import { Container } from '@mui/material'

const App = () => {
  // ...
  return (
    <Container>
      // ...
    </Container>
  )
}copy
```

#### Table
Let's start with the _Notes_ component. We'll render the list of notes as a

```
const Notes = ({ notes }) => (
  <div>
    <h2>Notes</h2>

    <TableContainer component={Paper}>
      <Table>
        <TableBody>
          {notes.map(note => (
            <TableRow key={note.id}>
              <TableCell>
                <Link to={`/notes/${note.id}`}>{note.content}</Link>
              </TableCell>
              <TableCell>
                {note.user}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  </div>
)copy
```

The table looks like so:
![browser notes materialUI table](../assets/1ae3e0dc89f8ab1c.png)
One less pleasant feature of Material UI is that each component has to be imported separately. The import list for the notes page is quite long:

```
import {
  Container,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableRow,
  Paper,
} from '@mui/material'copy
```

#### Form
Next, let's make the login form in the _Login_ view better using the

```
const Login = (props) => {
  const navigate = useNavigate()

  const onSubmit = (event) => {
    event.preventDefault()
    props.onLogin('mluukkai')
    navigate('/')
  }

  return (
    <div>
      <h2>login</h2>
      <form onSubmit={onSubmit}>
        <div>
          <TextField label="username" />
        </div>
        <div>
          <TextField label="password" type='password' />
        </div>
        <div>
          <Button variant="contained" color="primary" type="submit">
            login
          </Button>
        </div>
      </form>
    </div>
  )
}copy
```

The result is:
![browser notes app materialUI login form](../assets/629bf3fe7524a4b3.png)
MaterialUI, unlike Bootstrap, does not provide a component for the form itself. The form here is an ordinary HTML
Remember to import all the components used in the form.
#### Notification
The notification displayed on login can be done using the

```
<div>
  {(message &&    <Alert severity="success">      {message}    </Alert>  )}</div>copy
```

Alert is quite stylish:
![browser notes app materialUI notifications](../assets/24629bc3228f6ee9.png)
#### Navigation structure
We can implement navigation using the
If we use the example code from the documentation

```
<AppBar position="static">
  <Toolbar>
    <IconButton edge="start" color="inherit" aria-label="menu">
    </IconButton>
    <Button color="inherit">
      <Link to="/">home</Link>
    </Button>
    <Button color="inherit">
      <Link to="/notes">notes</Link>
    </Button>
    <Button color="inherit">
      <Link to="/users">users</Link>
    </Button>  
    <Button color="inherit">
      {user
        ? <em>{user} logged in</em>
        : <Link to="/login">login</Link>
      }
    </Button>                
  </Toolbar>
</AppBar>copy
```

we do get working navigation, but it could look better
![browser notes app materialUI blue navbar](../assets/b920025398d09886.png)
We can find a better way in the
By defining

```
<Button color="inherit" component={Link} to="/">
  home
</Button>copy
```

the _Button_ component is rendered so that its root component is react-router-dom's _Link_ , which receives its path as the prop field _to_.
The code for the navigation bar is the following:

```
<AppBar position="static">
  <Toolbar>
    <Button color="inherit" component={Link} to="/">
      home
    </Button>
    <Button color="inherit" component={Link} to="/notes">
      notes
    </Button>
    <Button color="inherit" component={Link} to="/users">
      users
    </Button>   
    {user
      ? <em>{user} logged in</em>
      : <Button color="inherit" component={Link} to="/login">
          login
        </Button>
    }                              
  </Toolbar>
</AppBar>copy
```

and it looks like we want it to:
![browser notes app MaterialUI blue nav bar white text](../assets/a13d2f28bf86ffd3.png)
The code of the application can be found
### Closing thoughts
The difference between react-bootstrap and MaterialUI is not big. It's up to you which one you find better looking. I have not used MaterialUI a lot, but my first impressions are positive. Its documentation is a bit better than react-bootstrap's. According to
![npmtrends of materialUI vs bootstrap](../assets/769df514377ebb19.png)
In the two previous examples, we used the UI frameworks with the help of React-integration libraries.
Instead of using the _Table_ component:

```
<Table striped>
  // ...
</Table>copy
```

We could have used a regular HTML _table_ and added the required CSS class:

```
<table className="table striped">
  // ...
</table>copy
```

The benefit of using the React Bootstrap library is not that evident from this example.
In addition to making the frontend code more compact and readable, another benefit of using React UI framework libraries is that they include the JavaScript that is needed to make specific components work. Some Bootstrap components require a few unpleasant
Some potential downsides to using UI frameworks through integration libraries instead of using them "directly" are that integration libraries may have unstable APIs and poor documentation. The situation with
There is also the question of whether or not UI framework libraries should be used in the first place. It is up to everyone to form their own opinion, but for people lacking knowledge in CSS and web design, they are very useful tools.
### Other UI frameworks
Here are some other UI frameworks for your consideration. If you do not see your favorite UI framework in the list, please make a pull request to the course material for adding it.
### Styled components
There are also
The
Let's make a few changes to the styles of our application with the help of styled components. First, install the package with the command:

```
npm install styled-componentscopy
```

Then let's define two components with styles:

```
import styled from 'styled-components'

const Button = styled.button`
  background: Bisque;
  font-size: 1em;
  margin: 1em;
  padding: 0.25em 1em;
  border: 2px solid Chocolate;
  border-radius: 3px;
`

const Input = styled.input`
  margin: 0.25em;
`copy
```

The code above creates styled versions of the _button_ and _input_ HTML elements and then assigns them to the _Button_ and _Input_ variables.
The syntax for defining the styles is quite interesting, as the CSS rules are defined inside of backticks.
The styled components that we defined work exactly like regular _button_ and _input_ elements, and they can be used in the same way:

```
const Login = (props) => {
  // ...
  return (
    <div>
      <h2>login</h2>
      <form onSubmit={onSubmit}>
        <div>
          username:
          <Input />        </div>
        <div>
          password:
          <Input type='password' />        </div>
        <Button type="submit" primary=''>login</Button>      </form>
    </div>
  )
}copy
```

Let's create a few more components for styling this application which will be styled versions of _div_ elements:

```
const Page = styled.div`
  padding: 1em;
  background: papayawhip;
`

const Navigation = styled.div`
  background: BurlyWood;
  padding: 1em;
`

const Footer = styled.div`
  background: Chocolate;
  padding: 1em;
  margin-top: 1em;
`copy
```

Let's use the components in our application:

```
const App = () => {
  // ...

  return (
     <Page>      <Navigation>        <Link style={padding} to="/">home</Link>
        <Link style={padding} to="/notes">notes</Link>
        <Link style={padding} to="/users">users</Link>
        {user
          ? <em>{user} logged in</em>
          : <Link style={padding} to="/login">login</Link>
        }
      </Navigation>      
      <Routes>
        <Route path="/notes/:id" element={<Note note={note} />} />  
        <Route path="/notes" element={<Notes notes={notes} />} />   
        <Route path="/users" element={user ? <Users /> : <Navigate replace to="/login" />} />
        <Route path="/login" element={<Login onLogin={login} />} />
        <Route path="/" element={<Home />} />      
      </Routes>

      <Footer>        <em>Note app, Department of Computer Science 2022</em>
      </Footer>    </Page>  )
}copy
```

The appearance of the resulting application is shown below:
![browser notes app styled components](../assets/b8c5750310d3329f.png)
Styled components have seen consistent growth in popularity in recent times, and quite a lot of people consider it to be the best way of defining styles in React applications.
### Exercises
The exercises related to the topics presented here can be found at the end of this course material section in the exercise set [for extending the blog list application](../part7/01-exercises-extending-the-bloglist.md).
[Part 7b **Previous part**](../part7/01-custom-hooks.md)[Part 7d **Next part**](../part7/01-webpack.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)
