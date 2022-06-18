# cookbook/schema.py
from pyexpat import model
import graphene
from graphene_django import DjangoObjectType
from hypothesis import note
from requests_toolbelt import user_agent
from applet import modelstore

from applet.modelstore.models import Category, Item

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "items")

class ModelType(DjangoObjectType):
    class Meta:
        model = Item
        fields = ("id", "name", "notes", "category")

class Query(graphene.ObjectType):
    all_models = graphene.List(ModelType)
    category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))

    def resolve_all_ingredients(root, info):
        # We can easily optimize query count in the resolve method
        return modelstore.objects.select_related("category").all()

    def resolve_category_by_name(root, info, name):
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            return None

class editUserMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)
        notes = graphene.String(required=True)
        catagory = graphene.Int(required=True)
        
    usermodel = graphene.Field(ModelType)
    @classmethod
    def mutate(cls, root, info, id, name, notes, catagory):
        usermodel = Item.objects.get(pk=id)
        usermodel.name = name
        usermodel.notes = notes
        usermodel.category = Category.objects.get(pk=catagory)
        usermodel.save()
        return editUserMutation(usermodel=usermodel)

class createUserMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        notes = graphene.String(required=True)
        catagory = graphene.Int(required=True)
    usermodel = graphene.Field(ModelType)
    @classmethod
    def mutate(cls, root, info, name, notes, catagory):
        usermodel = Item(name=name, notes=notes, category=Category.objects.get(pk=catagory))
        usermodel.save()
        return createUserMutation(usermodel=usermodel)

class deleteUserMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    usermodel = graphene.Field(ModelType)
    @classmethod 
    def mutate(cls, root, info, id):
        usermodel = Item.objects.get(pk=id)
        usermodel.delete()
        return deleteUserMutation(usermodel=usermodel)
    
        
class Mutation(graphene.ObjectType):
    # pre:
    create_user = createUserMutation.Field()

    # post:
    edit_user = editUserMutation.Field()
    delete_user = deleteUserMutation.Field()
    
    
    

schema = graphene.Schema(query=Query, mutation=Mutation)