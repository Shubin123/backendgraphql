# flask_sqlalchemy/schema.py
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Department as DepartmentModel, Employee as EmployeeModel


class Department(SQLAlchemyObjectType):
    class Meta:
        model = DepartmentModel
        interfaces = (relay.Node, )


class Employee(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeModel
        interfaces = (relay.Node, )




class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # Allows sorting over multiple columns, by default over the primary key
    all_employees = SQLAlchemyConnectionField(Employee.connection)
    # Disable sorting over this field
    all_departments = SQLAlchemyConnectionField(Department.connection, sort=None)

class createDepartment(graphene.Mutation):
    """creates new department with name"""

    class Arguments:
        name = graphene.String(required=True)
    department = graphene.Field(lambda: Department)
    
    def mutate(self, info, name):
        """hire employee with name and by existing department_id"""
        department = DepartmentModel(name=name)

        db_session.add(department)
        db_session.commit()

        return createDepartment(department=department)

class Hire(graphene.Mutation):
    """
    hire an employee
    """
    class Arguments:    
        name = graphene.String(required=True) 
        department_id = graphene.Int(required=True)
    employee = graphene.Field(lambda: Employee)        
    def mutate(self, info, name, department_id):
        """hire employee with name and by existing department_id"""
        employee = EmployeeModel(name=name, department_id=department_id)

        db_session.add(employee)
        db_session.commit()

        return Hire(employee=employee)


class Fire(graphene.Mutation):
    """
    fire an employee
    """
    class Arguments:
        id = graphene.ID(required=True)
        
    employee = graphene.Field(lambda: Employee)        
    def mutate(self, info, id):
        """fire employee with name and by existing id"""
        node = relay.Node.Field()
    # Allows sorting over multiple columns, by default over the primary key
        employee = SQLAlchemyConnectionField(Employee.connection).get_node(info, id)
   

        db_session.delete(employee)
        db_session.commit()

        return None

class Mutation(graphene.ObjectType):
    hire_employee = Hire.Field()
    fire_employee = Fire.Field()
    create_department = createDepartment.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)