

from djongo import models

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    class Meta:
        db_table = 'teams'
    def __str__(self):
        return self.name

class EmbeddedTeam(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    class Meta:
        abstract = True

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    team = models.EmbeddedField(model_container=EmbeddedTeam, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = 'users'
    def __str__(self):
        return self.email

class EmbeddedUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    class Meta:
        abstract = True

class Activity(models.Model):
    user = models.EmbeddedField(model_container=EmbeddedUser)
    activity_type = models.CharField(max_length=100)
    duration = models.PositiveIntegerField(help_text='Duration in minutes')
    date = models.DateField()
    class Meta:
        db_table = 'activities'
    def __str__(self):
        return f"{self.user.email} - {self.activity_type}"

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    # suggested_for omitted for EmbeddedModelField simplicity
    class Meta:
        db_table = 'workouts'
    def __str__(self):
        return self.name

class EmbeddedTeamRef(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        abstract = True

class Leaderboard(models.Model):
    team = models.EmbeddedField(model_container=EmbeddedTeamRef)
    total_points = models.PositiveIntegerField(default=0)
    class Meta:
        db_table = 'leaderboard'
    def __str__(self):
        return f"{self.team.name} - {self.total_points}"
