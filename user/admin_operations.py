from sqlalchemy import select

class Admin:
    def __init__(self, conn, admin_table):
        self.conn = conn
        self.admin_table = admin_table

    def authorize_user(self, username, password):
        query = select(self.admin_table).filter_by(username=username, password=password)
        data = self.conn.session.execute(query).fetchone()
        if data != None:
            return True
        
        return False