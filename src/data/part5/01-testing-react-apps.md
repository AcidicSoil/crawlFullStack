---{
  "title": "Testing React apps",
  "source_url": "https://fullstackopen.com/en/part5/testing_react_apps",
  "crawl_timestamp": "2025-10-04T19:16:46Z",
  "checksum": "d81e18b213e894ec53ee2f81a1ca87a9fa9d2969b83eeeaaac7d978f86a4c3b1"
}
---[Skip to content](../part5/01-testing-react-apps-course-main-content.md)
[{() => fs}](https://fullstackopen.com/en/)
  * [About course](../about/01-about.md)
  * [Course contents](../#course-contents/01-course-contents.md)
  * [FAQ](../faq/01-faq.md)
  * [Partners](../companies/01-companies.md)
  * [Challenge](../challenge/01-challenge.md)
[Search from the material](../search/01-search.md)Toggle dark theme
Select languageSuomi English 中文 Español Français Português(BR) 

[Fullstack](../#course-contents/01-course-contents.md)
[Part 5](../part5/01-part5.md)
Testing React apps
[a Login in frontend](../part5/01-login-in-frontend.md)[b props.children and proptypes](../part5/01-props-children-and-proptypes.md)
c Testing React apps
  * [Rendering the component for tests](../part5/01-testing-react-apps-rendering-the-component-for-tests.md)
  * [Test file location](../part5/01-testing-react-apps-test-file-location.md)
  * [Searching for content in a component](../part5/01-testing-react-apps-searching-for-content-in-a-component.md)
  * [Debugging tests](../part5/01-testing-react-apps-debugging-tests.md)
  * [Clicking buttons in tests](../part5/01-testing-react-apps-clicking-buttons-in-tests.md)
  * [Tests for the Togglable component](../part5/01-testing-react-apps-tests-for-the-togglable-component.md)
  * [Testing the forms](../part5/01-testing-react-apps-testing-the-forms.md)
  * [About finding the elements](../part5/01-testing-react-apps-about-finding-the-elements.md)
  * [Test coverage](../part5/01-testing-react-apps-test-coverage.md)
  * [Exercises 5.13.-5.16.](../part5/01-testing-react-apps-exercises-5-13-5-16.md)
  * [Frontend integration tests](../part5/01-testing-react-apps-frontend-integration-tests.md)
  * [Snapshot testing](../part5/01-testing-react-apps-snapshot-testing.md)


[d End to end testing: Playwright](../part5/01-end-to-end-testing-playwright.md)[e End to end testing: Cypress](../part5/01-end-to-end-testing-cypress.md)
c
# Testing React apps
There are many different ways of testing React applications. Let's take a look at them next.
The course previously used the 
Let's start by installing Vitest and the 
```
npm install --save-dev vitest jsdomcopy
```

In addition to Vitest, we also need another testing library that will help us render components for testing purposes. The current best option for this is 
Let's install the libraries with the command:
```
npm install --save-dev @testing-library/react @testing-library/jest-domcopy
```

Before we can do the first test, we need some configurations.
We add a script to the _package.json_ file to run the tests:
```
{
  "scripts": {
    // ...
    "test": "vitest run"
  }
  // ...
}copy
```

Let's create a file _testSetup.js_ in the project root with the following content
```
import { afterEach } from 'vitest'
import { cleanup } from '@testing-library/react'
import '@testing-library/jest-dom/vitest'

afterEach(() => {
  cleanup()
})copy
```

Now, after each test, the function _cleanup_ is executed to reset jsdom, which is simulating the browser.
Expand the _vite.config.js_ file as follows
```
export default defineConfig({
  // ...
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './testSetup.js', 
  }
})copy
```

With _globals: true_ , there is no need to import keywords such as _describe_ , _test_ and _expect_ into the tests.
Let's first write tests for the component that is responsible for rendering a note:
```
const Note = ({ note, toggleImportance }) => {
  const label = note.important
    ? 'make not important'
    : 'make important'

  return (
    <li className='note'>      {note.content}
      <button onClick={toggleImportance}>{label}</button>
    </li>
  )
}copy
```

Notice that the _li_ element has the value _note_ for the 
### Rendering the component for tests
We will write our test in the _src/components/Note.test.jsx_ file, which is in the same directory as the component itself.
The first test verifies that the component renders the contents of the note:
```
import { render, screen } from '@testing-library/react'
import Note from './Note'

test('renders content', () => {
  const note = {
    content: 'Component testing is done with react-testing-library',
    important: true
  }

  render(<Note note={note} />)

  const element = screen.getByText('Component testing is done with react-testing-library')
  expect(element).toBeDefined()
})copy
```

After the initial configuration, the test renders the component with the 
```
render(<Note note={note} />)copy
```

Normally React components are rendered to the 
We can use the object 
```
  const element = screen.getByText('Component testing is done with react-testing-library')
  expect(element).toBeDefined()copy
```

The existence of an element is checked using Vitest's _element_ argument of expect exists.
Run the test with command _npm test_ :
```
$ npm test

> notes-frontend@0.0.0 test
> vitest run


 RUN  v3.2.3 /home/vejolkko/repot/fullstack-examples/notes-frontend

 ✓ src/components/Note.test.jsx (1 test) 19ms
   ✓ renders content 18ms

 Test Files  1 passed (1)
      Tests  1 passed (1)
   Start at  14:31:54
   Duration  874ms (transform 51ms, setup 169ms, collect 19ms, tests 19ms, environment 454ms, prepare 87ms)copy
```

Eslint complains about the keywords _test_ and _expect_ in the tests. The problem can be solved by adding the following configuration to the _eslint.config.js_ file:
```
// ...

export default [
  // ...
  {    files: ['**/*.test.{js,jsx}'],    languageOptions: {      globals: {        ...globals.vitest      }    }  }]copy
```

This is how ESLint is informed that Vitest keywords are globally available in test files.
### Test file location
In React there are (at least) 
The other convention is to store the test files "normally" in a separate _test_ directory. Whichever convention we choose, it is almost guaranteed to be wrong according to someone's opinion.
I do not like this way of storing tests and application code in the same directory. However, we will follow this approach for now, as it is the most common practice in small projects.
### Searching for content in a component
The react-testing-library package offers many different ways of investigating the content of the component being tested. In reality, the _expect_ in our test is not needed at all:
```
import { render, screen } from '@testing-library/react'
import Note from './Note'

test('renders content', () => {
  const note = {
    content: 'Component testing is done with react-testing-library',
    important: true
  }

  render(<Note note={note} />)

  const element = screen.getByText('Component testing is done with react-testing-library')

  expect(element).toBeDefined()})copy
```

Test fails if _getByText_ does not find the element it is looking for.
The _getByText_ command, by default, searches for an element that contains only the **text provided as a parameter** and nothing else. Let us assume that a component would render text to an HTML element as follows:
```
const Note = ({ note, toggleImportance }) => {
  const label = note.important
    ? 'make not important' : 'make important'

  return (
    <li className='note'>
      Your awesome note: {note.content}      <button onClick={toggleImportance}>{label}</button>
    </li>
  )
}

export default Notecopy
```

The _getByText_ method that the test uses does _not_ find the element:
```
test('renders content', () => {
  const note = {
    content: 'Does not work anymore :(',
    important: true
  }

  render(<Note note={note} />)

  const element = screen.getByText('Does not work anymore :(')

  expect(element).toBeDefined()
})copy
```

If we want to look for an element that _contains_ the text, we could use an extra option:
```
const element = screen.getByText(
  'Does not work anymore :(', { exact: false }
)copy
```

or we could use the _findByText_ method:
```
const element = await screen.findByText('Does not work anymore :(')copy
```

It is important to notice that, unlike the other _ByText_ methods, _findByText_ returns a promise!
There are situations where yet another form of the _queryByText_ method is useful. The method returns the element but _it does not cause an exception_ if it is not found.
We could eg. use the method to ensure that something _is not rendered_ to the component:
```
test('does not render this', () => {
  const note = {
    content: 'This is a reminder',
    important: true
  }

  render(<Note note={note} />)

  const element = screen.queryByText('do not want this thing to be rendered')
  expect(element).toBeNull()
})copy
```

Other methods also exist, such as 
We could also use 
```
import { render, screen } from '@testing-library/react'
import Note from './Note'

test('renders content', () => {
  const note = {
    content: 'Component testing is done with react-testing-library',
    important: true
  }

  const { container } = render(<Note note={note} />)
  const div = container.querySelector('.note')  expect(div).toHaveTextContent(    'Component testing is done with react-testing-library'  )})copy
```

It is, however, recommended to search for elements primarily using methods other than the _container_ object and CSS selectors. CSS attributes can often be changed without affecting the application's functionality, and users are not aware of them. It is better to search for elements based on properties visible to the user, for example, by using the _getByText_ method. This way, the tests better simulate the actual nature of the component and how a user would find the element on the screen.
### Debugging tests
We typically run into many different kinds of problems when writing our tests.
Object _screen_ has method 
```
import { render, screen } from '@testing-library/react'
import Note from './Note'

test('renders content', () => {
  const note = {
    content: 'Component testing is done with react-testing-library',
    important: true
  }

  render(<Note note={note} />)

  screen.debug()
  // ...

})copy
```

the HTML gets printed to the console:
```
console.log
  <body>
    <div>
      <li
        class="note"
      >
        Component testing is done with react-testing-library
        <button>
          make not important
        </button>
      </li>
    </div>
  </body>copy
```

It is also possible to use the same method to print a wanted element to console:
```
import { render, screen } from '@testing-library/react'
import Note from './Note'

test('renders content', () => {
  const note = {
    content: 'Component testing is done with react-testing-library',
    important: true
  }

  render(<Note note={note} />)

  const element = screen.getByText('Component testing is done with react-testing-library')

  screen.debug(element)
  expect(element).toBeDefined()
})copy
```

Now the HTML of the wanted element gets printed:
```
  <li
    class="note"
  >
    Component testing is done with react-testing-library
    <button>
      make not important
    </button>
  </li>copy
```

### Clicking buttons in tests
In addition to displaying content, the _Note_ component also makes sure that when the button associated with the note is pressed, the _toggleImportance_ event handler function gets called.
Let us install a library 
```
npm install --save-dev @testing-library/user-eventcopy
```

Testing this functionality can be accomplished like this:
```
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'import Note from './Note'

// ...

test('clicking the button calls event handler once', async () => {
  const note = {
    content: 'Component testing is done with react-testing-library',
    important: true
  }
  
  const mockHandler = vi.fn()
  render(
    <Note note={note} toggleImportance={mockHandler} />  )

  const user = userEvent.setup()  const button = screen.getByText('make not important')  await user.click(button)
  expect(mockHandler.mock.calls).toHaveLength(1)})copy
```

There are a few interesting things related to this test. The event handler is a 
```
const mockHandler = vi.fn()copy
```

A 
```
const user = userEvent.setup()copy
```

The test finds the button _based on the text_ from the rendered component and clicks the element:
```
const button = screen.getByText('make not important')
await user.click(button)copy
```

Clicking happens with the method 
The expectation of the test uses _mock function_ has been called exactly once:
```
expect(mockHandler.mock.calls).toHaveLength(1)copy
```

The calls to the mock function are saved to the array 
In our example, the mock function is a perfect choice since it can be easily used for verifying that the method gets called exactly once.
### Tests for the _Togglable_ component
Let's write a few tests for the _Togglable_ component. The tests are shown below:
```
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import Togglable from './Togglable'

describe('<Togglable />', () => {
  beforeEach(() => {
    render(
      <Togglable buttonLabel="show...">
        <div>togglable content</div>
      </Togglable>
    )
  })

  test('renders its children', () => {
    screen.getByText('togglable content')
  })

  test('at start the children are not displayed', () => {
    const element = screen.getByText('togglable content')
    expect(element).not.toBeVisible()
  })

  test('after clicking the button, children are displayed', async () => {
    const user = userEvent.setup()
    const button = screen.getByText('show...')
    await user.click(button)

    const element = screen.getByText('togglable content')
    expect(element).toBeVisible()
  })copy
```

The _beforeEach_ function gets called before each test, which then renders the _Togglable_ component.
The first test verifies that the _Togglable_ component renders its child component
```
<div>
  togglable content
</div>copy
```

The remaining tests use the _toBeVisible_ method to verify that the child component of the _Togglable_ component is not visible initially, i.e. that the style of the _div_ element contains _{ display: 'none' }_. Another test verifies that when the button is pressed the component is visible, meaning that the style for hiding it _is no longer_ assigned to the component.
Let's also add a test that can be used to verify that the visible content can be hidden by clicking the second button of the component:
```
describe('<Togglable />', () => {

  // ...

  test('toggled content can be closed', async () => {
    const user = userEvent.setup()
    const button = screen.getByText('show...')
    await user.click(button)

    const closeButton = screen.getByText('cancel')
    await user.click(closeButton)

    const element = screen.getByText('togglable content')
    expect(element).not.toBeVisible()
  })
})copy
```

### Testing the forms
We already used the _click_ function of the 
```
const user = userEvent.setup()
const button = screen.getByText('show...')
await user.click(button)copy
```

We can also simulate text input with _userEvent_.
Let's make a test for the _NoteForm_ component. The code of the component is as follows.
```
import { useState } from 'react'

const NoteForm = ({ createNote }) => {
  const [newNote, setNewNote] = useState('')

  const addNote = event => {
    event.preventDefault()
    createNote({
      content: newNote,
      important: true
    })

    setNewNote('')
  }

  return (
    <div>
      <h2>Create a new note</h2>

      <form onSubmit={addNote}>
        <input
          value={newNote}
          onChange={event => setNewNote(event.target.value)}
        />
        <button type="submit">save</button>
      </form>
    </div>
  )
}

export default NoteFormcopy
```

The form works by calling the function received as props _createNote_ , with the details of the new note.
The test is as follows:
```
import { render, screen } from '@testing-library/react'
import NoteForm from './NoteForm'
import userEvent from '@testing-library/user-event'

test('<NoteForm /> updates parent state and calls onSubmit', async () => {
  const createNote = vi.fn()
  const user = userEvent.setup()

  render(<NoteForm createNote={createNote} />)

  const input = screen.getByRole('textbox')
  const sendButton = screen.getByText('save')

  await user.type(input, 'testing a form...')
  await user.click(sendButton)

  expect(createNote.mock.calls).toHaveLength(1)
  expect(createNote.mock.calls[0][0].content).toBe('testing a form...')
})copy
```

Tests get access to the input field using the function 
The method 
The first test expectation ensures that submitting the form calls the _createNote_ method. The second expectation checks that the event handler is called with the right parameters - that a note with the correct content is created when the form is filled.
It's worth noting that the good old _console.log_ works as usual in the tests. For example, if you want to see what the calls stored by the mock-object look like, you can do the following
```
test('<NoteForm /> updates parent state and calls onSubmit', async() => {
  const user = userEvent.setup()
  const createNote = vi.fn()

  render(<NoteForm createNote={createNote} />)

  const input = screen.getByRole('textbox')
  const sendButton = screen.getByText('save')

  await user.type(input, 'testing a form...')
  await user.click(sendButton)

  console.log(createNote.mock.calls)})copy
```

In the middle of running the tests, the following is printed in the console:
```
[ [ { content: 'testing a form...', important: true } ] ]copy
```

### About finding the elements
Let us assume that the form has two input fields
```
const NoteForm = ({ createNote }) => {
  // ...

  return (
    <div>
      <h2>Create a new note</h2>

      <form onSubmit={addNote}>
        <input
          value={newNote}
          onChange={event => setNewNote(event.target.value)}
        />
        <input          value={...}          onChange={...}        />        <button type="submit">save</button>
      </form>
    </div>
  )
}copy
```

Now the approach that our test uses to find the input field
```
const input = screen.getByRole('textbox')copy
```

would cause an error:
![node error that shows two elements with textbox since we use getByRole](../assets/7c380b054e574fbe.png)
The error message suggests using _getAllByRole_. The test could be fixed as follows:
```
const inputs = screen.getAllByRole('textbox')

await user.type(inputs[0], 'testing a form...')copy
```

Method _getAllByRole_ now returns an array and the right input field is the first element of the array. However, this approach is a bit suspicious since it relies on the order of the input fields.
If an _label_ were defined for the input field, the input field could be located using it with the getByLabelText method. For example, if we added a label to the input field:
```
  // ...
  <label>    content    <input
      value={newNote}
      onChange={event => setNewNote(event.target.value)}
    />
  </label>  // ...copy
```

The test could locate the input field as follows:
```
test('<NoteForm /> updates parent state and calls onSubmit', () => {
  const createNote = vi.fn()

  render(<NoteForm createNote={createNote} />) 

  const input = screen.getByLabelText('content')  const sendButton = screen.getByText('save')

  userEvent.type(input, 'testing a form...' )
  userEvent.click(sendButton)

  expect(createNote.mock.calls).toHaveLength(1)
  expect(createNote.mock.calls[0][0].content).toBe('testing a form...' )
})copy
```

Quite often input fields have a _placeholder_ text that hints user what kind of input is expected. Let us add a placeholder to our form:
```
const NoteForm = ({ createNote }) => {
  // ...

  return (
    <div>
      <h2>Create a new note</h2>

      <form onSubmit={addNote}>
        <input
          value={newNote}
          onChange={event => setNewNote(event.target.value)}
          placeholder='write note content here'        />
        <input
          value={...}
          onChange={...}
        />    
        <button type="submit">save</button>
      </form>
    </div>
  )
}copy
```

Now finding the right input field is easy with the method 
```
test('<NoteForm /> updates parent state and calls onSubmit', () => {
  const createNote = vi.fn()

  render(<NoteForm createNote={createNote} />) 

  const input = screen.getByPlaceholderText('write note content here')  const sendButton = screen.getByText('save')

  userEvent.type(input, 'testing a form...')
  userEvent.click(sendButton)

  expect(createNote.mock.calls).toHaveLength(1)
  expect(createNote.mock.calls[0][0].content).toBe('testing a form...')
})copy
```

Sometimes, finding the correct element using the methods described above can be challenging. In such cases, an alternative is the method _querySelector_ of the _container_ object, which is returned by _render_ , as was mentioned [earlier in this part](../part5/01-testing-react-apps-searching-for-content-in-a-component.md). Any CSS selector can be used with this method for searching elements in tests.
Consider eg. that we would define a unique _id_ to the input field:
```
const NoteForm = ({ createNote }) => {
  // ...

  return (
    <div>
      <h2>Create a new note</h2>

      <form onSubmit={addNote}>
        <input
          value={newNote}
          onChange={event => setNewNote(event.target.value)}
          id='note-input'        />
        <input
          value={...}
          onChange={...}
        />    
        <button type="submit">save</button>
      </form>
    </div>
  )
}copy
```

The input element could now be found in the test as follows:
```
const { container } = render(<NoteForm createNote={createNote} />)

const input = container.querySelector('#note-input')copy
```

However, we shall stick to the approach of using _getByPlaceholderText_ in the test.
### Test coverage
We can easily find out the 
```
npm test -- --coveragecopy
```

The first time you run the command, Vitest will ask you if you want to install the required library _@vitest/coverage-v8_. Install it, and run the command again:
![terminal output of test coverage](../assets/a2b4192e54366219.png)
A HTML report will be generated to the _coverage_ directory. The report will tell us the lines of untested code in each component:
![HTML report of the test coverage](../assets/ba6f58c368aa7f28.png)
Let's add the directory _coverage/_ to the _.gitignore_ file to exclude its contents from version control:
```
//...

coverage/copy
```

You can find the code for our current application in its entirety in the _part5-8_ branch of 
### Exercises 5.13.-5.16.
#### 5.13: Blog List Tests, step 1
Make a test, which checks that the component displaying a blog renders the blog's title and author, but does not render its URL or number of likes by default.
Add CSS classes to the component to help the testing as necessary.
#### 5.14: Blog List Tests, step 2
Make a test, which checks that the blog's URL and number of likes are shown when the button controlling the shown details has been clicked.
#### 5.15: Blog List Tests, step 3
Make a test, which ensures that if the _like_ button is clicked twice, the event handler the component received as props is called twice.
#### 5.16: Blog List Tests, step 4
Make a test for the new blog form. The test should check, that the form calls the event handler it received as props with the right details when a new blog is created.
### Frontend integration tests
In the previous part of the course material, we wrote integration tests for the backend that tested its logic and connected the database through the API provided by the backend. When writing these tests, we made the conscious decision not to write unit tests, as the code for that backend is fairly simple, and it is likely that bugs in our application occur in more complicated scenarios than unit tests are well suited for.
So far all of our tests for the frontend have been unit tests that have validated the correct functioning of individual components. Unit testing is useful at times, but even a comprehensive suite of unit tests is not enough to validate that the application works as a whole.
We could also make integration tests for the frontend. Integration testing tests the collaboration of multiple components. It is considerably more difficult than unit testing, as we would have to for example mock data from the server. We chose to concentrate on making end-to-end tests to test the whole application. We will work on the end-to-end tests in the last chapter of this part.
### Snapshot testing
Vitest offers a completely different alternative to "traditional" testing called 
The fundamental principle is to compare the HTML code defined by the component after it has changed to the HTML code that existed before it was changed.
If the snapshot notices some change in the HTML defined by the component, then either it is new functionality or a "bug" caused by accident. Snapshot tests notify the developer if the HTML code of the component changes. The developer has to tell Vitest if the change was desired or undesired. If the change to the HTML code is unexpected, it strongly implies a bug, and the developer can become aware of these potential issues easily thanks to snapshot testing.
[ Part 5b **Previous part** ](../part5/01-props-children-and-proptypes.md)[ Part 5d **Next part** ](../part5/01-end-to-end-testing-playwright.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)