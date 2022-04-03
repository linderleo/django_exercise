# django_exercise

1) create virtual python environment
python3 -m venv /Users/<home>/.local/lib/venv/django_env

2) activate the environment
source /Users/<home>/.local/lib/venv/django_env/bin/activate

3) go to home directory and pull application from GitHub
cd ~; git clone git@github.com:linderleo/django_exercise.git;

4) go to the directory and install requirements
cd django_exercise; pip install -r requirements.txt

5) go to project folder and migrate database
cd my_django_project; python3 manage.py migrate;

6) create superuseraccount
python3 manage.py createsuperuser
  - give username and password, email can be left empty

7) start the app
python3 manage.py runserver

8) open a web browser and go to -> http://localhost:8000/admin, login with the superuser account credentials

9) Add user (or many) from the site administration page, press '+ Add' next to 'Users'
   - add username and password

10) from the same site administration page, add token for the newly created users, press '+ Add' next to 'Tokens'
    - select the user and click save

11) you are now able to make crud (create, read, update, delete) operations (for GitHub projects and webhooks) in the app with the newly created user(s)
  - remember to use the correct token for a specific user, otherwise it will give permission denied
    - urls: 
      - http://127.0.0.1:8000/github_projects/ 
        (query string parameters ?sort_by=<rating|created>&order=<asc|desc> can be used too)
      - http://127.0.0.1:8000/github_projects/<id> 
      - http://127.0.0.1:8000/api/webhooks/
      - http://127.0.0.1:8000/api/webhooks/<id>

12) you may test the rest api usage from visual studio code with the users and tokens created
  - files under django_exercise/my_django_project/project_collection_app/requests
  - example (/requests/get_all_projects.rest):
    - paste your created token in the file (Authorization: token <paste_token_here>) and press 'send request'
  - for testing webhooks, you may get your specific url test link from https://webhook.site/