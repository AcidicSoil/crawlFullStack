---{
  "title": "Webpack",
  "source_url": "https://fullstackopen.com/en/part7/webpack",
  "crawl_timestamp": "2025-10-04T19:17:07Z",
  "checksum": "032615081725cf9a9fb9676e22f8dccce34cb828bce560b6098f83a90c02ca47"
}
---[Skip to content](../part7/01-webpack-course-main-content.md)
[{() => fs}](https://fullstackopen.com/en/)

- [About course](../about/01-about.md)
- [Course contents](../#course-contents/01-course-contents.md)
- [FAQ](../faq/01-faq.md)
- [Partners](../companies/01-companies.md)
- [Challenge](../challenge/01-challenge.md)
[Search from the material](../search/01-search.md)Toggle dark theme
Select languageSuomi English 中文 Español Français Português(BR)

[Fullstack](../#course-contents/01-course-contents.md)
[Part 7](../part7/01-part7.md)
Webpack
[a React Router](../part7/01-react-router.md)[b Custom hooks](../part7/01-custom-hooks.md)[c More about styles](../part7/01-more-about-styles.md)
d Webpack
[e Class components, Miscellaneous](../part7/01-class-components-miscellaneous.md)[f Exercises: extending the bloglist](../part7/01-exercises-extending-the-bloglist.md)
d
# Webpack
In the early days, React was somewhat famous for being very difficult to configure the tools required for application development. To make the situation easier,
Both Vite and Create React App use _bundlers_ to do the actual work. We will now familiarize ourselves with the bundler called
### Bundling
We have implemented our applications by dividing our code into separate modules that have been _imported_ to places that require them. Even though ES6 modules are defined in the ECMAScript standard, the older browsers do not know how to handle code that is divided into modules.
For this reason, code that is divided into modules must be _bundled_ for browsers, meaning that all of the source code files are transformed into a single file that contains all of the application code. When we deployed our React frontend to production in [part 3](../part3/01-deploying-app-to-internet.md), we performed the bundling of our application with the _npm run build_ command. Under the hood, the npm script bundles the source, and this produces the following collection of files in the _dist_ directory:

```
├── assets
│   ├── index-d526a0c5.css
│   ├── index-e92ae01e.js
│   └── react-35ef61ed.svg
├── index.html
└── vite.svg
```

The _index.html_ file located at the root of the _dist_ directory is the "main file" of the application which loads the bundled JavaScript file with a _script_ tag:

```
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Vite + React</title>
    <script type="module" crossorigin src="/assets/index-e92ae01e.js"></script>
    <link rel="stylesheet" href="/assets/index-d526a0c5.css">
  </head>
  <body>
    <div id="root"></div>
    
  </body>
</html>
```

As we can see from the example application that was created with Vite, the build script also bundles the application's CSS files into a single _/assets/index-d526a0c5.css_ file.
In practice, bundling is done so that we define an entry point for the application, which typically is the _index.js_ file. When webpack bundles the code, it includes not only the code from the entry point but also the code that is imported by the entry point, as well as the code imported by its import statements, and so on.
Since part of the imported files are packages like React, Redux, and Axios, the bundled JavaScript file will also contain the contents of each of these libraries.
> The old way of dividing the application's code into multiple files was based on the fact that the _index.html_ file loaded all of the separate JavaScript files of the application with the help of script tags. This resulted in decreased performance, since the loading of each separate file results in some overhead. For this reason, these days the preferred method is to bundle the code into a single file.
Next, we will create a webpack configuration by hand, suitable for a new React application.
Let's create a new directory for the project with the following subdirectories (_build_ and _src_) and files:

```
├── build
├── package.json
├── src
│   └── index.js
└── webpack.config.js
```

The contents of the _package.json_ file can e.g. be the following:

```
{
  "name": "webpack-part7",
  "version": "0.0.1",
  "description": "practicing webpack",
  "scripts": {},
  "license": "MIT"
}
```

Let's install webpack with the command:

```
npm install --save-dev webpack webpack-cli
```

We define the functionality of webpack in the _webpack.config.js_ file, which we initialize with the following content:

```
const path = require('path')

const config = () => {
  return {
    entry: './src/index.js',
    output: {
      path: path.resolve(__dirname, 'build'),
      filename: 'main.js'
    }
  }
}

module.exports = config
```

**Note:** it would be possible to make the definition directly as an object instead of a function:

```
const path = require('path')

const config = {
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname, 'build'),
    filename: 'main.js'
  }
}

module.exports = config
```

An object will suffice in many situations, but we will later need certain features that require the definition to be done as a function.
We will then define a new npm script called _build_ that will execute the bundling with webpack:

```
// ...
"scripts": {
  "build": "webpack --mode=development"
},
// ...
```

Let's add some more code to the _src/index.js_ file:

```
const hello = name => {
  console.log(`hello ${name}`)
}
```

When we execute the _npm run build_ command, our application code will be bundled by webpack. The operation will produce a new _main.js_ file that is added under the _build_ directory:
![terminal output webpack npm run build](../assets/74010fd38c661351.png)
The file contains a lot of stuff that looks quite interesting. We can also see the code we wrote earlier at the end of the file:

```
eval("const hello = name => {\n  console.log(`hello ${name}`)\n}\n\n//# sourceURL=webpack://webpack-osa7/./src/index.js?");
```

Let's add an _App.js_ file under the _src_ directory with the following content:

```
const App = () => {
  return null
}

export default App
```

Let's import and use the _App_ module in the _index.js_ file:

```
import App from './App';

const hello = name => {
  console.log(`hello ${name}`)
}

App()
```

When we bundle the application again with the _npm run build_ command, we notice that webpack has acknowledged both files:
![terminal output showing webpack generated two files](../assets/78816c97555df624.png)
Our application code can be found at the end of the bundle file in a rather obscure format:
![terminal output showing our minified code](../assets/0da1991bf12ccb3f.png)
### Configuration file
Let's take a closer look at the contents of our current _webpack.config.js_ file:

```
const path = require('path')

const config = () => {
  return {
    entry: './src/index.js',
    output: {
      path: path.resolve(__dirname, 'build'),
      filename: 'main.js'
    }
  }
}

module.exports = config
```

The configuration file has been written in JavaScript and the function returning the configuration object is exported using Node's module syntax.
Our minimal configuration definition almost explains itself. The
The _absolute path_ , which is easy to create with the
### Bundling React
Next, let's transform our application into a minimal React application. Let's install the required libraries:

```
npm install react react-dom
```

And let's turn our application into a React application by adding the familiar definitions in the _index.js_ file:

```
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'

ReactDOM.createRoot(document.getElementById('root')).render(<App />)
```

We will also make the following changes to the _App.js_ file:

```
import React from 'react' // we need this now also in component files

const App = () => {
  return (
    <div>
      hello webpack
    </div>
  )
}

export default App
```

We still need the _build/index.html_ file that will serve as the "main page" of our application, which will load our bundled JavaScript code with a _script_ tag:

```
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>React App</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="text/javascript" src="./main.js"></script>
  </body>
</html>
```

When we bundle our application, we run into the following problem:
![webpack terminal failed loader needed](../assets/ce1fd82b9a7ff157.png)
### Loaders
The error message from webpack states that we may need an appropriate _loader_ to bundle the _App.js_ file correctly. By default, webpack only knows how to deal with plain JavaScript. Although we may have become unaware of it, we are using

```
const App = () => {
  return (
    <div>
      hello webpack
    </div>
  )
}
```

The syntax used above comes from JSX and it provides us with an alternative way of defining a React element for an HTML _div_ tag.
We can use
Let's configure a loader to our application that transforms the JSX code into regular JavaScript:

```
const path = require('path')

const config = () => {
  return {
    entry: './src/index.js',
    output: {
      path: path.resolve(__dirname, 'build'),
      filename: 'main.js'
    },
    module: {      rules: [        {          test: /\.js$/,          loader: 'babel-loader',          options: {            presets: ['@babel/preset-react'],          },        },      ],    },  }
}

module.exports = config
```

Loaders are defined under the _module_ property in the _rules_ array.
The definition of a single loader consists of three parts:

```
{
  test: /\.js$/,
  loader: 'babel-loader',
  options: {
    presets: ['@babel/preset-react']
  }
}
```

The _test_ property specifies that the loader is for files that have names ending with _.js_. The _loader_ property specifies that the processing for those files will be done with _options_ property is used for specifying parameters for the loader, which configure its functionality.
Let's install the loader and its required packages as a _development dependency_ :

```
npm install @babel/core babel-loader @babel/preset-react --save-dev
```

Bundling the application will now succeed.
If we make some changes to the _App_ component and take a look at the bundled code, we notice that the bundled version of the component looks like this:

```
const App = () =>
  react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(
    'div',
    null,
    'hello webpack'
  )
```

As we can see from the example above, the React elements that were written in JSX are now created with regular JavaScript by using React's
You can test the bundled application by opening the _build/index.html_ file with the _open file_ functionality of your browser:
![browser hello webpack](../assets/d5997f3dfa3a38cb.png)
It's worth noting that if the bundled application's source code uses _async/await_ , the browser will not render anything on some browsers.

```
npm install core-js regenerator-runtime
```

You need to import these dependencies at the top of the _index.js_ file:

```
import 'core-js/stable/index.js'
import 'regenerator-runtime/runtime.js'
```

Our configuration contains nearly everything that we need for React development.
### Transpilers
The process of transforming code from one form of JavaScript to another is called
By using the configuration from the previous section, we are _transpiling_ the code containing JSX into regular JavaScript with the help of
As mentioned in part 1, most browsers do not support the latest features that were introduced in ES6 and ES7, and for this reason, the code is usually transpiled to a version of JavaScript that implements the ES5 standard.
The transpilation process that is executed by Babel is defined with
Currently, we are using the

```
{
  test: /\.js$/,
  loader: 'babel-loader',
  options: {
    presets: ['@babel/preset-react']  }
}
```

Let's add the

```
{
  test: /\.js$/,
  loader: 'babel-loader',
  options: {
    presets: ['@babel/preset-env', '@babel/preset-react']  }
}
```

Let's install the preset with the command:

```
npm install @babel/preset-env --save-dev
```

When we transpile the code, it gets transformed into old-school JavaScript. The definition of the transformed _App_ component looks like this:

```
var App = function App() {
  return _react2.default.createElement('div', null, 'hello webpack')
};
```

As we can see, variables are declared with the _var_ keyword, as ES5 JavaScript does not understand the _const_ keyword. Arrow functions are also not used, which is why the function definition used the _function_ keyword.
### CSS
Let's add some CSS to our application. Let's create a new _src/index.css_ file:

```
.container {
  margin: 10px;
  background-color: #dee8e4;
}
```

Then let's use the style in the _App_ component:

```
const App = () => {
  return (
    <div className="container">
      hello webpack
    </div>
  )
}
```

And we import the style in the _index.js_ file:

```
import './index.css'
```

This will cause the transpilation process to break:
![webpack failure missing loader for css/style](../assets/7e526fe9214225fd.png)
When using CSS, we have to use

```
{
  rules: [
    {
      test: /\.js$/,
      loader: 'babel-loader',
      options: {
        presets: ['@babel/preset-react', '@babel/preset-env'],
      },
    },
    {      test: /\.css$/,      use: ['style-loader', 'css-loader'],    },  ],
}
```

The job of the _CSS_ files and the job of the _style_ element that contains all of the styles of the application.
With this configuration, the CSS definitions are included in the _main.js_ file of the application. For this reason, there is no need to separately import the _CSS_ styles in the main _index.html_ file.
If needed, the application's CSS can also be generated into its own separate file, by using the
When we install the loaders:

```
npm install style-loader css-loader --save-dev
```

The bundling will succeed once again and the application gets new styles.
### Webpack-dev-server
The current configuration makes it possible to develop our application but the workflow is awful (to the point where it resembles the development workflow with Java). Every time we make a change to the code, we have to bundle it and refresh the browser to test it.
The

```
npm install --save-dev webpack-dev-server
```

Let's define an npm script for starting the dev server:

```
{
  // ...
  "scripts": {
    "build": "webpack --mode=development",
    "start": "webpack serve --mode=development"  },
  // ...
}
```

Let's also add a new _devServer_ property to the configuration object in the _webpack.config.js_ file:

```
const config = {
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname, 'build'),
    filename: 'main.js',
  },
  devServer: {    static: path.resolve(__dirname, 'build'),    compress: true,    port: 3000,  },  // ...
};
```

The _npm start_ command will now start the dev-server at port 3000, meaning that our application will be available by visiting
The process for updating the code is fast. When we use the dev-server, the code is not bundled the usual way into the _main.js_ file. The result of the bundling exists only in memory.
Let's extend the code by changing the definition of the _App_ component as shown below:

```
import React, { useState } from 'react'
import './index.css'

const App = () => {
  const [counter, setCounter] = useState(0)

  return (
    <div className="container">
      hello webpack {counter} clicks
      <button onClick={() => setCounter(counter + 1)}>
        press
      </button>
    </div>
  )
}

export default App
```

The application works nicely and the development workflow is quite smooth.
### Source maps
Let's extract the click handler into its own function and store the previous value of the counter in its own _values_ state:

```
const App = () => {
  const [counter, setCounter] = useState(0)
  const [values, setValues] = useState()
  const handleClick = () => {    setCounter(counter + 1)    setValues(values.concat(counter))  }
  return (
    <div className="container">
      hello webpack {counter} clicks
      <button onClick={handleClick}>        press
      </button>
    </div>
  )
}
```

The application no longer works and the console will display the following error:
![devtools console cannot concat on undefined in handleClick](../assets/4c9e6196fbefe6d4.png)
We know that the error is in the onClick method, but if the application was any larger the error message would be quite difficult to track down:

```
App.js:27 Uncaught TypeError: Cannot read property 'concat' of undefined
    at handleClick (App.js:27)
```

The location of the error indicated in the message does not match the actual location of the error in our source code. If we click the error message, we notice that the displayed source code does not resemble our application code:
![devtools source does not show our source code](../assets/369a96c61dddfdc9.png)
Of course, we want to see our actual source code in the error message.
Luckily, fixing this error message is quite easy. We will ask webpack to generate a so-called _map errors_ that occur during the execution of the bundle to the corresponding part in the original source code.
The source map can be generated by adding a new _devtool_ property to the configuration object with the value 'source-map':

```
const config = {
  entry: './src/index.js',
  output: {
    // ...
  },
  devServer: {
    // ...
  },
  devtool: 'source-map',  // ..
};
```

Webpack has to be restarted when we make changes to its configuration. It is also possible to make webpack watch for changes made to itself, but we will not do that this time.
The error message is now a lot better
![devtools console showing concat error at different line](../assets/315f67e8dd4fe4ec.png)
since it refers to the code we wrote:
![devtools source showing our actual code with values.concat](../assets/683b4353d067abf1.png)
Generating the source map also makes it possible to use the Chrome debugger:
![devtools debugger paused just before offending line](../assets/ab657b73eb89a190.png)
Let's fix the bug by initializing the state of _values_ as an empty array:

```
const App = () => {
  const [counter, setCounter] = useState(0)
  const [values, setValues] = useState([])
  // ...
}
```

### Minifying the code
When we deploy the application to production, we are using the _main.js_ code bundle that is generated by webpack. The size of the _main.js_ file is 1009487 bytes even though our application only contains a few lines of our code. The large file size is because the bundle also contains the source code for the entire React library. The size of the bundled code matters since the browser has to load the code when the application is first used. With high-speed internet connections, 1009487 bytes is not an issue, but if we were to keep adding more external dependencies, loading speeds could become an issue, particularly for mobile users.
If we inspect the contents of the bundle file, we notice that it could be greatly optimized in terms of file size by removing all of the comments. There's no point in manually optimizing these files, as there are many existing tools for the job.
The optimization process for JavaScript files is called _minification_. One of the leading tools intended for this purpose is
Starting from version 4 of webpack, the minification plugin does not require additional configuration to be used. It is enough to modify the npm script in the _package.json_ file to specify that webpack will execute the bundling of the code in _production_ mode:

```
{
  "name": "webpack-part7",
  "version": "0.0.1",
  "description": "practicing webpack",
  "scripts": {
    "build": "webpack --mode=production",    "start": "webpack serve --mode=development"
  },
  "license": "MIT",
  "dependencies": {
    // ...
  },
  "devDependencies": {
    // ...
  }
}
```

When we bundle the application again, the size of the resulting _main.js_ decreases substantially:

```
$ ls -l build/main.js
-rw-r--r--  1 mluukkai  ATKK\hyad-all  227651 Feb  7 15:58 build/main.js
```

The output of the minification process resembles old-school C code; all of the comments and even unnecessary whitespace and newline characters have been removed, variable names have been replaced with a single character.

```
function h(){if(!d){var e=u(p);d=!0;for(var t=c.length;t;){for(s=c,c=[];++f<t;)s&&s[f].run();f=-1,t=c.length}s=null,d=!1,function(e){if(o===clearTimeout)return clearTimeout(e);if((o===l||!o)&&clearTimeout)return o=clearTimeout,clearTimeout(e);try{o(e)}catch(t){try{return o.call(null,e)}catch(t){return o.call(this,e)}}}(e)}}a.nextTick=function(e){var t=new Array(arguments.length-1);if(arguments.length>1)
```

### Development and production configuration
Next, let's add a backend to our application by repurposing the now-familiar note application backend.
Let's store the following content in the _db.json_ file:

```
{
  "notes": [
    {
      "important": true,
      "content": "HTML is easy",
      "id": "5a3b8481bb01f9cb00ccb4a9"
    },
    {
      "important": false,
      "content": "Mongo can save js objects",
      "id": "5a3b920a61e8c8d3f484bdd0"
    }
  ]
}
```

Our goal is to configure the application with webpack in such a way that, when used locally, the application uses the json-server available in port 3001 as its backend.
The bundled file will then be configured to use the backend available at the
We will install _axios_ , start the json-server, and then make the necessary changes to the application. For the sake of changing things up, we will fetch the notes from the backend with our [custom hook](../part7/01-custom-hooks.md) called _useNotes_ :

```
import React, { useState, useEffect } from 'react'import axios from 'axios'const useNotes = (url) => {  const [notes, setNotes] = useState([])  useEffect(() => {    axios.get(url).then(response => {      setNotes(response.data)    })  }, [url])  return notes}
const App = () => {
  const [counter, setCounter] = useState(0)
  const [values, setValues] = useState([])
  const url = 'https://notes2023.fly.dev/api/notes'  const notes = useNotes(url)
  const handleClick = () => {
    setCounter(counter + 1)
    setValues(values.concat(counter))
  }

  return (
    <div className="container">
      hello webpack {counter} clicks
      <button onClick={handleClick}>press</button>
      <div>{notes.length} notes on server {url}</div>    </div>
  )
}

export default App
```

The address of the backend server is currently hardcoded in the application code. How can we change the address in a controlled fashion to point to the production backend server when the code is bundled for production?
Webpack's configuration function has two parameters, _env_ and _argv_. We can use the latter to find out the _mode_ defined in the npm script:

```
const path = require('path')

const config = (env, argv) => {  console.log('argv.mode:', argv.mode)
  return {
    // ...
  }
}

module.exports = config
```

Now, if we want, we can set Webpack to work differently depending on whether the application's operating environment, or _mode_ , is set to production or development.
We can also use webpack's _global default constants_ that can be used in the bundled code. Let's define a new global constant _BACKEND_URL_ that gets a different value depending on the environment that the code is being bundled for:

```
const path = require('path')
const webpack = require('webpack')
const config = (env, argv) => {
  console.log('argv', argv.mode)

  const backend_url = argv.mode === 'production'    ? 'https://notes2023.fly.dev/api/notes'    : 'http://localhost:3001/notes'
  return {
    entry: './src/index.js',
    output: {
      path: path.resolve(__dirname, 'build'),
      filename: 'main.js'
    },
    devServer: {
      static: path.resolve(__dirname, 'build'),
      compress: true,
      port: 3000,
    },
    devtool: 'source-map',
    module: {
      // ...
    },
    plugins: [      new webpack.DefinePlugin({        BACKEND_URL: JSON.stringify(backend_url)      })    ]  }
}

module.exports = config
```

The global constant is used in the following way in the code:

```
const App = () => {
  const [counter, setCounter] = useState(0)
  const [values, setValues] = useState([])
  const notes = useNotes(BACKEND_URL)
  // ...
  return (
    <div className="container">
      hello webpack {counter} clicks
      <button onClick={handleClick} >press</button>
      <div>{notes.length} notes on server {BACKEND_URL}</div>    </div>
  )
}
```

If the configuration for development and production differs a lot, it may be a good idea to
Now, if the application is started with the command _npm start_ in development mode, it fetches the notes from the address _npm run build_ uses the address
We can inspect the bundled production version of the application locally by executing the following command in the _build_ directory:

```
npx static-server
```

By default, the bundled application will be available at
### Polyfill
Our application is finished and works with all relatively recent versions of modern browsers, except for Internet Explorer. The reason for this is that, because of _axios_ , our code uses
![browser compatibility chart highlighting how bad internet explorer is](../assets/be729f3574160551.png)
There are many other things in the standard that IE does not support. Something as harmless as the
![browser compatibility chart showing IE does not support find method](../assets/6b1824168c62a0e6.png)
In these situations, it is not enough to transpile the code, as transpilation simply transforms the code from a newer version of JavaScript to an older one with wider browser support. IE understands Promises syntactically but it simply has not implemented their functionality. The _find_ property of arrays in IE is simply _undefined_.
If we want the application to be IE-compatible, we need to add a
Polyfills can be added with the help of
The polyfill provided by the

```
import PromisePolyfill from 'promise-polyfill'

if (!window.Promise) {
  window.Promise = PromisePolyfill
}
```

If the global _Promise_ object does not exist, meaning that the browser does not support Promises, the polyfilled Promise is stored in the global variable. If the polyfilled Promise is implemented well enough, the rest of the code should work without issues.
One exhaustive list of existing polyfills can be found
The browser compatibility of different APIs can be checked by visiting
[Part 7c **Previous part**](../part7/01-more-about-styles.md)[Part 7e **Next part**](../part7/01-class-components-miscellaneous.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)
