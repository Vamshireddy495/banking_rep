from app.core.database import Base, engine
from app.models import user, account, transaction

def create_tables():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Finished.")

if __name__ == '__main__':
    create_tables()

#Execution order 3