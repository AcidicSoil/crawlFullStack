---{
  "title": "Exercises: extending the bloglist",
  "source_url": "https://fullstackopen.com/en/part7/exercises_extending_the_bloglist",
  "crawl_timestamp": "2025-10-04T19:16:58Z",
  "checksum": "6a4a82f3ea259e98719acbc262346e59d32718bf73a3c094f85fb120af9e361b"
}
---[Skip to content](../part7/01-exercises-extending-the-bloglist-course-main-content.md)
[{() => fs}](https://fullstackopen.com/en/)
  * [About course](../about/01-about.md)
  * [Course contents](../#course-contents/01-course-contents.md)
  * [FAQ](../faq/01-faq.md)
  * [Partners](../companies/01-companies.md)
  * [Challenge](../challenge/01-challenge.md)
[Search from the material](../search/01-search.md)Toggle dark theme
Select languageSuomi English 中文 Español Français Português(BR) 

[Fullstack](../#course-contents/01-course-contents.md)
[Part 7](../part7/01-part7.md)
Exercises: extending the bloglist
[a React Router](../part7/01-react-router.md)[b Custom hooks](../part7/01-custom-hooks.md)[c More about styles](../part7/01-more-about-styles.md)[d Webpack](../part7/01-webpack.md)[e Class components, Miscellaneous](../part7/01-class-components-miscellaneous.md)
f Exercises: extending the bloglist
  * [Exercises 7.9.-7.21.](../part7/01-exercises-extending-the-bloglist-exercises-7-9-7-21.md)
  * [State Management: Redux](../part7/01-exercises-extending-the-bloglist-state-management-redux.md)
  * [State Management: React Query and Context](../part7/01-exercises-extending-the-bloglist-state-management-react-query-and-context.md)
  * [Views](../part7/01-exercises-extending-the-bloglist-views.md)


f
# Exercises: extending the bloglist
In addition to the eight exercises in the [React router](../part7/01-react-router.md) and [custom hooks](../part7/01-custom-hooks.md) sections of this seventh part of the course material, 13 exercises continue our work on the BlogList application that we worked on in parts four and five of the course material. Some of the following exercises are "features" that are independent of one another, meaning that there is no need to finish them in any particular order. You are free to skip over a part of the exercises if you wish to do so. Quite many of them are about applying the advanced state management technique (Redux, React Query and context) covered in [part 6](../part6/01-part6.md).
If you do not want to use your BlogList application, you are free to use the code from the model solution as a starting point for these exercises.
Many of the exercises in this part of the course material will require the refactoring of existing code. This is a common reality of extending existing applications, meaning that refactoring is an important and necessary skill even if it may feel difficult and unpleasant at times.
One good piece of advice for both refactoring and writing new code is to take _baby steps_. Losing your sanity is almost guaranteed if you leave the application in a completely broken state for long periods while refactoring.
### Exercises 7.9.-7.21.
#### 7.9: Automatic Code Formatting
In the previous parts, we used ESLint to ensure that the code follows the defined conventions. _an opinionated code formatter_ , that is, Prettier not only controls the code style but also formats the code according to the definition.
Prettier is easy to integrate into the code editor so that when it is saved, it is automatically formatted.
Take Prettier to use in your app and configure it to work with your editor.
### State Management: Redux
_There are two alternative versions to choose for exercises 7.10-7.13: you can do the state management of the application either using Redux or React Query and Context_. If you want to maximize your learning, you should do both versions!
#### 7.10: Redux, Step 1
Refactor the application to use Redux to manage the notification data.
#### 7.11: Redux, Step 2
_Note_ that this and the next two exercises are quite laborious but incredibly educational.
Store the information about blog posts in the Redux store. In this exercise, it is enough that you can see the blogs in the backend and create a new blog.
You are free to manage the state for logging in and creating new blog posts by using the internal state of React components.
#### 7.12: Redux, Step 3
Expand your solution so that it is again possible to like and delete a blog.
#### 7.13: Redux, Step 4
Store the information about the signed-in user in the Redux store.
### State Management: React Query and Context
_There are two alternative versions to choose for exercises 7.10-7.13: you can do the state management of the application either using Redux or React Query and Context_. If you want to maximize your learning, you should do both versions!
#### 7.10: React Query and Context step 1
Refactor the app to use the useReducer-hook and context to manage the notification data.
#### 7.11: React Query and Context step 2
Use React Query to manage the state for blog posts. For this exercise, it is sufficient that the application displays existing blogs and that the creation of a new blog is successful.
You are free to manage the state for logging in and creating new blog posts by using the internal state of React components.
#### 7.12: React Query and Context step 3
Expand your solution so that it is again possible to like and delete a blog.
#### 7.13: React Query and Context step 4
Use the useReducer-hook and context to manage the data for the logged in user.
### Views
The rest of the tasks are common to both the Redux and React Query versions.
#### 7.14: Users view
Implement a view to the application that displays all of the basic information related to users:
![browser blogs with users table showing blogs created](../assets/25b79fb46219b2e7.png)
#### 7.15: Individual User View
Implement a view for individual users that displays all of the blog posts added by that user:
![browser blogs showing users added blogs](../assets/54ed9dd4fa3750d6.png)
You can access this view by clicking the name of the user in the view that lists all users:
![browser blogs showing clickable users](../assets/a9767991aa4777e5.png)
_**NB:**_ you will almost certainly stumble across the following error message during this exercise:
![browser TypeError cannot read property name of undefined](../assets/4af89205f9231aa4.png)
The error message will occur if you refresh the individual user page.
The cause of the issue is that, when we navigate directly to the page of an individual user, the React application has not yet received the data from the backend. One solution for this problem is to use conditional rendering:
```
const User = () => {
  const user = ...
  if (!user) {    return null  }
  return (
    <div>
      // ...
    </div>
  )
}copy
```

#### 7.16: Blog View
Implement a separate view for blog posts. You can model the layout of your view after the following example:
![browser blogs showing single blog via URL /blogs/number](../assets/9bcc19f361427f73.png)
Users should be able to access this view by clicking the name of the blog post in the view that lists all of the blog posts.
![browser showing blogs are clickable](../assets/a5cc96e10d0bb221.png)
After you're done with this exercise, the functionality that was implemented in exercise 5.7 is no longer necessary. Clicking a blog post no longer needs to expand the item in the list and display the details of the blog post.
#### 7.17: Navigation
Implement a navigation menu for the application:
![browser blogs navigation navigation menu](../assets/008e70da1fe5d25a.png)
#### 7.18: Comments, step 1
Implement the functionality for commenting the blog posts:
![browser blogs showing list of comments for a blog](../assets/04890c1e0098bb89.png)
Comments should be anonymous, meaning that they are not associated with the user who left the comment.
In this exercise, it is enough for the frontend to only display the comments that the application receives from the backend.
An appropriate mechanism for adding comments to a blog post would be an HTTP POST request to the _api/blogs/:id/comments_ endpoint.
#### 7.19: Comments, step 2
Extend your application so that users can add comments to blog posts from the frontend:
![browser showing comments added via frontend](../assets/e56a5679e6ca5984.png)
#### 7.20: Styles, step 1
Improve the appearance of your application by applying one of the methods shown in the course material.
#### 7.21: Styles, step 2
You can mark this exercise as finished if you use an hour or more for styling your application.
This was the last exercise for this part of the course and it's time to push your code to GitHub and mark all of your finished exercises to the 
[ Part 7e **Previous part** ](../part7/01-class-components-miscellaneous.md)[ Part 8 **Next part** ](../part8/01-part8.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)