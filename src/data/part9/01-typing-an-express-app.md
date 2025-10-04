---{
  "title": "Typing an Express app",
  "source_url": "https://fullstackopen.com/en/part9/typing_an_express_app",
  "crawl_timestamp": "2025-10-04T19:17:28Z",
  "checksum": "66961d15b311aba475a442a127fb6f855811633767230caae208924ac51f04f2"
}
---[Skip to content](../part9/01-typing-an-express-app-course-main-content.md)
[{() => fs}](https://fullstackopen.com/en/)
  * [About course](../about/01-about.md)
  * [Course contents](../#course-contents/01-course-contents.md)
  * [FAQ](../faq/01-faq.md)
  * [Partners](../companies/01-companies.md)
  * [Challenge](../challenge/01-challenge.md)
[Search from the material](../search/01-search.md)Toggle dark theme
Select languageSuomi English 中文 Español Français Português(BR) 

A new exercise has been added at the end of Part 9 "Typing an Express app" at 28th August 2024. Because of that numbering of the Exercises 9.14- has changed.
x
[Fullstack](../#course-contents/01-course-contents.md)
[Part 9](../part9/01-part9.md)
Typing an Express app
[a Background and introduction](../part9/01-background-and-introduction.md)[b First steps with TypeScript](../part9/01-first-steps-with-type-script.md)
c Typing an Express app
  * [Setting up the project](../part9/01-typing-an-express-app-setting-up-the-project.md)
  * [Let there be code](../part9/01-typing-an-express-app-let-there-be-code.md)
  * [Exercises 9.8-9.9](../part9/01-typing-an-express-app-exercises-9-8-9-9.md)
  * [Implementing the functionality](../part9/01-typing-an-express-app-implementing-the-functionality.md)
  * [Node and JSON modules](../part9/01-typing-an-express-app-node-and-json-modules.md)
  * [Utility Types](../part9/01-typing-an-express-app-utility-types.md)
  * [Typing the request and response](../part9/01-typing-an-express-app-typing-the-request-and-response.md)
  * [Exercises 9.10-9.11](../part9/01-typing-an-express-app-exercises-9-10-9-11.md)
  * [Preventing an accidental undefined result](../part9/01-typing-an-express-app-preventing-an-accidental-undefined-result.md)
  * [Adding a new diary](../part9/01-typing-an-express-app-adding-a-new-diary.md)
  * [Validating requests](../part9/01-typing-an-express-app-validating-requests.md)
  * [Type guards](../part9/01-typing-an-express-app-type-guards.md)
  * [Enum](../part9/01-typing-an-express-app-enum.md)
  * [Exercises 9.12-9.13](../part9/01-typing-an-express-app-exercises-9-12-9-13.md)
  * [Using schema validation libraries](../part9/01-typing-an-express-app-using-schema-validation-libraries.md)
  * [Parsing request body in middleware](../part9/01-typing-an-express-app-parsing-request-body-in-middleware.md)
  * [Exercises 9.14](../part9/01-typing-an-express-app-exercises-9-14.md)


[d React with types](../part9/01-react-with-types.md)[e Grande finale: Patientor](../part9/01-grande-finale-patientor.md)
c
# Typing an Express app
Now that we have a basic understanding of how TypeScript works and how to create small projects with it, it's time to start creating something useful. We are now going to create a new project that will introduce use cases that are a little more realistic.
One major change from the previous part is that _we're not going to use ts-node anymore_. It is a handy tool that helps you get started, but in the long run, it is advisable to use the official TypeScript compiler that comes with the _typescript_ npm-package. The official compiler generates and packages JavaScript files from the .ts files so that the built _production version_ won't contain any TypeScript code anymore. This is the exact outcome we are aiming for since TypeScript itself is not executable by browsers or Node.
### Setting up the project
We will create a project for Ilari, who loves flying small planes but has a difficult time managing his flight history. He is a coder himself, so he doesn't necessarily need a user interface, but he'd like to use some custom software with HTTP requests and retain the possibility of later adding a web-based user interface to the application.
Let's start by creating our first real project: _Ilari's flight diaries_. As usual, run _npm init_ and install the _typescript_ package as a dev dependency.
```
 npm install typescript --save-devcopy
```

TypeScript's Native Compiler (_tsc_) can help us initialize our project by generating our _tsconfig.json_ file. First, we need to add the _tsc_ command to the list of executable scripts in _package.json_ (unless you have installed _typescript_ globally). Even if you installed TypeScript globally, you should always add it as a dev dependency to your project.
The npm script for running _tsc_ is set as follows:
```
{
  // ..
  "scripts": {
    "tsc": "tsc"  },
  // ..
}copy
```

The bare _tsc_ command is often added to _scripts_ so that other scripts can use it, hence don't be surprised to find it set up within the project like this.
We can now initialize our tsconfig.json settings by running:
```
 npm run tsc -- --initcopy
```

**Note** the extra _--_ before the actual argument! Arguments before _--_ are interpreted as being for the _npm_ command, while the ones after that are meant for the command that is run through the script (i.e. _tsc_ in this case).
The _tsconfig.json_ file we just created contains a lengthy list of every configuration available to us. However, most of them are commented out. Studying this file can help you find some configuration options you might need. It is also completely okay to keep the commented lines, in case you might need them someday.
At the moment, we want the following to be active:
```
{
  "compilerOptions": {
    "target": "ES6",
    "outDir": "./build/",
    "module": "commonjs",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "esModuleInterop": true
  }
}copy
```

Let's go through each configuration:
The _target_ configuration tells the compiler which _ECMAScript_ version to use when generating JavaScript. ES6 is supported by most browsers, so it is a good and safe option.
_outDir_ tells where the compiled code should be placed.
_module_ tells the compiler that we want to use _CommonJS_ modules in the compiled code. This means we can use the old _require_ syntax instead of the _import_ one, which is not supported in older versions of _Node_.
_strict_ is a shorthand for multiple separate options:
  * noImplicitAny
  * noImplicitThis
  * alwaysStrict
  * strictBindCallApply
  * strictNullChecks
  * strictFunctionTypes
  * strictPropertyInitialization


They guide our coding style to use the TypeScript features more strictly. For us, perhaps the most important is the already-familiar _any_ , which can for example happen if you don't type the parameters of a function. Details about the rest of the configurations can be found in the _strict_ is suggested by the official documentation.
  * _noUnusedLocals_ prevents having unused local variables, and _noUnusedParameters_ throws an error if a function has unused parameters.
  * _noImplicitReturns_ checks all code paths in a function to ensure they return a value.
  * _noFallthroughCasesInSwitch_ ensures that, in a _switch case_ , each case ends either with a _return_ or a _break_ statement.
  * _esModuleInterop_ allows interoperability between CommonJS and ES Modules


See more in the 
Now that we have set our configuration, we can continue by installing _express_ and, of course, also _@types/express_. Also, since this is a real project, which is intended to be grown over time, we will use ESlint from the very beginning:
```
npm install express
npm install --save-dev eslint @eslint/js typescript-eslint @stylistic/eslint-plugin @types/express @types/eslint__jscopy
```

Now our _package.json_ should look like this:
```
{
  "name": "flights",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "tsc": "tsc"
  },
  "author": "",
  "license": "ISC",
  "devDependencies": {
    "@eslint/js": "^9.8.0",
    "@stylistic/eslint-plugin": "^2.6.1",
    "@types/eslint__js": "^8.42.3",
    "@types/express": "^4.17.21",
    "eslint": "^9.8.0",
    "typescript": "^5.5.4",
    "typescript-eslint": "^8.0.0"
  },
  "dependencies": {
    "express": "^4.19.2"
  }
}copy
```

We also create a _eslint.config.mjs_ file with the following content:
```
import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
import stylistic from "@stylistic/eslint-plugin";

export default tseslint.config({
  files: ['**/*.ts'],
  extends: [
    eslint.configs.recommended,
    ...tseslint.configs.recommendedTypeChecked,
  ],
  languageOptions: {
    parserOptions: {
      project: true,
      tsconfigRootDir: import.meta.dirname,
    },
  },
  plugins: {
    "@stylistic": stylistic,
  },
  rules: {
    '@stylistic/semi': 'error',
    '@typescript-eslint/no-unsafe-assignment': 'error',
    '@typescript-eslint/no-explicit-any': 'error',
    '@typescript-eslint/explicit-function-return-type': 'off',
    '@typescript-eslint/explicit-module-boundary-types': 'off',
    '@typescript-eslint/restrict-template-expressions': 'off',
    '@typescript-eslint/restrict-plus-operands': 'off',
    '@typescript-eslint/no-unused-vars': [
      'error',
      { 'argsIgnorePattern': '^_' }
    ],
  },
});copy
```

Now we just need to set up our development environment, and we are ready to start writing some serious code. There are many different options for this. One option could be to use the familiar _nodemon_ with _ts-node_. However, as we saw earlier, _ts-node-dev_ does the same thing, so we will use that instead. So, let's install _ts-node-dev_ :
```
npm install --save-dev ts-node-devcopy
```

We finally define a few more npm scripts, and voilà, we are ready to begin:
```
{
  // ...
  "scripts": {
    "tsc": "tsc",
    "dev": "ts-node-dev index.ts",    "lint": "eslint ."  },
  // ...
}copy
```

As you can see, there is a lot of stuff to go through before beginning the actual coding. When you are working on a real project, careful preparations support your development process. Take the time needed to create a good setup for yourself and your team, so that everything runs smoothly in the long run.
### Let there be code
Now we can finally start coding! As always, we start by creating a ping endpoint, just to make sure everything is working.
The contents of the _index.ts_ file:
```
import express from 'express';
const app = express();
app.use(express.json());

const PORT = 3000;

app.get('/ping', (_req, res) => {
  console.log('someone pinged here');
  res.send('pong');
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});copy
```

Now, if we run the app with _npm run dev_ , we can verify that a request to _pong_ , so our configuration is set!
When starting the app with _npm run dev_ , it runs in development mode. The development mode is not suitable at all when we later operate the app in production.
Let's try to create a _production build_ by running the TypeScript compiler. Since we have defined the _outdir_ in our tsconfig.json, nothing's left but to run the script _npm run tsc_.
Just like magic, a native runnable JavaScript production build of the Express backend is created in file _index.js_ inside the directory _build_. The compiled code looks like this
```
"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const app = (0, express_1.default)();
app.use(express_1.default.json());
const PORT = 3000;
app.get('/ping', (_req, res) => {
    console.log('someone pinged here');
    res.send('pong');
});
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});copy
```

Currently, if we run ESlint it will also interpret the files in the _build_ directory. We don't want that, since the code there is compiler-generated. We can _eslint.config.mjs_ as follows:
```
// ...
export default tseslint.config({
  files: ['**/*.ts'],
  extends: [
    eslint.configs.recommended,
    ...tseslint.configs.recommendedTypeChecked,
  ],
  languageOptions: {
    parserOptions: {
      project: true,
      tsconfigRootDir: import.meta.dirname,
    },
  },
  plugins: {
    "@stylistic": stylistic,
  },
  ignores: ["build/*"],  rules: {
    // ...
  },
});copy
```

Let's add an npm script for running the application in production mode:
```
{
  // ...
  "scripts": {
    "tsc": "tsc",
    "dev": "ts-node-dev index.ts",
    "lint": "eslint .",
    "start": "node build/index.js"  },
  // ...
}copy
```

When we run the app with _npm start_ , we can verify that the production build also works:
![browser showing pong from localhost:3000/ping](../assets/8854f0dc828ca5b1.png)
Now we have a minimal working pipeline for developing our project. With the help of our compiler and ESlint, we ensure that good code quality is maintained. With this base, we can start creating an app that we could, later on, deploy into a production environment.
### Exercises 9.8-9.9
#### Before you start the exercises
For this set of exercises, you will be developing a backend for an existing project called **Patientor** , which is a simple medical record application for doctors who handle diagnoses and basic health information of their patients.
The 
#### WARNING
Quite often VS code loses track of what is really happening in the code and it shows type or style related warnings despite the code having been fixed. If this happens (to me it has happened quite often), close and open the file that is giving you trouble or just restart the editor. It is also good to doublecheck that everything really works by running the compiler and the ESlint from the command line with commands:
```
npm run tsc
npm run lintcopy
```

When run in command line you get the "real result" for sure. So, never trust the editor too much!
#### 9.8: Patientor backend, step1
Initialize a new backend project that will work with the frontend. Configure ESlint and tsconfig with the same configurations as proposed in the material. Define an endpoint that answers HTTP GET requests for route _/api/ping_.
The project should be runnable with npm scripts, both in development mode and, as compiled code, in production mode.
#### 9.9: Patientor backend, step2
Fork and clone the project 
You should be able to use the frontend without a functioning backend.
Ensure that the backend answers the ping request that the _frontend_ has made on startup. Check the developer tools to make sure it works:
![dev tools showing ping failed](../assets/18719d173b2448ce.png)
You might also want to have a look at the _console_ tab. If something fails, [part 3](../part3/01-part3.md) of the course shows how the problem can be solved.
### Implementing the functionality
Finally, we are ready to start writing some code.
Let's start from the basics. Ilari wants to be able to keep track of his experiences on his flight journeys.
He wants to be able to save _diary entries_ , which contain:
  * The date of the entry
  * Weather conditions (sunny, windy, cloudy, rainy or stormy)
  * Visibility (great, good, ok or poor)
  * Free text detailing the experience


We have obtained some sample data, which we will use as a base to build on. The data is saved in JSON format and can be found 
The data looks like the following:
```
[
  {
    "id": 1,
    "date": "2017-01-01",
    "weather": "rainy",
    "visibility": "poor",
    "comment": "Pretty scary flight, I'm glad I'm alive"
  },
  {
    "id": 2,
    "date": "2017-04-01",
    "weather": "sunny",
    "visibility": "good",
    "comment": "Everything went better than expected, I'm learning much"
  },
  // ...
]copy
```

Let's start by creating an endpoint that returns all flight diary entries.
First, we need to make some decisions on how to structure our source code. It is better to place all source code under _src_ directory, so source code is not mixed with configuration files. We will move _index.ts_ there and make the necessary changes to the npm scripts.
We will place all [routers](../part4/01-structure-of-backend-application-introduction-to-testing.md) and modules which are responsible for handling a set of specific resources such as _diaries_ , under the directory _src/routes_. This is a bit different than what we did in [part 4](../part4/01-part4.md), where we used the directory _src/controllers_.
The router taking care of all diary endpoints is in _src/routes/diaries.ts_ and looks like this:
```
import express from 'express';

const router = express.Router();

router.get('/', (_req, res) => {
  res.send('Fetching all diaries!');
});

router.post('/', (_req, res) => {
  res.send('Saving a diary!');
});

export default router;copy
```

We'll route all requests to prefix _/api/diaries_ to that specific router in _index.ts_
```
import express from 'express';
import diaryRouter from './routes/diaries';const app = express();
app.use(express.json());

const PORT = 3000;

app.get('/ping', (_req, res) => {
  console.log('someone pinged here');
  res.send('pong');
});

app.use('/api/diaries', diaryRouter);

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});copy
```

And now, if we make an HTTP GET request to _Fetching all diaries!_
Next, we need to start serving the seed data (found _data/entries.json_.
We won't be writing the code for the actual data manipulations in the router. We will create a _service_ that takes care of the data manipulation instead. It is quite a common practice to separate the "business logic" from the router code into modules, which are quite often called _services_. The name service originates from 
Let's create a _src/services_ directory and place the _diaryService.ts_ file in it. The file contains two functions for fetching and saving diary entries:
```
import diaryData from '../../data/entries.json';

const getEntries = () => {
  return diaryData;
};

const addDiary = () => {
  return null;
};

export default {
  getEntries,
  addDiary
};copy
```

But something is not right:
![vscode asking to consider using resolveJsonModule since can't find module](../assets/11e6701e7c9976c1.png)
The hint says we might want to use _resolveJsonModule_. Let's add it to our tsconfig:
```
{
  "compilerOptions": {
    "target": "ES6",
    "outDir": "./build/",
    "module": "commonjs",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "esModuleInterop": true,
    "resolveJsonModule": true  }
}copy
```

And our problem is solved.
> **NB** : For some reason, VSCode sometimes complains that it cannot find the file _../../data/entries.json_ from the service despite the file existing. That is a bug in the editor, and goes away when the editor is restarted.
Earlier, we saw how the compiler can decide the type of a variable by the value it is assigned. Similarly, the compiler can interpret large data sets consisting of objects and arrays. Due to this, the compiler warns us if we try to do something suspicious with the JSON data we are handling. For example, if we are handling an array containing objects of a specific type, and we try to add an object which does not have all the fields the other objects have, or has type conflicts (for example, a number where there should be a string), the compiler can give us a warning.
Even though the compiler is pretty good at making sure we don't do anything unwanted, it is safer to define the types for the data ourselves.
Currently, we have a basic working TypeScript Express app, but there are barely any actual _typings_ in the code. Since we know what type of data should be accepted for the _weather_ and _visibility_ fields, there is no reason for us not to include their types in the code.
Let's create a file for our types, _types.ts_ , where we'll define all our types for this project.
First, let's type the _Weather_ and _Visibility_ values using a 
```
export type Weather = 'sunny' | 'rainy' | 'cloudy' | 'windy' | 'stormy';

export type Visibility = 'great' | 'good' | 'ok' | 'poor';copy
```

And, from there, we can continue by creating a DiaryEntry type, which will be an 
```
export interface DiaryEntry {
  id: number;
  date: string;
  weather: Weather;
  visibility: Visibility;
  comment: string;
}copy
```

We can now try to type our imported JSON:
```
import diaryData from '../../data/entries.json';

import { DiaryEntry } from '../types';
const diaries: DiaryEntry[] = diaryData;
const getEntries = (): DiaryEntry[] => {  return diaries;};

const addDiary = () => {
  return null;
};

export default {
  getEntries,
  addDiary
};copy
```

But since the JSON already has its values declared, assigning a type for the data set results in an error:
![vscode showing string not assignable to weather error](../assets/d54dac9dad0a31d7.png)
The end of the error message reveals the problem: the _weather_ fields are incompatible. In _DiaryEntry_ , we specified that its type is _Weather_ , but the TypeScript compiler had inferred its type to be _string_.
We can fix the problem by doing a [mentioned](../part9/01-first-steps-with-type-script-type-assertion.md) type assertions should be done only if we are certain we know what we are doing!
If we assert the type of the variable _diaryData_ to be _DiaryEntry_ with the keyword _as_ , everything should work:
```
import diaryData from '../../data/entries.json'

import { Weather, Visibility, DiaryEntry } from '../types'

const diaries: DiaryEntry[] = diaryData as DiaryEntry[];
const getEntries = (): DiaryEntry[] => {
  return diaries;
}

const addDiary = () => {
  return null;
}

export default {
  getEntries,
  addDiary
};copy
```

We should never use type assertion unless there is no other way to proceed, as there is always the danger we assert an unfit type to an object and cause a nasty runtime error. While the compiler trusts you to know what you are doing when using _as_ , by doing this, we are not using the full power of TypeScript but relying on the coder to secure the code.
In our case, we could change how we export our data so we can type it within the data file. Since we cannot use typings in a JSON file, we should convert the JSON file to a ts file _entries.ts_ which exports the typed data like so:
```
import { DiaryEntry } from "../src/types";
const diaryEntries: DiaryEntry[] = [  {
      "id": 1,
      "date": "2017-01-01",
      "weather": "rainy",
      "visibility": "poor",
      "comment": "Pretty scary flight, I'm glad I'm alive"
  },
  // ...
];

export default diaryEntries;copy
```

Now, when we import the array, the compiler interprets it correctly:
```
import diaries from '../../data/entries';
import { DiaryEntry } from '../types';

const getEntries = (): DiaryEntry[] => {
  return diaries;
}

const addDiary = () => {
  return null;
}

export default {
  getEntries,
  addDiary
};copy
```

Note that, if we want to be able to save entries without a certain field, e.g. _comment_ , we could set the type of the field as _?_ to the type declaration:
```
export interface DiaryEntry {
  id: number;
  date: string;
  weather: Weather;
  visibility: Visibility;
  comment?: string;}copy
```

### Node and JSON modules
It is important to take note of a problem that may arise when using the tsconfig 
```
{
  "compilerOptions": {
    // ...
    "resolveJsonModule": true  }
}copy
```

According to the node documentation for 
```
 ["js", "json", "node"]copy
```

In addition to that, by default, _ts-node_ and _ts-node-dev_ extend the list of possible node module extensions to:
```
 ["js", "json", "node", "ts", "tsx"]copy
```

> **NB** : The validity of _.js_ , _.json_ and _.node_ files as modules in TypeScript depend on environment configuration, including _tsconfig_ options such as _allowJs_ and _resolveJsonModule_.
Consider a flat folder structure containing files:
```
  ├── myModule.json
  └── myModule.tscopy
```

In TypeScript, with the _resolveJsonModule_ option set to true, the file _myModule.json_ becomes a valid node module. Now, imagine a scenario where we wish to take the file _myModule.ts_ into use:
```
import myModule from "./myModule";copy
```

Looking closely at the order of node module extensions:
```
 ["js", "json", "node", "ts", "tsx"]copy
```

We notice that the _.json_ file extension takes precedence over _.ts_ and so _myModule.json_ will be imported and not _myModule.ts_.
To avoid time-eating bugs, it is recommended that within a flat directory, each file with a valid node module extension has a unique filename.
### Utility Types
Sometimes, we might want to use a specific modification of a type. For example, consider a page for listing some data, some of which is sensitive and some of which is non-sensitive. We might want to be sure that no sensitive data is used or displayed. We could _pick_ the fields of a type we allow to be used to enforce this. We can do that by using the utility type 
In our project, we should consider that Ilari might want to create a listing of all his diary entries _excluding_ the comment field since, during a very scary flight, he might end up writing something he wouldn't necessarily want to show to anyone else.
The 
In our case, to create a "censored" version of the _DiaryEntry_ for public displays, we can use _Pick_ in the function declaration:
```
const getNonSensitiveEntries =
  (): Pick<DiaryEntry, 'id' | 'date' | 'weather' | 'visibility'>[] => {
    // ...
  }copy
```

and the compiler would expect the function to return an array of values of the modified _DiaryEntry_ type, which includes only the four selected fields.
In this case, we want to exclude only one field, so it would be even better to use the 
```
const getNonSensitiveEntries = (): Omit<DiaryEntry, 'comment'>[] => {
  // ...
}copy
```

To improve the readability, we should most definitively define a _NonSensitiveDiaryEntry_ in the file _types.ts_ :
```
export type NonSensitiveDiaryEntry = Omit<DiaryEntry, 'comment'>;copy
```

The code becomes now much more clear and more descriptive:
```
import diaries from '../../data/entries';
import { NonSensitiveDiaryEntry, DiaryEntry } from '../types';
const getEntries = (): DiaryEntry[] => {
  return diaries;
};

const getNonSensitiveEntries = (): NonSensitiveDiaryEntry[] => {  return diaries;
};

const addDiary = () => {
  return null;
};

export default {
  getEntries,
  addDiary,
  getNonSensitiveEntries};copy
```

One thing in our application is a cause for concern. In _getNonSensitiveEntries_ , we are returning the complete diary entries, and _no error is given_ despite typing!
This happens because _not prohibited_ to return an object of type _DiaryEntry[]_ , but if we were to try to access the _comment_ field, it would not be possible because we would be accessing a field that TypeScript is unaware of even though it exists.
Unfortunately, this can lead to unwanted behavior if you are not aware of what you are doing; the situation is valid as far as TypeScript is concerned, but you are most likely allowing a use that is not wanted. If we were now to return all of the diary entries from the _getNonSensitiveEntries_ function to the frontend, we would be _leaking the unwanted fields to the requesting browser_ - even though our types seem to imply otherwise!
Because TypeScript doesn't modify the actual data but only its type, we need to exclude the fields ourselves:
```
import diaries from '../../data/entries.ts'

import { NonSensitiveDiaryEntry, DiaryEntry } from '../types'

const getEntries = () : DiaryEntry[] => {
  return diaries
}

const getNonSensitiveEntries = (): NonSensitiveDiaryEntry[] => {  return diaries.map(({ id, date, weather, visibility }) => ({    id,    date,    weather,    visibility,  }));};
const addDiary = () => {
  return null;
}

export default {
  getEntries,
  getNonSensitiveEntries,
  addDiary
}copy
```

If we now try to return this data with the basic _DiaryEntry_ type, i.e. if we type the function as follows:
```
const getNonSensitiveEntries = (): DiaryEntry[] => {copy
```

we would get the following error:
![vs code error - comment is declared here](../assets/6db4f91fdb0c3a15.png)
Again, the last line of the error message is the most helpful one. Let's undo this undesired modification.
Note that if you make the comment field optional (using the _?_ operator), everything will work fine.
Utility types include many handy tools, and it is undoubtedly worth it to take some time to study 
Finally, we can complete the route which returns all diary entries:
```
import express from 'express';
import diaryService from '../services/diaryService';
const router = express.Router();

router.get('/', (_req, res) => {
  res.send(diaryService.getNonSensitiveEntries());});

router.post('/', (_req, res) => {
  res.send('Saving a diary!');
});

export default router;copy
```

The response is what we expect it to be:
![browser api/diaries shows three json objects](../assets/0e21a9df17c50fe2.png)
### Typing the request and response
So far we have not discussed anything about the types of the route handler parameters. 
If we hover eg. the parameter _res_ , we notice it has the followng type:
```
Response<any, Record<string, any>, number>copy
```

It looks a bit weird. The type _Response_ is a _type parameters_. If we open the type definition (by right clicking and selecting _Go to Type Definition_ in the VS code) we see the following:
```
export interface Response<
    ResBody = any,
    LocalsObj extends Record<string, any> = Record<string, any>,
    StatusCode extends number = number,
> extends http.ServerResponse, Express.Response {copy
```

The first type parameter is the most interesting for us, it corresponds _the response body_ and has a default value _any_. So that is why TypeScript compiler accepts any type of response and we get no help to get the response right.
We could and propably should give a proper type as the type variable. In our case it is an array of diary entries:
```
import { Response } from 'express'
import { NonSensitiveDiaryEntry } from "../types";
// ...

router.get('/', (_req, res: Response<NonSensitiveDiaryEntry[]>) => {
  res.send(diaryService.getNonSensitiveEntries());
});

// ...copy
```

If we now try to respond with wrong type of data, the code does not compile
![vscode error unsafe assignment of any value](../assets/4daeda61cbb08595.png)
Simillarly the request parameter has the type _Request_ that is also a generic type. We shall have a closer look on it later on.
### Exercises 9.10-9.11
Similarly to Ilari's flight service, we do not use a real database in our app but instead use hardcoded data that is in the files _data_ in your project. All data modification can be done in runtime memory, so during this part, it is _not necessary to write to a file_.
#### 9.10: Patientor backend, step3
Create a type _Diagnosis_ and use it to create endpoint _/api/diagnoses_ for fetching all diagnoses with HTTP GET.
Structure your code properly by using meaningfully-named directories and files.
**Note** that _diagnoses_ may or may not contain the field _latin_. You might want to use 
#### 9.11: Patientor backend, step4
Create data type _Patient_ and set up the GET endpoint _/api/patients_ which returns all the patients to the frontend, excluding field _ssn_. Use a 
In this exercise, you may assume that field _gender_ has type _string_.
Try the endpoint with your browser and ensure that _ssn_ is not included in the response:
![api/patients browser shows no ssn in patients json](../assets/9ad2c91afaefaad0.png)
After creating the endpoint, ensure that the _frontend_ shows the list of patients:
![browser showing list of patients](../assets/60e7f07c081d516a.png)
### Preventing an accidental undefined result
Let's extend the backend to support fetching one specific entry with an HTTP GET request to route _api/diaries/:id_.
The DiaryService needs to be extended with a _findById_ function:
```
// ...

const findById = (id: number): DiaryEntry => {  const entry = diaries.find(d => d.id === id);  return entry;};
export default {
  getEntries,
  getNonSensitiveEntries,
  addDiary,
  findById}copy
```

But once again, a new problem emerges:
![vscode error can't assign undefined to DiaryEntry](../assets/9fb6fa210b90fa2a.png)
The issue is that there is no guarantee that an entry with the specified id can be found. It is good that we are made aware of this potential problem already at compile phase. Without TypeScript, we would not be warned about this problem, and in the worst-case scenario, we could have ended up returning an _undefined_ object instead of informing the user about the specified entry not being found.
First of all, in cases like this, we need to decide what the _return value_ should be if an object is not found, and how the case should be handled. The _find_ method of an array returns _undefined_ if the object is not found, and this is fine. We can solve our problem by typing the return value as follows:
```
const findById = (id: number): DiaryEntry | undefined => {  const entry = diaries.find(d => d.id === id);
  return entry;
}copy
```

The route handler is the following:
```
import express from 'express';
import diaryService from '../services/diaryService'

router.get('/:id', (req, res) => {
  const diary = diaryService.findById(Number(req.params.id));

  if (diary) {
    res.send(diary);
  } else {
    res.sendStatus(404);
  }
});

// ...

export default router;copy
```

### Adding a new diary
Let's start building the HTTP POST endpoint for adding new flight diary entries. The new entries should have the same type as the existing data.
The code handling of the response looks as follows:
```
router.post('/', (req, res) => {
  const { date, weather, visibility, comment } = req.body;
  const addedEntry = diaryService.addDiary(
    date,
    weather,
    visibility,
    comment,
  );
  res.json(addedEntry);
});copy
```

The corresponding method in _diaryService_ looks like this:
```
import {
  NonSensitiveDiaryEntry,
  DiaryEntry,
  Visibility,  Weather} from '../types';


const addDiary = (
    date: string, weather: Weather, visibility: Visibility, comment: string
  ): DiaryEntry => {

  const newDiaryEntry = {
    id: Math.max(...diaries.map(d => d.id)) + 1,
    date,
    weather,
    visibility,
    comment,
  };

  diaries.push(newDiaryEntry);
  return newDiaryEntry;
};copy
```

As you can see, the _addDiary_ function is becoming quite hard to read now that we have all the fields as separate parameters. It might be better to just send the data as an object to the function:
```
router.post('/', (req, res) => {
  const { date, weather, visibility, comment } = req.body;
  const addedEntry = diaryService.addDiary({    date,
    weather,
    visibility,
    comment,
  });  res.json(addedEntry);
})copy
```

But wait, what is the type of this object? It is not exactly a _DiaryEntry_ , since it is still missing the _id_ field. It could be useful to create a new type, _NewDiaryEntry_ , for an entry that hasn't been saved yet. Let's create that in _types.ts_ using the existing _DiaryEntry_ type and the 
```
export type NewDiaryEntry = Omit<DiaryEntry, 'id'>;copy
```

Now we can use the new type in our DiaryService, and destructure the new entry object when creating an entry to be saved:
```
import { NewDiaryEntry, NonSensitiveDiaryEntry, DiaryEntry } from '../types';
// ...

const addDiary = ( entry: NewDiaryEntry ): DiaryEntry => {  const newDiaryEntry = {
    id: Math.max(...diaries.map(d => d.id)) + 1,
    ...entry  };

  diaries.push(newDiaryEntry);
  return newDiaryEntry;
};copy
```

Now the code looks much cleaner!
There is still a complaint from our code:
![vscode error unsafe assignment of any value](../assets/2c150e1cfc28c7cb.png)
The cause is the ESlint rule 
For the time being, let us just ignore the ESlint rule from the whole file by adding the following as the first line of the file:
```
/* eslint-disable @typescript-eslint/no-unsafe-assignment */copy
```

To parse the incoming data we must have the _json_ middleware configured:
```
import express from 'express';
import diaryRouter from './routes/diaries';
const app = express();
app.use(express.json());
const PORT = 3000;

app.use('/api/diaries', diaryRouter);

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});copy
```

Now the application is ready to receive HTTP POST requests for new diary entries of the correct type!
### Validating requests
There are plenty of things that can go wrong when we accept data from outside sources. Applications rarely work completely on their own, and we are forced to live with the fact that data from sources outside of our system cannot be fully trusted. When we receive data from an outside source, there is no way it can already be typed when we receive it. We need to make decisions on how to handle the uncertainty that comes with this.
The disabled ESlint rule was hinting to us that the following assignment is risky:
```
const newDiaryEntry = diaryService.addDiary({
  date,
  weather,
  visibility,
  comment,
});copy
```

We would like to have the assurance that the object in a POST request has the correct type. Let us now define a function _toNewDiaryEntry_ that receives the request body as a parameter and returns a properly-typed _NewDiaryEntry_ object. The function shall be defined in the file _utils.ts_.
The route definition uses the function as follows:
```
import toNewDiaryEntry from '../utils';
// ...

router.post('/', (req, res) => {
  try {
    const newDiaryEntry = toNewDiaryEntry(req.body);
    const addedEntry = diaryService.addDiary(newDiaryEntry);    res.json(addedEntry);
  } catch (error: unknown) {
    let errorMessage = 'Something went wrong.';
    if (error instanceof Error) {
      errorMessage += ' Error: ' + error.message;
    }
    res.status(400).send(errorMessage);
  }
})copy
```

We can now also remove the first line that ignores the ESlint rule _no-unsafe-assignment_.
Since we are now writing secure code and trying to ensure that we are getting exactly the data we want from the requests, we should get started with parsing and validating each field we are expecting to receive.
The skeleton of the function _toNewDiaryEntry_ looks like the following:
```
import { NewDiaryEntry } from './types';

const toNewDiaryEntry = (object): NewDiaryEntry => {
  const newEntry: NewDiaryEntry = {
    // ...
  };

  return newEntry;
};

export default toNewDiaryEntry;copy
```

The function should parse each field and make sure that the return value is exactly of type _NewDiaryEntry_. This means we should check each field separately.
Once again, we have a type issue: what is the type of the parameter _object_? Since the _object_ is the body of a request, Express has typed it as _any_. Since the idea of this function is to map fields of unknown type to fields of the correct type and check whether they are defined as expected, this might be the rare case in which we _want to allow the**any** type_.
However, if we type the object as _any_ , ESlint complains about that:
![vscode eslint showing object should be typed something non-any and that its defined but never used](../assets/08ce3cbb4f6d59dc.png)
We could ignore the ESlint rule but a better idea is to follow one of the advices the editor gives in the _Quick Fix_ and set the parameter type to _unknown_ :
```
import { NewDiaryEntry } from './types';

const toNewDiaryEntry = (object: unknown): NewDiaryEntry => {  const newEntry: NewDiaryEntry = {
    // ...
  }

  return newEntry;
}

export default toNewDiaryEntry;copy
```

_any_ type, but can first verify the type and then confirm that is the expected type. With the use of _unknown_ , we also don't need to worry about the _@typescript-eslint/no-explicit-any_ ESlint rule, since we are not using _any_. However, we might still need to use _any_ in some cases in which we are not yet sure about the type and need to access the properties of an object of type _any_ to validate or type-check the property values themselves.
> #### A sidenote from the editor
> _If you are like me and hate having a code in broken state for a long time due to incomplete typing, you could start by "faking" the function:_
> ```
const toNewDiaryEntry = (object: unknown): NewDiaryEntry => {

 console.log(object); // now object is no longer unused
 const newEntry: NewDiaryEntry = {
   weather: 'cloudy', // fake the return value
   visibility: 'great',
   date: '2022-1-1',
   comment: 'fake news'
 };

 return newEntry;
};copy
```

> _So before the real data and types are ready to use, I am just returning here something that has for sure the right type. The code stays in an operational state all the time and my blood pressure remains at normal levels._
### Type guards
Let us start creating the parsers for each of the fields of the parameter _object: unknown_.
To validate the _comment_ field, we need to check that it exists and to ensure that it is of the type _string_.
The function should look something like this:
```
const parseComment = (comment: unknown): string => {
  if (!comment || !isString(comment)) {
    throw new Error('Incorrect or missing comment');
  }

  return comment;
};copy
```

The function gets a parameter of type _unknown_ and returns it as the type _string_ if it exists and is of the right type.
The string validation function looks like this:
```
const isString = (text: unknown): text is string => {
  return typeof text === 'string' || text instanceof String;
};copy
```

The function is a so-called _and_ has a _type predicate_ as the return type. In our case, the type predicate is:
```
text is stringcopy
```

The general form of a type predicate is _parameterName is Type_ where the _parameterName_ is the name of the function parameter and _Type_ is the targeted type.
If the type guard function returns true, the TypeScript compiler knows that the tested variable has the type that was defined in the type predicate.
Before the type guard is called, the actual type of the variable _comment_ is not known:
![vscode hovering over isString\(comment\) shows type unknown](../assets/e29ccd5e262f66df.png)
But after the call, if the code proceeds past the exception (that is, the type guard returned true), then the compiler knows that _comment_ is of type _string_ :
![vscode hovering over return comment shows type string](../assets/8e94fbef93bda7fd.png)
The use of a type guard that returns a type predicate is one way to do 
> #### Side note: testing if something is a string
> _Why do we have two conditions in the string type guard?_
> ```
const isString = (text: unknown): text is string => {
 return typeof text === 'string' || text instanceof String;}copy
```

> _Would it not be enough to write the guard like this?_
> ```
const isString = (text: unknown): text is string => {
 return typeof text === 'string';
}copy
```

> _Most likely, the simpler form is good enough for all practical purposes. However, if we want to be sure, both conditions are needed. There are two different ways to create string in JavaScript, one as a primitive and the other as an object, which both work a bit differently when compared to the**typeof** and **instanceof** operators:_
> ```
const a = "I'm a string primitive";
const b = new String("I'm a String Object");
typeof a; --> returns 'string'
typeof b; --> returns 'object'
a instanceof String; --> returns false
b instanceof String; --> returns truecopy
```

> _However, it is unlikely that anyone would create a string with a constructor function. Most likely the simpler version of the type guard would be just fine._
Next, let's consider the _date_ field. Parsing and validating the date object is pretty similar to what we did with comments. Since TypeScript doesn't know a type for a date, we need to treat it as a _string_. We should however still use JavaScript-level validation to check whether the date format is acceptable.
We will add the following functions:
```
const isDate = (date: string): boolean => {
  return Boolean(Date.parse(date));
};

const parseDate = (date: unknown): string => {
  if (!date || !isString(date) || !isDate(date)) {
      throw new Error('Incorrect or missing date: ' + date);
  }
  return date;
};copy
```

The code is nothing special. The only thing is that we can't use a type predicate based type guard here since a date in this case is only considered to be a _string_. Note that even though the _parseDate_ function accepts the _date_ variable as _unknown_ after we check the type with _isString_ , then its type is set as _string_ , which is why we can give the variable to the _isDate_ function requiring a string without any problems.
Finally, we are ready to move on to the last two types, _Weather_ and _Visibility_.
We would like the validation and parsing to work as follows:
```
const parseWeather = (weather: unknown): Weather => {
  if (!weather || !isString(weather) || !isWeather(weather)) {
      throw new Error('Incorrect or missing weather: ' + weather);
  }
  return weather;
};copy
```

The question is: how can we validate that the string is of a specific form? One possible way to write the type guard would be this:
```
const isWeather = (str: string): str is Weather => {
  return ['sunny', 'rainy', 'cloudy', 'stormy'].includes(str);
};copy
```

This would work just fine, but the problem is that the list of possible values for Weather does not necessarily stay in sync with the type definitions if the type is altered. This is most certainly not good, since we would like to have just one source for all possible weather types.
### Enum
In our case, a better solution would be to improve the actual _Weather_ type. Instead of a type alias, we should use the TypeScript 
Let us redefine the type _Weather_ as follows:
```
export enum Weather {
  Sunny = 'sunny',
  Rainy = 'rainy',
  Cloudy = 'cloudy',
  Stormy = 'stormy',
  Windy = 'windy',
}copy
```

Now we can check that a string is one of the accepted values, and the type guard can be written like this:
```
const isWeather = (param: string): param is Weather => {
  return Object.values(Weather).map(v => v.toString()).includes(param);
};copy
```

Note that we need to take the string representation of the enum values for the comparison, that is why we do the mapping.
One issue arises after these changes. Our data in file _data/entries.ts_ does not conform to our types anymore:
![vscode error rainy is not assignable to type Weather](../assets/af59af58c4b5ffa2.png)
This is because we cannot just assume a string is an enum.
We can fix this by mapping the initial data elements to the _DiaryEntry_ type with the _toNewDiaryEntry_ function:
```
import { DiaryEntry } from "../src/types";
import toNewDiaryEntry from "../src/utils";

const data = [
  {
      "id": 1,
      "date": "2017-01-01",
      "weather": "rainy",
      "visibility": "poor",
      "comment": "Pretty scary flight, I'm glad I'm alive"
  },
  // ...
]

const diaryEntries: DiaryEntry [] = data.map(obj => {
  const object = toNewDiaryEntry(obj) as DiaryEntry;
  object.id = obj.id;
  return object;
});

export default diaryEntries;copy
```

Note that since _toNewDiaryEntry_ returns an object of type _NewDiaryEntry_ , we need to assert it to be _DiaryEntry_ with the 
Enums are typically used when there is a set of predetermined values that are not expected to change in the future. Usually, they are used for much tighter unchanging values (for example, weekdays, months, cardinal directions), but since they offer us a great way to validate our incoming values, we might as well use them in our case.
We still need to give the same treatment to _Visibility_. The enum looks as follows:
```
export enum Visibility {
  Great = 'great',
  Good = 'good',
  Ok = 'ok',
  Poor = 'poor',
}copy
```

The type guard and the parser are below:
```
const isVisibility = (param: string): param is Visibility => {
  return Object.values(Visibility).map(v => v.toString()).includes(param);
};

const parseVisibility = (visibility: unknown): Visibility => {
  if (!visibility || !isString(visibility) || !isVisibility(visibility)) {
      throw new Error('Incorrect or missing visibility: ' + visibility);
  }
  return visibility;
};copy
```

And finally, we can finalize the _toNewDiaryEntry_ function that takes care of validating and parsing the fields of the POST body. There is however one more thing to take care of. If we try to access the fields of the parameter _object_ as follows:
```
const toNewDiaryEntry = (object: unknown): NewDiaryEntry => {
  const newEntry: NewDiaryEntry = {
    comment: parseComment(object.comment),
    date: parseDate(object.date),
    weather: parseWeather(object.weather),
    visibility: parseVisibility(object.visibility)
  };

  return newEntry;
};copy
```

we notice that the code does not compile. This is because the 
We can again fix the problem by type narrowing. We have now two type guards, the first checks that the parameter object exists and it has the type _object_. After this, the second type guard uses the 
```
const toNewDiaryEntry = (object: unknown): NewDiaryEntry => {
  if ( !object || typeof object !== 'object' ) {
    throw new Error('Incorrect or missing data');
  }

  if ('comment' in object && 'date' in object && 'weather' in object && 'visibility' in object)  {
    const newEntry: NewDiaryEntry = {
      weather: parseWeather(object.weather),
      visibility: parseVisibility(object.visibility),
      date: parseDate(object.date),
      comment: parseComment(object.comment)
    };

    return newEntry;
  }

  throw new Error('Incorrect data: some fields are missing');
};copy
```

If the guard does not evaluate to true, an exception is thrown.
The use of the operator _in_ actually now guarantees that the fields indeed exist in the object. Because of that, the existence checks in the parsers are no longer needed:
```
const parseVisibility = (visibility: unknown): Visibility => {
  // check !visibility removed:
  if (!isString(visibility) || !isVisibility(visibility)) {
      throw new Error('Incorrect visibility: ' + visibility);
  }
  return visibility;
};copy
```

If a field, e.g. _comment_ would be optional, the type narrowing should take that into account, and the operator _in_ test requires the field to be present.
If we now try to create a new diary entry with invalid or missing fields, we are getting an appropriate error message:
![postman showing 400 bad request with incorrect or missing visibility - awesome](../assets/7416751d60876d05.png)
The source code of the application can be found on 
### Exercises 9.12-9.13
#### 9.12: Patientor backend, step5
Create a POST endpoint _/api/patients_ for adding patients. Ensure that you can add patients also from the frontend. You can create unique ids of type _string_ using the 
```
import { v1 as uuid } from 'uuid'
const id = uuid()copy
```

#### 9.13: Patientor backend, step6
Set up safe parsing, validation and type predicate to the POST _/api/patients_ request.
Refactor the _gender_ field to use an 
### Using schema validation libraries
Writing a validator to the request body can be a huge burden. Thankfully there exists several _schema validator libraries_ that can help. Let us now have a look at 
Let us get started:
```
npm install zodcopy
```

Parsers of the primitive valued fields such as
```
const isString = (text: unknown): text is string => {
  return typeof text === 'string' || text instanceof String;
};

const parseComment = (comment: unknown): string => {
  if (!isString(comment)) {
    throw new Error('Incorrect comment');
  }

  return comment;
};copy
```

are easy to replace as follows:
```
const parseComment = (comment: unknown): string => {
  return z.string().parse(comment);};copy
```

First the _schema_ in Zod terms). After that the value (which is of the type _unknown_) is parsed with the method 
We do not actually need the helper function _parseComment_ anymore and can use the Zod parser directly:
```
export const toNewDiaryEntry = (object: unknown): NewDiaryEntry => {
  if ( !object || typeof object !== 'object' ) {
    throw new Error('Incorrect or missing data');
  }

  if ('comment' in object && 'date' in object && 'weather' in object && 'visibility' in object)  {
    const newEntry: NewDiaryEntry = {
      weather: parseWeather(object.weather),
      visibility: parseVisibility(object.visibility),
      date: parseDate(object.date),
      comment: z.string().parse(object.comment)    };

    return newEntry;
  }

  throw new Error('Incorrect data: some fields are missing');
};copy
```

Zod has a bunch of string specific validations, eg. one that validates if a string is a valid 
```
export const toNewDiaryEntry = (object: unknown): NewDiaryEntry => {
  if ( !object || typeof object !== 'object' ) {
    throw new Error('Incorrect or missing data');
  }

  if ('comment' in object && 'date' in object && 'weather' in object && 'visibility' in object)  {
    const newEntry: NewDiaryEntry = {
      weather: parseWeather(object.weather),
      visibility: parseVisibility(object.visibility), 
      date: z.string().date().parse(object.date),      comment: z.string().optional().parse(object.comment)    };

    return newEntry;
  }

  throw new Error('Incorrect data: some fields are missing');
};copy
```

We have also made the field comment 
Zod has also support for 
```
export const toNewDiaryEntry = (object: unknown): NewDiaryEntry => {
  if ( !object || typeof object !== 'object' ) {
    throw new Error('Incorrect or missing data');
  }

  if ('comment' in object && 'date' in object && 'weather' in object && 'visibility' in object)  {
    const newEntry: NewDiaryEntry = {
      weather: z.nativeEnum(Weather).parse(object.weather),      visibility: z.nativeEnum(Visibility).parse(object.visibility),      date: z.string().date().parse(object.date),
      comment: z.string().optional().parse(object.comment)
    };

    return newEntry;
  }

  throw new Error('Incorrect data: some fields are missing');
};copy
```

We have so far just used Zod to parse the type or schema of individual fields, but we can go one step further and define the whole _new diary entry_ as a Zod 
```
const newEntrySchema = z.object({
  weather: z.nativeEnum(Weather),
  visibility: z.nativeEnum(Visibility),
  date: z.string().date(),
  comment: z.string().optional()
});copy
```

Now it is just enough to call _parse_ of the defined schema:
```
export const toNewDiaryEntry = (object: unknown): NewDiaryEntry => {
  return newEntrySchema.parse(object);
};copy
```

With the help from 
```
router.post('/', (req, res) => {
  try {
    const newDiaryEntry = toNewDiaryEntry(req.body);
    const addedEntry = diaryService.addDiary(newDiaryEntry);
    res.json(addedEntry);

  } catch (error: unknown) {
    if (error instanceof z.ZodError) {      res.status(400).send({ error: error.issues });    } else {      res.status(400).send({ error: 'unknown error' });    }  }
});copy
```

The response in case of error looks pretty good:
![fullstack content](../assets/a741f1b4c9709b32.png)
We could develop our solution still some steps further. Our type definitions currently look like this:
```
export interface DiaryEntry {
  id: number;
  date: string;
  weather: Weather;
  visibility: Visibility;
  comment?: string;
}

export type NewDiaryEntry = Omit<DiaryEntry, 'id'>;copy
```

So besides the type _NewDiaryEntry_ we have also the Zod schema _NewEntrySchema_ that defines the shape of a new entry. We can use the schema to 
```
import { z } from 'zod';
import { newEntrySchema } from './utils'

export interface DiaryEntry {
  id: number;
  date: string;
  weather: Weather;
  visibility: Visibility;
  comment?: string;
}

// infer the type from schema
export type NewDiaryEntry = z.infer<typeof newEntrySchema>; copy
```

We could take this even a bit further and define the _DiaryEntry_ based on _NewDiaryEntry_ :
```
export type NewDiaryEntry = z.infer<typeof newEntrySchema>;

export interface DiaryEntry extends NewDiaryEntry {
  id: number;
}copy
```

This would remove all the duplication in the type and schema definitions but feels a bit backward so we decide to define the type _DiaryEntry_ explicitly with TypeScript.
Unfortunately the opposite is not possible: we can not define the Zod schema based on TypeScript type definitions, and due to this, the duplication in the type and schema definitions is hard to avoid.
The current state of the source code can be found in the part2 branch of 
### Parsing request body in middleware
We can now get rid of this method altogether
```
export const toNewDiaryEntry = (object: unknown): NewDiaryEntry => {
  return newEntrySchema.parse(object);
};copy
```

and just call the Zod-parser directly in the route handler:
```
import express, { Request, Response } from 'express';
import diaryService from '../services/diaryService';
import { NewEntrySchema } from '../utils';

router.post('/', (req, res) => {  try {
    const newDiaryEntry = NewEntrySchema.parse(req.body);    const addedEntry = diaryService.addDiary(newDiaryEntry);
    res.json(addedEntry);

  } catch (error: unknown) {
    if (error instanceof z.ZodError) {
      res.status(400).send({ error: error.issues });
    } else {
      res.status(400).send({ error: 'unknown error' });
    }
  }
});copy
```

Instead of calling the request body parsing method explicitly in the route handler, the validation of the input could also be done in a middleware function.
We have also added the type definitions to the route handler parameters, and shall also use types in the middleware function _newDiaryParser_ :
```
const newDiaryParser = (req: Request, _res: Response, next: NextFunction) => { 
  try {
    NewEntrySchema.parse(req.body);
    next();
  } catch (error: unknown) {
    next(error);
  }
};copy
```

The middleware just calls the schema parser to the request body. If the parsing throws an exception, that is passed to the error handling middleware.
So after the request passes this middleware, it _is known that the request body is a proper new diary entry_. We can tell this fact to TypeScript compiler by giving a type parameter to the _Request_ type:
```
router.post('/', newDiaryParser, (req: Request<unknown, unknown, NewDiaryEntry>, res: Response<DiaryEntry>) => {  const addedEntry = diaryService.addDiary(req.body);  res.json(addedEntry);
});copy
```

Thanks to the middleware, the request body is now known to be of right type and it can be directly given as parameter to the function _diaryService.addDiary_.
The syntax of the _Request <unknown, unknown, NewDiaryEntry>_ looks a bit odd. The _Request_ is a _NewDiaryEntry_ we have to give _some_ value to the two first parameters. We decide to define those _unknown_ since we do not need those for now.
Since the possible errors in validation are now handled in the error handling middleware, we need to define one that handles the Zod errors properly:
```
const errorMiddleware = (error: unknown, _req: Request, res: Response, next: NextFunction) => { 
  if (error instanceof z.ZodError) {
    res.status(400).send({ error: error.issues });
  } else {
    next(error);
  }
};

router.post('/', newDiaryParser, (req: Request<unknown, unknown, NewDiaryEntry>, res: Response<DiaryEntry>) => {
  // ...
});

router.use(errorMiddleware);copy
```

The final version of the source code can be found in the part3 branch of 
### Exercises 9.14
#### 9.14: Patientor backend, step7
Use Zod to validate the requests to the POST endpoint _/api/patients_.
[ Part 9b **Previous part** ](../part9/01-first-steps-with-type-script.md)[ Part 9d **Next part** ](../part9/01-react-with-types.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)