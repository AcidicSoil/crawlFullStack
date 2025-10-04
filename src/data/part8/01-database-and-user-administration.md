---{
  "title": "Database and user administration",
  "source_url": "https://fullstackopen.com/en/part8/database_and_user_administration",
  "crawl_timestamp": "2025-10-04T19:17:09Z",
  "checksum": "867f39ba70b42b81c1e45e5cc008b32a32d12a96a004118db67a5f6daddf6fac"
}
---[Skip to content](../part8/01-database-and-user-administration-course-main-content.md)
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
Database and user administration
[a GraphQL-server](../part8/01-graph-ql-server.md)[b React and GraphQL](../part8/01-react-and-graph-ql.md)
c Database and user administration

- [Mongoose and Apollo](../part8/01-database-and-user-administration-mongoose-and-apollo.md)
- [Validation](../part8/01-database-and-user-administration-validation.md)
- [User and log in](../part8/01-database-and-user-administration-user-and-log-in.md)
- [Friends list](../part8/01-database-and-user-administration-friends-list.md)
- [Exercises 8.13.-8.16](../part8/01-database-and-user-administration-exercises-8-13-8-16.md)


[d Login and updating the cache](../part8/01-login-and-updating-the-cache.md)[e Fragments and subscriptions](../part8/01-fragments-and-subscriptions.md)
c
# Database and user administration
We will now add user management to our application, but let's first start using a database for storing data.
### Mongoose and Apollo
Install Mongoose and dotenv:

```
npm install mongoose dotenvcopy
```

We will imitate what we did in parts [3](../part3/01-saving-data-to-mongo-db.md) and [4](../part4/01-structure-of-backend-application-introduction-to-testing.md).
The person schema has been defined as follows:

```
const mongoose = require('mongoose')

const schema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    minlength: 5
  },
  phone: {
    type: String,
    minlength: 5
  },
  street: {
    type: String,
    required: true,
    minlength: 5
  },
  city: {
    type: String,
    required: true,
    minlength: 3
  },
})

module.exports = mongoose.model('Person', schema)copy
```

We also included a few validations. _required: true_ , which makes sure that a value exists, is actually redundant: we already ensure that the fields exist with GraphQL. However, it is good to also keep validation in the database.
We can get the application to mostly work with the following changes:

```
// ...
const mongoose = require('mongoose')
mongoose.set('strictQuery', false)
const Person = require('./models/person')

require('dotenv').config()

const MONGODB_URI = process.env.MONGODB_URI

console.log('connecting to', MONGODB_URI)

mongoose.connect(MONGODB_URI)
  .then(() => {
    console.log('connected to MongoDB')
  })
  .catch((error) => {
    console.log('error connection to MongoDB:', error.message)
  })

const typeDefs = gql`
  ...
`

const resolvers = {
  Query: {
    personCount: async () => Person.collection.countDocuments(),
    allPersons: async (root, args) => {
      // filters missing
      return Person.find({})
    },
    findPerson: async (root, args) => Person.findOne({ name: args.name }),
  },
  Person: {
    address: (root) => {
      return {
        street: root.street,
        city: root.city,
      }
    },
  },
  Mutation: {
    addPerson: async (root, args) => {
      const person = new Person({ ...args })
      return person.save()
    },
    editNumber: async (root, args) => {
      const person = await Person.findOne({ name: args.name })
      person.phone = args.phone
      return person.save()
    },
  },
}copy
```

The changes are pretty straightforward. However, there are a few noteworthy things. As we remember, in Mongo, the identifying field of an object is called __id_ and we previously had to parse the name of the field to _id_ ourselves. Now GraphQL can do this automatically.
Another noteworthy thing is that the resolver functions now return a _promise_ , when they previously returned normal objects. When a resolver returns a promise, Apollo server
For example, if the following resolver function is executed,

```
allPersons: async (root, args) => {
  return Person.find({})
},copy
```

Apollo server waits for the promise to resolve, and returns the result. So Apollo works roughly like this:

```
allPersons: async (root, args) => {
  const result = await Person.find({})
  return result
}copy
```

Let's complete the _allPersons_ resolver so it takes the optional parameter _phone_ into account:

```
Query: {
  // ..
  allPersons: async (root, args) => {
    if (!args.phone) {
      return Person.find({})
    }

    return Person.find({ phone: { $exists: args.phone === 'YES' } })
  },
},copy
```

So if the query has not been given a parameter _phone_ , all persons are returned. If the parameter has the value _YES_ , the result of the query

```
Person.find({ phone: { $exists: true }})copy
```

is returned, so the objects in which the field _phone_ has a value. If the parameter has the value _NO_ , the query returns the objects in which the _phone_ field has no value:

```
Person.find({ phone: { $exists: false }})copy
```

### Validation
As well as in GraphQL, the input is now validated using the validations defined in the mongoose schema. For handling possible validation errors in the schema, we must add an error-handling _try/catch_ block to the _save_ method. When we end up in the catch, we throw an exception

```
Mutation: {
  addPerson: async (root, args) => {
      const person = new Person({ ...args })

      try {        await person.save()      } catch (error) {        throw new GraphQLError('Saving person failed', {          extensions: {            code: 'BAD_USER_INPUT',            invalidArgs: args.name,            error          }        })      }
      return person
  },
    editNumber: async (root, args) => {
      const person = await Person.findOne({ name: args.name })
      person.phone = args.phone

      try {        await person.save()      } catch (error) {        throw new GraphQLError('Saving number failed', {          extensions: {            code: 'BAD_USER_INPUT',            invalidArgs: args.name,            error          }        })      }
      return person
    }
}copy
```

We have also added the Mongoose error and the data that caused the error to the _extensions_ object that is used to convey more info about the cause of the error to the caller. The frontend can then display this information to the user, who can try the operation again with a better input.
The code of the backend can be found on _part8-4_.
### User and log in
Let's add user management to our application. For simplicity's sake, let's assume that all users have the same password which is hardcoded to the system. It would be straightforward to save individual passwords for all users following the principles from [part 4](../part4/01-user-administration.md), but because our focus is on GraphQL, we will leave out all that extra hassle this time.
The user schema is as follows:

```
const mongoose = require('mongoose')

const schema = new mongoose.Schema({
  username: {
    type: String,
    required: true,
    minlength: 3
  },
  friends: [
    {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Person'
    }
  ],
})

module.exports = mongoose.model('User', schema)copy
```

Every user is connected to a bunch of other persons in the system through the _friends_ field. The idea is that when a user, e.g. _mluukkai_ , adds a person, e.g. _Arto Hellas_ , to the list, the person is added to their _friends_ list. This way, logged-in users can have their own personalized view in the application.
Logging in and identifying the user are handled the same way we used in [part 4](../part4/01-token-authentication.md) when we used REST, by using tokens.
Let's extend the schema like so:

```
type User {
  username: String!
  friends: [Person!]!
  id: ID!
}

type Token {
  value: String!
}

type Query {
  // ..
  me: User
}

type Mutation {
  // ...
  createUser(
    username: String!
  ): User
  login(
    username: String!
    password: String!
  ): Token
}copy
```

The query _me_ returns the currently logged-in user. New users are created with the _createUser_ mutation, and logging in happens with the _login_ mutation.
The resolvers of the mutations are as follows:

```
const jwt = require('jsonwebtoken')

Mutation: {
  // ..
  createUser: async (root, args) => {
    const user = new User({ username: args.username })

    return user.save()
      .catch(error => {
        throw new GraphQLError('Creating the user failed', {
          extensions: {
            code: 'BAD_USER_INPUT',
            invalidArgs: args.username,
            error
          }
        })
      })
  },
  login: async (root, args) => {
    const user = await User.findOne({ username: args.username })

    if ( !user || args.password !== 'secret' ) {
      throw new GraphQLError('wrong credentials', {
        extensions: {
          code: 'BAD_USER_INPUT'
        }
      })        
    }

    const userForToken = {
      username: user.username,
      id: user._id,
    }

    return { value: jwt.sign(userForToken, process.env.JWT_SECRET) }
  },
},copy
```

The new user mutation is straightforward. The login mutation checks if the username/password pair is valid. And if it is indeed valid, it returns a jwt token familiar from [part 4](../part4/01-token-authentication.md). Note that the _JWT_SECRET_ must be defined in the _.env_ file.
User creation is done now as follows:

```
mutation {
  createUser (
    username: "mluukkai"
  ) {
    username
    id
  }
}copy
```

The mutation for logging in looks like this:

```
mutation {
  login (
    username: "mluukkai"
    password: "secret"
  ) {
    value
  }
}copy
```

Just like in the previous case with REST, the idea now is that a logged-in user adds a token they receive upon login to all of their requests. And just like with REST, the token is added to GraphQL queries using the _Authorization_ header.
In the Apollo Explorer, the header is added to a query like so:
![apollo explorer highlighting headers with authorization and bearer token](../assets/a59cae1780ec6d5f.png)
Modify the startup of the backend by giving the function that handles the startup

```
startStandaloneServer(server, {
  listen: { port: 4000 },
  context: async ({ req, res }) => {    const auth = req ? req.headers.authorization : null    if (auth && auth.startsWith('Bearer ')) {      const decodedToken = jwt.verify(        auth.substring(7), process.env.JWT_SECRET      )      const currentUser = await User        .findById(decodedToken.id).populate('friends')      return { currentUser }    }  },}).then(({ url }) => {
  console.log(`Server ready at ${url}`)
})copy
```

The object returned by context is given to all resolvers as their _third parameter_. Context is the right place to do things which are shared by multiple resolvers, like
So our code sets the object corresponding to the user who made the request to the _currentUser_ field of the context. If there is no user connected to the request, the value of the field is undefined.
The resolver of the _me_ query is very simple: it just returns the logged-in user it receives in the _currentUser_ field of the third parameter of the resolver, _context_. It's worth noting that if there is no logged-in user, i.e. there is no valid token in the header attached to the request, the query returns _null_ :

```
Query: {
  // ...
  me: (root, args, context) => {
    return context.currentUser
  }
},copy
```

If the header has the correct value, the query returns the user information identified by the header
![apollo studio showing query response object](../assets/a2fe2cdd34c93b74.png)
### Friends list
Let's complete the application's backend so that adding and editing persons requires logging in, and added persons are automatically added to the friends list of the user.
Let's first remove all persons not in anyone's friends list from the database.
_addPerson_ mutation changes like so:

```
Mutation: {
    addPerson: async (root, args, context) => {      const person = new Person({ ...args })
      const currentUser = context.currentUser
      if (!currentUser) {        throw new GraphQLError('not authenticated', {          extensions: {            code: 'BAD_USER_INPUT',          }        })      }
      try {
        await person.save()
        currentUser.friends = currentUser.friends.concat(person)        await currentUser.save()      } catch (error) {
        throw new GraphQLError('Saving user failed', {
          extensions: {
            code: 'BAD_USER_INPUT',
            invalidArgs: args.name,
            error
          }
        })
      }
      
      return person
    },
  //...
}copy
```

If a logged-in user cannot be found from the context, an _GraphQLError_ with a proper message is thrown. Creating new persons is now done with _async/await_ syntax, because if the operation is successful, the created person is added to the friends list of the user.
Let's also add functionality for adding an existing user to your friends list. The mutation is as follows:

```
type Mutation {
  // ...
  addAsFriend(
    name: String!
  ): User
}copy
```

And the mutation's resolver:

```
  addAsFriend: async (root, args, { currentUser }) => {
    const isFriend = (person) => 
      currentUser.friends.map(f => f._id.toString()).includes(person._id.toString())

    if (!currentUser) {
      throw new GraphQLError('wrong credentials', {
        extensions: { code: 'BAD_USER_INPUT' }
      }) 
    }

    const person = await Person.findOne({ name: args.name })
    if ( !isFriend(person) ) {
      currentUser.friends = currentUser.friends.concat(person)
    }

    await currentUser.save()

    return currentUser
  },copy
```

Note how the resolver _destructures_ the logged-in user from the context. So instead of saving _currentUser_ to a separate variable in a function

```
addAsFriend: async (root, args, context) => {
  const currentUser = context.currentUsercopy
```

it is received straight in the parameter definition of the function:

```
addAsFriend: async (root, args, { currentUser }) => {copy
```

The following query now returns the user's friends list:

```
query {
  me {
    username
    friends{
      name
      phone
    }
  }
}copy
```

The code of the backend can be found on _part8-5_.
### Exercises 8.13.-8.16
The following exercises are quite likely to break your frontend. Do not worry about it yet; the frontend shall be fixed and expanded in the next chapter.
#### 8.13: Database, part 1
Change the library application so that it saves the data to a database. You can find the _mongoose schema_ for books and authors from
Let's change the book graphql schema a little

```
type Book {
  title: String!
  published: Int!
  author: Author!  genres: [String!]!
  id: ID!
}copy
```

so that instead of just the author's name, the book object contains all the details of the author.
You can assume that the user will not try to add faulty books or authors, so you don't have to care about validation errors.
The following things do _not_ have to work just yet:

- _allBooks_ query with parameters
- _bookCount_ field of an author object
- _author_ field of a book
- _editAuthor_ mutation


**Note** : despite the fact that author is now an _object_ within a book, the schema for adding a book can remain same, only the _name_ of the author is given as a parameter

```
type Mutation {
  addBook(
    title: String!
    author: String!    published: Int!
    genres: [String!]!
  ): Book!
  editAuthor(name: String!, setBornTo: Int!): Author
}copy
```

#### 8.14: Database, part 2
Complete the program so that all queries (to get _allBooks_ working with the parameter _author_ and _bookCount_ field of an author object is not required) and mutations work.
Regarding the _genre_ parameter of the all books query, the situation is a bit more challenging. The solution is simple, but finding it can be a headache. You might benefit from
#### 8.15 Database, part 3
Complete the program so that database validation errors (e.g. book title or author name being too short) are handled sensibly. This means that they cause
#### 8.16 user and logging in
Add user management to your application. Expand the schema like so:

```
type User {
  username: String!
  favoriteGenre: String!
  id: ID!
}

type Token {
  value: String!
}

type Query {
  // ..
  me: User
}

type Mutation {
  // ...
  createUser(
    username: String!
    favoriteGenre: String!
  ): User
  login(
    username: String!
    password: String!
  ): Token
}copy
```

Create resolvers for query _me_ and the new mutations _createUser_ and _login_. Like in the course material, you can assume all users have the same hardcoded password.
Make the mutations _addBook_ and _editAuthor_ possible only if the request includes a valid token.
(Don't worry about fixing the frontend for the moment.)
[Part 8b **Previous part**](../part8/01-react-and-graph-ql.md)[Part 8d **Next part**](../part8/01-login-and-updating-the-cache.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)
