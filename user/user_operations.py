from sqlalchemy import select, insert, delete

class Labour:
    def __init__(self, conn, labour_table):
        self.conn = conn
        self.labour_table = labour_table

    def Create(self, name, area):
        query = insert(self.labour_table).values(name=name, area=area)
        self.conn.session.execute(query)
        self.conn.session.commit()
        print("Successfully Inserted Into Database")

    def GetLabourByID(self, id):
        query = select(self.labour_table).filter_by(id=id)
        data = self.conn.session.execute(query).scalar_one()
        return data

    def GetLaboursBySMID(self, smid):
        query = select(self.labour_table).filter_by(sales_manager=smid)
        data = self.conn.session.execute(query)
        return data

    def GetAll(self):
        query = select(self.labour_table)
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
        query = delete(self.labour_table).filter_by(id=id)
        self.conn.session.execute(query)
        self.conn.session.commit()
        print("Sucessfully Deleted From Database")

