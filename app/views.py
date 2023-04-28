from flask import render_template, request, session, redirect, url_for, flash
import random, string
from hackergram import app
import models as models


# Renders errors
def error(msg):
    if 'username' in session:
        username = session['username']
        user = models.get_user_settings(username)
        return render_template('error.html', current_user=user, msg=msg)
    else:
        return render_template('error.html', msg=msg)


# Renders errors
@app.route('/reset', methods=['GET', 'POST'])
def reset():
    models.reset()
    flash('Hackergram was reset', 'success')
    return redirect(url_for('home'))


# Homepage (redirects to login if user is not logged in)
@app.route('/')
def home():
    if 'username' in session:
        username = session['username']
        user = models.get_user_settings(username)
        try:
            posts_to_show = models.get_posts('')[::-1]
        except Exception as e:
            return error(e)

        if user:
            return render_template('home.html', current_user=user, posts=posts_to_show)
    return redirect(url_for('login'))


# Signs in users
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        username = session['username']
        user = models.get_user_settings(username)
        flash('You are already logged in', 'error')
        return redirect(url_for('home'))
    
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']

    if username == "" or password == "":
        flash("Invalid username or password", 'error')
        return redirect(url_for('login'))

    try:
        user = models.login(username, password)
    except Exception as e:
        return error(e)

    if not user:
        flash('Invalid username or password', 'error')
        return redirect(url_for('login'))

    session['username'] = username
    flash('Signed in successfully', 'success')
    return redirect(url_for('home'))


# Signs up new users
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'username' in session:
        username = session['username']
        user = models.get_user_settings(username)
        flash('You are already logged in', 'error')
        return redirect(url_for('home'))

    if request.method == 'GET':
        return render_template('signup.html')

    username = request.form['username']
    name = request.form['name']
    password = request.form['password']

    if username == "" or name == "" or password == "":
        flash("Invalid username, name or password", 'error')
        return redirect(url_for('signup'))

    try:
        user = models.get_user_settings(username)
    except Exception as e:
        return error(e)

    if user:
        flash("@%s is already taken" % user.username, 'error')
        return redirect(url_for('signup'))

    try:
        user = models.signup(username, password, name)
    except Exception as e:
        return error(e)

    session['username'] = username
    flash('Account created', 'success')
    return redirect(url_for('home'))


# Logs out users
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('home'))


# Allows a user to see and change their settings
@app.route('/settings', methods=["GET", "POST"])
def settings():
    if 'username' in session:
        username = session['username']
        user = models.get_user_settings(username)
    else:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('settings.html', current_user=user)
    
    new_name = request.form['name']
    if not new_name:
        new_name = user.name

    new_bio = request.form['bio']
    if not new_bio:
        new_bio = user.bio

    new_photo = request.files['photo']
    if not new_photo or new_photo == '':
        new_photo_filename = user.photo
    else:
        new_photo_filename = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '_' + new_photo.filename
        new_photo.save(app.config['photos_folder'] + new_photo_filename)
    
    current_password = request.form['currentpassword']
    new_password = request.form['newpassword']
    if not new_password:
        new_password = current_password
    else:
        if current_password == new_password:
            flash("New password must be different from current password", 'error')
            return render_template('settings.html', current_user=user)
    if current_password != user.password:
        flash("Invalid password", 'error')
        return render_template('settings.html', current_user=user)
    
    try:
        user = models.update_user_settings(username, new_name, new_password, new_bio, new_photo_filename)
    except Exception as e:
        return error(e)

    if user:
        flash("Your settings were updated", 'success')
        return render_template('settings.html', current_user=user)


# Shows the profile of user with [username]
@app.route('/profile', methods=["GET"])
def profile():
    if 'username' in session:
        username = session['username']
        user = models.get_user_settings(username)

        u = request.args.get('username')
        if not u:
            return error("No user provided")
        try:
            profile = models.get_profile(u)
            if profile == None:
                return error("User does not exist")
        except Exception as e:
            return error(e)
        
        if user:
            is_friend = False
            is_pending_requestee = False
            is_pending_requester = False
            if u in models.get_username_of_friends(username):
                is_friend = True
            else:
                if models.is_request_pending(u, username):
                    is_pending_requestee = True
                if models.is_request_pending(username, u):
                    is_pending_requester = True
            return render_template('profile.html', current_user=user, profile=profile, is_friend=is_friend, is_pending_requester=is_pending_requester, is_pending_requestee=is_pending_requestee)
    return redirect(url_for('login'))


# Creates a new post
@app.route('/create_post', methods=["GET", "POST"])
def create_post():
    if 'username' in session:
        username = session['username']
        user = models.get_user_settings(username)
    else:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('create_post.html', current_user=user)

    new_content = request.form['content']

    if not new_content:
        flash("You cannot publish an empty post", 'error')
        return render_template('create_post.html', current_user=user)

    try:
        new_post = models.create_post(username, new_content)
    except Exception as e:
        return error(e)

    if new_post:
        flash("New post published", 'success')
    else:
        flash("Failed to publish the new post", 'error')

    return redirect(url_for('home'))


# Edits post with [id]
@app.route('/edit_post', methods=["GET", "POST"])
def edit_post():
    if 'username' in session:
        username = session['username']
        user = models.get_user_settings(username)
    else:
        return redirect(url_for('login'))

    if request.method == 'GET':
        post_id = request.args.get('id')
        if int(post_id) not in models.get_post_ids(username):
            flash("You cannot edit other users' posts", 'error')
            return redirect(url_for('home'))
        try:
            post = models.get_post(post_id)
        except Exception as e:
            return error(e)
        return render_template('edit_post.html', current_user=user, post=post)

    new_content = request.form['content']
    post_id = request.form['id']

    if int(post_id) not in models.get_post_ids(username):
        flash("You cannot edit other users' posts", 'error')
        return redirect(url_for('home'))

    if not new_content:
        flash("You cannot publish an empty post", 'error')
        return render_template('edit_post.html', current_user=user, post=post)

    try:
        new_post = models.edit_post(post_id, new_content)
    except Exception as e:
        return error(e)

    if new_post:
        flash("Post was edited", 'success')
    else:
        flash("Failed to edit post", 'error')

    return redirect(url_for('home'))


# Deletes post with [id]
@app.route('/delete_post', methods=["GET"])
def delete_post():
    if 'username' in session:
        username = session['username']
        user = models.get_user_settings(username)
    else:
        return redirect(url_for('login'))
    if request.method == 'GET':
        post_id = request.args.get('id')
        if int(post_id) not in models.get_post_ids(username):
            flash("You cannot delete other users' posts", 'error')
            return redirect(url_for('home'))
        try:
            post = models.delete_post(post_id)
        except Exception as e:
            return error(e)
        flash("Post deleted", 'success')
        return redirect(url_for('home'))


# Sends friendship request to user with [username]
@app.route('/request_friend', methods=["POST"])
def request_friend():
    if 'username' in session:
        username = session['username']
        user = models.get_user_settings(username)
    else:
        return redirect(url_for('login'))

    new_friend = request.form['username']
    if not models.get_user_settings(new_friend):
        flash("@%s does not exist" % new_friend, 'error')
        return redirect(url_for('home'))
    if not new_friend or new_friend == username:
        flash("Invalid username", 'error')
        return redirect(url_for('home'))
    if new_friend in models.get_username_of_friends(username): 
        flash("@%s is already your friend" % new_friend, 'error')
        return redirect(url_for('home'))
    if models.is_request_pending(new_friend, username):
        flash("You have a pending friendship request to/from @%s." % new_friend, 'error')
        return redirect(url_for('home'))

    try:
        new_request = models.new_friend_request(username, new_friend)
    except Exception as e:
        return error(e)

    if new_request:
        flash("Friendship request sent to @%s" % new_friend, 'success')
    else:
        flash("Failed to send friendship request to @%s" % new_friend, 'error')

    return redirect(url_for('profile')+'?username='+new_friend)


# Accepts friendship request from user with [username]
@app.route('/requests', methods=["GET"])
def requests():
    if 'username' in session:
        username = session['username']
        user = models.get_user_settings(username)
    else:
        return redirect(url_for('login'))
    try:
        friend_requests = models.get_friend_requests(username)
    except Exception as e:
        return error(e)

    accept_friend = request.args.get('username', default = "")
    if accept_friend == "":
        return render_template('requests.html', current_user=user, friend_requests=friend_requests)
    if not accept_friend or not models.is_request_pending(accept_friend, username):
        flash("Invalid friendship request", 'error')
        return render_template('requests.html', current_user=user, friend_requests=friend_requests)
    try:
        new_friend = models.accept_friend_request(username, accept_friend)
    except Exception as e:
        return error(e)
    if new_friend:
        flash("Friendship request from @%s was accepted" % accept_friend, 'success')
    else:
        flash("Failed to accept friendship request from @%s" % accept_friend, 'error')

    origin = request.args.get('origin', default = "")
    if origin == 'requests':
        return redirect(url_for('requests'))
    elif origin == 'profile':
        return redirect(url_for('profile')+'?username='+accept_friend)
    else:
        return redirect(url_for('home'))


# Removes friendship request from user with [username]
@app.route('/remove_request', methods=["POST"])
def remove_request():
    if 'username' in session:
        username = session['username']
        user = models.get_user_settings(username)
    else:
        return redirect(url_for('login'))
    
    tentative_friend = request.form['username']
    if not tentative_friend:# or not models.is_request_pending(tentative_friend, username) or not models.is_request_pending(username, tentative_friend):
        return error("Invalid friendship request")
    try:
        success = models.remove_friend_request(username, tentative_friend)
    except Exception as e:
        return error(e)
    if success:
        flash("Friendship request was removed", 'success')
    else:
        flash("Failed to remove friendship request", 'error')
    
    origin = request.form['origin']
    if origin == 'requests':
        return redirect(url_for('requests'))
    elif origin == 'profile':
        return redirect(url_for('profile')+'?username='+tentative_friend)
    else:
        return redirect(url_for('home'))
    

# Removes friendship with user with [username]
@app.route('/remove_friend', methods=["POST"])
def remove_friend():
    if 'username' in session:
        username = session['username']
        user = models.get_user_settings(username)
    else:
        return redirect(url_for('login'))
    
    friend = request.form['username']
    if not friend or friend not in models.get_username_of_friends(username):
        return error("Introduce an existing friend.")
    try:
        success = models.remove_friend(username, friend)
    except Exception as e:
        return error(e)
    if success:
        flash("@%s is no longer your friend" % friend, 'success')
    else:
        flash("Failed to remove friend", 'error')
    
    return redirect(url_for('profile')+'?username='+friend)


# Shows friends of user with [username] that match the search [query]
@app.route('/friends', methods=["GET"])
def friends():
    if 'username' in session:
        username = session['username']
        user = models.get_user_settings(username)
    else:
        return redirect(url_for('login'))

    u = request.args.get('username')
    if not u:
        return error("No user provided")
    query = request.args.get('search', default = "")

    try:
        friends = models.get_friends(u, query)
    except Exception as e:
        return error(e)

    return render_template('friends.html', current_user=user, friends=friends, username=u, query=query)


# Shows users that match the search [query]
@app.route('/users', methods=["GET"])
def users():
    if 'username' in session:
        username = session['username']
        user = models.get_user_settings(username)
    else:
        return redirect(url_for('login'))

    query = request.args.get('search', default = "")

    try:
        users = models.get_users(query)
    except Exception as e:
        return error(e)

    return render_template('users.html', current_user=user, users=users, query=query)


# Shows posts that match the search [query]
@app.route('/posts', methods=["GET"])
def posts():
    if 'username' in session:
        username = session['username']
        user = models.get_user_settings(username)
    else:
        return redirect(url_for('login'))

    query = request.args.get('search', default = "")

    try:
        posts = models.get_posts(query)[::-1]
    except Exception as e:
        return error(e)

    return render_template('posts.html', current_user=user, posts=posts, query=query)