# # applet/schema.py (inner schema to model)
# from pyexpat import model
# from unicodedata import category
# import graphene
# from graphene_django import DjangoObjectType
# from graphql import GraphQLError
# from hypothesis import note
# from numpy import require
# from requests_toolbelt import user_agent
# from ..models import Item
# # from ..models import Category
#
#
#
# class ModelType(DjangoObjectType):
#     class Meta:
#         model = Item
#         fields = ("password", "name", "notes", "category")
#
# class userQuery(graphene.AbstractType):
#     me = graphene.Field(ModelType)
#     users = graphene.List(ModelType)
#
#     def resolve_me(self, info):
#         user = info.context.user
#         if user.is_anonymous:
#             raise GraphQLError("Not logged in!")
#         return user
# class Query(graphene.ObjectType):
#
#     all_models = graphene.List(ModelType)
#
#
#
#     def resolve_all_models(root, info):
#         return Item.objects.all()
#
#
#
# # items mutations
#
# class createUserMutation(graphene.Mutation):
#     class Arguments:
#         username = graphene.String(required=True)
#         notes = graphene.String(required=True)
#         categoryid = graphene.Int(required=True)
#         password = graphene.String(required=True)
#     usermodel = graphene.Field(ModelType)
#     @classmethod
#     def mutate(cls, root, info, password, username, notes, categoryid):
#         """we need to check user does exist with the same name-> able to create"""
#         if Item.objects.filter(username=username).exists():
#             raise GraphQLError('account already exists with the same name')
#         else:
#             usermodel = Item(password = password, username=username, notes=notes)
#             usermodel.save()
#             return createUserMutation(usermodel=usermodel)
#
# class editUserMutation(graphene.Mutation):
#     class Arguments:
#         password = graphene.String(required=True)
#         username = graphene.String(required=True)
#         notes = graphene.String(required=True)
#
#     usermodel = graphene.Field(ModelType)
#     @classmethod
#     def mutate(cls, root, info, password, username, notes):
#         """we need to check name exists and  does not exist -> able to edit"""
#         if not Item.objects.filter(pk=password).exists():
#             raise GraphQLError("user with this password does not exist")
#         else:
#             usermodel = Item.objects.get(pk=password)
#             usermodel.username = username
#             usermodel.notes = notes
#             usermodel.save()
#             return editUserMutation(usermodel=usermodel)
#
# class deleteUserMutation(graphene.Mutation):
#     class Arguments:
#         # password = graphene.String(required=True)
#         username = graphene.String(required=True)
#     usermodel = graphene.Field(ModelType)
#     @classmethod
#     def mutate(cls, root, info, username):
#         """check pk userid exist -> able to delete"""
#         if Item.objects.filter(username=username).exists():
#             # check user passwored maches the one for the user
#
#             usermodel = Item.objects.get(username=username)
#             usermodel.delete()
#             return deleteUserMutation(usermodel=usermodel)
#         else:
#             raise GraphQLError('user does not exist')
#
# # # category mutations
# # class createCategoryMutation(graphene.Mutation):
# #     """create category with name and category id (primary key)"""
# #     class Arguments:
# #         catagory_id = graphene.Int(required=True)
# #         name = graphene.String(required=True)
# #
# #     categorymodel = graphene.Field(CategoryType)
# #     @classmethod
# #     def mutate(cls, root, info, catagory_id, name):
# #         """check category does not exist with the same name-> able to create"""
# #         if Category.objects.filter(name=name).exists():
# #             raise GraphQLError('category already exists with the same name')
# #         else:
# #             categorymodel = Category(pk=catagory_id, name=name)
# #             categorymodel.save()
# #             return createCategoryMutation(categorymodel=categorymodel)
# #
#
# # class deleteCategoryMutation(graphene.Mutation):
# #     """deletes a category by name"""
# #     class Arguments:
# #         catagory_id = graphene.Int(required=True)
# #     categorymodel = graphene.Field(CategoryType)
# #     @classmethod
# #     def mutate(cls, root, info, catagory_id):
# #         if Category.objects.filter(pk=catagory_id).exists():
# #             categorymodel = Category.objects.get(pk=catagory_id)
# #             categorymodel.delete()
# #             return deleteCategoryMutation(categorymodel=categorymodel)
# #         else:
# #             raise GraphQLError('category not found')
#
# class checkUserMutation(graphene.Mutation):
#     class Arguments:
#         username = graphene.String(required=True)
#         notes = graphene.String(required=True)
#     usermodel = graphene.Field(ModelType)
#     @classmethod
#     def mutate(cls, root, info, username, notes):
#         if Item.objects.filter(name=username).exists():
#             a =  Item.objects.get(name=username)
#             if a.notes == notes:
#                 raise GraphQLError('yay')
#         else:
#             raise GraphQLError('account doe not exists with the same name')
#
# class Mutation(graphene.ObjectType):
#     # pre:
#     # create_catagory = createCategoryMutation.Field()
#     create_user = createUserMutation.Field()
#     check_user = checkUserMutation.Field()
#     # post:
#     # delete_category = deleteCategoryMutation.Field()
#     edit_user = editUserMutation.Field()
#     delete_user = deleteUserMutation.Field()
#
#
#
# # schema = graphene.Schema(query=Query, mutation=Mutation) schema now initialized on proxy layer
