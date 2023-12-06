from pony .orm import Database, Required, PrimaryKey


db=Database()


class Pokemon(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    type = Required(str)





db.bind(provider='sqlite',filename='poke_db',create_db=True)
db.generate_mapping(create_tables=True)
