---{
  "title": "Class components, Miscellaneous",
  "source_url": "https://fullstackopen.com/en/part7/class_components_miscellaneous",
  "crawl_timestamp": "2025-10-04T19:16:54Z",
  "checksum": "38b3ab3fa3695e60a3409c84e115509895a53d8e91392a0e6832df1627437c45"
}
---[Skip to content](../part7/01-class-components-miscellaneous-course-main-content.md)
[{() => fs}](https://fullstackopen.com/en/)
  * [About course](../about/01-about.md)
  * [Course contents](../#course-contents/01-course-contents.md)
  * [FAQ](../faq/01-faq.md)
  * [Partners](../companies/01-companies.md)
  * [Challenge](../challenge/01-challenge.md)
[Search from the material](../search/01-search.md)Toggle dark theme
Select languageSuomi English 中文 Español Français Português(BR) 

[Fullstack](../#course-contents/01-course-contents.md)
[Part 7](../part7/01-part7.md)
Class components, Miscellaneous
[a React Router](../part7/01-react-router.md)[b Custom hooks](../part7/01-custom-hooks.md)[c More about styles](../part7/01-more-about-styles.md)[d Webpack](../part7/01-webpack.md)
e Class components, Miscellaneous
  * [Class Components](../part7/01-class-components-miscellaneous-class-components.md)
  * [Organization of code in React application](../part7/01-class-components-miscellaneous-organization-of-code-in-react-application.md)
  * [Frontend and backend in the same repository](../part7/01-class-components-miscellaneous-frontend-and-backend-in-the-same-repository.md)
  * [Changes on the server](../part7/01-class-components-miscellaneous-changes-on-the-server.md)
  * [Virtual DOM](../part7/01-class-components-miscellaneous-virtual-dom.md)
  * [On the role of React in applications](../part7/01-class-components-miscellaneous-on-the-role-of-react-in-applications.md)
  * [React/node-application security](../part7/01-class-components-miscellaneous-react-node-application-security.md)
  * [Current trends](../part7/01-class-components-miscellaneous-current-trends.md)
  * [Useful libraries and interesting links](../part7/01-class-components-miscellaneous-useful-libraries-and-interesting-links.md)


[f Exercises: extending the bloglist](../part7/01-exercises-extending-the-bloglist.md)
e
# Class components, Miscellaneous
### Class Components
During the course, we have only used React components having been defined as Javascript functions. This was not possible without the 
It is beneficial to at least be familiar with Class Components to some extent since the world contains a lot of old React code, which will probably never be completely rewritten using the updated syntax.
Let's get to know the main features of Class Components by producing yet another very familiar anecdote application. We store the anecdotes in the file _db.json_ using _json-server_. The contents of the file are lifted from 
The initial version of the Class Component looks like this
```
import React from 'react'

class App extends React.Component {
  constructor(props) {
    super(props)
  }

  render() {
    return (
      <div>
        <h1>anecdote of the day</h1>
      </div>
    )
  }
}

export default Appcopy
```

The component now has a 
Let's define a state for the list of anecdotes and the currently-visible anecdote. In contrast to when using the 
```
class App extends React.Component {
  constructor(props) {
    super(props)

    this.state = {      anecdotes: [],      current: 0    }  }

  render() {
    if (this.state.anecdotes.length === 0) {      return <div>no anecdotes...</div>    }
    return (
      <div>
        <h1>anecdote of the day</h1>
        <div>          {this.state.anecdotes[this.state.current].content}        </div>        <button>next</button>      </div>
    )
  }
}copy
```

The component state is in the instance variable _this.state_. The state is an object having two properties. _this.state.anecdotes_ is the list of anecdotes and _this.state.current_ is the index of the currently-shown anecdote.
In Functional components, the right place for fetching data from a server is inside an 
The 
```
class App extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      anecdotes: [],
      current: 0
    }
  }

  componentDidMount = () => {    axios.get('http://localhost:3001/anecdotes').then(response => {      this.setState({ anecdotes: response.data })    })  }
  // ...
}copy
```

The callback function of the HTTP request updates the component state using the method _current_ remains unchanged.
Calling the method setState always triggers the rerender of the Class Component, i.e. calling the method _render_.
We'll finish off the component with the ability to change the shown anecdote. The following is the code for the entire component with the addition highlighted:
```
class App extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      anecdotes: [],
      current: 0
    }
  }

  componentDidMount = () => {
    axios.get('http://localhost:3001/anecdotes').then(response => {
      this.setState({ anecdotes: response.data })
    })
  }

  handleClick = () => {    const current = Math.floor(      Math.random() * this.state.anecdotes.length    )    this.setState({ current })  }
  render() {
    if (this.state.anecdotes.length === 0 ) {
      return <div>no anecdotes...</div>
    }

    return (
      <div>
        <h1>anecdote of the day</h1>
        <div>{this.state.anecdotes[this.state.current].content}</div>
        <button onClick={this.handleClick}>next</button>      </div>
    )
  }
}copy
```

For comparison, here is the same application as a Functional component:
```
const App = () => {
  const [anecdotes, setAnecdotes] = useState([])
  const [current, setCurrent] = useState(0)

  useEffect(() =>{
    axios.get('http://localhost:3001/anecdotes').then(response => {
      setAnecdotes(response.data)
    })
  },[])

  const handleClick = () => {
    setCurrent(Math.round(Math.random() * (anecdotes.length - 1)))
  }

  if (anecdotes.length === 0) {
    return <div>no anecdotes...</div>
  }

  return (
    <div>
      <h1>anecdote of the day</h1>
      <div>{anecdotes[current].content}</div>
      <button onClick={handleClick}>next</button>
    </div>
  )
}copy
```

In the case of our example, the differences were minor. The biggest difference between Functional components and Class components is mainly that the state of a Class component is a single object, and that the state is updated using the method _setState_ , while in Functional components the state can consist of multiple different variables, with all of them having their own update function.
In some more advanced use cases, the effect hook offers a considerably better mechanism for controlling side effects compared to the lifecycle methods of Class Components.
A notable benefit of using Functional components is not having to deal with the self-referencing _this_ reference of the Javascript class.
In my opinion, and the opinion of many others, Class Components offer little benefit over Functional components enhanced with hooks, except for the so-called 
When writing fresh code, 
### Organization of code in React application
In most applications, we followed the principle by which components were placed in the directory _components_ , reducers were placed in the directory _reducers_ , and the code responsible for communicating with the server was placed in the directory _services_. This way of organizing fits a smaller application just fine, but as the amount of components increases, better solutions are needed. There is no one correct way to organize a project. The article 
### Frontend and backend in the same repository
During the course, we have created the frontend and backend into separate repositories. This is a very typical approach. However, we did the deployment by [copying](../part3/01-deploying-app-to-internet-serving-static-files-from-the-backend.md) the bundled frontend code into the backend repository. A possibly better approach would have been to deploy the frontend code separately.
Sometimes, there may be a situation where the entire application is to be put into a single repository. In this case, a common approach is to put the _package.json_ and _webpack.config.js_ in the root directory, as well as place the frontend and backend code into their own directories, e.g. _client_ and _server_.
### Changes on the server
If there are changes in the state on the server, e.g. when new blogs are added by other users to the bloglist service, the React frontend we implemented during this course will not notice these changes until the page reloads. A similar situation arises when the frontend triggers a time-consuming computation in the backend. How do we reflect the results of the computation to the frontend?
One way is to execute 
A more sophisticated way is to use 
WebSockets is an API provided by the browser, which is not yet fully supported on all browsers:
![caniuse chart showing websockets not usable by all yet](../assets/d65cc8f79a90c770.png)
Instead of directly using the WebSocket API, it is advisable to use the _fallback_ options in case the browser does not have full support for WebSockets.
In [part 8](../part8/01-part8.md), our topic is GraphQL, which provides a nice mechanism for notifying clients when there are changes in the backend data.
### Virtual DOM
The concept of the Virtual DOM often comes up when discussing React. What is it all about? As mentioned in [part 0](../part0/01-fundamentals-of-web-apps-document-object-model-or-dom.md), browsers provide a 
When a software developer uses React, they rarely or never directly manipulate the DOM. The function defining the React component returns a set of 
```
const element = <h1>Hello, world</h1>copy
```

they are also just JavaScript-based React elements at their core.
The React elements defining the appearance of the components of the application make up the 
With the help of the 
```
ReactDOM.createRoot(document.getElementById('root')).render(<App />)copy
```

When the state of the application changes, a _new virtual DOM_ gets defined by the components. React has the previous version of the virtual DOM in memory and instead of directly rendering the new virtual DOM using the DOM API, React computes the optimal way to update the DOM (remove, add or modify elements in the DOM) such that the DOM reflects the new virtual DOM.
### On the role of React in applications
In the material, we may not have put enough emphasis on the fact that React is primarily a library for managing the creation of views for an application. If we look at the traditional _View_. React has a more narrow area of application than e.g. _framework_ , but a _library_.
In small applications, data handled by the application is stored in the state of the React components, so in this scenario, the state of the components can be thought of as _models_ of an MVC architecture.
However, MVC architecture is not usually mentioned when talking about React applications. Furthermore, if we are using Redux, then the applications follow the [Redux Thunk](../part6/01-communicating-with-server-in-a-redux-application-asynchronous-actions-and-redux-thunk.md) familiar from part 6, then the business logic can be almost completely separated from the React code.
Because both React and 
Part 6 [last chapter](../part6/01-react-query-use-reducer-and-the-context.md) covers the newer trends of state management in React. React's hook functions _useReducer_ and _useContext_ provide a kind of lightweight version of Redux. _React Query_ , on the other hand, is a library that solves many of the problems associated with handling state on the server, eliminating the need for a React application to store data retrieved from the server directly in frontend state.
### React/node-application security
So far during the course, we have not touched on information security much. We do not have much time for this now either, but fortunately, University of Helsinki has a MOOC course 
We will, however, take a look at some things specific to this course.
The Open Web Application Security Project, otherwise known as 
At the top of the list, we find _injection_ , which means that e.g. text sent using a form in an application is interpreted completely differently than the software developer had intended. The most famous type of injection is probably 
For example, imagine that the following SQL query is executed in a vulnerable application:
```
let query = "SELECT * FROM Users WHERE name = '" + userName + "';"copy
```

Now let's assume that a malicious user _Arto Hellas_ would define their name as
```
Arto Hell-as'; DROP TABLE Users; --copy
```

so that the name would contain a single quote `'`, which is the beginning and end character of a SQL string. As a result of this, two SQL operations would be executed, the second of which would destroy the database table _Users_ :
```
SELECT * FROM Users WHERE name = 'Arto Hell-as'; DROP TABLE Users; --'copy
```

SQL injections are prevented using `?`):
```
execute("SELECT * FROM Users WHERE name = ?", [userName])copy
```

Injection attacks are also possible in NoSQL databases. However, mongoose prevents them by 
_Cross-site scripting (XSS)_ is an attack where it is possible to inject malicious JavaScript code into a legitimate web application. The malicious code would then be executed in the browser of the victim. If we try to inject the following into e.g. the notes application:
```
<script>
  alert('Evil XSS attack')
</script>copy
```

the code is not executed, but is only rendered as 'text' on the page:
![browser showing notes with XSS attempt](../assets/fbaba65b829eecbf.png)
since React 
One needs to remain vigilant when using libraries; if there are security updates to those libraries, it is advisable to update those libraries in one's applications. Security updates for Express are found in the 
You can check how up-to-date your dependencies are using the command
```
npm outdated --depth 0copy
```

The one-year-old project that is used in [part 9](../part9/01-part9.md) of this course already has quite a few outdated dependencies:
![npm outdated output of patientor](../assets/51c34854bf75144e.png)
The dependencies can be brought up to date by updating the file _package.json_. The best way to do that is by using a tool called _npm-check-updates_. It can be installed globally by running the command:
```
npm install -g npm-check-updatescopy
```

Using this tool, the up-to-dateness of dependencies is checked in the following way:
```
$ npm-check-updates
Checking ...\ultimate-hooks\package.json
[====================] 9/9 100%

 @testing-library/react       ^13.0.0  →  ^13.1.1
 @testing-library/user-event  ^14.0.4  →  ^14.1.1
 react-scripts                  5.0.0  →    5.0.1

Run ncu -u to upgrade package.jsoncopy
```

The file _package.json_ is brought up to date by running the command _ncu -u_.
```
$ ncu -u
Upgrading ...\ultimate-hooks\package.json
[====================] 9/9 100%

 @testing-library/react       ^13.0.0  →  ^13.1.1
 @testing-library/user-event  ^14.0.4  →  ^14.1.1
 react-scripts                  5.0.0  →    5.0.1

Run npm install to install new versions.copy
```

Then it is time to update the dependencies by running the command _npm install_. However, old versions of the dependencies are not necessarily a security risk.
The npm 
Running _npm audit_ on the same project, it prints a long list of complaints and suggested fixes. Below is a part of the report:
```
$ patientor npm audit

... many lines removed ...

url-parse  <1.5.2
Severity: moderate
Open redirect in url-parse - https://github.com/advisories/GHSA-hh27-ffr2-f2jc
fix available via `npm audit fix`
node_modules/url-parse

ws  6.0.0 - 6.2.1 || 7.0.0 - 7.4.5
Severity: moderate
ReDoS in Sec-Websocket-Protocol header - https://github.com/advisories/GHSA-6fc8-4gx4-v693
ReDoS in Sec-Websocket-Protocol header - https://github.com/advisories/GHSA-6fc8-4gx4-v693
fix available via `npm audit fix`
node_modules/webpack-dev-server/node_modules/ws
node_modules/ws

120 vulnerabilities (102 moderate, 16 high, 2 critical)

To address issues that do not require attention, run:
  npm audit fix

To address all issues (including breaking changes), run:
  npm audit fix --forcecopy
```

After only one year, the code is full of small security threats. Luckily, there are only 2 critical threats. Let's run _npm audit fix_ as the report suggests:
```
$ npm audit fix

+ mongoose@5.9.1
added 19 packages from 8 contributors, removed 8 packages and updated 15 packages in 7.325s
fixed 354 of 416 vulnerabilities in 20047 scanned packages
  1 package update for 62 vulns involved breaking changes
  (use `npm audit fix --force` to install breaking changes; or refer to `npm audit` for steps to fix these manually)copy
```

62 threats remain because, by default, _audit fix_ does not update dependencies if their _major_ version number has increased. Updating these dependencies could lead to the whole application breaking down.
The source for the critical bug is the library 
```
immer  <9.0.6
Severity: critical
Prototype Pollution in immer - https://github.com/advisories/GHSA-33f9-j839-rf8h
fix available via `npm audit fix --force`
Will install react-scripts@5.0.0, which is a breaking changecopy
```

Running _npm audit fix --force_ would upgrade the library version but would also upgrade the library _react-scripts_ and that would potentially break down the development environment. So we will leave the library upgrades for later...
One of the threats mentioned in the list from OWASP is _Broken Authentication_ and the related _Broken Access Control_. The token-based authentication we have been using is fairly robust if the application is being used on the traffic-encrypting HTTPS protocol. When implementing access control, one should e.g. remember to not only check a user's identity in the browser but also on the server. Bad security would be to prevent some actions to be taken only by hiding the execution options in the code of the browser.
On Mozilla's MDN, there is a very good 
![screenshot of website security from MDN](../assets/96747bbbe81bc425.png)
The documentation for Express includes a section on security: 
Using the ESlint 
### Current trends
Finally, let's take a look at some technology of tomorrow (or, actually, already today), and the directions in which Web development is heading.
#### Typed versions of JavaScript
Sometimes, the [PropTypes](../part5/01-props-children-and-proptypes-prop-types.md): a mechanism which enables one to enforce type-checking for props passed to React components.
Lately, there has been a notable uplift in the interest in [part 9](../part9/01-part9.md).
#### Server-side rendering, isomorphic applications and universal code
The browser is not the only domain where components defined using React can be rendered. The rendering can also be done on the _server-side rendering_.
One motivation for server-side rendering is Search Engine Optimization (SEO). Search engines have traditionally been very bad at recognizing JavaScript-rendered content. However, the tide might be turning, e.g. take a look at 
Of course, server-side rendering is not anything specific to React or even JavaScript. Using the same programming language throughout the stack in theory simplifies the execution of the concept because the same code can be run on both the front- and backend.
Along with server-side rendering, there has been talk of so-called _isomorphic applications_ and _universal code_ , although there has been some debate about their definitions. According to some 
React and Node provide a desirable option for implementing an isomorphic application as universal code.
Writing universal code directly using React is currently still pretty cumbersome. Lately, a library called 
#### Progressive web apps
Lately, people have started using the term 
In short, we are talking about web applications working as well as possible on every platform and taking advantage of the best parts of those platforms. The smaller screen of mobile devices must not hamper the usability of the application. PWAs should also work flawlessly in offline mode or with a slow internet connection. On mobile devices, they must be installable just like any other application. All the network traffic in a PWA should be encrypted.
#### Microservice architecture
During this course, we have only scratched the surface of the server end of things. In our applications, we had a _monolithic_ backend, meaning one application making up a whole and running on a single server, serving only a few API endpoints.
As the application grows, the monolithic backend approach starts turning problematic both in terms of performance and maintainability.
A 
For example, the bloglist application could consist of two services: one handling the user and another taking care of the blogs. The responsibility of the user service would be user registration and user authentication, while the blog service would take care of operations related to the blogs.
The image below visualizes the difference between the structure of an application based on a microservice architecture and one based on a more traditional monolithic structure:
![microservices vs traditional approach diagram](../assets/614123fd317b5dde.png)
The role of the frontend (enclosed by a square in the picture) does not differ much between the two models. There is often a so-called 
Microservice architectures emerged and evolved for the needs of large internet-scale applications. The trend was set by Amazon far before the appearance of the term microservice. The critical starting point was an email sent to all employees in 2002 by Amazon CEO Jeff Bezos:
> All teams will henceforth expose their data and functionality through service interfaces.
> Teams must communicate with each other through these interfaces.
> There will be no other form of inter-process communication allowed: no direct linking, no direct reads of another team’s data store, no shared-memory model, no back-doors whatsoever. The only communication allowed is via service interface calls over the network.
> It doesn’t matter what technology you use.
> All service interfaces, without exception, must be designed from the ground up to be externalize-able. That is to say, the team must plan and design to be able to expose the interface to developers in the outside world.
> No exceptions.
> Anyone who doesn’t do this will be fired. Thank you; have a nice day!
Nowadays, one of the biggest forerunners in the use of microservices is 
The use of microservices has steadily been gaining hype to be kind of a 
Unfortunately, we cannot dive deeper into this important topic during this course. Even a cursory look at the topic would require at least 5 more weeks.
#### Serverless
After the release of Amazon's 
The main thing about lambda, and nowadays also Google's _the execution of individual functions_ in the cloud. Before, the smallest executable unit in the cloud was a single _process_ , e.g. a runtime environment running a Node backend.
E.g. Using Amazon's 
Serverless is not about there not being a server in applications, but about how the server is defined. Software developers can shift their programming efforts to a higher level of abstraction as there is no longer a need to programmatically define the routing of HTTP requests, database relations, etc., since the cloud infrastructure provides all of this. Cloud functions also lend themselves to creating a well-scaling system, e.g. Amazon's Lambda can execute a massive amount of cloud functions per second. All of this happens automatically through the infrastructure and there is no need to initiate new servers, etc.
### Useful libraries and interesting links
The JavaScript developer community has produced a large variety of useful libraries. If you are developing anything more substantial, it is worth it to check if existing solutions are already available. Below are listed some libraries recommended by trustworthy parties.
If your application has to handle complicated data, [part 4](../part4/01-structure-of-backend-application-introduction-to-testing-exercises-4-3-4-7.md), is a good library to use. If you prefer the functional programming style, you might consider using 
If you are handling times and dates, 
If you have complex forms in your apps, have a look at whether 
If your application displays graphs, there are multiple options to choose from. Both 
The [remember](../part6/01-flux-architecture-and-redux-pure-functions-immutable.md) from part 6, reducers must be pure functions, meaning they must not modify the store's state but instead have to replace it with a new one when a change occurs.
[Redux Thunk](../part6/01-communicating-with-server-in-a-redux-application-asynchronous-actions-and-redux-thunk.md) familiar from part 6. Some embrace the hype and like it. I don't.
For single-page applications, the gathering of analytics data on the interaction between the users and the page is 
You can take advantage of your React know-how when developing mobile applications using Facebook's extremely popular [part 10](../part10/01-part10.md) of the course.
When it comes to the tools used for the management and bundling of JavaScript projects, the community has been very fickle. Best practices have changed rapidly (the years are approximations, nobody remembers that far back in the past):
  * 2011 
  * 2012 
  * 2013-14 
  * 2012-14 
  * 2015-2023 
  * 2023- 


Hipsters seemed to have lost their interest in tool development after webpack started to dominate the markets. A few years ago, 
The site 
If you know some recommendable links or libraries, make a pull request!
[ Part 7d **Previous part** ](../part7/01-webpack.md)[ Part 7f **Next part** ](../part7/01-exercises-extending-the-bloglist.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)