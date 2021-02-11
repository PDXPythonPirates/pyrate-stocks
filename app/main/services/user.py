from .. import main

##### HOME #####

@main.route('/user')
def user():
    return "User Page"