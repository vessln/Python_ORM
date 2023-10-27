import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character


def create_pet(name: str, species: str):
    pet = Pet.objects.create(
        name=name,
        species=species,
    )
    return f"{pet.name} is a very cute {pet.species}!"

# print(create_pet('Buddy', 'Dog'))
# print(create_pet('Whiskers', 'Cat'))
# print(create_pet('Rocky', 'Hamster'))


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool):
    artifact = Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )
    return f"The artifact {artifact.name} is {artifact.age} years old!"

def delete_all_artifacts():
    Artifact.objects.all().delete()

# print(create_artifact('Ancient Sword', 'Lost Kingdom', 500, 'A legendary sword with a rich history', True))
# print(create_artifact('Crystal Amulet', 'Mystic Forest', 300, 'A magical amulet believed to bring good fortune', True))


def show_all_locations():
    ordered_locations = Location.objects.all().order_by("-id")

    return "\n".join(str(el) for el in ordered_locations)


def new_capital():
    capital = Location.objects.first()
    capital.is_capital = True
    capital.save()

def get_capitals():
    return Location.objects.filter(is_capital=True).values("name")

def delete_first_location():
    Location.objects.first().delete()

# print(show_all_locations())
# print(new_capital())
# print(get_capitals())


def apply_discount():
    all_cars = Car.objects.all()

    for car in all_cars:
        discount = float(car.price) * (sum(int(x) for x in str(car.year)) / 100)
        car.price_with_discount = float(car.price) - discount
        car.save()

def get_recent_cars():
    return Car.objects.all().filter(year__gte=2020).values("model", "price_with_discount")

def delete_last_car():
    Car.objects.all().last().delete()

# apply_discount()
# print(get_recent_cars())
# delete_last_car()


def show_unfinished_tasks():
    unfinished = Task.objects.all().filter(is_finished=False)

    return "\n".join(str(task) for task in unfinished)

def complete_odd_tasks():
    all_tasks = Task.objects.all()

    for task in all_tasks:
        if task.id % 2 != 0:
            task.is_finished = True
            task.save()

def encode_and_replace(text: str, task_title: str):
    decoded = "".join(chr(ord(el) - 3) for el in text)
    Task.objects.filter(title=task_title).update(description=decoded)

# complete_odd_tasks()
# encode_and_replace("Zdvk#wkh#glvkhv$", "Simple Task")
# print(Task.objects.get(title ='Simple Task') .description)


def get_deluxe_rooms():
    deluxe_rooms = HotelRoom.objects.filter(room_type="Deluxe")
    even_deluxe_rooms = []

    for room in deluxe_rooms:
        if room.id % 2 == 0:
            even_deluxe_rooms.append(str(room))

    return '\n'.join(even_deluxe_rooms)


def increase_room_capacity():
    rooms = HotelRoom.objects.all().order_by("id")
    previous_room_cp = None

    for room in rooms:
        if not room.is_reserved:
            continue
        if previous_room_cp:
            room.capacity += previous_room_cp
        else:
            room.capacity += room.id

        previous_room_cp = room.capacity
        room.save()

def reserve_first_room():
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()


def delete_last_room():
    last_room = HotelRoom.objects.last()
    if last_room.is_reserved:
        last_room.delete()

# print(get_deluxe_rooms())
# reserve_first_room()
# print(HotelRoom.objects.get(room_number=101).is_reserved)


def update_characters():
    all_characters = Character.objects.all()

    for char in all_characters:
        if char.class_name == "Mage":
            char.level += 3
            char.intelligence -= 7
        elif char.class_name == "Warrior":
            char.hit_points /= 2
            char.dexterity += 4
        elif char.class_name == "Assassin" or char.class_name == "Scout":
            char.inventory = "The inventory is empty"

        char.save()

def fuse_characters(first_character: Character, second_character: Character):
    inventory_types = {
        "Mage": "Bow of the Elven Lords, Amulet of Eternal Wisdom",
        "Scout": "Bow of the Elven Lords, Amulet of Eternal Wisdom",
        "Warrior": "Dragon Scale Armor, Excalibur",
        "Assassin": "Dragon Scale Armor, Excalibur"
    }
    mega_char_name = first_character.name + " " + second_character.name
    mega_char_class_name = "Fusion"
    mega_char_level = (first_character.level + second_character.level) // 2
    mega_char_strength = (first_character.strength + second_character.strength) * 1.2
    mega_char_dexterity = (first_character.dexterity + second_character.dexterity) * 1.4
    mega_char_intelligence = (first_character.intelligence + second_character.intelligence) * 1.5
    mega_char_hit_points = first_character.hit_points + second_character.hit_points
    mega_char_inv = inventory_types[first_character.class_name]

    Character.objects.create(
        name=mega_char_name,
        class_name=mega_char_class_name,
        level=mega_char_level,
        strength=mega_char_strength,
        dexterity=mega_char_dexterity,
        intelligence=mega_char_intelligence,
        hit_points=mega_char_hit_points,
        inventory=mega_char_inv
    )

    first_character.delete()
    second_character.delete()

def grand_dexterity():
    Character.objects.all().update(dexterity=30)

def grand_intelligence():
    Character.objects.all().update(intelligence=40)

def grand_strength():
    Character.objects.all().update(strength=50)

def delete_characters():
    Character.objects.filter(inventory="The inventory is empty").delete()


# character1 = Character.objects.create(
#     name="Gandalf",
#     class_name="Mage",
#     level=10,
#     strength=15,
#     dexterity=20,
#     intelligence=25,
#     hit_points=100,
#     inventory="Staff of Magic, Spellbook",
# )
#
# character2 = Character.objects.create(
#     name="Hector",
#     class_name="Warrior",
#     level=12,
#     strength=30,
#     dexterity=15,
#     intelligence=10,
#     hit_points=150,
#     inventory="Sword of Troy, Shield of Protection",
# )
#
# fuse_characters(character1, character2)






