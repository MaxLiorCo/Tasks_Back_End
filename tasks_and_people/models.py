from django.db import models
# __str__ method allows us to describe how the model is printed to the user, here it is overwritten

"""
Person class that manages the Person model interactions in the code and its table in the database.
-We don't need an id field since it is automatically generated
-Email must be unique
"""
class Person(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=30, unique=True)
    favoriteProgrammingLanguage = models.CharField(max_length=20)
    activeTaskCount = models.IntegerField(default=0)

    def __str__(self):
        return "Person-> id:%s, name:%s " % (self.id, self.name)

"""
Task class that manages the Task model interactions in the code and its table in the database.
-We don't need an id field since it is automatically generated
-Instead of ownerId, here we save a reference to the whole object.
 In case of owners deletion it automatically deletes all his of tasks
 ForeignKey allows us to create Many-To-One relationships
"""
class Task(models.Model):
    title = models.CharField(max_length=20, default='')
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)
    isDone = models.BooleanField(default=False)  # instead of status: active/done
    details = models.CharField(max_length=200)
    dueDate = models.DateField()

    def __str__(self):
        return "Task-> id:%s, owner name:%s " % (self.id, self.owner.name)  # TODO be more descriptive
