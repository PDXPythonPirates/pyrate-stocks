from .. import main

@main.route('/ticker')
def ticker():
    return 'this is the ticker service'