---{
  "title": "First steps with TypeScript",
  "source_url": "https://fullstackopen.com/en/part9/first_steps_with_type_script",
  "crawl_timestamp": "2025-10-04T19:17:19Z",
  "checksum": "5a92c6b18ad1fb956bd961c84e938cdf87dda20c76230f26119bd28e4de667da"
}
---[Skip to content](../part9/01-first-steps-with-type-script-course-main-content.md)
[{() => fs}](https://fullstackopen.com/en/)

- [About course](../about/01-about.md)
- [Course contents](../#course-contents/01-course-contents.md)
- [FAQ](../faq/01-faq.md)
- [Partners](../companies/01-companies.md)
- [Challenge](../challenge/01-challenge.md)
[Search from the material](../search/01-search.md)Toggle dark theme
Select languageSuomi English 中文 Español Français Português(BR)

A new exercise has been added at the end of Part 9 "Typing an Express app" at 28th August 2024. Because of that numbering of the Exercises 9.14- has changed.
x
[Fullstack](../#course-contents/01-course-contents.md)
[Part 9](../part9/01-part9.md)
First steps with TypeScript
[a Background and introduction](../part9/01-background-and-introduction.md)
b First steps with TypeScript

- [Setting things up](../part9/01-first-steps-with-type-script-setting-things-up.md)
- [Creating your first own types](../part9/01-first-steps-with-type-script-creating-your-first-own-types.md)
- [Type narrowing](../part9/01-first-steps-with-type-script-type-narrowing.md)
- [Accessing command line arguments](../part9/01-first-steps-with-type-script-accessing-command-line-arguments.md)
- [@types/{npm_package}](../part9/01-first-steps-with-type-script-types-npm-package.md)
- [Improving the project](../part9/01-first-steps-with-type-script-improving-the-project.md)
- [The alternative array syntax](../part9/01-first-steps-with-type-script-the-alternative-array-syntax.md)
- [Exercises 9.1-9.3](../part9/01-first-steps-with-type-script-exercises-9-1-9-3.md)
- [More about tsconfig](../part9/01-first-steps-with-type-script-more-about-tsconfig.md)
- [Adding Express to the mix](../part9/01-first-steps-with-type-script-adding-express-to-the-mix.md)
- [Exercises 9.4-9.5](../part9/01-first-steps-with-type-script-exercises-9-4-9-5.md)
- [The horrors of any](../part9/01-first-steps-with-type-script-the-horrors-of-any.md)
- [Type assertion](../part9/01-first-steps-with-type-script-type-assertion.md)
- [Exercises 9.6-9.7](../part9/01-first-steps-with-type-script-exercises-9-6-9-7.md)


[c Typing an Express app](../part9/01-typing-an-express-app.md)[d React with types](../part9/01-react-with-types.md)[e Grande finale: Patientor](../part9/01-grande-finale-patientor.md)
b
# First steps with TypeScript
After the brief introduction to the main principles of TypeScript, we are now ready to start our journey toward becoming FullStack TypeScript developers. Rather than giving you a thorough introduction to all aspects of TypeScript, we will focus in this part on the most common issues that arise when developing an Express backend or a React frontend with TypeScript. In addition to language features, we will also have a strong emphasis on tooling.
### Setting things up
Install TypeScript support to your editor of choice.
As mentioned earlier, TypeScript code is not executable by itself. It has to be first compiled into executable JavaScript. When TypeScript is compiled into JavaScript, the code becomes subject to type erasure. This means that type annotations, interfaces, type aliases, and other type system constructs are removed and the result is pure ready-to-run JavaScript.
In a production environment, the need for compilation often means that you have to set up a "build step." During the build step, all TypeScript code is compiled into JavaScript in a separate folder, and the production environment then runs the code from that folder. In a development environment, it is often easier to make use of real-time compilation and auto-reloading so one can see the resulting changes more quickly.
Let's start writing our first TypeScript app. To keep things simple, let's start by using the npm package
You can install both _ts-node_ and the official _typescript_ package globally by running:

```
npm install --location=global ts-node typescriptcopy
```

If you can't or don't want to install global packages, you can create an npm project that has the required dependencies and run your scripts in it. We will also take this approach.
As we recall from [part 3](../part3/01-part3.md), an npm project is set by running the command _npm init_ in an empty directory. Then we can install the dependencies by running

```
npm install --save-dev ts-node typescriptcopy
```

and setting up _scripts_ within the package.json:

```
{
  // ..
  "scripts": {
    "ts-node": "ts-node"  },
  // ..
}copy
```

You can now use _ts-node_ within this directory by running _npm run ts-node_. Note that if you are using ts-node through package.json, command-line arguments that include short or long-form options for the _npm run script_ need to be prefixed with _--_. So if you want to run file.ts with _ts-node_ and options _-s_ and _--someoption_ , the whole command is:

```
npm run ts-node file.ts -- -s --someoptioncopy
```

It is worth mentioning that TypeScript also provides an online playground, where you can quickly try out TypeScript code and instantly see the resulting JavaScript and possible compilation errors. You can access TypeScript's official playground
**NB:** The playground might contain different tsconfig rules (which will be introduced later) than your local environment, which is why you might see different warnings there compared to your local environment. The playground's tsconfig is modifiable through the config dropdown menu.
#### A note about the coding style
JavaScript is a quite relaxed language in itself, and things can often be done in multiple different ways. For example, we have named vs anonymous functions, using const and let or var, and the optional use of _semicolons_. This part of the course differs from the rest by using semicolons. It is not a TypeScript-specific pattern but a general coding style decision taken when creating any kind of JavaScript project. Whether to use them or not is usually in the hands of the programmer, but since it is expected to adapt one's coding habits to the existing codebase, you are expected to use semicolons and adjust to the coding style in the exercises for this part. This part has some other coding style differences compared to the rest of the course as well, e.g. in the directory naming conventions.
Let us add a configuration file _tsconfig.json_ to the project with the following content:

```
{
  "compilerOptions":{
    "noImplicitAny": false
  }
}copy
```

The _tsconfig.json_ file is used to define how the TypeScript compiler should interpret the code, how strictly the compiler should work, which files to watch or ignore, and
Let's start by creating a simple Multiplier. It looks exactly as it would in JavaScript.

```
const multiplicator = (a, b, printText) => {
  console.log(printText,  a * b);
}

multiplicator(2, 4, 'Multiplied numbers 2 and 4, the result is:');copy
```

As you can see, this is still ordinary basic JavaScript with no additional TS features. It compiles and runs nicely with _npm run ts-node -- multiplier.ts_ , as it would with Node.
But what happens if we end up passing the wrong _types_ of arguments to the multiplicator function?
Let's try it out!

```
const multiplicator = (a, b, printText) => {
  console.log(printText,  a * b);
}

multiplicator('how about a string?', 4, 'Multiplied a string and 4, the result is:');copy
```

Now when we run the code, the output is: _Multiplied a string and 4, the result is: NaN_.
Wouldn't it be nice if the language itself could prevent us from ending up in situations like this? This is where we see the first benefits of TypeScript. Let's add types to the parameters and see where it takes us.
TypeScript natively supports multiple types including _number_ , _string_ and _Array_. See the comprehensive list
The first two parameters of our function are of type number and the last one is of type string, both types are

```
const multiplicator = (a: number, b: number, printText: string) => {
  console.log(printText,  a * b);
}

multiplicator('how about a string?', 4, 'Multiplied a string and 4, the result is:');copy
```

Now the code is no longer valid JavaScript but in fact TypeScript. When we try to run the code, we notice that it does not compile:
![terminal output showing error assigning string to number](../assets/dbf18b8a164e7774.png)
One of the best things about TypeScript's editor support is that you don't necessarily need to even run the code to see the issues. VSCode is so efficient, that it informs you immediately when you are trying to use an incorrect type:
![vscode showing same error about string as number](../assets/9b020ee2b1253f91.png)
### Creating your first own types
Let's expand our multiplicator into a slightly more versatile calculator that also supports addition and division. The calculator should accept three arguments: two numbers and the operation, either _multiply_ , _add_ or _divide_ , which tells it what to do with the numbers.
In JavaScript, the code would require additional validation to make sure the last argument is indeed a string. TypeScript offers a way to define specific types for inputs, which describe exactly what type of input is acceptable. On top of that, TypeScript can also show the info on the accepted values already at the editor level.
We can create a _type_ using the TypeScript native keyword _type_. Let's describe our type _Operation_ :

```
type Operation = 'multiply' | 'add' | 'divide';copy
```

Now the _Operation_ type accepts only three kinds of values; exactly the three strings we wanted. Using the OR operator _|_ we can define a variable to accept multiple values by creating a _string | number_.
The _type_ keyword defines a new name for a type:
Let's look at our calculator now:

```
type Operation = 'multiply' | 'add' | 'divide';

const calculator = (a: number, b: number, op: Operation) => {
  if (op === 'multiply') {
    return a * b;
  } else if (op === 'add') {
    return a + b;
  } else if (op === 'divide') {
    if (b === 0) return 'can\'t divide by 0!';
    return a / b;
  }
}copy
```

Now, when we hover on top of the _Operation_ type in the calculator function, we can immediately see suggestions on what to do with it:
![vs code suggestion operation 3 types](../assets/9b4186c8fab9122c.png)
And if we try to use a value that is not within the _Operation_ type, we get the familiar red warning signal and extra info from our editor:
![vscode warning when trying to have 'yolo' as Operation](../assets/c145bbdd2ab89f1f.png)
This is already pretty nice, but one thing we haven't touched yet is typing the return value of a function. Usually, you want to know what a function returns, and it would be nice to have a guarantee that it returns what it says it does. Let's add a return value _number_ to the calculator function:

```
type Operation = 'multiply' | 'add' | 'divide';

const calculator = (a: number, b: number, op: Operation): number => {
  if (op === 'multiply') {
    return a * b;
  } else if (op === 'add') {
    return a + b;
  } else if (op === 'divide') {
    if (b === 0) return 'this cannot be done';
    return a / b;
  }
}copy
```

The compiler complains straight away because, in one case, the function returns a string. There are a couple of ways to fix this:
We could extend the return type to allow string values, like so:

```
const calculator = (a: number, b: number, op: Operation): number | string =>  {
  // ...
}copy
```

Or we could create a return type, which includes both possible types, much like our Operation type:

```
type Result = string | number;

const calculator = (a: number, b: number, op: Operation): Result =>  {
  // ...
}copy
```

But now the question is if it's _really_ okay for the function to return a string?
When your code can end up in a situation where something is divided by 0, something has probably gone terribly wrong and an error should be thrown and handled where the function was called. When you are deciding to return values you weren't originally expecting, the warnings you see from TypeScript prevent you from making rushed decisions and help you to keep your code working as expected.
One more thing to consider is, that even though we have defined types for our parameters, the generated JavaScript used at runtime does not contain the type checks. So if, for example, the _Operation_ parameter's value comes from an external interface, there is no definite guarantee that it will be one of the allowed values. Therefore, it's still better to include error handling and be prepared for the unexpected to happen. In this case, when there are multiple possible accepted values and all unexpected ones should result in an error, the
The code of our calculator should look something like this:

```
type Operation = 'multiply' | 'add' | 'divide';

const calculator = (a: number, b: number, op: Operation) : number => {  switch(op) {
    case 'multiply':
      return a * b;
    case 'divide':
      if (b === 0) throw new Error('Can\'t divide by 0!');      return a / b;
    case 'add':
      return a + b;
    default:
      throw new Error('Operation is not multiply, add or divide!');  }
}

try {
  console.log(calculator(1, 5 , 'divide'));
} catch (error: unknown) {
  let errorMessage = 'Something went wrong: '
  if (error instanceof Error) {
    errorMessage += error.message;
  }
  console.log(errorMessage);
}copy
```

### Type narrowing
The default type of the catch block parameter _error_ is _unknown_. The _any_. Anything is assignable to _unknown_ , but _unknown_ isn’t assignable to anything but itself and _any_ without a type assertion or a control flow-based type narrowing. Likewise, no operations are permitted on an _unknown_ without first asserting or narrowing it to a more specific type.
Both the possible causes of exception (wrong operator or division by zero) will throw an
If our code would be JavaScript, we could print the error message by just referring to the field _error_ as follows:

```
try {
  console.log(calculator(1, 5 , 'divide'));
} catch (error) {
  console.log('Something went wrong: ' + error.message);}copy
```

Since the default type of the _error_ object in TypeScript is _unknown_ , we have to

```
try {
  console.log(calculator(1, 5 , 'divide'));
} catch (error: unknown) {
  let errorMessage = 'Something went wrong: '
  // here we can not use error.message
  if (error instanceof Error) {    // the type is narrowed and we can refer to error.message
    errorMessage += error.message;  }
  // here we can not use error.message

  console.log(errorMessage);
}copy
```

Here the narrowing was done with the
### Accessing command line arguments
The programs we have written are alright, but it sure would be better if we could use command-line arguments instead of always having to change the code to calculate different things.
Let's try it out, as we would in a regular Node application, by accessing _process.argv_. If you are using a recent npm-version (7.0 or later), there are no problems, but with an older setup something is not right:
![vs code error cannot find name process need to install type definitions](../assets/8925698555cfa232.png)
So what is the problem with older setups?
### @types/{npm_package}
Let's return to the basic idea of TypeScript. TypeScript expects all globally-used code to be typed, as it does for your code when your project has a reasonable configuration. The TypeScript library itself contains only typings for the code of the TypeScript package. It is possible to write your own typing for a library, but that is rarely needed - since the TypeScript community has done it for us!
As with npm, the TypeScript world also celebrates open-source code. The community is active and continuously reacting to updates and changes in commonly used npm packages. You can almost always find the typings for npm packages, so you don't have to create types for all of your thousands of dependencies alone.
Usually, types for existing packages can be found from the _@types_ organization within npm, and you can add the relevant types to your project by installing an npm package with the name of your package with a _@types/_ prefix. For example:

```
npm install --save-dev @types/react @types/express @types/lodash @types/jest @types/mongoosecopy
```

and so on and so on. The _@types/_ are maintained by
Sometimes, an npm package can also include its types within the code and, in that case, installing the corresponding _@types/_ is not necessary.
> **NB:** Since the typings are only used before compilation, the typings are not needed in the production build and they should _always_ be in the devDependencies of the package.json.
Since the global variable _process_ is defined by the Node itself, we get its typings from the package _@types/node_.
Since version 10.0 _ts-node_ has defined _@types/node_ as a

```
npm install --save-dev @types/nodecopy
```

When the package _@types/node_ is installed, the compiler does not complain about the variable _process_. Note that there is no need to require the types to the code, the installation of the package is enough!
### Improving the project
Next, let's add npm scripts to run our two programs _multiplier_ and _calculator_ :

```
{
  "name": "fs-open",
  "version": "1.0.0",
  "description": "",
  "main": "index.ts",
  "scripts": {
    "ts-node": "ts-node",
    "multiply": "ts-node multiplier.ts",    "calculate": "ts-node calculator.ts"  },
  "author": "",
  "license": "ISC",
  "devDependencies": {
    "ts-node": "^10.5.0",
    "typescript": "^4.5.5"
  }
}copy
```

We can get the multiplier to work with command-line parameters with the following changes:

```
const multiplicator = (a: number, b: number, printText: string) => {
  console.log(printText,  a * b);
}

const a: number = Number(process.argv[2])
const b: number = Number(process.argv[3])
multiplicator(a, b, `Multiplied ${a} and ${b}, the result is:`);copy
```

And we can run it with:

```
npm run multiply 5 2copy
```

If the program is run with parameters that are not of the right type, e.g.

```
npm run multiply 5 lolcopy
```

it "works" but gives us the answer:

```
Multiplied 5 and NaN, the result is: NaNcopy
```

The reason for this is, that _Number('lol')_ returns _NaN_ , which is actually of type _number_ , so TypeScript has no power to rescue us from this kind of situation.
To prevent this kind of behavior, we have to validate the data given to us from the command line.
The improved version of the multiplicator looks like this:

```
interface MultiplyValues {
  value1: number;
  value2: number;
}

const parseArguments = (args: string[]): MultiplyValues => {
  if (args.length < 4) throw new Error('Not enough arguments');
  if (args.length > 4) throw new Error('Too many arguments');

  if (!isNaN(Number(args[2])) && !isNaN(Number(args[3]))) {
    return {
      value1: Number(args[2]),
      value2: Number(args[3])
    }
  } else {
    throw new Error('Provided values were not numbers!');
  }
}

const multiplicator = (a: number, b: number, printText: string) => {
  console.log(printText,  a * b);
}

try {
  const { value1, value2 } = parseArguments(process.argv);
  multiplicator(value1, value2, `Multiplied ${value1} and ${value2}, the result is:`);
} catch (error: unknown) {
  let errorMessage = 'Something bad happened.'
  if (error instanceof Error) {
    errorMessage += ' Error: ' + error.message;
  }
  console.log(errorMessage);
}copy
```

When we now run the program:

```
npm run multiply 1 lolcopy
```

we get a proper error message:

```
Something bad happened. Error: Provided values were not numbers!copy
```

There is quite a lot going on in the code. The most important addition is the function _parseArguments_ which ensures that the parameters given to _multiplicator_ are of the right type. If not, an exception is thrown with a descriptive error message.
The definition of the function has a couple of interesting things:

```
const parseArguments = (args: string[]): MultiplyValues => {
  // ...
}copy
```

Firstly, the parameter _args_ is an
The return value of the function has the type _MultiplyValues_ , which is defined as follows:

```
interface MultiplyValues {
  value1: number;
  value2: number;
}copy
```

The definition utilizes TypeScript's _value1_ and _value2_ , which should both be of type number.
### The alternative array syntax
Note that there is also an alternative syntax for

```
let values: number[];copy
```

we could use the "generics syntax" and write

```
let values: Array<number>;copy
```

In this course we shall mostly be following the convention enforced by the Eslint rule
### Exercises 9.1-9.3
#### setup
Exercises 9.1-9.7. will all be made in the same node project. Create the project in an empty directory with _npm init_ and install the ts-node and typescript packages. Also, create the file _tsconfig.json_ in the directory with the following content:

```
{
  "compilerOptions": {
    "noImplicitAny": true,
  }
}copy
```

The compiler option
#### 9.1 Body mass index
Create the code of this exercise in the file _bmiCalculator.ts_.
Write a function _calculateBmi_ that calculates a
Call the function in the same file with hard-coded parameters and print out the result. The code

```
console.log(calculateBmi(180, 74))copy
```

should print the following message:

```
Normal rangecopy
```

Create an npm script for running the program with the command _npm run calculateBmi_.
#### 9.2 Exercise calculator
Create the code of this exercise in file _exerciseCalculator.ts_.
Write a function _calculateExercises_ that calculates the average time of _daily exercise hours_ , compares it to the _target amount_ of daily hours and returns an object that includes the following values:

- the number of days
- the number of training days
- the original target value
- the calculated average time
- boolean value describing if the target was reached
- a rating between the numbers 1-3 that tells how well the hours are met. You can decide on the metric on your own.
- a text value explaining the rating, you can come up with the explanations


The daily exercise hours are given to the function as an

```
[3, 0, 2, 4.5, 0, 3, 1]copy
```

For the Result object, you should create an
If you call the function with parameters _[3, 0, 2, 4.5, 0, 3, 1]_ and _2_ , it should return:

```
{ 
  periodLength: 7,
  trainingDays: 5,
  success: false,
  rating: 2,
  ratingDescription: 'not too bad but could be better',
  target: 2,
  average: 1.9285714285714286
}copy
```

Create an npm script, _npm run calculateExercises_ , to call the function with hard-coded values.
#### 9.3 Command line
Change the previous exercises so that you can give the parameters of _bmiCalculator_ and _exerciseCalculator_ as command-line arguments.
Your program could work eg. as follows:

```
$ npm run calculateBmi 180 91

Overweightcopy
```

and:

```
$ npm run calculateExercises 2 1 0 2 4.5 0 3 1 0 4

{
  periodLength: 9,
  trainingDays: 6,
  success: false,
  rating: 2,
  ratingDescription: 'not too bad but could be better',
  target: 2,
  average: 1.7222222222222223
}copy
```

In the example, the _first argument_ is the target value.
Handle exceptions and errors appropriately. The _exerciseCalculator_ should accept inputs of varied lengths. Determine by yourself how you manage to collect all needed input.
A couple of things to notice:
If you define helper functions in other modules, you should use the

```
import { isNotNumber } from "./utils";copy
```

and exporting

```
export const isNotNumber = (argument: any): boolean =>
  isNaN(Number(argument));

export default "this is the default..."copy
```

Another note: somehow surprisingly TypeScript does not allow to define the same variable in many files at a "block-scope", that is, outside functions (or classes):
![vs code showing error cannot redeclare block-scoped variable x](../assets/149eb5457ac1d9ab.png)
This is actually not quite true. This rule applies only to files that are treated as "scripts". A file is a script if it does not contain any export or import statements. If a file has those, then the file is treated as a _and_ the variables do not get defined in the block scope.
### More about tsconfig
We have so far used only one tsconfig rule
As mentioned, the
Let's specify the following configuration in our _tsconfig.json_ file:

```
{
  "compilerOptions": {
    "target": "ES2022",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitAny": true,    "esModuleInterop": true,
    "moduleResolution": "node"
  }
}copy
```

Do not worry too much about the _compilerOptions_ , they will be under closer inspection later on.
You can find explanations for each of the configurations from the TypeScript documentation or from the really handy
### Adding Express to the mix
Right now, we are in a pretty good place. Our project is set up and we have two executable calculators in it. However, since we aim to learn FullStack development, it is time to start working with some HTTP requests.
Let us start by installing Express:

```
npm install expresscopy
```

and then add the _start_ script to package.json:

```
{
  // ..
  "scripts": {
    "ts-node": "ts-node",
    "multiply": "ts-node multiplier.ts",
    "calculate": "ts-node calculator.ts",
    "start": "ts-node index.ts"  },
  // ..
}copy
```

Now we can create the file _index.ts_ , and write the HTTP GET _ping_ endpoint to it:

```
const express = require('express');
const app = express();

app.get('/ping', (req, res) => {
  res.send('pong');
});

const PORT = 3003;

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});copy
```

Everything else seems to be ok but, as you'd expect, the _req_ and _res_ parameters of _app.get_ need typing. If you look carefully, VSCode is also complaining about the importing of Express. You can see a short yellow line of dots under _require_. Let's hover over the problem:
![vscode warning to change require to import](../assets/9ba47c6d1902f6c8.png)
The complaint is that the _'require' call may be converted to an import_. Let us follow the advice and write the import as follows:

```
import express from 'express';copy
```

**NB** : VSCode offers you the possibility to fix the issues automatically by clicking the _Quick Fix..._ button. Keep your eyes open for these helpers/quick fixes; listening to your editor usually makes your code better and easier to read. The automatic fixes for issues can be a major time saver as well.
Now we run into another problem, the compiler complains about the import statement. Once again, the editor is our best friend when trying to find out what the issue is:
![vscode error about not finding express](../assets/cde8406a3f7c565f.png)
We haven't installed types for _express_. Let's do what the suggestion says and run:

```
npm install --save-dev @types/expresscopy
```

There should not be any errors remaining. Note that you may need to reopen the file in the editor to get VS Code in sync.
Let's take a look at what changed.
When we hover over the _require_ statement, we can see that the compiler interprets everything express-related to be of type _any_.
![vscode showing problem of implicitly having any type](../assets/71bd3f9036c15bee.png)
Whereas when we use _import_ , the editor knows the actual types:
![vscode showing req is of type Request](../assets/a8eb318138739896.png)
Which import statement to use depends on the export method used in the imported package.
A good rule of thumb is to try importing a module using the _import_ statement first. We have already used this method in the frontend. If _import_ does not work, try a combined method: _import ... = require('...')_.
We strongly suggest you read more about TypeScript modules
There is one more problem with the code:
![vscode showing req declared but never read](../assets/9c2c1f638a3f112d.png)
This is because we banned unused parameters in our _tsconfig.json_ :

```
{
  "compilerOptions": {
    "target": "ES2022",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitAny": true,
    "esModuleInterop": true,
    "moduleResolution": "node"
  }
}copy
```

This configuration might create problems if you have library-wide predefined functions that require declaring a variable even if it's not used at all, as is the case here. Fortunately, this issue has already been solved on the configuration level. Once again hovering over the issue gives us a solution. This time we can just click the quick fix button:
![vscode quickfix to add underscore to variable](../assets/1ef7cf16839a164f.png)
If it is absolutely impossible to get rid of an unused variable, you can prefix it with an underscore to inform the compiler you have thought about it and there is nothing you can do.
Let's rename the _req_ variable to __req_. Finally, we are ready to start the application. It seems to work fine:
![browser result showing pong on /ping](../assets/055e677d12a676f4.png)
To simplify the development, we should enable _auto-reloading_ to improve our workflow. In this course, you have already used _nodemon_ , but ts-node has an alternative called _ts-node-dev_. It is meant to be used only with a development environment that takes care of recompilation on every change, so restarting the application won't be necessary.
Let's install _ts-node-dev_ to our development dependencies:

```
npm install --save-dev ts-node-devcopy
```

Add a script to _package.json_ :

```
{
  // ...
  "scripts": {
      // ...
      "dev": "ts-node-dev index.ts",  },
  // ...
}copy
```

And now, by running _npm run dev_ , we have a working, auto-reloading development environment for our project!
### Exercises 9.4-9.5
#### 9.4 Express
Add Express to your dependencies and create an HTTP GET endpoint _hello_ that answers 'Hello Full Stack!'
The web app should be started with the commands _npm start_ in production mode and _npm run dev_ in development mode. The latter should also use _ts-node-dev_ to run the app.
Replace also your existing _tsconfig.json_ file with the following content:

```
{
  "compilerOptions": {
    "noImplicitAny": true,
    "noImplicitReturns": true,
    "strictNullChecks": true,
    "strictPropertyInitialization": true,
    "strictBindCallApply": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitThis": true,
    "alwaysStrict": true,
    "esModuleInterop": true,
    "declaration": true,
  }
}copy
```

Make sure there aren't any errors!
#### 9.5 WebBMI
Add an endpoint for the BMI calculator that can be used by doing an HTTP GET request to the endpoint _bmi_ and specifying the input with
The response is a JSON of the form:

```
{
  weight: 72,
  height: 180,
  bmi: "Normal range"
}copy
```

See the
If the query parameters of the request are of the wrong type or missing, a response with proper status code and an error message is given:

```
{
  error: "malformatted parameters"
}copy
```

Do not copy the calculator code to file _index.ts_ ; instead, make it a _index.ts_.
For _calculateBmi_ to work correctly from both the command line and the endpoint, consider adding a check _require.main === module_ to the file _bmiCalculator.ts_. It tests whether the module is main, i.e. it is run directly from the command line (in our case, _npm run calculateBmi_), or it is used by other modules that import functions from it (e.g. _index.ts_). Parsing command-line arguments makes sense only if the module is main. Without this condition, you might see argument validation errors when starting the application via _npm start_ or _npm run dev_.
See the Node
### The horrors of _any_
Now that we have our first endpoints completed, you might notice that we have used barely any TypeScript in these small examples. When examining the code a bit closer, we can see a few dangers lurking there.
Let's add the HTTP POST endpoint _calculate_ to our app:

```
import { calculator } from './calculator';

app.use(express.json());

// ...

app.post('/calculate', (req, res) => {
  const { value1, value2, op } = req.body;

  const result = calculator(value1, value2, op);
  res.send({ result });
});copy
```

To get this working, we must add an _export_ to the function _calculator_ :

```
export const calculator = (a: number, b: number, op: Operation) : number => {copy
```

When you hover over the _calculate_ function, you can see the typing of the _calculator_ even though the code itself does not contain any typing:
![vscode showing calculator types when hovering the function](../assets/eaf0c3c89510226e.png)
But if you hover over the values parsed from the request, an issue arises:
![vscode problematically showing any when hovering over values parsed in to calculate](../assets/751f7f5859f29207.png)
All of the variables have the type _any_. It is not all that surprising, as no one has given them a type yet. There are a couple of ways to fix this, but first, we have to consider why this is accepted and where the type _any_ came from.
In TypeScript, every untyped variable whose type cannot be inferred implicitly becomes of type _whatever_ type. Things become implicitly any type quite often when one forgets to type functions.
We can also explicitly type things _any_. The only difference between the implicit and explicit any type is how the code looks; the compiler does not care about the difference.
Programmers however see the code differently when _any_ is explicitly enforced than when it is implicitly inferred. Implicit _any_ typings are usually considered problematic since it is quite often due to the coder forgetting to assign types (or being too lazy to do it), and it also means that the full power of TypeScript is not properly exploited.
This is why the configuration rule

```
const a : any = /* no clue what the type will be! */.copy
```

We already have _noImplicitAny: true_ configured in our example, so why does the compiler not complain about the implicit _any_ types? The reason is that the _body_ field of an Express _any_. The same is true for the _request.query_ field that Express uses for the query parameters.
What if we would like to restrict developers from using the _any_ type? Fortunately, we have methods other than _tsconfig.json_ to enforce a coding style. What we can do is use _ESlint_ to manage our code. Let's install ESlint and its TypeScript extensions:

```
npm install --save-dev eslint @eslint/js @types/eslint__js typescript typescript-eslintcopy
```

We will configure ESlint to _eslint.config.mjs_ :

```
import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';

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
  rules: {
    '@typescript-eslint/no-explicit-any': 'error',
  },
});copy
```

Let us also set up a _lint_ npm script to inspect the files by modifying the _package.json_ file:

```
{
  // ...
  "scripts": {
      "start": "ts-node index.ts",
      "dev": "ts-node-dev index.ts",
      "lint": "eslint ."      //  ...
  },
  // ...
}copy
```

Now lint will complain if we try to define a variable of type _any_ :
![vscode showing ESlint complaining about using the any type](../assets/f145a7fbdacfbae9.png)
On top of the recommended settings, we should try to get familiar with the coding style required in this part and _set the semicolon at the end of each line of code to be required_. For that, we should install and configure

```
npm install --save-dev @stylistic/eslint-plugincopy
```

Our final _eslint.config.mjs_ looks as follows:

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

Quite a few semicolons are missing, but those are easy to add. We also have to solve the ESlint issues concerning the _any_ type:
![vscode error unsafe assignment of any value](../assets/99305c6941440488.png)
We could and probably should disable some ESlint rules to get the data from the request body.
Disabling _@typescript-eslint/no-unsafe-assignment_ for the destructuring assignment and calling the

```
app.post('/calculate', (req, res) => {
  // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment  const { value1, value2, op } = req.body;

  const result = calculator(Number(value1), Number(value2), op);  res.send({ result });
});copy
```

However this still leaves one problem to deal with, the last parameter in the function call is not safe:
![vscode showing unsafe argument of any type assigned to the parameter of type Operation](../assets/c7449a46afbd8d22.png)
We can just disable another ESlint rule to get rid of that:

```
app.post('/calculate', (req, res) => {
  // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
  const { value1, value2, op } = req.body;

  // eslint-disable-next-line @typescript-eslint/no-unsafe-argument  const result = calculator(Number(value1), Number(value2), op);
  res.send({ result });
});copy
```

We now have ESlint silenced but we are totally at the mercy of the user. We most definitively should do some validation to the post data and give a proper error message if the data is invalid:

```
app.post('/calculate', (req, res) => {
  // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
  const { value1, value2, op } = req.body;

  if ( !value1 || isNaN(Number(value1)) ) {    return res.status(400).send({ error: '...'});  }
  // more validations here...

  // eslint-disable-next-line @typescript-eslint/no-unsafe-argument
  const result = calculator(Number(value1), Number(value2), op);
  return res.send({ result });
});copy
```

We shall see later in this part some techniques on how the _any_ typed data (eg. the input an app receives from the user) can be _narrowed_ to a more specific type (such as number). With a proper narrowing of types, there is no more need to silence the ESlint rules.
### Type assertion
Using a _calculator.ts_ :

```
export type Operation = 'multiply' | 'add' | 'divide';copy
```

Now we can import the type and use the type assertion _as_ to tell the TypeScript compiler what type a variable has:

```
import { calculator, Operation } from './calculator';
app.post('/calculate', (req, res) => {
  // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
  const { value1, value2, op } = req.body;

  // validate the data here

  // assert the type
  const operation = op as Operation;
  const result = calculator(Number(value1), Number(value2), operation);
  return res.send({ result });
});copy
```

The defined constant _operation_ has now the type _Operation_ and the compiler is perfectly happy, no quieting of the Eslint rule is needed on the following function call. The new variable is actually not needed, the type assertion can be done when an argument is passed to the function:

```
app.post('/calculate', (req, res) => {
  // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
  const { value1, value2, op } = req.body;

  // validate the data here

  const result = calculator(
    Number(value1), Number(value2), op as Operation  );

  return res.send({ result });
});copy
```

Using a type assertion (or quieting an Eslint rule) is always a bit risky. It leaves the TypeScript compiler off the hook, the compiler just trusts that we as developers know what we are doing. If the asserted type _does not_ have the right kind of value, the result will be a runtime error, so one must be pretty careful when validating the data if a type assertion is used.
In the next chapter, we shall have a look at
### Exercises 9.6-9.7
#### 9.6 Eslint
Configure your project to use the above ESlint settings and fix all the warnings.
#### 9.7 WebExercises
Add an endpoint to your app for the exercise calculator. It should be used by doing a HTTP POST request to the endpoint

```
{
  "daily_exercises": [1, 0, 2, 0, 3, 0, 2.5],
  "target": 2.5
}copy
```

The response is a JSON of the following form:

```
{
    "periodLength": 7,
    "trainingDays": 4,
    "success": false,
    "rating": 1,
    "ratingDescription": "bad",
    "target": 2.5,
    "average": 1.2142857142857142
}copy
```

If the body of the request is not in the right form, a response with the proper status code and an error message are given. The error message is either

```
{
  error: "parameters missing"
}copy
```

or

```
{
  error: "malformatted parameters"
}copy
```

depending on the error. The latter happens if the input values do not have the right type, i.e. they are not numbers or convertible to numbers.
In this exercise, you might find it beneficial to use the _explicit any_ type when handling the data in the request body. Our ESlint configuration is preventing this but you may unset this rule for a particular line by inserting the following comment as the previous line:

```
// eslint-disable-next-line @typescript-eslint/no-explicit-anycopy
```

You might also get in trouble with rules _no-unsafe-member-access_ and _no-unsafe-assignment_. These rules may be ignored in this exercise.
Note that you need to have a correct setup to get the request body; see [part 3](../part3/01-node-js-and-express-receiving-data.md).
[Part 9a **Previous part**](../part9/01-background-and-introduction.md)[Part 9c **Next part**](../part9/01-typing-an-express-app.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)
