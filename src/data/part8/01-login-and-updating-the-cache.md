---{
  "title": "Login and updating the cache",
  "source_url": "https://fullstackopen.com/en/part8/login_and_updating_the_cache",
  "crawl_timestamp": "2025-10-04T19:17:14Z",
  "checksum": "5f67fa78b7298b6e08ff78235df88a1003048b840d1f16663ca2691210eef53f"
}
---[Skip to content](../part8/01-login-and-updating-the-cache-course-main-content.md)
[{() => fs}](https://fullstackopen.com/en/)

- [About course](../about/01-about.md)
- [Course contents](../#course-contents/01-course-contents.md)
- [FAQ](../faq/01-faq.md)
- [Partners](../companies/01-companies.md)
- [Challenge](../challenge/01-challenge.md)
[Search from the material](../search/01-search.md)Toggle dark theme
Select languageSuomi English 中文 Español Français Português(BR)

[Fullstack](../#course-contents/01-course-contents.md)
[Part 8](../part8/01-part8.md)
Login and updating the cache
[a GraphQL-server](../part8/01-graph-ql-server.md)[b React and GraphQL](../part8/01-react-and-graph-ql.md)[c Database and user administration](../part8/01-database-and-user-administration.md)
d Login and updating the cache

- [User login](../part8/01-login-and-updating-the-cache-user-login.md)
- [Adding a token to a header](../part8/01-login-and-updating-the-cache-adding-a-token-to-a-header.md)
- [Updating cache, revisited](../part8/01-login-and-updating-the-cache-updating-cache-revisited.md)
- [Exercises 8.17.-8.22](../part8/01-login-and-updating-the-cache-exercises-8-17-8-22.md)


[e Fragments and subscriptions](../part8/01-fragments-and-subscriptions.md)
d
# Login and updating the cache
The frontend of our application shows the phone directory just fine with the updated server. However, if we want to add new persons, we have to add login functionality to the frontend.
### User login
Let's add the variable _token_ to the application's state. When a user is logged in, it will contain a user token. If _token_ is undefined, we render the _LoginForm_ component responsible for user login. The component receives an error handler and the _setToken_ function as parameters:

```
const App = () => {
  const [token, setToken] = useState(null)
  // ...

  if (!token) {
    return (
      <div>
        <Notify errorMessage={errorMessage} />
        <h2>Login</h2>
        <LoginForm
          setToken={setToken}
          setError={notify}
        />
      </div>
    )
  }

  return (
    // ...
  )
}copy
```

Next, we define a mutation for logging in:

```
export const LOGIN = gql`
  mutation login($username: String!, $password: String!) {
    login(username: $username, password: $password)  {
      value
    }
  }
`copy
```

The _LoginForm_ component works pretty much just like all the other components doing mutations that we have previously created. Interesting lines in the code have been highlighted:

```
import { useState, useEffect } from 'react'
import { useMutation } from '@apollo/client'
import { LOGIN } from '../queries'

const LoginForm = ({ setError, setToken }) => {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const [ login, result ] = useMutation(LOGIN, {    onError: (error) => {
      setError(error.graphQLErrors[0].message)
    }
  })

  useEffect(() => {    if ( result.data ) {      const token = result.data.login.value      setToken(token)      localStorage.setItem('phonenumbers-user-token', token)    }  }, [result.data])
  const submit = async (event) => {
    event.preventDefault()

    login({ variables: { username, password } })
  }

  return (
    <div>
      <form onSubmit={submit}>
        <div>
          username <input
            value={username}
            onChange={({ target }) => setUsername(target.value)}
          />
        </div>
        <div>
          password <input
            type='password'
            value={password}
            onChange={({ target }) => setPassword(target.value)}
          />
        </div>
        <button type='submit'>login</button>
      </form>
    </div>
  )
}

export default LoginFormcopy
```

We are using an effect hook to save the token's value to the state of the _App_ component and the local storage after the server has responded to the mutation. Use of the effect hook is necessary to avoid an endless rendering loop.
Let's also add a button which enables a logged-in user to log out. The button's onClick handler sets the _token_ state to null, removes the token from local storage and resets the cache of the Apollo client. The last step is
We can reset the cache using the _client_ object. The client can be accessed with the

```
const App = () => {
  const [token, setToken] = useState(null)
  const [errorMessage, setErrorMessage] = useState(null)
  const result = useQuery(ALL_PERSONS)
  const client = useApolloClient()
  if (result.loading)  {
    return <div>loading...</div>
  }

  const logout = () => {    setToken(null)    localStorage.clear()    client.resetStore()  }
  if (!token) {    return (      <>        <Notify errorMessage={errorMessage} />        <LoginForm setToken={setToken} setError={notify} />      </>    )  }
  return (
    <>
      <Notify errorMessage={errorMessage} />
      <button onClick={logout}>logout</button>      <Persons persons={result.data.allPersons} />
      <PersonForm setError={notify} />
      <PhoneForm setError={notify} />
    </>
  )
}copy
```

### Adding a token to a header
After the backend changes, creating new persons requires that a valid user token is sent with the request. In order to send the token, we have to change the way we define the _ApolloClient_ object in _main.jsx_ a little.

```
import { ApolloClient, InMemoryCache, ApolloProvider, createHttpLink } from '@apollo/client'import { setContext } from '@apollo/client/link/context'
const authLink = setContext((_, { headers }) => {  const token = localStorage.getItem('phonenumbers-user-token')  return {    headers: {      ...headers,      authorization: token ? `Bearer ${token}` : null,    }  }})
const httpLink = createHttpLink({
  uri: 'http://localhost:4000',
})

const client = new ApolloClient({
  cache: new InMemoryCache(),
  link: authLink.concat(httpLink)})copy
```

The field _uri_ that was previously used when creating the _client_ object has been replaced by the field _link_ , which defines in a more complicated case how Apollo is connected to the server. The server url is now wrapped using the function _authorization_ for each request to the server.
Creating new persons and changing numbers works again. There is however one remaining problem. If we try to add a person without a phone number, it is not possible.
![browser showing person validation failed](../assets/257b68761b99c226.png)
Validation fails, because frontend sends an empty string as the value of _phone_.
Let's change the function creating new persons so that it sets _phone_ to _undefined_ if user has not given a value.

```
const PersonForm = ({ setError }) => {
  // ...
  const submit = async (event) => {
    event.preventDefault()
    createPerson({
      variables: { 
        name, street, city,        phone: phone.length > 0 ? phone : undefined      }
    })

  // ...
  }

  // ...
}copy
```

### Updating cache, revisited
We have to [update](../part8/01-react-and-graph-ql-updating-the-cache.md) the cache of the Apollo client on creating new persons. We can update it using the mutation's _refetchQueries_ option to define that the _ALL_PERSONS_ query is done again.

```
const PersonForm = ({ setError }) => {
  // ...

  const [ createPerson ] = useMutation(CREATE_PERSON, {
    refetchQueries: [  {query: ALL_PERSONS} ],    onError: (error) => {
      const messages = error.graphQLErrors.map(e => e.message).join('\n')
      setError(messages)
    }
  })copy
```

This approach is pretty good, the drawback being that the query is always rerun with any updates.
It is possible to optimize the solution by handling updating the cache ourselves. This is done by defining a suitable

```
const PersonForm = ({ setError }) => {
  // ...

  const [ createPerson ] = useMutation(CREATE_PERSON, {
    onError: (error) => {
      const messages = error.graphQLErrors.map(e => e.message).join('\n')
      setError(messages)
    },
    update: (cache, response) => {      cache.updateQuery({ query: ALL_PERSONS }, ({ allPersons }) => {        return {          allPersons: allPersons.concat(response.data.addPerson),        }      })    },  })
 
  // ..
}  copy
```

The callback function is given a reference to the cache and the data returned by the mutation as parameters. For example, in our case, this would be the created person.
Using the function
In some situations, the only sensible way to keep the cache up to date is using the _update_ callback.
When necessary, it is possible to disable cache for the whole application or _no-cache_.
Be diligent with the cache. Old data in the cache can cause hard-to-find bugs. As we know, keeping the cache up to date is very challenging. According to a coder proverb:
> _There are only two hard things in Computer Science: cache invalidation and naming things._ Read more
The current code of the application can be found on _part8-5_.
### Exercises 8.17.-8.22
#### 8.17 Listing books
After the backend changes, the list of books does not work anymore. Fix it.
#### 8.18 Log in
Adding new books and changing the birth year of an author do not work because they require a user to be logged in.
Implement login functionality and fix the mutations.
It is not necessary yet to handle validation errors.
You can decide how the login looks on the user interface. One possible solution is to make the login form into a separate view which can be accessed through a navigation menu:
![browser books showing login button highlighted](../assets/91474aa44313df7d.png)
The login form:
![browser showing login form](../assets/1deb4d35c1248dee.png)
When a user is logged in, the navigation changes to show the functionalities which can only be done by a logged-in user:
![browser showing addbook and logout buttons](../assets/fe6412dcd70ed16b.png)
#### 8.19 Books by genre, part 1
Complete your application to filter the book list by genre. Your solution might look something like this:
![browser showing books buttons down at the bottom](../assets/c45bef676bca5a4c.png)
In this exercise, the filtering can be done using just React.
#### 8.20 Books by genre, part 2
Implement a view which shows all the books based on the logged-in user's favourite genre.
![browser showing two books via patterns](../assets/becf4956bfc9dee8.png)
#### 8.21 books by genre with GraphQL
In the previous two exercises, the filtering could have been done using just React. To complete this exercise, you should redo the filtering of the books based on a selected genre (that was done in exercise 8.19) using a GraphQL query to the server. If you already did so then you do not have to do anything.
This and the next exercise are quite **challenging** , like they should be this late in the course. It may help you to complete the easier exercises in the [next part](../part8/01-fragments-and-subscriptions.md) before doing 8.21 and 8.22.
#### 8.22 Up-to-date cache and book recommendations
If you did the previous exercise, that is, fetch the books in a genre with GraphQL, ensure somehow that the books view is kept up to date. So when a new book is added, the books view is updated **at least** when a genre selection button is pressed.
_When new genre selection is not done, the view does not have to be updated._
[Part 8c **Previous part**](../part8/01-database-and-user-administration.md)[Part 8e **Next part**](../part8/01-fragments-and-subscriptions.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)
