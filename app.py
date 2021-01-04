from Website import create_app
from sys import argv
app = create_app()

# if the last argument is 'restart' restarts the database
if argv[-1] == 'restart':
    from Website import db
    with app.app_context():
        db.drop_all()
        db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
