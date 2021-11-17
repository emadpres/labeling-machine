# Labeling Machine (lm) Platform


**Labeling Machine** is a web application written in Python that is intended to be used by researchers for _labeling data_ with minimum effort. Here are some of its key features:  
+ **Very lightweight**: The tool is based on [Flask](https://flask.palletsprojects.com)
+ **Ready to go and Dockerized**: Just follow [Deployment](#deployment-with-docker) section to see a demo of the tool in 15 minutes
+ **Easy to customize**: Follow [Customizing the Project](#customizing-the-project) steps to quickly adopt teh tool for your project


### Backstory
Labeling Machine was originally implemented back in 2019 to be internally used for our empirical [research study](https://dl.acm.org/doi/10.1109/ICSE.2019.00122) which involved labeling data from StackOverflow, Apache Mailing Lists, and GitHub issues and PRs. Later is went through several iterations and been used in more studies.  As the tool became more mature and proven to be a practically useful tool, I decided to make it available to all researchers as an open-source tool.  
   


## Setting-Up Project for Development

### 1. Requirements
Make sure _Python 3.x_ is installed
```
# Check your Python version
$ python --version
Python 3.x

$ pip --version
xxxxx (python 3.x)
```

### 2. Create `venv`
```shell
$ cd [Project]
$ python3 -m venv ./venv
$ source ./venv/bin/activate

# install dependencies
(venv)$ pip3 install -r requirements.txt
# verify flask in installed
(venv)$ flask --version

(venv)$ deactivate
$
```
   
### 3.a Run Project in _PyCharm_
1. Open the project in PyCharm
2. Configure the Python Interpreter: `Preference` > `Project interpreter` > `[Show All]` > `+` > path to `[Project]/venv/bin/python`
3. Create run configurations:
    1. `flask-run`: for running webapp server
        - Run > Edit Configurations > + > python:
        - Name: _flask-run_
        - Allow parallel run: _unchecked_
        - Script Path: _<absolute_path_to_project>/<venv>/bin/flask_
        - Parameters: _run_
        - Environment variables: `FLASK_APP=src; FLASK_ENV=development;`
        - Python Interpreter: Project default
        - Working Directory: _<absolute_path_to_project>/webapp/_
    2. `flask-initdb`: for database initialization for the first time
        - Run > Edit Configurations > select newly created `flask-run` > Copy Configuration
        - Name: _flask-initdb_
        - Parameters: _initdb_ 
          - Note that the `initdb` name for parameter comes from `@app.cli.command('initdb')`

**Note:** If you want to make the server visible to externals (i.e., accepting connection from all network adapters): `(venv)$ flask run --host=0.0.0.0`

Now we are ready to run the project:
1. (**only first time**) Initialize the database by running `flask-initdb` configuration
   - This will run the method associated with `@app.cli.command('initdb')`
   - Delete the existing database (`/db/app.sqlite`) for a fresh start
2. Run the WebApp by runing `flask-run` confguration
   - The webapp will be running on http://127.0.0.1:5000 by default

#### PyCharm Troubleshooting
**Q1.** Why does PyCharm shows red lines all over the source code?
- You should mark `[Project]/webapp/` folder as the root of source code: _right-click on the folder > Mark Directory as > Sources Root_ 

### 3.b Run Project in Terminal
```shell
$ source [Project]/venv/bin/activate
(venv)$ cd [Project]/webapp/

# define path to our `app` variable
(venv)$ export FLASK_APP=src;
# enables auto code reloading on code changes, and provides helpful debugging info
(venv)$ export FLASK_ENV=development

(venv)$ flask initdb  # initialize the database for the first time
(venv)$ flask run     # run the WebApp
# The webapp will be running on http://127.0.0.1:5000 by default
```

If you want to make the server visible to externals (i.e., accepting connection from all network adapters): `(venv)$ flask run --host=0.0.0.0`

## Customizing the Project
Please follow steps below for customizing the project to your needs. For all steps I already implemented a sample showcase. If something is not clear, make sure to open an [issue](https://github.com/emadpres/labeling-machine/issues).
1. **Importing your artifacts to be labeled**:
    1. Update database scheme to store artifacts to be labeled on `Artifact` table. For that, simply update `Artifact` class in `models.py`.
    2. Update `initdb.py > import_my_data()` method to import your artifact data.
    3. Run `initdb` configuration to perform the initialization (see _Run Project_ sections above to learn more)
2. **Displaying artifacts to labelers**:
    1. Update `routes_labeling.py > labeling_with_artifact(target_artifact_id)` method to send the content required to be displayed (i.e., the artifact content)
    2. Update `artifact.html` to display the artifact in the way you like (_NOTE:_ HTML files are written in _Jinja_ web template language. Don't afraid. With Jinja syntax you technically have access to Python objects you sent in the previous step)
3. **Update the logic to collect labeled data**:
    1. Design your own input form in `labeling_layout.html` to collect labeling data. (_NOTE:_ For the showcase, I already implemented a simple pull-down menu that users can either (1) create a new label and select it, or (2) select a label among previously created labels (by any user).
    2. Update database schema to store submitted data on `LabelingData` table. For that, simply update `LabelingData` class in `models.py`.   
    3. Store submitted labels on the database by updating `routes_labeling.py > label()` method.

**Database Technology**: By default, the tool uses _SQLite_ as the database technology. However, since _Labeling Machine_ relies on [SQLAlchemy](www.sqlalchemy.org), an ORM toolkit, you can use any other DB technology (MYSQL, PostgreSQL, etc.) with change of a couple of lines [here](webapp/src/__init__.py).

## Deployment (with _Docker_)

### I. Using `docker-compose`
```shell
$ cd [Project]/docker
# Build image
$ docker-compose build
# Start a container (http://localhost:45000)
$ docker-compose up -d lm
# Stop the container
$ docker-compose down
```

### II. Manually
```shell
$ cd [Project]/docker # the directory of Dockerfile
$ docker build -t lm-minimal:latest --file ./Dockerfile ..
# Start a container (http://localhost:45000)
$ docker run --name lm-minimal -p 45000:5000 -d lm-minimal:latest
# Stop the container
$ docker stop lm-minimal
$ docker rm lm-minimal
```

<details open>
<summary>Docker Troubleshooting</summary>

**Q1.** Why do I still see the old database, although I updated db in the new image?
- If Docker Volume for older container exist, the volume doesn't get replaced with new images. Otherwise, we couldn't update our image without losing our existing data.
- **Solution**:
  1. Find the volume's name: `docker inspect <container_name>` and look for `Mounts > Name` field.
  2. Delete the volume: `docker volume rm <volume_name>`
     - If it errors that volume is in use, try to stop container: `docker stop <container_name>` 
     - Note: if you created the volume using `docker-compose` in the first place you have to remove the container:
       1. `docker rm -v <container_name>` (`-v`: remove volume as well) 
       2. `docker volume rm <volume_name>`  

**Q2.** How can I copy database from the running container?
- `docker cp <container_name>:/labeling-machine/webapp/db/app.sqlite ~/local/path`

**Q3.** How can I update the python code on the fly?
1. `docker exec -it <container_name> /bin/bash`
2. Do your changes
3.`exit`
3. **Note**: Such changes are not persistent, so it's better you update source-code and build a new image.
</details>
