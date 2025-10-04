---{
  "title": "Grande finale: Patientor",
  "source_url": "https://fullstackopen.com/en/part9/grande_finale_patientor",
  "crawl_timestamp": "2025-10-04T19:17:22Z",
  "checksum": "62438befa541ee343c3fcf13df0bb7314abe509b719d3556d3b49831bcdeaeec"
}
---[Skip to content](../part9/01-grande-finale-patientor-course-main-content.md)
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
Grande finale: Patientor
[a Background and introduction](../part9/01-background-and-introduction.md)[b First steps with TypeScript](../part9/01-first-steps-with-type-script.md)[c Typing an Express app](../part9/01-typing-an-express-app.md)[d React with types](../part9/01-react-with-types.md)
e Grande finale: Patientor
  * [Working with an existing codebase](../part9/01-grande-finale-patientor-working-with-an-existing-codebase.md)
  * [Patientor frontend](../part9/01-grande-finale-patientor-patientor-frontend.md)
  * [Exercises 9.21-9.22](../part9/01-grande-finale-patientor-exercises-9-21-9-22.md)
  * [Full entries](../part9/01-grande-finale-patientor-full-entries.md)
  * [Omit with unions](../part9/01-grande-finale-patientor-omit-with-unions.md)
  * [Exercises 9.23-9.30](../part9/01-grande-finale-patientor-exercises-9-23-9-30.md)
  * [Submitting exercises and getting the credits](../part9/01-grande-finale-patientor-submitting-exercises-and-getting-the-credits.md)


e
# Grande finale: Patientor
### Working with an existing codebase
When diving into an existing codebase for the first time, it is good to get an overall view of the conventions and structure of the project. You can start your research by reading the _README.md_ in the root of the repository. Usually, the README contains a brief description of the application and the requirements for using it, as well as how to start it for development. If the README is not available or someone has "saved time" and left it as a stub, you can take a peek at the _package.json_. It is always a good idea to start the application and click around to verify you have a functional development environment.
You can also browse the folder structure to get some insight into the application's functionality and/or the architecture used. These are not always clear, and the developers might have chosen a way to organize code that is not familiar to you. The 
TypeScript provides types for what kind of data structures, functions, components, and state to expect. You can try looking for _types.ts_ or something similar to get started. VSCode is a big help and simply highlighting variables and parameters can provide quite a lot of insight. All this naturally depends on how types are used in the project.
If the project has unit, integration or end-to-end tests, reading those is most likely beneficial. Test cases are your most important tool when refactoring or adding new features to the application. You want to make sure not to break any existing features when hammering around the code. TypeScript can also give you guidance with argument and return types when changing the code.
Remember that reading code is a skill in itself, so don't worry if you don't understand the code on your first readthrough. The code may have a lot of corner cases, and pieces of logic may have been added here and there throughout its development cycle. It is hard to imagine what kind of problems the previous developer has wrestled with. Think of it all like 
### Patientor frontend
It's time to get our hands dirty finalizing the frontend for the backend we built in [exercises 9.8.-9.13](../part9/01-typing-an-express-app.md). We will actually also need some new features to the backend for finishing the app.
Before diving into the code, let us start both the frontend and the backend.
If all goes well, you should see a patient listing page. It fetches a list of patients from our backend, and renders it to the screen as a simple table. There is also a button for creating new patients on the backend. As we are using mock data instead of a database, the data will not persist - closing the backend will delete all the data we have added. UI design has not been a strong point of the creators, so let's disregard the UI for now.
After verifying that everything works, we can start studying the code. All the interesting stuff resides in the _src_ folder. For your convenience, there is already a _types.ts_ file for basic types used in the app, which you will have to extend or refactor in the exercises.
In principle, we could use the same types for both the backend and the frontend, but usually, the frontend has different data structures and use cases for the data, which causes the types to be different. For example, the frontend has a state and may want to keep data in objects or maps whereas the backend uses an array. The frontend might also not need all the fields of a data object saved in the backend, and it may need to add some new fields to use for rendering.
The folder structure looks as follows:
![vscode folder structure for patientor](../assets/67ce9c90d2ea10dc.png)
Besides the component _App_ and a directory for services, there are currently three main components: _AddPatientModal_ and _PatientListPage_ which are both defined in a directory and a component _HealthRatingBar_ defined in a file. If a component has some subcomponents not used elsewhere in the app, it might be a good idea to define the component and its subcomponents in a directory. For example, now the AddPatientModal is defined in the file _components/AddPatientModal/index.tsx_ and its subcomponent _AddPatientForm_ in its own file under the same directory.
There is nothing too surprising in the code. The state and communication with the backend are implemented with _useState_ hook and Axios, similar to the notes app in the previous section. [Material UI](../part7/01-more-about-styles-material-ui.md) is used to style the app and the navigation structure is implemented with [React Router](../part7/01-react-router.md), both familiar to us from part 7 of the course.
From the typing point of view, there are a couple of interesting things. Component _App_ passes the function _setPatients_ as a prop to the component _PatientListPage_ :
```
const App = () => {
  const [patients, setPatients] = useState<Patient[]>([]);
  // ...
  
  return (
    <div className="App">
      <Router>
        <Container>
          <Routes>
            // ...
            <Route path="/" element={
              <PatientListPage
                patients={patients}
                setPatients={setPatients}              />} 
            />
          </Routes>
        </Container>
      </Router>
    </div>
  );
};copy
```

To keep the TypeScript compiler happy, the props are typed as follows:
```
interface Props {
  patients : Patient[]
  setPatients: React.Dispatch<React.SetStateAction<Patient[]>>
}

const PatientListPage = ({ patients, setPatients } : Props ) => { 
  // ...
}copy
```

So the function _setPatients_ has type _React.Dispatch <React.SetStateAction<Patient[]>>_. We can see the type in the editor when we hover over the function:
![vscode showing Patient array as type for setPatients](../assets/34d42c5a34b48d95.png)
The 
_PatientListPage_ passes four props to the component _AddPatientModal_. Two of these props are functions. Let us have a look at how these are typed:
```
const PatientListPage = ({ patients, setPatients } : Props ) => {

  const [modalOpen, setModalOpen] = useState<boolean>(false);
  const [error, setError] = useState<string>();

  // ...

  const closeModal = (): void => {    setModalOpen(false);
    setError(undefined);
  };

  const submitNewPatient = async (values: PatientFormValues) => {    // ...
  };
  // ...

  return (
    <div className="App">
      // ...
      <AddPatientModal
        modalOpen={modalOpen}
        onSubmit={submitNewPatient}        error={error}
        onClose={closeModal}      />
    </div>
  );
};copy
```

Types look like the following:
```
interface Props {
  modalOpen: boolean;
  onClose: () => void;
  onSubmit: (values: PatientFormValues) => Promise<void>;
  error?: string;
}

const AddPatientModal = ({ modalOpen, onClose, onSubmit, error }: Props) => {
  // ...
}copy
```

_onClose_ is just a function that takes no parameters and does not return anything, so the type is:
```
() => voidcopy
```

The type of _onSubmit_ is a bit more interesting, it has one parameter that has the type _PatientFormValues_. The return value of the function is _Promise <void>_. So again the function type is written with the arrow syntax:
```
(values: PatientFormValues) => Promise<void>copy
```

The return value of a _async_ function is a _Promise <void>_.
### Exercises 9.21-9.22
We will soon add a new type for our app, _Entry_ , which represents a lightweight patient journal entry. It consists of a journal text, i.e. a _description_ , a creation date, information regarding the specialist who created it and possible diagnosis codes. Diagnosis codes map to the ICD-10 codes returned from the _/api/diagnoses_ endpoint. Our naive implementation will be that a patient has an array of entries.
Before going into this, we need some preparatory work.
#### 9.21: Patientor, step1
Create an endpoint _/api/patients/:id_ to the backend that returns all of the patient information for one patient, including the array of patient entries that is still empty for all the patients. For the time being, expand the backend types as follows:
```
// eslint-disable-next-line @typescript-eslint/no-empty-object-type
export interface Entry {
}

export interface Patient {
  id: string;
  name: string;
  ssn: string;
  occupation: string;
  gender: Gender;
  dateOfBirth: string;
  entries: Entry[]}

export type NonSensitivePatient = Omit<Patient, 'ssn' | 'entries'>;copy
```

The response should look as follows:
![browser showing entries blank array when accessing patient](../assets/c0a881be7769576d.png)
#### 9.22: Patientor, step2
Create a page for showing a patient's full information in the frontend.
The user should be able to access a patient's information by clicking the patient's name.
Fetch the data from the endpoint created in the previous exercise.
You may use 
You might want to have a look at [part 7](../part7/01-react-router.md) if you don't yet have a grasp on how the 
The result could look like this:
![browser showing patientor with one patient](../assets/dd0c286a6c0a31e9.png)
The example uses 
### Full entries
In [exercise 9.10](../part9/01-typing-an-express-app-exercises-9-10-9-11.md) we implemented an endpoint for fetching information about various diagnoses, but we are still not using that endpoint at all. Since we now have a page for viewing a patient's information, it would be nice to expand our data a bit. Let's add an _Entry_ field to our patient data so that a patient's data contains their medical entries, including possible diagnoses.
Let's ditch our old patient seed data from the backend and start using 
Let us now create a proper _Entry_ type based on the data we have.
If we take a closer look at the data, we can see that the entries are quite different from one another. For example, let's take a look at the first two entries:
```
{
  id: 'd811e46d-70b3-4d90-b090-4535c7cf8fb1',
  date: '2015-01-02',
  type: 'Hospital',
  specialist: 'MD House',
  diagnosisCodes: ['S62.5'],
  description:
    "Healing time appr. 2 weeks. patient doesn't remember how he got the injury.",
  discharge: {
    date: '2015-01-16',
    criteria: 'Thumb has healed.',
  }
}
...
{
  id: 'fcd59fa6-c4b4-4fec-ac4d-df4fe1f85f62',
  date: '2019-08-05',
  type: 'OccupationalHealthcare',
  specialist: 'MD House',
  employerName: 'HyPD',
  diagnosisCodes: ['Z57.1', 'Z74.3', 'M51.2'],
  description:
    'Patient mistakenly found himself in a nuclear plant waste site without protection gear. Very minor radiation poisoning. ',
  sickLeave: {
    startDate: '2019-08-05',
    endDate: '2019-08-28'
  }
}copy
```

Immediately, we can see that while the first few fields are the same, the first entry has a _discharge_ field and the second entry has _employerName_ and _sickLeave_ fields. All the entries seem to have some fields in common, but some fields are entry-specific.
When looking at the _type_ , we can see that there are three kinds of entries:
  * _OccupationalHealthcare_
  * _Hospital_
  * _HealthCheck_


This indicates we need three separate types. Since they all have some fields in common, we might just want to create a base entry interface that we can extend with the different fields in each type.
When looking at the data, it seems that the fields _id_ , _description_ , _date_ and _specialist_ are something that can be found in each entry. On top of that, it seems that _diagnosisCodes_ is only found in one _OccupationalHealthcare_ and one _Hospital_ type entry. Since it is not always used, even in those types of entries, it is safe to assume that the field is optional. We could consider adding it to the _HealthCheck_ type as well since it might just not be used in these specific entries.
So our _BaseEntry_ from which each type could be extended would be the following:
```
interface BaseEntry {
  id: string;
  description: string;
  date: string;
  specialist: string;
  diagnosisCodes?: string[];
}copy
```

If we want to finetune it a bit further, since we already have a _Diagnosis_ type defined in the backend, we might just want to refer to the _code_ field of the _Diagnosis_ type directly in case its type ever changes. We can do that like so:
```
interface BaseEntry {
  id: string;
  description: string;
  date: string;
  specialist: string;
  diagnosisCodes?: Diagnosis['code'][];
}copy
```

As was mentioned [earlier in this part](../part9/01-the-alternative-array-syntax.md), we could define an array with the syntax _Array <Type>_ instead of defining it _Type[]_. In this particular case writing _Diagnosis['code'][]_ starts to look a bit strange so we will decide to use the alternative syntax (that is also recommended by the ESlint rule 
```
interface BaseEntry {
  id: string;
  description: string;
  date: string;
  specialist: string;
  diagnosisCodes?: Array<Diagnosis['code']>;}copy
```

Now that we have the _BaseEntry_ defined, we can start creating the extended entry types we will actually be using. Let's start by creating the _HealthCheckEntry_ type.
Entries of type _HealthCheck_ contain the field _HealthCheckRating_ , which is an integer from 0 to 3, zero meaning _Healthy_ and three meaning _CriticalRisk_. This is a perfect case for an enum definition. With these specifications, we could write a _HealthCheckEntry_ type definition like so:
```
export enum HealthCheckRating {
  "Healthy" = 0,
  "LowRisk" = 1,
  "HighRisk" = 2,
  "CriticalRisk" = 3
}

interface HealthCheckEntry extends BaseEntry {
  type: "HealthCheck";
  healthCheckRating: HealthCheckRating;
}copy
```

Now we only need to create the _OccupationalHealthcareEntry_ and _HospitalEntry_ types so we can combine them in a union and export them as an Entry type like this:
```
export type Entry =
  | HospitalEntry
  | OccupationalHealthcareEntry
  | HealthCheckEntry;copy
```

### Omit with unions
An important point concerning unions is that, when you use them with _Omit_ to exclude a property, it works in a possibly unexpected way. Suppose that we want to remove the _id_ from each _Entry_. We could think of using
```
Omit<Entry, 'id'>copy
```

but 
```
// Define special omit for unions
type UnionOmit<T, K extends string | number | symbol> = T extends unknown ? Omit<T, K> : never;
// Define Entry without the 'id' property
type EntryWithoutId = UnionOmit<Entry, 'id'>;copy
```

### Exercises 9.23-9.30
Now we are ready to put the finishing touches to the app!
#### 9.23: Patientor, step 3
Define the types _OccupationalHealthcareEntry_ and _HospitalEntry_ so that those conform with the new example data. Ensure that your backend returns the entries properly when you go to an individual patient's route:
![browser showing entries json data properly for patient](../assets/9aa2b5ffc6c6ba18.png)
Use types properly in the backend! For now, there is no need to do a proper validation for all the fields of the entries in the backend, it is enough e.g. to check that the field _type_ has a correct value.
#### 9.24: Patientor, step 4
Extend a patient's page in the frontend to list the _date_ , _description_ and _diagnoseCodes_ of the patient's entries.
You can use the same type definition for an _Entry_ in the frontend. For these exercises, it is enough to just copy/paste the definitions from the backend to the frontend.
Your solution could look like this:
![browser showing list of diagnosis codes for patient](../assets/25c9eb1ffa79cd4f.png)
#### 9.25: Patientor, step 5
Fetch and add diagnoses to the application state from the _/api/diagnoses_ endpoint. Use the new diagnosis data to show the descriptions for patient's diagnosis codes:
![browser showing list of codes and their descriptions for patient ](../assets/2ac03800a06d886c.png)
#### 9.26: Patientor, step 6
Extend the entry listing on the patient's page to include the Entry's details, with a new component that shows the rest of the information of the patient's entries, distinguishing different types from each other.
You could use eg. 
You should use a _switch case_ -based rendering and _exhaustive type checking_ so that no cases can be forgotten.
Like this:
![vscode showing error for healthCheckEntry not being assignable to type never](../assets/6c8f4828dda968a4.png)
The resulting entries in the listing _could_ look something like this:
![browser showing list of entries and their details in a nicer format](../assets/ff7b18e4a8f59b28.png)
#### 9.27: Patientor, step 7
We have established that patients can have different kinds of entries. We don't yet have any way of adding entries to patients in our app, so, at the moment, it is pretty useless as an electronic medical record.
Your next task is to add endpoint _/api/patients/:id/entries_ to your backend, through which you can POST an entry for a patient.
Remember that we have different kinds of entries in our app, so our backend should support all those types and check that at least all required fields are given for each type.
In this exercise, you quite likely need to remember [this trick](../part9/01-grande-finale-patientor-omit-with-unions.md).
You may assume that the diagnostic codes are sent in the correct form and use eg. the following kind of parser to extract those from the request body:
```
const parseDiagnosisCodes = (object: unknown): Array<Diagnosis['code']> =>  {
  if (!object || typeof object !== 'object' || !('diagnosisCodes' in object)) {
    // we will just trust the data to be in correct form
    return [] as Array<Diagnosis['code']>;
  }

  return object.diagnosisCodes as Array<Diagnosis['code']>;
};copy
```

#### 9.28: Patientor, step 8
Now that our backend supports adding entries, we want to add the corresponding functionality to the frontend. In this exercise, you should add a form for adding an entry to a patient. An intuitive place for accessing the form would be on a patient's page.
In this exercise, it is enough to **support one entry type**. All the fields in the form can be just plain text inputs, so it is up to the user to enter valid values.
Upon a successful submission the new entry should be added to the correct patient and the patient's entries on the patient page should be updated to contain the new entry.
Your form might look something like this:
![Patientor new healthcheck entry form](../assets/8b306a6a68460775.png)
If a user enters invalid values to the form and backend rejects the addition, show a proper error message to the user
![browser showing healthCheckRating incorrect 15 error](../assets/34c55cc1ac961eee.png)
#### 9.29: Patientor, step 9
Extend your solution so that it supports _all the entry types_
#### 9.30: Patientor, step 10
Improve the entry creation forms so that it makes it hard to enter incorrect dates, diagnosis codes and health rating.
Your improved form might look something like this:
![patientor showing fancy calendar ui](../assets/406e6173ef6e3f70.png)
Diagnosis codes are now set with Material UI 
### Submitting exercises and getting the credits
Exercises of this part are submitted via 
Once you have completed the exercises and want to get the credits, let us know through the exercise submission system that you have completed the course:
![Submissions](../assets/770a7d941952a2f6.png)
**Note** that you need a registration to the corresponding course part to get the credits registered, see [here](../part0/01-general-info-parts-and-completion.md) for more information.
You can download the certificate for completing this part by clicking one of the flag icons. The flag icon corresponds to the certificate's language.
[ Part 9d **Previous part** ](../part9/01-react-with-types.md)[ Part 10 **Next part** ](../part10/01-part10.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)