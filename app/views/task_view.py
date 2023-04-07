from xml.sax.handler import feature_namespace_prefixes
from flask import render_template, g, Blueprint, redirect, render_template, request, make_response
from api.task_api import Task, TaskDB
from models.artwork_db_modifier import timestamp
from models.ArtCollection_db_modifier import description
from models.artwork_db_modifier import img_url
from models.artwork_db_modifier import collection_name

from models.ArtCollection_db_modifier import ArtCollectionDB, ArtCollection
from models.user_db_modifier import UserDB, User
from models.artwork_db_modifier import artworkDB, ArtWork
import datetime


task_list_blueprint = Blueprint('task_list_blueprint', __name__)


# Home Page
@task_list_blueprint.route("/")
def index():
    return render_template("index.html")


# Register page
@task_list_blueprint.route("/register")
def register():
    return render_template("register.html")


# Action to properly register a user
@task_list_blueprint.route("/registration", methods = ["POST"])
def register_user():
    user_db = UserDB(g.mysql_db, g.mysql_cursor)
    user = User(request.form.get("uname"), request.form.get("passwd"))
    users_username = request.form.get("uname")
    users_password = request.form.get("passwd")
    if user_db.validate_user(users_username, users_password):
        return redirect("/taken-uname")
    else:
        user_db.add_user(user)
        return render_template("register-success.html")


# if the username is taken
@task_list_blueprint.route("/taken-uname")
def taken_uname():
    return render_template("taken-uname.html")


# route to our main gallery/ timeline page
@task_list_blueprint.route("/gallery", methods=["GET", "POST"])
def gallery():
    artcollection_db = ArtCollectionDB(g.mysql_db, g.mysql_cursor)
    art_collection = request.form.get("collection")
    artcollection_db.get_collection(art_collection)
    return render_template("gallery.html")


# login page
@task_list_blueprint.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


# check to see if a proper username and password have been
# entered correclty and are in our database
@task_list_blueprint.route("/login-check", methods=["POST"])
def login_check():
    user_db = UserDB(g.mysql_db, g.mysql_cursor)
    users_username = request.form.get("uname")
    users_password = request.form.get("passwd")

    if user_db.validate_user(users_username, users_password):
        resp = make_response(redirect("/gallery"))
        resp.set_cookie('userID', users_username)
        return resp
    else:
        return redirect("/login")

    
# login-error page
@task_list_blueprint.route("/login-error")
def login_fail():
    return render_template("login-error.html")  


# upload art page
@task_list_blueprint.route("/upload", methods=["GET"])
def submission():
    return render_template("upload.html")


# action of uploading art into our database
@task_list_blueprint.route("/upload-art", methods=["POST"])
def upload_art():
    # obtaining the time to put into the uploaded artwork
    curr_time = datetime.datetime.now()

    # connecting to both user and artwork DB
    user_db = UserDB(g.mysql_db, g.mysql_cursor)
    artwork_db = artworkDB(g.mysql_db, g.mysql_cursor)
    artcollection_db = ArtCollectionDB(g.mysql_db, g.mysql_cursor)

    # Get the User id to create an artwork associated to it 
    curr_username = request.cookies.get('userID')
    curr_id = user_db.get_usernames_id(curr_username)

    # creation of the artwork object
    uploaded_artwork = ArtWork(curr_id['id'], request.form.get("url"), request.form.get("description"), curr_time, request.form.get("artstyle"), request.form.get("collection"))
    artwork_id = artwork_db.add_artwork(uploaded_artwork)
    new_collection = ArtCollection(request.form.get("collection"), request.form.get("description"))
    artcollection_db.add_art_collection(artwork_id['id'], new_collection)

    return redirect("/gallery")


# profile page
@task_list_blueprint.route("/profile", methods=["GET"])
def profile():
    user_db = UserDB(g.mysql_db, g.mysql_cursor)
    prof_name = request.cookies.get('userID')
    user_id = user_db.get_usernames_id(prof_name)
    firstname = request.cookies.get('firstname')
    lastname = request.cookies.get('lastname')
    email = request.cookies.get('email')
    description = request.cookies.get('description')
    if (user_id['first_name'] != firstname and user_id['last_name'] != lastname and user_id['email'] != email and user_id['description'] != description):
        return render_template("profile.html", prof_name=prof_name)
    if (user_id['username'] == prof_name):
        return render_template("profile.html", prof_name=prof_name, firstname=firstname, lastname=lastname, email=email, description=description)


# logout page
@task_list_blueprint.route("/logout")
def logout():
    return render_template("logout.html")


# if a user forgets their passowrd they get rick rolled
@task_list_blueprint.route("/rickroll")
def rickroll():
    return render_template("rick.html")


# manage profile page
@task_list_blueprint.route("/manage-profile", methods=["POST"])
def manage_profile():
    return render_template("manage-profile.html")

# Collection Page
@task_list_blueprint.route("/Collection", methods=["GET"])
def Collection():
    artwork_db = artworkDB(g.mysql_db, g.mysql_cursor)
    searched_collection = request.args.get("search")
    art_style = request.args.get("artstyle")
    art_work = artwork_db.get_artwork(art_style, searched_collection)
    art_work_img = art_work['img_url']
    art_work_desc = art_work['description']

    resp = make_response(render_template("Collection.html", name=searched_collection, style=art_style, image=art_work_img, description=art_work_desc))

    resp.set_cookie('artstyle', art_style)
    resp.set_cookie('searched_collection', searched_collection)
   
    return resp

# profile modification action
@task_list_blueprint.route("/profile-mod", methods=["POST"])
def profile_mod():
    user_db = UserDB(g.mysql_db, g.mysql_cursor)
    user_name = request.cookies.get('userID')
    user_id = user_db.get_usernames_id(user_name)

    resp = make_response(redirect("/profile"))

    firstname = request.form.get("fname")
    lastname = request.form.get("lname")
    email = request.form.get("email")
    description = request.form.get("description")

    resp.set_cookie('firstname', firstname)
    resp.set_cookie('lastname', lastname)
    resp.set_cookie('email', email)
    resp.set_cookie('description', description)

    user_db.update_first_name(user_id['id'], firstname)
    user_db.update_last_name(user_id['id'], lastname)
    user_db.update_email(user_id['id'], email)
    user_db.update_description(user_id['id'], description)
    
    return resp


# delete account page
@task_list_blueprint.route("/delete-account", methods=["GET"])
def delete_account():
    return render_template("/delete-account.html")


# Action of deleting a user
@task_list_blueprint.route("/deleted", methods=["POST"])
def deleted_account():
    user_db = UserDB(g.mysql_db, g.mysql_cursor)
    user_name = request.cookies.get('userID')
    user_id = user_db.get_usernames_id(user_name)
    user_db.delete_user(user_id['id'])
    return redirect("/")


@task_list_blueprint.route("/manage-collection", methods=["POST"])
def manage_collection():
    return render_template("/manage-collection.html")


@task_list_blueprint.route("/delete-collection", methods=["POST"])
def delete_collection():
    return render_template("/delete-collection.html")


@task_list_blueprint.route("/deleted-art", methods=["POST"])
def deleted_art():
    artcollection_db = ArtCollectionDB(g.mysql_db, g.mysql_cursor)
    artwork_db = artworkDB(g.mysql_db, g.mysql_cursor)
    searched_collection = request.cookies.get('searched_collection')
    art_style = request.cookies.get('artstyle')
    art_work = artwork_db.get_artwork(art_style, searched_collection)
    art_collection = artcollection_db.get_collection(searched_collection)
    artcollection_db.delete_artwork(art_collection['id'])
    artwork_db.delete_artwork(art_work['id'])

    return redirect("/gallery")
