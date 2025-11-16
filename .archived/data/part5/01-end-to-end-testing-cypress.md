---{
  "title": "End to end testing: Cypress",
  "source_url": "https://fullstackopen.com/en/part5/end_to_end_testing_cypress",
  "crawl_timestamp": "2025-10-04T19:16:37Z",
  "checksum": "9bf87865e51d10bb3fc19c66b36e02704c266e9c62624511006af58aa70a8b7a"
}
---[Skip to content](../part5/01-end-to-end-testing-cypress-course-main-content.md)
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
End to end testing: Cypress
[a Login in frontend](../part5/01-login-in-frontend.md)[b props.children and proptypes](../part5/01-props-children-and-proptypes.md)[c Testing React apps](../part5/01-testing-react-apps.md)[d End to end testing: Playwright](../part5/01-end-to-end-testing-playwright.md)
e End to end testing: Cypress

- [Cypress](../part5/01-end-to-end-testing-cypress-cypress.md)
- [Writing to a form](../part5/01-end-to-end-testing-cypress-writing-to-a-form.md)
- [Testing new note form](../part5/01-end-to-end-testing-cypress-testing-new-note-form.md)
- [Controlling the state of the database](../part5/01-end-to-end-testing-cypress-controlling-the-state-of-the-database.md)
- [Failed login test](../part5/01-end-to-end-testing-cypress-failed-login-test.md)
- [Bypassing the UI](../part5/01-end-to-end-testing-cypress-bypassing-the-ui.md)
- [Changing the importance of a note](../part5/01-end-to-end-testing-cypress-changing-the-importance-of-a-note.md)
- [Running and debugging the tests](../part5/01-end-to-end-testing-cypress-running-and-debugging-the-tests.md)
- [Exercises 5.17.-5.23.](../part5/01-end-to-end-testing-cypress-exercises-5-17-5-23.md)


e
# End to end testing: Cypress
If your choice is Cypress, please proceed. If you end up using Playwright, go [here](../part5/01-end-to-end-testing-playwright.md).
### Cypress
E2E library
Let's make some end-to-end tests for our note application.
Unlike the backend tests or unit tests done on the React front-end, End to End tests do not need to be located in the same npm project where the code is. Let's make a completely separate project for the E2E tests with the _npm init_ command. Then install Cypress to _the new project_ as a development dependency

```
npm install --save-dev cypresscopy
```

and by adding an npm-script to run it:

```
{
  // ...
  "scripts": {
    "cypress:open": "cypress open"  },
  // ...
}copy
```

We also made a small change to the script that starts the application, without the change Cypress can not access the app.
Unlike the frontend's unit tests, Cypress tests can be in the frontend or the backend repository, or even in their separate repository.
The tests require that the system being tested is running. Unlike our backend integration tests, Cypress tests _do not start_ the system when they are run.
Let's add an npm script to _the backend_ which starts it in test mode, or so that _NODE_ENV_ is _test_.

```
{
  // ...
  "scripts": {
    "start": "cross-env NODE_ENV=production node index.js",
    "dev": "cross-env NODE_ENV=development node --watch index.js",
    "test": "cross-env NODE_ENV=test node --test",
    "lint": "eslint .",
    // ...
    "start:test": "cross-env NODE_ENV=test node --watch index.js"  },
  // ...
}copy
```

**NB** To get Cypress working with WSL2 one might need to do some additional configuring first. These two
When both the backend and frontend are running, we can start Cypress with the command

```
npm run cypress:opencopy
```

Cypress asks what type of tests we are doing. Let us answer "E2E Testing":
![cypress arrow towards e2e testing option](../assets/8cde17dfa3540688.png)
Next a browser is selected (e.g. Chrome) and then we click "Create new spec":
![create new spec with arrow pointing towards it](../assets/8dfd4f1376f734dc.png)
Let us create the test file _cypress/e2e/note_app.cy.js_ :
![cypress with path cypress/e2e/note_app.cy.js](../assets/8a2c4757792ddb07.png)
We could edit the tests in Cypress but let us rather use VS Code:
![vscode showing edits of test and cypress showing spec added](../assets/c4766d11668eec63.png)
We can now close the edit view of Cypress.
Let us change the test content as follows:

```
describe('Note app', function() {
  it('front page can be opened', function() {
    cy.visit('http://localhost:5173')
    cy.contains('Notes')
    cy.contains('Note app, Department of Computer Science, University of Helsinki 2025')
  })
})copy
```

The test is run by clicking on the test in Cypress:
Running the test shows how the application behaves as the test is run:
![cypress showing automation of note test](../assets/a1cd0a62d2750e21.png)
The structure of the test should look familiar. They use _describe_ blocks to group different test cases, just like Vitest. The test cases have been defined with the _it_ method. Cypress borrowed these parts from the
We could have declared the test using an arrow function

```
describe('Note app', () => {  it('front page can be opened', () => {    cy.visit('http://localhost:5173')
    cy.contains('Notes')
    cy.contains('Note app, Department of Computer Science, University of Helsinki 2025')
  })
})copy
```

However, Mocha
If _cy.contains_ does not find the text it is searching for, the test does not pass. So if we extend our test like so

```
describe('Note app', function() {
  it('front page can be opened',  function() {
    cy.visit('http://localhost:5173')
    cy.contains('Notes')
    cy.contains('Note app, Department of Computer Science, University of Helsinki 2025')
  })

  it('front page contains random text', function() {    cy.visit('http://localhost:5173')    cy.contains('wtf is this app?')  })})copy
```

the test fails
![cypress showing failure expecting to find wtf but no](../assets/127ca79549698743.png)
Let's remove the failing code from the test.
### Writing to a form
Let's extend our tests so that our new test tries to login to our application. We assume our backend contains a user with the username _mluukkai_ and password _salainen_.
The test begins by opening the login form.

```
describe('Note app',  function() {
  // ...

  it('user can login', function() {
    cy.visit('http://localhost:5173')
    cy.contains('button', 'login').click()
  })
})copy
```

The test first searches for a _button_ element with the desired text and clicks the button with the command
Both of our tests begin the same way, by opening the page _beforeEach_ block run before each test:

```
describe('Note app', function() {
  beforeEach(function() {    cy.visit('http://localhost:5173')  })
  it('front page can be opened', function() {
    cy.contains('Notes')
    cy.contains('Note app, Department of Computer Science, University of Helsinki 2025')
  })

  it('user can login', function() {
    cy.contains('button', 'login').click()
  })
})copy
```

The login field contains two _input_ fields, which the test should write into.
The
We can access the first and the last input field on the page, and write to them with the command

```
it('user can login', function () {
  cy.contains('button', 'login').click()
  cy.get('input:first').type('mluukkai')
  cy.get('input:last').type('salainen')
})  copy
```

The test works. The problem is if we later add more input fields, the test will break because it expects the fields it needs to be the first and the last on the page.
Let's take advantage of the existing elements of the login form. The input fields of the login form have been assigned unique _labels_ :

```
// ...
<form onSubmit={handleSubmit}>
  <div>
    <label>      username      <input
        type="text"
        value={username}
        onChange={handleUsernameChange}
      />
    </label>  </div>
  <div>
    <label>      password      <input
        type="password"
        value={password}
        onChange={handlePasswordChange}
      />
    </label>  </div>
  <button type="submit">login</button>
</form>
// ...copy
```

Input fields can and should be located in tests using _labels_ :

```
describe('Note app', function () {
  // ...

  it('user can login', function () {
    cy.contains('button', 'login').click()
    cy.contains('label', 'username').type('mluukkai')    cy.contains('label', 'password').type('salainen')  })
})copy
```

When locating elements, it makes sense to aim to utilize the content visible to the user in the interface, as this best simulates how a user would actually find the desired input field while navigating the application.
When the username and password have been entered into the form, the next step is to press the _login_ button. However, this causes a bit of a headache, since there are actually two _login_ buttons on the page. The _Togglable_ component we are using also contains a button with the same name, which is hidden by giving it the visibility attribute style="display: none" when the login form is visible.
To ensure that the test clicks the correct button, we assign a unique _id_ attribute to the login form’s _login_ button:

```
const LoginForm = ({ ... }) => {
  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        // 

        <button id="login-button" type="submit">          login
        </button>
      </form>
    </div>
  )
}copy
```

The test becomes:

```
describe('Note app',  function() {
  // ..
  it('user can login', function () {
    cy.contains('button', 'login').click()
    cy.contains('label', 'username').type('mluukkai')
    cy.contains('label', 'password').type('salainen')
    cy.get('#login-button').click()
    cy.contains('Matti Luukkainen logged in')  })
})copy
```

The last row ensures that the login was successful.
Note that the CSS's _login-button_ the CSS selector is _#login-button_.
Please note that passing the test at this stage requires that there is a user in the test database of the backend test environment, whose username is _mluukkai_ and the password is _salainen_. Create a user if needed!
### Testing new note form
Next, let's add tests to test the "new note" functionality:

```
describe('Note app', function() {
  // ..
  describe('when logged in', function() {    beforeEach(function() {      cy.contains('button', 'login').click()      cy.contains('label', 'username').type('mluukkai')      cy.contains('label', 'password').type('salainen')      cy.get('#login-button').click()    })
    it('a new note can be created', function() {      cy.contains('new note').click()      cy.get('input').type('a note created by cypress')      cy.contains('save').click()      cy.contains('a note created by cypress')    })  })})copy
```

The test has been defined in its own _describe_ block. Only logged-in users can create new notes, so we added logging in to the application to a _beforeEach_ block.
The test trusts that when creating a new note the page contains only one input, so it searches for it like so:

```
cy.get('input')copy
```

If the page contained more inputs, the test would break
![cypress error - cy.type can only be called on a single element](../assets/3e025d75f89de9c7.png)
Due to this problem, it would again be better to give the input an _ID_ and search for the element by its ID. Let's stick with the simplest solution for now.
The structure of the tests looks like so:

```
describe('Note app', function() {
  // ...

  it('user can login', function() {
    cy.contains('button', 'login').click()
    cy.contains('label', 'username').type('mluukkai')
    cy.contains('label', 'password').type('salainen')
    cy.get('#login-button').click()

    cy.contains('Matti Luukkainen logged in')
  })

  describe('when logged in', function() {
    beforeEach(function() {
      cy.contains('button', 'login').click()
      cy.contains('label', 'username').type('mluukkai')
      cy.contains('label', 'password').type('salainen')
      cy.get('#login-button').click()
    })

    it('a new note can be created', function() {
      // ...
    })
  })
})copy
```

Cypress runs the tests in the order they are in the code. So first it runs _user can login_ , where the user logs in. Then cypress will run _a new note can be created_ for which a _beforeEach_ block logs in as well. Why do this? Isn't the user logged in after the first test? No, because _each_ test starts from zero as far as the browser is concerned. All changes to the browser's state are reversed after each test.
### Controlling the state of the database
If the tests need to be able to modify the server's database, the situation immediately becomes more complicated. Ideally, the server's database should be the same each time we run the tests, so our tests can be reliably and easily repeatable.
As with unit and integration tests, with E2E tests it is best to empty the database and possibly format it before the tests are run. The challenge with E2E tests is that they do not have access to the database.
The solution is to create API endpoints for the backend tests. We can empty the database using these endpoints. Let's create a new router for the tests inside the _controllers_ folder, in the _testing.js_ file

```
const testingRouter = require('express').Router()
const Note = require('../models/note')
const User = require('../models/user')

testingRouter.post('/reset', async (request, response) => {
  await Note.deleteMany({})
  await User.deleteMany({})

  response.status(204).end()
})

module.exports = testingRoutercopy
```

and add it to the backend only _if the application is run in test-mode_ :

```
// ...

app.use('/api/login', loginRouter)
app.use('/api/users', usersRouter)
app.use('/api/notes', notesRouter)

if (process.env.NODE_ENV === 'test') {  const testingRouter = require('./controllers/testing')  app.use('/api/testing', testingRouter)}
app.use(middleware.unknownEndpoint)
app.use(middleware.errorHandler)

module.exports = appcopy
```

After the changes, an HTTP POST request to the _/api/testing/reset_ endpoint empties the database. Make sure your backend is running in test mode by starting it with this command (previously configured in the package.json file):

```
  npm run start:testcopy
```

The modified backend code can be found on the _part5-1_.
Next, we will change the _beforeEach_ block so that it empties the server's database before tests are run.
Currently, it is not possible to add new users through the frontend's UI, so we add a new user to the backend from the beforeEach block.

```
describe('Note app', function() {
   beforeEach(function() {
    cy.request('POST', 'http://localhost:3001/api/testing/reset')    const user = {      name: 'Matti Luukkainen',      username: 'mluukkai',      password: 'salainen'    }    cy.request('POST', 'http://localhost:3001/api/users/', user)     cy.visit('http://localhost:5173')
  })
  
  it('front page can be opened', function() {
    // ...
  })

  it('user can login', function() {
    // ...
  })

  describe('when logged in', function() {
    // ...
  })
})copy
```

During the formatting, the test does HTTP requests to the backend with
Unlike earlier, now the testing starts with the backend in the same state every time. The backend will contain one user and no notes.
Let's add one more test for checking that we can change the importance of notes.
A while ago we changed the frontend so that a new note is important by default, so the _important_ field is _true_ :

```
const NoteForm = ({ createNote }) => {
  // ...

  const addNote = (event) => {
    event.preventDefault()
    createNote({
      content: newNote,
      important: true    })

    setNewNote('')
  }
  // ...
} copy
```

There are multiple ways to test this. In the following example, we first search for a note and click its _make not important_ button. Then we check that the note now contains a _make important_ button.

```
describe('Note app', function() {
  // ...

  describe('when logged in', function() {
    // ...

    describe('and a note exists', function () {
      beforeEach(function () {
        cy.contains('new note').click()
        cy.get('input').type('another note cypress')
        cy.contains('save').click()
      })

      it('it can be made not important', function () {
        cy.contains('another note cypress')
          .contains('button', 'make not important')
          .click()

        cy.contains('another note cypress')
          .contains('button', 'make important')
      })
    })
  })
})copy
```

The first command does several things. First, it searches for an element containing the text _another note cypress_. Then, within the found element, it searches for the _make not important_ button and clicks it.
The second command checks that the text on the button has changed to _make important_.
### Failed login test
Let's make a test to ensure that a login attempt fails if the password is wrong.
Cypress will run all tests each time by default, and as the number of tests increases, it starts to become quite time-consuming. When developing a new test or when debugging a broken test, we can define the test with _it.only_ instead of _it_ , so that Cypress will only run the required test. When the test is working, we can remove _.only_.
First version of our tests is as follows:

```
describe('Note app', function() {
  // ...

  it.only('login fails with wrong password', function() {
    cy.contains('button', 'login').click()
    cy.contains('label', 'username').type('mluukkai')
    cy.contains('label', 'password').type('wrong')
    cy.get('#login-button').click()

    cy.contains('wrong credentials')
  })

  // ...
)}copy
```

The test uses
The application renders the error message to a component with the CSS class _error_ :

```
const Notification = ({ message }) => {
  if (message === null) {
    return null
  }

  return (
    <div className="error">      {message}
    </div>
  )
}copy
```

We could make the test ensure that the error message is rendered to the correct component, that is, the component with the CSS class _error_ :

```
it('login fails with wrong password', function() {
  // ...

  cy.get('.error').contains('wrong credentials')})copy
```

First, we use _error_. Then we check that the error message can be found in this component. Note that the _error_ is _.error_.
We could do the same using the

```
it('login fails with wrong password', function() {
  // ...

  cy.get('.error').should('contain', 'wrong credentials')})copy
```

Using should is a bit trickier than using _contains_ , but it allows for more diverse tests than _contains_ which works based on text content only.
A list of the most common assertions which can be used with _should_ can be found
We can, for example, make sure that the error message is red and it has a border:

```
it('login fails with wrong password', function() {
  // ...

  cy.get('.error').should('contain', 'wrong credentials') 
  cy.get('.error').should('have.css', 'color', 'rgb(255, 0, 0)')
  cy.get('.error').should('have.css', 'border-style', 'solid')
})copy
```

Cypress requires the colors to be given as
Because all tests are for the same component we accessed using

```
it('login fails with wrong password', function() {
  // ...

  cy.get('.error')
    .should('contain', 'wrong credentials')
    .and('have.css', 'color', 'rgb(255, 0, 0)')
    .and('have.css', 'border-style', 'solid')
})copy
```

Let's finish the test so that it also checks that the application does not render the success message _'Matti Luukkainen logged in'_ :

```
it('login fails with wrong password', function() {
  cy.contains('button', 'login').click()
  cy.contains('label', 'username').type('mluukkai')
  cy.contains('label', 'password').type('wrong')
  cy.get('#login-button').click()

  cy.get('.error')
    .should('contain', 'wrong credentials')
    .and('have.css', 'color', 'rgb(255, 0, 0)')
    .and('have.css', 'border-style', 'solid')

  cy.get('html').should('not.contain', 'Matti Luukkainen logged in')})copy
```

The command _should_ is most often used by chaining it after the command _get_ (or another similar command that can be chained). The _cy.get('html')_ used in the test practically means the visible content of the entire application.
We would also check the same by chaining the command _contains_ with the command _should_ with a slightly different parameter:

```
cy.contains('Matti Luukkainen logged in').should('not.exist')copy
```

**NOTE:** Some CSS properties
![running](../assets/df353e2cd71ed965.png)
then tests that involve, for example, `border-style`, `border-radius` and `padding`, will pass in Chrome or Electron, but fail in Firefox:
![borderstyle](../assets/b3b1c7810633381c.png)
### Bypassing the UI
Currently, we have the following tests:

```
describe('Note app', function() {
  it('user can login', function() {
    cy.contains('button', 'login').click()
    cy.contains('label', 'username').type('mluukkai')
    cy.contains('label', 'password').type('salainen')
    cy.get('#login-button').click()

    cy.contains('Matti Luukkainen logged in')
  })

  it('login fails with wrong password', function() {
    // ...
  })

  describe('when logged in', function() {
    beforeEach(function() {
      cy.contains('button', 'login').click()
      cy.contains('label', 'username').type('mluukkai')
      cy.contains('label', 'password').type('salainen')
      cy.get('#login-button').click()
    })

    it('a new note can be created', function() {
      // ... 
    })
   
  })
})copy
```

First, we test logging in. Then, in their own describe block, we have a bunch of tests, which expect the user to be logged in. User is logged in in the _beforeEach_ block.
As we said above, each test starts from zero! Tests do not start from the state where the previous tests ended.
The Cypress documentation gives us the following advice: _beforeEach_ block, we are going to bypass the UI and do a HTTP request to the backend to login. The reason for this is that logging in with a HTTP request is much faster than filling out a form.
Our situation is a bit more complicated than in the example in the Cypress documentation because when a user logs in, our application saves their details to the localStorage. However, Cypress can handle that as well. The code is the following:

```
describe('when logged in', function() {
  beforeEach(function() {
    cy.request('POST', 'http://localhost:3001/api/login', {      username: 'mluukkai', password: 'salainen'    }).then(response => {      localStorage.setItem('loggedNoteappUser', JSON.stringify(response.body))      cy.visit('http://localhost:5173')    })  })

  it('a new note can be created', function() {
    // ...
  })

  // ...
})copy
```

We can access to the response of a _cy.request_ , like all Cypress commands, are
If and when we write new tests to our application, we have to use the login code in multiple places, we should make it a
Custom commands are declared in _cypress/support/commands.js_. The code for logging in is as follows:

```
Cypress.Commands.add('login', ({ username, password }) => {
  cy.request('POST', 'http://localhost:3001/api/login', {
    username, password
  }).then(({ body }) => {
    localStorage.setItem('loggedNoteappUser', JSON.stringify(body))
    cy.visit('http://localhost:5173')
  })
})copy
```

Using our custom command is easy, and our test becomes cleaner:

```
describe('when logged in', function() {
  beforeEach(function() {
    cy.login({ username: 'mluukkai', password: 'salainen' })  })

  it('a new note can be created', function() {
    // ...
  })

  // ...
})copy
```

The same applies to creating a new note now that we think about it. We have a test, which makes a new note using the form. We also make a new note in the _beforeEach_ block of the test that changes the importance of a note:

```
describe('Note app', function() {
  // ...

  describe('when logged in', function() {
    beforeEach(function () {
      cy.login({ username: 'mluukkai', password: 'salainen' })
    })

    it('a new note can be created', function() {
      cy.contains('new note').click()
      cy.get('input').type('a note created by cypress')
      cy.contains('save').click()

      cy.contains('a note created by cypress')
    })

    describe('and a note exists', function () {
      beforeEach(function () {
        cy.contains('new note').click()        cy.get('input').type('another note cypress')        cy.contains('save').click()      })

      it('it can be made important', function () {
        // ...
      })
    })
  })
})copy
```

Let's make a new custom command for making a new note. The command will make a new note with an HTTP POST request:

```
Cypress.Commands.add('createNote', ({ content, important }) => {
  cy.request({
    url: 'http://localhost:3001/api/notes',
    method: 'POST',
    body: { content, important },
    headers: {
      'Authorization': `Bearer ${JSON.parse(localStorage.getItem('loggedNoteappUser')).token}`
    }
  })

  cy.visit('http://localhost:5173')
})copy
```

The command expects the user to be logged in and the user's details to be saved to localStorage.
Now the note beforeEach block becomes:

```
describe('Note app', function() {
  // ...

  describe('when logged in', function() {
    // ...

    describe('and a note exists', function () {
      beforeEach(function () {
        cy.createNote({          content: 'another note cypress',          important: true        })      })

      it('it can be made important', function () {
        // ...
      })
    })
  })
})copy
```

There is one more annoying feature in our tests. The frontend address _http:localhost:5173/api_ to the backend:

```
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:3001',
        changeOrigin: true,
      },
    }
  },
  // ...
})copy
```

So we can replace all the addresses in the tests from
Let's define the _baseUrl_ for the application in the Cypress pre-generated _cypress.config.js_ :

```
const { defineConfig } = require("cypress")

module.exports = defineConfig({
  e2e: {
    setupNodeEvents(on, config) {
    },
    baseUrl: 'http://localhost:5173'  },
})copy
```

All commands in the tests and in the _command.js_ file that use the application's address

```
cy.visit('http://localhost:5173')copy
```

can be transformed into

```
cy.visit('')copy
```

### Changing the importance of a note
Lastly, let's take a look at the test we did for changing the importance of a note. First, we'll change the beforeEach block so that it creates three notes instead of one. The tests change as follows:

```
describe('when logged in', function () {
  beforeEach(function () {
    cy.login({ username: 'mluukkai', password: 'salainen' })
  })

  it('a new note can be created', function () {
    cy.contains('new note').click()
    cy.get('input').type('a note created by cypress')
    cy.contains('save').click()
    cy.contains('a note created by cypress')
  })
  describe('and several notes exist', function () {    beforeEach(function () {
      cy.createNote({ content: 'first note', important: true })      cy.createNote({ content: 'second note', important: true })      cy.createNote({ content: 'third note', important: true })    })

    it('one of those can be made non important', function () {      cy.contains('second note')        .contains('button', 'make not important')
        .click()

      cy.contains('second note')        .contains('button', 'make important')
    })
  })
})copy
```

How does the
When we click the _-contains 'second note'_ command in Cypress _second note_ :
![cypress test runner clicking second note](../assets/ff1d3174297ea378.png)
By clicking the next line _-contains 'button, make not important'_ we see that the test uses the _make not important_ button corresponding to the _second note_ :
![cypress test runner clicking make important](../assets/2a192ef5618dc0ff.png)
When chained, the second _contains_ command _continues_ the search from within the component found by the first command.
If we had not chained the commands, and instead write:

```
cy.contains('second note')
cy.contains('button', 'make not important').click()copy
```

the result would have been entirely different. The second line of the test would click the button of a wrong note:
![cypress showing error and incorrectly trying to click first button](../assets/aef801099adbf33e.png)
When coding tests, you should check in the test runner that the tests use the right components!
Let's change the _Note_ component so that the text of the note is rendered to a _span_.

```
const Note = ({ note, toggleImportance }) => {
  const label = note.important
    ? 'make not important' : 'make important'

  return (
    <li className='note'>
      <span>{note.content}</span>      <button onClick={toggleImportance}>{label}</button>
    </li>
  )
}copy
```

Our tests break! As the test runner reveals, _cy.contains('second note')_ now returns the component containing the text, and the button is not in it.
![cypress showing test is broken trying to click make important](../assets/e68d4b38327b186c.png)
One way to fix this is the following:

```
it('one of those can be made non important', function () {
  cy.contains('second note').parent().find('button').click()
  cy.contains('second note')
    .parent()
    .find('button')
    .should('contain', 'make important')
})copy
```

In the first line, we use the _second note_ and find the button from within it. Then we click the button and check that the text on it changes.
Note that we use the command _whole_ page and would return all 5 buttons on the page.
Unfortunately, we have some copy-paste in the tests now, because the code for searching for the right button is always the same.
In these kinds of situations, it is possible to use the

```
it('one of those can be made non important', function () {
  cy.contains('second note').parent().find('button').as('theButton')
  cy.get('@theButton').click()
  cy.get('@theButton').should('contain', 'make important')
})copy
```

Now the first line finds the right button and uses _as_ to save it as _theButton_. The following lines can use the named element with _cy.get('@theButton')_.
### Running and debugging the tests
Finally, some notes on how Cypress works and debugging your tests.
Because of the form of the Cypress tests, it gives the impression that they are normal JavaScript code, and we could for example try this:

```
const button = cy.contains('button', 'login')
button.click()
debugger
cy.contains('logout').click()copy
```

This won't work, however. When Cypress runs a test, it adds each _cy_ command to an execution queue. When the code of the test method has been executed, Cypress will execute each command in the queue one by one.
Cypress commands always return _undefined_ , so _button.click()_ in the above code would cause an error. An attempt to start the debugger would not stop the code between executing the commands, but before any commands have been executed.
Cypress commands are _like promises_ , so if we want to access their return values, we have to do it using the

```
it('then example', function() {
  cy.get('button').then( buttons => {
    console.log('number of buttons', buttons.length)
    cy.wrap(buttons[0]).click()
  })
})copy
```

Stopping the test execution with the debugger is
The developer console is all sorts of useful when debugging your tests. You can see the HTTP requests done by the tests on the Network tab, and the console tab will show you information about your tests:
![developer console while running cypress](../assets/419db8bcf1affe80.png)
So far we have run our Cypress tests using the graphical test runner. It is also possible to run them

```
  "scripts": {
    "cypress:open": "cypress open",
    "test:e2e": "cypress run"  },copy
```

Now we can run our tests from the command line with the command _npm run test:e2e_
![terminal output of running npm e2e tests showing passed](../assets/124e73456591633e.png)
It is also possible to record a video of the test execution in Cypress. Recording a video can be especially useful, for example, when debugging or in a CI/CD pipeline, as the video allows you to easily review what happened in the browser before an error occurred. The feature is disabled by default; instructions for enabling it can be found in the Cypress
Tests are found in
Final version of the frontend code can be found on the _part5-9_.
### Exercises 5.17.-5.23
In the last exercises of this part, we will do some E2E tests for our blog application. The material of this part should be enough to complete the exercises. You **must check out the Cypress**. It is probably the best documentation I have ever seen for an open-source project.
I especially recommend reading
> _This is the single most important guide for understanding how to test with Cypress. Read it. Understand it._
#### 5.17: Blog List End To End Testing, step 1
Configure Cypress for your project. Make a test for checking that the application displays the login form by default.
The structure of the test must be as follows:

```
describe('Blog app', function() {
  beforeEach(function() {
    cy.visit('http://localhost:5173')
  })

  it('Login form is shown', function() {
    // ...
  })
})copy
```

#### 5.18: Blog List End To End Testing, step 2
Make tests for logging in. Test both successful and unsuccessful login attempts. Make a new user in the _beforeEach_ block for the tests.
The test structure extends like so:

```
describe('Blog app', function() {
  beforeEach(function() {
    // empty the db here
    // create a user for the backend here
    cy.visit('http://localhost:5173')
  })

  it('Login form is shown', function() {
    // ...
  })

  describe('Login',function() {
    it('succeeds with correct credentials', function() {
      // ...
    })

    it('fails with wrong credentials', function() {
      // ...
    })
  })
})copy
```

The _beforeEach_ block must empty the database using, for example, the reset method we used in the [material](../part5/01-end-to-end-testing-cypress-controlling-the-state-of-the-database.md).
_Optional bonus exercise_ : Check that the notification shown with unsuccessful login is displayed red.
#### 5.19: Blog List End To End Testing, step 3
Make a test that verifies a logged-in user can create a new blog. The structure of the test could be as follows:

```
describe('Blog app', function() {
  // ...

  describe('When logged in', function() {
    beforeEach(function() {
      // ...
    })

    it('A blog can be created', function() {
      // ...
    })
  })

})copy
```

The test has to ensure that a new blog is added to the list of all blogs.
#### 5.20: Blog List End To End Testing, step 4
Make a test that confirms users can like a blog.
#### 5.21: Blog List End To End Testing, step 5
Make a test for ensuring that the user who created a blog can delete it.
#### 5.22: Blog List End To End Testing, step 6
Make a test for ensuring that only the creator can see the delete button of a blog, not anyone else.
#### 5.23: Blog List End To End Testing, step 7
Make a test that checks that the blogs are ordered by likes, with the most liked blog being first.
_This exercise is quite a bit trickier than the previous ones._ One solution is to add a certain class for the element which wraps the blog's content and use the

```
cy.get('.blog').eq(0).should('contain', 'The title with the most likes')
cy.get('.blog').eq(1).should('contain', 'The title with the second most likes')copy
```

Note that you might end up having problems if you click a like button many times in a row. It might be that cypress does the clicking so fast that it does not have time to update the app state in between the clicks. One remedy for this is to wait for the number of likes to update in between all clicks.
This was the last exercise of this part, and it's time to push your code to GitHub and mark the exercises you completed in the
[Part 5d **Previous part**](../part5/01-end-to-end-testing-playwright.md)[Part 6 **Next part**](../part6/01-part6.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)
