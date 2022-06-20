#  outer schema located in root (auth lair connected to inner schema)
import graphene
import applet.modelstore.schema.schema
import graphql_jwt
class Query(applet.modelstore.schema.schema.Query, graphene.ObjectType):
    pass

class Mutation(applet.modelstore.schema.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)