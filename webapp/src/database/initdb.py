from src import app, db
from src.database.models import *


# Registers 'initdb' cli command.
# Usage: `flask initdb`
@app.cli.command('initdb')
def initdb():
    print("Creating non-existing tables ...", end='')
    db.create_all(app=app)  # SQLAlchemy: creates tables defined in `models.py` (only if do not exist)
    print("\t[SUCCESS]")

    initialize_database()
    import_my_data()


def initialize_database():
    print("Initializing tables with basic data ...", end='')
    # if User.query.count() == 0:
    #     db.session.add(User(username='ADMIN', gender='', education='', occupation='', affiliation='', years_xp=-1))
    # db.session.commit()
    print("\t[SUCCESS]")


def import_my_data():
    print("Loading artifacts ...", end='')
    if Artifact.query.count() != 0:
        print("\t[ALREADY DONE]")
        return

    for i in range(100):
        db.session.add(Artifact(id=i))

    # conn = sqlite3.connect("path/to/data.csv")
    # cursor = conn.cursor()
    # cursor.execute("""SELECT * FROM Artifact;""")
    #
    # for row in cursor:
    #     id = int(row[0])
    #     db.session.add(Artifact(id=id))
    # conn.close()

    db.session.commit()
    print("\t[SUCCESS]")
