# Hackergram Lab


## Description

Hackergram is an intentionally vulnerable web application that was designed with the purpose of providing students and security enthusiasts with a lab environment where they can gain practical experience in identifying and exploiting web vulnerabilities, such as Cross-Site Request Forgery, Cross-Site Scripting and SQL Injection.


## Summary 

This vulnerable web application consists of a simple social networking website. In Hackergram, users can create an account by registering their username, password and name. Once registered, users can log into their account and start using its various features:
- Posts are the main feature of the website. Users can write posts that will then be shown to other users on the homepage.
- Posts can also be edited or deleted.
- Users can connect with each other by sending friendship requests, which can be accepted or declined.
- A user can also remove his friendship with another user at any time.
- Users can navigate to any user's profile to see their information (i.e., name, username, picture and bio), as well as their posts and friends.
- A user is allowed to change their own settings (i.e., name, password, picture and bio).
- There is a search functionality that allows users to search for posts with a specific word or content and search for other users by username.

Hackergram is not an attempt at replicating or improving upon any existing social networking websites. Instead, it provides a controlled environment where students and security enthusiasts can test their knowledge and skills without causing any harm to real-world systems or users. Hackergram was created to be a simple, yet realistic web application and its features were purposefully designed to be vulnerable to these attacks.


## Setting up the lab

### 1. Clone this repository

```
$ git clone https://github.com/0xDrogon/hackergram-lab.git
```

### 2. Run the script

```
$ chmod +x docker_run.sh
$ ./docker_run.sh
```

### 3. Hackergram is available at

```
http://localhost:5000
```

### Docker image

A Docker image is also available at `https://hub.docker.com/r/0xdrogon/hackergram`
```
docker pull 0xdrogon/hackergram
```



## Default users

| Username   | Password       |
|------------|----------------|
| admin      | 1_4m_Th3_4dm1n |
| mr_robot   | elliot123      | 
| dpr        | silk-road      | 
| satoshi    | bitcoin2009    | 
| heisenberg | walter1958     |
| rick       | RickC-137      | 
| stark      | winterfell     | 
| anon1      | 1              | 
| anon2      | 2              | 
| anon3      | 3              | 



## Attacks tested

- Cross-Site Request Forgery
    - CSRF with a GET request
        - on `/delete_post` endpoint
        - on `/requests` endpoint 
    - CSRF with a POST request
        - on `/create_post` endpoint
        - on `/edit_post` endpoint
        - on `/request_friend` endpoint
        - on `/remove_friend` endpoint
- Cross-Site Scripting
    - Stored XSS
        - on `/create_post` endpoint
        - on `/settings` endpoint
    - Reflected XSS
        - on `/users` endpoint
        - on `/posts` endpoint
    - XSS worm
        - on `/create_post` endpoint
        - on `/settings` endpoint
- SQL Injection
    - Authentication bypass
        - on `/login` endpoint
    - Union-based SQLi
        - on `/users` endpoint
        - on `/posts` endpoint
    - Piggybacked SQLi
        - on `/users` endpoint
        - on `/posts` endpoint
    - Eror-based SQLi
        - on `/users` endpoint
        - on `/posts` endpoint
    - Boolean-based SQLi
        - on `/users` endpoint
        - on `/posts` endpoint
    - Time-based SQLi
        - on `/users` endpoint
        - on `/posts` endpoint
    - Using SQLi to change other user's profile
        - on `/settings` endpoint



## Disclaimer

This lab is extremely vulnerable and intended for educational purposes only. Do not use it in production.