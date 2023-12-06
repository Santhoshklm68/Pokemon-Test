from flask_restx import Api, Resource, reqparse, fields, marshal_with, Namespace
from enum import Enum
from database.poke_database import Database, Pokemon
from pony.orm import db_session, commit, select

api=Api()
ns=Namespace('PoKeR')

pokemon_model = api.model('Pokemon', {
    'id': fields.Integer(required=True),
    'name': fields.String(required=True),
    'type': fields.String(required=True),
})

class ValidTypes(Enum):
    GRASS='grass'
    FIRE='fire'
    WATER='water'

parser = reqparse.RequestParser()
parser.add_argument('id', type=int,  help='Filter Pokémon by id')
# parser.add_argument('type', type=str, choices=[t.value for t in ValidTypes], help='Filter Pokémon by type')
 

#----------------------------------------post and patch method-------------------------------------------------------#
parsertype = reqparse.RequestParser()
parsertype.add_argument('id', type=int, required=True, help='Pokémon id cannot be blank')
parsertype.add_argument('name', type=str, required=True, help='Pokémon name cannot be blank')
parsertype.add_argument('type', type=str, required=True, help='Pokémon type cannot be blank')

#---------------------------------------delete method------------------------------------------------------#
parsing= reqparse.RequestParser()
parsing.add_argument('id', type=int, required=True, help='Pokémon id cannot be blank')




@ns.route('/')
class PokemonResource(Resource):
    @db_session
    @ns.expect(parser)
    @ns.marshal_with(pokemon_model)
    def get(self):
        args = parser.parse_args()
        type_filter = args.get('id')

        if type_filter:
            pokemon_data = select(p for p in Pokemon if p.id == type_filter)
        else:
             pokemon_data = select(p for p in Pokemon)
            
        return list(pokemon_data)
        

    
   
    @db_session
    @ns.expect(pokemon_model)
    @ns.marshal_with(pokemon_model)
    def post(self):
        args = parsertype.parse_args()
        new_pokemon = Pokemon( name=args['name'], type=args['type'])
        commit()

        return new_pokemon
    


    @db_session
    @ns.expect(pokemon_model)
    @ns.marshal_with(pokemon_model)
    def patch(self):
        args = parsertype.parse_args()
        pokemon_id = args['id']
        pokemon_name = args['name']
        pokemon_type = args['type']

        existing_pokemon = Pokemon.get(id=pokemon_id)

        if existing_pokemon:
            existing_pokemon.name = pokemon_name
            existing_pokemon.type = pokemon_type
            commit()
            return existing_pokemon
        else:
            return {'message': f'Pokemon with name {pokemon_id} not found'}, 404
        
        

    @db_session
    @ns.expect(parsing)
    # @ns.marshal_with(pokemon_model)
    def delete(self):
        args = parsing.parse_args()
        pokemon_id = args['id']

        existing_pokemon = Pokemon.get(id=pokemon_id)

        if existing_pokemon:
            existing_pokemon.delete()
            commit()
            return {'message': f'Pokemon with id {pokemon_id} deleted successfully'}
        else:
            return {'message': f'Pokemon with id {pokemon_id} not found'}, 404
