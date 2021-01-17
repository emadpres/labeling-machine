# Labeling Machine (lm) Platform

## Setting-Up Project for Development

### Requirements
- __Python 3.x__: Double check your python version
    ```
    # Check your Python version
    $ python --version
    Python 3.x
    
    $ pip --version
    xxxxx (python 3.x)
    ```

### Create `venv`
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
   
### Run Project in _PyCharm_
1. Open the project in PyCharm
2. Configure the Python Interpreter: `Preference` > `Project interpreter` > `[Show All]` > `+` > path to `[Project]/venv/bin/python`
3. Create run configurations:
    1. `flask-run`: for running webapp server
        - Run > Edit Configurations > + > python:
        - Name: _flask-run_
        - Allow parallel run: _unchecked_
        - Script Path: _<absolute_path_to_project>/<venv>/bin/flask_
        - Parameters: _run_
        - Environment variables: _FLASK_APP=src; FLASK_ENV=development;_
        - Python Interpreter: Project default
        - Working Directory: _<absolute_path_to_project>/lmwebapp/_
    2. `flask-initdb`: for database initialization for the first time
        - Run > Edit Configurations > select newly created `flask-run` > Copy Configuration (Cmd+D)
        - Name: _flask-initdb_
        - Parameters: _initdb_
4. Initialize the database (needed only first time): run `flask-initdb`
   - Delete the existing database (`/db/app.sqlite`) for a fresh start
5. Running WebApp: run `flask-run`

### Run Project from Terminal
```shell
$ source [Project]/venv/bin/activate
(venv)$ cd [Project]/webapp/

# define path to our `app` variable
(venv)$ export FLASK_APP=src;
# enables auto code reloading on code changes, and provides helpful debugging info
(venv)$ export FLASK_ENV=development

(venv)$ flask initdb  # initialize the database for the first time
(venv)$ flask run     # run the WebApp
```

   
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

<details>
<summary>Deployment Troubleshooting</summary>

1. Why I still see the old database, although I updated db in the new image?
   - If Docker Volume for older container exist, the volume doesn't get replaced with new images. Otherwise, we couldn't update our image without losing our existing data.
   - **Solution**:
     1. Find "Volume Name": `docker inspect container_name` and look for `Mounts > Name` field.
     2. Delete the volume: `docker volume rm volume_name`
        - If it errors that volume is in use, try to stop container: `docker stop container_name` 
        - Note: if you created the volume using `docker-compose` in the first place you have to remove the container:
          1. `docker rm -v container_name` (`-v`: remove volume as well) 
          2. `docker volume rm volume_name`  

2. How can I copy database from the running container?
   - `docker cp container_name:/app/LabelingMachine/db/app.sqlite ~/local/path`

3. How can I update the python code on the fly?
    - `docker exec -it container_name /bin/bash`
    - Do your changes
    - `exit`
    - **Note**: Such changes are not persistent, so it's better you update source-code and build a new image.
</details>