#### 1. Create an environment
Create a venv folder in the project root folder:
```
$ python3 -m venv venv
```
#### 2.Activate the environment
Before you work on your project, activate the corresponding environment:
```
$ venv/bin/activate
```

#### 3. Install dependencies
Within the activated environment, use the following command to install dependencies:
```
$ pip install -r requirements.txt
```

#### 4. Run the application
To run the application, use the flask command:
```
flask --app flaskr run
```