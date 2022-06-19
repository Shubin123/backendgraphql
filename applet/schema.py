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
    all_categorys = graphene.List(CategoryType)
    all_models = graphene.List(ModelType)
    category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True)) # make this main query method

    def resolve_all_ingredients(root, info):
        # We can easily optimize query count in the resolve method
        return modelstore.objects.select_related("category").all()

    def resolve_category_by_name(root, info, name):
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            return None



# items mutations
class editUserMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)
        notes = graphene.String(required=True)
        categoryname = graphene.Int(required=True)
        
    usermodel = graphene.Field(ModelType)
    @classmethod
    def mutate(cls, root, info, id, name, notes, categoryname):
        """we need to check pk category name exist -> able to edit"""
        usermodel = Item.objects.get(pk=id)
        usermodel.name = name
        usermodel.notes = notes
        usermodel.category = Category.objects.get(pk=categoryname)
        usermodel.save()
        return editUserMutation(usermodel=usermodel)

class createUserMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        notes = graphene.String(required=True)
        category = graphene.Int(required=True)
    usermodel = graphene.Field(ModelType)
    @classmethod
    def mutate(cls, root, info, name, notes, category):
        """we need to check pk category name does not exist -> able to create"""
        usermodel = Item(name=name, notes=notes, category=Category.objects.get(pk=category))
        usermodel.save()
        return createUserMutation(usermodel=usermodel)

class deleteUserMutation(graphene.Mutation):
    class Arguments:
        userid = graphene.Int(required=True)
    usermodel = graphene.Field(ModelType)
    @classmethod 
    def mutate(cls, root, info, userid):
        """we need to check pk userid exist -> able to delete"""
        usermodel = Item.objects.get(pk=userid)
        usermodel.delete()
        return deleteUserMutation(usermodel=usermodel)

# category mutations 
class createCategoryMutation(graphene.Mutation):
    """create category with name and category id (primary key)"""
    class Arguments:
        catagory_id = graphene.Int(required=True)
        name = graphene.String(required=True)
        
    categorymodel = graphene.Field(CategoryType)
    @classmethod
    def mutate(cls, root, info, catagory_id, name):
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
        categorymodel = Category.objects.get(pk=catagory_id)
        categorymodel.delete()
        return deleteCategoryMutation(categorymodel=categorymodel)

class Mutation(graphene.ObjectType):
    # pre:
    create_catagory = createCategoryMutation.Field()
    create_user = createUserMutation.Field()
    
    # post:
    delete_category = deleteCategoryMutation.Field()
    edit_user = editUserMutation.Field()
    delete_user = deleteUserMutation.Field()
    
schema = graphene.Schema(query=Query, mutation=Mutation)
