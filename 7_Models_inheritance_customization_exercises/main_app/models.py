from datetime import timedelta

from django.db import models
from django.core.exceptions import ValidationError


class BaseCharacter(models.Model):
    name = models.CharField(
        max_length=100,
    )
    description = models.TextField()

    class Meta:
        abstract = True


class Mage(BaseCharacter):
    elemental_power = models.CharField(
        max_length=100,
    )
    spellbook_type = models.CharField(
        max_length=100,
    )


class Assassin(BaseCharacter):
    weapon_type = models.CharField(
        max_length=100,
    )
    assassination_technique = models.CharField(
        max_length=100,
    )


class DemonHunter(BaseCharacter):
    weapon_type = models.CharField(
        max_length=100,
    )
    demon_slaying_ability = models.CharField(
        max_length=100,
    )


class TimeMage(Mage):
    time_magic_mastery = models.CharField(
        max_length=100,
    )
    temporal_shift_ability = models.CharField(
        max_length=100,
    )


class Necromancer(Mage):
    raise_dead_ability = models.CharField(
        max_length=100,
    )


class ViperAssassin(Assassin):
    venomous_strikes_mastery = models.CharField(
        max_length=100,
    )
    venomous_bite_ability = models.CharField(
        max_length=100,
    )


class ShadowbladeAssassin(Assassin):
    shadowstep_ability = models.CharField(
        max_length=100,
    )


class VengeanceDemonHunter(DemonHunter):
    vengeance_mastery = models.CharField(
        max_length=100,
    )
    retribution_ability = models.CharField(
        max_length=100,
    )


class FelbladeDemonHunter(DemonHunter):
    felblade_ability = models.CharField(
        max_length=100,
    )


class UserProfile(models.Model):
    username = models.CharField(
        max_length=70,
        unique=True,
    )
    email = models.EmailField(
        unique=True,
    )
    bio = models.TextField(
        null=True,
        blank=True,
    )

class Message(models.Model):
    sender = models.ForeignKey(
        to="UserProfile",
        related_name="sent_messages",
        on_delete=models.CASCADE,
    )
    receiver = models.ForeignKey(
        to="UserProfile",
        related_name="received_messages",
        on_delete=models.CASCADE,
    )
    content = models.TextField()

    timestamp = models.DateTimeField(
        auto_now_add=True,
    )
    is_read = models.BooleanField(
        default=False,
    )

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def mark_as_unread(self):
        self.is_read = False
        self.save()

    def reply_to_message(self, reply_content, receiver):
        reply_message = Message(sender=self.receiver, receiver=receiver, content=reply_content)
        reply_message.save()
        return reply_message

    def forward_message(self, sender, receiver):
        forward_message = Message(sender=sender, receiver=receiver, content=self.content)
        forward_message.save()
        return forward_message


class StudentIDField(models.PositiveIntegerField):

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value

        return int(value)

# #    second option:
#     def to_python(self, value):
#         try:
#             return int(value)
#         except ValueError:
#             pass  # raise ValidationError("Wrong type")

class Student(models.Model):
    name = models.CharField(
        max_length=100,
    )
    student_id = StudentIDField()


class MaskedCreditCardField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 20
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if not isinstance(value, str):
            raise ValidationError("The card number must be a string")

        if not value.isdigit():
            raise ValidationError("The card number must contain only digits")

        if len(value) != 16:
            raise ValidationError("The card number must be exactly 16 characters long")

        return f"****-****-****-{value[12:]}"


class CreditCard(models.Model):
    card_owner = models.CharField(
        max_length=100,
    )
    card_number = MaskedCreditCardField()


