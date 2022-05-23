# Python Flask Web API

## Api requests

### /get/<int: id>

Go to search bar and type note id only admin can see all notes in database

### /getall

Get all the notes

### /put/<int: id>

Update single note, admin can update any note

### /create

Create new note

### /delete/<int: id>

Delete a note, admin can delete any note

### /login

login admin and user

### /sign-up

sign-up for user

### /sign-up?admin=True

sign-up for admin

## How to use app

### authentication

Go to /login for existing user, /sign-up for registering a new user and /sign-up?admin=True for admin user.

### default user

Email: default@gmail.com
password: default@gmail.com

### default admin user

Email: defaultadmin@gmail.com
password: defaultadmin@gmail.com

#### creating a note

Go to /create and create a note

#### deleting a note

Go to /delete/<int: id>


#### updating a note

Go to /update/<int:id>


#### Reading a note

Go to /get/<int:id>

#### Reading all note

Go to /getall

