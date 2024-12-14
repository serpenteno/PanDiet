from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    inheritance_AND_logic = models.BooleanField(
        default=False,
        help_text="Zaznacz, jezeli wszystkie obiekty podrzedne musza miec ten tag, aby obiekt nadrzedny go odziedziczyl."
    )

    def __str__(self):
        return self.name

