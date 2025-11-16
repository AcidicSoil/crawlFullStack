---{
  "title": "React with types",
  "source_url": "https://fullstackopen.com/en/part9/react_with_types",
  "crawl_timestamp": "2025-10-04T19:17:25Z",
  "checksum": "1b228165b7e2704b9c5dce1d51acf6605c5b6ddc564e47aa2b7505c96e152a62"
}
---[Skip to content](../part9/01-react-with-types-course-main-content.md)
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
React with types
[a Background and introduction](../part9/01-background-and-introduction.md)[b First steps with TypeScript](../part9/01-first-steps-with-type-script.md)[c Typing an Express app](../part9/01-typing-an-express-app.md)
d React with types

- [Vite with TypeScript](../part9/01-react-with-types-vite-with-type-script.md)
- [React components with TypeScript](../part9/01-react-with-types-react-components-with-type-script.md)
- [Exercise 9.15](../part9/01-react-with-types-exercise-9-15.md)
- [Deeper type usage](../part9/01-react-with-types-deeper-type-usage.md)
- [More type narrowing](../part9/01-react-with-types-more-type-narrowing.md)
- [Exercise 9.16](../part9/01-react-with-types-exercise-9-16.md)
- [React app with state](../part9/01-react-with-types-react-app-with-state.md)
- [Communicating with the server](../part9/01-react-with-types-communicating-with-the-server.md)
- [A note about defining object types](../part9/01-react-with-types-a-note-about-defining-object-types.md)
- [Exercises 9.17-9.20](../part9/01-react-with-types-exercises-9-17-9-20.md)


[e Grande finale: Patientor](../part9/01-grande-finale-patientor.md)
d
# React with types
Before we start delving into how you can use TypeScript with React, we should first have a look at what we want to achieve. When everything works as it should, TypeScript will help us catch the following errors:

- Trying to pass an extra/unwanted prop to a component
- Forgetting to pass a required prop to a component
- Passing a prop with the wrong type to a component


If we make any of these errors, TypeScript can help us catch them in our editor right away. If we didn't use TypeScript, we would have to catch these errors later during testing. We might be forced to do some tedious debugging to find the cause of the errors.
That's enough reasoning for now. Let's start getting our hands dirty!
### Vite with TypeScript
We can use _react-ts_ in the initialization script. So to create a TypeScript app, run the following command:

```
npm create vite@latest my-app-name -- --template react-tscopy
```

After running the command, you should have a complete basic React app that uses TypeScript. You can start the app by running _npm run dev_ in the application's root.
If you take a look at the files and folders, you'll notice that the app is not that different from one using pure JavaScript. The only differences are that the _.jsx_ files are now _.tsx_ files, they contain some type annotations, and the root directory contains a _tsconfig.json_ file.
Now, let's take a look at the _tsconfig.json_ file that has been created for us:

```
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,

    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",

    /* Linting */
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}copy
```

Notice _compilerOptions_ now has the key _document_)". Everything else should be more or less fine.
In our previous project, we used ESlint to help us enforce a coding style, and we'll do the same with this app. We do not need to install any dependencies, since Vite has taken care of that already.
When we look at the _main.tsx_ file that Vite has generated, it looks familiar but there is a small but remarkable difference, there is a exclamation mark after the statement _document.getElementById('root')_ :

```
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)copy
```

The reason for this is that the statement might return value null but the _ReactDOM.createRoot_ does not accept null as parameter. With the
Earlier in this part we [warned](../part9/01-first-steps-with-type-script-type-assertion.md) about the dangers of type assertions, but in our case the assertion is ok since we are sure that the file _index.html_ indeed has this particular id and the function is always returning a HTMLElement.
### React components with TypeScript
Let us consider the following JavaScript React example:

```
import ReactDOM from 'react-dom/client'
import PropTypes from "prop-types";

const Welcome = props => {
  return <h1>Hello, {props.name}</h1>;
};

Welcome.propTypes = {
  name: PropTypes.string
};

ReactDOM.createRoot(document.getElementById('root')).render(
  <Welcome name="Sarah" />
)copy
```

In this example, we have a component called _Welcome_ to which we pass a _name_ as a prop. It then renders the name to the screen. We know that the _name_ should be a string, and we use the [part 5](../part5/01-props-children-and-proptypes-prop-types.md) to receive hints about the desired types of a component's props and warnings about invalid prop types.
With TypeScript, we don't need the _prop-types_ package anymore. We can define the types with the help of TypeScript, just like we define types for a regular function as React components are nothing but mere functions. We will use an interface for the parameter types (i.e. props) and _JSX.Element_ as the return type for any React component:

```
import ReactDOM from 'react-dom/client'

interface WelcomeProps {
  name: string;
}

const Welcome = (props: WelcomeProps): JSX.Element => {
  return <h1>Hello, {props.name}</h1>;
};

ReactDOM.createRoot(document.getElementById('root')!).render(
  <Welcome name="Sarah" />
)copy
```

We defined a new type, _WelcomeProps_ , and passed it to the function's parameter types.

```
const Welcome = (props: WelcomeProps): JSX.Element => {copy
```

You could write the same thing using a more verbose syntax:

```
const Welcome = ({ name }: { name: string }): JSX.Element => (
  <h1>Hello, {name}</h1>
);copy
```

Now our editor knows that the _name_ prop is a string.
There is actually no need to define the return type of a React component since the TypeScript compiler infers the type automatically, so we can just write:

```
interface WelcomeProps {
  name: string;
}

const Welcome = (props: WelcomeProps) => {  return <h1>Hello, {props.name}</h1>;
};

ReactDOM.createRoot(document.getElementById('root')!).render(
  <Welcome name="Sarah" />
)copy
```

### Exercise 9.15
#### 9.15
Create a new Vite app with TypeScript.
This exercise is similar to the one you have already done in [Part 1](../part1/01-java-script-exercises-1-3-1-5.md) of the course, but with TypeScript and some extra tweaks. Start off by modifying the contents of _main.tsx_ to the following:

```
import ReactDOM from 'react-dom/client'
import App from './App';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <App />
)copy
```

and _App.tsx_ :

```
const App = () => {
  const courseName = "Half Stack application development";
  const courseParts = [
    {
      name: "Fundamentals",
      exerciseCount: 10
    },
    {
      name: "Using props to pass data",
      exerciseCount: 7
    },
    {
      name: "Deeper type usage",
      exerciseCount: 14
    }
  ];

  const totalExercises = courseParts.reduce((sum, part) => sum + part.exerciseCount, 0);

  return (
    <div><h1>{courseName}</h1><p>{courseParts[0].name}{courseParts[0].exerciseCount}</p><p>{courseParts[1].name}{courseParts[1].exerciseCount}</p><p>{courseParts[2].name}{courseParts[2].exerciseCount}</p><p>
        Number of exercises {totalExercises}</p></div>
  );
};

export default App;copy
```

and remove the unnecessary files.
The whole app is now in one component. That is not what we want, so refactor the code so that it consists of three components: _Header_ , _Content_ and _Total_. All data is still kept in the _App_ component, which passes all necessary data to each component as props. _Be sure to add type declarations for each component's props!_
The _Header_ component should take care of rendering the name of the course. _Content_ should render the names of the different parts and the number of exercises in each part, and _Total_ should render the total sum of exercises in all parts.
The _App_ component should look somewhat like this:

```
const App = () => {
  // const-declarations

  return (
    <div><Header name={courseName} /><Content ... /><Total ... /></div>
  )
};copy
```

### Deeper type usage
In the previous exercise, we had three parts of a course, and all parts had the same attributes _name_ and _exerciseCount_. But what if we need additional attributes for a specific part? How would this look, codewise? Let's consider the following example:

```
const courseParts = [
  {
    name: "Fundamentals",
    exerciseCount: 10,
    description: "This is an awesome course part"
  },
  {
    name: "Using props to pass data",
    exerciseCount: 7,
    groupProjectCount: 3
  },
  {
    name: "Basics of type Narrowing",
    exerciseCount: 7,
    description: "How to go from unknown to string"
  },
  {
    name: "Deeper type usage",
    exerciseCount: 14,
    description: "Confusing description",
    backgroundMaterial: "https://type-level-typescript.com/template-literal-types"
  },
];copy
```

In the above example, we have added some additional attributes to each course part. Each part has the _name_ and _exerciseCount_ attributes, but the first, the third and fourth also have an attribute called _description_. The second and fourth parts also have some distinct additional attributes.
Let's imagine that our application just keeps on growing, and we need to pass the different course parts around in our code. On top of that, there are also additional attributes and course parts added to the mix. How can we know that our code is capable of handling all the different types of data correctly, and we are not for example forgetting to render a new course part on some page? This is where TypeScript comes in handy!
Let's start by defining types for our different course parts. We notice that the first and third have the same set of attributes. The second and fourth are a bit different so we have three different kinds of course part elements.
So let us define a type for each of the different kind of course parts:

```
interface CoursePartBasic {
  name: string;
  exerciseCount: number;
  description: string;
  kind: "basic"
}

interface CoursePartGroup {
  name: string;
  exerciseCount: number;
  groupProjectCount: number;
  kind: "group"
}

interface CoursePartBackground {
  name: string;
  exerciseCount: number;
  description: string;
  backgroundMaterial: string;
  kind: "background"
}copy
```

Besides the attributes that are found in the various course parts, we have now introduced an additional attribute called _kind_ that has a
Next, we will create a type

```
type CoursePart = CoursePartBasic | CoursePartGroup | CoursePartBackground;copy
```

Now we can set the type for our _courseParts_ variable:

```
const App = () => {
  const courseName = "Half Stack application development";
  const courseParts: CoursePart[] = [
    {
      name: "Fundamentals",
      exerciseCount: 10,
      description: "This is an awesome course part",
      kind: "basic"    },
    {
      name: "Using props to pass data",
      exerciseCount: 7,
      groupProjectCount: 3,
      kind: "group"    },
    {
      name: "Basics of type Narrowing",
      exerciseCount: 7,
      description: "How to go from unknown to string",
      kind: "basic"    },
    {
      name: "Deeper type usage",
      exerciseCount: 14,
      description: "Confusing description",
      backgroundMaterial: "https://type-level-typescript.com/template-literal-types",
      kind: "background"    },
  ]

  // ...
}copy
```

Note that we have now added the attribute _kind_ with a proper value to each element of the array.
Our editor will automatically warn us if we use the wrong type for an attribute, use an extra attribute, or forget to set an expected attribute. If we e.g. try to add the following to the array

```
{
  name: "TypeScript in frontend",
  exerciseCount: 10,
  kind: "basic",
},copy
```

We will immediately see an error in the editor:
![vscode exerciseCount not assignable to type CoursePart - description missing](../assets/393e41e259c5d817.png)
Since our new entry has the attribute _kind_ with value _"basic"_ , TypeScript knows that the entry does not only have the type _CoursePart_ but it is actually meant to be a _CoursePartBasic_. So here the attribute _kind_ "narrows" the type of the entry from a more general to a more specific type that has a certain set of attributes. We shall soon see this style of type narrowing in action in the code!
But we're not satisfied yet! There is still a lot of duplication in our types, and we want to avoid that. We start by identifying the attributes all course parts have in common, and defining a base type that contains them. Then we will

```
interface CoursePartBase {
  name: string;
  exerciseCount: number;
}

interface CoursePartBasic extends CoursePartBase {
  description: string;
  kind: "basic"
}

interface CoursePartGroup extends CoursePartBase {
  groupProjectCount: number;
  kind: "group"
}

interface CoursePartBackground extends CoursePartBase {
  description: string;
  backgroundMaterial: string;
  kind: "background"
}

type CoursePart = CoursePartBasic | CoursePartGroup | CoursePartBackground;copy
```

### More type narrowing
How should we now use these types in our components?
If we try to access the objects in the array _courseParts: CoursePart[]_ we notice that it is possible to only access the attributes that are common to all the types in the union:
![vscode showing part.exerciseCou](../assets/b9bb1ff737858628.png)
And indeed, the TypeScript
> _TypeScript will only allow an operation (or attribute access) if it is valid for every member of the union._
The documentation also mentions the following:
> _The solution is to narrow the union with code... Narrowing occurs when TypeScript can deduce a more specific type for a value based on the structure of the code._
So once again the
One handy way to narrow these kinds of types in TypeScript is to use _switch case_ expressions. Once TypeScript has inferred that a variable is of union type and that each type in the union contains a certain literal attribute (in our case _kind_), we can use that as a type identifier. We can then build a switch case around that attribute and TypeScript will know which attributes are available within each case block:
![vscode showing part. and then the attributes](../assets/fe25c10f30029452.png)
In the above example, TypeScript knows that a _part_ has the type _CoursePart_ and it can then infer that _part_ is of either type _CoursePartBasic_ , _CoursePartGroup_ or _CoursePartBackground_ based on the value of the attribute _kind_.
The specific technique of type narrowing where a union type is narrowed based on literal attribute value is called
Note that the narrowing can naturally be also done with _if_ clause. We could eg. do the following:

```
  courseParts.forEach(part => {
    if (part.kind === 'background') {
      console.log('see the following:', part.backgroundMaterial)
    }

    // can not refer to part.backgroundMaterial here!
  });copy
```

What about adding new types? If we were to add a new course part, wouldn't it be nice to know if we had already implemented handling that type in our code? In the example above, a new type would go to the _default_ block and nothing would get printed for a new type. Sometimes this is wholly acceptable. For instance, if you wanted to handle only specific (but not all) cases of a type union, having a default is fine. Nonetheless, it is recommended to handle all variations separately in most cases.
With TypeScript, we can use a method called _never_.
A straightforward version of the function could look like this:

```
/**
 * Helper function for exhaustive type checking
 */
const assertNever = (value: never): never => {
  throw new Error(
    `Unhandled discriminated union member: ${JSON.stringify(value)}`
  );
};copy
```

If we now were to replace the contents of our _default_ block to:

```
default:
  return assertNever(part);copy
```

and remove the case that handles the type _CoursePartBackground_ , we would see the following error:
![vscode error Argument of Ttype CoursePart not assignable to type never](../assets/e22280ccd7d88fcc.png)
The error message says that

```
'CoursePartBackground' is not assignable to parameter of type 'never'.copy
```

which tells us that we are using a variable somewhere where it should never be used. This tells us that something needs to be fixed.
### Exercise 9.16
#### 9.16
Let us now continue extending the app created in exercise 9.15. First, add the type information and replace the variable _courseParts_ with the one from the example below.

```
interface CoursePartBase {
  name: string;
  exerciseCount: number;
}

interface CoursePartBasic extends CoursePartBase {
  description: string;
  kind: "basic"
}

interface CoursePartGroup extends CoursePartBase {
  groupProjectCount: number;
  kind: "group"
}

interface CoursePartBackground extends CoursePartBase {
  description: string;
  backgroundMaterial: string;
  kind: "background"
}

type CoursePart = CoursePartBasic | CoursePartGroup | CoursePartBackground;

const courseParts: CoursePart[] = [
  {
    name: "Fundamentals",
    exerciseCount: 10,
    description: "This is an awesome course part",
    kind: "basic"
  },
  {
    name: "Using props to pass data",
    exerciseCount: 7,
    groupProjectCount: 3,
    kind: "group"
  },
  {
    name: "Basics of type Narrowing",
    exerciseCount: 7,
    description: "How to go from unknown to string",
    kind: "basic"
  },
  {
    name: "Deeper type usage",
    exerciseCount: 14,
    description: "Confusing description",
    backgroundMaterial: "https://type-level-typescript.com/template-literal-types",
    kind: "background"
  },
  {
    name: "TypeScript in frontend",
    exerciseCount: 10,
    description: "a hard part",
    kind: "basic",
  },
];copy
```

Now we know that both interfaces _CoursePartBasic_ and _CoursePartBackground_ share not only the base attributes but also an attribute called _description_ , which is a string in both interfaces.
Your first task is to declare a new interface that includes the _description_ attribute and extends the _CoursePartBase_ interface. Then modify the code so that you can remove the _description_ attribute from both _CoursePartBasic_ and _CoursePartBackground_ without getting any errors.
Then create a component _Part_ that renders all attributes of each type of course part. Use a switch case-based exhaustive type checking! Use the new component in component _Content_.
Lastly, add another course part interface with the following attributes: _name_ , _exerciseCount_ , _description_ and _requirements_ , the latter being a string array. The objects of this type look like the following:

```
{
  name: "Backend development",
  exerciseCount: 21,
  description: "Typing the backend",
  requirements: ["nodejs", "jest"],
  kind: "special"
}copy
```

Then add that interface to the type union _CoursePart_ and add the corresponding data to the _courseParts_ variable. Now, if you have not modified your _Content_ component correctly, you should get an error, because you have not yet added support for the fourth course part type. Do the necessary changes to _Content_ , so that all attributes for the new course part also get rendered and that the compiler doesn't produce any errors.
The result might look like the following:
![browser showing half stack application development](../assets/a9c13b5db6fcd246.png)
### React app with state
So far, we have only looked at an application that keeps all the data in a typed variable but does not have any state. Let us once more go back to the note app, and build a typed version of it.
We start with the following code:

```
import { useState } from 'react';

const App = () => {
  const [newNote, setNewNote] = useState('');
  const [notes, setNotes] = useState([]);

  return null
}copy
```

When we hover over the _useState_ calls in the editor, we notice a couple of interesting things.
The type of the first call _useState('')_ looks like the following:

```
useState<string>(initialState: string | (() => string)):
  [string, React.Dispatch<React.SetStateAction<string>>]copy
```

The type is somewhat challenging to decipher. It has the following "form":

```
functionName(parameters): return_valuecopy
```

So we notice that TypeScript compiler has inferred that the initial state is either a string or a function that returns a string:

```
initialState: string | (() => string))copy
```

The type of the returned array is the following:

```
[string, React.Dispatch<React.SetStateAction<string>>]copy
```

So the first element, assigned to _newNote_ is a string and the second element that we assigned _setNewNote_ has a slightly more complex type. We notice that there is a string mentioned there, so we know that it must be the type of a function that sets a valued data. See
From all this we see that TypeScript has indeed
When we look at the second useState that has the initial value _[]_ , the type looks quite different

```
useState<never[]>(initialState: never[] | (() => never[])): 
  [never[], React.Dispatch<React.SetStateAction<never[]>>] copy
```

TypeScript can just infer that the state has type _never[]_ , it is an array but it has no clue what the elements stored to the array are, so we clearly need to help the compiler and provide the type explicitly.
One of the best sources for information about typing React is the _type parameter_ in situations where the compiler can not infer the type.
Let us now define a type for notes:

```
interface Note {
  id: string,
  content: string
}copy
```

The solution is now simple:

```
const [notes, setNotes] = useState<Note[]>([]);copy
```

And indeed, the type is set correctly:

```
useState<Note[]>(initialState: Note[] | (() => Note[])):
  [Note[], React.Dispatch<React.SetStateAction<Note[]>>]copy
```

So in technical terms useState is _type parameter_ in those cases when the compiler can not infer the type.
Rendering the notes is now easy. Let us just add some data to the state so that we can see that the code works:

```
interface Note {
  id: string,
  content: string
}

import { useState } from "react";

const App = () => {
  const [notes, setNotes] = useState<Note[]>([
    { id: '1', content: 'testing' }  ]);
  const [newNote, setNewNote] = useState('');

  return (
    <div>      <ul>        {notes.map(note =>          <li key={note.id}>{note.content}</li>        )}      </ul>    </div>  )
}copy
```

The next task is to add a form that makes it possible to create new notes:

```
const App = () => {
  const [notes, setNotes] = useState<Note[]>([
    { id: 1, content: 'testing' }
  ]);
  const [newNote, setNewNote] = useState('');

  return (
    <div>
      <form>        <input          value={newNote}          onChange={(event) => setNewNote(event.target.value)}         />        <button type='submit'>add</button>      </form>      <ul>
        {notes.map(note =>
          <li key={note.id}>{note.content}</li>
        )}
      </ul>
    </div>
  )
}copy
```

It just works, there are no complaints about types! When we hover over the _event.target.value_ , we see that it is indeed a string, just what is expected for the parameter of _setNewNote_ :
![vscode showing variable is a string](../assets/6eda4eea8b293bc7.png)
So we still need the event handler for adding the new note. Let us try the following:

```
const App = () => {
  // ...

  const noteCreation = (event) => {    event.preventDefault()    // ...  };
  return (
    <div>
      <form onSubmit={noteCreation}>        <input
          value={newNote}
          onChange={(event) => setNewNote(event.target.value)} 
        />
        <button type='submit'>add</button>
      </form>
      // ...
    </div>
  )
}copy
```

It does not quite work, there is an Eslint error complaining about implicit any:
![vscode error event implicitly has any type](../assets/8524def2acf12e06.png)
TypeScript compiler now has no clue what the type of the parameter is, this is why the type is the infamous implicit any that we want to [avoid](../part9/01-first-steps-with-type-script-the-horrors-of-any.md) at all costs. The React TypeScript cheatsheet comes to the rescue again, the chapter about _React.SyntheticEvent_.
The code becomes

```
interface Note {
  id: string,
  content: string
}

const App = () => {
  const [notes, setNotes] = useState<Note[]>([]);
  const [newNote, setNewNote] = useState('');

  const noteCreation = (event: React.SyntheticEvent) => {    event.preventDefault()    const noteToAdd = {      content: newNote,      id: String(notes.length + 1)    }    setNotes(notes.concat(noteToAdd));    setNewNote('')  };
  return (
    <div>
      <form onSubmit={noteCreation}>
        <input value={newNote} onChange={(event) => setNewNote(event.target.value)} />
        <button type='submit'>add</button>
      </form>
      <ul>
        {notes.map(note =>
          <li key={note.id}>{note.content}</li>
        )}
      </ul>
    </div>
  )
}copy
```

And that's it, our app is ready and perfectly typed!
### Communicating with the server
Let us modify the app so that the notes are saved in a JSON server backend in url
As usual, we shall use Axios and the useEffect hook to fetch the initial state from the server.
Let us try the following:

```
const App = () => {
  // ...
  useEffect(() => {
    axios.get('http://localhost:3001/notes').then(response => {
      console.log(response.data);
    })
  }, [])
  // ...
}copy
```

When we hover over the _response.data_ we see that it has the type _any_
![vscode response.data showing the any type](../assets/bc8fc1a4d6dafe46.png)
To set the data to the state with function _setNotes_ we must type it properly.
With a little

```
  useEffect(() => {
    axios.get<Note[]>('http://localhost:3001/notes').then(response => {      console.log(response.data);
    })
  }, [])copy
```

When we hover over the response.data we see that it has the correct type:
![vscode showing response.data has Note array type](../assets/88db8b6b615cb095.png)
We can now set the data in the state _notes_ to get the code working:

```
  useEffect(() => {
    axios.get<Note[]>('http://localhost:3001/notes').then(response => {
      setNotes(response.data)    })
  }, [])copy
```

So just like with _useState_ , we gave a type parameter to _axios.get_ to instruct it on how the typing should be done. Just like _useState_ , _axios.get_ is also a _axios.get_ has a default value of _any_ so, if the function is used without defining the type parameter, the type of the response data will be any.
The code works, compiler and Eslint are happy and remain quiet. However, giving a type parameter to _axios.get_ is a potentially dangerous thing to do. The _response body can contain data in an arbitrary form_ , and when giving a type parameter we are essentially just telling the TypeScript compiler to trust us that the data has type _Note[]_.
So our code is essentially as safe as it would be if a [type assertion](../part9/01-first-steps-with-type-script-type-assertion.md) would be used (not good):

```
  useEffect(() => {
    axios.get('http://localhost:3001/notes').then(response => {
      // response.body is of type any
      setNotes(response.data as Note[])    })
  }, [])copy
```

Since the TypeScript types do not even exist in runtime, our code does not give us any safety against situations where the request body contains data in the wrong form.
Giving a type parameter to _axios.get_ might be ok if we are _absolutely sure_ that the backend behaves correctly and always returns the data in the correct form. If we want to build a robust system we should prepare for surprises and parse the response data (similar to what we did [in the previous section](../part9/01-typing-an-express-app-proofing-requests.md) for the requests to the backend).
Let us now wrap up our app by implementing the new note addition:

```
  const noteCreation = (event: React.SyntheticEvent) => {
    event.preventDefault()
    axios.post<Note>('http://localhost:3001/notes', { content: newNote })      .then(response => {        setNotes(notes.concat(response.data))      })
    setNewNote('')
  };copy
```

We are again giving _axios.post_ a type parameter. We know that the server response is the added note, so the proper type parameter is _Note_.
Let us clean up the code a bit. For the type definitions, we create a file _types.ts_ with the following content:

```
export interface Note {
  id: string,
  content: string
}

export type NewNote = Omit<Note, 'id'>copy
```

We have added a new type for a _new note_ , one that does not yet have the _id_ field assigned.
The code that communicates with the backend is also extracted to a module in the file _noteService.ts_

```
import axios from 'axios';
import { Note, NewNote } from "./types";

const baseUrl = 'http://localhost:3001/notes'

export const getAllNotes = () => {
  return axios
    .get<Note[]>(baseUrl)
    .then(response => response.data)
}

export const createNote = (object: NewNote) => {
  return axios
    .post<Note>(baseUrl, object)
    .then(response => response.data)
}copy
```

The component _App_ is now much cleaner:

```
import { useState, useEffect } from "react";
import { Note } from "./types";import { getAllNotes, createNote } from './noteService';
const App = () => {
  const [notes, setNotes] = useState<Note[]>([]);
  const [newNote, setNewNote] = useState('');

  useEffect(() => {
    getAllNotes().then(data => {      setNotes(data)    })  }, [])

  const noteCreation = (event: React.SyntheticEvent) => {
    event.preventDefault()
    createNote({ content: newNote }).then(data => {      setNotes(notes.concat(data))    })
    setNewNote('')
  };

  return (
    // ...
  )
}copy
```

The app is now nicely typed and ready for further development!
The code of the typed notes can be found
### A note about defining object types
We have used

```
interface DiaryEntry {
  id: number;
  date: string;
  weather: Weather;
  visibility: Visibility;
  comment?: string;
} copy
```

and in the course part of this section

```
interface CoursePartBase {
  name: string;
  exerciseCount: number;
}copy
```

We actually could have achieved the same effect by using a

```
type DiaryEntry = {
  id: number;
  date: string;
  weather: Weather;
  visibility: Visibility;
  comment?: string;
} copy
```

In most cases, you can use either _type_ or _interface_ , whichever syntax you prefer. However, there are a few things to keep in mind. For example, if you define multiple interfaces with the same name, they will result in a merged interface, whereas if you try to define multiple types with the same name, it will result in an error stating that a type with the same name is already declared.
TypeScript documentation
### Exercises 9.17-9.20
Let us now build a frontend for the Ilari's flight diaries that was developed in [the previous section](../part9/01-typing-an-express-app.md). The source code of the backend can be found in
#### Exercise 9.17
Create a TypeScript React app with similar configurations as the apps of this section. Fetch the diaries from the backend and render those to screen. Do all the required typing and ensure that there are no Eslint errors.
Remember to keep the network tab open. It might give you a valuable hint...
You can decide how the diary entries are rendered. If you wish, you may take inspiration from the figure below. Note that the backend API does not return the diary comments, you may modify it to return also those on a GET request.
#### Exercise 9.18
Make it possible to add new diary entries from the frontend. In this exercise you may skip all validations and assume that the user just enters the data in a correct form.
#### Exercise 9.19
Notify the user if the the creation of a diary entry fails in the backend, show also the reason for the failure.
See eg.
Your solution may look like this:
![browser showing error incorrect visibility best ever](../assets/9b960f134e4d41e8.png)
#### Exercise 9.20
Addition of a diary entry is now very error prone since user can type anything to the input fields. The situation must be improved.
Modify the input form so that the date is set with a HTML [part 6](../part6/01-many-reducers-store-with-complex-state.md), that material may or may not be useful...
Your app should all the time stay well typed and there should not be any Eslint errors and no Eslint rules should be ignored.
Your solution could look like this:
![browser showing add new entry form for diaries](../assets/804c091524e9f0c7.png)
[Part 9c **Previous part**](../part9/01-typing-an-express-app.md)[Part 9e **Next part**](../part9/01-grande-finale-patientor.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)
