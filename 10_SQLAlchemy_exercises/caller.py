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
    searched_recipes = [el.name for el in (session.query(Recipe).filter(
                                            Recipe.ingredients.ilike(f"%{ingredient_name}%")).all())
                        ]

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


@session_decorator(session)
def relate_recipe_with_chef_by_name(recipe_name, chef_name):
    recipe = session.query(Recipe).filter_by(name=recipe_name).first()

    if recipe and recipe.chef:
        raise Exception(f"Recipe: {recipe_name} already has a related chef")

    chef = session.query(Chef).filter_by(name=chef_name).first()

    recipe.chef = chef

    return f"Related recipe {recipe_name} with chef {chef_name}"

# musaka_recipe = Recipe(name="Musaka", ingredients="Potatoes, Ground Meat, Onions, Eggs, Milk, Cheese, Spices",
#     instructions="Layer potatoes and meat mixture, pour egg and milk mixture on top, bake until golden brown.")
#
# bulgarian_chef1 = Chef(name="Ivan Zvezdev")
# bulgarian_chef2 = Chef(name="Uti Buchvarov")
#
# session.add(musaka_recipe)
# session.add(bulgarian_chef1)
# session.add(bulgarian_chef2)
# session.commit()
#
# print(relate_recipe_with_chef_by_name("Musaka", "Ivan Zvezdev"))
# print(relate_recipe_with_chef_by_name("Musaka", "Chef Uti"))


@session_decorator(session)
def get_recipes_with_chef():
    recipes_with_related_chefs = (
        session.query(Recipe.name, Chef.name.label("name_of_chef"))  # SELECT Chef.name as "name_of_chef" (alias)
        .join(Chef, Recipe.chef).all()
                                  )

    result = []
    for r_name, name_of_chef in recipes_with_related_chefs:
        result.append(f"Recipe: {r_name} made by chef: {name_of_chef}")

    return "\n".join(result)

# chef1 = Chef(name="Gordon Ramsay")
# chef2 = Chef(name="Julia Child")
# chef3 = Chef(name="Jamie Oliver")
# chef4 = Chef(name="Nigella Lawson")
# recipe1 = Recipe(name="Beef Wellington", ingredients="Beef fillet, Puff pastry, Mushrooms, Foie gras", instructions="Prepare the fillet and encase it in puff pastry.")
# recipe1.chef = chef1
# recipe2 = Recipe(name="Boeuf Bourguignon", ingredients="Beef, Red wine, Onions, Carrots", instructions="Slow-cook the beef with red wine and vegetables.")
# recipe2.chef = chef2
# recipe3 = Recipe(name="Spaghetti Carbonara", ingredients="Spaghetti, Eggs, Pancetta, Cheese", instructions="Cook pasta, mix ingredients.")
# recipe3.chef = chef3
# recipe4 = Recipe(name="Chocolate Cake", ingredients="Chocolate, Flour, Sugar, Eggs", instructions="Bake a delicious chocolate cake.")
# recipe4.chef = chef4
# recipe5 = Recipe(name="Chicken Tikka Masala", ingredients="Chicken, Yogurt, Tomatoes, Spices", instructions="Marinate chicken and cook in a creamy tomato sauce.")
# recipe5.chef = chef3
# session.add_all([chef1, chef2, chef3, chef4, recipe1, recipe2, recipe3, recipe4, recipe5])
# session.commit()
# print(get_recipes_with_chef())


