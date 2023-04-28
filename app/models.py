from hackergram import mysql
import subprocess


def reset():
    with open('start.sql', 'r') as f:
        sql = f.read()
    subprocess.run(['mysql', '-u', 'root'], input=sql.encode())


# Function for SELECT queries
def get_from_database(query):
    con = mysql.connection.cursor()
    con.execute(query)
    mysql.connection.commit()
    data = con.fetchall()
    con.close()
    return data


# Function for UPDATE, INSERT and DELETE queries
def commit_to_database(query):
    con = mysql.connection.cursor()
    con.execute(query)
    mysql.connection.commit()
    con.close()


# Gets user with given username, password to login
def login(username, password):
    query = "SELECT * FROM Users"
    query+= " WHERE username = '%s'" % (username)
    query+= " AND password = '%s'" % (password)
    
    data = get_from_database(query)

    if len(data) == 1:
        user = User(*(data[0]))
        return user
    else:
        return None
    

# Signs up new user
def signup(username, password, name):
    query = "INSERT INTO Users (username, password, name)"
    query+= " VALUES ('%s', '%s', '%s')" % (username, password, name)

    commit_to_database(query)
    return User(username, password, name)


# Gets profile with given username
def get_profile(username):
    query = "SELECT Posts.id, Posts.content, Posts.posted_at, Users.name, Users.bio, Users.photo"
    query+= " FROM Posts"
    query+= " JOIN Users ON Posts.author = Users.username"
    query+= " WHERE Users.username = '%s'" % (username)

    data = get_from_database(query)
    
    if not data:
        query2 = "SELECT name, bio, photo FROM Users"
        query2+= " WHERE username = '%s'" % (username)
        data2 = get_from_database(query2)
        if not data2:
            return None
        name, bio, photo = data2[0]
        profile = Profile(username=username, name=name, bio=bio, photo=photo, posts=None)

    else:
        posts = []
        for d in data:
            posts.append(PostToShow(id=d[0], author=username, name=d[3], photo=d[5], content=d[1], posted_at=d[2]))
        posts = posts[::-1]
        profile = Profile(username=username, name=data[0][3], bio=data[0][4], photo=data[0][5], posts=posts)

    return profile


# Gets user with given username
def get_user_settings(username):
    query = "SELECT * FROM Users"
    query+= " WHERE username = '%s'" % (username)

    data = get_from_database(query)

    if len(data) == 1:
        user = User(*(data[0]))
        return user
    else:
        return None
    

# Updates user
def update_user_settings(username, name, password, bio, photo):
    query = "UPDATE Users"
    query+= " SET username='%s', password='%s', name='%s', bio='%s', photo='%s'" % (username, password, name, bio, photo)
    query+= " WHERE username = '%s'" % (username)

    commit_to_database(query)
    return User(username, password, name, bio, photo)
    

# Creates new post
def create_post(username, content):
    query = "INSERT INTO Posts (author, content)"
    query+= " VALUES ('%s', '%s')" % (username, content)

    commit_to_database(query)
    return True


# Gets post with given id
def get_post(id):
    query = "SELECT * FROM Posts"
    query+= " WHERE id = '%s'" % (id)

    data = get_from_database(query)

    if len(data) == 1:
        post = Post(*(data[0]))
        return post
    else:
        return None


# Edits post with given id
def edit_post(id, content):
    query = "UPDATE Posts"
    query+= " SET content='%s'" % (content)
    query+= " WHERE id = '%s'" % (id)

    commit_to_database(query)
    return True


# Deletes post with given id
def delete_post(id):
    query = "DELETE FROM Posts"
    query+= " WHERE id = '%s'" % (id)

    commit_to_database(query)
    return True


# Gets ids of posts made by user
def get_post_ids(username):
    query = "SELECT id FROM Posts"
    query+= " WHERE author = '%s'" % (username)

    data = get_from_database(query)
    ids = []

    for d in data:
        ids.append(d[0])
    return ids


# Creates a friend request
def new_friend_request(username, new_friend):
    query = "INSERT INTO Requests (username1, username2)"
    query+= " VALUES ('%s', '%s')" % (username, new_friend)

    commit_to_database(query)
    return True


# Checks if there is a pending request 
def is_request_pending(requester, username):
    query = "SELECT username1 FROM Requests"
    query+= " WHERE username1 = '%s' AND username2 = '%s'" % (requester, username)
    
    data = get_from_database(query)
    return data


# Gets friend requests to user with given username
def get_friend_requests(username):
    query = "SELECT * from Users"
    query+= " WHERE username IN"
    query+= " (SELECT username1 FROM Requests"
    query+= "  WHERE username2 = '%s')" % (username)
    
    data = get_from_database(query)
    users = []

    for d in data:
        users.append(User(*d))

    return users


# Accepts friend request 
def accept_friend_request(username, accept_friend):
    query = "INSERT INTO Friends (username1, username2)"
    query+= " VALUES ('%s', '%s');" % (accept_friend, username)
    con = mysql.connection.cursor()
    con.execute(query)

    query = "DELETE FROM Requests"
    query+= " WHERE username1='%s' AND username2='%s';" % (accept_friend, username)
    con.execute(query)
    mysql.connection.commit()

    con.close()
    return True


# Removes friend request 
def remove_friend_request(username, tentative_friend):
    query = "DELETE FROM Requests"
    query+= " WHERE (username1='%s' AND username2='%s')" % (tentative_friend, username)
    query+= " OR (username1 = '%s' AND username2 = '%s')" % (username, tentative_friend)

    commit_to_database(query)
    return True


# Removes friend  
def remove_friend(username, friend):
    query = "DELETE FROM Friends"
    query+= " WHERE (username1='%s' AND username2='%s')" % (friend, username)
    query+= " OR (username1 = '%s' AND username2 = '%s')" % (username, friend)

    commit_to_database(query)
    return True


# Gets friends of user with username that match the search query
def get_friends(username, search):
    query = "SELECT * FROM Users"
    query+= " WHERE username LIKE '%%%s%%'" % (search)
    query+= " AND username IN" 
    query+= " (SELECT username1 FROM Friends"
    query+= "  WHERE username2 = '%s'" % (username)
    query+= "  UNION SELECT username2 FROM Friends"
    query+= "  WHERE username1 = '%s')" % (username)

    data = get_from_database(query)
    friends = []

    for d in data:
        friends.append(User(*d))

    return friends


# Gets friends of user (just username)
def get_username_of_friends(username):
    query = "SELECT username2 FROM Friends"
    query+= " WHERE username1 = '%s'" % (username)
    query+= " UNION"
    query+= " SELECT username1 FROM Friends"
    query+= " WHERE username2 = '%s'" % (username)

    data = get_from_database(query)
    friends = []

    for d in data:
        friends.append(d[0])
    return friends


# Gets users that match the search query
def get_users(search):
    query = "SELECT * FROM Users"
    query+= " WHERE username LIKE '%%%s%%'" % (search)

    data = get_from_database(query)
    users = []

    for d in data:
        users.append(User(*d))

    return users


# Gets posts that match the search query
def get_posts(search):
    query = "SELECT Posts.id, Users.username, Users.name, Users.photo, Posts.content, Posts.posted_at"
    query+= " FROM Posts"
    query+= " INNER JOIN Users ON Posts.author = Users.username"
    query+= " WHERE Posts.content LIKE '%%%s%%'" % (search)

    data = get_from_database(query)
    posts = []

    for d in data:
        posts.append(PostToShow(*d))

    return posts


# User class
class User():
    def __init__(self, username, password, name='', bio='', photo=''):
        self.username = username
        self.password = password
        self.name = name
        self.bio = bio
        self.photo = photo
    
    def __repr__(self):
        return '<User: username=%s, password=%s, name=%s, bio=%s, photo=%s>' % (self.username, self.password, self.name, self.bio, self.photo)
    

# Profile class
class Profile():
    def __init__(self, username, name='', bio='', photo='', posts=''):
        self.username = username
        self.name = name
        self.bio = bio
        self.photo = photo
        self.posts = posts
    
    def __repr__(self):
        return '<Profile: username=%s, name=%s, bio=%s, photo=%s, posts=%s>' % (self.username, self.name, self.bio, self.photo, self.posts)


# Post class
class Post():
    def __init__(self, id, author, content, posted_at):
        self.id = id
        self.author = author
        self.content = content
        self.posted_at = posted_at
    
    def __repr__(self):
        return '<Post: id=%s, author=%s, content=%s, posted_at=%s>' % (self.id, self.author, self.content, self.posted_at)


# PostToShow class
class PostToShow():
    def __init__(self, id, author, name, photo, content, posted_at):
        self.id = id
        self.author = author
        self.name = name
        self.photo = photo
        self.content = content
        self.posted_at = posted_at
        
    def __repr__(self):
        return '<PostToShow: id=%d, author=%s, name=%s, photo=%s, content=%s, posted_at=%s>' % (self.id, self.author, self.name, self.photo, self.content, self.posted_at)