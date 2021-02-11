from .. import main

##### HOME #####

@main.route('/user')
def user():
    return "Hello, Hello, World!"

if __name__=='__main__':
    main.run(debug=True)