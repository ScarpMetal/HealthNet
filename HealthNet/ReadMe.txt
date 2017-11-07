***********************************************************************************************
did it work?
Program Installation
The target platforms for this installation are python3.5 and Django 1.9
All necessary installations can be performed through the windows command prompt.

The following steps are necessary to succesfully run the HEALTHnet program

Python and Django must be installed before completing the following....
1.)	Unzip files and save to desired location.
2.)	From windows command prompt “cd path/to/HealthNet/repository”
3.)	From windows command prompt execute “python manage.py makemigrations HNApp”
4.)	From windows command prompt execute “python manage.py migrate HNApp”
5.)	From windows command prompt  execute “python manage.py runserver”
6.)	Open web browser and enter http://127.0.0.1:8000/

This will bring the user to the login/create user page. 
If the login page is not displayed please contact your program administrator. 

***********************************************************************************************

Know Bugs and disclaimers...

>>>When logged in as a Doctor you will be auotomatically looged out if you try and access the 
   profile tab.
>>>Program crash if nurse loggin is atempted
>>>Appointments can be created to close together but not exact.

************************************************************************************************

Features not included in Beta release

>>>Prescriptions must be added through the admin superuser.
   (See: create superuser at bottom of ReadMe file.)
>>>Appoinment callender view.
>>>Apointments created in 30 minute blocks.
>>>Statistics and activity logs
>>>Impliment Nurses page


************************************************************************************************

Basic Execution and usage
At the create user page user will be prompted to fill in a number of basic 
information fields.
All fields are required and must be filled in for successful registration.
The User must enter a unique username and password. 
The password must be at least 8 characters and cannot be common in nature. 
System will prompt user for alternate password if it does not meet requirements.  
The system will also prompt user for alternate username if chosen user name already exists. 
The registrant is also prompted to enter his/her date of birth and must follow the format
YYYY-MM-DD if the registrant does not comply, the system will prompt for a valid date. 
The registrant’s doctor must also be selected in order to register.
The registrants phone number must be entered with no dashes.

*************************************************************************************************

Create Superuser
1.)	Open windows command prompt
2.)	Enter “python manage.py createsuperuser”
3.)	Enter required information(username,email,password)
4.)	Open the web browser and enter http://127.0.0.1:8000/admin

This process allows administration personnel to create and admin account
so that accounts of any kind may be created or deleted. 

