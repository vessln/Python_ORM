from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from decorator import session_decorator
from models import Recipe, Chef

engine = create_engine("postgresql+psycopg2://postgres-user:password@localhost/sqlalchemy_db")
Session = sessionmaker(bind=engine)

session = Session()


@session_decorator(session)
def create_recipe(name, ingredients, instructions):
    my_recipe = Recipe(
        name=name,
        ingredients=ingredients,
        instructions=instructions,
    )

    session.add(my_recipe)

# recipe1 = create_recipe("Spaghetti Carbonara",	"Pasta, Eggs, Pancetta, Cheese", "Cook the pasta, mix it with eggs, pancetta, and cheese")
# recipe2 = create_recipe("Chicken Stir-Fry", "Chicken, Bell Peppers, Soy Sauce, Vegetables", "Stir-fry chicken and vegetables with soy sauce")
# recipe3 = create_recipe("Caesar Salad", "Romaine Lettuce, Croutons, Caesar Dressing", "Toss lettuce with dressing and top with croutons")


@session_decorator(session)
def update_recipe_by_name(name, new_name,  new_ingredients, new_instructions):

    num_update_records = (
        session.query(Recipe).filter_by(name=name).update(
            {Recipe.name: new_name,
             Recipe.ingredients: new_ingredients,
             Recipe.instructions: new_instructions,
             }
        )
    )

    return f"{num_update_records} records are updated"


# print(update_recipe_by_name(
#     "Spaghetti Carbonara",
#     new_name="Carbonara Pasta",
#     new_ingredients="Pasta, Eggs, Guanciale, Cheese",
#     new_instructions="Cook the pasta, mix with eggs, guanciale, and cheese"
# ))
# updated_recipe = session.query(Recipe).filter(Recipe.name == "Carbonara Pasta").first()
#
# print("Updated Recipe Details:")
# print(f"Name: {updated_recipe.name}")
# print(f"Ingredients: {updated_recipe.ingredients}")
# print(f"Instructions: {updated_recipe.instructions}")


@session_decorator(session)
def delete_recipe_by_name(name):
    num_deleted_records = (
        session.query(Recipe).filter_by(name=name).delete()
    )

    return f"{num_deleted_records} records are deleted."

# print(delete_recipe_by_name("Carbonara Pasta"))
# recipes = session.query(Recipe).all()
# for recipe in recipes:
#     print(f"Recipe name: {recipe.name}")


@session_decorator(session)
def get_recipes_by_ingredient(ingredient_name):
    searched_recipes = [el.name for el in (
        session.query(Recipe).filter(
            Recipe.ingredients.ilike(f"%{ingredient_name}%")).all()
    )]

    return "\n".join(searched_recipes)

# print(get_recipes_by_ingredient("Chicken"))


@session_decorator(session)
def swap_recipe_ingredients_by_name(first_recipe_name, second_recipe_name):
    recipe1 = (session.query(Recipe)
               .filter_by(name=first_recipe_name)
               .with_for_update()  # lock record-only this update is performed for the current records in one session
               .one())  # return one record

    recipe2 = (session.query(Recipe)
               .filter_by(name=second_recipe_name)
               .with_for_update()
               .one())

    recipe1.ingredients, recipe2.ingredients = recipe2.ingredients, recipe1.ingredients

# create_recipe("Pancakes", "Flour, Eggs, Milk", "Mix and cook on a griddle")
# create_recipe("Waffles", "Flour, Eggs, Milk, Baking Powder", "Mix and cook in a waffle iron")
#
# swap_recipe_ingredients_by_name("Pancakes", "Waffles")
#
# recipe1 = session.query(Recipe).filter_by(name="Pancakes").first()
# recipe2 = session.query(Recipe).filter_by(name="Waffles").first()
# print(f"Pancakes ingredients {recipe1.ingredients}")
# print(f"Waffles ingredients {recipe2.ingredients}")





