# Schoolsaurus
Schoolsaurus is an app to help students to find schools easier<br>
This is a group project for CZ3002 in NTU

## Project Description
- The project language is python, and HTML for the frontend
- This project is implemented by using django http://djangoproject.com/ and Bootstrap Themes
https://www.creative-tim.com/
- This project is deployed automatically for every passed test commit to heroku. You can see this project live at http://schoolsaurus.herokuapp.com/

The project source code can be found on src/ folder
The project deliverables can be found on deliverables/ folder

## How to start
1. You need to finish the django tutorial https://www.djangoproject.com/
2. Download python and install a virtualenv for this project `virtualenv venv` using pip install
3. Use the virtualenv `source venv/bin/activate` for LINUX/MAC, for WINDOWS use `venv/Scripts/activate`
4. install the requirements: `pip install -r requirements.txt`
5. Go to src/ folder and do initial migration by using `python manage.py migrate`
6. create superuser using `python manage.py createsuperuser`, ensure that the username is in email format.
7. Start the server using `python manage.py runserver`
8. Login using superuser account to access admin page.
9. Go to Schedulers tab and click MANUALLY REFRESH API and wait for a few minutes to load the school general and CCA data into the    database.
10. Go to School tab and it will display a list of school if step 9 is completed.
11. After loading the school data, use console to run importdata file using `python importdata.py` to link school logo, location and PSLE score to the school.
12. Re-start the server(step 7) and check that school logos are showing in schools tab. 

## How to test
1. Use the virtualenv `source venv/bin/activate` for LINUX/MAC, for WINDOWS use `venv/Scripts/activate`
2. install the requirements: `pip install -r requirements.txt`
3. Go to src/ folder
4. to run functional test: python functional_tests.py
5. to run unit test: python manage.py test
