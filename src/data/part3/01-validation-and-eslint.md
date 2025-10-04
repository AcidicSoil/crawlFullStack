---{
  "title": "Validation and ESLint",
  "source_url": "https://fullstackopen.com/en/part3/validation_and_es_lint",
  "crawl_timestamp": "2025-10-04T19:16:25Z",
  "checksum": "e5facfa4d245205a2d55f11aa683dfdbdd5fdbac2b330ff1b69bad624448ab61"
}
---[Skip to content](../part3/01-validation-and-es-lint-course-main-content.md)
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
Validation and ESLint
[a Node.js and Express](../part3/01-node-js-and-express.md)[b Deploying app to internet](../part3/01-deploying-app-to-internet.md)[c Saving data to MongoDB](../part3/01-saving-data-to-mongo-db.md)
d Validation and ESLint
  * [Deploying the database backend to production](../part3/01-validation-and-es-lint-deploying-the-database-backend-to-production.md)
  * [Exercises 3.19.-3.21.](../part3/01-validation-and-es-lint-exercises-3-19-3-21.md)
  * [Lint](../part3/01-validation-and-es-lint-lint.md)
  * [Formatting the Configuration File](../part3/01-validation-and-es-lint-formatting-the-configuration-file.md)
  * [Running the Linter](../part3/01-validation-and-es-lint-running-the-linter.md)
  * [Adding More Style Rules](../part3/01-validation-and-es-lint-adding-more-style-rules.md)
  * [Exercise 3.22.](../part3/01-validation-and-es-lint-exercise-3-22.md)


d
# Validation and ESLint
There are usually constraints that we want to apply to the data that is stored in our application's database. Our application shouldn't accept notes that have a missing or empty _content_ property. The validity of the note is checked in the route handler:
```
app.post('/api/notes', (request, response) => {
  const body = request.body
  if (!body.content) {    return response.status(400).json({ error: 'content missing' })  }
  // ...
})copy
```

If the note does not have the _content_ property, we respond to the request with the status code _400 bad request_.
One smarter way of validating the format of the data before it is stored in the database is to use the 
We can define specific validation rules for each field in the schema:
```
const noteSchema = new mongoose.Schema({
  content: {    type: String,    minLength: 5,    required: true  },  important: Boolean
})copy
```

The _content_ field is now required to be at least five characters long and it is set as required, meaning that it can not be missing. We have not added any constraints to the _important_ field, so its definition in the schema has not changed.
The _minLength_ and _required_ validators are 
If we try to store an object in the database that breaks one of the constraints, the operation will throw an exception. Let's change our handler for creating a new note so that it passes any potential exceptions to the error handler middleware:
```
app.post('/api/notes', (request, response, next) => {  const body = request.body

  const note = new Note({
    content: body.content,
    important: body.important || false,
  })

  note.save()
    .then(savedNote => {
      response.json(savedNote)
    })
    .catch(error => next(error))})copy
```

Let's expand the error handler to deal with these validation errors:
```
const errorHandler = (error, request, response, next) => {
  console.error(error.message)

  if (error.name === 'CastError') {
    return response.status(400).send({ error: 'malformatted id' })
  } else if (error.name === 'ValidationError') {    return response.status(400).json({ error: error.message })  }

  next(error)
}copy
```

When validating an object fails, we return the following default error message from Mongoose:
![postman showing error message](../assets/3772158fb4b16eae.png)
### Deploying the database backend to production
The application should work almost as-is in Fly.io/Render. We do not have to generate a new production build of the frontend since changes thus far were only on our backend.
The environment variables defined in dotenv will only be used when the backend is not in _production mode_ , i.e. Fly.io or Render.
For production, we have to set the database URL in the service that is hosting our app.
In Fly.io that is done _fly secrets set_ :
```
fly secrets set MONGODB_URI='mongodb+srv://fullstack:thepasswordishere@cluster0.a5qfl.mongodb.net/noteApp?retryWrites=true&w=majority'copy
```

When the app is being developed, it is more than likely that something fails. Eg. when I deployed my app for the first time with the database, not a single note was seen:
![browser showing no notes appearing](../assets/ba09595ad033be2f.png)
The network tab of the browser console revealed that fetching the notes did not succeed, the request just remained for a long time in the _pending_ state until it failed with status code 502.
The browser console has to be open _all the time!_
It is also vital to follow continuously the server logs. The problem became obvious when the logs were opened with _fly logs_ :
![fly.io server log showing connecting to undefined](../assets/d8bda79b000a5820.png)
The database url was _undefined_ , so the command _fly secrets set MONGODB_URI_ was forgotten.
You will also need to whitelist the fly.io app's IP address in MongoDB Atlas. If you don't MongoDB will refuse the connection.
Sadly, fly.io does not provide you a dedicated IPv4 address for your app, so you will need to allow all IP addresses in MongoDB Atlas.
When using Render, the database url is given by defining the proper env in the dashboard:
![render dashboard showing the MONGODB_URI env variable](../assets/4b32d67f18cdd6aa.png)
The Render Dashboard shows the server logs:
![render dashboard with arrow pointing to server running on port 10000](../assets/c4864302c1e42c1c.png)
You can find the code for our current application in its entirety in the _part3-6_ branch of 
### Exercises 3.19.-3.21.
#### 3.19*: Phonebook database, step 7
Expand the validation so that the name stored in the database has to be at least three characters long.
Expand the frontend so that it displays some form of error message when a validation error occurs. Error handling can be implemented by adding a _catch_ block as shown below:
```
personService
    .create({ ... })
    .then(createdPerson => {
      // ...
    })
    .catch(error => {
      // this is the way to access the error message
      console.log(error.response.data.error)
    })copy
```

You can display the default error message returned by Mongoose, even though they are not as readable as they could be:
![phonebook screenshot showing person validation failure](../assets/f4dd41ddd0886bec.png)
**NB:** On update operations, mongoose validators are off by default. 
#### 3.20*: Phonebook database, step 8
Add validation to your phonebook application, which will make sure that phone numbers are of the correct form. A phone number must:
  * have length of 8 or more
  * be formed of two parts that are separated by -, the first part has two or three numbers and the second part also consists of numbers
    * eg. 09-1234556 and 040-22334455 are valid phone numbers
    * eg. 1234556, 1-22334455 and 10-22-334455 are invalid


Use a 
If an HTTP POST request tries to add a person with an invalid phone number, the server should respond with an appropriate status code and error message.
#### 3.21 Deploying the database backend to production
Generate a new "full stack" version of the application by creating a new production build of the frontend, and copying it to the backend directory. Verify that everything works locally by using the entire application from the address 
Push the latest version to Fly.io/Render and verify that everything works there as well.
**NOTE:** You shall NOT be deploying the frontend directly at any stage of this part. Only the backend repository is deployed throughout the whole part. The frontend production build is added to the backend repository, and the backend serves it as described in the section [Serving static files from the backend](../part3/01-deploying-app-to-internet-serving-static-files-from-the-backend.md).
### Lint
Before we move on to the next part, we will take a look at an important tool called 
> _Generically, lint or a linter is any tool that detects and flags errors in programming languages, including stylistic errors. The term lint-like behavior is sometimes applied to the process of flagging suspicious language usage. Lint-like tools generally perform static analysis of source code._
In compiled statically typed languages like Java, IDEs like NetBeans can point out errors in the code, even ones that are more than just compile errors. Additional tools for performing 
In the JavaScript universe, the current leading tool for static analysis (aka "linting") is 
Let's add ESLint as a _development dependency_ for the backend. Development dependencies are tools that are only needed during the development of the application. For example, tools related to testing are such dependencies. When the application is run in production mode, development dependencies are not needed.
Install ESLint as a development dependency for the backend with the command:
```
npm install eslint @eslint/js --save-devcopy
```

The contents of the package.json file will change as follows:
```
{
  //...
  "dependencies": {
    "dotenv": "^16.4.7",
    "express": "^5.1.0",
    "mongoose": "^8.11.0"
  },
  "devDependencies": {    "@eslint/js": "^9.22.0",    "eslint": "^9.22.0"  }
}copy
```

The command added a _devDependencies_ section to the file and included the packages _eslint_ and _@eslint/js_ , and installed the required libraries into the _node_modules_ directory.
After this we can initialize a default ESlint configuration with the command:
```
npx eslint --initcopy
```

We will answer all of the questions:
![terminal output from ESlint init](../assets/be983fc889c5422b.png)
The configuration will be saved in the generated _eslint.config.mjs_ file.
### Formatting the Configuration File
Let's reformat the configuration file _eslint.config.mjs_ from its current form to the following:
```
import globals from 'globals'

export default [
  {
    files: ['**/*.js'],
    languageOptions: {
      sourceType: 'commonjs',
      globals: { ...globals.node },
      ecmaVersion: 'latest',
    },
  },
]copy
```

So far, our ESLint configuration file defines the _files_ option with _["*_/_.js"]_, which tells ESLint to look at all JavaScript files in our project folder. The _languageOptions_ property specifies options related to language features that ESLint should expect, in which we defined the _sourceType_ option as "commonjs". This indicates that the JavaScript code in our project uses the CommonJS module system, allowing ESLint to parse the code accordingly. 
The _globals_ property specifies global variables that are predefined. The spread operator applied here tells ESLint to include all global variables defined in the _globals.node_ settings such as the _process_. In the case of browser code we would define here _globals.browser_ to allow browser specific global variables like _window_ , and _document_.
Finally, the _ecmaVersion_ property is set to "latest". This sets the ECMAScript version to the latest available version, meaning ESLint will understand and properly lint the latest JavaScript syntax and features.
We want to make use of _@eslint/js_ package we installed earlier provides us with predefined configurations for ESLint. We'll import it and enable it in the configuration file:
```
import globals from 'globals'
import js from '@eslint/js'// ...

export default [
  js.configs.recommended,  {
    // ...
  },
]copy
```

We've added the _js.configs.recommended_ to the top of the configuration array, this ensures that ESLint's recommended settings are applied first before our own custom options.
Let's continue building the configuration file. Install a 
```
npm install --save-dev @stylistic/eslint-plugin-jscopy
```

Import and enable the plugin, and add these four code style rules:
```
import globals from 'globals'
import js from '@eslint/js'
import stylisticJs from '@stylistic/eslint-plugin-js'
export default [
  {
    // ...
    plugins: {       '@stylistic/js': stylisticJs,    },    rules: {       '@stylistic/js/indent': ['error', 2],      '@stylistic/js/linebreak-style': ['error', 'unix'],      '@stylistic/js/quotes': ['error', 'single'],      '@stylistic/js/semi': ['error', 'never'],    },   },
]copy
```

The _@stylistic/eslint-plugin-js_ , which adds JavaScript stylistic rules for ESLint. In addition, rules for indentation, line breaks, quotes, and semicolons have been added. These four rules are all defined in the 
**Note for Windows users:** The linebreak style is set to _unix_ in the style rules. It is recommended to use Unix-style linebreaks (_\n_) regardless of your operating system, as they are compatible with most modern operating systems and facilitate collaboration when multiple people are working on the same files. If you are using Windows-style linebreaks, ESLint will produce the following errors: _Expected linebreaks to be 'LF' but found 'CRLF'_. In this case, configure Visual Studio Code to use Unix-style linebreaks by following 
### Running the Linter
Inspecting and validating a file like _index.js_ can be done with the following command:
```
npx eslint index.jscopy
```

It is recommended to create a separate _npm script_ for linting:
```
{
  // ...
  "scripts": {
    "start": "node index.js",
    "dev": "node --watch index.js",
    "test": "echo \"Error: no test specified\" && exit 1",
    "lint": "eslint ."    // ...
  },
  // ...
}copy
```

Now the _npm run lint_ command will check every file in the project.
Files in the _dist_ directory also get checked when the command is run. We do not want this to happen, and we can accomplish this by adding an object with the 
```
// ...
export default [
  js.configs.recommended,
  {
    files: ['**/*.js'],
    // ...
  },
  {     ignores: ['dist/**'],   },]copy
```

This causes the entire _dist_ directory to not be checked by ESlint.
Lint has quite a lot to say about our code:
![terminal output of ESlint errors](../assets/6c3b8a76029d3448.png)
A better alternative to executing the linter from the command line is to configure an _eslint-plugin_ to the editor, that runs the linter continuously. By using the plugin you will see errors in your code immediately. You can find more information about the Visual Studio ESLint plugin 
The VS Code ESlint plugin will underline style violations with a red line:
![Screenshot of vscode ESlint plugin showing errors](../assets/562a8db1a17e6612.png)
This makes errors easy to spot and fix right away.
### Adding More Style Rules
ESlint has a vast array of _eslint.config.mjs_ file.
Let's add the 
```
export default [
  // ...
  rules: {
    // ...
   eqeqeq: 'error',  },
  // ...
]copy
```

While we're at it, let's make a few other changes to the rules.
Let's prevent unnecessary 
```
export default [
  // ...
  rules: {
    // ...
    eqeqeq: 'error',
    'no-trailing-spaces': 'error',    'object-curly-spacing': ['error', 'always'],    'arrow-spacing': ['error', { before: true, after: true }],  },
]copy
```

Our default configuration takes a bunch of predefined rules into use from:
```
// ...

export default [
  js.configs.recommended,
  // ...
]copy
```

This includes a rule that warns about _console.log_ commands which we don't want to use. Disabling a rule can be accomplished by defining its "value" as 0 or _off_ in the configuration file. Let's do this for the _no-console_ rule in the meantime.
```
[
  {
    // ...
    rules: {
      // ...
      eqeqeq: 'error',
      'no-trailing-spaces': 'error',
      'object-curly-spacing': ['error', 'always'],
      'arrow-spacing': ['error', { before: true, after: true }],
      'no-console': 'off',    },
  },
]copy
```

Disabling the no-console rule will allow us to use console.log statements without ESLint flagging them as issues. This can be particularly useful during development when you need to debug your code. Here's the complete configuration file with all the changes we have made so far:
```
import globals from 'globals'
import js from '@eslint/js'
import stylisticJs from '@stylistic/eslint-plugin-js'

export default [
  js.configs.recommended,
  {
    files: ['**/*.js'],
    languageOptions: {
      sourceType: 'commonjs',
      globals: { ...globals.node },
      ecmaVersion: 'latest',
    },
    plugins: {
      '@stylistic/js': stylisticJs,
    },
    rules: {
      '@stylistic/js/indent': ['error', 2],
      '@stylistic/js/linebreak-style': ['error', 'unix'],
      '@stylistic/js/quotes': ['error', 'single'],
      '@stylistic/js/semi': ['error', 'never'],
      eqeqeq: 'error',
      'no-trailing-spaces': 'error',
      'object-curly-spacing': ['error', 'always'],
      'arrow-spacing': ['error', { before: true, after: true }],
      'no-console': 'off',
    },
  },
  {
    ignores: ['dist/**'],
  },
]copy
```

**NB** when you make changes to the _eslint.config.mjs_ file, it is recommended to run the linter from the command line. This will verify that the configuration file is correctly formatted:
![terminal output from npm run lint](../assets/3ea8e80b2d68192b.png)
If there is something wrong in your configuration file, the lint plugin can behave quite erratically.
Many companies define coding standards that are enforced throughout the organization through the ESlint configuration file. It is not recommended to keep reinventing the wheel over and over again, and it can be a good idea to adopt a ready-made configuration from someone else's project into yours. Recently many projects have adopted the Airbnb 
You can find the code for our current application in its entirety in the _part3-7_ branch of 
### Exercise 3.22.
#### 3.22: Lint configuration
Add ESlint to your application and fix all the warnings.
This was the last exercise of this part of the course. It's time to push your code to GitHub and mark all of your finished exercises to the 
[ Part 3c **Previous part** ](../part3/01-saving-data-to-mongo-db.md)[ Part 4 **Next part** ](../part4/01-part4.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)