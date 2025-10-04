---{
  "title": "Deployment",
  "source_url": "https://fullstackopen.com/en/part11/deployment",
  "crawl_timestamp": "2025-10-04T19:15:46Z",
  "checksum": "0da44984afb32e1ed14d259a9ebc8514a231f285d9a0afd545bb232e63329a0a"
}
---[Skip to content](../part11/01-deployment-course-main-content.md)
[{() => fs}](https://fullstackopen.com/en/)
  * [About course](../about/01-about.md)
  * [Course contents](../#course-contents/01-course-contents.md)
  * [FAQ](../faq/01-faq.md)
  * [Partners](../companies/01-companies.md)
  * [Challenge](../challenge/01-challenge.md)
[Search from the material](../search/01-search.md)Toggle dark theme
Select languageSuomi English 中文 Español Français Português(BR) 

[Fullstack](../#course-contents/01-course-contents.md)
[Part 11](../part11/01-part11.md)
Deployment
[a Introduction to CI/CD](../part11/01-introduction-to-ci-cd.md)[b Getting started with GitHub Actions](../part11/01-getting-started-with-git-hub-actions.md)
c Deployment
  * [Anything that can go wrong...](../part11/01-deployment-anything-that-can-go-wrong.md)
  * [What does a good deployment system do?](../part11/01-deployment-what-does-a-good-deployment-system-do.md)
  * [Has the app been deployed?](../part11/01-deployment-has-the-app-been-deployed.md)
  * [Exercises 11.10-11.12. (Fly.io)](../part11/01-deployment-exercises-11-10-11-12-fly-io.md)
  * [Exercises 11.10-11.12. (Render)](../part11/01-deployment-exercises-11-10-11-12-render.md)


[d Keeping green](../part11/01-keeping-green.md)[e Expanding Further](../part11/01-expanding-further.md)
c
# Deployment
Having written a nice application it's time to think about how we're going to deploy it to the use of real users. 
In [part 3](../part3/01-deploying-app-to-internet.md) of this course, we did this by simply running a single command from terminal to get the code up and running the servers of the cloud provider 
It is pretty simple to release software in Fly.io and Render at least compared to many other types of hosting setups but it still contains risks: nothing prevents us from accidentally releasing broken code to production.
Next, we're going to look at the principles of making a deployment safely and some of the principles of deploying software on both a small and large scale. 
### Anything that can go wrong...
We'd like to define some rules about how our deployment process should work but before that, we have to look at some constraints of reality.
One phrasing of Murphy's Law holds that: "Anything that can go wrong will go wrong."
It's important to remember this when we plan out our deployment system. Some of the things we'll need to consider could include:
  * What if my computer crashes or hangs during deployment?
  * I'm connected to the server and deploying over the internet, what happens if my internet connection dies?
  * What happens if any specific instruction in my deployment script/system fails?
  * What happens if, for whatever reason, my software doesn't work as expected on the server I'm deploying to? Can I roll back to a previous version?
  * What happens if a user does an HTTP request to our software just before we do deployment (we didn't have time to send a response to the user)?


These are just a small selection of what can go wrong during a deployment, or rather, things that we should plan for. Regardless of what happens, our deployment system should **never** leave our software in a broken state. We should also always know (or be easily able to find out) what state a deployment is in.
Another important rule to remember when it comes to deployments (and CI in general) is: "Silent failures are **very** bad!"
This doesn't mean that failures need to be shown to the users of the software, it means we need to be aware if anything goes wrong. If we are aware of a problem, we can fix it. If the deployment system doesn't give any errors but fails, we may end up in a state where we believe we have fixed a critical bug but the deployment failed, leaving the bug in our production environment and us unaware of the situation.
### What does a good deployment system do?
Defining definitive rules or requirements for a deployment system is difficult, let's try anyway:
  * Our deployment system should be able to fail gracefully at **any** step of the deployment.
  * Our deployment system should **never** leave our software in a broken state.
  * Our deployment system should let us know when a failure has happened. It's more important to notify about failure than about success.
  * Our deployment system should allow us to roll back to a previous deployment
    * Preferably this rollback should be easier to do and less prone to failure than a full deployment
    * Of course, the best option would be an automatic rollback in case of deployment failures
  * Our deployment system should handle the situation where a user makes an HTTP request just before/during a deployment.
  * Our deployment system should make sure that the software we are deploying meets the requirements we have set for this (e.g. don't deploy if tests haven't been run).


Let's define some things we **want** in this hypothetical deployment system too:
  * We would like it to be fast
  * We'd like to have no downtime during the deployment (this is distinct from the requirement we have for handling user requests just before/during the deployment).


Next we will have two sets of exercises for automating the deployment with GitHub Actions, one for 
### Has the app been deployed?
Since we are not making any real changes to the app, it might be a bit hard to see if the app deployment really works. Let us create a dummy endpoint in the app that makes it possible to do some code changes and to ensure that the deployed version has really changed:
```
app.get('/version', (req, res) => {
  res.send('1') // change this string to ensure a new version deployed
})copy
```

### Exercises 11.10-11.12. (Fly.io)
If you rather want to use other hosting options, there is an alternative set of exercises for [Render](../part11/01-deployment-exercises-11-10-11-12-render.md).
#### 11.10 Deploying your application to Fly.io
Setup your application in [part 3](../part3/01-deploying-app-to-internet-application-to-the-internet.md).
In contrast to part 3, in this part we _do not deploy the code_ to Fly.io ourselves (with the command _flyctl deploy_), we let the GitHub Actions workflow do that for us. 
Before going to the automated deployment, we shall ensure in this exercise that the app can be deployed manually.
So, create a new app in Fly.io. After that generate a Fly.io API token with the command
```
fly tokens create deploycopy
```

You'll need the token soon for your deployment workflow so save it somewhere (but do not commit that to GitHub)!
As said, before setting up the deployment pipeline in the next exercise we will now ensure that a manual deployment with the command _flyctl deploy_ works.
A couple of changes are needed.
The configuration file _fly.toml_ should be modified to include the following:
```
[env]
  PORT = "3000" # add this where PORT matches the internal_port below

[processes]
  app = "node app.js" # add this

[http_service]
  internal_port = 3000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  processes = ["app"]copy
```

In 
We also need to alter the file _.dockerignore_ a bit, the next line should be removed:
```
distcopy
```

If the line is not removed, the product build of the frontend does not get downloaded to the Fly.io server.
Deployment should now work _if_ the production build exists in the local machine, that is, the command _npm build_ is run.
Before moving to the next exercise, make sure that the manual deployment with the command _flyctl deploy_ works!
#### 11.11 Automatic deployments
Extend the workflow with a step to deploy your application to Fly.io by following the advice given 
Note that the GitHub Action should create the production build (with _npm run build_) before the deployment step!
You need the authorization token that you just created for the deployment. The proper way to pass it's value to GitHub Actions is to use _Repository secrets_ :
![repo secret](../assets/d0403ce087bd9216.png)
Now the workflow can access the token value as follows:
```
${{secrets.FLY_API_TOKEN}}copy
```

If all goes well, your workflow log should look a bit like this:
![fullstack content](../assets/66d677689440d80f.png)
**Remember** that it is always essential to keep an eye on what is happening in server logs when playing around with product deployments, so use `flyctl logs` early and use it often. No, use it all the time!
#### 11.12 Health check
Each deployment in Fly.io creates a 
```
$ flyctl releases
VERSION	STATUS  	DESCRIPTION	USER           	DATE
v18    	complete	Release    	mluukkai@iki.fi	16h56m ago
v17    	complete	Release    	mluukkai@iki.fi	17h3m ago
v16    	complete	Release    	mluukkai@iki.fi	21h22m ago
v15    	complete	Release    	mluukkai@iki.fi	21h25m ago
v14    	complete	Release    	mluukkai@iki.fi	21h34m agocopy
```

It is essential to ensure that a deployment ends up in a _succeeding_ release, where the app is in healthy functional state. Fortunately, Fly.io has several configuration options that take care of the application health check.
If we change the app as follows, it fails to start:
```
app.listen(PORT, () => {
  this_causes_error
  // eslint-disable-next-line no-console
  console.log(`server started on port ${PORT}`)
})copy
```

In this case, the deployment fails:
```
$ flyctl releases
VERSION	STATUS  	DESCRIPTION	USER           	DATE
v19    	failed  	Release    	mluukkai@iki.fi	3m52s ago
v18    	complete	Release    	mluukkai@iki.fi	16h56m ago
v17    	complete	Release    	mluukkai@iki.fi	17h3m ago
v16    	complete	Release    	mluukkai@iki.fi	21h22m ago
v15    	complete	Release    	mluukkai@iki.fi	21h25m ago
v14    	complete	Release    	mluukkai@iki.fi	21h34m agocopy
```

The app however stays up and running, Fly.io does not replace the functioning version (v18) with the broken one (v19).
Let us consider the following change
```
// start app in a wrong port
app.listen(PORT + 1, () => {
  // eslint-disable-next-line no-console
  console.log(`server started on port ${PORT}`)
})copy
```

Now the app starts but it is connected to the wrong port, so the service will not be functional. Fly.io thinks this is a successful deployment, so it deploys the app in a broken state.
One possibility to prevent broken deployments is to use an HTTP-level check defined in section 
Add a simple endpoint for doing an application health check to the backend. You may e.g. copy this code:
```
app.get('/health', (req, res) => {
  res.send('ok')
})copy
```

Configure then an 
You also need to set the _fly.toml_) of the app to be _canary_. These strategies ensure that only an app with a healthy state gets deployed.
Ensure that GitHub Actions notices if a deployment breaks your application:
![fullstack content](../assets/673360b6865f6b88.png)
You may simulate this e.g. as follows:
```
app.get('/health', (req, res) => {
  // eslint-disable-next-line no-constant-condition
  if (true) throw('error...  ')
  res.send('ok')
})copy
```

### Exercises 11.10-11.12. (Render)
If you rather want to use other hosting options, there is an alternative set of exercises for [Fly.io](../part11/01-exercises-11-10-11-12-fly-io.md).
#### 11.10 Deploying your application to Render
Set up your application in [part 3](../part3/01-deploying-app-to-internet-application-to-the-internet.md). You have to carefully think about what should go to these settings:
![fullstack content](../assets/f923d6a23d4cc423.png)
If you need to run several commands in the build or start command, you may use a simple shell script for that.
Create eg. a file _build_step.sh_ with the following content:
```
#!/bin/bash

echo "Build script"

# add the commands herecopy
```

Give it execution permissions (Google or see e.g. 
```
$ ./build_step.sh
Build scriptcopy
```

Other option is to use a 
You also need to open the _Advanced settings_ and turn the auto-deploy off since we want to control the deployment in the GitHub Actions:
![fullstack content](../assets/55bbf798a89a397e.png)
Ensure now that you get the app up and running. Use the _Manual deploy_.
Most likely things will fail at the start, so remember to keep the _Logs_ open all the time.
#### 11.11 Automatic deployments
Next step is to automate the deployment. There are two options, a ready-made custom action or the use of the Render deploy hook.
**Deployment with custom action**
Go to GitHub Actions _render deploy_. There are several actions to choose from. You can pick any. Quite often the best choice is the one with the most stars. It is also a good idea to look if the action is actively maintained (time of the last release) and does it have many open issues or pull requests. 
**Warning** : for some reason, the most starred option 
Set up the action to your workflow and ensure that every commit that passes all the checks results in a new deployment. Note that you need Render API key and the app service id for the deployment. See _srv-_) is the id:
```
https://dashboard.render.com/web/srv-randomcharachtersherecopy
```

**Deployment with deploy hook**
Alternative, and perhaps a more reliable option is to use 
![fsorender1](../assets/beec97b81cea319b.png)
DON'T USE the plain URL in your pipeline. Instead create GitHub secrets for your key and service id: ![fsorender2](../assets/a33f390c5ba48cd2.png) Then you can use them like this: 
```
- name: Trigger deployment
  run: curl https://api.render.com/deploy/srv-${{ secrets.RENDER_SERVICE_ID }}?key=${{ secrets.RENDER_API_KEY }}copy
```

The deployment takes some time. See the events tab of the Render dashboard to see when the new deployment is ready:
![fullstack content](../assets/8d1899a83f6aada9.png)
#### 11.12 Health check
All tests pass and the new version of the app gets automatically deployed to Render so everything seems to be in order. But does the app really work? Besides the checks done in the deployment pipeline, it is extremely beneficial to have also some "application level" health checks ensuring that the app for real is in a functional state.
The 
Add a simple endpoint for doing an application health check to the backend. You may e.g. copy this code:
```
app.get('/health', (req, res) => {
  res.send('ok')
})copy
```

Commit the code and push it to GitHub. Ensure that you can access the health check endpoint of your app.
Configure now a _Health Check Path_ to your app. The configuration is done in the settings tab of the Render dashboard.
Make a change in your code, push it to GitHub, and ensure that the deployment succeeds.
Note that you can see the log of deployment by clicking the most recent deployment in the events tab.
When you are set up with the health check, simulate a broken deployment by changing the code as follows:
```
app.get('/health', (req, res) => {
  // eslint-disable-next-line no-constant-condition
  if (true) throw('error...  ')
  res.send('ok')
})copy
```

Push the code to GitHub and ensure that a broken version does not get deployed and the previous version of the app keeps running.
Before moving on, fix your deployment and ensure that the application works again as intended.
[ Part 11b **Previous part** ](../part11/01-getting-started-with-git-hub-actions.md)[ Part 11d **Next part** ](../part11/01-keeping-green.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)