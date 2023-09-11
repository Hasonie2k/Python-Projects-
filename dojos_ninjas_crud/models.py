from mysqlconnection import connectToMySQL
class Dj:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM dojos_ninjas.dojos WHERE id = %(id)s;"
        result = connectToMySQL('dojos_ninjas').query_db(query, data)
        if result:
            return cls(result[0])
        else:
            return None
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dojos_ninjas.dojos;"
        results = connectToMySQL('dojos_ninjas').query_db(query)
        dojos = []
        for dojo in results:
            dojos.append(cls(dojo))
        return dojos

    @classmethod
    def add_dojo(cls, name):
        query = "INSERT INTO dojos_ninjas.dojos (name) VALUES (%(name)s);"
        data = {"name": name}
        connectToMySQL('dojos_ninjas').query_db(query, data)

    def get_ninjas(self):
        query = "SELECT * FROM dojos_ninjas.ninjas WHERE dojo_id = %(dojo_id)s;"
        data = {"dojo_id": self.id}
        results = connectToMySQL('dojos_ninjas').query_db(query, data)
        ninjas = []
        for ninja in results:
            ninjas.append(Ninjas(ninja))
        return ninjas
        
        
class Ninjas:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.dojos_id = data['dojos_id']
        self.age = data['age']

    @classmethod
    def get_all_ninjas(cls):
        query = "SELECT * FROM dojos_ninjas.ninjas;"
        results = connectToMySQL('dojos_ninjas').query_db(query)
        ninjas = []
        for ninja in results:
            ninjas.append(cls(ninja))
        return ninjas

    @classmethod
    def add_ninja(cls, data):
        query = "INSERT INTO dojos_ninjas.ninjas (first_name, last_name, age, dojos_id) VALUES (%(first_name)s, %(last_name)s, %(age)s, %(dojo_id)s);"
        connectToMySQL('dojos_ninjas').query_db(query, data)
