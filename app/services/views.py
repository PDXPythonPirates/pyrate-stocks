from ..main import main

@main.route('/')
def home():
    return 'Welcome Home!'

if __name__=='__main__':
    main.run(debug=True)