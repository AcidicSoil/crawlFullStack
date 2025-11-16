---{
  "title": "User administration",
  "source_url": "https://fullstackopen.com/en/part4/user_administration",
  "crawl_timestamp": "2025-10-04T19:16:34Z",
  "checksum": "8849532fbdc1c5f1461bc452522e513d9729d510d1164653fbffb1a0f196ade3"
}
---[Skip to content](../part4/01-user-administration-course-main-content.md)
[{() => fs}](https://fullstackopen.com/en/)

- [About course](../about/01-about.md)
- [Course contents](../#course-contents/01-course-contents.md)
- [FAQ](../faq/01-faq.md)
- [Partners](../companies/01-companies.md)
- [Challenge](../challenge/01-challenge.md)
[Search from the material](../search/01-search.md)Toggle dark theme
Select languageSuomi English 中文 Español Français Português(BR)

[Fullstack](../#course-contents/01-course-contents.md)
[Part 4](../part4/01-part4.md)
User administration
[a Structure of backend application, introduction to testing](../part4/01-structure-of-backend-application-introduction-to-testing.md)[b Testing the backend](../part4/01-testing-the-backend.md)
c User administration

- [References across collections](../part4/01-user-administration-references-across-collections.md)
- [Mongoose schema for users](../part4/01-user-administration-mongoose-schema-for-users.md)
- [Creating users](../part4/01-user-administration-creating-users.md)
- [Creating a new note](../part4/01-user-administration-creating-a-new-note.md)
- [Populate](../part4/01-user-administration-populate.md)


[d Token authentication](../part4/01-token-authentication.md)
c
# User administration
We want to add user authentication and authorization to our application. Users should be stored in the database and every note should be linked to the user who created it. Deleting and editing a note should only be allowed for the user who created it.
Let's start by adding information about users to the database. There is a one-to-many relationship between the user (_User_) and notes (_Note_):
![diagram linking user and notes](../assets/e042900de20930b0.png)
If we were working with a relational database the implementation would be straightforward. Both resources would have their separate database tables, and the id of the user who created a note would be stored in the notes table as a foreign key.
When working with document databases the situation is a bit different, as there are many different ways of modeling the situation.
The existing solution saves every note in the _notes collection_ in the database. If we do not want to change this existing collection, then the natural choice is to save users in their own collection, _users_ for example.
Like with all document databases, we can use object IDs in Mongo to reference documents in other collections. This is similar to using foreign keys in relational databases.
Traditionally document databases like Mongo do not support _join queries_ that are available in relational databases, used for aggregating data from multiple tables. However, starting from version 3.2. Mongo has supported
If we need functionality similar to join queries, we will implement it in our application code by making multiple queries. In certain situations, Mongoose can take care of joining and aggregating data, which gives the appearance of a join query. However, even in these situations, Mongoose makes multiple queries to the database in the background.
### References across collections
If we were using a relational database the note would contain a _reference key_ to the user who created it. In document databases, we can do the same thing.
Let's assume that the _users_ collection contains two users:

```
[
  {
    username: 'mluukkai',
    _id: 123456,
  },
  {
    username: 'hellas',
    _id: 141414,
  },
]copy
```

The _notes_ collection contains three notes that all have a _user_ field that references a user in the _users_ collection:

```
[
  {
    content: 'HTML is easy',
    important: false,
    _id: 221212,
    user: 123456,
  },
  {
    content: 'The most important operations of HTTP protocol are GET and POST',
    important: true,
    _id: 221255,
    user: 123456,
  },
  {
    content: 'A proper dinosaur codes with Java',
    important: false,
    _id: 221244,
    user: 141414,
  },
]copy
```

Document databases do not demand the foreign key to be stored in the note resources, it could _also_ be stored in the users collection, or even both:

```
[
  {
    username: 'mluukkai',
    _id: 123456,
    notes: [221212, 221255],
  },
  {
    username: 'hellas',
    _id: 141414,
    notes: [221244],
  },
]copy
```

Since users can have many notes, the related ids are stored in an array in the _notes_ field.
Document databases also offer a radically different way of organizing the data: In some situations, it might be beneficial to nest the entire notes array as a part of the documents in the users collection:

```
[
  {
    username: 'mluukkai',
    _id: 123456,
    notes: [
      {
        content: 'HTML is easy',
        important: false,
      },
      {
        content: 'The most important operations of HTTP protocol are GET and POST',
        important: true,
      },
    ],
  },
  {
    username: 'hellas',
    _id: 141414,
    notes: [
      {
        content:
          'A proper dinosaur codes with Java',
        important: false,
      },
    ],
  },
]copy
```

In this schema, notes would be tightly nested under users and the database would not generate ids for them.
The structure and schema of the database are not as self-evident as it was with relational databases. The chosen schema must support the use cases of the application the best. This is not a simple design decision to make, as all use cases of the applications are not known when the design decision is made.
Paradoxically, schema-less databases like Mongo require developers to make far more radical design decisions about data organization at the beginning of the project than relational databases with schemas. On average, relational databases offer a more or less suitable way of organizing data for many applications.
### Mongoose schema for users
In this case, we decide to store the ids of the notes created by the user in the user document. Let's define the model for representing a user in the _models/user.js_ file:

```
const mongoose = require('mongoose')

const userSchema = new mongoose.Schema({
  username: String,
  name: String,
  passwordHash: String,
  notes: [
    {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Note'
    }
  ],
})

userSchema.set('toJSON', {
  transform: (document, returnedObject) => {
    returnedObject.id = returnedObject._id.toString()
    delete returnedObject._id
    delete returnedObject.__v
    // the passwordHash should not be revealed
    delete returnedObject.passwordHash
  }
})

const User = mongoose.model('User', userSchema)

module.exports = Usercopy
```

The ids of the notes are stored within the user document as an array of Mongo ids. The definition is as follows:

```
{
  type: mongoose.Schema.Types.ObjectId,
  ref: 'Note'
}copy
```

The field type is _ObjectId_ , meaning it refers to another document. The _ref_ field specifies the name of the model being referenced. Mongo does not inherently know that this is a field that references notes, the syntax is purely related to and defined by Mongoose.
Let's expand the schema of the note defined in the _models/note.js_ file so that the note contains information about the user who created it:

```
const noteSchema = new mongoose.Schema({
  content: {
    type: String,
    required: true,
    minlength: 5
  },
  important: Boolean,
  user: {    type: mongoose.Schema.Types.ObjectId,    ref: 'User'  }})copy
```

In stark contrast to the conventions of relational databases, _references are now stored in both documents_ : the note references the user who created it, and the user has an array of references to all of the notes created by them.
### Creating users
Let's implement a route for creating new users. Users have a unique _username_ , a _name_ and something called a _passwordHash_. The password hash is the output of a
Let's install the

```
npm install bcryptcopy
```

Creating new users happens in compliance with the RESTful conventions discussed in [part 3](../part3/01-node-js-and-express-rest.md), by making an HTTP POST request to the _users_ path.
Let's define a separate _router_ for dealing with users in a new _controllers/users.js_ file. Let's take the router into use in our application in the _app.js_ file, so that it handles requests made to the _/api/users_ url:

```
// ...
const notesRouter = require('./controllers/notes')
const usersRouter = require('./controllers/users')
// ...

app.use('/api/notes', notesRouter)
app.use('/api/users', usersRouter)
// ...copy
```

The contents of the file, _controllers/users.js_ , that defines the router is as follows:

```
const bcrypt = require('bcrypt')
const usersRouter = require('express').Router()
const User = require('../models/user')

usersRouter.post('/', async (request, response) => {
  const { username, name, password } = request.body

  const saltRounds = 10
  const passwordHash = await bcrypt.hash(password, saltRounds)

  const user = new User({
    username,
    name,
    passwordHash,
  })

  const savedUser = await user.save()

  response.status(201).json(savedUser)
})

module.exports = usersRoutercopy
```

The password sent in the request is _not_ stored in the database. We store the _hash_ of the password that is generated with the _bcrypt.hash_ function.
The fundamentals of
Our current code does not contain any error handling or input validation for verifying that the username and password are in the desired format.
The new feature can and should initially be tested manually with a tool like Postman. However testing things manually will quickly become too cumbersome, especially once we implement functionality that enforces usernames to be unique.
It takes much less effort to write automated tests, and it will make the development of our application much easier.
Our initial tests could look like this:

```
const bcrypt = require('bcrypt')
const User = require('../models/user')

//...

describe('when there is initially one user in db', () => {
  beforeEach(async () => {
    await User.deleteMany({})

    const passwordHash = await bcrypt.hash('sekret', 10)
    const user = new User({ username: 'root', passwordHash })

    await user.save()
  })

  test('creation succeeds with a fresh username', async () => {
    const usersAtStart = await helper.usersInDb()

    const newUser = {
      username: 'mluukkai',
      name: 'Matti Luukkainen',
      password: 'salainen',
    }

    await api
      .post('/api/users')
      .send(newUser)
      .expect(201)
      .expect('Content-Type', /application\/json/)

    const usersAtEnd = await helper.usersInDb()
    assert.strictEqual(usersAtEnd.length, usersAtStart.length + 1)

    const usernames = usersAtEnd.map(u => u.username)
    assert(usernames.includes(newUser.username))
  })
})copy
```

The tests use the _usersInDb()_ helper function that we implemented in the _tests/test_helper.js_ file. The function is used to help us verify the state of the database after a user is created:

```
const User = require('../models/user')

// ...

const usersInDb = async () => {
  const users = await User.find({})
  return users.map(u => u.toJSON())
}

module.exports = {
  initialNotes,
  nonExistingId,
  notesInDb,
  usersInDb,
}copy
```

The _beforeEach_ block adds a user with the username _root_ to the database. We can write a new test that verifies that a new user with the same username can not be created:

```
describe('when there is initially one user in db', () => {
  // ...

  test('creation fails with proper statuscode and message if username already taken', async () => {
    const usersAtStart = await helper.usersInDb()

    const newUser = {
      username: 'root',
      name: 'Superuser',
      password: 'salainen',
    }

    const result = await api
      .post('/api/users')
      .send(newUser)
      .expect(400)
      .expect('Content-Type', /application\/json/)

    const usersAtEnd = await helper.usersInDb()
    assert(result.body.error.includes('expected `username` to be unique'))

    assert.strictEqual(usersAtEnd.length, usersAtStart.length)
  })
})copy
```

The test case obviously will not pass at this point. We are essentially practicing
Mongoose validations do not provide a direct way to check the uniqueness of a field value. However, it is possible to achieve uniqueness by defining

```
const mongoose = require('mongoose')

const userSchema = mongoose.Schema({
  username: {    type: String,    required: true,    unique: true // this ensures the uniqueness of username  },  name: String,
  passwordHash: String,
  notes: [
    {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Note'
    }
  ],
})

// ...copy
```

However, we want to be careful when using the uniqueness index. If there are already documents in the database that violate the uniqueness condition, _root_ to the database twice, and these must be removed for the index to be formed and the code to work.
Mongoose validations do not detect the index violation, and instead of _ValidationError_ they return an error of type _MongoServerError_. We therefore need to extend the error handler for that case:

```
const errorHandler = (error, request, response, next) => {
  if (error.name === 'CastError') {
    return response.status(400).send({ error: 'malformatted id' })
  } else if (error.name === 'ValidationError') {
    return response.status(400).json({ error: error.message })
  } else if (error.name === 'MongoServerError' && error.message.includes('E11000 duplicate key error')) {    return response.status(400).json({ error: 'expected `username` to be unique' })  }
  next(error)
}copy
```

After these changes, the tests will pass.
We could also implement other validations into the user creation. We could check that the username is long enough, that the username only consists of permitted characters, or that the password is strong enough. Implementing these functionalities is left as an optional exercise.
Before we move onward, let's add an initial implementation of a route handler that returns all of the users in the database:

```
usersRouter.get('/', async (request, response) => {
  const users = await User.find({})
  response.json(users)
})copy
```

For making new users in a production or development environment, you may send a POST request to `/api/users/` via Postman or REST Client in the following format:

```
{
    "username": "root",
    "name": "Superuser",
    "password": "salainen"
}copy
```

The list looks like this:
![browser api/users shows JSON data with notes array](../assets/4d5f3bdd3364b471.png)
You can find the code for our current application in its entirety in the _part4-7_ branch of
### Creating a new note
The code for creating a new note has to be updated so that the note is assigned to the user who created it.
Let's expand our current implementation in _controllers/notes.js_ so that the information about the user who created a note is sent in the _userId_ field of the request body:

```
const notesRouter = require('express').Router()
const Note = require('../models/note')
const User = require('../models/user')
//...

notesRouter.post('/', async (request, response) => {
  const body = request.body

  const user = await User.findById(body.userId)
  if (!user) {    return response.status(400).json({ error: 'userId missing or not valid' })  }
  const note = new Note({
    content: body.content,
    important: body.important || false,
    user: user._id  })

  const savedNote = await note.save()
  user.notes = user.notes.concat(savedNote._id)  await user.save()
  response.status(201).json(savedNote)
})

// ...copy
```

The database is first queried for a user using the _userId_ provided in the request. If the user is not found, the response is sent with a status code of 400 (_Bad Request_) and an error message: _"userId missing or not valid"_.
It's worth noting that the _user_ object also changes. The _id_ of the note is stored in the _notes_ field of the _user_ object:

```
const user = await User.findById(body.userId)

// ...

user.notes = user.notes.concat(savedNote._id)
await user.save()copy
```

Let's try to create a new note
![Postman creating a new note](../assets/f87ee38d4ade1176.png)
The operation appears to work. Let's add one more note and then visit the route for fetching all users:
![api/users returns JSON with users and their array of notes](../assets/d22bd72648432956.png)
We can see that the user has two notes.
Likewise, the ids of the users who created the notes can be seen when we visit the route for fetching all notes:
![api/notes shows ids of users in JSON](../assets/97530c0d3c14349c.png)
Due to the changes we made, the tests no longer pass, but we leave fixing the tests as an optional exercise. The changes we made have also not been accounted for in the frontend, so the note creation functionality no longer works. We will fix the frontend in part 5 of the course.
### Populate
We would like our API to work in such a way, that when an HTTP GET request is made to the _/api/users_ route, the user objects would also contain the contents of the user's notes and not just their id. In a relational database, this functionality would be implemented with a _join query_.
As previously mentioned, document databases do not properly support join queries between collections, but the Mongoose library can do some of these joins for us. Mongoose accomplishes the join by doing multiple queries, which is different from join queries in relational databases which are _transactional_ , meaning that the state of the database does not change during the time that the query is made. With join queries in Mongoose, nothing can guarantee that the state between the collections being joined is consistent, meaning that if we make a query that joins the user and notes collections, the state of the collections may change during the query.
The Mongoose join is done with the _controllers/users.js_ file:

```
usersRouter.get('/', async (request, response) => {
  const users = await User    .find({}).populate('notes')
  response.json(users)
})copy
```

The _find_ method making the initial query. The argument given to the populate method defines that the _ids_ referencing _note_ objects in the _notes_ field of the _user_ document will be replaced by the referenced _note_ documents. Mongoose first queries the _users_ collection for the list of users, and then queries the collection corresponding to the model object specified by the _ref_ property in the users schema for data with the given object id.
The result is almost exactly what we wanted:
![JSON data showing populated notes and users data with repetition](../assets/c95478746d2b64c2.png)
We can use the populate method for choosing the fields we want to include from the documents. In addition to the field _id_ we are now only interested in _content_ and _important_.
The selection of fields is done with the Mongo

```
usersRouter.get('/', async (request, response) => {
  const users = await User
    .find({}).populate('notes', { content: 1, important: 1 })

  response.json(users)
})copy
```

The result is now exactly like we want it to be:
![combined data showing no repetition](../assets/2c3acce28788e8d4.png)
Let's also add a suitable population of user information to notes in the _controllers/notes.js_ file:

```
notesRouter.get('/', async (request, response) => {
  const notes = await Note
    .find({}).populate('user', { username: 1, name: 1 })

  response.json(notes)
})copy
```

Now the user's information is added to the _user_ field of note objects.
![notes JSON now has user info embedded too](../assets/d5df0304ba851874.png)
It's important to understand that the database does not know that the ids stored in the _user_ field of the notes collection reference documents in the user collection.
The functionality of the _populate_ method of Mongoose is based on the fact that we have defined "types" to the references in the Mongoose schema with the _ref_ option:

```
const noteSchema = new mongoose.Schema({
  content: {
    type: String,
    required: true,
    minlength: 5
  },
  important: Boolean,
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  }
})copy
```

You can find the code for our current application in its entirety in the _part4-8_ branch of
[Part 4b **Previous part**](../part4/01-testing-the-backend.md)[Part 4d **Next part**](../part4/01-token-authentication.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)
