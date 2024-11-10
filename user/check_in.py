from sqlalchemy import select, insert, delete

class check_in_time:
    def __init__(self, conn, check_in_time_table):
        self.conn = conn
        self.salesmanager_table = check_in_time_table

    def Create(self, in_time, out_time):
        query = insert(self.check_in_time_table).values(in_time=in_time, out_time=out_time)
        self.conn.session.execute(query)
        self.conn.session.commit()
        print("Successfully Inserted Into Database")
