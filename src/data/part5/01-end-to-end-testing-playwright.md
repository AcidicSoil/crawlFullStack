---{
  "title": "End to end testing: Playwright",
  "source_url": "https://fullstackopen.com/en/part5/end_to_end_testing_playwright",
  "crawl_timestamp": "2025-10-04T19:16:40Z",
  "checksum": "13e245b013651f572bd5ed93438cd16a8bde455eea19eab975ff07eba90af5cf"
}
---[Skip to content](../part5/01-end-to-end-testing-playwright-course-main-content.md)
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
End to end testing: Playwright
[a Login in frontend](../part5/01-login-in-frontend.md)[b props.children and proptypes](../part5/01-props-children-and-proptypes.md)[c Testing React apps](../part5/01-testing-react-apps.md)
d End to end testing: Playwright

- [Playwright](../part5/01-end-to-end-testing-playwright-playwright.md)
- [Initializing tests](../part5/01-end-to-end-testing-playwright-initializing-tests.md)
- [Testing our own code](../part5/01-end-to-end-testing-playwright-testing-our-own-code.md)
- [Writing on the form](../part5/01-end-to-end-testing-playwright-writing-on-the-form.md)
- [Test Initialization](../part5/01-end-to-end-testing-playwright-test-initialization.md)
- [Testing note creation](../part5/01-end-to-end-testing-playwright-testing-note-creation.md)
- [Controlling the state of the database](../part5/01-end-to-end-testing-playwright-controlling-the-state-of-the-database.md)
- [Test for failed login](../part5/01-end-to-end-testing-playwright-test-for-failed-login.md)
- [Running tests one by one](../part5/01-end-to-end-testing-playwright-running-tests-one-by-one.md)
- [Helper functions for tests](../part5/01-end-to-end-testing-playwright-helper-functions-for-tests.md)
- [Note importance change revisited](../part5/01-end-to-end-testing-playwright-note-importance-change-revisited.md)
- [Test development and debugging](../part5/01-end-to-end-testing-playwright-test-development-and-debugging.md)
- [Exercises 5.17.-5.23.](../part5/01-end-to-end-testing-playwright-exercises-5-17-5-23.md)


[e End to end testing: Cypress](../part5/01-end-to-end-testing-cypress.md)
d
# End to end testing: Playwright
So far we have tested the backend as a whole on an API level using integration tests and tested some frontend components using unit tests.
Next, we will look into one way to test the _End to End_ (E2E) tests.
We can do E2E testing of a web application using a browser and a testing library. There are multiple libraries available. One example is
E2E tests are potentially the most useful category of tests because they test the system through the same interface as real users use.
They do have some drawbacks too. Configuring E2E tests is more challenging than unit or integration tests. They also tend to be quite slow, and with a large system, their execution time can be minutes or even hours. This is bad for development because during coding it is beneficial to be able to run tests as often as possible in case of code
E2E tests can also be
Perhaps the two easiest libraries for End to End testing at the moment are
From the statistics on
![cypress vs playwright in npm trends](../assets/813111145f8da6c1.png)
This course has been using Cypress for years. Now Playwright is a new addition. You can choose whether to complete the E2E testing part of the course with Cypress or Playwright. The operating principles of both libraries are very similar, so your choice is not very important. However, Playwright is now the preferred E2E library for the course.
If your choice is Playwright, please proceed. If you end up using Cypress, go [here](../part5/01-end-to-end-testing-cypress.md).
### Playwright
So
Many blogs have been written about library comparisons, e.g.
It is difficult to say which library is better. One advantage of Playwright is its browser support; Playwright supports Chrome, Firefox and Webkit-based browsers like Safari. Currently, Cypress includes support for all these browsers, although Webkit support is experimental and does not support all of Cypress features. At the time of writing (1.3.2024), my personal preference leans slightly towards Playwright.
Now let's explore Playwright.
### Initializing tests
Unlike the backend tests or unit tests done on the React front-end, End to End tests do not need to be located in the same npm project where the code is. Let's make a completely separate project for the E2E tests with the _npm init_ command. Then install Playwright by running in the new project directory the command:

```
npm init playwright@latestcopy
```

The installation script will ask a few questions, answer them as follows:
![answer: javascript, tests, false, true](../assets/a364eba2abe03642.png)
Note that when installing Playwright your operating system may not support all of the browsers Playwright offers and you may see an error message like below:

```
Webkit 18.0 (playwright build v2070) downloaded to /home/user/.cache/ms-playwright/webkit-2070
Playwright Host validation warning: 
╔══════════════════════════════════════════════════════╗
║ Host system is missing dependencies to run browsers. ║
║ Missing libraries:                                   ║
║     libicudata.so.66                                 ║
║     libicui18n.so.66                                 ║
║     libicuuc.so.66                                   ║
║     libjpeg.so.8                                     ║
║     libwebp.so.6                                     ║
║     libpcre.so.3                                     ║
║     libffi.so.7                                      ║
╚══════════════════════════════════════════════════════╝copy
```

If this is the case you can either specify specific browsers to test with `--project=` in your _package.json_ :

```
    "test": "playwright test --project=chromium --project=firefox",copy
```

or remove the entry for any problematic browsers from your _playwright.config.js_ file:

```
  projects: [
    // ...
    //{
    //  name: 'webkit',
    //  use: { ...devices['Desktop Safari'] },
    //},
    // ...
  ]copy
```

Let's define an npm script for running tests and test reports in _package.json_ :

```
{
  // ...
  "scripts": {
    "test": "playwright test",
    "test:report": "playwright show-report"
  },
  // ...
}copy
```

During installation, the following is printed to the console:

```
And check out the following files:
  - ./tests/example.spec.js - Example end-to-end test
  - ./tests-examples/demo-todo-app.spec.js - Demo Todo App end-to-end tests
  - ./playwright.config.js - Playwright Test configurationcopy
```

that is, the location of a few example tests for the project that the installation has created.
Let's run the tests:

```
$ npm test

> notes-e2e@1.0.0 test
> playwright test


Running 6 tests using 5 workers
  6 passed (3.9s)

To open last HTML report run:

  npx playwright show-reportcopy
```

The tests pass. A more detailed test report can be opened either with the command suggested by the output, or with the npm script we just defined:

```
npm run test:reportcopy
```

Tests can also be run via the graphical UI with the command:

```
npm run test -- --uicopy
```

Sample tests in the file tests/example.spec.js look like this:

```
// @ts-check
import { test, expect } from '@playwright/test';

test('has title', async ({ page }) => {
  await page.goto('https://playwright.dev/');
  // Expect a title "to contain" a substring.
  await expect(page).toHaveTitle(/Playwright/);
});

test('get started link', async ({ page }) => {
  await page.goto('https://playwright.dev/');

  // Click the get started link.
  await page.getByRole('link', { name: 'Get started' }).click();

  // Expects page to have a heading with the name of Installation.
  await expect(page.getByRole('heading', { name: 'Installation' })).toBeVisible();
});copy
```

The first line of the test functions says that the tests are testing the page at
### Testing our own code
Now let's remove the sample tests and start testing our own application.
Playwright tests assume that the system under test is running when the tests are executed. Unlike, for example, backend integration tests, Playwright tests _do not start_ the system under test during testing.
Let's make an npm script for the _backend_ , which will enable it to be started in testing mode, i.e. so that _NODE_ENV_ gets the value _test_.

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

Let's start the frontend and backend, and create the first test file for the application `tests/note_app.spec.js`:

```
const { test, expect } = require('@playwright/test')

test('front page can be opened', async ({ page }) => {
  await page.goto('http://localhost:5173')

  const locator = page.getByText('Notes')
  await expect(locator).toBeVisible()
  await expect(page.getByText('Note app, Department of Computer Science, University of Helsinki 2024')).toBeVisible()
})copy
```

First, the test opens the application with the method _Notes_ is found.
The method
The second check is done without using the auxiliary variable.
The test fails because an old year ended up in the test. Playwright opens the test report in the browser and it becomes clear that Playwright has actually performed the tests with three different browsers: Chrome, Firefox and Webkit, i.e. the browser engine used by Safari:
![test report showing the test failing in three different browsers](../assets/77e19ea08958d4d9.png)
By clicking on the report of one of the browsers, we can see a more detailed error message:
![test error message](../assets/d0f64faaed763520.png)
In the big picture, it is of course a very good thing that the testing takes place with all three commonly used browser engines, but this is slow, and when developing the tests it is probably best to carry them out mainly with only one browser. You can define the browser engine to be used with the command line parameter:

```
npm test -- --project chromiumcopy
```

Now let's fix the test with the correct year and let's add a _describe_ block to the tests:

```
const { test, describe, expect } = require('@playwright/test')

describe('Note app', () => {  test('front page can be opened', async ({ page }) => {
    await page.goto('http://localhost:5173')

    const locator = page.getByText('Notes')
    await expect(locator).toBeVisible()
    await expect(page.getByText('Note app, Department of Computer Science, University of Helsinki 2025')).toBeVisible()
  })
})copy
```

Before we move on, let's break the tests one more time. We notice that the execution of the tests is quite fast when they pass, but much slower if the they do not pass. The reason for this is that Playwright's policy is to wait for searched elements until _TimeoutError_ is raised and the test fails. Playwright waits for elements by default for 5 or 30 seconds
When developing tests, it may be wiser to reduce the waiting time to a few seconds. According to the _playwright.config.js_ as follows:

```
export default defineConfig({
  // ...
  timeout: 3000,  fullyParallel: false,  workers: 1,  // ...
})copy
```

We also made two other changes to the file, specifying that all tests
### Writing on the form
Let's write a new test that tries to log into the application. Let's assume that a user is stored in the database, with username _mluukkai_ and password _salainen_.
Let's start by opening the login form.

```
describe('Note app', () => {
  // ...

  test('user can log in', async ({ page }) => {
    await page.goto('http://localhost:5173')

    await page.getByRole('button', { name: 'login' }).click()
  })
})copy
```

The test first uses the method
When developing tests, you could use Playwright's

```
npm test -- --uicopy
```

We now see that the test finds the button
![playwright UI rendering the notes app while testing it](../assets/3c9b8672c75b153b.png)
After clicking, the form will appear
![playwright UI rendering the login form of the notes app](../assets/2dbc2ccfa8318e0f.png)
When the form is opened, the test should look for the text fields and enter the username and password in them. Let's make the first attempt using the method

```
describe('Note app', () => {
  // ...

  test('user can log in', async ({ page }) => {
    await page.goto('http://localhost:5173')

    await page.getByRole('button', { name: 'login' }).click()
    await page.getByRole('textbox').fill('mluukkai')  })
})copy
```

This results to an error:

```
Error: locator.fill: Error: strict mode violation: getByRole('textbox') resolved to 2 elements:
  1) <input value=""/> aka locator('div').filter({ hasText: /^username$/ }).getByRole('textbox')
  2) <input value="" type="password"/> aka locator('input[type="password"]')copy
```

The problem now is that _getByRole_ finds two text fields, and calling the

```
describe('Note app', () => {
  // ...

  test('user can log in', async ({ page }) => {
    await page.goto('http://localhost:5173')

    await page.getByRole('button', { name: 'login' }).click()
    await page.getByRole('textbox').first().fill('mluukkai')    await page.getByRole('textbox').last().fill('salainen')    await page.getByRole('button', { name: 'login' }).click()    await expect(page.getByText('Matti Luukkainen logged in')).toBeVisible()  })
})copy
```

After writing in the text fields, the test presses the _login_ button and checks that the application renders the logged-in user's information on the screen.
If there were more than two text fields, using the methods _first_ and _last_ would not be enough. One possibility would be to use the

```
describe('Note app', () => {
  // ...
  test('user can log in', async ({ page }) => {
    await page.goto('http://localhost:5173')

    await page.getByRole('button', { name: 'login' }).click()
    const textboxes = await page.getByRole('textbox').all()    await textboxes[0].fill('mluukkai')    await textboxes[1].fill('salainen')
    await page.getByRole('button', { name: 'login' }).click()
  
    await expect(page.getByText('Matti Luukkainen logged in')).toBeVisible()
  })  
})copy
```

Both this and the previous version of the test work. However, both are problematic to the extent that if the registration form is changed, the tests may break, as they rely on the fields to be on the page in a certain order.
If an element is difficult to locate in tests, you can assign it a separate _test-id_ attribute and find the element in tests using the
Let's now take advantage of the existing elements of the login form. The input fields of the login form have been assigned unique _labels_ :

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

Input fields can and should be located in tests using _labels_ with the

```
describe('Note app', () => {
  // ...

  test('user can log in', async ({ page }) => {
    await page.goto('http://localhost:5173')

    await page.getByRole('button', { name: 'login' }).click()
    await page.getByLabel('username').fill('mluukkai')    await page.getByLabel('password').fill('salainen')  
    await page.getByRole('button', { name: 'login' }).click() 
  
    await expect(page.getByText('Matti Luukkainen logged in')).toBeVisible()
  })
})copy
```

When locating elements, it makes sense to aim to utilize the content visible to the user in the interface, as this best simulates how a user would actually find the desired input field while navigating the application.
Note that passing the test at this stage requires that there is a user in the _test_ database of the backend with username _mluukkai_ and password _salainen_. Create a user if needed!
### Test Initialization
Since both tests start in the same way, i.e. by opening the page _beforeEach_ block that is executed before each test:

```
const { test, describe, expect, beforeEach } = require('@playwright/test')

describe('Note app', () => {
  beforeEach(async ({ page }) => {    await page.goto('http://localhost:5173')  })
  test('front page can be opened', async ({ page }) => {
    const locator = page.getByText('Notes')
    await expect(locator).toBeVisible()
    await expect(page.getByText('Note app, Department of Computer Science, University of Helsinki 2025')).toBeVisible()
  })

  test('user can log in', async ({ page }) => {
    await page.getByRole('button', { name: 'login' }).click()
    await page.getByLabel('username').fill('mluukkai')
    await page.getByLabel('password').fill('salainen')
    await page.getByRole('button', { name: 'login' }).click()
    await expect(page.getByText('Matti Luukkainen logged in')).toBeVisible()
  })
})copy
```

### Testing note creation
Next, let's create a test that adds a new note to the application:

```
const { test, describe, expect, beforeEach } = require('@playwright/test')

describe('Note app', () => {
  // ...

  describe('when logged in', () => {
    beforeEach(async ({ page }) => {
      await page.getByRole('button', { name: 'login' }).click()
      await page.getByLabel('username').fill('mluukkai')
      await page.getByLabel('password').fill('salainen')
      await page.getByRole('button', { name: 'login' }).click()
    })

    test('a new note can be created', async ({ page }) => {
      await page.getByRole('button', { name: 'new note' }).click()
      await page.getByRole('textbox').fill('a note created by playwright')
      await page.getByRole('button', { name: 'save' }).click()
      await expect(page.getByText('a note created by playwright')).toBeVisible()
    })
  })  
})copy
```

The test is defined in its own _describe_ block. Creating a note requires that the user is logged in, which is handled in the _beforeEach_ block.
The test trusts that when creating a new note, there is only one input field on the page, so it searches for it as follows:

```
page.getByRole('textbox')copy
```

If there were more fields, the test would break. Because of this, it could be better to add a _test-id_ to the form input and search for it in the test based on this id.
**Note:** the test will only pass the first time. The reason for this is that its expectation

```
await expect(page.getByText('a note created by playwright')).toBeVisible()copy
```

causes problems when the same note is created in the application more than once. The problem will be solved in the next chapter.
The structure of the tests looks like this:

```
const { test, describe, expect, beforeEach } = require('@playwright/test')

describe('Note app', () => {
  // ....

  test('user can log in', async ({ page }) => {
    await page.getByRole('button', { name: 'login' }).click()
    await page.getByLabel('username').fill('mluukkai')
    await page.getByLabel('password').fill('salainen')
    await page.getByRole('button', { name: 'login' }).click()
    await expect(page.getByText('Matti Luukkainen logged in')).toBeVisible()
  })

  describe('when logged in', () => {
    beforeEach(async ({ page }) => {
      await page.getByRole('button', { name: 'login' }).click()
      await page.getByLabel('username').fill('mluukkai')
      await page.getByLabel('password').fill('salainen')
      await page.getByRole('button', { name: 'login' }).click()
    })

    test('a new note can be created', async ({ page }) => {
      await page.getByRole('button', { name: 'new note' }).click()
      await page.getByRole('textbox').fill('a note created by playwright')
      await page.getByRole('button', { name: 'save' }).click()
      await expect(page.getByText('a note created by playwright')).toBeVisible()
    })
  })
})copy
```

Since we have prevented the tests from running in parallel, Playwright runs the tests in the order they appear in the test code. That is, first the test _user can log in_ , where the user logs into the application, is performed. After this the test _a new note can be created_ gets executed, which also does a log in, in the _beforeEach_ block. Why is this done, isn't the user already logged in thanks to the previous test? No, because the execution of _each_ test starts from the browser's "zero state", all changes made to the browser's state by the previous tests are reset.
### Controlling the state of the database
If the tests need to be able to modify the server's database, the situation immediately becomes more complicated. Ideally, the server's database should be the same each time we run the tests, so our tests can be reliably and easily repeatable.
As with unit and integration tests, with E2E tests it is best to empty the database and possibly format it before the tests are run. The challenge with E2E tests is that they do not have access to the database.
The solution is to create API endpoints for the backend tests. We can empty the database using these endpoints. Let's create a new router for the tests inside the _controllers_ folder, in the _testing.js_ file

```
const router = require('express').Router()
const Note = require('../models/note')
const User = require('../models/user')

router.post('/reset', async (request, response) => {
  await Note.deleteMany({})
  await User.deleteMany({})

  response.status(204).end()
})

module.exports = routercopy
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
describe('Note app', () => {
  beforeEach(async ({ page, request }) => {
    await request.post('http://localhost:3001/api/testing/reset')
    await request.post('http://localhost:3001/api/users', {
      data: {
        name: 'Matti Luukkainen',
        username: 'mluukkai',
        password: 'salainen'
      }
    })

    await page.goto('http://localhost:5173')
  })
  
  test('front page can be opened',  () => {
    // ...
  })

  test('user can login', () => {
    // ...
  })

  describe('when logged in', () => {
    // ...
  })
})copy
```

During initialization, the test makes HTTP requests to the backend with the method _request_.
Unlike before, now the testing of the backend always starts from the same state, i.e. there is one user and no notes in the database.
Let's make a test that checks that the importance of the notes can be changed.
There are a few different approaches to taking the test.
In the following, we first look for a note and click on its button that has text _make not important_. After this, we check that the note contains the button with _make important_.

```
describe('Note app', () => {
  // ...

  describe('when logged in', () => {
    // ...

    describe('and a note exists', () => {      beforeEach(async ({ page }) => {        await page.getByRole('button', { name: 'new note' }).click()        await page.getByRole('textbox').fill('another note by playwright')        await page.getByRole('button', { name: 'save' }).click()      })      test('importance can be changed', async ({ page }) => {        await page.getByRole('button', { name: 'make not important' }).click()        await expect(page.getByText('make important')).toBeVisible()      })    })
  })
})copy
```

The first command first searches for the component where there is the text _another note by playwright_ and inside it the button _make not important_ and clicks on it.
The second command ensures that the text of the same button has changed to _make important_.
The current code for the tests is on _part5-1_.
### Test for failed login
Now let's do a test that ensures that the login attempt fails if the password is wrong.
The first version of the test looks like this:

```
describe('Note app', () => {
  // ...

  test('login fails with wrong password', async ({ page }) => {
    await page.getByRole('button', { name: 'login' }).click()
    await page.getByLabel('username').fill('mluukkai')
    await page.getByLabel('password').fill('wrong')
    await page.getByRole('button', { name: 'login' }).click()

    await expect(page.getByText('wrong credentials')).toBeVisible()
  })

  // ...
})copy
```

The test verifies with the method
The application renders the error message to an element containing the CSS class _error_ :

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

We could refine the test to ensure that the error message is printed exactly in the right place, i.e. in the element containing the CSS class _error_ :

```
test('login fails with wrong password', async ({ page }) => {
  // ...

  const errorDiv = page.locator('.error')  await expect(errorDiv).toContainText('wrong credentials')
})copy
```

So the test uses the _error_ and stores it in a variable. The correctness of the text associated with the component can be verified with the expectation _error_ class selector is _.error_.
It is possible to test the application's CSS styles with matcher

```
test('login fails with wrong password', async ({ page }) => {
  // ...

  const errorDiv = page.locator('.error')
  await expect(errorDiv).toContainText('wrong credentials')
  await expect(errorDiv).toHaveCSS('border-style', 'solid')  await expect(errorDiv).toHaveCSS('color', 'rgb(255, 0, 0)')})copy
```

Colors must be defined to Playwright as
Let's finalize the test so that it also ensures that the application **does not render** the text describing a successful login _'Matti Luukkainen logged in'_ :

```
test('login fails with wrong password', async ({ page }) =>{
  await page.getByRole('button', { name: 'login' }).click()
  await page.getByLabel('username').fill('mluukkai')
  await page.getByLabel('password').fill('wrong')
  await page.getByRole('button', { name: 'login' }).click()

  const errorDiv = page.locator('.error')
  await expect(errorDiv).toContainText('wrong credentials')
  await expect(errorDiv).toHaveCSS('border-style', 'solid')
  await expect(errorDiv).toHaveCSS('color', 'rgb(255, 0, 0)')

  await expect(page.getByText('Matti Luukkainen logged in')).not.toBeVisible()})copy
```

### Running tests one by one
By default, Playwright always runs all tests, and as the number of tests increases, it becomes time-consuming. When developing a new test or debugging a broken one, the test can be defined instead than with the command _test_ , with the command _test.only_ , in which case Playwright will run only that test:

```
describe(() => {
  // this is the only test executed!
  test.only('login fails with wrong password', async ({ page }) => {    // ...
  })

  // this test is skipped...
  test('user can login with correct credentials', async ({ page }) => {
    // ...
  })

  // ...
})copy
```

When the test is ready, _only_ can and **should** be deleted.
Another option to run a single test is to use a command line parameter:

```
npm test -- -g "login fails with wrong password"copy
```

### Helper functions for tests
Our application tests currently look like this:

```
const { test, describe, expect, beforeEach } = require('@playwright/test')

describe('Note app', () => {
  // ...

  test('user can login with correct credentials', async ({ page }) => {
    await page.getByRole('button', { name: 'login' }).click()
    await page.getByLabel('username').fill('mluukkai')
    await page.getByLabel('password').fill('salainen')
    await page.getByRole('button', { name: 'login' }).click()
    await expect(page.getByText('Matti Luukkainen logged in')).toBeVisible()
  })

  test('login fails with wrong password', async ({ page }) =>{
    // ...
  })

  describe('when logged in', () => {
    beforeEach(async ({ page, request }) => {
      await page.getByRole('button', { name: 'login' }).click()
      await page.getByLabel('username').fill('mluukkai')
      await page.getByLabel('password').fill('salainen')
      await page.getByRole('button', { name: 'login' }).click()
    })

    test('a new note can be created', async ({ page }) => {
      // ...
    })
  
    // ...
  })  
})copy
```

First, the login function is tested. After this, another _describe_ block contains a set of tests that assume that the user is logged in, the login is handled inside the initializing _beforeEach_ block.
As already stated earlier, each test is executed starting from the initial state (where the database is cleared and one user is created there), so even though the test is defined after another test in the code, it does not start from the same state where the tests in the code executed earlier have left!
It is also worth striving for having non-repetitive code in tests. Let's isolate the code that handles the login as a helper function, which is placed e.g. in the file _tests/helper.js_ :

```
const loginWith = async (page, username, password)  => {
  await page.getByRole('button', { name: 'login' }).click()
  await page.getByLabel('username').fill(username)
  await page.getByLabel('password').fill(password)
  await page.getByRole('button', { name: 'login' }).click()
}

export { loginWith }copy
```

The tests becomes simpler and clearer:

```
const { test, describe, expect, beforeEach } = require('@playwright/test')
const { loginWith } = require('./helper')
describe('Note app', () => {
  // ...

  test('user can log in', async ({ page }) => {
    await loginWith(page, 'mluukkai', 'salainen')    await expect(page.getByText('Matti Luukkainen logged in')).toBeVisible()
  })

  test('login fails with wrong password', async ({ page }) => {
    await loginWith(page, 'mluukkai', 'wrong')
    const errorDiv = page.locator('.error')
    // ...
  })

  describe('when logged in', () => {
    beforeEach(async ({ page }) => {
      await loginWith(page, 'mluukkai', 'salainen')    })

    // ...
  })
})copy
```

Playwright also offers a
The corresponding repeating code actually also applies to creating a new note. For that, there is a test that creates a note using a form. Also in the _beforeEach_ initialization block of the test that tests changing the importance of the note, a note is created using the form:

```
describe('Note app', function() {
  // ...

  describe('when logged in', () => {
    test('a new note can be created', async ({ page }) => {
      await page.getByRole('button', { name: 'new note' }).click()
      await page.getByRole('textbox').fill('a note created by playwright')
      await page.getByRole('button', { name: 'save' }).click()
      await expect(page.getByText('a note created by playwright')).toBeVisible()
    })
  
    describe('and a note exists', () => {
      beforeEach(async ({ page }) => {
        await page.getByRole('button', { name: 'new note' }).click()
        await page.getByRole('textbox').fill('another note by playwright')
        await page.getByRole('button', { name: 'save' }).click()
      })
  
      test('it can be made important', async ({ page }) => {
        // ...
      })
    })
  })
})copy
```

Creation of a note is also isolated as its helper function. The file _tests/helper.js_ expands as follows:

```
const loginWith = async (page, username, password)  => {
  await page.getByRole('button', { name: 'login' }).click()
  await page.getByLabel('username').fill(username)
  await page.getByLabel('password').fill(password)
  await page.getByRole('button', { name: 'login' }).click()
}

const createNote = async (page, content) => {  await page.getByRole('button', { name: 'new note' }).click()  await page.getByRole('textbox').fill(content)  await page.getByRole('button', { name: 'save' }).click()}
export { loginWith, createNote }copy
```

The tests are simplified as follows:

```
const { test, describe, expect, beforeEach } = require('@playwright/test')
const { createNote, loginWith } = require('./helper')
describe('Note app', () => {
  // ...

  describe('when logged in', () => {
    beforeEach(async ({ page }) => {
      await loginWith(page, 'mluukkai', 'salainen')
    })

    test('a new note can be created', async ({ page }) => {
      await createNote(page, 'a note created by playwright')      await expect(page.getByText('a note created by playwright')).toBeVisible()
    })

    describe('and a note exists', () => {
      beforeEach(async ({ page }) => {
        await createNote(page, 'another note by playwright')      })
  
      test('importance can be changed', async ({ page }) => {
        await page.getByRole('button', { name: 'make not important' }).click()
        await expect(page.getByText('make important')).toBeVisible()
      })
    })
  })
})copy
```

There is one more annoying feature in our tests. The frontend address _http:localhost:5173_ and the backend address _http:localhost:3001_ are hardcoded for tests. Of these, the address of the backend is actually useless, because a proxy has been defined in the Vite configuration of the frontend, which forwards all requests made by the frontend to the address _http:localhost:5173/api_ to the backend:

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
We can now define the _baseUrl_ for the application in the tests configuration file _playwright.config.js_ :

```
export default defineConfig({
  // ...
  use: {
    baseURL: 'http://localhost:5173',
    // ...
  },
  // ...
})copy
```

All the commands in the tests that use the application url, e.g.

```
await page.goto('http://localhost:5173')
await page.post('http://localhost:5173/api/testing/reset')copy
```

can now be transformed into:

```
await page.goto('/')
await page.post('/api/testing/reset')copy
```

The current code for the tests is on _part5-2_.
### Note importance change revisited
Let's take a look at the test we did earlier, which verifies that it is possible to change the importance of a note.
Let's change the initialization block of the test so that it creates two notes instead of one:

```
describe('when logged in', () => {
  // ...
  describe('and several notes exists', () => {    beforeEach(async ({ page }) => {
      await createNote(page, 'first note')      await createNote(page, 'second note')    })

    test('one of those can be made nonimportant', async ({ page }) => {
      const otherNoteElement = page.getByText('first note')

      await otherNoteElement
        .getByRole('button', { name: 'make not important' }).click()
      await expect(otherNoteElement.getByText('make important')).toBeVisible()
    })
  })
})copy
```

The test first searches for the element corresponding to the first created note using the method _page.getByText_ and stores it in a variable. After this, a button with the text _make not important_ is searched inside the element and the button is pressed. Finally, the test verifies that the button's text has changed to _make important_.
The test could also have been written without the auxiliary variable:

```
test('one of those can be made nonimportant', async ({ page }) => {
  page.getByText('first note')
    .getByRole('button', { name: 'make not important' }).click()

  await expect(page.getByText('first note').getByText('make important'))
    .toBeVisible()
})copy
```

Let's change the _Note_ component so that the note text is rendered inside a _span_ element

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

Tests break! The reason for the problem is that the command _page.getByText('first note')_ now returns a _span_ element containing only text, and the button is outside of it.
One way to fix the problem is as follows:

```
test('one of those can be made nonimportant', async ({ page }) => {
  const otherNoteText = page.getByText('first note')  const otherNoteElement = otherNoteText.locator('..')
  await otherNoteElement.getByRole('button', { name: 'make not important' }).click()
  await expect(otherNoteElement.getByText('make important')).toBeVisible()
})copy
```

The first line now looks for the _span_ element containing the text associated with the first created note. In the second line, the function _locator_ is used and _.._ is given as an argument, which retrieves the element's parent element. The locator function is very flexible, and we take advantage of the fact that accepts
Of course, the test can also be written using only one auxiliary variable:

```
test('one of those can be made nonimportant', async ({ page }) => {
  const secondNoteElement = page.getByText('second note').locator('..')
  await secondNoteElement.getByRole('button', { name: 'make not important' }).click()
  await expect(secondNoteElement.getByText('make important')).toBeVisible()
})copy
```

Let's change the test so that three notes are created, the importance is changed in the second created note:

```
describe('when logged in', () => {
  beforeEach(async ({ page }) => {
    await loginWith(page, 'mluukkai', 'salainen')
  })

  test('a new note can be created', async ({ page }) => {
    await createNote(page, 'a note created by playwright', true)
    await expect(page.getByText('a note created by playwright')).toBeVisible()
  })

  describe('and several notes exists', () => {
    beforeEach(async ({ page }) => {
      await createNote(page, 'first note')
      await createNote(page, 'second note')
      await createNote(page, 'third note')    })

    test('one of those can be made nonimportant', async ({ page }) => {
      const otherNoteText = page.getByText('second note')      const otherNoteElement = otherNoteText.locator('..')
    
      await otherNoteElement.getByRole('button', { name: 'make not important' }).click()
      await expect(otherNoteElement.getByText('make important')).toBeVisible()
    })
  })
}) copy
```

For some reason the test starts working unreliably, sometimes it passes and sometimes it doesn't. It's time to roll up your sleeves and learn how to debug tests.
### Test development and debugging
If, and when the tests don't pass and you suspect that the fault is in the tests instead of in the code, you should run the tests in
The following command runs the problematic test in debug mode:

```
npm test -- -g'one of those can be made nonimportant' --debugcopy
```

Playwright-inspector shows the progress of the tests step by step. The arrow-dot button at the top takes the tests one step further. The elements found by the locators and the interaction with the browser are visualized in the browser:
![playwright inspector highlighting element found by the selected locator in the application](../assets/d326ca7dcf4db933.png)
By default, debug steps through the test command by command. If it is a complex test, it can be quite a burden to step through the test to the point of interest. This can be avoided by using the command _await page.pause()_ :

```
describe('Note app', () => {
  beforeEach(async ({ page, request }) => {
    // ...
  })

  describe('when logged in', () => {
    beforeEach(async ({ page }) => {
      // ...
    })

    describe('and several notes exists', () => {
      beforeEach(async ({ page }) => {
        await createNote(page, 'first note')
        await createNote(page, 'second note')
        await createNote(page, 'third note')
      })
  
      test('one of those can be made nonimportant', async ({ page }) => {
        await page.pause()        const otherNoteText = page.getByText('second note')
        const otherNoteElement = otherNoteText.locator('..')
      
        await otherNoteElement.getByRole('button', { name: 'make not important' }).click()
        await expect(otherNoteElement.getByText('make important')).toBeVisible()
      })
    })
  })
})copy
```

Now in the test you can go to _page.pause()_ in one step, by pressing the green arrow symbol in the inspector.
When we now run the test and jump to the _page.pause()_ command, we find an interesting fact:
![playwright inspector showing the state of the application at page.pause](../assets/cd930e0a034345a1.png)
It seems that the browser _does not render_ all the notes created in the block _beforeEach_. What is the problem?
The reason for the problem is that when the test creates one note, it starts creating the next one even before the server has responded, and the added note is rendered on the screen. This in turn can cause some notes to be lost (in the picture, this happened to the second note created), since the browser is re-rendered when the server responds, based on the state of the notes at the start of that insert operation.
The problem can be solved by "slowing down" the insert operations by using the

```
const createNote = async (page, content) => {
  await page.getByRole('button', { name: 'new note' }).click()
  await page.getByRole('textbox').fill(content)
  await page.getByRole('button', { name: 'save' }).click()
  await page.getByText(content).waitFor()}copy
```

Instead of, or alongside debugging mode, running tests in UI mode can be useful. As already mentioned, tests are started in UI mode as follows:

```
npm run test -- --uicopy
```

Almost the same as UI mode is use of the Playwright's

```
npm run test -- --trace oncopy
```

If necessary, Trace can be viewed with the command

```
npx playwright show-reportcopy
```

or with the npm script we defined _npm run test:report_
Trace looks practically the same as running tests in UI mode.
UI mode and Trace Viewer also offer the possibility of assisted search for locators. This is done by pressing the double circle on the left side of the lower bar, and then by clicking on the desired user interface element. Playwright displays the element locator:
![playwright's trace viewer with red arrows pointing at the locator assisted search location and to the element selected with it showing a suggested locator for the element](../assets/8924ebee7fa8a54b.png)
Playwright suggests the following as the locator for the third note

```
page.locator('li').filter({ hasText: 'third note' }).getByRole('button')copy
```

The method _li_ , i.e. we search for all li elements on the page, of which there are three in total. After this, using the _third note_ and the button element inside it is taken using the
The locator generated by Playwright is somewhat different from the locator used by our tests, which was

```
page.getByText('first note').locator('..').getByRole('button', { name: 'make not important' })copy
```

Which of the locators is better is probably a matter of taste.
Playwright also includes a

```
npx playwright codegen http://localhost:5173/copy
```

When the _Record_ mode is on, the test generator "records" the user's interaction in the Playwright inspector, from where it is possible to copy the locators and actions to the tests:
![playwright's record mode enabled with its output in the inspector after user interaction](../assets/dc2dab6363e30706.png)
Instead of the command line, Playwright can also be used via the
To avoid problem situations and increase understanding, it is definitely worth browsing Playwright's high-quality

- the section about
- section
- the section about


In-depth details can be found in the
The final version of the tests is in full on _part5-3_.
The final version of the frontend code is in its entirety on _part5-9_.
### Exercises 5.17.-5.23
In the last exercises of this part, let's do some E2E tests for the blog application. The material above should be enough to do most of the exercises. However, you should definitely read Playwright's
#### 5.17: Blog List End To End Testing, step 1
Create a new npm project for tests and configure Playwright there.
Make a test to ensure that the application displays the login form by default.
The body of the test should be as follows:

```
const { test, expect, beforeEach, describe } = require('@playwright/test')

describe('Blog app', () => {
  beforeEach(async ({ page }) => {
    await page.goto('http://localhost:5173')
  })

  test('Login form is shown', async ({ page }) => {
    // ...
  })
})copy
```

#### 5.18: Blog List End To End Testing, step 2
Do the tests for login. Test both successful and failed login. For tests, create a user in the _beforeEach_ block.
The body of the tests expands as follows

```
const { test, expect, beforeEach, describe } = require('@playwright/test')

describe('Blog app', () => {
  beforeEach(async ({ page, request }) => {
    // empty the db here
    // create a user for the backend here
    // ...
  })

  test('Login form is shown', async ({ page }) => {
    // ...
  })

  describe('Login', () => {
    test('succeeds with correct credentials', async ({ page }) => {
      // ...
    })

    test('fails with wrong credentials', async ({ page }) => {
      // ...
    })
  })
})copy
```

The _beforeEach_ block must empty the database using, for example, the reset method we used in the [material](../part5/01-end-to-end-testing-playwright-controlling-the-state-of-the-database.md).
#### 5.19: Blog List End To End Testing, step 3
Create a test that verifies that a logged in user can create a blog. The body of the test may look like the following

```
describe('When logged in', () => {
  beforeEach(async ({ page }) => {
    // ...
  })

  test('a new blog can be created', async ({ page }) => {
    // ...
  })
})copy
```

The test should ensure that the created blog is visible in the list of blogs.
#### 5.20: Blog List End To End Testing, step 4
Do a test that makes sure the blog can be liked.
#### 5.21: Blog List End To End Testing, step 5
Make a test that ensures that the user who added the blog can delete the blog. If you use the _window.confirm_ dialog in the delete operation, you may have to Google how to use the dialog in the Playwright tests.
#### 5.22: Blog List End To End Testing, step 6
Make a test that ensures that only the user who added the blog sees the blog's delete button.
#### 5.23: Blog List End To End Testing, step 7
Do a test that ensures that the blogs are arranged in the order according to the likes, the blog with the most likes first.
_This task is significantly more challenging than the previous ones._
This was the last task of the section and it's time to push the code to GitHub and mark the completed tasks in the
[Part 5c **Previous part**](../part5/01-testing-react-apps.md)[Part 5e **Next part**](../part5/01-end-to-end-testing-cypress.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)
