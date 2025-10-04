---{
  "title": "Introduction to React Native",
  "source_url": "https://fullstackopen.com/en/part10/introduction_to_react_native",
  "crawl_timestamp": "2025-10-04T19:15:30Z",
  "checksum": "3065397d44c9c55e40fc40f10eb6e46bbdd5e0d81029761f425914dd48d2bcbe"
}
---[Skip to content](../part10/01-introduction-to-react-native-course-main-content.md)
[{() => fs}](https://fullstackopen.com/en/)
  * [About course](../about/01-about.md)
  * [Course contents](../#course-contents/01-course-contents.md)
  * [FAQ](../faq/01-faq.md)
  * [Partners](../companies/01-companies.md)
  * [Challenge](../challenge/01-challenge.md)
[Search from the material](../search/01-search.md)Toggle dark theme
Select languageSuomi English 中文 Español Français Português(BR) 

[Fullstack](../#course-contents/01-course-contents.md)
[Part 10](../part10/01-part10.md)
Introduction to React Native
a Introduction to React Native
  * [About this part](../part10/01-introduction-to-react-native-about-this-part.md)
  * [Submitting exercises and earning credits](../part10/01-introduction-to-react-native-submitting-exercises-and-earning-credits.md)
  * [Initializing the application](../part10/01-introduction-to-react-native-initializing-the-application.md)
  * [Setting up the development environment](../part10/01-introduction-to-react-native-setting-up-the-development-environment.md)
  * [Exercise 10.1](../part10/01-introduction-to-react-native-exercise-10-1.md)
  * [ESLint](../part10/01-introduction-to-react-native-es-lint.md)
  * [Exercise 10.2](../part10/01-introduction-to-react-native-exercise-10-2.md)
  * [Debugging](../part10/01-introduction-to-react-native-debugging.md)


[b React Native basics](../part10/01-react-native-basics.md)[c Communicating with server](../part10/01-communicating-with-server.md)[d Testing and extending our application](../part10/01-testing-and-extending-our-application.md)
a
# Introduction to React Native
Traditionally, developing native iOS and Android applications has required the developer to use platform-specific programming languages and development environments. For iOS development, this means using Objective C or Swift and for Android development using JVM-based languages such as Java, Scala or Kotlin. Releasing an application for both these platforms technically requires developing two separate applications with different programming languages. This requires lots of development resources.
One of the popular approaches to unify the platform-specific development has been to utilize the browser as the rendering engine. 
The speed of development and gentle learning curve for developers familiar with React is one of the most important benefits of React Native. Here's a motivational quote from Coinbase's article 
> _If we were to reduce the benefits of React Native to a single word, it would be “velocity”. On average, our team was able to onboard engineers in less time, share more code (which we expect will lead to future productivity boosts), and ultimately deliver features faster than if we had taken a purely native approach._
### About this part
During this part, we will learn how to build an actual React Native application from the bottom up. We will learn concepts such as what are React Native's core components, how to create beautiful user interfaces, how to communicate with a server and how to test a React Native application.
We will be developing an application for rating 
![Application preview](../assets/015e30dc7aab7b18.png)
All the exercises in this part have to be submitted into _a single GitHub repository_ which will eventually contain the entire source code of your application. There will be model solutions available for each section of this part which you can use to fill in incomplete submissions. This part is structured based on the idea that you develop your application as you progress in the material. So _do not_ wait until the exercises to start the development. Instead, develop your application at the same pace as the material progresses.
This part will heavily rely on concepts covered in the previous parts. Before starting this part you will need basic knowledge of JavaScript, React and GraphQL. Deep knowledge of server-side development is not required and all the server-side code is provided for you. However, we will be making network requests from your React Native applications, for example, using GraphQL queries. The recommended parts to complete before this part are [part 1](../part1/01-part1.md), [part 2](../part2/01-part2.md), [part 5](../part5/01-part5.md), [part 7](../part7/01-part7.md) and [part 8](../part8/01-part8.md).
### Submitting exercises and earning credits
Exercises are submitted via the _to a different course instance_ than in parts 0-9. Parts 1-4 in the submission system refer to sections a-d in this part. This means that you will be submitting exercises a single section at a time starting with this section, "Introduction to React Native", which is part 1 in the submission system.
During this part, you will earn credits based on the number of exercises you complete. Completing _at least 25 exercises_ in this part will earn you _2 credits_. Once you have completed the exercises and want to get the credits, let us know through the exercise submission system that you have completed the course:
![Submitting exercises for credits](../assets/14f7f4dcc3ce17a9.png)
**Note** that you need a registration to the corresponding course part for getting the credits registered, see [here](../part0/01-general-info-parts-and-completion.md) for more information.
You can download the certificate for completing this part by clicking one of the flag icons. The flag icon corresponds to the certificate's language. Note that you must have completed at least one credit worth of exercises before you can download the certificate.
### Initializing the application
To get started with our application we need to set up our development environment. We have learned from previous parts that there are useful tools for setting up React applications quickly such as Create React App. Luckily React Native has these kinds of tools as well.
For the development of our application, we will be using _create-expo-app_ :
```
npx create-expo-app rate-repository-app --template expo-template-blank@sdk-50copy
```

Note, that the _@sdk-50_ sets the project's _Expo SDK version to 50_ , which supports _React Native version 0.73_. Using other Expo SDK versions might cause you trouble while following this material. Also, Expo has a 
Next, let's navigate to the created _rate-repository-app_ directory with the terminal and install a few dependencies we'll be needing soon:
```
npx expo install react-native-web@~0.19.6 react-dom@18.2.0 @expo/metro-runtime@~3.1.1copy
```

Now that our application has been initialized, open the created _rate-repository-app_ directory with an editor such as 
![Project structure](../assets/172b30a06182ca58.png)
We might spot some familiar files and directories such as _package.json_ and _node_modules_. On top of those, the most relevant files are the _app.json_ file which contains Expo-related configuration and _App.js_ which is the root component of our application. _Do not_ rename or move the _App.js_ file because by default Expo imports it to 
Let's look at the _scripts_ section of the _package.json_ file which has the following scripts:
```
{
  // ...
  "scripts": {
    "start": "expo start",
    "android": "expo start --android",
    "ios": "expo start --ios",
    "web": "expo start --web"
  },
  // ...
}copy
```

Let us now run the script _npm start_
![metro bundler console output](../assets/f6bdbe5a17b44a33.png)
> _If the script fails with error_ _the problem is most likely your Node version. In case of problems, switch to version _20_. _
The script starts the 
Expo command-line interface suggests a few ways to open our application. Let's press the "w" key in the terminal window to open the application in a browser. We should soon see the text defined in the _App.js_ file in a browser window. Open the _App.js_ file with an editor and make a small change to the text in the _Text_ component. After saving the file you should be able to see that the changes you have made in the code are visible in the browser window after refresh the web page.
### Setting up the development environment
We have had the first glance of our application using the Expo's browser view. Although the browser view is quite usable, it is still a quite poor simulation of the native environment. Let's have a look at the alternatives we have regarding the development environment.
Android and iOS devices such as tablets and phones can be emulated in computers using specific _emulators_. This is very useful for developing native applications. macOS users can use both Android and iOS emulators with their computers. Users of other operating systems such as Linux or Windows have to settle for Android emulators. Next, depending on your operating system follow one of these instructions on setting up an emulator:
After you have set up the emulator and it is running, start the Expo development tools as we did before, by running _npm start_. Depending on the emulator you are running either press the corresponding key for the "open Android" or "open iOS simulator". After pressing the key, Expo should connect to the emulator and you should eventually see the application in your emulator. Be patient, this might take a while.
In addition to emulators, there is one extremely useful way to develop React Native applications with Expo, the Expo mobile app. With the Expo mobile app, you can preview your application using your actual mobile device, which provides a bit more concrete development experience compared to emulators. To get started, install the Expo mobile app by following the instructions in the _the same local network_ (e.g. connected to the same Wi-Fi network) as the computer you are using for development.
When the Expo mobile app has finished installing, open it up. Next, if the Expo development tools are not already running, start them by running _npm start_. You should be able to see a QR code at the beginning of the command output. Open the app by scanning the QR code, in Android with Expo app or in iOS with the Camera app. The Expo mobile app should start building the JavaScript bundle and after it is finished you should be able to see your application. Now, every time you want to reopen your application in the Expo mobile app, you should be able to access the application without scanning the QR code by pressing it in the _Recently opened_ list in the _Projects_ view.
### Exercise 10.1
#### Exercise 10.1: initializing the application
Initialize your application with Expo command-line interface and set up the development environment either using an emulator or Expo's mobile app. It is recommended to try both and find out which development environment is the most suitable for you. The name of the application is not that relevant. You can, for example, go with _rate-repository-app_.
To submit this exercise and all future exercises you need to _expo init_. If you decide to create a private repository, add GitHub user 
Now that the repository is created, run _git init_ within your application's root directory to make sure that the directory is initialized as a Git repository. Next, to add the created repository as the remote run _git remote add origin git@github.com: <YOUR _GITHUB_ USERNAME>/<NAME _OF_ YOUR_REPOSITORY>.git_ (remember to replace the placeholder values in the command). Finally, just commit and push your changes into the repository and you are all done.
### ESLint
Now that we are somewhat familiar with the development environment let's enhance our development experience even further by configuring a linter. We will be using 
```
npm install --save-dev eslint @babel/eslint-parser eslint-plugin-react eslint-plugin-react-nativecopy
```

Next, let's add a _.eslintrc.json_ file in the _rate-repository-app_ directory with the ESLint configuration into the following content:
```
{
  "plugins": ["react", "react-native"],
  "settings": {
    "react": {
      "version": "detect"
    }
  },
  "extends": ["eslint:recommended", "plugin:react/recommended"],
  "parser": "@babel/eslint-parser",
  "env": {
    "react-native/react-native": true
  },
  "rules": {
    "react/prop-types": "off",
    "react/react-in-jsx-scope": "off"
  }
}copy
```

And finally, let's add a _lint_ script to the _package.json_ file to check the linting rules in specific files:
```
{
  // ...
  "scripts": {
    "start": "expo start",
    "android": "expo start --android",
    "ios": "expo start --ios",
    "web": "expo start --web",
    "lint": "eslint ./src/**/*.{js,jsx} App.js --no-error-on-unmatched-pattern"  },
  // ...
}copy
```

Now we can check that the linting rules are obeyed in JavaScript files in the _src_ directory and in the _App.js_ file by running _npm run lint_. We will be adding our future code to the _src_ directory but because we haven't added any files there yet, we need the _no-error-on-unmatched-pattern_ flag. Also if possible integrate ESLint with your editor. If you are using Visual Studio Code you can do that by, going to the extensions section and checking that the ESLint extension is installed and enabled:
![Visual Studio Code ESLint extensions](../assets/1d668636356e5848.png)
The provided ESLint configuration contains only the basis for the configuration. Feel free to improve the configuration and add new plugins if you feel like it.
### Exercise 10.2
#### Exercise 10.2: setting up the ESLint
Set up ESLint in your project so that you can perform linter checks by running _npm run lint_. To get most of linting it is also recommended to integrate ESLint with your editor.
This was the last exercise in this section. It's time to push your code to GitHub and mark all of your finished exercises to the 
### Debugging
When our application doesn't work as intended, we should immediately start _debugging_ it. In practice, this means that we'll need to reproduce the erroneous behavior and monitor the code execution to find out which part of the code behaves incorrectly. During the course, we have already done a bunch of debugging by logging messages, inspecting network traffic, and using specific development tools, such as _React Development Tools_. In general, debugging isn't that different in React Native, we'll just need the right tools for the job.
The good old console.log messages appear in the Expo development tools command line:
![GraphQL structure](../assets/5effbe2cc231d7df.png)
That might actually be enough in most cases, but sometimes we need more. React Native provides an in-app developer menu which offers several debugging options. Read more about 
To inspect the React element tree, props, and state you can install React DevTools. 
```
npx react-devtoolscopy
```

Read here about 
[ Part 9 **Previous part** ](../part9/01-part9.md)[ Part 10b **Next part** ](../part10/01-react-native-basics.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)