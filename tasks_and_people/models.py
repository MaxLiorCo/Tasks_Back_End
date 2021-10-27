from django.db import models


class Person(models.Model):
    id = models.CharField(max_length=20, primary_key=True) # I assume system id, not necessarily id of length 9
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    favoriteProgrammingLanguage = models.CharField(max_length=20)
    activeTaskCount = models.IntegerField()

    def __str__(self):
        return "Person-> id:%s, name:%s " % (self.id, self.name)

class Task(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    # instead of ownerId, here we save reference to the whole object
    # in case of owners deletion it automatically deletes all his tasks
    # ForeignKey allows us to create Many-To-One relationships
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)
    isDone = models.BooleanField(default=False) # instead of status: active/done
    details = models.CharField(max_length=200)
    dueDate = models.DateField()

    def __str__(self):
        return "Task-> id:%s, owner name:%s " % (self.id, self.owner.name) #TODO be more descriptive
