

def Get(self, id):
        data = {}
        query = f"SELECT * FROM persons WHERE username={usernme};"
        self.cursor.execute(query)
        SM = self.cursor.fetchall()
        for i in SM:
            data["name"] = salesmanager[i][0]
            data["area"] = salesmanager[i][1]          
        return data