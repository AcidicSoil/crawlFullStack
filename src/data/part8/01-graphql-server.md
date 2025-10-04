---{
  "title": "GraphQL-server",
  "source_url": "https://fullstackopen.com/en/part8/graph_ql_server",
  "crawl_timestamp": "2025-10-04T19:17:12Z",
  "checksum": "6e97f94ff3d18f439e6142bf68a81de289c5d1469d8104cd2a874cd762cef37d"
}
---[Skip to content](../part8/01-graph-ql-server-course-main-content.md)
[{() => fs}](https://fullstackopen.com/en/)
  * [About course](../about/01-about.md)
  * [Course contents](../#course-contents/01-course-contents.md)
  * [FAQ](../faq/01-faq.md)
  * [Partners](../companies/01-companies.md)
  * [Challenge](../challenge/01-challenge.md)
[Search from the material](../search/01-search.md)Toggle dark theme
Select languageSuomi English 中文 Español Français Português(BR) 

[Fullstack](../#course-contents/01-course-contents.md)
[Part 8](../part8/01-part8.md)
GraphQL-server
a GraphQL-server
  * [Schemas and queries](../part8/01-graph-ql-server-schemas-and-queries.md)
  * [Apollo Server](../part8/01-graph-ql-server-apollo-server.md)
  * [Apollo Studio Explorer](../part8/01-graph-ql-server-apollo-studio-explorer.md)
  * [Parameters of a resolver](../part8/01-graph-ql-server-parameters-of-a-resolver.md)
  * [The default resolver](../part8/01-graph-ql-server-the-default-resolver.md)
  * [Object within an object](../part8/01-graph-ql-server-object-within-an-object.md)
  * [Mutations](../part8/01-graph-ql-server-mutations.md)
  * [Error handling](../part8/01-graph-ql-server-error-handling.md)
  * [Enum](../part8/01-graph-ql-server-enum.md)
  * [Changing a phone number](../part8/01-graph-ql-server-changing-a-phone-number.md)
  * [More on queries](../part8/01-graph-ql-server-more-on-queries.md)
  * [Exercises 8.1.-8.7](../part8/01-graph-ql-server-exercises-8-1-8-7.md)


[b React and GraphQL](../part8/01-react-and-graph-ql.md)[c Database and user administration](../part8/01-database-and-user-administration.md)[d Login and updating the cache](../part8/01-login-and-updating-the-cache.md)[e Fragments and subscriptions](../part8/01-fragments-and-subscriptions.md)
a
# GraphQL-server
REST, familiar to us from the previous parts of the course, has long been the most prevalent way to implement the interfaces servers offer for browsers, and in general the integration between different applications on the web.
In recent years, 
The GraphQL philosophy is very different from REST. REST is _resource-based_. Every resource, for example a _user_ , has its own address which identifies it, for example _/users/10_. All operations done to the resource are done with HTTP requests to its URL. The action depends on the HTTP method used.
The resource-basedness of REST works well in most situations. However, it can be a bit awkward sometimes.
Let's consider the following example: our bloglist application contains some kind of social media functionality, and we would like to show a list of all the blogs that were added by users who have commented on any of the blogs of the users we follow.
If the server implemented a REST API, we would probably have to do multiple HTTP requests from the browser before we had all the data we wanted. The requests would also return a lot of unnecessary data, and the code on the browser would probably be quite complicated.
If this was an often-used functionality, there could be a REST endpoint for it. If there were a lot of these kinds of scenarios however, it would become very laborious to implement REST endpoints for all of them.
A GraphQL server is well-suited for these kinds of situations.
The main principle of GraphQL is that the code on the browser forms a _query_ describing the data wanted, and sends it to the API with an HTTP POST request. Unlike REST, all GraphQL queries are sent to the same address, and their type is POST.
The data described in the above scenario could be fetched with (roughly) the following query:
```
query FetchBlogsQuery {
  user(username: "mluukkai") {
    followedUsers {
      blogs {
        comments {
          user {
            blogs {
              title
            }
          }
        }
      }
    }
  }
}copy
```

The content of the `FetchBlogsQuery` can be roughly interpreted as: find a user named `"mluukkai"` and for each of his `followedUsers`, find all their `blogs`, and for each blog, all its `comments`, and for each `user` who wrote each comment, find their `blogs`, and return the `title` of each of them.
The server's response would be about the following JSON object:
```
{
  "data": {
    "followedUsers": [
      {
        "blogs": [
          {
            "comments": [
              {
                "user": {
                  "blogs": [
                    {
                      "title": "Goto considered harmful"
                    },
                    {
                      "title": "End to End Testing with Cypress is most enjoyable"
                    },
                    {
                      "title": "Navigating your transition to GraphQL"
                    },
                    {
                      "title": "From REST to GraphQL"
                    }
                  ]
                }
              }
            ]
          }
        ]
      }
    ]
  }
}copy
```

The application logic stays simple, and the code on the browser gets exactly the data it needs with a single query.
### Schemas and queries
We will get to know the basics of GraphQL by implementing a GraphQL version of the phonebook application from parts 2 and 3.
In the heart of all GraphQL applications is a 
```
type Person {
  name: String!
  phone: String
  street: String!
  city: String!
  id: ID! 
}

type Query {
  personCount: Int!
  allPersons: [Person!]!
  findPerson(name: String!): Person
}copy
```

The schema describes two _Person_ , determines that persons have five fields. Four of the fields are type _String_ , which is one of the _phone_ , must be given a value. This is marked by the exclamation mark on the schema. The type of the field _id_ is _ID_. _ID_ fields are strings, but GraphQL ensures they are unique. 
The second type is a 
The phonebook describes three different queries. _personCount_ returns an integer, _allPersons_ returns a list of _Person_ objects and _findPerson_ is given a string parameter and it returns a _Person_ object.
Again, exclamation marks are used to mark which return values and parameters are _Non-Null_. _personCount_ will, for sure, return an integer. The query _findPerson_ must be given a string as a parameter. The query returns a _Person_ -object or _null_. _allPersons_ returns a list of _Person_ objects, and the list does not contain any _null_ values.
So the schema describes what queries the client can send to the server, what kind of parameters the queries can have, and what kind of data the queries return.
The simplest of the queries, _personCount_ , looks as follows:
```
query {
  personCount
}copy
```

Assuming our application has saved the information of three people, the response would look like this:
```
{
  "data": {
    "personCount": 3
  }
}copy
```

The query fetching the information of all of the people, _allPersons_ , is a bit more complicated. Because the query returns a list of _Person_ objects, the query must describe _which_ of the objects the query returns:
```
query {
  allPersons {
    name
    phone
  }
}copy
```

The response could look like this:
```
{
  "data": {
    "allPersons": [
      {
        "name": "Arto Hellas",
        "phone": "040-123543"
      },
      {
        "name": "Matti Luukkainen",
        "phone": "040-432342"
      },
      {
        "name": "Venla Ruuska",
        "phone": null
      }
    ]
  }
}copy
```

A query can be made to return any field described in the schema. For example, the following would also be possible:
```
query {
  allPersons{
    name
    city
    street
  }
}copy
```

The last example shows a query which requires a parameter, and returns the details of one person.
```
query {
  findPerson(name: "Arto Hellas") {
    phone 
    city 
    street
    id
  }
}copy
```

So, first, the parameter is described in round brackets, and then the fields of the return value object are listed in curly brackets.
The response is like this:
```
{
  "data": {
    "findPerson": {
      "phone": "040-123543",
      "city": "Espoo",
      "street": "Tapiolankatu 5 A"
      "id": "3d594650-3436-11e9-bc57-8b80ba54c431"
    }
  }
}copy
```

The return value was marked as nullable, so if we search for the details of an unknown
```
query {
  findPerson(name: "Joe Biden") {
    phone 
  }
}copy
```

the return value is _null_.
```
{
  "data": {
    "findPerson": null
  }
}copy
```

As you can see, there is a direct link between a GraphQL query and the returned JSON object. One can think that the query describes what kind of data it wants as a response. The difference to REST queries is stark. With REST, the URL and the type of the request have nothing to do with the form of the returned data.
GraphQL query describes only the data moving between a server and the client. On the server, the data can be organized and saved any way we like.
Despite its name, GraphQL does not actually have anything to do with databases. It does not care how the data is saved. The data a GraphQL API uses can be saved into a relational database, document database, or to other servers which a GraphQL server can access with for example REST.
### Apollo Server
Let's implement a GraphQL server with today's leading library: 
Create a new npm project with _npm init_ and install the required dependencies.
```
npm install @apollo/server graphqlcopy
```

Also create a `index.js` file in your project's root directory.
The initial code is as follows:
```
const { ApolloServer } = require('@apollo/server')
const { startStandaloneServer } = require('@apollo/server/standalone')

let persons = [
  {
    name: "Arto Hellas",
    phone: "040-123543",
    street: "Tapiolankatu 5 A",
    city: "Espoo",
    id: "3d594650-3436-11e9-bc57-8b80ba54c431"
  },
  {
    name: "Matti Luukkainen",
    phone: "040-432342",
    street: "Malminkaari 10 A",
    city: "Helsinki",
    id: '3d599470-3436-11e9-bc57-8b80ba54c431'
  },
  {
    name: "Venla Ruuska",
    street: "Nallemäentie 22 C",
    city: "Helsinki",
    id: '3d599471-3436-11e9-bc57-8b80ba54c431'
  },
]

const typeDefs = `
  type Person {
    name: String!
    phone: String
    street: String!
    city: String! 
    id: ID!
  }

  type Query {
    personCount: Int!
    allPersons: [Person!]!
    findPerson(name: String!): Person
  }
`

const resolvers = {
  Query: {
    personCount: () => persons.length,
    allPersons: () => persons,
    findPerson: (root, args) =>
      persons.find(p => p.name === args.name)
  }
}

const server = new ApolloServer({
  typeDefs,
  resolvers,
})

startStandaloneServer(server, {
  listen: { port: 4000 },
}).then(({ url }) => {
  console.log(`Server ready at ${url}`)
})copy
```

The heart of the code is an 
```
const server = new ApolloServer({
  typeDefs,
  resolvers,
})copy
```

The first parameter, _typeDefs_ , contains the GraphQL schema.
The second parameter is an object, which contains the _how_ GraphQL queries are responded to.
The code of the resolvers is the following:
```
const resolvers = {
  Query: {
    personCount: () => persons.length,
    allPersons: () => persons,
    findPerson: (root, args) =>
      persons.find(p => p.name === args.name)
  }
}copy
```

As you can see, the resolvers correspond to the queries described in the schema.
```
type Query {
  personCount: Int!
  allPersons: [Person!]!
  findPerson(name: String!): Person
}copy
```

So there is a field under _Query_ for every query described in the schema.
The query
```
query {
  personCount
}copy
```

Has the resolver
```
() => persons.lengthcopy
```

So the response to the query is the length of the array _persons_.
The query which fetches all persons
```
query {
  allPersons {
    name
  }
}copy
```

has a resolver which returns _all_ objects from the _persons_ array.
```
() => personscopy
```

Start the server by running `node index.js` in the terminal.
### Apollo Studio Explorer
When Apollo server is run in development mode the page _Query your server_ that takes us to 
Let's try it out:
![apollo studio Example Query with response allPersons](../assets/64ab5073393a9665.png)
At the left side Explorer shows the API-documentation that it has automatically generated based on the schema.
### Parameters of a resolver
The query fetching a single person
```
query {
  findPerson(name: "Arto Hellas") {
    phone 
    city 
    street
  }
}copy
```

has a resolver which differs from the previous ones because it is given _two parameters_ :
```
(root, args) => persons.find(p => p.name === args.name)copy
```

The second parameter, _args_ , contains the parameters of the query. The resolver then returns from the array _persons_ the person whose name is the same as the value of _args.name_. The resolver does not need the first parameter _root_.
In fact, all resolver functions are given 
### The default resolver
When we do a query, for example
```
query {
  findPerson(name: "Arto Hellas") {
    phone 
    city 
    street
  }
}copy
```

the server knows to send back exactly the fields required by the query. How does that happen?
A GraphQL server must define resolvers for _each_ field of each type in the schema. We have so far only defined resolvers for fields of the type _Query_ , so for each query of the application.
Because we did not define resolvers for the fields of the type _Person_ , Apollo has defined 
```
const resolvers = {
  Query: {
    personCount: () => persons.length,
    allPersons: () => persons,
    findPerson: (root, args) => persons.find(p => p.name === args.name)
  },
  Person: {    name: (root) => root.name,    phone: (root) => root.phone,    street: (root) => root.street,    city: (root) => root.city,    id: (root) => root.id  }}copy
```

The default resolver returns the value of the corresponding field of the object. The object itself can be accessed through the first parameter of the resolver, _root_.
If the functionality of the default resolver is enough, you don't need to define your own. It is also possible to define resolvers for only some fields of a type, and let the default resolvers handle the rest.
We could for example define that the address of all persons is _Manhattan New York_ by hard-coding the following to the resolvers of the street and city fields of the type _Person_ :
```
Person: {
  street: (root) => "Manhattan",
  city: (root) => "New York"
}copy
```

### Object within an object
Let's modify the schema a bit
```
type Address {  street: String!  city: String! }
type Person {
  name: String!
  phone: String
  address: Address!  id: ID!
}

type Query {
  personCount: Int!
  allPersons: [Person!]!
  findPerson(name: String!): Person
}copy
```

so a person now has a field with the type _Address_ , which contains the street and the city.
The queries requiring the address change into
```
query {
  findPerson(name: "Arto Hellas") {
    phone 
    address {
      city 
      street
    }
  }
}copy
```

and the response is now a person object, which _contains_ an address object.
```
{
  "data": {
    "findPerson": {
      "phone": "040-123543",
      "address":  {
        "city": "Espoo",
        "street": "Tapiolankatu 5 A"
      }
    }
  }
}copy
```

We still save the persons in the server the same way we did before.
```
let persons = [
  {
    name: "Arto Hellas",
    phone: "040-123543",
    street: "Tapiolankatu 5 A",
    city: "Espoo",
    id: "3d594650-3436-11e9-bc57-8b80ba54c431"
  },
  // ...
]copy
```

The person-objects saved in the server are not exactly the same as the GraphQL type _Person_ objects described in the schema.
Contrary to the _Person_ type, the _Address_ type does not have an _id_ field, because they are not saved into their own separate data structure in the server.
Because the objects saved in the array do not have an _address_ field, the default resolver is not sufficient. Let's add a resolver for the _address_ field of _Person_ type :
```
const resolvers = {
  Query: {
    personCount: () => persons.length,
    allPersons: () => persons,
    findPerson: (root, args) =>
      persons.find(p => p.name === args.name)
  },
  Person: {    address: (root) => {      return {         street: root.street,        city: root.city      }    }  }}copy
```

So every time a _Person_ object is returned, the fields _name_ , _phone_ and _id_ are returned using their default resolvers, but the field _address_ is formed by using a self-defined resolver. The parameter _root_ of the resolver function is the person-object, so the street and the city of the address can be taken from its fields.
The current code of the application can be found on _part8-1_.
### Mutations
Let's add a functionality for adding new persons to the phonebook. In GraphQL, all operations which cause a change are done with _Mutation_.
The schema for a mutation for adding a new person looks as follows:
```
type Mutation {
  addPerson(
    name: String!
    phone: String
    street: String!
    city: String!
  ): Person
}copy
```

The Mutation is given the details of the person as parameters. The parameter _phone_ is the only one which is nullable. The Mutation also has a return value. The return value is type _Person_ , the idea being that the details of the added person are returned if the operation is successful and if not, null. Value for the field _id_ is not given as a parameter. Generating an id is better left for the server.
Mutations also require a resolver:
```
const { v1: uuid } = require('uuid')

// ...

const resolvers = {
  // ...
  Mutation: {
    addPerson: (root, args) => {
      const person = { ...args, id: uuid() }
      persons = persons.concat(person)
      return person
    }
  }
}copy
```

The mutation adds the object given to it as a parameter _args_ to the array _persons_ , and returns the object it added to the array.
The _id_ field is given a unique value using the 
A new person can be added with the following mutation
```
mutation {
  addPerson(
    name: "Pekka Mikkola"
    phone: "045-2374321"
    street: "Vilppulantie 25"
    city: "Helsinki"
  ) {
    name
    phone
    address{
      city
      street
    }
    id
  }
}copy
```

Note that the person is saved to the _persons_ array as
```
{
  name: "Pekka Mikkola",
  phone: "045-2374321",
  street: "Vilppulantie 25",
  city: "Helsinki",
  id: "2b24e0b0-343c-11e9-8c2a-cb57c2bf804f"
}copy
```

But the response to the mutation is
```
{
  "data": {
    "addPerson": {
      "name": "Pekka Mikkola",
      "phone": "045-2374321",
      "address": {
        "city": "Helsinki",
        "street": "Vilppulantie 25"
      },
      "id": "2b24e0b0-343c-11e9-8c2a-cb57c2bf804f"
    }
  }
}copy
```

So the resolver of the _address_ field of the _Person_ type formats the response object to the right form.
### Error handling
If we try to create a new person, but the parameters do not correspond with the schema description, the server gives an error message:
![apollo showing error with addPerson GRAPHQL VALIDATION FAILED](../assets/234ba43e5087bcdd.png)
So some of the error handling can be automatically done with GraphQL 
However, GraphQL cannot handle everything automatically. For example, stricter rules for data sent to a Mutation have to be added manually. An error could be handled by throwing 
Let's prevent adding the same name to the phonebook multiple times:
```
const { GraphQLError } = require('graphql')
// ...

const resolvers = {
  // ..
  Mutation: {
    addPerson: (root, args) => {
      if (persons.find(p => p.name === args.name)) {        throw new GraphQLError('Name must be unique', {          extensions: {            code: 'BAD_USER_INPUT',            invalidArgs: args.name          }        })      }
      const person = { ...args, id: uuid() }
      persons = persons.concat(person)
      return person
    }
  }
}copy
```

So if the name to be added already exists in the phonebook, throw _GraphQLError_ error.
![apollo showing error BAD_USER_INPUT](../assets/8015df54d44525aa.png)
The current code of the application can be found on _part8-2_.
### Enum
Let's add a possibility to filter the query returning all persons with the parameter _phone_ so that it returns only persons with a phone number
```
query {
  allPersons(phone: YES) {
    name
    phone 
  }
}copy
```

or persons without a phone number
```
query {
  allPersons(phone: NO) {
    name
  }
}copy
```

The schema changes like so:
```
enum YesNo {  YES  NO}
type Query {
  personCount: Int!
  allPersons(phone: YesNo): [Person!]!  findPerson(name: String!): Person
}copy
```

The type _YesNo_ is a GraphQL _YES_ or _NO_. In the query _allPersons_ , the parameter _phone_ has the type _YesNo_ , but is nullable.
The resolver changes like so:
```
Query: {
  personCount: () => persons.length,
  allPersons: (root, args) => {    if (!args.phone) {      return persons    }    const byPhone = (person) =>      args.phone === 'YES' ? person.phone : !person.phone    return persons.filter(byPhone)  },  findPerson: (root, args) =>
    persons.find(p => p.name === args.name)
},copy
```

### Changing a phone number
Let's add a mutation for changing the phone number of a person. The schema of this mutation looks as follows:
```
type Mutation {
  addPerson(
    name: String!
    phone: String
    street: String!
    city: String!
  ): Person
  editNumber(    name: String!    phone: String!  ): Person}copy
```

and is done by a resolver:
```
Mutation: {
  // ...
  editNumber: (root, args) => {
    const person = persons.find(p => p.name === args.name)
    if (!person) {
      return null
    }

    const updatedPerson = { ...person, phone: args.phone }
    persons = persons.map(p => p.name === args.name ? updatedPerson : p)
    return updatedPerson
  }   
}copy
```

The mutation finds the person to be updated by the field _name_.
The current code of the application can be found on _part8-3_.
### More on queries
With GraphQL, it is possible to combine multiple fields of type _Query_ , or "separate queries" into one query. For example, the following query returns both the amount of persons in the phonebook and their names:
```
query {
  personCount
  allPersons {
    name
  }
}copy
```

The response looks as follows:
```
{
  "data": {
    "personCount": 3,
    "allPersons": [
      {
        "name": "Arto Hellas"
      },
      {
        "name": "Matti Luukkainen"
      },
      {
        "name": "Venla Ruuska"
      }
    ]
  }
}copy
```

Combined query can also use the same query multiple times. You must however give the queries alternative names like so:
```
query {
  havePhone: allPersons(phone: YES){
    name
  }
  phoneless: allPersons(phone: NO){
    name
  }
}copy
```

The response looks like:
```
{
  "data": {
    "havePhone": [
      {
        "name": "Arto Hellas"
      },
      {
        "name": "Matti Luukkainen"
      }
    ],
    "phoneless": [
      {
        "name": "Venla Ruuska"
      }
    ]
  }
}copy
```

In some cases, it might be beneficial to name the queries. This is the case especially when the queries or mutations have 
### Exercises 8.1.-8.7
Through the exercises, we will implement a GraphQL backend for a small library. Start with _npm init_ and to install dependencies!
#### 8.1: The number of books and authors
Implement queries _bookCount_ and _authorCount_ which return the number of books and the number of authors.
The query
```
query {
  bookCount
  authorCount
}copy
```

should return
```
{
  "data": {
    "bookCount": 7,
    "authorCount": 5
  }
}copy
```

#### 8.2: All books
Implement query _allBooks_ , which returns the details of all books.
In the end, the user should be able to do the following query:
```
query {
  allBooks { 
    title 
    author
    published 
    genres
  }
}copy
```

#### 8.3: All authors
Implement query _allAuthors_ , which returns the details of all authors. The response should include a field _bookCount_ containing the number of books the author has written.
For example the query
```
query {
  allAuthors {
    name
    bookCount
  }
}copy
```

should return
```
{
  "data": {
    "allAuthors": [
      {
        "name": "Robert Martin",
        "bookCount": 2
      },
      {
        "name": "Martin Fowler",
        "bookCount": 1
      },
      {
        "name": "Fyodor Dostoevsky",
        "bookCount": 2
      },
      {
        "name": "Joshua Kerievsky",
        "bookCount": 1
      },
      {
        "name": "Sandi Metz",
        "bookCount": 1
      }
    ]
  }
}copy
```

#### 8.4: Books of an author
Modify the _allBooks_ query so that a user can give an optional parameter _author_. The response should include only books written by that author.
For example query
```
query {
  allBooks(author: "Robert Martin") {
    title
  }
}copy
```

should return
```
{
  "data": {
    "allBooks": [
      {
        "title": "Clean Code"
      },
      {
        "title": "Agile software development"
      }
    ]
  }
}copy
```

#### 8.5: Books by genre
Modify the query _allBooks_ so that a user can give an optional parameter _genre_. The response should include only books of that genre.
For example query
```
query {
  allBooks(genre: "refactoring") {
    title
    author
  }
}copy
```

should return
```
{
  "data": {
    "allBooks": [
      {
        "title": "Clean Code",
        "author": "Robert Martin"
      },
      {
        "title": "Refactoring, edition 2",
        "author": "Martin Fowler"
      },
      {
        "title": "Refactoring to patterns",
        "author": "Joshua Kerievsky"
      },
      {
        "title": "Practical Object-Oriented Design, An Agile Primer Using Ruby",
        "author": "Sandi Metz"
      }
    ]
  }
}copy
```

The query must work when both optional parameters are given:
```
query {
  allBooks(author: "Robert Martin", genre: "refactoring") {
    title
    author
  }
}copy
```

#### 8.6: Adding a book
Implement mutation _addBook_ , which can be used like this:
```
mutation {
  addBook(
    title: "NoSQL Distilled",
    author: "Martin Fowler",
    published: 2012,
    genres: ["database", "nosql"]
  ) {
    title,
    author
  }
}copy
```

The mutation works even if the author is not already saved to the server:
```
mutation {
  addBook(
    title: "Pimeyden tango",
    author: "Reijo Mäki",
    published: 1997,
    genres: ["crime"]
  ) {
    title,
    author
  }
}copy
```

If the author is not yet saved to the server, a new author is added to the system. The birth years of authors are not saved to the server yet, so the query
```
query {
  allAuthors {
    name
    born
    bookCount
  }
}copy
```

returns
```
{
  "data": {
    "allAuthors": [
      // ...
      {
        "name": "Reijo Mäki",
        "born": null,
        "bookCount": 1
      }
    ]
  }
}copy
```

#### 8.7: Updating the birth year of an author
Implement mutation _editAuthor_ , which can be used to set a birth year for an author. The mutation is used like so:
```
mutation {
  editAuthor(name: "Reijo Mäki", setBornTo: 1958) {
    name
    born
  }
}copy
```

If the correct author is found, the operation returns the edited author:
```
{
  "data": {
    "editAuthor": {
      "name": "Reijo Mäki",
      "born": 1958
    }
  }
}copy
```

If the author is not in the system, _null_ is returned:
```
{
  "data": {
    "editAuthor": null
  }
}copy
```

[ Part 7 **Previous part** ](../part7/01-part7.md)[ Part 8b **Next part** ](../part8/01-react-and-graph-ql.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)