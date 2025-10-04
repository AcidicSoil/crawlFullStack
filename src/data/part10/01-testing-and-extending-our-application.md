---{
  "title": "Testing and extending our application",
  "source_url": "https://fullstackopen.com/en/part10/testing_and_extending_our_application",
  "crawl_timestamp": "2025-10-04T19:15:46Z",
  "checksum": "a85ddeda479d0a78e44c02804bc15205f0a38ef44d2e98b25c29b04732a9e7de"
}
---[Skip to content](../part10/01-testing-and-extending-our-application-course-main-content.md)
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
Testing and extending our application
[a Introduction to React Native](../part10/01-introduction-to-react-native.md)[b React Native basics](../part10/01-react-native-basics.md)[c Communicating with server](../part10/01-communicating-with-server.md)
d Testing and extending our application

- [Testing React Native applications](../part10/01-testing-and-extending-our-application-testing-react-native-applications.md)
- [Organizing tests](../part10/01-testing-and-extending-our-application-organizing-tests.md)
- [Testing components](../part10/01-testing-and-extending-our-application-testing-components.md)
- [Handling dependencies in tests](../part10/01-testing-and-extending-our-application-handling-dependencies-in-tests.md)
- [Exercises 10.17. - 10.18](../part10/01-testing-and-extending-our-application-exercises-10-17-10-18.md)
- [Extending our application](../part10/01-testing-and-extending-our-application-extending-our-application.md)
- [Exercises 10.19. - 10.26](../part10/01-testing-and-extending-our-application-exercises-10-19-10-26.md)
- [Cursor-based pagination](../part10/01-testing-and-extending-our-application-cursor-based-pagination.md)
- [Infinite scrolling](../part10/01-testing-and-extending-our-application-infinite-scrolling.md)
- [Exercise 10.27](../part10/01-testing-and-extending-our-application-exercise-10-27.md)
- [Additional resources](../part10/01-testing-and-extending-our-application-additional-resources.md)
- [Closing words](../part10/01-testing-and-extending-our-application-closing-words.md)


d
# Testing and extending our application
Now that we have established a good foundation for our project, it is time to start expanding it. In this section you can put to use all the React Native knowledge you have gained so far. Along with expanding our application we will cover some new areas, such as testing, and additional resources.
### Testing React Native applications
To start testing code of any kind, the first thing we need is a testing framework, which we can use to run a set of test cases and inspect their results. For testing a JavaScript application,

```
npm install --save-dev jest jest-expo eslint-plugin-jestcopy
```

To use the jest-expo preset in Jest, we need to add the following Jest configuration to the _package.json_ file along with the _test_ script:

```
{
  // ...
  "scripts": {
    // other scripts...
    "test": "jest"  },
  "jest": {    "preset": "jest-expo",    "transform": {      "^.+\\.jsx?$": "babel-jest"    },    "transformIgnorePatterns": [      "node_modules/(?!((jest-)?react-native|@react-native(-community)?)|expo(nent)?|@expo(nent)?/.*|@expo-google-fonts/.*|react-navigation|@react-navigation/.*|@unimodules/.*|unimodules|sentry-expo|native-base|react-native-svg|react-router-native)"    ]  },  // ...
}copy
```

The _transform_ option tells Jest to transform _.js_ and _.jsx_ files with the _transformIgnorePatterns_ option is for ignoring certain directories in the _node_modules_ directory while transforming files. This Jest configuration is almost identical to the one proposed in the Expo's
To use the eslint-plugin-jest plugin in ESLint, we need to include it in the plugins and extensions array in the _.eslintrc.json_ file:

```
{
  "plugins": ["react", "react-native"],
  "settings": {
    "react": {
      "version": "detect"
    }
  },
  "extends": ["eslint:recommended", "plugin:react/recommended", "plugin:jest/recommended"],  "parser": "@babel/eslint-parser",
  "env": {
    "react-native/react-native": true
  },
  "rules": {
    "react/prop-types": "off",
    "react/react-in-jsx-scope": "off"
  }
}copy
```

To see that the setup is working, create a directory ___tests___ in the _src_ directory and in the created directory create a file _example.test.js_. In that file, add this simple test:

```
describe('Example', () => {
  it('works', () => {
    expect(1).toBe(1);
  });
});copy
```

Now, let's run our example test by running _npm test_. The command's output should indicate that the test located in the _src/__tests__/example.test.js_ file is passed.
### Organizing tests
Organizing test files in a single ___tests___ directory is one approach in organizing the tests. When choosing this approach, it is recommended to put the test files in their corresponding subdirectories just like the code itself. This means that for example tests related to components are in the _components_ directory, tests related to utilities are in the _utils_ directory, and so on. This will result in the following structure:

```
src/
  __tests__/
    components/
      AppBar.js
      RepositoryList.js
      ...
    utils/
      authStorage.js
      ...
    ...copy
```

Another approach is to organize the tests near the implementation. This means that for example, the test file containing tests for the _AppBar_ component is in the same directory as the component's code. This will result in the following structure:

```
src/
  components/
    AppBar/
      AppBar.test.jsx
      index.jsx
    ...
  ...copy
```

In this example, the component's code is in the _index.jsx_ file and the test in the _AppBar.test.jsx_ file. Note that in order for Jest to find your test files you either have to put them into a ___tests___ directory, use the _.test_ or _.spec_ suffix, or
### Testing components
Now that we have managed to set up Jest and run a very simple test, it is time to find out how to test components. As we know, testing components requires a way to serialize a component's render output and simulate firing different kind of events, such as pressing a button. For these purposes, there is the
In [part 5](../part5/01-testing-react-apps.md) we got familiar with one of these libraries, the _toHaveTextContent_ and _toHaveProp_. These matchers are provided by the

```
npm install --save-dev --legacy-peer-deps react-test-renderer@18.2.0 @testing-library/react-native @testing-library/jest-nativecopy
```

__NB:__ If you face peer dependency issues, make sure that the react-test-renderer version matches the project's React version in the _npm install_ command above. You can check the React version by running _npm list react --depth=0_.
If the installation fails due to peer dependency issues, try again using the _--legacy-peer-deps_ flag with the _npm install_ command.
To be able to use these matchers we need to extend the Jest's _expect_ object. This can be done by using a global setup file. Create a file _setupTests.js_ in the root directory of your project, that is, the same directory where the _package.json_ file is located. In that file add the following line:

```
import '@testing-library/jest-native/extend-expect';copy
```

Next, configure this file as a setup file in the Jest's configuration in the _package.json_ file (note that the _< rootDir>_ in the path is intentional and there is no need to replace it):

```
{
  // ...
  "jest": {
    "preset": "jest-expo",
    "transform": {
      "^.+\\.jsx?$": "babel-jest"
    },
    "transformIgnorePatterns": [
      "node_modules/(?!(jest-)?react-native|react-clone-referenced-element|@react-native-community|expo(nent)?|@expo(nent)?/.*|react-navigation|@react-navigation/.*|@unimodules/.*|unimodules|sentry-expo|native-base|@sentry/.*|react-router-native)"
    ],
    "setupFilesAfterEnv": ["<rootDir>/setupTests.js"]  }
  // ...
}copy
```

The main concepts of the React Native Testing Library are the _Text_ element has the correct textual content:

```
import { Text, View } from 'react-native';
import { render, screen } from '@testing-library/react-native';

const Greeting = ({ name }) => {
  return (
    <View>
      <Text>Hello {name}!</Text>
    </View>
  );
};

describe('Greeting', () => {
  it('renders a greeting message based on the name prop', () => {
    render(<Greeting name="Kalle" />);

    screen.debug();

    expect(screen.getByText('Hello Kalle!')).toBeDefined();
  });
});copy
```

Tests use the object
We acquire the _Text_ node containing certain text by using the _getByText_ function. The Jest matcher
React Native Testing Library's documentation has some good hints on
The object _render_ function looks like.
For all available queries, check the React Native Testing Library's
The second very important React Native Testing Library concept is firing events. We can fire an event in a provided node by using the

```
import { useState } from 'react';
import { Text, TextInput, Pressable, View } from 'react-native';
import { render, fireEvent, screen } from '@testing-library/react-native';

const Form = ({ onSubmit }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = () => {
    onSubmit({ username, password });
  };

  return (
    <View>
      <View>
        <TextInput
          value={username}
          onChangeText={(text) => setUsername(text)}
          placeholder="Username"
        />
      </View>
      <View>
        <TextInput
          value={password}
          onChangeText={(text) => setPassword(text)}
          placeholder="Password"
        />
      </View>
      <View>
        <Pressable onPress={handleSubmit}>
          <Text>Submit</Text>
        </Pressable>
      </View>
    </View>
  );
};

describe('Form', () => {
  it('calls function provided by onSubmit prop after pressing the submit button', () => {
    const onSubmit = jest.fn();
    render(<Form onSubmit={onSubmit} />);

    fireEvent.changeText(screen.getByPlaceholderText('Username'), 'kalle');
    fireEvent.changeText(screen.getByPlaceholderText('Password'), 'password');
    fireEvent.press(screen.getByText('Submit'));

    expect(onSubmit).toHaveBeenCalledTimes(1);

    // onSubmit.mock.calls[0][0] contains the first argument of the first call
    expect(onSubmit.mock.calls[0][0]).toEqual({
      username: 'kalle',
      password: 'password',
    });
  });
});copy
```

In this test, we want to test that after filling the form's fields using the _fireEvent.changeText_ method and pressing the submit button using the _fireEvent.press_ method, the _onSubmit_ callback function is called correctly. To inspect whether the _onSubmit_ function is called and with which arguments, we can use a
Before heading further into the world of testing React Native applications, play around with these examples by adding a test file in the ___tests___ directory we created earlier.
### Handling dependencies in tests
Components in the previous examples are quite easy to test because they are more or less _pure_. Pure components don't depend on _side effects_ such as network requests or using some native API such as the AsyncStorage. The _Form_ component is much less pure than the _Greeting_ component because its state changes can be counted as a side effect. Nevertheless, testing it isn't too difficult.
Next, let's have a look at a strategy for testing components with side effects. Let's pick the _RepositoryList_ component from our application as an example. At the moment the component has one side effect, which is a GraphQL query for fetching the reviewed repositories. The current implementation of the _RepositoryList_ component looks something like this:

```
const RepositoryList = () => {
  const { repositories } = useRepositories();

  const repositoryNodes = repositories
    ? repositories.edges.map((edge) => edge.node)
    : [];

  return (
    <FlatList
      data={repositoryNodes}
      // ...
    />
  );
};

export default RepositoryList;copy
```

The only side effect is the use of the _useRepositories_ hook, which sends a GraphQL query. There are a few ways to test this component. One way is to mock the Apollo Client's responses as instructed in the Apollo Client's _useRepositories_ hook works as intended (preferably through testing it) and extract the components "pure" code into another component, such as the _RepositoryListContainer_ component:

```
export const RepositoryListContainer = ({ repositories }) => {
  const repositoryNodes = repositories
    ? repositories.edges.map((edge) => edge.node)
    : [];

  return (
    <FlatList
      data={repositoryNodes}
      // ...
    />
  );
};

const RepositoryList = () => {
  const { repositories } = useRepositories();

  return <RepositoryListContainer repositories={repositories} />;
};

export default RepositoryList;copy
```

Now, the _RepositoryList_ component contains only the side effects and its implementation is quite simple. We can test the _RepositoryListContainer_ component by providing it with paginated repository data through the _repositories_ prop and checking that the rendered content has the correct information.
### Exercises 10.17. - 10.18
#### Exercise 10.17: testing the reviewed repositories list
Implement a test that ensures that the _RepositoryListContainer_ component renders repository's name, description, language, forks count, stargazers count, rating average, and review count correctly. One approach in implementing this test is to add a

```
const RepositoryItem = (/* ... */) => {
  // ...

  return (
    <View testID="repositoryItem" {/* ... */}>
      {/* ... */}
    </View>
  )
};copy
```

Once the _testID_ prop is added, you can use the

```
const repositoryItems = screen.getAllByTestId('repositoryItem');
const [firstRepositoryItem, secondRepositoryItem] = repositoryItems;

// expect something from the first and the second repository itemcopy
```

Having those elements you can use the
Use this as a base for your test:

```
describe('RepositoryList', () => {
  describe('RepositoryListContainer', () => {
    it('renders repository information correctly', () => {
      const repositories = {
        totalCount: 8,
        pageInfo: {
          hasNextPage: true,
          endCursor:
            'WyJhc3luYy1saWJyYXJ5LnJlYWN0LWFzeW5jIiwxNTg4NjU2NzUwMDc2XQ==',
          startCursor: 'WyJqYXJlZHBhbG1lci5mb3JtaWsiLDE1ODg2NjAzNTAwNzZd',
        },
        edges: [
          {
            node: {
              id: 'jaredpalmer.formik',
              fullName: 'jaredpalmer/formik',
              description: 'Build forms in React, without the tears',
              language: 'TypeScript',
              forksCount: 1619,
              stargazersCount: 21856,
              ratingAverage: 88,
              reviewCount: 3,
              ownerAvatarUrl:
                'https://avatars2.githubusercontent.com/u/4060187?v=4',
            },
            cursor: 'WyJqYXJlZHBhbG1lci5mb3JtaWsiLDE1ODg2NjAzNTAwNzZd',
          },
          {
            node: {
              id: 'async-library.react-async',
              fullName: 'async-library/react-async',
              description: 'Flexible promise-based React data loader',
              language: 'JavaScript',
              forksCount: 69,
              stargazersCount: 1760,
              ratingAverage: 72,
              reviewCount: 3,
              ownerAvatarUrl:
                'https://avatars1.githubusercontent.com/u/54310907?v=4',
            },
            cursor:
              'WyJhc3luYy1saWJyYXJ5LnJlYWN0LWFzeW5jIiwxNTg4NjU2NzUwMDc2XQ==',
          },
        ],
      };

      // Add your test code here
    });
  });
});copy
```

You can put the test file where you please. However, it is recommended to follow one of the ways of organizing test files introduced earlier. Use the _repositories_ variable as the repository data for the test. There should be no need to alter the variable's value. Note that the repository data contains two repositories, which means that you need to check that both repositories' information is present.
#### Exercise 10.18: testing the sign in form
Implement a test that ensures that filling the sign in form's username and password fields and pressing the submit button _will call_ the _onSubmit_ handler with _correct arguments_. The _first argument_ of the handler should be an object representing the form's values. You can ignore the other arguments of the function. Remember that the _onSubmit_ handler is called or not.
You don't have to test any Apollo Client or AsyncStorage related code which is in the _useSignIn_ hook. As in the previous exercise, extract the pure code into its own component and test it in the test.
Note that Formik's form submissions are _asynchronous_ so expecting the _onSubmit_ function to be called immediately after pressing the submit button won't work. You can get around this issue by making the test function an async function using the _async_ keyword and using the React Native Testing Library's _waitFor_ function can be used to wait for expectations to pass. If the expectations don't pass within a certain period, the function will throw an error. Here is a rough example of how to use it:

```
import { render, screen, fireEvent, waitFor } from '@testing-library/react-native';
// ...

describe('SignIn', () => {
  describe('SignInContainer', () => {
    it('calls onSubmit function with correct arguments when a valid form is submitted', async () => {
      // render the SignInContainer component, fill the text inputs and press the submit button

      await waitFor(() => {
        // expect the onSubmit function to have been called once and with a correct first argument
      });
    });
  });
});copy
```

### Extending our application
It is time to put everything we have learned so far to good use and start extending our application. Our application still lacks a few important features such as reviewing a repository and registering a user. The upcoming exercises will focus on these essential features.
### Exercises 10.19. - 10.26
#### Exercise 10.19: the single repository view
Implement a view for a single repository, which contains the same repository information as in the reviewed repositories list but also a button for opening the repository in GitHub. It would be a good idea to reuse the _RepositoryItem_ component used in the _RepositoryList_ component and display the GitHub repository button for example based on a boolean prop.
The repository's URL is in the _url_ field of the _Repository_ type in the GraphQL schema. You can fetch a single repository from the Apollo server with the _repository_ query. The query has a single argument, which is the id of the repository. Here's a simple example of the _repository_ query:

```
{
  repository(id: "jaredpalmer.formik") {
    id
    fullName
    url
  }
}copy
```

As always, test your queries in the Apollo Sandbox first before using them in your application. If you are unsure about the GraphQL schema or what are the available queries, take a look at the documentation next to the operations editor. If you have trouble using the id as a variable in the query, take a moment to study the Apollo Client's
To learn how to open a URL in a browser, read the Expo's
The view should have its own route. It would be a good idea to define the repository's id in the route's path as a path parameter, which you can access by using the _RepositoryItem_ with a _RepositoryList_ component and using _navigate_ function to change the route in an _onPress_ event handler. You can access the _navigate_ function with the
The final version of the single repository view should look something like this:
![Application preview](../assets/e7ae265330250b44.jpg)
__Note__ if the peer depencendy issues prevent installing the library, try the _--legacy-peer-deps_ option:

```
npm install expo-linking --legacy-peer-depscopy
```

#### Exercise 10.20: repository's review list
Now that we have a view for a single repository, let's display repository's reviews there. Repository's reviews are in the _reviews_ field of the _Repository_ type in the GraphQL schema. _reviews_ is a similar paginated list as in the _repositories_ query. Here's an example of getting reviews of a repository:

```
{
  repository(id: "jaredpalmer.formik") {
    id
    fullName
    reviews {
      edges {
        node {
          id
          text
          rating
          createdAt
          user {
            id
            username
          }
        }
      }
    }
  }
}copy
```

Review's _text_ field contains the textual review, _rating_ field a numeric rating between 0 and 100, and _createdAt_ the date when the review was created. Review's _user_ field contains the reviewer's information, which is of type _User_.
We want to display reviews as a scrollable list, which makes _FlatList_ component's _RepositoryList_ component. Here's an example of the structure:

```
const RepositoryInfo = ({ repository }) => {
  // Repository's information implemented in the previous exercise
};

const ReviewItem = ({ review }) => {
  // Single review item
};

const SingleRepository = () => {
  // ...

  return (
    <FlatList
      data={reviews}
      renderItem={({ item }) => <ReviewItem review={item} />}
      keyExtractor={({ id }) => id}
      ListHeaderComponent={() => <RepositoryInfo repository={repository} />}
      // ...
    />
  );
};

export default SingleRepository;copy
```

The final version of the repository's reviews list should look something like this:
![Application preview](../assets/1ffde7816293e9b6.jpg)
The date under the reviewer's username is the creation date of the review, which is in the _createdAt_ field of the _Review_ type. The date format should be user-friendly such as _day.month.year_. You can for example install the
The round shape of the rating's container can be achieved with the _borderRadius_ style property. You can make it round by fixing the container's _width_ and _height_ style property and setting the border-radius as _width / 2_.
#### Exercise 10.21: the review form
Implement a form for creating a review using Formik. The form should have four fields: repository owner's GitHub username (for example "jaredpalmer"), repository's name (for example "formik"), a numeric rating, and a textual review. Validate the fields using Yup schema so that it contains the following validations:

- Repository owner's username is a required string
- Repository's name is a required string
- Rating is a required number between 0 and 100
- Review is a optional string


Explore Yup's _message_ argument. You can make the review field expand to multiple lines by using _TextInput_ component's
You can create a review using the _createReview_ mutation. Check this mutation's arguments in the Apollo Sandbox. You can use the
After a successful _createReview_ mutation, redirect the user to the repository's view you implemented in the previous exercise. This can be done with the _navigate_ function after you have obtained it using the _repositoryId_ field which you can use to construct the route's path.
To prevent getting cached data with the _repository_ query in the single repository view, use the _cache-and-network_ _useQuery_ hook like this:

```
useQuery(GET_REPOSITORY, {
  fetchPolicy: 'cache-and-network',
  // Other options
});copy
```

Note that only _an existing public GitHub repository_ can be reviewed and a user can review the same repository _only once_. You don't have to handle these error cases, but the error payload includes specific codes and messages for these errors. You can try out your implementation by reviewing one of your own public repositories or any other public repository.
The review form should be accessible through the app bar. Create a tab to the app bar with a label "Create a review". This tab should only be visible to users who have signed in. You will also need to define a route for the review form.
The final version of the review form should look something like this:
![Application preview](../assets/dbb90a8fe575c03e.jpg)
This screenshot has been taken after invalid form submission to present what the form should look like in an invalid state.
#### Exercise 10.22: the sign up form
Implement a sign up form for registering a user using Formik. The form should have three fields: username, password, and password confirmation. Validate the form using Yup schema so that it contains the following validations:

- Username is a required string with a length between 5 and 30
- Password is a required string with a length between 5 and 50
- Password confirmation matches the password


The password confirmation field's validation can be a bit tricky, but it can be done for example by using the
You can create a new user by using the _createUser_ mutation. Find out how this mutation works by exploring the documentation in the Apollo Sandbox. After a successful _createUser_ mutation, sign the created user in by using the _useSignIn_ hook as we did in the sign in the form. After the user has been signed in, redirect the user to the reviewed repositories list view.
The user should be able to access the sign-up form through the app bar by pressing a "Sign up" tab. This tab should only be visible to users that aren't signed in.
The final version of the sign up form should look something like this:
![Application preview](../assets/85f395a93ced2415.jpg)
This screenshot has been taken after invalid form submission to present what the form should look like in an invalid state.
#### Exercise 10.23: sorting the reviewed repositories list
At the moment repositories in the reviewed repositories list are ordered by the date of repository's first review. Implement a feature that allows users to select the principle, which is used to order the repositories. The available ordering principles should be:

- Latest repositories. The repository with the latest first review is on the top of the list. This is the current behavior and should be the default principle.
- Highest rated repositories. The repository with the _highest_ average rating is on the top of the list.
- Lowest rated repositories. The repository with the _lowest_ average rating is on the top of the list.


The _repositories_ query used to fetch the reviewed repositories has an argument called _orderBy_ , which you can use to define the ordering principle. The argument has two allowed values: CREATED_AT (order by the date of repository's first review) and RATING_AVERAGE, (order by the repository's average rating). The query also has an argument called _orderDirection_ which can be used to change the order direction. The argument has two allowed values: _ASC_ (ascending, smallest value first) and _DESC_ (descending, biggest value first).
The selected ordering principle state can be maintained for example using the React's _repositories_ query can be given to the _useRepositories_ hook as an argument.
You can use for example _FlatList_ component's
The final version of the feature, depending on the selection component in use, should look something like this:
![Application preview](../assets/b0a857cb35c9afa3.jpg)
#### Exercise 10.24: filtering the reviewed repositories list
The Apollo Server allows filtering repositories using the repository's name or the owner's username. This can be done using the _searchKeyword_ argument in the _repositories_ query. Here's an example of how to use the argument in a query:

```
{
  repositories(searchKeyword: "ze") {
    edges {
      node {
        id
        fullName
      }
    }
  }
}copy
```

Implement a feature for filtering the reviewed repositories list based on a keyword. Users should be able to type in a keyword into a text input and the list should be filtered as the user types. You can use a simple _TextInput_ component or something a bit fancier such as React Native Paper's _FlatList_ component's header.
To avoid a multitude of unnecessary requests while the user types the keyword fast, only pick the latest input after a short delay. This technique is often referred to as _useState_ hook and then pass the debounced value to the query as the value of the _searchKeyword_ argument.
You probably face an issue that the text input component loses focus after each keystroke. This is because the content provided by the _ListHeaderComponent_ prop is constantly unmounted. This can be fixed by turning the component rendering the _FlatList_ component into a class component and defining the header's render function as a class property like this:

```
export class RepositoryListContainer extends React.Component {
  renderHeader = () => {
    // this.props contains the component's props
    const props = this.props;

    // ...

    return (
      <RepositoryListHeader
      // ...
      />
    );
  };

  render() {
    return (
      <FlatList
        // ...
        ListHeaderComponent={this.renderHeader}
      />
    );
  }
}copy
```

The final version of the filtering feature should look something like this:
![Application preview](../assets/bcaa50ce4074d51d.jpg)
#### Exercise 10.25: the user's reviews view
Implement a feature which allows user to see their reviews. Once signed in, the user should be able to access this view by pressing a "My reviews" tab in the app bar. Here is what the review list view should roughly look like:
![Application preview](../assets/6f6b5016290f9006.jpg)
Remember that you can fetch the authenticated user from the Apollo Server with the _me_ query. This query returns a _User_ type, which has a field _reviews_. If you have already implemented a reusable _me_ query in your code, you can customize this query to fetch the _reviews_ field conditionally. This can be done using GraphQL's
Let's say that the current query is implemented roughly in the following manner:

```
const GET_CURRENT_USER = gql`
  query {
    me {
      # user fields...
    }
  }
`;copy
```

You can provide the query with an _includeReviews_ argument and use that with the _include_ directive:

```
const GET_CURRENT_USER = gql`
  query getCurrentUser($includeReviews: Boolean = false) {
    me {
      # user fields...
      reviews @include(if: $includeReviews) {
        edges {
          node {
            # review fields...
          }
        }
      }
    }
  }
`;copy
```

The _includeReviews_ argument has a default value of _false_ , because we don't want to cause additional server overhead unless we explicitly want to fetch authenticated user's reviews. The principle of the _include_ directive is quite simple: if the value of the _if_ argument is _true_ , include the field, otherwise omit it.
#### Exercise 10.26: review actions
Now that user can see their reviews, let's add some actions to the reviews. Under each review on the review list, there should be two buttons. One button is for viewing the review's repository. Pressing this button should take the user to the single repository view implemented in one of the earlier exercises. The other button is for deleting the review. Pressing this button should delete the review. Here is what the actions should roughly look like:
![Application preview](../assets/c2e91a8472ade507.jpg)
Pressing the delete button should be followed by a confirmation alert. If the user confirms the deletion, the review is deleted. Otherwise, the deletion is discarded. You can implement the confirmation using the _Alert.alert_ method won't open any window in Expo web preview. Use either Expo mobile app or an emulator to see the what the alert window looks like.
Here is the confirmation alert that should pop out once the user presses the delete button:
![Application preview](../assets/b55b5a1e1789ca9c.jpg)
You can delete a review using the _deleteReview_ mutation. This mutation has a single argument, which is the id of the review to be deleted. After the mutation has been performed, the easiest way to update the review list's query is to call the
### Cursor-based pagination
When an API returns an ordered list of items from some collection, it usually returns a subset of the whole set of items to reduce the required bandwidth and to decrease the memory usage of the client applications. The desired subset of items can be parameterized so that the client can request for example the first twenty items on the list after some index. This technique is commonly referred to as _pagination_. When items can be requested after a certain item defined by a _cursor_ , we are talking about _cursor-based pagination_.
So cursor is just a serialized presentation of an item in an ordered list. Let's have a look at the paginated repositories returned by the _repositories_ query using the following query:

```
{
  repositories(first: 2) {
    totalCount
    edges {
      node {
        id
        fullName
        createdAt
      }
      cursor
    }
    pageInfo {
      endCursor
      startCursor
      hasNextPage
    }
  }
}copy
```

The _first_ argument tells the API to return only the first two repositories. Here's an example of a result of the query:

```
{
  "data": {
    "repositories": {
      "totalCount": 10,
      "edges": [
        {
          "node": {
            "id": "zeit.next.js",
            "fullName": "zeit/next.js",
            "createdAt": "2020-05-15T11:59:57.557Z"
          },
          "cursor": "WyJ6ZWl0Lm5leHQuanMiLDE1ODk1NDM5OTc1NTdd"
        },
        {
          "node": {
            "id": "zeit.swr",
            "fullName": "zeit/swr",
            "createdAt": "2020-05-15T11:58:53.867Z"
          },
          "cursor": "WyJ6ZWl0LnN3ciIsMTU4OTU0MzkzMzg2N10="
        }
      ],
      "pageInfo": {
        "endCursor": "WyJ6ZWl0LnN3ciIsMTU4OTU0MzkzMzg2N10=",
        "startCursor": "WyJ6ZWl0Lm5leHQuanMiLDE1ODk1NDM5OTc1NTdd",
        "hasNextPage": true
      }
    }
  }
}copy
```

The format of the result object and the arguments are based on the _edges_ array containing items with _node_ and _cursor_ attributes. As we know, the _node_ contains the repository itself. The _cursor_ on the other hand is a Base64 encoded representation of the node. In this case, it contains the repository's id and date of repository's creation as a timestamp. This is the information we need to point to the item when they are ordered by the creation time of the repository. The _pageInfo_ contains information such as the cursor of the first and the last item in the array.
Let's say that we want to get the next set of items _after_ the last item of the current set, which is the "zeit/swr" repository. We can set the _after_ argument of the query as the value of the _endCursor_ like this:

```
{
  repositories(first: 2, after: "WyJ6ZWl0LnN3ciIsMTU4OTU0MzkzMzg2N10=") {
    totalCount
    edges {
      node {
        id
        fullName
        createdAt
      }
      cursor
    }
    pageInfo {
      endCursor
      startCursor
      hasNextPage
    }
  }
}copy
```

Now that we have the next two items and we can keep on doing this until the _hasNextPage_ has the value _false_ , meaning that we have reached the end of the list. To dig deeper into cursor-based pagination, read Shopify's article
### Infinite scrolling
Vertically scrollable lists in mobile and desktop applications are commonly implemented using a technique called _infinite scrolling_. The principle of infinite scrolling is quite simple:

- Fetch the initial set of items
- When the user reaches the last item, fetch the next set of items after the last item


The second step is repeated until the user gets tired of scrolling or some scrolling limit is exceeded. The name "infinite scrolling" refers to the way the list seems to be infinite - the user can just keep on scrolling and new items keep on appearing on the list.
Let's have a look at how this works in practice using the Apollo Client's _useQuery_ hook. Apollo Client has a great
First, we need to know when the user has reached the end of the list. Luckily, the _FlatList_ component has a prop _onEndReach_ callback is called using the _RepositoryList_ component's _FlatList_ component so that it calls a function once the end of the list is reached:

```
export const RepositoryListContainer = ({
  repositories,
  onEndReach,
  /* ... */,
}) => {
  const repositoryNodes = repositories
    ? repositories.edges.map((edge) => edge.node)
    : [];

  return (
    <FlatList
      data={repositoryNodes}
      // ...
      onEndReached={onEndReach}
      onEndReachedThreshold={0.5}
    />
  );
};

const RepositoryList = () => {
  // ...

  const { repositories } = useRepositories(/* ... */);

  const onEndReach = () => {
    console.log('You have reached the end of the list');
  };

  return (
    <RepositoryListContainer
      repositories={repositories}
      onEndReach={onEndReach}
      // ...
    />
  );
};

export default RepositoryList;copy
```

Try scrolling to the end of the reviewed repositories list and you should see the message in the logs.
Next, we need to fetch more repositories once the end of the list is reached. This can be achieved using the _useQuery_ hook. To describe to Apollo Client how to merge the existing repositories in the cache with the next set of repositories, we can use a
Let's add a field policy for the _repositories_ query in the _apolloClient.js_ file:

```
import { ApolloClient, InMemoryCache, createHttpLink } from '@apollo/client';
import { setContext } from '@apollo/client/link/context';
import Constants from 'expo-constants';
import { relayStylePagination } from '@apollo/client/utilities';
const { apolloUri } = Constants.manifest.extra;

const httpLink = createHttpLink({
  uri: apolloUri,
});

const cache = new InMemoryCache({  typePolicies: {    Query: {      fields: {        repositories: relayStylePagination(),      },    },  },});
const createApolloClient = (authStorage) => {
  const authLink = setContext(async (_, { headers }) => {
    try {
      const accessToken = await authStorage.getAccessToken();

      return {
        headers: {
          ...headers,
          authorization: accessToken ? `Bearer ${accessToken}` : '',
        },
      };
    } catch (e) {
      console.log(e);

      return {
        headers,
      };
    }
  });

  return new ApolloClient({
    link: authLink.concat(httpLink),
    cache,  });
};

export default createApolloClient;copy
```

As mentioned earlier, the format of the pagination's result object and the arguments are based on the Relay's pagination specification. Luckily, Apollo Client provides a predefined field policy, _relayStylePagination_ , which can be used in this case.
Next, let's alter the _useRepositories_ hook so that it returns a decorated _fetchMore_ function, which calls the actual _fetchMore_ function with appropriate arguments so that we can fetch the next set of repositories:

```
const useRepositories = (variables) => {
  const { data, loading, fetchMore, ...result } = useQuery(GET_REPOSITORIES, {
    variables,
    // ...
  });

  const handleFetchMore = () => {
    const canFetchMore = !loading && data?.repositories.pageInfo.hasNextPage;

    if (!canFetchMore) {
      return;
    }

    fetchMore({
      variables: {
        after: data.repositories.pageInfo.endCursor,
        ...variables,
      },
    });
  };

  return {
    repositories: data?.repositories,
    fetchMore: handleFetchMore,
    loading,
    ...result,
  };
};copy
```

Make sure you have the _pageInfo_ and the _cursor_ fields in your _repositories_ query as described in the pagination examples. You will also need to include the _after_ and _first_ arguments for the query.
The _handleFetchMore_ function will call the Apollo Client's _fetchMore_ function if there are more items to fetch, which is determined by the _hasNextPage_ property. We also want to prevent fetching more items if fetching is already in process. In this case, _loading_ will be _true_. In the _fetchMore_ function we are providing the query with an _after_ variable, which receives the latest _endCursor_ value.
The final step is to call the _fetchMore_ function in the _onEndReach_ handler:

```
const RepositoryList = () => {
  // ...

  const { repositories, fetchMore } = useRepositories({
    first: 8,
    // ...
  });

  const onEndReach = () => {
    fetchMore();
  };

  return (
    <RepositoryListContainer
      repositories={repositories}
      onEndReach={onEndReach}
      // ...
    />
  );
};

export default RepositoryList;copy
```

Use a relatively small _first_ argument value such as 3 while trying out the infinite scrolling. This way you don't need to review too many repositories. You might face an issue that the _onEndReach_ handler is called immediately after the view is loaded. This is most likely because the list contains so few repositories that the end of the list is reached immediately. You can get around this issue by increasing the value of _first_ argument. Once you are confident that the infinite scrolling is working, feel free to use a larger value for the _first_ argument.
### Exercise 10.27
#### Exercise 10.27: infinite scrolling for the repository's reviews list
Implement infinite scrolling for the repository's reviews list. The _Repository_ type's _reviews_ field has the _first_ and _after_ arguments similar to the _repositories_ query. _ReviewConnection_ type also has the _pageInfo_ field just like the _RepositoryConnection_ type.
Here's an example query:

```
{
  repository(id: "jaredpalmer.formik") {
    id
    fullName
    reviews(first: 2, after: "WyIxYjEwZTRkOC01N2VlLTRkMDAtODg4Ni1lNGEwNDlkN2ZmOGYuamFyZWRwYWxtZXIuZm9ybWlrIiwxNTg4NjU2NzUwMDgwXQ==") {
      totalCount
      edges {
        node {
          id
          text
          rating
          createdAt
          repositoryId
          user {
            id
            username
          }
        }
        cursor
      }
      pageInfo {
        endCursor
        startCursor
        hasNextPage
      }
    }
  }
}copy
```

The cache's field policy can be similar as with the _repositories_ query:

```
const cache = new InMemoryCache({
  typePolicies: {
    Query: {
      fields: {
        repositories: relayStylePagination(),
      },
    },
    Repository: {      fields: {        reviews: relayStylePagination(),      },    },  },
});copy
```

As with the reviewed repositories list, use a relatively small _first_ argument value while you are trying out the infinite scrolling. You might need to create a few new users and use them to create a few new reviews to make the reviews list long enough to scroll. Set the value of the _first_ argument high enough so that the _onEndReach_ handler isn't called immediately after the view is loaded, but low enough so that you can see that more reviews are fetched once you reach the end of the list. Once everything is working as intended you can use a larger value for the _first_ argument.
This was the last exercise in this section. It's time to push your code to GitHub and mark all of your finished exercises to the
### Additional resources
As we are getting closer to the end of this part, let's take a moment to look at some additional React Native related resources.
#### React Native Paper
> Paper is a collection of customizable and production-ready components for React Native, following Google’s Material Design guidelines.
#### Styled-components
> Utilising tagged template literals (a recent addition to JavaScript) and the power of CSS, styled-components allows you to write actual CSS code to style your components. It also removes the mapping between components and styles – using components as a low-level styling construct could not be easier!
_StyleSheet.create_ method and the _style_ prop.
In styled-components components' styles are defined with the component using a feature called _at runtime_. This brings many possibilities, such as seamlessly switching between a light and a dark theme. It also has a full _Text_ component with style variations based on props:

```
import styled from 'styled-components/native';
import { css } from 'styled-components';

const FancyText = styled.Text`
  color: grey;
  font-size: 14px;

  ${({ isBlue }) =>
    isBlue &&
    css`
      color: blue;
    `}${({ isBig }) =>
    isBig &&
    css`
      font-size: 24px;
      font-weight: 700;
    `}`;

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

Because styled-components processes the style definitions, it is possible to use CSS-like snake case syntax with the property names and units in property values. However, units don't have any effect because property values are internally unitless. For more information on styled-components, head out to the
#### React-spring
> react-spring is a spring-physics based animation library that should cover most of your UI related animation needs. It gives you tools flexible enough to confidently cast your ideas into moving interfaces.
#### React Navigation
> Routing and navigation for your React Native apps
### Closing words
That's it, our application is ready. Good job! We have learned many new concepts during our journey such as setting up our React Native application using Expo, using React Native's core components and adding style to them, communicating with the server, and testing React Native applications. The final piece of the puzzle would be to deploy the application to the Apple App Store and Google Play Store.
Deploying the application is entirely _optional_ and it isn't quite trivial, because you also need to fork and deploy the
[Part 10c __Previous part__](../part10/01-communicating-with-server.md)[Part 11 __Next part__](../part11/01-part11.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)
