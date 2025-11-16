---{
  "title": "Deploying app to internet",
  "source_url": "https://fullstackopen.com/en/part3/deploying_app_to_internet",
  "crawl_timestamp": "2025-10-04T19:16:15Z",
  "checksum": "6c8b6c065293b04528bd68b2e7e2a51b51ef597b94976bf99d408ad09c4e4547"
}
---[Skip to content](../part3/01-deploying-app-to-internet-course-main-content.md)
[{() => fs}](https://fullstackopen.com/en/)

- [About course](../about/01-about.md)
- [Course contents](../#course-contents/01-course-contents.md)
- [FAQ](../faq/01-faq.md)
- [Partners](../companies/01-companies.md)
- [Challenge](../challenge/01-challenge.md)
[Search from the material](../search/01-search.md)Toggle dark theme
Select languageSuomi English 中文 Español Français Português(BR)

[Fullstack](../#course-contents/01-course-contents.md)
[Part 3](../part3/01-part3.md)
Deploying app to internet
[a Node.js and Express](../part3/01-node-js-and-express.md)
b Deploying app to internet

- [Same origin policy and CORS](../part3/01-deploying-app-to-internet-same-origin-policy-and-cors.md)
- [Application to the Internet](../part3/01-deploying-app-to-internet-application-to-the-internet.md)
- [Frontend production build](../part3/01-deploying-app-to-internet-frontend-production-build.md)
- [Serving static files from the backend](../part3/01-deploying-app-to-internet-serving-static-files-from-the-backend.md)
- [The whole app to the internet](../part3/01-deploying-app-to-internet-the-whole-app-to-the-internet.md)
- [Streamlining deploying of the frontend](../part3/01-deploying-app-to-internet-streamlining-deploying-of-the-frontend.md)
- [Proxy](../part3/01-deploying-app-to-internet-proxy.md)
- [Exercises 3.9.-3.11](../part3/01-deploying-app-to-internet-exercises-3-9-3-11.md)


[c Saving data to MongoDB](../part3/01-saving-data-to-mongo-db.md)[d Validation and ESLint](../part3/01-validation-and-es-lint.md)
b
# Deploying app to internet
Next, let's connect the frontend we made in [part 2](../part2/01-part2.md) to our own backend.
In the previous part, the frontend could ask for the list of notes from the json-server we had as a backend, from the address **baseUrl** in the frontend notes app at _src/services/notes.js_ like so:

```
import axios from 'axios'
const baseUrl = 'http://localhost:3001/api/notes'
const getAll = () => {
  const request = axios.get(baseUrl)
  return request.then(response => response.data)
}

// ...

export default { getAll, create, update }copy
```

Now frontend's GET request to
![Get request showing error in dev tools](../assets/ddf1e62f43cde44e.png)
What's going on here? We can access the backend from a browser and from postman without any problems.
### Same origin policy and CORS
The issue lies with a thing called _same origin policy_. A URL's origin is defined by the combination of protocol (AKA scheme), hostname, and port.

```
http://example.com:80/index.html
  
protocol: http
host: example.com
port: 80copy
```

When you visit a website (e.g. _example.com_ is hosted on or a different website. When the browser sees reference(s) to a URL in the source HTML, it issues a request. If the request is issued using the URL that the source HTML was fetched from, then the browser processes the response without any issues. However, if the resource is fetched using a URL that doesn't share the same origin(scheme, host, port) as the source HTML, the browser will have to check the _Access-Control-Allow-origin_ response header. If it contains _*_ on the URL of the source HTML, the browser will process the response, otherwise the browser will refuse to process it and throws an error.
The **same-origin policy** is a security mechanism implemented by browsers in order to prevent session hijacking among other security vulnerabilities.
In order to enable legitimate cross-origin requests (requests to URLs that don't share the same origin) W3C came up with a mechanism called **CORS**(Cross-Origin Resource Sharing). According to
> _Cross-origin resource sharing (CORS) is a mechanism that allows restricted resources (e.g. fonts) on a web page to be requested from another domain outside the domain from which the first resource was served. A web page may freely embed cross-origin images, stylesheets, scripts, iframes, and videos. Certain "cross-domain" requests, notably Ajax requests, are forbidden by default by the same-origin security policy._
The problem is that, by default, the JavaScript code of an application that runs in a browser can only communicate with a server in the same
Keep in mind, that
We can allow requests from other _origins_ by using Node's
In your backend repository, install _cors_ with the command

```
npm install corscopy
```

take the middleware to use and allow for requests from all origins:

```
const cors = require('cors')

app.use(cors())copy
```

**Note:** When you are enabling cors, you should think about how you want to configure it. In the case of our application, since the backend is not expected to be visible to the public in the production environment, it may make more sense to only enable cors from a specific origin (e.g. the front end).
Now most of the features in the frontend work! The functionality for changing the importance of notes has not yet been implemented on the backend so naturally that does not yet work in the frontend. We shall fix that later.
You can read more about CORS from
The setup of our app now looks as follows:
![diagram of react app and browser](../assets/268ef57c0921a59a.png)
The react app running in the browser now fetches the data from node/express-server that runs in localhost:3001.
### Application to the Internet
Now that the whole stack is ready, let's move our application to Internet.
There is an ever-growing number of services that can be used to host an app on the internet. The developer-friendly services like PaaS (i.e. Platform as a Service) take care of installing the execution environment (eg. Node.js) and could also provide various services such as databases.
For a decade,
We are now introducing two services
There are also some other free hosting options that work well for this course, at least for all parts other than part 11 (CI/CD) which might have one tricky exercise for other platforms.
Some course participants have also used the following services:
If you know easy-to-use and free services for hosting NodeJS, please let us know!
For both Fly.io and Render, we need to change the definition of the port our application uses at the bottom of the _index.js_ file in the backend like so:

```
const PORT = process.env.PORT || 3001app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`)
})copy
```

Now we are using the port defined in the _PORT_ or port 3001 if the environment variable _PORT_ is undefined. It is possible to configure the application port based on the environment variable both in Fly.io and in Render.
#### Fly.io
_Note that you may need to give your credit card number to Fly.io!_
If you decide to use
Start by

```
fly auth logincopy
```

Note if the command _fly_ does not work on your machine, you can try the longer version _flyctl_. Eg. on MacOS, both forms of the command work.
_If you do not get the flyctl to work in your machine, you could try Render (see next section), it does not require anything to be installed in your machine._
Initializing an app happens by running the following command in the root directory of the app

```
fly launch --no-deploycopy
```

Give the app a name or let Fly.io auto-generate one. Pick a region where the app will be run. Do not create a Postgres database for the app and do not create an Upstash Redis database, since these are not needed.
Fly.io creates a file _fly.toml_ in the root of your app where we can configure it. To get the app up and running we _might_ need to do a small addition to the configuration:

```
[build]

[env]
  PORT = "3001" # add this

[http_service]
  internal_port = 3001 # ensure that this is same as PORT
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  processes = ["app"]copy
```

We have now defined in the part [env] that environment variable PORT will get the correct port (defined in part [http_service]) where the app should create the server.
We are now ready to deploy the app to the Fly.io servers. That is done with the following command:

```
fly deploycopy
```

If all goes well, the app should now be up and running. You can open it in the browser with the command

```
fly apps opencopy
```

A particularly important command is _fly logs_. This command can be used to view server logs. It is best to keep logs always visible!
**Note:** Fly may create 2 machines for your app, if it does then the state of the data in your app will be inconsistent between requests, i.e. you would have two machines each with its own notes variable, you could POST to one machine then your next GET could go to another machine. You can check the number of machines by using the command "$ fly scale show", if the COUNT is greater than 1 then you can enforce it to be 1 with the command "$ fly scale count 1". The machine count can also be checked on the dashboard.
**Note:** In some cases (the cause is so far unknown) running Fly.io commands especially on Windows WSL (Windows Subsystem for Linux) has caused problems. If the following command just hangs

```
flyctl ping -o personalcopy
```

your computer can not for some reason connect to Fly.io. If this happens to you,
If the output of the below command looks like this:

```
$ flyctl ping -o personal
35 bytes from fdaa:0:8a3d::3 (gateway), seq=0 time=65.1ms
35 bytes from fdaa:0:8a3d::3 (gateway), seq=1 time=28.5ms
35 bytes from fdaa:0:8a3d::3 (gateway), seq=2 time=29.3ms
...copy
```

then there are no connection problems!
Whenever you make changes to the application, you can take the new version to production with a command

```
fly deploycopy
```

#### Render
_Note that you may need to give your credit card number to Render!_
The following assumes that the
After signing in, let us create a new "web service":
![Image showing the option to create a new Web Service](../assets/36678b73c230c52c.png)
The app repository is then connected to Render:
![Image showing the application repository on Render.](../assets/6bd81be3035d6d87.png)
The connection seems to require that the app repository is public.
Next we will define the basic configurations. If the app is _not_ at the root of the repository the _Root directory_ needs to be given a proper value:
![image showing the Root Directory field as optional](../assets/b369ec13859263b7.png)
After this, the app starts up in the Render. The dashboard tells us the app state and the url where the app is running:
![The top left corner of the image shows the status of the application and its URL](../assets/40a7a5fc6d851f8f.png)
According to the
Fortunately, it is also possible to manually redeploy the app:
![Menu with the option to deploy latest commit highlighted](../assets/efa2fe4bf37d5436.png)
Also, the app logs can be seen in the dashboard:
![Image with the logs tab highlighted on the left corner. On the right side, the application logs](../assets/c4864302c1e42c1c.png)
We notice now from the logs that the app has been started in the port 10000. The app code gets the right port through the environment variable PORT so it is essential that the file _index.js_ has been updated in the backend as follows:

```
const PORT = process.env.PORT || 3001app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`)
})copy
```

### Frontend production build
So far we have been running React code in _development mode_. In development mode the application is configured to give clear error messages, immediately render code changes to the browser, and so on.
When the application is deployed, we must create a
A production build for applications created with Vite can be created with the command
Let's run this command from the _root of the notes frontend project_ that we developed in [Part 2](../part2/01-part2.md).
This creates a directory called _dist_ which contains the only HTML file of our application (_index.html_) and the directory _assets_. _dist_ directory. Even though the application code is in multiple files, all of the JavaScript will be minified into one file. All of the code from all of the application's dependencies will also be minified into this single file.
The minified code is not very readable. The beginning of the code looks like this:

```
!function(e){function r(r){for(var n,f,i=r[0],l=r[1],a=r[2],c=0,s=[];c<i.length;c++)f=i[c],o[f]&&s.push(o[f][0]),o[f]=0;for(n in l)Object.prototype.hasOwnProperty.call(l,n)&&(e[n]=l[n]);for(p&&p(r);s.length;)s.shift()();return u.push.apply(u,a||[]),t()}function t(){for(var e,r=0;r<u.length;r++){for(var t=u[r],n=!0,i=1;i<t.length;i++){var l=t[i];0!==o[l]&&(n=!1)}n&&(u.splice(r--,1),e=f(f.s=t[0]))}return e}var n={},o={2:0},u=[];function f(r){if(n[r])return n[r].exports;var t=n[r]={i:r,l:!1,exports:{}};return e[r].call(t.exports,t,t.exports,f),t.l=!0,t.exports}f.m=e,f.c=n,f.d=function(e,r,t){f.o(e,r)||Object.defineProperty(e,r,{enumerable:!0,get:t})},f.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"})copy
```

### Serving static files from the backend
One option for deploying the frontend is to copy the production build (the _dist_ directory) to the root of the backend directory and configure the backend to show the frontend's _main page_ (the file _dist/index.html_) as its main page.
We begin by copying the production build of the frontend to the root of the backend. With a Mac or Linux computer, the copying can be done from the frontend directory with the command

```
cp -r dist ../backendcopy
```

If you are using a Windows computer, you may use either
The backend directory should now look as follows:
![bash screenshot of ls showing dist directory](../assets/81a874a9f47c7659.png)
To make Express show _static content_ , the page _index.html_ and the JavaScript, etc., it fetches, we need a built-in middleware from Express called
When we add the following amidst the declarations of middlewares

```
app.use(express.static('dist'))copy
```

whenever Express gets an HTTP GET request it will first check if the _dist_ directory contains a file corresponding to the request's address. If a correct file is found, Express will return it.
Now HTTP GET requests to the address _www.serversaddress.com/index.html_ or _www.serversaddress.com_ will show the React frontend. GET requests to the address _www.serversaddress.com/api/notes_ will be handled by the backend code.
Because of our situation, both the frontend and the backend are at the same address, we can declare _baseUrl_ as a

```
import axios from 'axios'
const baseUrl = '/api/notes'
const getAll = () => {
  const request = axios.get(baseUrl)
  return request.then(response => response.data)
}

// ...copy
```

After the change, we have to create a new production build of the frontend and copy it to the root of the backend directory.
The application can now be used from the _backend_ address
![Notes application in localhost:3001](../assets/effe1c10404af403.png)
Our application now works exactly like the [single-page app](../part0/01-fundamentals-of-web-apps-single-page-app.md) example application we studied in part 0.
When we use a browser to go to the address _index.html_ file from the _dist_ directory. The contents of the file are as follows:

```
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Vite + React</title>
    <script type="module" crossorigin src="/assets/index-5f6faa37.js"></script>
    <link rel="stylesheet" href="/assets/index-198af077.css">
  </head>
  <body>
    <div id="root"></div>
    
  </body>
</html>copy
```

The file contains instructions to fetch a CSS stylesheet defining the styles of the application, and one _script_ tag that instructs the browser to fetch the JavaScript code of the application - the actual React application.
The React code fetches notes from the server address _Network_ tab of the developer console:
![Network tab of notes application on backend](../assets/5a3be519aab1e7c9.png)
The setup that is ready for a product deployment looks as follows:
![diagram of deployment ready react app](../assets/ad31591aa1800a01.png)
Unlike when running the app in a development environment, everything is now in the same node/express-backend that runs in localhost:3001. When the browser goes to the page, the file _index.html_ is rendered. That causes the browser to fetch the production version of the React app. Once it starts to run, it fetches the json-data from the address localhost:3001/api/notes.
### The whole app to the internet
After ensuring that the production version of the application works locally, we are ready to move the whole application to the selected host service.
**In the case of Fly.io** the new deployment is done with the command

```
fly deploycopy
```

**NOTE:** The _.dockerignore_ file in your project directory lists files not uploaded during deployment. The dist directory may be included by default. If that's the case, remove its reference from the .dockerignore file, ensuring your app is properly deployed.
**In the case of Render** , commit the changes, and push the code to GitHub again. Make sure the directory _dist_ is not ignored by git on the backend. A push to GitHub _might_ be enough. If the automatic deployment does not work, select the "manual deploy" from the Render dashboard.
The application works perfectly, except we haven't added the functionality for changing the importance of a note to the backend yet.
![screenshot of notes application](../assets/9fadc54cfb0a3d29.png)
_**NOTE:** changing the importance DOES NOT work yet since the backend has no implementation for it yet._
Our application saves the notes to a variable. If the application crashes or is restarted, all of the data will disappear.
The application needs a database. Before we introduce one, let's go through a few things.
The setup now looks like as follows:
![diagram of react app on fly.io](../assets/3d1d38cb77956c94.png)
The node/express-backend now resides in the Fly.io/Render server. When the root address is accessed, the browser loads and executes the React app that fetches the json-data from the Fly.io/Render server.
### Streamlining deploying of the frontend
To create a new production build of the frontend without extra manual work, let's add some npm-scripts to the _package.json_ of the backend repository.
#### Fly.io script
The scripts look like this:

```
{
  "scripts": {
    // ...
    "build:ui": "rm -rf dist && cd ../notes-frontend/ && npm run build && cp -r dist ../notes-backend",
    "deploy": "fly deploy",
    "deploy:full": "npm run build:ui && npm run deploy",    
    "logs:prod": "fly logs"
  }
}copy
```

The script _npm run build:ui_ builds the frontend and copies the production version under the backend repository. The script _npm run deploy_ releases the current backend to Fly.io.
_npm run deploy:full_ combines these two scripts, i.e., _npm run build:ui_ and _npm run deploy_.
There is also a script _npm run logs:prod_ to show the Fly.io logs.
Note that the directory paths in the script _build:ui_ depend on the location of the frontend and backend directories in the file system.
##### Note for Windows users
Note that the standard shell commands in `build:ui` do not natively work in Windows. Powershell in Windows works differently, in which case the script could be written as

```
"build:ui": "@powershell Remove-Item -Recurse -Force dist && cd ../frontend && npm run build && @powershell Copy-Item dist -Recurse ../backend",copy
```

If the script does not work on Windows, confirm that you are using Powershell and not Command Prompt. If you have installed Git Bash or another Linux-like terminal, you may be able to run Linux-like commands on Windows as well.
#### Render
Note: When you attempt to deploy your backend to Render, make sure you have a separate repository for the backend and deploy that github repo through Render, attempting to deploy through your Fullstackopen repository will often throw "ERR path ....package.json".
In case of Render, the scripts look like the following

```
{
  "scripts": {
    //...
    "build:ui": "rm -rf dist && cd ../frontend && npm run build && cp -r dist ../backend",
    "deploy:full": "npm run build:ui && git add . && git commit -m uibuild && git push"
  }
}copy
```

The script _npm run build:ui_ builds the frontend and copies the production version under the backend repository. _npm run deploy:full_ contains also the necessary _git_ commands to update the backend repository.
Note that the directory paths in the script _build:ui_ depend on the location of the frontend and backend directories in the file system.
> **NB** On Windows, npm scripts are executed in cmd.exe as the default shell which does not support bash commands. For the above bash commands to work, you can change the default shell to Bash (in the default Git for Windows installation) as follows:

```
npm config set script-shell "C:\\Program Files\\git\\bin\\bash.exe"copy
```

Another option is the use of
### Proxy
Changes on the frontend have caused it to no longer work in development mode (when started with command _npm run dev_), as the connection to the backend does not work.
![Network dev tools showing a 404 on getting notes](../assets/6bca6dca6b930c89.png)
This is due to changing the backend address to a relative URL:

```
const baseUrl = '/api/notes'copy
```

Because in development mode the frontend is at the address _localhost:5173_ , the requests to the backend go to the wrong address _localhost:5173/api/notes_. The backend is at _localhost:3001_.
If the project was created with Vite, this problem is easy to solve. It is enough to add the following declaration to the _vite.config.js_ file of the frontend directory.

```
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {    proxy: {      '/api': {        target: 'http://localhost:3001',        changeOrigin: true,      },    }  },})copy
```

After restarting, the React development environment will act as
Now the frontend is also working correctly. It functions both in development mode and in production mode together with the server. Since from the frontend's perspective all requests are made to _index.js_ file and remove _cors_ from the project's dependencies:

```
npm remove corscopy
```

We have now successfully deployed the entire application to the internet. There are many other ways to implement deployments. For example, deploying the frontend code as its own application may be sensible in some situations, as it can facilitate the implementation of an automated [part 11](../part11/01-part11.md) of the course.
The current backend code can be found on _part3-3_. The changes in frontend code are in _part3-1_ branch of the
### Exercises 3.9.-3.11
The following exercises don't require many lines of code. They can however be challenging, because you must understand exactly what is happening and where, and the configurations must be just right.
#### 3.9 Phonebook backend step 9
Make the backend work with the phonebook frontend from the exercises of the previous part. Do not implement the functionality for making changes to the phone numbers yet, that will be implemented in exercise 3.17.
You will probably have to do some small changes to the frontend, at least to the URLs for the backend. Remember to keep the developer console open in your browser. If some HTTP requests fail, you should check from the _Network_ -tab what is going on. Keep an eye on the backend's console as well. If you did not do the previous exercise, it is worth it to print the request data or _request.body_ to the console in the event handler responsible for POST requests.
#### 3.10 Phonebook backend step 10
Deploy the backend to the internet, for example to Fly.io or Render. If you are using Fly.io the commands should be run in the root directory of the backend (that is, in the same directory where the backend package.json is).
**PRO TIP:** When you deploy your application to Internet, it is worth it to at least in the beginning keep an eye on the logs of the application **AT ALL TIMES**.
Test the deployed backend with a browser and Postman or VS Code REST client to ensure it works.
Create a README.md at the root of your repository, and add a link to your online application to it.
#### 3.11 Full Stack Phonebook
Generate a production build of your frontend, and add it to the Internet application using the method introduced in this part.
Also, make sure that the frontend still works locally (in development mode when started with command _npm run dev_).
If you use Render, make sure the directory _dist_ is not ignored by git on the backend.
**NOTE:** You shall NOT be deploying the frontend directly at any stage of this part. Only the backend repository is deployed throughout the whole part. The frontend production build is added to the backend repository, and the backend serves it as described in the section [Serving static files from the backend](../part3/01-deploying-app-to-internet-serving-static-files-from-the-backend.md).
[Part 3a **Previous part**](../part3/01-node-js-and-express.md)[Part 3c **Next part**](../part3/01-saving-data-to-mongo-db.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)
