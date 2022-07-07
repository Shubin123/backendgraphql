#  outer schema located in root (auth lair connected to inner schema)

# import applet.modelstore.schema.schema as super
import graphene



from graphql_auth.schema import UserQuery
from graphql_auth import mutations

class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    update_account = mutations.UpdateAccount.Field()
    password_change = mutations.PasswordChange.Field()
    password_reset = mutations.PasswordReset.Field()
    delete_account = mutations.DeleteAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()

class Query(UserQuery, graphene.ObjectType):
    pass

class Mutation(AuthMutation,
# super.Mutation,
graphene.ObjectType):
   pass

schema = graphene.Schema(query=Query,
                         mutation=Mutation
)