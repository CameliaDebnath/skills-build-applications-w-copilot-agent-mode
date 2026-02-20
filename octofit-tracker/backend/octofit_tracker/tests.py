from django.test import TestCase
from .models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class ModelTests(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name='Marvel', description='Marvel superheroes')
        self.user = User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=self.team)
        self.workout = Workout.objects.create(name='Web Swing', description='Swinging through the city')
        self.activity = Activity.objects.create(user=self.user, activity_type='Swing', duration=30, date=timezone.now().date())
        self.leaderboard = Leaderboard.objects.create(team=self.team, total_points=100)
        self.workout.suggested_for.add(self.user)

    def test_user_team(self):
        self.assertEqual(self.user.team.name, 'Marvel')

    def test_activity_user(self):
        self.assertEqual(self.activity.user.email, 'spiderman@marvel.com')

    def test_workout_suggestion(self):
        self.assertIn(self.user, self.workout.suggested_for.all())

    def test_leaderboard_team(self):
        self.assertEqual(self.leaderboard.team.name, 'Marvel')
