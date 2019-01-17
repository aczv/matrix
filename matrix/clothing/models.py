from django.db import models


class Branch(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "branches"

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Responsible(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Cloth(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "clothes"

    def __str__(self):
        return self.name


class Reservation(models.Model):
    branch = models.ForeignKey(Branch, models.PROTECT)
    department = models.ForeignKey(Department, models.PROTECT, blank=True, null=True)
    responsible = models.ForeignKey(Responsible, models.PROTECT, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True)

    cloth = models.ForeignKey(Cloth, models.PROTECT)
    quantity = models.IntegerField()

    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'
    GENDER_UNI = 'U'
    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_UNI, 'Uni'),
    )
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True)

    SIZE_S = 'S'
    SIZE_M = 'M'
    SIZE_L = 'L'
    SIZE_XL = 'XL'
    SIZE_CHOICES = (
        (SIZE_S, 'Small'),
        (SIZE_M, 'Medium'),
        (SIZE_L, 'Large'),
        (SIZE_XL, 'Extra Large'),
    )
    size = models.CharField(max_length=20, choices=SIZE_CHOICES, blank=True)

    note = models.CharField(max_length=100, blank=True)
    # confirmed = models.BooleanField(default=False)

    def __str__(self):
        return "%s - %s" % (self.branch.name, self.cloth.name)
