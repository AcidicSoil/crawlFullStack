---{
  "title": "Fundamentals of Web apps",
  "source_url": "https://fullstackopen.com/en/part0/fundamentals_of_web_apps",
  "crawl_timestamp": "2025-10-04T19:15:27Z",
  "checksum": "6f1d7c98ebb60d3c0673fa9f25d0fceef049e52ca8c2ead25dfb51750e31a710"
}
---[Skip to content](../part0/01-fundamentals-of-web-apps-course-main-content.md)
[{() => fs}](https://fullstackopen.com/en/)
  * [About course](../about/01-about.md)
  * [Course contents](../#course-contents/01-course-contents.md)
  * [FAQ](../faq/01-faq.md)
  * [Partners](../companies/01-companies.md)
  * [Challenge](../challenge/01-challenge.md)
[Search from the material](../search/01-search.md)Toggle dark theme
Select languageSuomi English 中文 Español Français Português(BR) 

[Fullstack](../#course-contents/01-course-contents.md)
[Part 0](../part0/01-part0.md)
Fundamentals of Web apps
[a General info](../part0/01-general-info.md)
b Fundamentals of Web apps
  * [HTTP GET](../part0/01-fundamentals-of-web-apps-http-get.md)
  * [Traditional web applications](../part0/01-fundamentals-of-web-apps-traditional-web-applications.md)
  * [Running application logic in the browser](../part0/01-fundamentals-of-web-apps-running-application-logic-in-the-browser.md)
  * [Event handlers and Callback functions](../part0/01-fundamentals-of-web-apps-event-handlers-and-callback-functions.md)
  * [Document Object Model or DOM](../part0/01-fundamentals-of-web-apps-document-object-model-or-dom.md)
  * [Manipulating the document object from console](../part0/01-fundamentals-of-web-apps-manipulating-the-document-object-from-console.md)
  * [CSS](../part0/01-fundamentals-of-web-apps-css.md)
  * [Loading a page containing JavaScript - review](../part0/01-fundamentals-of-web-apps-loading-a-page-containing-java-script-review.md)
  * [Forms and HTTP POST](../part0/01-fundamentals-of-web-apps-forms-and-http-post.md)
  * [AJAX](../part0/01-fundamentals-of-web-apps-ajax.md)
  * [Single page app](../part0/01-fundamentals-of-web-apps-single-page-app.md)
  * [JavaScript-libraries](../part0/01-fundamentals-of-web-apps-java-script-libraries.md)
  * [Full-stack web development](../part0/01-fundamentals-of-web-apps-full-stack-web-development.md)
  * [JavaScript fatigue](../part0/01-fundamentals-of-web-apps-java-script-fatigue.md)
  * [Exercises 0.1.-0.6.](../part0/01-fundamentals-of-web-apps-exercises-0-1-0-6.md)


b
# Fundamentals of Web apps
Before we start programming, we will go through some principles of web development by examining an example application at 
The application exists only to demonstrate some basic concepts of the course, and is, by no means, an example of _how_ a modern web application should be made. On the contrary, it demonstrates some old techniques of web development, which could even be considered _bad practices_ nowadays.
Code will conform to contemporary best practices from [part 1](../part1/01-part1.md) onwards.
Open the 
The course material was done with and adapted for the Chrome browser.
**The 1st rule of web development** : Always keep the Developer Console open on your web browser. On macOS, open the console by pressing _fn_ -_F12_ or _option-cmd-i_ simultaneously. On Windows or Linux, open the console by pressing _Fn_ -_F12_ or _ctrl-shift-i_ simultaneously. The console can also be opened via the 
Remember to _always_ keep the Developer Console open when developing web applications.
The console looks like this:
![A screenshot of the developer tools open in a browser](../assets/23f7eafffaef02db.png)
Make sure that the _Network_ tab is open, and check the _Disable cache_ option as shown. _Preserve log_ can also be useful (it saves the logs printed by the application when the page is reloaded) as well as "Hide extension URLs"(hides requests of any extensions installed in the browser, not shown in the picture above).
**NB:** The most important tab is the _Console_ tab. However, in this introduction, we will be using the _Network_ tab quite a bit.
### HTTP GET
The server and the web browser communicate with each other using the _Network_ tab shows how the browser and the server communicate.
When you reload the page (To refresh a webpage, on windows, press the _Fn_ -_F5_ keys. On macOS, press _command_ -_R_. Or press the ↻ symbol on your browser), the console will show that two events have happened:
  * The browser has fetched the contents of the page _studies.cs.helsinki.fi/exampleapp_ from the server
  * And has downloaded the image _kuva.png_

![Screenshot of the developer console showing these two events](../assets/56c067065cdbe67a.png)
On a small screen, you might have to widen the console window to see these.
Clicking the first event reveals more information on what's happening:
![Detailed view of a single event](../assets/176f09fd77657354.png)
The upper part, _General_ , shows that the browser requested the address 
The request and the server response have several 
![Screenshot of response headers](../assets/ec00e3a96d653e96.png)
The _Response headers_ on top tell us e.g. the size of the response in bytes and the exact time of the response. An important header 
The _Response_ tab shows the response data, a regular HTML page. The _body_ section determines the structure of the page rendered to the screen:
![Screenshot of the response tab](../assets/391bf15932ff7447.png)
The page contains a _notes_ , and an 
Because of the img tag, the browser does a second _HTTP request_ to fetch the image _kuva.png_ from the server. The details of the request are as follows:
![Detailed view of the second event](../assets/f67d6ad99fec1564.png)
The request was made to the address _image/png_ , so it is a png image. The browser uses this information to render the image correctly to the screen.
The chain of events caused by opening the page 
![Sequence diagram of the flow covered above](../assets/9de07c8273d1598d.png)
The sequence diagram visualizes how the browser and server are communicating over the time. The time flows in the diagram from top to bottom, so the diagram starts with the first request that the browser sends to server, followed by the response.
First, the browser sends an HTTP GET request to the server to fetch the HTML code of the page. The _img_ tag in the HTML prompts the browser to fetch the image _kuva.png_. The browser renders the HTML page and the image to the screen.
Even though it is difficult to notice, the HTML page begins to render before the image has been fetched from the server.
### Traditional web applications
The homepage of the example application works like a _traditional web application_. When entering the page, the browser fetches the HTML document detailing the structure and the textual content of the page from the server.
The server has formed this document somehow. The document can be a _static_ text file saved into the server's directory. The server can also form the HTML documents _dynamically_ according to the application's code, using, for example, data from a database. The HTML code of the example application has been formed dynamically because it contains information on the number of created notes.
The HTML code of the homepage is formed dynamically on the server as follows:
```
const getFrontPageHtml = noteCount => {
  return `
    <!DOCTYPE html>
    <html>
      <head>
      </head>
      <body>
        <div class='container'>
          <h1>Full stack example app</h1>
          <p>number of notes created ${noteCount}</p>
          <a href='/notes'>notes</a>
          <img src='kuva.png' width='200' />
        </div>
      </body>
    </html>
`
}

app.get('/', (req, res) => {
  const page = getFrontPageHtml(notes.length)
  res.send(page)
})copy
```

You don't have to understand the code just yet.
The content of the HTML page has been saved as a template string or a string that allows for evaluating, for example, variables, like _noteCount_ , in the midst of it. The dynamically changing part of the homepage, the number of saved notes (in the code _noteCount_), is replaced by the current number of notes (in the code _notes.length_) in the template string.
Writing HTML amid the code is of course not smart, but for old-school PHP programmers, it was a normal practice.
In traditional web applications, the browser is "dumb". It only fetches HTML data from the server, and all application logic is on the server. A server can be created using 
The example uses 
### Running application logic in the browser
Keep the Developer Console open. Empty the console by clicking the 🚫 symbol, or by typing clear() in the console. Now when you go to the 
![Screenshot of the developer console with the 4 requests visible](../assets/c4df278c632e65c0.png)
All of the requests have _different_ types. The first request's type is _document_. It is the HTML code of the page, and it looks as follows:
![Detailed view of the first request](../assets/5b1f80ce8943a3da.png)
When we compare the page shown on the browser and the HTML code returned by the server, we notice that the code does not contain the list of notes. The _main.js_.
The JavaScript code looks as follows:
```
var xhttp = new XMLHttpRequest()

xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    const data = JSON.parse(this.responseText)
    console.log(data)

    var ul = document.createElement('ul')
    ul.setAttribute('class', 'notes')

    data.forEach(function(note) {
      var li = document.createElement('li')

      ul.appendChild(li)
      li.appendChild(document.createTextNode(note.content))
    })

    document.getElementById('notes').appendChild(ul)
  }
}

xhttp.open('GET', '/data.json', true)
xhttp.send()copy
```

The details of the code are not important right now, but some code has been included to spice up the images and the text. We will properly start coding in [part 1](../part1/01-part1.md). The sample code in this part is actually not relevant at all to the coding techniques of this course.
> Some might wonder why xhttp-object is used instead of the modern fetch. This is due to not wanting to go into promises at all yet, and the code having a secondary role in this part. We will return to modern ways to make requests to the server in [part 2](../part2/01-part2.md).
Immediately after fetching the _script_ tag, the browser begins to execute the code.
The last two lines instruct the browser to do an HTTP GET request to the server's address _/data.json_ :
```
xhttp.open('GET', '/data.json', true)
xhttp.send()copy
```

This is the bottom-most request shown on the Network tab.
We can try going to the address 
![Raw JSON Data](../assets/5270132c2d60cfa2.png)
There we find the notes in 
![Formatted JSON output](../assets/77e2de1a3731d3b2.png)
So, the JavaScript code of the notes page above downloads the JSON data containing the notes, and forms a bullet-point list from the note contents:
This is done by the following code:
```
const data = JSON.parse(this.responseText)
console.log(data)

var ul = document.createElement('ul')
ul.setAttribute('class', 'notes')

data.forEach(function(note) {
  var li = document.createElement('li')

  ul.appendChild(li)
  li.appendChild(document.createTextNode(note.content))
})

document.getElementById('notes').appendChild(ul)copy
```

The code first creates an unordered list with a 
```
var ul = document.createElement('ul')
ul.setAttribute('class', 'notes')copy
```

...and then adds one _content_ field of each note becomes the contents of the li-tag. The timestamps found in the raw data are not used for anything here.
```
data.forEach(function(note) {
  var li = document.createElement('li')

  ul.appendChild(li)
  li.appendChild(document.createTextNode(note.content))
})copy
```

Now open the _Console_ tab on your Developer Console:
![Screenshot of the console tab on the developer console](../assets/619242063d349688.png)
By clicking the little triangle at the beginning of the line, you can expand the text on the console.
![Screenshot of one of the previously collapsed entries expanded](../assets/01a20485047f0c5b.png)
This output on the console is caused by the _console.log_ command in the code:
```
const data = JSON.parse(this.responseText)
console.log(data)copy
```

So, after receiving data from the server, the code prints it to the console.
The _Console_ tab and the _console.log_ command will become very familiar to you during the course.
### Event handlers and Callback functions
The structure of this code is a bit odd:
```
var xhttp = new XMLHttpRequest()

xhttp.onreadystatechange = function() {
  // code that takes care of the server response
}

xhttp.open('GET', '/data.json', true)
xhttp.send()copy
```

The request to the server is sent on the last line, but the code to handle the response can be found further up. What's going on?
```
xhttp.onreadystatechange = function () {copy
```

On this line, an _event handler_ for the event _onreadystatechange_ is defined for the _xhttp_ object doing the request. When the state of the object changes, the browser calls the event handler function. The function code checks that the _The operation is complete_) and that the HTTP status code of the response is 200.
```
xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    // code that takes care of the server response
  }
}copy
```

The mechanism of invoking event handlers is very common in JavaScript. Event handler functions are called _event_ has occurred.
### Document Object Model or DOM
We can think of HTML pages as implicit tree structures.
```
html
  head
    link
    script
  body
    div
      h1
      div
        ul
          li
          li
          li
      form
        input
        inputcopy
```

The same treelike structure can be seen on the console's _Elements_ tab.
![A screenshot of the Elements tab of the developer console](../assets/500435061f1fc013.png)
The functioning of the browser is based on the idea of depicting HTML elements as a tree.
Document Object Model, or _API_) that enables programmatic modification of the _element trees_ corresponding to web pages.
The JavaScript code introduced in the previous chapter used the DOM-API to add a list of notes to the page.
The following code creates a new node, assigns it to the variable _ul_ , and adds some child nodes to it:
```
var ul = document.createElement('ul')

data.forEach(function(note) {
  var li = document.createElement('li')

  ul.appendChild(li)
  li.appendChild(document.createTextNode(note.content))
})copy
```

Finally, the tree branch of the _ul_ variable is connected to its proper place in the HTML tree of the whole page:
```
document.getElementById('notes').appendChild(ul)copy
```

### Manipulating the document object from console
The topmost node of the DOM tree of an HTML document is called the _document_ object. We can perform various operations on a webpage using the DOM-API. You can access the _document_ object by typing _document_ into the Console tab:
![document in console tab of developer tools](../assets/2f97ff9185612f87.png)
Let's add a new note to the page from the console.
First, we'll get the list of notes from the page. The list is in the first ul-element of the page:
```
list = document.getElementsByTagName('ul')[0]copy
```

Then create a new li-element and add some text content to it:
```
newElement = document.createElement('li')
newElement.textContent = 'Page manipulation from console is easy'copy
```

And add the new li-element to the list:
```
list.appendChild(newElement)copy
```

![Screenshot of the page with the new note added to the list](../assets/4d3ee3ed83155ada.png)
Even though the page updates on your browser, the changes are not permanent. If the page is reloaded, the new note will disappear, because the changes were not pushed to the server. The JavaScript code the browser fetches will always create the list of notes based on JSON data from the address 
### CSS
The _head_ element of the HTML code of the Notes page contains a 
Cascading Style Sheets, or CSS, is a style sheet language used to determine the appearance of web pages.
The fetched CSS file looks as follows:
```
.container {
  padding: 10px;
  border: 1px solid;
}

.notes {
  color: blue;
}copy
```

The file defines two 
A class selector definition always starts with a period and contains the name of the class.
Classes are 
CSS attributes can be examined in the _Elements_ tab of the console:
![Screenshot of the Elements tab on the developer console](../assets/c4d8eef55080d18f.png)
The outermost _div_ element has the class _container_. The _ul_ element containing the list of notes has the class _notes_.
The CSS rule defines that elements with the _container_ class will be outlined with a one-pixel wide 
The second CSS rule sets the text color of the _notes_ class as blue.
HTML elements can also have other attributes apart from classes. The _div_ element containing the notes has an 
The _Elements_ tab of the console can be used to change the styles of the elements.
![developer tools elements tab showing CSS rules applied to container class](../assets/254a8ea7e30cd449.png)
Changes made on the console will not be permanent. If you want to make lasting changes, they must be saved to the CSS style sheet on the server.
### Loading a page containing JavaScript - review
Let's review what happens when the page 
![sequence diagram of browser/server interaction](../assets/9f81e0dd370e862e.png)
  * The browser fetches the HTML code defining the content and the structure of the page from the server using an HTTP GET request.
  * Links in the HTML code cause the browser to also fetch the CSS style sheet _main.css_...
  * ...and the JavaScript code file _main.js_
  * The browser executes the JavaScript code. The code makes an HTTP GET request to the address 
  * When the data has been fetched, the browser executes an _event handler_ , which renders the notes to the page using the DOM-API.


### Forms and HTTP POST
Next, let's examine how adding a new note is done.
The Notes page contains a 
![form element highlight in webpage and developer tools](../assets/868007cc42b262ad.png)
When the button on the form is clicked, the browser will send the user input to the server. Let's open the _Network_ tab and see what submitting the form looks like:
![Screenshot of the Network tab where the events for submitting the form are shown](../assets/fa77f7412f73530c.png)
Surprisingly, submitting the form causes no fewer than _five_ HTTP requests. The first one is the form submit event. Let's zoom into it:
![Detailed view of the first request](../assets/e51dab25f9e0e07b.png)
It is an _new_note_. The server responds with HTTP status code 302. This is a _Location_ - the address _notes_.
So, the browser reloads the Notes page. The reload causes three more HTTP requests: fetching the style sheet (main.css), the JavaScript code (main.js), and the raw data of the notes (data.json).
The Network tab also shows the data submitted with the form. You can view the data by first selecting the request name and then checking the Payload tab:
![form data dropdown in developer tools](../assets/1d795dd5d71d46fc.png)
The Form tag has attributes _action_ and _method_ , which define that submitting the form is done as an HTTP POST request to the address _new_note_.
![action and method highlight](../assets/0a6001108c79ef80.png)
The code on the server responsible for the POST request is quite simple (NB: this code is on the server, and not on the JavaScript code fetched by the browser):
```
app.post('/new_note', (req, res) => {
  notes.push({
    content: req.body.note,
    date: new Date(),
  })

  return res.redirect('/notes')
})copy
```

Data is sent as the 
The server can access the data by accessing the _req.body_ field of the request object _req_.
The server creates a new note object, and adds it to an array called _notes_.
```
notes.push({
  content: req.body.note,
  date: new Date(),
})copy
```

Each note object has two fields: _content_ containing the actual content of the note, and _date_ containing the date and time the note was created.
The server does not save new notes to a database, so new notes disappear when the server is restarted.
### AJAX
The Notes page of the application follows an early-nineties style of web development and uses "Ajax". As such, it's on the crest of the wave of early 2000s web technology.
Before the AJAX era, all web pages worked like the [traditional web application](../part0/01-fundamentals-of-web-apps-traditional-web-applications.md) we saw earlier in this chapter. All of the data shown on the page was fetched with the HTML code generated by the server.
The Notes page uses AJAX to fetch the notes data. Submitting the form still uses the traditional mechanism of submitting web forms.
The application URLs reflect the old, carefree times. JSON data is fetched from the URL [part 3](../part3/01-part3.md).
The thing termed AJAX is now so commonplace that it's taken for granted. The term has faded into oblivion, and the new generation has not even heard of it.
### Single page app
In our example app, the home page works like a traditional webpage: All of the logic is on the server, and the browser only renders the HTML as instructed.
The Notes page gives some of the responsibility, generating the HTML code for existing notes, to the browser. The browser tackles this task by executing the JavaScript code it fetched from the server. The code fetches the notes from the server as JSON data and adds HTML elements for displaying the notes to the page using the [DOM-API](../part0/01-fundamentals-of-web-apps-document-object-model-or-dom.md).
In recent years, the 
The Notes page of our application bears some resemblance to SPA-style apps, but it's not quite there yet. Even though the logic for rendering the notes is run on the browser, the page still uses the traditional way of adding new notes. The data is sent to the server via the form's submit, and the server instructs the browser to reload the Notes page with a _redirect_.
A single-page app version of our example application can be found at _spa.js_) and there is a small change in how the form-tag is defined:
![form with missing action and method](../assets/ec9ee03947326c9d.png)
The form has no _action_ or _method_ attributes to define how and where to send the input data.
Open the _Network_ tab and empty it. When you now create a new note, you'll notice that the browser sends only one request to the server.
![Network tab showing one POST request to new_note_spa](../assets/19d3a0f00f463d36.png)
The POST request to the address _new_note_spa_ contains the new note as JSON data containing both the content of the note (_content_) and the timestamp (_date_):
```
{
  content: "single page app does not reload the whole page",
  date: "2019-05-25T15:15:59.905Z"
}copy
```

The _Content-Type_ header of the request tells the server that the included data is represented in JSON format.
![highlight of Content-type header with application/json value](../assets/d69d04201cb7ec72.png)
Without this header, the server would not know how to correctly parse the data.
The server responds with status code 
The SPA version of the app does not traditionally send the form data, but instead uses the JavaScript code it fetched from the server. We'll look into this code a bit, even though understanding all the details of it is not important just yet.
```
var form = document.getElementById('notes_form')
form.onsubmit = function(e) {
  e.preventDefault()

  var note = {
    content: e.target.elements[0].value,
    date: new Date(),
  }

  notes.push(note)
  e.target.elements[0].value = ''
  redrawNotes()
  sendToServer(note)
}copy
```

The command _document.getElementById('notes_form')_ instructs the code to fetch a reference to the HTML form element on the page that has the ID "notes_form" and to register an _event handler_ to handle the form's submit event. The event handler immediately calls the method _e.preventDefault()_ to prevent the default handling of form's submit. The default method would send the data to the server and cause a new GET request, which we don't want to happen.
Then the event handler creates a new note, adds it to the notes list with the command _notes.push(note)_ , rerenders the note list on the page and sends the new note to the server.
The code for sending the note to the server is as follows:
```
var sendToServer = function(note) {
  var xhttpForPost = new XMLHttpRequest()
  // ...

  xhttpForPost.open('POST', '/new_note_spa', true)
  xhttpForPost.setRequestHeader('Content-type', 'application/json')
  xhttpForPost.send(JSON.stringify(note))
}copy
```

The code determines that the data is to be sent with an HTTP POST request and the data type is to be JSON. The data type is determined with a _Content-type_ header. Then the data is sent as JSON string.
The application code is available at _new_note_spa_ that new notes are sent to, does not adhere to current best practices.
### JavaScript-libraries
The sample app is done with so-called 
Instead of using JavaScript and the DOM-API only, different libraries containing tools that are easier to work with compared to the DOM-API are often used to manipulate pages. One of these libraries is the ever-so-popular 
jQuery was developed back when web applications mainly followed the traditional style of the server generating HTML pages, the functionality of which was enhanced on the browser side using JavaScript written with jQuery. One of the reasons for the success of jQuery was its so-called cross-browser compatibility. The library worked regardless of the browser or the company that made it, so there was no need for browser-specific solutions. Nowadays using jQuery is not as justified given the advancement of JavaScript, and the most popular browsers generally support basic functionalities well.
The rise of the single-page app brought several more "modern" ways of web development than jQuery. The favorite of the first wave of developers was 
However, the popularity of Angular plummeted in October 2014 after the 
Currently, the most popular tool for implementing the browser-side logic of web applications is Facebook's 
The status of React seems strong, but the world of JavaScript is ever-changing. For example, recently a newcomer - 
### Full-stack web development
What does the name of the course, _Full stack web development_ , mean? Full stack is a buzzword that everyone talks about, but no one knows what it means. Or at least, there is no agreed-upon definition for the term.
Practically all web applications have (at least) two "layers": the browser, being closer to the end-user, is the top layer, and the server the bottom one. There is often also a database layer below the server. We can therefore think of the _architecture_ of a web application as a _stack_ of layers.
Often, we also talk about the 
In the context of this course, full-stack web development means that we focus on all parts of the application: the frontend, the backend, and the database. Sometimes the software on the server and its operating system are seen as parts of the stack, but we won't go into those.
We will code the backend with JavaScript, using the 
It used to be more common for developers to specialize in one layer of the stack, for example, the backend. Technologies on the backend and the frontend were quite different. With the Full stack trend, it has become common for developers to be proficient in all layers of the application and the database. Oftentimes, full-stack developers must also have enough configuration and administration skills to operate their applications, for example, in the cloud.
### JavaScript fatigue
Full-stack web development is challenging in many ways. Things are happening in many places at once, and debugging is quite a bit harder than with regular desktop applications. JavaScript does not always work as you'd expect it to (compared to many other languages), and the asynchronous way its runtime environments work causes all sorts of challenges. Communicating on the web requires knowledge of the HTTP protocol. One must also handle databases and server administration and configuration. It would also be good to know enough CSS to make applications at least somewhat presentable.
The world of JavaScript develops fast, which brings its own set of challenges. Tools, libraries and the language itself are under constant development. Some are starting to get tired of the constant change, and have coined a term for it: _JavaScript fatigue_. See 
You will suffer from JavaScript fatigue yourself during this course. Fortunately for us, there are a few ways to smooth the learning curve, and we can start with coding instead of configuration. We can't avoid configuration completely, but we can merrily push ahead in the next few weeks while avoiding the worst of configuration hells.
### Exercises 0.1.-0.6.
The exercises are submitted via GitHub, and by marking the exercises as done in the "my submissions" tab of the 
You can submit all of the exercises into the same repository, or use multiple different repositories. If you submit exercises from different parts into the same repository, name your directories well. If you use a private repository to submit the exercises, add _mluukkai_ as a collaborator to it.
One good way to name the directories in your submission repository is as follows:
```
part0
part1
  courseinfo
  unicafe
  anecdotes
part2
  courseinfo
  phonebook
  countriescopy
```

So, each part has its own directory, which contains a directory for each exercise set (like the unicafe exercises in part 1).
The exercises are submitted **one part at a time**. When you have submitted the exercises for a part, you can no longer submit any missed exercises for that part.
#### 0.1: HTML
Review the basics of HTML by reading this tutorial from Mozilla: 
_This exercise is not submitted to GitHub, it's enough to just read the tutorial_
#### 0.2: CSS
Review the basics of CSS by reading this tutorial from Mozilla: 
_This exercise is not submitted to GitHub, it's enough to just read the tutorial_
#### 0.3: HTML forms
Learn about the basics of HTML forms by reading Mozilla's tutorial 
_This exercise is not submitted to GitHub, it's enough to just read the tutorial_
#### 0.4: New note diagram
In the section [Loading a page containing JavaScript - review](../part0/01-fundamentals-of-web-apps-loading-a-page-containing-java-script-review.md), the chain of events caused by opening the page 
The diagram was made as a GitHub Markdown-file using the 
```
sequenceDiagram
    participant browser
    participant server

    browser->>server: GET https://studies.cs.helsinki.fi/exampleapp/notes
    activate server
    server-->>browser: HTML document
    deactivate server

    browser->>server: GET https://studies.cs.helsinki.fi/exampleapp/main.css
    activate server
    server-->>browser: the css file
    deactivate server

    browser->>server: GET https://studies.cs.helsinki.fi/exampleapp/main.js
    activate server
    server-->>browser: the JavaScript file
    deactivate server

    Note right of browser: The browser starts executing the JavaScript code that fetches the JSON from the server

    browser->>server: GET https://studies.cs.helsinki.fi/exampleapp/data.json
    activate server
    server-->>browser: [{ "content": "HTML is easy", "date": "2023-1-1" }, ... ]
    deactivate server

    Note right of browser: The browser executes the callback function that renders the notescopy
```

**Create a similar diagram** depicting the situation where the user creates a new note on the page _Save_ button.
If necessary, show operations on the browser or on the server as comments on the diagram.
The diagram does not have to be a sequence diagram. Any sensible way of presenting the events is fine.
All necessary information for doing this, and the next two exercises, can be found in the text of [this part](../part0/01-fundamentals-of-web-apps-forms-and-http-post.md). The idea of these exercises is to read the text once more and to think through what is going on there. Reading the application 
You can do the diagrams with any program, but perhaps the easiest and the best way to do diagrams is the 
#### 0.5: Single page app diagram
Create a diagram depicting the situation where the user goes to the [single-page app](../part0/01-fundamentals-of-web-apps-single-page-app.md) version of the notes app at 
#### 0.6: New note in Single page app diagram
Create a diagram depicting the situation where the user creates a new note using the single-page version of the app.
This was the last exercise, and it's time to push your answers to GitHub and mark the exercises as done in the 
[ Part 0a **Previous part** ](../part0/01-general-info.md)[ Part 1 **Next part** ](../part1/01-part1.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)