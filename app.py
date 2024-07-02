from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# Create the object of the Flask class
app = Flask(__name__)

# Connecting the flask app with SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'

# Creating an object of SQLAlchemy class
database = SQLAlchemy(app)

# Writing python class to insert data into table
class Task(database.Model):
    sno = database.Column(database.Integer, primary_key=True)
    taskTitle = database.Column(database.String(100), nullable=False)
    taskDescription = database.Column(database.String(200), nullable=False)

# First route: Index route/default route
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Fetch the values of title and description
        task_title = request.form.get('title')
        task_description = request.form.get('description')

        # Add it to the database
        task = Task(taskTitle=task_title, taskDescription=task_description)
        database.session.add(task)
        database.session.commit()

        # Returning the index.html page
        return redirect('/')

    else:
        # Fetching all tasks from the database
        allTask = Task.query.all()
        return render_template('index.html', allTask=allTask)

# Second route: Contact us
@app.route('/contact')
def contact():
    # Returning the response
    return render_template('contact.html')

# Third route: About us
@app.route('/about')
def about():
    # Returning the response
    return render_template('about.html')

# Fourth route: Delete a task from database 
@app.route("/delete")
def delete():
    # Extracting the sno
    serial_number = request.args.get('sno')

    # Fetching task with sno=serial_number
    task = Task.query.filter_by(sno=serial_number).first()
    
    # Deleting the task
    database.session.delete(task)
    database.session.commit()

    # Reassign serial numbers
    all_tasks = Task.query.order_by(Task.sno).all()
    for index, task in enumerate(all_tasks, start=1):
        task.sno = index
    database.session.commit()

    # Redirect to index page
    return redirect('/')

# Fifth route: Update a task from database
@app.route("/update", methods=["GET", "POST"])
def update():
    # Getting the sno for update
    serial_number = request.args.get('sno')

    # Fetching the task from database to update the task
    reqTask = Task.query.filter_by(sno=serial_number).first()

    if request.method == "POST":
        # Fetching the updated values
        updatedTitle = request.form.get('title')
        updatedDescription = request.form.get('description')

        # Changing the value of the existing task
        reqTask.taskTitle = updatedTitle
        reqTask.taskDescription = updatedDescription

        # Committing the update in database
        database.session.add(reqTask)
        database.session.commit()

        # Redirecting to index.html page
        return redirect('/')
    else:
        # Rendering the update.html page
        return render_template('update.html', reqTask=reqTask)

# Running the Flask application
if __name__ == "__main__":
    app.run(debug=True)
