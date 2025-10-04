---{
  "title": "React Native basics",
  "source_url": "https://fullstackopen.com/en/part10/react_native_basics",
  "crawl_timestamp": "2025-10-04T19:15:44Z",
  "checksum": "846e3a90941ddfb52a0278ed0351d75d167d3023ef6525b1c876b62e69d1ff56"
}
---[Skip to content](../part10/01-react-native-basics-course-main-content.md)
[{() => fs}](https://fullstackopen.com/en/)

- [About course](../about/01-about.md)
- [Course contents](../#course-contents/01-course-contents.md)
- [FAQ](../faq/01-faq.md)
- [Partners](../companies/01-companies.md)
- [Challenge](../challenge/01-challenge.md)
[Search from the material](../search/01-search.md)Toggle dark theme
Select languageSuomi English 中文 Español Français Português(BR)

[Fullstack](../#course-contents/01-course-contents.md)
[Part 10](../part10/01-part10.md)
React Native basics
[a Introduction to React Native](../part10/01-introduction-to-react-native.md)
b React Native basics

- [Core components](../part10/01-react-native-basics-core-components.md)
- [Manually reloading the application](../part10/01-react-native-basics-manually-reloading-the-application.md)
- [Exercise 10.3](../part10/01-react-native-basics-exercise-10-3.md)
- [Style](../part10/01-react-native-basics-style.md)
- [Consistent user interface with theming](../part10/01-react-native-basics-consistent-user-interface-with-theming.md)
- [Using flexbox for layout](../part10/01-react-native-basics-using-flexbox-for-layout.md)
- [Exercises 10.4-10.5](../part10/01-react-native-basics-exercises-10-4-10-5.md)
- [Routing](../part10/01-react-native-basics-routing.md)
- [Exercises 10.6-10.7](../part10/01-react-native-basics-exercises-10-6-10-7.md)
- [Form state management](../part10/01-react-native-basics-form-state-management.md)
- [Exercise 10.8](../part10/01-react-native-basics-exercise-10-8.md)
- [Form validation](../part10/01-react-native-basics-form-validation.md)
- [Exercise 10.9](../part10/01-react-native-basics-exercise-10-9.md)
- [Platform-specific code](../part10/01-react-native-basics-platform-specific-code.md)
- [Exercise 10.10](../part10/01-react-native-basics-exercise-10-10.md)


[c Communicating with server](../part10/01-communicating-with-server.md)[d Testing and extending our application](../part10/01-testing-and-extending-our-application.md)
b
# React Native basics
Now that we have set up our development environment we can get into React Native basics and get started with the development of our application. In this section, we will learn how to build user interfaces with React Native's core components, how to add style properties to these core components, how to transition between views, and how to manage the form's state efficiently.
### Core components
In the previous parts, we have learned that we can use React to define components as functions, which receive props as an argument and returns a tree of React elements. This tree is usually represented with JSX syntax. In the browser environment, we have used the

```
const HelloWorld = props => {
  return <div>Hello world!</div>;
};copy
```

The _HelloWorld_ component returns a single _div_ element which is created using the JSX syntax. We might remember that this JSX syntax is compiled into _React.createElement_ method calls, such as this:

```
React.createElement('div', null, 'Hello world!');copy
```

This line of code creates a _div_ element without any props and with a single child element which is a string _"Hello world"_. When we render this component into a root DOM element using the _ReactDOM.render_ method the _div_ element will be rendered as the corresponding DOM element.
As we can see, React is not bound to a certain environment, such as the browser environment. Instead, there are libraries such as ReactDOM that can render _a set of predefined components_ , such as DOM elements, in a specific environment. In React Native these predefined components are called _core components_.

```
import { Text } from 'react-native';
const HelloWorld = props => {
  return <Text>Hello world!</Text>;};copy
```

So we import the _div_ element with a _Text_ element. Many familiar DOM elements have their React Native "counterparts". Here are some examples picked from React Native's

- _the only_ React Native component that can have textual children. It is similar to for example the _< strong>_ and the _< h1>_ elements.
- _< div>_ element.
- _< input>_ element.
- _< button>_ element.


There are a few notable differences between core components and DOM elements. The first difference is that the _Text_ component is _the only_ React Native component that can have textual children. This means that you can't, for example, replace the _Text_ component with the _View_ component in the previous example.
The second notable difference is related to the event handlers. While working with the DOM elements we are used to adding event handlers such as _onClick_ to basically any element such as _< div>_ and _< button>_. In React Native we have to carefully read the

```
import { Text, Pressable, Alert } from 'react-native';

const PressableText = props => {
  return (
    <Pressable
      onPress={() => Alert.alert('You pressed the text!')}
    >
      <Text>You can press me</Text>
    </Pressable>
  );
};copy
```

Now that we have a basic understanding of the core components, let's start to give our project some structure. Create a _src_ directory in the root directory of your project and in the _src_ directory create a _components_ directory. In the _components_ directory create a file _Main.jsx_ with the following content:

```
import Constants from 'expo-constants';
import { Text, StyleSheet, View } from 'react-native';

const styles = StyleSheet.create({
  container: {
    marginTop: Constants.statusBarHeight,
    flexGrow: 1,
    flexShrink: 1,
  },
});

const Main = () => {
  return (
    <View style={styles.container}>
      <Text>Rate Repository Application</Text>
    </View>
  );
};

export default Main;copy
```

Next, let's use the _Main_ component in the _App_ component in the _App.js_ file which is located in our project's root directory. Replace the current content of the file with this:

```
import Main from './src/components/Main';

const App = () => {
  return <Main />;
};

export default App;copy
```

### Manually reloading the application
As we have seen, Expo will automatically reload the application when we make changes to the code. However, there might be times when automatic reload isn't working and the application has to be reloaded manually. This can be achieved through the in-app developer menu.
You can access the developer menu by shaking your device or by selecting "Shake Gesture" inside the Hardware menu in the iOS Simulator. You can also use the _⌘D_ keyboard shortcut when your app is running in the iOS Simulator, or _⌘M_ when running in an Android emulator on Mac OS and _Ctrl+M_ on Windows and Linux.
Once the developer menu is open, simply press "Reload" to reload the application. After the application has been reloaded, automatic reloads should work without the need for a manual reload.
### Exercise 10.3
#### Exercise 10.3: the reviewed repositories list
In this exercise, we will implement the first version of the reviewed repositories list. The list should contain the repository's full name, description, language, number of forks, number of stars, rating average and number of reviews. Luckily React Native provides a handy component for displaying a list of data, which is the
Implement components _RepositoryList_ and _RepositoryItem_ in the _components_ directory's files _RepositoryList.jsx_ and _RepositoryItem.jsx_. The _RepositoryList_ component should render the _FlatList_ component and _RepositoryItem_ a single item on the list (hint: use the _FlatList_ component's _RepositoryList.jsx_ file:

```
import { FlatList, View, StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  separator: {
    height: 10,
  },
});

const repositories = [
  {
    id: 'jaredpalmer.formik',
    fullName: 'jaredpalmer/formik',
    description: 'Build forms in React, without the tears',
    language: 'TypeScript',
    forksCount: 1589,
    stargazersCount: 21553,
    ratingAverage: 88,
    reviewCount: 4,
    ownerAvatarUrl: 'https://avatars2.githubusercontent.com/u/4060187?v=4',
  },
  {
    id: 'rails.rails',
    fullName: 'rails/rails',
    description: 'Ruby on Rails',
    language: 'Ruby',
    forksCount: 18349,
    stargazersCount: 45377,
    ratingAverage: 100,
    reviewCount: 2,
    ownerAvatarUrl: 'https://avatars1.githubusercontent.com/u/4223?v=4',
  },
  {
    id: 'django.django',
    fullName: 'django/django',
    description: 'The Web framework for perfectionists with deadlines.',
    language: 'Python',
    forksCount: 21015,
    stargazersCount: 48496,
    ratingAverage: 73,
    reviewCount: 5,
    ownerAvatarUrl: 'https://avatars2.githubusercontent.com/u/27804?v=4',
  },
  {
    id: 'reduxjs.redux',
    fullName: 'reduxjs/redux',
    description: 'Predictable state container for JavaScript apps',
    language: 'TypeScript',
    forksCount: 13902,
    stargazersCount: 52869,
    ratingAverage: 0,
    reviewCount: 0,
    ownerAvatarUrl: 'https://avatars3.githubusercontent.com/u/13142323?v=4',
  },
];

const ItemSeparator = () => <View style={styles.separator} />;

const RepositoryList = () => {
  return (
    <FlatList
      data={repositories}
      ItemSeparatorComponent={ItemSeparator}
      // other props
    />
  );
};

export default RepositoryList;copy
```

_Do not_ alter the contents of the _repositories_ variable, it should contain everything you need to complete this exercise. Render the _RepositoryList_ component in the _Main_ component which we previously added to the _Main.jsx_ file. The reviewed repository list should roughly look something like this:
![Application preview](../assets/e884581606c6095c.jpg)
### Style
Now that we have a basic understanding of how core components work and we can use them to build a simple user interface it is time to add some styles. In [part 2](../part2/01-adding-styles-to-react-app.md) we learned that in the browser environment we can define React component's style properties using CSS. We had the option to either define these styles inline using the _style_ prop or in a CSS file with a suitable selector.
There are many similarities in the way style properties are attached to React Native's core components and the way they are attached to DOM elements. In React Native most of the core components accept a prop called _style_. The _style_ prop accepts an object with style properties and their values. These style properties are in most cases the same as in CSS, however, property names are in _camelCase_. This means that CSS properties such as _padding-top_ and _font-size_ are written as _paddingTop_ and _fontSize_. Here is a simple example of how to use the _style_ prop:

```
import { Text, View } from 'react-native';

const BigBlueText = () => {
  return (
    <View style={{ padding: 20 }}>
      <Text style={{ color: 'blue', fontSize: 24, fontWeight: '700' }}>
        Big blue text
      </Text>
    </View>
  );
};copy
```

On top of the property names, you might have noticed another difference in the example. In CSS numerical property values commonly have a unit such as _px_ , _%_ , _em_ or _rem_. In React Native all dimension-related property values such as _width_ , _height_ , _padding_ , and _margin_ as well as font sizes are _unitless_. These unitless numeric values represent _density-independent pixels_. In case you are wondering what are the available style properties for certain core components, check the
In general, defining styles directly in the _style_ prop is not considered such a great idea, because it makes components bloated and unclear. Instead, we should define styles outside the component's render function using the _StyleSheet.create_ method accepts a single argument which is an object consisting of named style objects and it creates a StyleSheet style reference from the given object. Here is an example of how to refactor the previous example using the _StyleSheet.create_ method:

```
import { Text, View, StyleSheet } from 'react-native';
const styles = StyleSheet.create({  container: {    padding: 20,  },  text: {    color: 'blue',    fontSize: 24,    fontWeight: '700',  },});
const BigBlueText = () => {
  return (
    <View style={styles.container}>      <Text style={styles.text}>        Big blue text
      </Text>
    </View>
  );
};copy
```

We create two named style objects, _styles.container_ and _styles.text_. Inside the component, we can access specific style objects the same way we would access any key in a plain object.
In addition to an object, the _style_ prop also accepts an array of objects. In the case of an array, the objects are merged from left to right so that latter-style properties take precedence. This works recursively, so we can have for example an array containing an array of styles and so forth. If an array contains values that evaluate to false, such as _null_ or _undefined_ , these values are ignored. This makes it easy to define _conditional styles_ for example, based on the value of a prop. Here is an example of conditional styles:

```
import { Text, View, StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  text: {
    color: 'grey',
    fontSize: 14,
  },
  blueText: {
    color: 'blue',
  },
  bigText: {
    fontSize: 24,
    fontWeight: '700',
  },
});

const FancyText = ({ isBlue, isBig, children }) => {
  const textStyles = [
    styles.text,
    isBlue && styles.blueText,
    isBig && styles.bigText,
  ];

  return <Text style={textStyles}>{children}</Text>;
};

const Main = () => {
  return (
    <>
      <FancyText>Simple text</FancyText>
      <FancyText isBlue>Blue text</FancyText>
      <FancyText isBig>Big text</FancyText>
      <FancyText isBig isBlue>
        Big blue text
      </FancyText>
    </>
  );
};copy
```

In the example, we use the _& &_ operator with the expression _condition && exprIfTrue_. This expression yields _exprIfTrue_ if the _condition_ evaluates to true, otherwise it will yield _condition_ , which in that case is a value that evaluates to false. This is an extremely widely used and handy shorthand. Another option would be to use the

```
condition ? exprIfTrue : exprIfFalsecopy
```

### Consistent user interface with theming
Let's stick with the concept of styling but with a bit wider perspective. Most of us have used a multitude of different applications and might agree that one trait that makes a good user interface is _consistency_. This means that the appearance of user interface components such as their font size, font family and color follows a consistent pattern. To achieve this we have to somehow _parametrize_ the values of different style properties. This method is commonly known as _theming_.
Users of popular user interface libraries such as _colors.primary_ instead of _#0366d6_ when defining styles. This leads to increased consistency and flexibility.
Let's see how theming could work in practice in our application. We will be using a lot of text with different variations, such as different font sizes and colors. Because React Native does not support global styles, we should create our own _Text_ component to keep the textual content consistent. Let's get started by adding the following theme configuration object in a _theme.js_ file in the _src_ directory:

```
const theme = {
  colors: {
    textPrimary: '#24292e',
    textSecondary: '#586069',
    primary: '#0366d6',
  },
  fontSizes: {
    body: 14,
    subheading: 16,
  },
  fonts: {
    main: 'System',
  },
  fontWeights: {
    normal: '400',
    bold: '700',
  },
};

export default theme;copy
```

Next, we should create the actual _Text_ component which uses this theme configuration. Create a _Text.jsx_ file in the _components_ directory where we already have our other components. Add the following content to the _Text.jsx_ file:

```
import { Text as NativeText, StyleSheet } from 'react-native';

import theme from '../theme';

const styles = StyleSheet.create({
  text: {
    color: theme.colors.textPrimary,
    fontSize: theme.fontSizes.body,
    fontFamily: theme.fonts.main,
    fontWeight: theme.fontWeights.normal,
  },
  colorTextSecondary: {
    color: theme.colors.textSecondary,
  },
  colorPrimary: {
    color: theme.colors.primary,
  },
  fontSizeSubheading: {
    fontSize: theme.fontSizes.subheading,
  },
  fontWeightBold: {
    fontWeight: theme.fontWeights.bold,
  },
});

const Text = ({ color, fontSize, fontWeight, style, ...props }) => {
  const textStyle = [
    styles.text,
    color === 'textSecondary' && styles.colorTextSecondary,
    color === 'primary' && styles.colorPrimary,
    fontSize === 'subheading' && styles.fontSizeSubheading,
    fontWeight === 'bold' && styles.fontWeightBold,
    style,
  ];

  return <NativeText style={textStyle} {...props} />;
};

export default Text;copy
```

Now we have implemented our text component. This text component has consistent color, font size and font weight variants that we can use anywhere in our application. We can get different text variations using different props like this:

```
import Text from './Text';

const Main = () => {
  return (
    <>
      <Text>Simple text</Text>
      <Text style={{ paddingBottom: 10 }}>Text with custom style</Text>
      <Text fontWeight="bold" fontSize="subheading">
        Bold subheading
      </Text>
      <Text color="textSecondary">Text with secondary color</Text>
    </>
  );
};

export default Main;copy
```

Feel free to extend or modify this component if you feel like it. It might also be a good idea to create reusable text components such as _Subheading_ which use the _Text_ component. Also, keep on extending and modifying the theme configuration as your application progresses.
### Using flexbox for layout
The last concept we will cover related to styling is implementing layouts with
Flexbox is a layout entity consisting of two separate components: a _flex container_ and inside it a set of _flex items_. A Flex container has a set of properties that control the flow of its items. To make a component a flex container it must have the style property _display_ set as _flex_ which is the default value for the _display_ property. Here is an example of a flex container:

```
import { View, StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  flexContainer: {
    flexDirection: 'row',
  },
});

const FlexboxExample = () => {
  return <View style={styles.flexContainer}>{/* ... */}</View>;
};copy
```

Perhaps the most important properties of a flex container are the following:

- _row_ , _row-reverse_ , _column_ (default value) and _column-reverse_. Flex direction _row_ will lay out the flex items from left to right, whereas _column_ from top to bottom. _*-reverse_ directions will just reverse the order of the flex items.
- _flexDirection_ property). Possible values for this property are _flex-start_ (default value), _flex-end_ , _center_ , _space-between_ , _space-around_ and _space-evenly_.
- _justifyContent_ but for the opposite axis. Possible values for this property are _flex-start_ , _flex-end_ , _center_ , _baseline_ and _stretch_ (default value).


Let's move on to flex items. As mentioned, a flex container can contain one or many flex items. Flex items have properties that control how they behave in respect of other flex items in the same flex container. To make a component a flex item all you have to do is to set it as an immediate child of a flex container:

```
import { View, Text, StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  flexContainer: {
    display: 'flex',
  },
  flexItemA: {
    flexGrow: 0,
    backgroundColor: 'green',
  },
  flexItemB: {
    flexGrow: 1,
    backgroundColor: 'blue',
  },
});

const FlexboxExample = () => {
  return (
    <View style={styles.flexContainer}>
      <View style={styles.flexItemA}>
        <Text>Flex item A</Text>
      </View>
      <View style={styles.flexItemB}>
        <Text>Flex item B</Text>
      </View>
    </View>
  );
};copy
```

One of the most commonly used properties of flex items is the _flexGrow_ of _1_ , they will share all the available space evenly. If a flex item has a _flexGrow_ of _0_ , it will only use the space its content requires and leave the rest of the space for other flex items.
Here you can find how to simplify layouts with Flexbox gap:
Next, read the article _camelCase_ naming. However, the _property values_ such as _flex-start_ and _space-between_ are exactly the same.
**NB:** React Native and CSS has some differences regarding the flexbox. The most important difference is that in React Native the default value for the _flexDirection_ property is _column_. It is also worth noting that the _flex_ shorthand doesn't accept multiple values in React Native. More on React Native's flexbox implementation can be read in the
### Exercises 10.4-10.5
#### Exercise 10.4: the app bar
We will soon need to navigate between different views in our application. That is why we need an _AppBar.jsx_ in the _components_ folder with the following content:

```
import { View, StyleSheet } from 'react-native';
import Constants from 'expo-constants';

const styles = StyleSheet.create({
  container: {
    paddingTop: Constants.statusBarHeight,
    // ...
  },
  // ...
});

const AppBar = () => {
  return <View style={styles.container}>{/* ... */}</View>;
};

export default AppBar;copy
```

Now that the _AppBar_ component will prevent the status bar from overlapping the content, you can remove the _marginTop_ style we added for the _Main_ component earlier in the _Main.jsx_ file. The _AppBar_ component should currently contain a tab with the text _"Repositories"_. Make the tab pressable by using the _onPress_ event in any way. Add the _AppBar_ component to the _Main_ component so that it is the uppermost component on the screen. The _AppBar_ component should look something like this:
![Application preview](../assets/0a2b0ea53094f703.jpg)
The background color of the app bar in the image is _#24292e_ but you can use any other color as well. It might be a good idea to add the app bar's background color into the theme configuration so that it is easy to change it if needed. Another good idea might be to separate the app bar's tab into a component like _AppBarTab_ so that it is easy to add new tabs in the future.
#### Exercise 10.5: polished reviewed repositories list
The current version of the reviewed repositories list looks quite grim. Modify the _RepositoryItem_ component so that it also displays the repository author's avatar image. You can implement this by using the
![Application preview](../assets/b4173ea6e18da690.jpg)
In the image, the _Main_ component's background color is set to _#e1e4e8_ whereas _RepositoryItem_ component's background color is set to _white_. The language tag's background color is _#0366d6_ which is the value of the _colors.primary_ variable in the theme configuration. Remember to exploit the _Text_ component we implemented earlier. Also when needed, split the _RepositoryItem_ component into smaller components.
### Routing
When we start to expand our application we will need a way to transition between different views such as the repositories view and the sign-in view. In [part 7](../part7/01-react-router.md) we got familiar with
Routing in a React Native application is a bit different from routing in a web application. The main difference is that we can't reference pages with URLs, which we type into the browser's address bar, and can't navigate back and forth through the user's history using the browser's
With React Native we can use the entire React router's core, including the hooks and components. The only difference to the browser environment is that we must replace the _BrowserRouter_ with React Native compatible _react-router-native_ library:

```
npm install react-router-nativecopy
```

Next, open the _App.js_ file and add the _NativeRouter_ component to the _App_ component:

```
import { StatusBar } from 'expo-status-bar';
import { NativeRouter } from 'react-router-native';
import Main from './src/components/Main';

const App = () => {
  return (
    <>      <NativeRouter>        <Main />      </NativeRouter>      <StatusBar style="auto" />    </>  );
};

export default App;copy
```

Once the router is in place, let's add our first route to the Main component in the _Main.jsx_ file:

```
import { StyleSheet, View } from 'react-native';
import { Route, Routes, Navigate } from 'react-router-native';
import RepositoryList from './RepositoryList';
import AppBar from './AppBar';
import theme from '../theme';

const styles = StyleSheet.create({
  container: {
    backgroundColor: theme.colors.mainBackground,
    flexGrow: 1,
    flexShrink: 1,
  },
});

const Main = () => {
  return (
    <View style={styles.container}>
      <AppBar />
      <Routes>        <Route path="/" element={<RepositoryList />} />        <Route path="*" element={<Navigate to="/" replace />} />      </Routes>    </View>
  );
};

export default Main;copy
```

That's it! The last _Route_ inside the _Routes_ is for catching paths that don't match any previously defined path. In this case, we want to navigate to the home view.
### Exercises 10.6-10.7
#### Exercise 10.6: the sign-in view
We will soon implement a form, that a user can use to _sign in_ to our application. Before that, we must implement a view that can be accessed from the app bar. Create a file _SignIn.jsx_ in the _components_ directory with the following content:

```
import Text from './Text';

const SignIn = () => {
  return <Text>The sign-in view</Text>;
};

export default SignIn;copy
```

Set up a route for this _SignIn_ component in the _Main_ component. Also, add a tab with the text "Sign in" to the app bar next to the "Repositories" tab. Users should be able to navigate between the two views by pressing the tabs (hint: you can use the React router's
#### Exercise 10.7: scrollable app bar
As we are adding more tabs to our app bar, it is a good idea to allow horizontal scrolling once the tabs won't fit the screen. The
Wrap the tabs in the _AppBar_ component's tabs with a _ScrollView_ component:

```
const AppBar = () => {
  return (
    <View style={styles.container}>
      <ScrollView horizontal>{/* ... */}</ScrollView>    </View>
  );
};copy
```

Setting the _true_ will cause the _ScrollView_ component to scroll horizontally once the content won't fit the screen. Note that, you will need to add suitable style properties to the _ScrollView_ component so that the tabs will be laid in a _row_ inside the flex container. You can make sure that the app bar can be scrolled horizontally by adding tabs until the last tab won't fit the screen. Just remember to remove the extra tabs once the app bar is working as intended.
### Form state management
Now that we have a placeholder for the sign-in view the next step would be to implement the sign-in form. Before we get to that let's talk about forms from a wider perspective.
Implementation of forms relies heavily on state management. Using React's _useState_ hook for state management might get the job done for smaller forms. However, it will quickly make state management for more complex forms quite tedious. Luckily there are many good libraries in the React ecosystem that ease the state management of forms. One of these libraries is
The main concepts of Formik are the _context_ and the _field_. However, the easiest way to do a simple form submit is by using useFormik(). It is a custom React hook that will return all Formik state and helpers directly.
There are some restrictions concerning the use of UseFormik(). Read this to become familiar with
Let's see how this works by creating a form for calculating the

```
import { Text, TextInput, Pressable, View } from 'react-native';
import { useFormik } from 'formik';

const initialValues = {
  mass: '',
  height: '',
};

const getBodyMassIndex = (mass, height) => {
  return Math.round(mass / Math.pow(height, 2));
};

const BodyMassIndexForm = ({ onSubmit }) => {
  const formik = useFormik({
    initialValues,
    onSubmit,
  });

  return (
    <View>
      <TextInput
        placeholder="Weight (kg)"
        value={formik.values.mass}
        onChangeText={formik.handleChange('mass')}
      />
      <TextInput
        placeholder="Height (m)"
        value={formik.values.height}
        onChangeText={formik.handleChange('height')}
      />
      <Pressable onPress={formik.handleSubmit}>
        <Text>Calculate</Text>
      </Pressable>
    </View>
  );
};

const BodyMassIndexCalculator = () => {
  const onSubmit = values => {
    const mass = parseFloat(values.mass);
    const height = parseFloat(values.height);

    if (!isNaN(mass) && !isNaN(height) && height !== 0) {
      console.log(`Your body mass index is: ${getBodyMassIndex(mass, height)}`);
    }
  };

  return <BodyMassIndexForm onSubmit={onSubmit} />;
};

export default BodyMassIndexCalculator;copy
```

This example is not part of our application, so you don't need to add this code to the application. You can however try it out for example in _Snack Player_ on a website. You might have bumped into Snack Players for example in this material and React Native documentation.
### Exercise 10.8
#### Exercise 10.8: the sign-in form
Implement a sign-in form to the _SignIn_ component we added earlier in the _SignIn.jsx_ file. The sign-in form should include two text fields, one for the username and one for the password. There should also be a button for submitting the form. You don't need to implement an _onSubmit_ callback function, it is enough that the form values are logged using _console.log_ when the form is submitted:

```
const onSubmit = (values) => {
  console.log(values);
};copy
```

The first step is to install Formik:

```
npm install formikcopy
```

You can use the _TextInput_ component to obscure the password input.
The sign-in form should look something like this:
![Application preview](../assets/2fa1387c53b69712.jpg)
### Form validation
Formik offers two approaches to form validation: a validation function or a validation schema. A validation function is a function provided for the _Formik_ component as the value of the
The second approach is the validation schema which is provided for the _Formik_ component as the value of the

```
npm install yupcopy
```

Next, as an example, let's create a validation schema for the body mass index form we implemented earlier. We want to validate that both _mass_ and _height_ fields are present and they are numeric. Also, the value of _mass_ should be greater or equal to 1 and the value of _height_ should be greater or equal to 0.5. Here is how we define the schema:

```
import * as yup from 'yup';
// ...

const validationSchema = yup.object().shape({  mass: yup    .number()    .min(1, 'Weight must be greater or equal to 1')    .required('Weight is required'),  height: yup    .number()    .min(0.5, 'Height must be greater or equal to 0.5')    .required('Height is required'),});
const BodyMassIndexForm = ({ onSubmit }) => {
  const formik = useFormik({
    initialValues,
    validationSchema,    onSubmit,
  });

  return (
    <View>
      <TextInput
        placeholder="Weight (kg)"
        value={formik.values.mass}
        onChangeText={formik.handleChange('mass')}
      />
      {formik.touched.mass && formik.errors.mass && (
        <Text style={{ color: 'red' }}>{formik.errors.mass}</Text>
      )}
      <TextInput
        placeholder="Height (m)"
        value={formik.values.height}
        onChangeText={formik.handleChange('height')}
      />
      {formik.touched.height && formik.errors.height && (
        <Text style={{ color: 'red' }}>{formik.errors.height}</Text>
      )}
      <Pressable onPress={formik.handleSubmit}>
        <Text>Calculate</Text>
      </Pressable>
    </View>
  );
};

const BodyMassIndexCalculator = () => {
  // ...copy
```

Be aware that you need to include these Text components within the View returned by the form to display the validation errors:

```
 {formik.touched.mass && formik.errors.mass && (
  <Text style={{ color: 'red' }}>{formik.errors.mass}</Text>
 )}copy
```

```
 {formik.touched.height && formik.errors.height && (
  <Text style={{ color: 'red' }}>{formik.errors.height}</Text>
 )}copy
```

The validation is performed by default every time a field's value changes and when the _handleSubmit_ function is called. If the validation fails, the function provided for the _onSubmit_ prop of the _Formik_ component is not called.
### Exercise 10.9
#### Exercise 10.9: validating the sign-in form
Validate the sign-in form so that both username and password fields are required. Note that the _onSubmit_ callback implemented in the previous exercise, _should not be called_ if the form validation fails.
The current implementation of the _TextInput_ component should display an error message if a touched field has an error. Emphasize this error message by giving it a red color.
On top of the red error message, give an invalid field a visual indication of an error by giving it a red border color. Remember that if a field has an error, the _TextInput_ component sets the _TextInput_ component's _error_ prop as _true_. You can use the value of the _error_ prop to attach conditional styles to the _TextInput_ component.
Here's what the sign-in form should roughly look like with an invalid field:
![Application preview](../assets/b01ab872bb8ad6d6.jpg)
The red color used in this implementation is _#d73a4a_.
### Platform-specific code
A big benefit of React Native is that we don't need to worry about whether the application is run on an Android or iOS device. However, there might be cases where we need to execute _platform-specific code_. Such cases could be for example using a different implementation of a component on a different platform.
We can access the user's platform through the _Platform.OS_ constant:

```
import { React } from 'react';
import { Platform, Text, StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  text: {
    color: Platform.OS === 'android' ? 'green' : 'blue',
  },
});

const WhatIsMyPlatform = () => {
  return <Text style={styles.text}>Your platform is: {Platform.OS}</Text>;
};copy
```

Possible values for the _Platform.OS_ constants are _android_ and _ios_. Another useful way to define platform-specific code branches is to use the _Platform.select_ method. Given an object where keys are one of _ios_ , _android_ , _native_ and _default_ , the _Platform.select_ method returns the most fitting value for the platform the user is currently running on. We can rewrite the _styles_ variable in the previous example using the _Platform.select_ method like this:

```
const styles = StyleSheet.create({
  text: {
    color: Platform.select({
      android: 'green',
      ios: 'blue',
      default: 'black',
    }),
  },
});copy
```

We can even use the _Platform.select_ method to require a platform-specific component:

```
const MyComponent = Platform.select({
  ios: () => require('./MyIOSComponent'),
  android: () => require('./MyAndroidComponent'),
})();

<MyComponent />;copy
```

However, a more sophisticated method for implementing and importing platform-specific components (or any other piece of code) is to use the _.ios.jsx_ and _.android.jsx_ file extensions. Note that the _.jsx_ extension could also be another extension recognized by the bundler, such as _.js_. We can for example have files _Button.ios.jsx_ and _Button.android.jsx_ which we can import like this:

```
import Button from './Button';

const PlatformSpecificButton = () => {
  return <Button />;
};copy
```

Now, the Android bundle of the application will have the component defined in the _Button.android.jsx_ whereas the iOS bundle the one defined in the _Button.ios.jsx_ file.
### Exercise 10.10
#### Exercise 10.10: a platform-specific font
Currently, the font family of our application is set to _System_ in the theme configuration located in the _theme.js_ file. Instead of the _System_ font, use a platform-specific _Roboto_ font and on the iOS platform, use the _Arial_ font. The default font can be _System_.
This was the last exercise in this section. It's time to push your code to GitHub and mark all of your finished exercises to the
[Part 10a **Previous part**](../part10/01-introduction-to-react-native.md)[Part 10c **Next part**](../part10/01-communicating-with-server.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)
