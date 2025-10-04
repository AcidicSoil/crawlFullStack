---{
  "title": "Communicating with server",
  "source_url": "https://fullstackopen.com/en/part10/communicating_with_server",
  "crawl_timestamp": "2025-10-04T19:15:42Z",
  "checksum": "68ce575258c9e8f42c9009d7f14ba20daf7a8752d3186b075c64a22f083c60e1"
}
---[Skip to content](../part10/01-communicating-with-server-course-main-content.md)
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
Communicating with server
[a Introduction to React Native](../part10/01-introduction-to-react-native.md)[b React Native basics](../part10/01-react-native-basics.md)
c Communicating with server

- [HTTP requests](../part10/01-communicating-with-server-http-requests.md)
- [GraphQL and Apollo client](../part10/01-communicating-with-server-graph-ql-and-apollo-client.md)
- [Organizing GraphQL related code](../part10/01-communicating-with-server-organizing-graph-ql-related-code.md)
- [Evolving the structure](../part10/01-communicating-with-server-evolving-the-structure.md)
- [Exercise 10.11](../part10/01-communicating-with-server-exercise-10-11.md)
- [Environment variables](../part10/01-communicating-with-server-environment-variables.md)
- [Exercise 10.12](../part10/01-communicating-with-server-exercise-10-12.md)
- [Storing data in the user's device](../part10/01-communicating-with-server-storing-data-in-the-users-device.md)
- [Exercises 10.13. - 10.14](../part10/01-communicating-with-server-exercises-10-13-10-14.md)
- [Enhancing Apollo Client's requests](../part10/01-communicating-with-server-enhancing-apollo-clients-requests.md)
- [Using React Context for dependency injection](../part10/01-communicating-with-server-using-react-context-for-dependency-injection.md)
- [Exercises 10.15. - 10.16](../part10/01-communicating-with-server-exercises-10-15-10-16.md)


[d Testing and extending our application](../part10/01-testing-and-extending-our-application.md)
c
# Communicating with server
So far we have implemented features to our application without any actual server communication. For example, the reviewed repositories list we have implemented uses mock data and the sign in form doesn't send the user's credentials to any authentication endpoint. In this section, we will learn how to communicate with a server using HTTP requests, how to use Apollo Client in a React Native application, and how to store data in the user's device.
Soon we will learn how to communicate with a server in our application. Before we get to that, we need a server to communicate with. For this purpose, we have a completed server implementation in the
Before heading further into the material, set up the rate-repository-api server by following the setup instructions in the repository's _on the same computer_. This eases network requests considerably.
### HTTP requests
React Native provides
People who have used both Fetch API and XMLHttpRequest API most likely agree that the Fetch API is easier to use and more modern. However, this doesn't mean that XMLHttpRequest API doesn't have its uses. For the sake of simplicity, we will be only using the Fetch API in our examples.
Sending HTTP requests using the Fetch API can be done using the _fetch_ function. The first argument of the function is the URL of the resource:

```
fetch('https://my-api.com/get-end-point');copy
```

The default request method is _GET_. The second argument of the _fetch_ function is an options object, which you can use to for example to specify a different request method, request headers, or request body:

```
fetch('https://my-api.com/post-end-point', {
  method: 'POST',
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    firstParam: 'firstValue',
    secondParam: 'secondValue',
  }),
});copy
```

Note that these URLs are made up and won't (most likely) send a response to your requests. In comparison to Axios, the Fetch API operates on a bit lower level. For example, there isn't any request or response body serialization and parsing. This means that you have to for example set the _Content-Type_ header by yourself and use _JSON.stringify_ method to serialize the request body.
The _fetch_ function returns a promise which resolves a _are not rejected_ like for example in Axios. In case of a JSON formatted response we can parse the response body using the _Response.json_ method:

```
const fetchMovies = async () => {
  const response = await fetch('https://reactnative.dev/movies.json');
  const json = await response.json();

  return json;
};copy
```

For a more detailed introduction to the Fetch API, read the
Next, let's try the Fetch API in practice. The rate-repository-api server provides an endpoint for returning a paginated list of reviewed repositories. Once the server is running, you should be able to access the endpoint at _node_ key in the _edges_ array.
Unfortunately, if we´re using external device, we can't access the server directly in our application by using the _npm start_. In the console you should be able to see an URL starting with _exp://_ below the QR code, after the "Metro waiting on" text:
![metro console output with highlight over exp://<ip> url](../assets/01ec3c013259ce0e.png)
Copy the IP address between the _exp://_ and _:_ , which is in this example _192.168.1.33_. Construct an URL in format _<http://><IP_ADDRESS>:5000/api/repositories_ and open it in the browser. You should see the same response as you did with the _localhost_ URL.
Now that we know the end point's URL let's use the actual server-provided data in our reviewed repositories list. We are currently using mock data stored in the _repositories_ variable. Remove the _repositories_ variable and replace the usage of the mock data with this piece of code in the _RepositoryList.jsx_ file in the _components_ directory:

```
import { useState, useEffect } from 'react';
// ...

const RepositoryList = () => {
  const [repositories, setRepositories] = useState();

  const fetchRepositories = async () => {
    // Replace the IP address part with your own IP address!
    const response = await fetch('http://192.168.1.33:5000/api/repositories');
    const json = await response.json();

    console.log(json);

    setRepositories(json);
  };

  useEffect(() => {
    fetchRepositories();
  }, []);

  // Get the nodes from the edges array
  const repositoryNodes = repositories
    ? repositories.edges.map(edge => edge.node)
    : [];

  return (
    <FlatList
      data={repositoryNodes}
      // Other props
    />
  );
};

export default RepositoryList;copy
```

We are using the React's _useState_ hook to maintain the repository list state and the _useEffect_ hook to call the _fetchRepositories_ function when the _RepositoryList_ component is mounted. We extract the actual repositories into the _repositoryNodes_ variable and replace the previously used _repositories_ variable in the _FlatList_ component's _data_ prop with it. Now you should be able to see actual server-provided data in the reviewed repositories list.
It is usually a good idea to log the server's response to be able to inspect it as we did in the _fetchRepositories_ function. You should be able to see this log message in the Expo development tools if you navigate to your device's logs as we learned in the [Debugging](../part10/01-introduction-to-react-native-debugging.md) section. If you are using the Expo's mobile app for development and the network request is failing, make sure that the computer you are using to run the server and your phone are _connected to the same Wi-Fi network_. If that's not possible either use an emulator in the same computer as the server is running in or set up a tunnel to the localhost, for example, using
The current data fetching code in the RepositoryList component could do with some refactoring. For instance, the component is aware of the network request's details such as the end point's URL. In addition, the data fetching code has lots of reuse potential. Let's refactor the component's code by extract the data fetching code into its own hook. Create a directory _hooks_ in the _src_ directory and in that _hooks_ directory create a file _useRepositories.js_ with the following content:

```
import { useState, useEffect } from 'react';

const useRepositories = () => {
  const [repositories, setRepositories] = useState();
  const [loading, setLoading] = useState(false);

  const fetchRepositories = async () => {
    setLoading(true);

    // Replace the IP address part with your own IP address!
    const response = await fetch('http://192.168.1.33:5000/api/repositories');
    const json = await response.json();

    setLoading(false);
    setRepositories(json);
  };

  useEffect(() => {
    fetchRepositories();
  }, []);

  return { repositories, loading, refetch: fetchRepositories };
};

export default useRepositories;copy
```

Now that we have a clean abstraction for fetching the reviewed repositories, let's use the _useRepositories_ hook in the _RepositoryList_ component:

```
// ...
import useRepositories from '../hooks/useRepositories';
const RepositoryList = () => {
  const { repositories } = useRepositories();
  const repositoryNodes = repositories
    ? repositories.edges.map(edge => edge.node)
    : [];

  return (
    <FlatList
      data={repositoryNodes}
      // Other props
    />
  );
};

export default RepositoryList;copy
```

That's it, now the _RepositoryList_ component is no longer aware of the way the repositories are acquired. Maybe in the future, we will acquire them through a GraphQL API instead of a REST API. We will see what happens.
### GraphQL and Apollo client
In [part 8](../part8/01-part8.md) we learned about GraphQL and how to send GraphQL queries to an Apollo Server using the
As mentioned earlier, the rate-repository-api server provides a GraphQL API which is implemented with Apollo Server. Once the server is running, you can access the _always_ test it with the Apollo Sandbox first before implementing it in the code. It is much easier to debug possible problems in the query in the Apollo Sandbox than in the application. If you are uncertain what the available queries are or how to use them, you can see the documentation next to the operations editor:
![Apollo Sandbox](../assets/e34c16527441267a.png)
In our React Native application, we will be using the same

```
npm install @apollo/client graphqlcopy
```

Before we can start using Apollo Client, we will need to slightly configure the Metro bundler so that it handles the _.cjs_ file extensions used by the Apollo Client. First, let's install the _@expo/metro-config_ package which has the default Metro configuration:

```
npm install @expo/metro-config@0.17.4copy
```

Then, we can add the following configuration to a _metro.config.js_ in the root directory of our project:

```
const { getDefaultConfig } = require('@expo/metro-config');

const defaultConfig = getDefaultConfig(__dirname);

defaultConfig.resolver.sourceExts.push('cjs');

module.exports = defaultConfig;copy
```

Restart the Expo development tools so that changes in the configuration are applied.
Now that the Metro configuration is in order, let's create a utility function for creating the Apollo Client with the required configuration. Create a _utils_ directory in the _src_ directory and in that _utils_ directory create a file _apolloClient.js_. In that file configure the Apollo Client to connect to the Apollo Server:

```
import { ApolloClient, InMemoryCache } from '@apollo/client';


const createApolloClient = () => {
  return new ApolloClient({
    uri: 'http://192.168.1.100:4000/graphql',
    cache: new InMemoryCache(),
  });
};

export default createApolloClient;copy
```

The URL used to connect to the Apollo Server is otherwise the same as the one you used with the Fetch API except the port is _4000_ and the path is _/graphql_. Lastly, we need to provide the Apollo Client using the _App_ component in the _App.js_ file:

```
import { NativeRouter } from 'react-router-native';
import { ApolloProvider } from '@apollo/client';
import Main from './src/components/Main';
import createApolloClient from './src/utils/apolloClient';
const apolloClient = createApolloClient();
const App = () => {
  return (
    <NativeRouter>
      <ApolloProvider client={apolloClient}>        <Main />
      </ApolloProvider>    </NativeRouter>
  );
};

export default App;copy
```

### Organizing GraphQL related code
It is up to you how to organize the GraphQL related code in your application. However, for the sake of a reference structure, let's have a look at one quite simple and efficient way to organize the GraphQL related code. In this structure, we define queries, mutations, fragments, and possibly other entities in their own files. These files are located in the same directory. Here is an example of the structure you can use to get started:
![GraphQL structure](../assets/3fe54e3166fbbbf4.png)
You can import the _gql_ template literal tag used to define GraphQL queries from _@apollo/client_ library. If we follow the structure suggested above, we could have a _queries.js_ file in the _graphql_ directory for our application's GraphQL queries. Each of the queries can be stored in a variable and exported like this:

```
import { gql } from '@apollo/client';

export const GET_REPOSITORIES = gql`
  query {
    repositories {
      ${/* ... */}
    }
  }
`;

// other queries...copy
```

We can import these variables and use them with the _useQuery_ hook like this:

```
import { useQuery } from '@apollo/client';

import { GET_REPOSITORIES } from '../graphql/queries';

const Component = () => {
  const { data, error, loading } = useQuery(GET_REPOSITORIES);
  // ...
};copy
```

The same goes for organizing mutations. The only difference is that we define them in a different file, _mutations.js_. It is recommended to use
### Evolving the structure
Once our application grows larger there might be times when certain files grow too large to manage. For example, we have component _A_ which renders the components _B_ and _C_. All these components are defined in a file _A.jsx_ in a _components_ directory. We would like to extract components _B_ and _C_ into their own files _B.jsx_ and _C.jsx_ without major refactors. We have two options:

- Create files _B.jsx_ and _C.jsx_ in the _components_ directory. This results in the following structure:


```
components/
  A.jsx
  B.jsx
  C.jsx
  ...copy
```

- Create a directory _A_ in the _components_ directory and create files _B.jsx_ and _C.jsx_ there. To avoid breaking components that import the _A.jsx_ file, move the _A.jsx_ file to the _A_ directory and rename it to _index.jsx_. This results in the following structure:


```
components/
  A/
    B.jsx
    C.jsx
    index.jsx
  ...copy
```

The first option is fairly decent, however, if components _B_ and _C_ are not reusable outside the component _A_ , it is useless to bloat the _components_ directory by adding them as separate files. The second option is quite modular and doesn't break any imports because importing a path such as _./A_ will match both _A.jsx_ and _A/index.jsx_.
### Exercise 10.11
#### Exercise 10.11: fetching repositories with Apollo Client
We want to replace the Fetch API implementation in the _useRepositories_ hook with a GraphQL query. Open the Apollo Sandbox at _repositories_ query. The query has some arguments, however, all of these are optional so you don't need to specify them. In the Apollo Sandbox form a query for fetching the repositories with the fields you are currently displaying in the application. The result will be paginated and it contains the up to first 30 results by default. For now, you can ignore the pagination entirely.
Once the query is working in the Apollo Sandbox, use it to replace the Fetch API implementation in the _useRepositories_ hook. This can be achieved using the _gql_ template literal tag can be imported from the _@apollo/client_ library as instructed earlier. Consider using the structure recommended earlier for the GraphQL related code. To avoid future caching issues, use the _cache-and-network_ _useQuery_ hook like this:

```
useQuery(MY_QUERY, {
  fetchPolicy: 'cache-and-network',
  // Other options
});copy
```

The changes in the _useRepositories_ hook should not affect the _RepositoryList_ component in any way.
### Environment variables
Every application will most likely run in more than one environment. Two obvious candidates for these environments are the development environment and the production environment. Out of these two, the development environment is the one we are running the application right now. Different environments usually have different dependencies, for example, the server we are developing locally might use a local database whereas the server that is deployed to the production environment uses the production database. To make the code environment independent we need to parametrize these dependencies. At the moment we are using one very environment dependant hardcoded value in our application: the URL of the server.
We have previously learned that we can provide running programs with environment variables. These variables can be defined in the command line or using environment configuration files such as _.env_ files and third-party libraries such as _Dotenv_. Unfortunately, React Native doesn't have direct support for environment variables. However, we can access the Expo configuration defined in the _app.json_ file at runtime from our JavaScript code. This configuration can be used to define and access environment dependant variables.
The configuration can be accessed by importing the _Constants_ constant from the _expo-constants_ module as we have done a few times before. Once imported, the _Constants.expoConfig_ property will contain the configuration. Let's try this by logging _Constants.expoConfig_ in the _App_ component:

```
import { NativeRouter } from 'react-router-native';
import { ApolloProvider } from '@apollo/client';
import Constants from 'expo-constants';
import Main from './src/components/Main';
import createApolloClient from './src/utils/apolloClient';

const apolloClient = createApolloClient();

const App = () => {
  console.log(Constants.expoConfig);
  return (
    <NativeRouter>
      <ApolloProvider client={apolloClient}>
        <Main />
      </ApolloProvider>
    </NativeRouter>
  );
};

export default App;copy
```

You should now see the configuration in the logs.
The next step is to use the configuration to define environment dependant variables in our application. Let's get started by renaming the _app.json_ file to _app.config.js_. Once the file is renamed, we can use JavaScript inside the configuration file. Change the file contents so that the previous object:

```
{
  "expo": {
    "name": "rate-repository-app",
    // rest of the configuration...
  }
}copy
```

Is turned into an export, which contains the contents of the _expo_ property:

```
export default {
   name: 'rate-repository-app',
   // rest of the configuration...
};copy
```

Expo has reserved an _env_ variable into our application's configuration. Note, that the older versions used (now deprecated) manifest instead of expoConfig.

```
export default {
   name: 'rate-repository-app',
   // rest of the configuration...
   extra: {     env: 'development'   },};copy
```

If you make changes in configuration, the restart may not be enough. You may need to start the application with cache cleared by command:

```
npx expo start --clearcopy
```

Now, restart Expo development tools to apply the changes and you should see that the value of _Constants.expoConfig_ property has changed and now includes the _extra_ property containing our application-specific configuration. Now the value of the _env_ variable is accessible through the _Constants.expoConfig.extra.env_ property.
Because using hard coded configuration is a bit silly, let's use an environment variable instead:

```
export default {
   name: 'rate-repository-app',
   // rest of the configuration...
   extra: {     env: process.env.ENV,   },};copy
```

As we have learned, we can set the value of an environment variable through the command line by defining the variable's name and value before the actual command. As an example, start Expo development tools and set the environment variable _ENV_ as _test_ like this:

```
ENV=test npm startcopy
```

If you take a look at the logs, you should see that the _Constants.expoConfig.extra.env_ property has changed.
We can also load environment variables from an _.env_ file as we have learned in the previous parts. First, we need to install the

```
npm install dotenvcopy
```

Next, add a _.env_ file in the root directory of our project with the following content:

```
ENV=developmentcopy
```

Finally, import the library in the _app.config.js_ file:

```
import 'dotenv/config';
export default {
   name: 'rate-repository-app',
   // rest of the configuration...
   extra: {
     env: process.env.ENV,
   },
};copy
```

You need to restart Expo development tools to apply the changes you have made to the _.env_ file.
Note that it is _never_ a good idea to put sensitive data into the application's configuration. The reason for this is that once a user has downloaded your application, they can, at least in theory, reverse engineer your application and figure out the sensitive data you have stored into the code.
### Exercise 10.12
#### Exercise 10.12: environment variables
Instead of the hardcoded Apollo Server's URL, use an environment variable defined in the _.env_ file when initializing the Apollo Client. You can name the environment variable for example _APOLLO_URI_.
_Do not_ try to access environment variables like _process.env.APOLLO_URI_ outside the _app.config.js_ file. Instead use the _Constants.expoConfig.extra_ object like in the previous example. In addition, do not import the dotenv library outside the _app.config.js_ file or you will most likely face errors.
### Storing data in the user's device
There are times when we need to store some persisted pieces of data in the user's device. One such common scenario is storing the user's authentication token so that we can retrieve it even if the user closes and reopens our application. In web development, we have used the browser's _localStorage_ object to achieve such functionality. React Native provides similar persistent storage, the
We can use the _npx expo install_ command to install the version of the _@react-native-async-storage/async-storage_ package that is suitable for our Expo SDK version:

```
npx expo install @react-native-async-storage/async-storagecopy
```

The API of the _AsyncStorage_ is in many ways same as the _localStorage_ API. They are both key-value storages with similar methods. The biggest difference between the two is that, as the name implies, the operations of _AsyncStorage_ are _asynchronous_.
Because _AsyncStorage_ operates with string keys in a global namespace it is a good idea to create a simple abstraction for its operations. This abstraction can be implemented for example using a

```
import AsyncStorage from '@react-native-async-storage/async-storage';

class ShoppingCartStorage {
  constructor(namespace = 'shoppingCart') {
    this.namespace = namespace;
  }

  async getProducts() {
    const rawProducts = await AsyncStorage.getItem(
      `${this.namespace}:products`,
    );

    return rawProducts ? JSON.parse(rawProducts) : [];
  }

  async addProduct(productId) {
    const currentProducts = await this.getProducts();
    const newProducts = [...currentProducts, productId];

    await AsyncStorage.setItem(
      `${this.namespace}:products`,
      JSON.stringify(newProducts),
    );
  }

  async clearProducts() {
    await AsyncStorage.removeItem(`${this.namespace}:products`);
  }
}

const doShopping = async () => {
  const shoppingCartA = new ShoppingCartStorage('shoppingCartA');
  const shoppingCartB = new ShoppingCartStorage('shoppingCartB');

  await shoppingCartA.addProduct('chips');
  await shoppingCartA.addProduct('soda');

  await shoppingCartB.addProduct('milk');

  const productsA = await shoppingCartA.getProducts();
  const productsB = await shoppingCartB.getProducts();

  console.log(productsA, productsB);

  await shoppingCartA.clearProducts();
  await shoppingCartB.clearProducts();
};

doShopping();copy
```

Because _AsyncStorage_ keys are global, it is usually a good idea to add a _namespace_ for the keys. In this context, the namespace is just a prefix we provide for the storage abstraction's keys. Using the namespace prevents the storage's keys from colliding with other _AsyncStorage_ keys. In this example, the namespace is defined as the constructor's argument and we are using the _namespace:key_ format for the keys.
We can add an item to the storage using the _must be a string_ , so we need to serialize non-string values as we did with the _JSON.stringify_ method. The
**NB:** _AsyncStorage_ but it encrypts the stored data. This makes it more suitable for storing more sensitive data such as the user's credit card number.
### Exercises 10.13. - 10.14
#### Exercise 10.13: the sign in form mutation
The current implementation of the sign in form doesn't do much with the submitted user's credentials. Let's do something about that in this exercise. First, read the rate-repository-api server's
Once you have figured out how the authentication works, create a file _useSignIn.js_ file in the _hooks_ directory. In that file implement a _useSignIn_ hook that sends the _authenticate_ mutation using the _authenticate_ mutation has a _single_ argument called _credentials_ , which is of type _AuthenticateInput_. This _username_ and _password_ fields.
The return value of the hook should be a tuple _[signIn, result]_ where _result_ is the mutations result as it is returned by the _useMutation_ hook and _signIn_ a function that runs the mutation with a _{ username, password }_ object argument. Hint: don't pass the mutation function to the return value directly. Instead, return a function that calls the mutation function like this:

```
const useSignIn = () => {
  const [mutate, result] = useMutation(/* mutation arguments */);

  const signIn = async ({ username, password }) => {
    // call the mutate function here with the right arguments
  };

  return [signIn, result];
};copy
```

Once the hook is implemented, use it in the _SignIn_ component's _onSubmit_ callback for example like this:

```
const SignIn = () => {
  const [signIn] = useSignIn();

  const onSubmit = async (values) => {
    const { username, password } = values;

    try {
      const { data } = await signIn({ username, password });
      console.log(data);
    } catch (e) {
      console.log(e);
    }
  };

  // ...
};copy
```

This exercise is completed once you can log the user's _authenticate_ mutations result after the sign in form has been submitted. The mutation result should contain the user's access token.
#### Exercise 10.14: storing the access token step1
Now that we can obtain the access token we need to store it. Create a file _authStorage.js_ in the _utils_ directory with the following content:

```
import AsyncStorage from '@react-native-async-storage/async-storage';

class AuthStorage {
  constructor(namespace = 'auth') {
    this.namespace = namespace;
  }

  getAccessToken() {
    // Get the access token for the storage
  }

  setAccessToken(accessToken) {
    // Add the access token to the storage
  }

  removeAccessToken() {
    // Remove the access token from the storage
  }
}

export default AuthStorage;copy
```

Next, implement the methods _AuthStorage.getAccessToken_ , _AuthStorage.setAccessToken_ and _AuthStorage.removeAccessToken_. Use the _namespace_ variable to give your keys a namespace like we did in the previous example.
### Enhancing Apollo Client's requests
Now that we have implemented storage for storing the user's access token, it is time to start using it. Initialize the storage in the _App_ component:

```
import { NativeRouter } from 'react-router-native';
import { ApolloProvider } from '@apollo/client';

import Main from './src/components/Main';
import createApolloClient from './src/utils/apolloClient';
import AuthStorage from './src/utils/authStorage';
const authStorage = new AuthStorage();const apolloClient = createApolloClient(authStorage);
const App = () => {
  return (
    <NativeRouter>
      <ApolloProvider client={apolloClient}>
        <Main />
      </ApolloProvider>
    </NativeRouter>
  );
};

export default App;copy
```

We also provided the storage instance for the _createApolloClient_ function as an argument. This is because next, we will send the access token to Apollo Server in each request. The Apollo Server will expect that the access token is present in the _Authorization_ header in the format _Bearer <ACCESS_TOKEN>_. We can enhance the Apollo Client's request by using the _createApolloClient_ function in the _apolloClient.js_ file:

```
import { ApolloClient, InMemoryCache, createHttpLink } from '@apollo/client';
import Constants from 'expo-constants';
import { setContext } from '@apollo/client/link/context';
// You might need to change this depending on how you have configured the Apollo Server's URI
const { apolloUri } = Constants.expoConfig.extra;

const httpLink = createHttpLink({
  uri: apolloUri,
});

const createApolloClient = (authStorage) => {  const authLink = setContext(async (_, { headers }) => {    try {      const accessToken = await authStorage.getAccessToken();      return {        headers: {          ...headers,          authorization: accessToken ? `Bearer ${accessToken}` : '',        },      };    } catch (e) {      console.log(e);      return {        headers,      };    }  });  return new ApolloClient({    link: authLink.concat(httpLink),    cache: new InMemoryCache(),  });};
export default createApolloClient;copy
```

### Using React Context for dependency injection
The last piece of the sign-in puzzle is to integrate the storage to the _useSignIn_ hook. To achieve this the hook must be able to access token storage instance we have initialized in the _App_ component. React _contexts_ in the _src_ directory. In that directory create a file _AuthStorageContext.js_ with the following content:

```
import { createContext } from 'react';

const AuthStorageContext = createContext();

export default AuthStorageContext;copy
```

Now we can use the _AuthStorageContext.Provider_ to provide the storage instance to the descendants of the context. Let's add it to the _App_ component:

```
import { NativeRouter } from 'react-router-native';
import { ApolloProvider } from '@apollo/client';

import Main from './src/components/Main';
import createApolloClient from './src/utils/apolloClient';
import AuthStorage from './src/utils/authStorage';
import AuthStorageContext from './src/contexts/AuthStorageContext';
const authStorage = new AuthStorage();
const apolloClient = createApolloClient(authStorage);

const App = () => {
  return (
    <NativeRouter>
      <ApolloProvider client={apolloClient}>
        <AuthStorageContext.Provider value={authStorage}>          <Main />
        </AuthStorageContext.Provider>      </ApolloProvider>
    </NativeRouter>
  );
};

export default App;copy
```

Accessing the storage instance in the _useSignIn_ hook is now possible using the React's

```
// ...
import { useContext } from 'react';
import AuthStorageContext from '../contexts/AuthStorageContext';
const useSignIn = () => {
  const authStorage = useContext(AuthStorageContext);  // ...
};copy
```

Note that accessing a context's value using the _useContext_ hook only works if the _useContext_ hook is used in a component that is a _descendant_ of the
Accessing the _AuthStorage_ instance with _useContext(AuthStorageContext)_ is quite verbose and reveals the details of the implementation. Let's improve this by implementing a _useAuthStorage_ hook in a _useAuthStorage.js_ file in the _hooks_ directory:

```
import { useContext } from 'react';
import AuthStorageContext from '../contexts/AuthStorageContext';

const useAuthStorage = () => {
  return useContext(AuthStorageContext);
};

export default useAuthStorage;copy
```

The hook's implementation is quite simple but it improves the readability and maintainability of the hooks and components using it. We can use the hook to refactor the _useSignIn_ hook like this:

```
// ...
import useAuthStorage from '../hooks/useAuthStorage';
const useSignIn = () => {
  const authStorage = useAuthStorage();  // ...
};copy
```

The ability to provide data to component's descendants opens tons of use cases for React Context, as we already saw in the [last chapter](../part6/01-react-query-use-reducer-and-the-context.md) of part 6.
To learn more about these use cases, read Kent C. Dodds' enlightening article
### Exercises 10.15. - 10.16
#### Exercise 10.15: storing the access token step2
Improve the _useSignIn_ hook so that it stores the user's access token retrieved from the _authenticate_ mutation. The return value of the hook should not change. The only change you should make to the _SignIn_ component is that you should redirect the user to the reviewed repositories list view after a successful sign in. You can achieve this by using the
After the _authenticate_ mutation has been executed and you have stored the user's access token to the storage, you should reset the Apollo Client's store. This will clear the Apollo Client's cache and re-execute all active queries. You can do this by using the Apollo Client's _useSignIn_ hook using the

```
const { data } = await mutate(/* options */);
await authStorage.setAccessToken(/* access token from the data */);
apolloClient.resetStore();copy
```

#### Exercise 10.16: sign out
The final step in completing the sign in feature is to implement a sign out feature. The _me_ query can be used to check the authenticated user's information. If the query's result is _null_ , that means that the user is not authenticated. Open the Apollo Sandbox and run the following query:

```
{
  me {
    id
    username
  }
}copy
```

You will probably end up with the _null_ result. This is because the Apollo Sandbox is not authenticated, meaning that it doesn't send a valid access token with the request. Revise the _authenticate_ mutation. Use this access token in the _Authorization_ header as instructed in the documentation. Now, run the _me_ query again and you should be able to see the authenticated user's information.
Open the _AppBar_ component in the _AppBar.jsx_ file where you currently have the tabs "Repositories" and "Sign in". Change the tabs so that if the user is signed in the tab "Sign out" is displayed, otherwise show the "Sign in" tab. You can achieve this by using the _me_ query with the
Pressing the "Sign out" tab should remove the user's access token from the storage and reset the Apollo Client's store with the _resetStore_ method should automatically re-execute all active queries which means that the _me_ query should be re-executed. Note that the order of execution is crucial: access token must be removed from the storage _before_ the Apollo Client's store is reset.
This was the last exercise in this section. It's time to push your code to GitHub and mark all of your finished exercises to the
[Part 10b **Previous part**](../part10/01-react-native-basics.md)[Part 10d **Next part**](../part10/01-testing-and-extending-our-application.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)
