from sqlalchemy import select, insert, delete

class Salesmanager:
    def __init__(self, conn, salesmanager_table):
        self.conn = conn
        self.salesmanager_table = salesmanager_table

    def Create(self, name , area):
        query = insert(self.salesmanager_table).values( name=name , area=area)
        self.conn.session.execute(query)
        self.conn.session.commit()
        print("Successfully Inserted Into Database")

    def Get(self, id):
        query = select(self.salesmanager_table).filter_by(id=id)
        data = self.conn.session.execute(query).scalar_one()
        return data

    def GetAll(self):
        query = select(self.salesmanager_table)
        data = self.conn.session.execute(query)
        

        data_map = []
        for i in data:
            m = {}
            m["id"] = i[0].id
            m["name"] = i[0].name
            m["area"] = i[0].area
            data_map.append(m)

        return data_map
        
    def Delete(self, id):
        query = delete(self.salesmanager_table).filter_by(id=id)
        self.conn.session.execute(query)
        self.conn.session.commit()
        print("Sucessfully Deleted From Database")

