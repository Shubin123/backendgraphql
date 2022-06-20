# applet/schema.py (inner schema to model)
from pyexpat import model
from typing_extensions import Required
from unicodedata import category
import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from hypothesis import note
from numpy import require
from requests_toolbelt import user_agent
from ..models import Category, Item

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "items")

class ModelType(DjangoObjectType):
    class Meta:
        model = Item
        fields = ("password", "name", "notes", "category")

class userQuery(graphene.AbstractType):
    me = graphene.Field(ModelType)
    users = graphene.List(ModelType)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Not logged in!")
        return user
class Query(graphene.ObjectType):
    all_categorys = graphene.List(CategoryType)
    all_models = graphene.List(ModelType)
    category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True)) # make this main query method
    
    
    def resolve_all_categorys(root, info):
        return Category.objects.all()

    def resolve_all_models(root, info):
        return Item.objects.all()
    def resolve_category_by_name(root, info, name):
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            return None


# items mutations

class createUserMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        notes = graphene.String(required=True)
        categoryid = graphene.Int(required=True)
        password = graphene.String(required=True)
    usermodel = graphene.Field(ModelType)
    @classmethod
    def mutate(cls, root, info, password, username, notes, categoryid):
        """we need to check user does exist with the same name-> able to create"""
        if Item.objects.filter(name=username).exists():
            raise GraphQLError('account already exists with the same name')
        else:
            usermodel = Item(password = password, name=username, notes=notes, category=Category.objects.get(pk=categoryid))
            usermodel.save()
            return createUserMutation(usermodel=usermodel)

class editUserMutation(graphene.Mutation):
    class Arguments:
        password = graphene.String(required=True)
        name = graphene.String(required=True)
        notes = graphene.String(required=True)
        categoryID = graphene.Int(required=True)
        
    usermodel = graphene.Field(ModelType)
    @classmethod
    def mutate(cls, root, info, password, name, notes, categoryID):
        """we need to check name exists and  does not exist -> able to edit"""
        if not Item.objects.filter(pk=password).exists():
            raise GraphQLError("user with this password does not exist")
        else:
            usermodel = Item.objects.get(pk=password)
            usermodel.name = name
            usermodel.notes = notes
            usermodel.category = Category.objects.get(pk=categoryID)
            usermodel.save()
            return editUserMutation(usermodel=usermodel)

class deleteUserMutation(graphene.Mutation):
    class Arguments:
        password = graphene.String(required=True)
    usermodel = graphene.Field(ModelType)
    @classmethod 
    def mutate(cls, root, info, userid):
        """check pk userid exist -> able to delete"""
        if Item.objects.filter(pk=userid).exists():
            usermodel = Item.objects.get(pk=userid)
            usermodel.delete()
            return deleteUserMutation(usermodel=usermodel)
        else:
            raise GraphQLError('user does not exist')

# category mutations 
class createCategoryMutation(graphene.Mutation):
    """create category with name and category id (primary key)"""
    class Arguments:
        catagory_id = graphene.Int(required=True)
        name = graphene.String(required=True)
        
    categorymodel = graphene.Field(CategoryType)
    @classmethod
    def mutate(cls, root, info, catagory_id, name):
        """check category does not exist with the same name-> able to create"""
        if Category.objects.filter(name=name).exists():
            raise GraphQLError('category already exists with the same name')
        else:
            categorymodel = Category(pk=catagory_id, name=name)
            categorymodel.save()
            return createCategoryMutation(categorymodel=categorymodel)

class deleteCategoryMutation(graphene.Mutation):
    """deletes a category by name"""
    class Arguments:
        catagory_id = graphene.Int(required=True)
    categorymodel = graphene.Field(CategoryType)
    @classmethod    
    def mutate(cls, root, info, catagory_id):
        if Category.objects.filter(pk=catagory_id).exists():
            categorymodel = Category.objects.get(pk=catagory_id)
            categorymodel.delete()
            return deleteCategoryMutation(categorymodel=categorymodel)
        else:
            raise GraphQLError('category not found')

class checkUserMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        notes = graphene.String(required=True)
    usermodel = graphene.Field(ModelType)
    @classmethod
    def mutate(cls, root, info, username, notes):
        if Item.objects.filter(name=username).exists():
            a =  Item.objects.get(name=username)
            if a.notes == notes:
                raise GraphQLError('yay')
        else:
            raise GraphQLError('account doe not exists with the same name')

class Mutation(graphene.ObjectType):
    # pre:
    create_catagory = createCategoryMutation.Field()
    create_user = createUserMutation.Field()
    check_user = checkUserMutation.Field()
    # post:
    delete_category = deleteCategoryMutation.Field()
    edit_user = editUserMutation.Field()
    delete_user = deleteUserMutation.Field()
    
# schema = graphene.Schema(query=Query, mutation=Mutation) schema now initialized on proxy layer
