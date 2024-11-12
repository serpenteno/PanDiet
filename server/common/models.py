from django.db import models

class Tags(models.IntegerChoices):
    SALT = 1
    SUGAR = 2
    FAT = 4
    PROCESSED_FOOD = 8
    ADDITIVES = 16
    GLUTEN = 32
    MILK = 64
    EGGS = 128
    NUTS = 256
    PEANUTS = 512
    SEASAME = 1024
    SOYBEANS = 2048
    CELERY = 4096
    MUSTARD = 8192
    LUPIN = 16384
    FISH = 32768
    CRUSTACEANS = 65536
    MOLLUSCS = 131072
    VEGAN = 262144
    VEGETARIAN = 524288
    PALM_OIL = 1048576