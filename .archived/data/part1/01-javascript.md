---{
  "title": "JavaScript",
  "source_url": "https://fullstackopen.com/en/part1/java_script",
  "crawl_timestamp": "2025-10-04T19:15:40Z",
  "checksum": "46fcd24d9537c6ec3ecaf23cfabc6ba3329714ae330b09b9aa670f13550e53fa"
}
---[Skip to content](../part1/01-java-script-course-main-content.md)
[{() => fs}](https://fullstackopen.com/en/)

- [About course](../about/01-about.md)
- [Course contents](../#course-contents/01-course-contents.md)
- [FAQ](../faq/01-faq.md)
- [Partners](../companies/01-companies.md)
- [Challenge](../challenge/01-challenge.md)
[Search from the material](../search/01-search.md)Toggle dark theme
Select languageSuomi English 中文 Español Français Português(BR)

[Fullstack](../#course-contents/01-course-contents.md)
[Part 1](../part1/01-part1.md)
JavaScript
[a Introduction to React](../part1/01-introduction-to-react.md)
b JavaScript

- [Variables](../part1/01-java-script-variables.md)
- [Arrays](../part1/01-java-script-arrays.md)
- [Objects](../part1/01-java-script-objects.md)
- [Functions](../part1/01-java-script-functions.md)
- [Exercises 1.3.-1.5.](../part1/01-java-script-exercises-1-3-1-5.md)
- [Object methods and "this"](../part1/01-java-script-object-methods-and-this.md)
- [Classes](../part1/01-java-script-classes.md)
- [JavaScript materials](../part1/01-java-script-java-script-materials.md)


[c Component state, event handlers](../part1/01-component-state-event-handlers.md)[d A more complex state, debugging React apps](../part1/01-a-more-complex-state-debugging-react-apps.md)
b
# JavaScript
During the course, we have a goal and a need to learn a sufficient amount of JavaScript in addition to web development.
JavaScript has advanced rapidly in the last few years and in this course, we use features from the newer versions. The official name of the JavaScript standard is
Browsers do not yet support all of JavaScript's newest features. Due to this fact, a lot of code run in browsers has been _transpiled_ from a newer version of JavaScript to an older, more compatible version.
Today, the most popular way to do transpiling is by using [part 7](../part7/01-part7.md) of this course.
The code is written into files ending with _.js_ that are run by issuing the command _node name_of_file.js_
It is also possible to write JavaScript code into the Node.js console, which is opened by typing _node_ in the command line, as well as into the browser's developer tool console.
JavaScript is sort of reminiscent, both in name and syntax, to Java. But when it comes to the core mechanism of the language they could not be more different. Coming from a Java background, the behavior of JavaScript can seem a bit alien, especially if one does not make the effort to look up its features.
In certain circles, it has also been popular to attempt "simulating" Java features and design patterns in JavaScript. We do not recommend doing this as the languages and respective ecosystems are ultimately very different.
### Variables
In JavaScript there are a few ways to go about defining variables:

```
const x = 1
let y = 5

console.log(x, y)   // 1 5 are printed
y += 10
console.log(x, y)   // 1 15 are printed
y = 'sometext'
console.log(x, y)   // 1 sometext are printed
x = 4               // causes an errorcopy
```

_constant_ for which the value can no longer be changed. On the other hand,
In the example above, we also see that the variable's data type can change during execution. At the start, _y_ stores an integer; at the end, it stores a string.
It is also possible to define variables in JavaScript using the keyword
### Arrays
An

```
const t = [1, -1, 3]

t.push(5)

console.log(t.length) // 4 is printed
console.log(t[1])     // -1 is printed

t.forEach(value => {
  console.log(value)  // numbers 1, -1, 3, 5 are printed, each on its own line
})                    copy
```

Notable in this example is the fact that although a variable declared with const cannot be reassigned to a different value, the contents of the object it references can still be modified. This is because the const declaration ensures the immutability of the reference itself, not the data it points to. Think of it like changing the furniture inside a house, while the address of the house remains the same.
One way of iterating through the items of the array is using _forEach_ as seen in the example. _forEach_ receives a _function_ defined using the arrow syntax as a parameter.

```
value => {
  console.log(value)
}copy
```

forEach calls the function _for each of the items in the array_ , always passing the individual item as an argument. The function as the argument of forEach may also receive
In the previous example, a new item was added to the array using the method

```
const t = [1, -1, 3]

const t2 = t.concat(5)  // creates new array

console.log(t)  // [1, -1, 3] is printed
console.log(t2) // [1, -1, 3, 5] is printedcopy
```

The method call _t.concat(5)_ does not add a new item to the old array but returns a new array which, besides containing the items of the old array, also contains the new item.
There are plenty of useful methods defined for arrays. Let's look at a short example of using the

```
const t = [1, 2, 3]

const m1 = t.map(value => value * 2)
console.log(m1)   // [2, 4, 6] is printedcopy
```

Based on the old array, map creates a _new array_ , for which the function given as a parameter is used to create the items. In the case of this example, the original value is multiplied by two.
Map can also transform the array into something completely different:

```
const m2 = t.map(value => '<li>' + value + '</li>')
console.log(m2)  
// [ '<li>1</li>', '<li>2</li>', '<li>3</li>' ] is printedcopy
```

Here an array filled with integer values is transformed into an array containing strings of HTML using the map method. In [part 2](../part2/01-part2.md) of this course, we will see that map is used quite frequently in React.
Individual items of an array are easy to assign to variables with the help of the

```
const t = [1, 2, 3, 4, 5]

const [first, second, ...rest] = t

console.log(first, second)  // 1 2 is printed
console.log(rest)          // [3, 4, 5] is printedcopy
```

Above, the variable _first_ is assigned the first integer of the array and the variable _second_ is assigned the second integer of the array. The variable _rest_ "collects" the remaining integers into its own array.
### Objects
There are a few different ways of defining objects in JavaScript. One very common method is using

```
const object1 = {
  name: 'Arto Hellas',
  age: 35,
  education: 'PhD',
}

const object2 = {
  name: 'Full Stack web application development',
  level: 'intermediate studies',
  size: 5,
}

const object3 = {
  name: {
    first: 'Dan',
    last: 'Abramov',
  },
  grades: [2, 3, 5, 3],
  department: 'Stanford University',
}copy
```

The values of the properties can be of any type, like integers, strings, arrays, objects...
The properties of an object are referenced by using the "dot" notation, or by using brackets:

```
console.log(object1.name)         // Arto Hellas is printed
const fieldName = 'age'
console.log(object1[fieldName])    // 35 is printedcopy
```

You can also add properties to an object on the fly by either using dot notation or brackets:

```
object1.address = 'Helsinki'
object1['secret number'] = 12341copy
```

The latter of the additions has to be done by using brackets because when using dot notation, _secret number_ is not a valid property name because of the space character.
Naturally, objects in JavaScript can also have methods. However, during this course, we do not need to define any objects with methods of their own. This is why they are only discussed briefly during the course.
Objects can also be defined using so-called constructor functions, which results in a mechanism reminiscent of many other programming languages, e.g. Java's classes. Despite this similarity, JavaScript does not have classes in the same sense as object-oriented programming languages. There has been, however, the addition of the _class syntax_ starting from version ES6, which in some cases helps structure object-oriented classes.
### Functions
We have already become familiar with defining arrow functions. The complete process, without cutting corners, of defining an arrow function is as follows:

```
const sum = (p1, p2) => {
  console.log(p1)
  console.log(p2)
  return p1 + p2
}copy
```

and the function is called as can be expected:

```
const result = sum(1, 5)
console.log(result)copy
```

If there is just a single parameter, we can exclude the parentheses from the definition:

```
const square = p => {
  console.log(p)
  return p * p
}copy
```

If the function only contains a single expression then the braces are not needed. In this case, the function only returns the result of its only expression. Now, if we remove console printing, we can further shorten the function definition:

```
const square = p => p * pcopy
```

This form is particularly handy when manipulating arrays - e.g. when using the map method:

```
const t = [1, 2, 3]
const tSquared = t.map(p => p * p)
// tSquared is now [1, 4, 9]copy
```

The arrow function feature was added to JavaScript in 2015, with version _function_.
There are two ways to reference the function; one is giving a name in a

```
function product(a, b) {
  return a * b
}

const result = product(2, 6)
// result is now 12copy
```

The other way to define the function is by using a

```
const average = function(a, b) {
  return (a + b) / 2
}

const result = average(2, 5)
// result is now 3.5copy
```

During this course, we will define all functions using the arrow syntax.
### Exercises 1.3.-1.5
_We continue building the application that we started working on in the previous exercises. You can write the code into the same project since we are only interested in the final state of the submitted application._
**Pro-tip:** you may run into issues when it comes to the structure of the _props_ that components receive. A good way to make things more clear is by printing the props to the console, e.g. as follows:

```
const Header = (props) => {
  console.log(props)  return <h1>{props.course}</h1>
}copy
```

If and _when_ you encounter an error message
> _Objects are not valid as a React child_
keep in mind the things told [here](../part1/01-introduction-to-react-do-not-render-objects.md).
#### 1.3: Course Information step 3
Let's move forward to using objects in our application. Modify the variable definitions of the _App_ component as follows and also refactor the application so that it still works:

```
const App = () => {
  const course = 'Half Stack application development'
  const part1 = {
    name: 'Fundamentals of React',
    exercises: 10
  }
  const part2 = {
    name: 'Using props to pass data',
    exercises: 7
  }
  const part3 = {
    name: 'State of a component',
    exercises: 14
  }

  return (
    <div>
      ...
    </div>
  )
}copy
```

#### 1.4: Course Information step 4
Place the objects into an array. Modify the variable definitions of _App_ into the following form and modify the other parts of the application accordingly:

```
const App = () => {
  const course = 'Half Stack application development'
  const parts = [
    {
      name: 'Fundamentals of React',
      exercises: 10
    },
    {
      name: 'Using props to pass data',
      exercises: 7
    },
    {
      name: 'State of a component',
      exercises: 14
    }
  ]

  return (
    <div>
      ...
    </div>
  )
}copy
```

**NB** at this point _you can assume that there are always three items_ , so there is no need to go through the arrays using loops. We will come back to the topic of rendering components based on items in arrays with a more thorough exploration in the [next part of the course](../part2/01-part2.md).
However, do not pass different objects as separate props from the _App_ component to the components _Content_ and _Total_. Instead, pass them directly as an array:

```
const App = () => {
  // const definitions

  return (
    <div>
      <Header course={course} />
      <Content parts={parts} />
      <Total parts={parts} />
    </div>
  )
}copy
```

#### 1.5: Course Information step 5
Let's take the changes one step further. Change the course and its parts into a single JavaScript object. Fix everything that breaks.

```
const App = () => {
  const course = {
    name: 'Half Stack application development',
    parts: [
      {
        name: 'Fundamentals of React',
        exercises: 10
      },
      {
        name: 'Using props to pass data',
        exercises: 7
      },
      {
        name: 'State of a component',
        exercises: 14
      }
    ]
  }

  return (
    <div>
      ...
    </div>
  )
}copy
```

### Object methods and "this"
Because this course uses a version of React containing React Hooks we do not need to define objects with methods. **The contents of this chapter are not relevant to the course** but are certainly in many ways good to know. In particular, when using older versions of React one must understand the topics of this chapter.
Arrow functions and functions defined using the _function_ keyword vary substantially when it comes to how they behave with respect to the keyword
We can assign methods to an object by defining properties that are functions:

```
const arto = {
  name: 'Arto Hellas',
  age: 35,
  education: 'PhD',
  greet: function() {    console.log('hello, my name is ' + this.name)  },}

arto.greet()  // "hello, my name is Arto Hellas" gets printedcopy
```

Methods can be assigned to objects even after the creation of the object:

```
const arto = {
  name: 'Arto Hellas',
  age: 35,
  education: 'PhD',
  greet: function() {
    console.log('hello, my name is ' + this.name)
  },
}

arto.growOlder = function() {  this.age += 1}
console.log(arto.age)   // 35 is printed
arto.growOlder()
console.log(arto.age)   // 36 is printedcopy
```

Let's slightly modify the object:

```
const arto = {
  name: 'Arto Hellas',
  age: 35,
  education: 'PhD',
  greet: function() {
    console.log('hello, my name is ' + this.name)
  },
  doAddition: function(a, b) {    console.log(a + b)  },}

arto.doAddition(1, 4)        // 5 is printed

const referenceToAddition = arto.doAddition
referenceToAddition(10, 15)   // 25 is printedcopy
```

Now the object has the method _doAddition_ which calculates the sum of numbers given to it as parameters. The method is called in the usual way, using the object _arto.doAddition(1, 4)_ or by storing a _method reference_ in a variable and calling the method through the variable: _referenceToAddition(10, 15)_.
If we try to do the same with the method _greet_ we run into an issue:

```
arto.greet()       // "hello, my name is Arto Hellas" gets printed

const referenceToGreet = arto.greet
referenceToGreet() // prints "hello, my name is undefined"copy
```

When calling the method through a reference, the method loses knowledge of what the original _this_ was. Contrary to other languages, in JavaScript the value of _how the method is called_. When calling the method through a reference, the value of _this_ becomes the so-called
Losing track of _this_ when writing JavaScript code brings forth a few potential issues. Situations often arise where React or Node (or more specifically the JavaScript engine of the web browser) needs to call some method in an object that the developer has defined. However, in this course, we avoid these issues by using "this-less" JavaScript.
One situation leading to the "disappearance" of _this_ arises when we set a timeout to call the _greet_ function on the _arto_ object, using the

```
const arto = {
  name: 'Arto Hellas',
  greet: function() {
    console.log('hello, my name is ' + this.name)
  },
}

setTimeout(arto.greet, 1000)copy
```

As mentioned, the value of _this_ in JavaScript is defined based on how the method is being called. When _setTimeout_ is calling the method, it is the JavaScript engine that actually calls the method and, at that point, _this_ refers to the global object.
There are several mechanisms by which the original _this_ can be preserved. One of these is using a method called

```
setTimeout(arto.greet.bind(arto), 1000)copy
```

Calling _arto.greet.bind(arto)_ creates a new function where _this_ is bound to point to Arto, independent of where and how the method is being called.
Using _this_. They should not, however, be used as methods for objects because then _this_ does not work at all. We will come back later to the behavior of _this_ in relation to arrow functions.
If you want to gain a better understanding of how _this_ works in JavaScript, the Internet is full of material about the topic, e.g. the screencast series
### Classes
As mentioned previously, there is no class mechanism in JavaScript like the ones in object-oriented programming languages. There are, however, features to make "simulating" object-oriented
Let's take a quick look at the _class syntax_ that was introduced into JavaScript with ES6, which substantially simplifies the definition of classes (or class-like things) in JavaScript.
In the following example we define a "class" called Person and two Person objects:

```
class Person {
  constructor(name, age) {
    this.name = name
    this.age = age
  }
  greet() {
    console.log('hello, my name is ' + this.name)
  }
}

const adam = new Person('Adam Ondra', 29)
adam.greet()

const janja = new Person('Janja Garnbret', 23)
janja.greet()copy
```

When it comes to syntax, JavaScript classes and the instances created from them are very reminiscent of how classes and objects work in Java. Their behavior is also quite similar to Java objects. At their core, however, they are still plain JavaScript objects built on _Object_ , because JavaScript fundamentally defines only a limited set of types:
The introduction of the class syntax was a controversial addition. Check out
The ES6 class syntax is used a lot in "old" React and also in Node.js, hence an understanding of it is beneficial even in this course. However, since we are using the new
### JavaScript materials
There exist both good and poor guides for JavaScript on the Internet. Most of the links on this page relating to JavaScript features reference
It is highly recommended to immediately read
If you wish to get to know JavaScript deeply there is a great free book series on the Internet called
Another great resource for learning JavaScript is
The free and highly engaging book
[Part 1a **Previous part**](../part1/01-introduction-to-react.md)[Part 1c **Next part**](../part1/01-component-state-event-handlers.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)
