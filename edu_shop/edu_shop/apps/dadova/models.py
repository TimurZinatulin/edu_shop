# complete
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):

	name = models.CharField('Имя категории', max_length=255)
	slug = models.SlugField(unique=True)
	img = models.ImageField(null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'Categories'


class Course(models.Model):

	category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)

	title = models.CharField('Название курса', max_length=255)
	price = models.BigIntegerField('Цена')
	time = models.CharField('Длительность', max_length=255)
	desc = models.TextField('Описание курса')
	img = models.ImageField('Изображение', max_length=255)
	is_featured = models.BooleanField(default=False, null=True)

	def __str__(self):
		return self.title


class BoughtedCourse(models.Model):

	profile = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

	courses = models.ManyToManyField(Course, blank=True)

	def __str__(self):
		return str(self.profile)


class Balance(models.Model):

	profile = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

	amount = models.BigIntegerField('Баланс:', blank=True)


class Review(models.Model):

	course = models.ForeignKey(Course, on_delete=models.CASCADE)

	author = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
	text = models.TextField('Отзыв о курсе')

	def __str__(self):
		return self.author


class Cart(models.Model):

	owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

	courses = models.ManyToManyField(Course, blank=True)

	def __str__(self):
		return str(self.owner)


class Type(models.Model):

	title = models.CharField('Название типа события', max_length=255)

	def __str__(self):
		return self.title


class Event(models.Model):

	event_type = models.ForeignKey(Type, on_delete=models.PROTECT)

	title = models.CharField('Название события', max_length=255)

	def __str__(self):
		return self.title