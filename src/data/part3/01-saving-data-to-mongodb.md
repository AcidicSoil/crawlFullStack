---{
  "title": "Saving data to MongoDB",
  "source_url": "https://fullstackopen.com/en/part3/saving_data_to_mongo_db",
  "crawl_timestamp": "2025-10-04T19:16:23Z",
  "checksum": "921fa742ae3e94346b525410bbf568f9b28301a3c9ca7aad4cf4a7a3d213031a"
}
---[Skip to content](../part3/01-saving-data-to-mongo-db-course-main-content.md)
[{() => fs}](https://fullstackopen.com/en/)
  * [About course](../about/01-about.md)
  * [Course contents](../#course-contents/01-course-contents.md)
  * [FAQ](../faq/01-faq.md)
  * [Partners](../companies/01-companies.md)
  * [Challenge](../challenge/01-challenge.md)
[Search from the material](../search/01-search.md)Toggle dark theme
Select languageSuomi English 中文 Español Français Português(BR) 

[Fullstack](../#course-contents/01-course-contents.md)
[Part 3](../part3/01-part3.md)
Saving data to MongoDB
[a Node.js and Express](../part3/01-node-js-and-express.md)[b Deploying app to internet](../part3/01-deploying-app-to-internet.md)
c Saving data to MongoDB
  * [Debugging Node applications](../part3/01-saving-data-to-mongo-db-debugging-node-applications.md)
  * [MongoDB](../part3/01-saving-data-to-mongo-db-mongo-db.md)
  * [Schema](../part3/01-saving-data-to-mongo-db-schema.md)
  * [Creating and saving objects](../part3/01-saving-data-to-mongo-db-creating-and-saving-objects.md)
  * [Fetching objects from the database](../part3/01-saving-data-to-mongo-db-fetching-objects-from-the-database.md)
  * [Exercise 3.12.](../part3/01-saving-data-to-mongo-db-exercise-3-12.md)
  * [Connecting the backend to a database](../part3/01-saving-data-to-mongo-db-connecting-the-backend-to-a-database.md)
  * [Moving db configuration to its own module](../part3/01-saving-data-to-mongo-db-moving-db-configuration-to-its-own-module.md)
  * [Defining environment variables using the dotenv library](../part3/01-saving-data-to-mongo-db-defining-environment-variables-using-the-dotenv-library.md)
  * [Using database in route handlers](../part3/01-saving-data-to-mongo-db-using-database-in-route-handlers.md)
  * [Verifying frontend and backend integration](../part3/01-saving-data-to-mongo-db-verifying-frontend-and-backend-integration.md)
  * [A true full stack developer's oath](../part3/01-saving-data-to-mongo-db-a-true-full-stack-developers-oath.md)
  * [Exercises 3.13.-3.14.](../part3/01-saving-data-to-mongo-db-exercises-3-13-3-14.md)
  * [Error handling](../part3/01-saving-data-to-mongo-db-error-handling.md)
  * [Moving error handling into middleware](../part3/01-saving-data-to-mongo-db-moving-error-handling-into-middleware.md)
  * [The order of middleware loading](../part3/01-saving-data-to-mongo-db-the-order-of-middleware-loading.md)
  * [Other operations](../part3/01-saving-data-to-mongo-db-other-operations.md)
  * [Exercises 3.15.-3.18.](../part3/01-saving-data-to-mongo-db-exercises-3-15-3-18.md)


[d Validation and ESLint](../part3/01-validation-and-es-lint.md)
c
# Saving data to MongoDB
Before we move into the main topic of persisting data in a database, we will take a look at a few different ways of debugging Node applications.
### Debugging Node applications
Debugging Node applications is slightly more difficult than debugging JavaScript running in your browser. Printing to the console is a tried and true method, and it's always worth doing. Some people think that more sophisticated methods should be used instead, but I disagree. Even the world's elite open-source developers 
#### Visual Studio Code
The Visual Studio Code debugger can be useful in some situations. You can launch the application in debugging mode like this (in this and the next few images, the notes have a field _date_ which has been removed from the current version of the application):
![screenshot showing how to launch debugger in vscode](../assets/f33788d9b611a24c.png)
Note that the application shouldn't be running in another console, otherwise the port will already be in use.
**NB** A newer version of Visual Studio Code may have _Run_ instead of _Debug_. Furthermore, you may have to configure your _launch.json_ file to start debugging. This can be done by choosing _Add Configuration..._ on the drop-down menu, which is located next to the green play button and above _VARIABLES_ menu, and select _Run "npm start" in a debug terminal_. For more detailed setup instructions, visit Visual Studio Code's 
Below you can see a screenshot where the code execution has been paused in the middle of saving a new note:
![vscode screenshot of execution at a breakpoint](../assets/1e763e2f277ebcad.png)
The execution stopped at the _breakpoint_ in line 69. In the console, you can see the value of the _note_ variable. In the top left window, you can see other things related to the state of the application.
The arrows at the top can be used for controlling the flow of the debugger.
For some reason, I don't use the Visual Studio Code debugger a whole lot.
#### Chrome dev tools
Debugging is also possible with the Chrome developer console by starting your application with the command:
```
node --inspect index.jscopy
```

You can access the debugger by clicking the green icon - the node logo - that appears in the Chrome developer console:
![dev tools with green node logo icon](../assets/53304d0434c34df8.png)
The debugging view works the same way as it did with React applications. The _Sources_ tab can be used for setting breakpoints where the execution of the code will be paused.
![dev tools sources tab breakpoint and watch variables](../assets/3f250f4226b400a9.png)
All of the application's _console.log_ messages will appear in the _Console_ tab of the debugger. You can also inspect values of variables and execute your own JavaScript code.
![dev tools console tab showing note object typed in](../assets/93e881c87920ac9f.png)
#### Question everything
Debugging Full Stack applications may seem tricky at first. Soon our application will also have a database in addition to the frontend and backend, and there will be many potential areas for bugs in the application.
When the application "does not work", we have to first figure out where the problem actually occurs. It's very common for the problem to exist in a place where you didn't expect it, and it can take minutes, hours, or even days before you find the source of the problem.
The key is to be systematic. Since the problem can exist anywhere, _you must question everything_ , and eliminate all possibilities one by one. Logging to the console, Postman, debuggers, and experience will help.
When bugs occur, _the worst of all possible strategies_ is to continue writing code. It will guarantee that your code will soon have even more bugs, and debugging them will be even more difficult. The 
### MongoDB
To store our saved notes indefinitely, we need a database. Most of the courses taught at the University of Helsinki use relational databases. In most parts of this course, we will use 
The reason for using Mongo as the database is its lower complexity compared to a relational database. [Part 13](../part13/01-part13.md) of the course shows how to build Node.js backends that use a relational database.
Document databases differ from relational databases in how they organize data as well as in the query languages they support. Document databases are usually categorized under the 
You can read more about document databases and NoSQL from the course material for 
Read now the chapters on 
Naturally, you can install and run MongoDB on your computer. However, the internet is also full of Mongo database services that you can use. Our preferred MongoDB provider in this course will be 
Once you've created and logged into your account, let's create a new cluster using the button visible on the front page. From the view that opens, select the free plan, determine the cloud provider and data center, and create the cluster:
![mongodb picking shared, aws and region](../assets/8ee558dbe0d0bd4f.png)
The provider selected is _AWS_ and the region is _Stockholm (eu-north-1)_. Note that if you choose something else, your database connection string will be slightly different from this example. Wait for the cluster to be ready, which will take a few minutes.
**NB** do not continue before the cluster is ready.
Let's use the _security_ tab for creating user credentials for the database. Please note that these are not the same credentials you use for logging into MongoDB Atlas. These will be used for your application to connect to the database.
![mongodb security quickstart](../assets/1db40a07542a2114.png)
Next, we have to define the IP addresses that are allowed access to the database. For the sake of simplicity we will allow access from all IP addresses:
![mongodb network access/add ip access list](../assets/dbd818c8f96897a9.png)
Note: In case the modal menu is different for you, according to MongoDB documentation, adding 0.0.0.0 as an IP allows access from anywhere as well.
Finally, we are ready to connect to our database. To do this, we need the database connection string, which can be found by selecting _Connect_ and then _Drivers_ from the view, under the _Connect to your application_ section:
![mongodb database deployment connect](../assets/3c4e82e1c9b866c4.png)
The view displays the _MongoDB URI_ , which is the address of the database that we will supply to the MongoDB client library we will add to our application:
![mongodb connect application](../assets/9120607a85d1abdb.png)
The address looks like this:
```
mongodb+srv://fullstack:thepasswordishere@cluster0.a5qfl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0copy
```

We are now ready to use the database.
We could use the database directly from our JavaScript code with the 
Mongoose could be described as an _object document mapper_ (ODM), and saving JavaScript objects as Mongo documents is straightforward with this library.
Let's install Mongoose in our notes project backend:
```
npm install mongoosecopy
```

Let's not add any code dealing with Mongo to our backend just yet. Instead, let's make a practice application by creating a new file, _mongo.js_ in the root of the notes backend application:
```
const mongoose = require('mongoose')

if (process.argv.length < 3) {
  console.log('give password as argument')
  process.exit(1)
}

const password = process.argv[2]

const url = `mongodb+srv://fullstack:${password}@cluster0.a5qfl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0`

mongoose.set('strictQuery',false)

mongoose.connect(url)

const noteSchema = new mongoose.Schema({
  content: String,
  important: Boolean,
})

const Note = mongoose.model('Note', noteSchema)

const note = new Note({
  content: 'HTML is easy',
  important: true,
})

note.save().then(result => {
  console.log('note saved!')
  mongoose.connection.close()
})copy
```

**NB:** Depending on which region you selected when building your cluster, the _MongoDB URI_ may be different from the example provided above. You should verify and use the correct URI that was generated from MongoDB Atlas.
The code also assumes that it will be passed the password from the credentials we created in MongoDB Atlas, as a command line parameter. We can access the command line parameter like this:
```
const password = process.argv[2]copy
```

When the code is run with the command _node mongo.js yourPassword_ , Mongo will add a new document to the database.
**NB:** Please note the password is the password created for the database user, not your MongoDB Atlas password. Also, if you created a password with special characters, then you'll need to 
We can view the current state of the database from the MongoDB Atlas from _Browse collections_ , in the Database tab.
![mongodb databases browse collections button](../assets/f3e6498a2945c827.png)
As the view states, the _document_ matching the note has been added to the _notes_ collection in the _myFirstDatabase_ database.
![mongodb collections tab db myfirst app notes](../assets/6601350678cceaec.png)
Let's destroy the default database _test_ and change the name of the database referenced in our connection string to _noteApp_ instead, by modifying the URI:
```
const url = `mongodb+srv://fullstack:${password}@cluster0.a5qfl.mongodb.net/noteApp?retryWrites=true&w=majority&appName=Cluster0`copy
```

Let's run our code again:
![mongodb collections tab noteApp notes](../assets/ab3076502a6838d6.png)
The data is now stored in the right database. The view also offers the _create database_ functionality, that can be used to create new databases from the website. Creating a database like this is not necessary, since MongoDB Atlas automatically creates a new database when an application tries to connect to a database that does not exist yet.
### Schema
After establishing the connection to the database, we define the 
```
const noteSchema = new mongoose.Schema({
  content: String,
  important: Boolean,
})

const Note = mongoose.model('Note', noteSchema)copy
```

First, we define the _noteSchema_ variable. The schema tells Mongoose how the note objects are to be stored in the database.
In the _Note_ model definition, the first _"Note"_ parameter is the singular name of the model. The name of the collection will be the lowercase plural _notes_ , because the _notes_) when the schema refers to them in the singular (e.g. _Note_).
Document databases like Mongo are _schemaless_ , meaning that the database itself does not care about the structure of the data that is stored in the database. It is possible to store documents with completely different fields in the same collection.
The idea behind Mongoose is that the data stored in the database is given a _schema at the level of the application_ that defines the shape of the documents stored in any given collection.
### Creating and saving objects
Next, the application creates a new note object with the help of the _Note_
```
const note = new Note({
  content: 'HTML is Easy',
  important: false,
})copy
```

Models are _constructor functions_ that create new JavaScript objects based on the provided parameters. Since the objects are created with the model's constructor function, they have all the properties of the model, which include methods for saving the object to the database.
Saving the object to the database happens with the appropriately named _save_ method, which can be provided with an event handler with the _then_ method:
```
note.save().then(result => {
  console.log('note saved!')
  mongoose.connection.close()
})copy
```

When the object is saved to the database, the event handler provided to _then_ gets called. The event handler closes the database connection with the command `mongoose.connection.close()`. If the connection is not closed, the connection remains open until the program terminates.
The result of the save operation is in the _result_ parameter of the event handler. The result is not that interesting when we're storing one object in the database. You can print the object to the console if you want to take a closer look at it while implementing your application or during debugging.
Let's also save a few more notes by modifying the data in the code and by executing the program again.
**NB:** Unfortunately the Mongoose documentation is not very consistent, with parts of it using callbacks in its examples and other parts, other styles, so it is not recommended to copy and paste code directly from there. Mixing promises with old-school callbacks in the same code is not recommended.
### Fetching objects from the database
Let's comment out the code for generating new notes and replace it with the following:
```
Note.find({}).then(result => {
  result.forEach(note => {
    console.log(note)
  })
  mongoose.connection.close()
})copy
```

When the code is executed, the program prints all the notes stored in the database:
![node mongo.js outputs notes as JSON](../assets/df5250d5062f3ad7.png)
The objects are retrieved from the database with the _Note_ model. The parameter of the method is an object expressing search conditions. Since the parameter is an empty object`{}`, we get all of the notes stored in the _notes_ collection.
The search conditions adhere to the Mongo search query 
We could restrict our search to only include important notes like this:
```
Note.find({ important: true }).then(result => {
  // ...
})copy
```

### Exercise 3.12.
#### 3.12: Command-line database
Create a cloud-based MongoDB database for the phonebook application with MongoDB Atlas.
Create a _mongo.js_ file in the project directory, that can be used for adding entries to the phonebook, and for listing all of the existing entries in the phonebook.
**NB:** Do not include the password in the file that you commit and push to GitHub!
The application should work as follows. You use the program by passing three command-line arguments (the first is the password), e.g.:
```
node mongo.js yourpassword Anna 040-1234556copy
```

As a result, the application will print:
```
added Anna number 040-1234556 to phonebookcopy
```

The new entry to the phonebook will be saved to the database. Notice that if the name contains whitespace characters, it must be enclosed in quotes:
```
node mongo.js yourpassword "Arto Vihavainen" 045-1232456copy
```

If the password is the only parameter given to the program, meaning that it is invoked like this:
```
node mongo.js yourpasswordcopy
```

Then the program should display all of the entries in the phonebook:
```
phonebook:
Anna 040-1234556
Arto Vihavainen 045-1232456
Ada Lovelace 040-1231236copy
```

You can get the command-line parameters from the 
**NB: do not close the connection in the wrong place**. E.g. the following code will not work:
```
Person
  .find({})
  .then(persons=> {
    // ...
  })

mongoose.connection.close()copy
```

In the code above the _mongoose.connection.close()_ command will get executed immediately after the _Person.find_ operation is started. This means that the database connection will be closed immediately, and the execution will never get to the point where _Person.find_ operation finishes and the _callback_ function gets called.
The correct place for closing the database connection is at the end of the callback function:
```
Person
  .find({})
  .then(persons=> {
    // ...
    mongoose.connection.close()
  })copy
```

**NB:** If you define a model with the name _Person_ , mongoose will automatically name the associated collection as _people_.
### Connecting the backend to a database
Now we have enough knowledge to start using Mongo in our notes application backend.
Let's get a quick start by copy-pasting the Mongoose definitions to the _index.js_ file:
```
const mongoose = require('mongoose')

// DO NOT SAVE YOUR PASSWORD TO GITHUB!!
const password = process.argv[2]
const url = `mongodb+srv://fullstack:${password}@cluster0.a5qfl.mongodb.net/noteApp?retryWrites=true&w=majority&appName=Cluster0`

mongoose.set('strictQuery',false)
mongoose.connect(url)

const noteSchema = new mongoose.Schema({
  content: String,
  important: Boolean,
})

const Note = mongoose.model('Note', noteSchema)copy
```

Let's change the handler for fetching all notes to the following form:
```
app.get('/api/notes', (request, response) => {
  Note.find({}).then(notes => {
    response.json(notes)
  })
})copy
```

Let's start the backend with the command `node --watch index.js yourpassword` so we can verify in the browser that the backend correctly displays all notes saved to the database:
![api/notes in browser shows notes in JSON](../assets/665e83823724a28f.png)
The application works almost perfectly. The frontend assumes that every object has a unique id in the _id_ field. We also don't want to return the mongo versioning field ___v_ to the frontend.
One way to format the objects returned by Mongoose is to _toJSON_ method of the schema, which is used on all instances of the models produced with that schema. Modification can be done as follows:
```
noteSchema.set('toJSON', {
  transform: (document, returnedObject) => {
    returnedObject.id = returnedObject._id.toString()
    delete returnedObject._id
    delete returnedObject.__v
  }
})copy
```

Even though the __id_ property of Mongoose objects looks like a string, it is in fact an object. The _toJSON_ method we defined transforms it into a string just to be safe. If we didn't make this change, it would cause more harm to us in the future once we start writing tests.
No changes are needed in the handler:
```
app.get('/api/notes', (request, response) => {
  Note.find({}).then(notes => {
    response.json(notes)
  })
})copy
```

The code automatically uses the defined _toJSON_ when formatting notes to the response.
### Moving db configuration to its own module
Before we refactor the rest of the backend to use the database, let's extract the Mongoose-specific code into its own module.
Let's create a new directory for the module called _models_ , and add a file called _note.js_ :
```
const mongoose = require('mongoose')

mongoose.set('strictQuery', false)

const url = process.env.MONGODB_URI
console.log('connecting to', url)
mongoose.connect(url)
  .then(result => {    console.log('connected to MongoDB')  })  .catch(error => {    console.log('error connecting to MongoDB:', error.message)  })
const noteSchema = new mongoose.Schema({
  content: String,
  important: Boolean,
})

noteSchema.set('toJSON', {
  transform: (document, returnedObject) => {
    returnedObject.id = returnedObject._id.toString()
    delete returnedObject._id
    delete returnedObject.__v
  }
})

module.exports = mongoose.model('Note', noteSchema)copy
```

There are some changes in the code compared to before. The database connection URL is now passed to the application via the MONGODB_URI environment variable, as hardcoding it into the application is not a good idea:
```
const url = process.env.MONGODB_URIcopy
```

There are many ways to define the value of an environment variable. For example, we can define it when starting the application as follows:
```
MONGODB_URI="your_connection_string_here" npm run devcopy
```

We will soon learn a more sophisticated way to define environment variables.
The way that the connection is made has changed slightly:
```
mongoose.connect(url)
  .then(result => {
    console.log('connected to MongoDB')
  })
  .catch(error => {
    console.log('error connecting to MongoDB:', error.message)
  })copy
```

The method for establishing the connection is now given functions for dealing with a successful and unsuccessful connection attempt. Both functions just log a message to the console about the success status:
![node output when wrong username/password](../assets/bbff70b2cf80fad4.png)
Defining Node [ES6 modules](../part2/01-rendering-a-collection-modules-refactoring-modules.md) in part 2.
The public interface of the module is defined by setting a value to the _module.exports_ variable. We will set the value to be the _Note_ model. The other things defined inside of the module, like the variables _mongoose_ and _url_ will not be accessible or visible to users of the module.
Importing the module happens by adding the following line to _index.js_ :
```
const Note = require('./models/note')copy
```

This way the _Note_ variable will be assigned to the same object that the module defines.
### Defining environment variables using the dotenv library
A more sophisticated way to define environment variables is to use the 
```
npm install dotenvcopy
```

To use the library, we create a _.env_ file at the root of the project. The environment variables are defined inside of the file, and it can look like this:
```
MONGODB_URI=mongodb+srv://fullstack:thepasswordishere@cluster0.a5qfl.mongodb.net/noteApp?retryWrites=true&w=majority&appName=Cluster0
PORT=3001copy
```

We also added the hardcoded port of the server into the _PORT_ environment variable.
**The _.env_ file should be gitignored right away since we do not want to publish any confidential information publicly online!**
![.gitignore in vscode with .env line added](../assets/76389fc7c9b7396d.png)
The environment variables defined in the _.env_ file can be taken into use with the expression _require('dotenv').config()_ and you can reference them in your code just like you would reference normal environment variables, with the _process.env.MONGODB_URI_ syntax.
Let's load the environment variables at the beginning of the index.js file so that they are available throughout the entire application. Let's change the _index.js_ file in the following way:
```
require('dotenv').config()const express = require('express')
const Note = require('./models/note')
const app = express()
// ..

const PORT = process.env.PORTapp.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`)
})copy
```

It's important that _dotenv_ gets imported before the _note_ model is imported. This ensures that the environment variables from the _.env_ file are available globally before the code from the other modules is imported.
#### Important note about defining environment variables in Fly.io and Render
**Fly.io users:** Because GitHub is not used with Fly.io, the file .env also gets to the Fly.io servers when the app is deployed. Because of this, the env variables defined in the file will be available there.
However, a _.dockerignore_ , with the following contents
```
.envcopy
```

and set the env value from the command line with the command:
```
fly secrets set MONGODB_URI="mongodb+srv://fullstack:thepasswordishere@cluster0.a5qfl.mongodb.net/noteApp?retryWrites=true&w=majority&appName=Cluster0"copy
```

**Render users:** When using Render, the database url is given by defining the proper env in the dashboard:
![browser showing render environment variables](../assets/4b32d67f18cdd6aa.png)
Set just the URL starting with _mongodb+srv://..._ to the _value_ field.
### Using database in route handlers
Next, let's change the rest of the backend functionality to use the database.
Creating a new note is accomplished like this:
```
app.post('/api/notes', (request, response) => {
  const body = request.body

  if (!body.content) {
    return response.status(400).json({ error: 'content missing' })
  }

  const note = new Note({
    content: body.content,
    important: body.important || false,
  })

  note.save().then(savedNote => {
    response.json(savedNote)
  })
})copy
```

The note objects are created with the _Note_ constructor function. The response is sent inside of the callback function for the _save_ operation. This ensures that the response is sent only if the operation succeeded. We will discuss error handling a little bit later.
The _savedNote_ parameter in the callback function is the saved and newly created note. The data sent back in the response is the formatted version created automatically with the _toJSON_ method:
```
response.json(savedNote)copy
```

Using Mongoose's 
```
app.get('/api/notes/:id', (request, response) => {
  Note.findById(request.params.id).then(note => {
    response.json(note)
  })
})copy
```

### Verifying frontend and backend integration
When the backend gets expanded, it's a good idea to test the backend first with **the browser, Postman or the VS Code REST client**. Next, let's try creating a new note after taking the database into use:
![VS code rest client doing a post](../assets/f5ce38c74e970a59.png)
Only once everything has been verified to work in the backend, is it a good idea to test that the frontend works with the backend. It is highly inefficient to test things exclusively through the frontend.
It's probably a good idea to integrate the frontend and backend one functionality at a time. First, we could implement fetching all of the notes from the database and test it through the backend endpoint in the browser. After this, we could verify that the frontend works with the new backend. Once everything seems to be working, we would move on to the next feature.
Once we introduce a database into the mix, it is useful to inspect the state persisted in the database, e.g. from the control panel in MongoDB Atlas. Quite often little Node helper programs like the _mongo.js_ program we wrote earlier can be very helpful during development.
You can find the code for our current application in its entirety in the _part3-4_ branch of 
### A true full stack developer's oath
It is again time for the exercises. The complexity of our app has now taken another step since besides frontend and backend we also have a database. There are indeed really many potential sources of error.
So we should once more extend our oath:
Full stack development is _extremely hard_ , that is why I will use all the possible means to make it easier
  * I will have my browser developer console open all the time
  * I will use the network tab of the browser dev tools to ensure that frontend and backend are communicating as I expect
  * I will constantly keep an eye on the state of the server to make sure that the data sent there by the frontend is saved there as I expect
  * _I will keep an eye on the database: does the backend save data there in the right format_
  * I progress with small steps
  * I will write lots of _console.log_ statements to make sure I understand how the code behaves and to help pinpoint problems
  * If my code does not work, I will not write more code. Instead, I start deleting the code until it works or just return to a state when everything was still working
  * When I ask for help in the course Discord channel or elsewhere I formulate my questions properly, see [here](../part0/01-general-info-how-to-get-help-in-discord.md) how to ask for help


### Exercises 3.13.-3.14.
The following exercises are pretty straightforward, but if your frontend stops working with the backend, then finding and fixing the bugs can be quite interesting.
#### 3.13: Phonebook database, step 1
Change the fetching of all phonebook entries so that the data is _fetched from the database_.
Verify that the frontend works after the changes have been made.
In the following exercises, write all Mongoose-specific code into its own module, just like we did in the chapter [Database configuration into its own module](../part3/01-saving-data-to-mongo-db-moving-db-configuration-to-its-own-module.md).
#### 3.14: Phonebook database, step 2
Change the backend so that new numbers are _saved to the database_. Verify that your frontend still works after the changes.
At this stage, you can ignore whether there is already a person in the database with the same name as the person you are adding.
### Error handling
If we try to visit the URL of a note with an id that does not exist e.g. _5c41c90e84d891c15dfa3431_ is not an id stored in the database, then the response will be _null_.
Let's change this behavior so that if a note with the given id doesn't exist, the server will respond to the request with the HTTP status code 404 not found. In addition let's implement a simple _catch_ block to handle cases where the promise returned by the _findById_ method is _rejected_ :
```
app.get('/api/notes/:id', (request, response) => {
  Note.findById(request.params.id)
    .then(note => {
      if (note) {        response.json(note)      } else {        response.status(404).end()      }    })
    .catch(error => {      console.log(error)      response.status(500).end()    })})copy
```

If no matching object is found in the database, the value of _note_ will be _null_ and the _else_ block is executed. This results in a response with the status code _404 not found_. If a promise returned by the _findById_ method is rejected, the response will have the status code _500 internal server error_. The console displays more detailed information about the error.
On top of the non-existing note, there's one more error situation that needs to be handled. In this situation, we are trying to fetch a note with the wrong kind of _id_ , meaning an _id_ that doesn't match the Mongo identifier format.
If we make the following request, we will get the error message shown below:
```
Method: GET
Path:   /api/notes/someInvalidId
Body:   {}
---
{ CastError: Cast to ObjectId failed for value "someInvalidId" at path "_id"
    at CastError (/Users/mluukkai/opetus/_fullstack/osa3-muisiinpanot/node_modules/mongoose/lib/error/cast.js:27:11)
    at ObjectId.cast (/Users/mluukkai/opetus/_fullstack/osa3-muisiinpanot/node_modules/mongoose/lib/schema/objectid.js:158:13)
    ...copy
```

Given a malformed id as an argument, the _findById_ method will throw an error causing the returned promise to be rejected. This will cause the callback function defined in the _catch_ block to be called.
Let's make some small adjustments to the response in the _catch_ block:
```
app.get('/api/notes/:id', (request, response) => {
  Note.findById(request.params.id)
    .then(note => {
      if (note) {
        response.json(note)
      } else {
        response.status(404).end() 
      }
    })
    .catch(error => {
      console.log(error)
      response.status(400).send({ error: 'malformatted id' })    })
})copy
```

If the format of the id is incorrect, then we will end up in the error handler defined in the _catch_ block. The appropriate status code for the situation is 
> _The 400 (Bad Request) status code indicates that the server cannot or will not process the request due to something that is perceived to be a client error (e.g., malformed request syntax, invalid request message framing, or deceptive request routing)._
We have also added some data to the response to shed some light on the cause of the error.
When dealing with Promises, it's almost always a good idea to add error and exception handling. Otherwise, you will find yourself dealing with strange bugs.
It's never a bad idea to print the object that caused the exception to the console in the error handler:
```
.catch(error => {
  console.log(error)  response.status(400).send({ error: 'malformatted id' })
})copy
```

The reason the error handler gets called might be something completely different than what you had anticipated. If you log the error to the console, you may save yourself from long and frustrating debugging sessions. Moreover, most modern services where you deploy your application support some form of logging system that you can use to check these logs. As mentioned, Fly.io is one.
Every time you're working on a project with a backend, _it is critical to keep an eye on the console output of the backend_. If you are working on a small screen, it is enough to just see a tiny slice of the output in the background. Any error messages will catch your attention even when the console is far back in the background:
![sample screenshot showing tiny slice of output](../assets/1527b9acfb69fe11.png)
### Moving error handling into middleware
We have written the code for the error handler among the rest of our code. This can be a reasonable solution at times, but there are cases where it is better to implement all error handling in a single place. This can be particularly useful if we want to report data related to errors to an external error-tracking system like 
Let's change the handler for the _/api/notes/:id_ route so that it passes the error forward with the _next_ function. The next function is passed to the handler as the third parameter:
```
app.get('/api/notes/:id', (request, response, next) => {  Note.findById(request.params.id)
    .then(note => {
      if (note) {
        response.json(note)
      } else {
        response.status(404).end()
      }
    })
    .catch(error => next(error))})copy
```

The error that is passed forward is given to the _next_ function as a parameter. If _next_ was called without an argument, then the execution would simply move onto the next route or middleware. If the _next_ function is called with an argument, then the execution will continue to the _error handler middleware_.
Express _four parameters_. Our error handler looks like this:
```
const errorHandler = (error, request, response, next) => {
  console.error(error.message)

  if (error.name === 'CastError') {
    return response.status(400).send({ error: 'malformatted id' })
  } 

  next(error)
}

// this has to be the last loaded middleware, also all the routes should be registered before this!
app.use(errorHandler)copy
```

The error handler checks if the error is a _CastError_ exception, in which case we know that the error was caused by an invalid object id for Mongo. In this situation, the error handler will send a response to the browser with the response object passed as a parameter. In all other error situations, the middleware passes the error forward to the default Express error handler.
Note that the error-handling middleware has to be the last loaded middleware, also all the routes should be registered before the error-handler!
### The order of middleware loading
The execution order of middleware is the same as the order that they are loaded into Express with the _app.use_ function. For this reason, it is important to be careful when defining middleware.
The correct order is the following:
```
app.use(express.static('dist'))
app.use(express.json())
app.use(requestLogger)

app.post('/api/notes', (request, response) => {
  const body = request.body
  // ...
})

const unknownEndpoint = (request, response) => {
  response.status(404).send({ error: 'unknown endpoint' })
}

// handler of requests with unknown endpoint
app.use(unknownEndpoint)

const errorHandler = (error, request, response, next) => {
  // ...
}

// handler of requests with result to errors
app.use(errorHandler)copy
```

The json-parser middleware should be among the very first middleware loaded into Express. If the order was the following:
```
app.use(requestLogger) // request.body is undefined!

app.post('/api/notes', (request, response) => {
  // request.body is undefined!
  const body = request.body
  // ...
})

app.use(express.json())copy
```

Then the JSON data sent with the HTTP requests would not be available for the logger middleware or the POST route handler, since the _request.body_ would be _undefined_ at that point.
It's also important that the middleware for handling unsupported routes is loaded only after all the endpoints have been defined, just before the error handler. For example, the following loading order would cause an issue:
```
const unknownEndpoint = (request, response) => {
  response.status(404).send({ error: 'unknown endpoint' })
}

// handler of requests with unknown endpoint
app.use(unknownEndpoint)

app.get('/api/notes', (request, response) => {
  // ...
})copy
```

Now the handling of unknown endpoints is ordered _before the HTTP request handler_. Since the unknown endpoint handler responds to all requests with _404 unknown endpoint_ , no routes or middleware will be called after the response has been sent by unknown endpoint middleware. The only exception to this is the error handler which needs to come at the very end, after the unknown endpoints handler.
### Other operations
Let's add some missing functionality to our application, including deleting and updating an individual note.
The easiest way to delete a note from the database is with the 
```
app.delete('/api/notes/:id', (request, response, next) => {
  Note.findByIdAndDelete(request.params.id)
    .then(result => {
      response.status(204).end()
    })
    .catch(error => next(error))
})copy
```

In both of the "successful" cases of deleting a resource, the backend responds with the status code _204 no content_. The two different cases are deleting a note that exists, and deleting a note that does not exist in the database. The _result_ callback parameter could be used for checking if a resource was actually deleted, and we could use that information for returning different status codes for the two cases if we deem it necessary. Any exception that occurs is passed onto the error handler.
Let's implement the functionality to update a single note, allowing the importance of the note to be changed. The note updating is done as follows:
```
app.put('/api/notes/:id', (request, response, next) => {
  const { content, important } = request.body

  Note.findById(request.params.id)
    .then(note => {
      if (!note) {
        return response.status(404).end()
      }

      note.content = content
      note.important = important

      return note.save().then((updatedNote) => {
        response.json(updatedNote)
      })
    })
    .catch(error => next(error))
})copy
```

The note to be updated is first fetched from the database using the _findById_ method. If no object is found in the database with the given id, the value of the variable _note_ is _null_ , and the query responds with the status code _404 Not Found_.
If an object with the given id is found, its _content_ and _important_ fields are updated with the data provided in the request, and the modified note is saved to the database using the _save()_ method. The HTTP request responds by sending the updated note in the response.
One notable point is that the code now has nested promises, meaning that within the outer _.then_ method, another 
```
    .then(note => {
      if (!note) {
        return response.status(404).end()
      }

      note.content = content
      note.important = important

      return note.save().then((updatedNote) => {        response.json(updatedNote)      })copy
```

Usually, this is not recommended because it can make the code difficult to read. In this case, however, the solution works because it ensures that the _.then_ block following the _save()_ method is only executed if a note with the given id is found in the database and the _save()_ method is called. In the fourth part of the course, we will explore the async/await syntax, which offers an easier and clearer way to handle such situations.
After testing the backend directly with Postman or the VS Code REST client, we can verify that it seems to work. The frontend also appears to work with the backend using the database.
You can find the code for our current application in its entirety in the _part3-5_ branch of 
### Exercises 3.15.-3.18.
#### 3.15: Phonebook database, step 3
Change the backend so that deleting phonebook entries is reflected in the database.
Verify that the frontend still works after making the changes.
#### 3.16: Phonebook database, step 4
Move the error handling of the application to a new error handler middleware.
#### 3.17*: Phonebook database, step 5
If the user tries to create a new phonebook entry for a person whose name is already in the phonebook, the frontend will try to update the phone number of the existing entry by making an HTTP PUT request to the entry's unique URL.
Modify the backend to support this request.
Verify that the frontend works after making your changes.
#### 3.18*: Phonebook database step 6
Also update the handling of the _api/persons/:id_ and _info_ routes to use the database, and verify that they work directly with the browser, Postman, or VS Code REST client.
Inspecting an individual phonebook entry from the browser should look like this:
![screenshot of browser showing one person with api/persons/their_id](../assets/da2229eb81ea82f6.png)
[ Part 3b **Previous part** ](../part3/01-deploying-app-to-internet.md)[ Part 3d **Next part** ](../part3/01-validation-and-es-lint.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)