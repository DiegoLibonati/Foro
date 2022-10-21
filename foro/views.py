from unicodedata import category, name
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_required, current_user
from .models import User, Post, Post_Category, Comment, Comment_Like, Subs
from . import db
from werkzeug.security import check_password_hash, generate_password_hash
import json
import os
from datetime import datetime
from .functions import save_images, check_files_on_update, get_time_login

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    users_array = []
    users_on = []

    if request.method == "POST":
        pass

    if request.method == 'GET':
        users_db = User.query.limit(10).all()
        users_db_ons = User.query.all()
        categorys = Post_Category.query.all()
        
        time_now = datetime.utcnow()

        for user in users_db_ons:
            time_afk = time_now - user.is_active
            time_afk = str(time_afk)
            values_time = time_afk.split(":")
            minutes = int(values_time[1])
            if minutes < 5:
                users_on.append(user)
        
        for user in users_db:
            user_json = {"img": user.profile_photo,
            "nick": user.username,
            "id": user.id,}
            users_array.append(user_json)

        return render_template("index.html", user=current_user, users = users_db, usersjson = users_array, users_on = users_on, categorys = categorys)


@views.route('/profile/<user>', methods= ['GET', 'POST'])
@login_required
def profile(user):
    user_db = User.query.filter_by(username=user).first()
    profile_comments_db = db.session.query(User,Comment).join(Comment).filter_by(profile_id = user_db.id)
    subs_db = db.session.query(User,Subs).join(Subs).filter_by(profile_id = user_db.id).all()
    subs_profile = Subs.query.filter_by(profile_id = user_db.id).all()

    print(current_user.subs)

    if request.method == 'POST':

        content = request.form.get('comment')

        new_comment = Comment(content = content,user_id = current_user.id, profile_id = user_db.id)
        db.session.add(new_comment)
        db.session.commit()

        if user_db and user == current_user.username:
            return redirect(url_for('views.profile', user = current_user.username))
        else:
            return redirect(url_for('views.profile', user = user_db.username))

    if request.method == 'GET':

        if user_db and user == current_user.username:
            return render_template('profile.html', user=current_user, comments = profile_comments_db, subs = subs_db, subs_profile = subs_profile)
        elif user_db and user == user_db.username:
            return render_template('profile.html', user=user_db, comments = profile_comments_db, subs = subs_db, subs_profile = subs_profile)
        else:
            return render_template("<h2>User Not Found</h2>")

@views.route('/profile/edit/<username>', methods = ['GET', 'POST'])
@login_required
def profile_update(username):
    
    user_db = User.query.filter_by(username=username).first()
    profile_comments_db = db.session.query(User,Comment).join(Comment).filter_by(profile_id = user_db.id)

    # El update se va a cargar solo si el usuario que se pasa por url es igual al usuario logeado.
    if username == current_user.username:

        if request.method == "POST":
            # Obtenemos todos los datos del form.
            username = request.form.get('username')
            email = request.form.get('email')
            profile_photo = request.files.get('profile_photo')
            remove_profile_photo = request.form.get('removeprofilephoto')
            profile_banner = request.files.get('profile_banner')
            remove_profile_banner = request.form.get('removeprofilebanner')
            profile_background = request.files.get('profile_background')
            remove_profile_background = request.form.get('removeprofilebackground')
            password = request.form.get('password')

            # Obtenemos si el username existe en la base de datos al igual que el mail.
            user_db = User.query.filter_by(username=username).first()
            email_db = User.query.filter_by(email=email).first()


            # Chequea si todos los datos del update al dar update son iguales, es decir, si no fueron editados.
            if (user_db and user_db.username == username) and user_db.email == email and not profile_photo and not remove_profile_photo == "on" and not profile_banner and not remove_profile_banner == "on" and not profile_background and not remove_profile_background == "on":
                flash("You cant edit with the same information.", category="error")
                return redirect(url_for('views.profile', user = current_user.username))
            else:
                # Si no existe dicho usuario.
                if not user_db or user_db.username == current_user.username:
                    # Si no existe dicho email.
                    if not email_db or email_db.email == current_user.email:
                        # Si la contraseña pasada es igual a la contraseña encriptada en la base de datos
                        if check_password_hash(current_user.password, password):

                            current_user.username = username
                            current_user.email = email
                            current_profile_photo_user = current_user.profile_photo 
                            current_profile_banner_user = current_user.profile_banner 
                            current_profile_background_user = current_user.profile_background 
                            
                            print(current_profile_background_user)

                            current_user.profile_photo = check_files_on_update(current_profile_photo_user, profile_photo, current_app, remove_profile_photo, "profilephotos", "default.webp")
                            current_user.profile_banner = check_files_on_update(current_profile_banner_user, profile_banner, current_app, remove_profile_banner, "profilebanners", "default.jpg") 
                            current_user.profile_background = check_files_on_update(current_profile_background_user, profile_background, current_app, remove_profile_background, "profilebackgrounds", None) 


                            db.session.commit()
                            return redirect(url_for('views.profile', user = current_user.username))   
                        else:
                            flash("The changes could not be applied because the password is invalid.", category="error")
                            return redirect(url_for('views.profile', user = current_user.username))
                    else:
                        flash("The changes could not be applied because the email already exists.", category="error")
                        return redirect(url_for('views.profile', user = current_user.username))
                else:
                    flash("The changes could not be applied because the user already exists.", category="error")
                    return redirect(url_for('views.profile', user = current_user.username))

                         

        return render_template('update.html', user=current_user, comments = profile_comments_db)
    else:
        return "<h2>User Not Found</h2>"


@views.route("/<user>/<comment_id>/like", methods=['GET'])
@login_required
def like(user, comment_id):
    comment = Comment.query.filter_by(id = comment_id).first()
    user_db = User.query.filter_by(id=comment.profile_id).first()
    like = Comment_Like.query.filter_by(user_id = current_user.id, comment_id = comment_id).first()

    if not comment:
        flash('Comment does not exist.', category="error")
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Comment_Like(user_id = current_user.id, comment_id = comment_id)
        db.session.add(like)
        db.session.commit()

    if user_db:
        return redirect(url_for('views.profile', user = user_db.username))

@views.route("<user>/<comment_id>/delete")
@login_required
def delete_comment(user ,comment_id):
    comment = Comment.query.filter_by(id = comment_id).first()


    if not comment:
        flash('Comment does not exist.', category="error")
    else:
        user_db = User.query.filter_by(id=comment.profile_id).first()

        db.session.delete(comment)
        db.session.commit()

        if user_db:
            return redirect(url_for('views.profile', user = user_db.username))

    return redirect(url_for('views.profile', user = user))


@views.before_request
@login_required
def update_user_is_active():
    current_user.is_active = datetime.utcnow()
    current_user.last_connection = get_time_login()
    db.session.commit()

@views.route('/posts/<category_id>', methods = ['GET'])
@login_required
def posts(category_id):

    posts_db = db.session.query(User,Post).join(Post).filter_by(category_id = category_id).all()
    category = Post_Category.query.filter_by(id = category_id).first()

    return render_template('posts.html', user=current_user, posts = posts_db, category = category)

@views.route('/posts/<category_id>/create-post', methods=['GET', 'POST'])
@login_required
def create_post(category_id):
    category = Post_Category.query.filter_by(id = category_id).first()

    if request.method == "POST":
        post_title = request.form.get('title_post').strip()
        post_content = request.form.get('content_post').strip()
        post_user_id = current_user.id
        post_category_id = category_id
        
        if post_title and post_content and post_user_id and post_category_id:
            new_post = Post(title=post_title, content=post_content, user_id = post_user_id, category_id = post_category_id)
            db.session.add(new_post)
            db.session.commit()
            flash("Post created.", category="success")
            return redirect(url_for('views.posts', category_id = category_id))
        else:
            flash("You failed to create the post.", category="error")
            return redirect(url_for('views.posts', category_id = category_id))

    if request.method == "GET":
        return render_template('post_create.html', user=current_user, category = category)

@views.route('/posts/<category_id>/<title>', methods = ['GET', 'POST'])
@login_required
def post(category_id, title):

    post_db = Post.query.filter_by(title = title).first()
    user_db = User.query.filter_by(id = post_db.user_id).first()
    post_comments_db = db.session.query(User,Comment).join(Comment).filter_by(post_id = post_db.id)

    if request.method == "POST":
        content = request.form.get('content')

        new_post_comment = Comment(content = content, profile_id=None, user_id = current_user.id, post_id = post_db.id)
        db.session.add(new_post_comment)
        db.session.commit()
        return redirect(url_for('views.post', category_id=category_id, title=title))

    return render_template('post.html', user=current_user, post = post_db, author = user_db, comments = post_comments_db)

@views.route('posts/<category_id>/<title>/delete_post')
@login_required
def delete_post(category_id, title):
    post_db = Post.query.filter_by(title = title).first()

    if post_db:
        db.session.delete(post_db)
        db.session.commit()
        return redirect(url_for('views.posts', category_id = category_id))

@views.route('posts/<category_id>/<title>/like_post')
@login_required
def like_post(category_id, title):
    post_db = Post.query.filter_by(title=title).first()
    like = Comment_Like.query.filter_by(user_id = current_user.id, post_id = post_db.id).first()

    if like:
        db.session.delete(like)
        db.session.commit()
        return redirect(url_for('views.post', category_id = category_id, title = title))
    elif not like:
        new_like = Comment_Like(user_id = current_user.id, post_id = post_db.id)
        db.session.add(new_like)
        db.session.commit()
        return redirect(url_for('views.post', category_id = category_id, title = title))

@views.route('posts/<category_id>/<title>/<comment_id>/delete_post_comment')
@login_required
def delete_post_comment(category_id, title, comment_id):
    comment_db = Comment.query.filter_by(id = comment_id).first() 

    if comment_db:
        db.session.delete(comment_db)
        db.session.commit()
        return redirect(url_for('views.post', category_id = category_id, title=title))


@views.route('posts/<category_id>/<title>/<comment_id>/like_post_comment')
@login_required
def like_post_comment(category_id, title, comment_id):
    comment_db = Comment.query.filter_by(id = comment_id).first()
    like = Comment_Like.query.filter_by(user_id = current_user.id, comment_id = comment_db.id).first()

    if like:
        db.session.delete(like)
        db.session.commit()
        return redirect(url_for('views.post', category_id = category_id, title = title))
    elif not like:
        new_like = Comment_Like(user_id = current_user.id, comment_id = comment_db.id)
        db.session.add(new_like)
        db.session.commit()
        return redirect(url_for('views.post', category_id = category_id, title = title))


@views.route('search', methods=['GET', 'POST'])
@login_required
def search():
    
    if request.method == "POST":
        username = request.form.get('name_find_user')
        search = f"%{username}%"

        users_db = User.query.filter(User.username.like(search)).all()

        return render_template('search.html', user=current_user, users = users_db, query = username)

    return render_template('search.html', user=current_user, users = None)

@views.route('/profile/<user>/sub', methods=['GET'])
@login_required
def subs(user):
    user_profile = User.query.filter_by(username = user).first()
    sub_db = Subs.query.filter_by(user_id = current_user.id, profile_id = user_profile.id).first()

    if sub_db:
        db.session.delete(sub_db)
        db.session.commit()
        return redirect(url_for('views.profile', user = user))
    elif not sub_db:
        new_sub = Subs(user_id = current_user.id, profile_id = user_profile.id)
        print(new_sub)
        db.session.add(new_sub)
        db.session.commit()
        return redirect(url_for('views.profile', user = user))
