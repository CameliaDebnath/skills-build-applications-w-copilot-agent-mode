from django.core.management.base import BaseCommand
from octofit_tracker.models import Team, User, Activity, Workout, Leaderboard
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Populate the database with test data for Octofit Tracker'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Populating database with test data...'))

        # Create Teams
        teams = []
        team_dicts = []
        for tname in ['Alpha', 'Beta', 'Gamma']:
            team, _ = Team.objects.get_or_create(name=tname, defaults={'description': f'{tname} team'})
            teams.append(team)
            team_dicts.append({'name': team.name, 'description': team.description})

        # Create Users with embedded team info
        users = []
        for i in range(1, 6):
            idx = random.randint(0, len(team_dicts)-1)
            team_dict = team_dicts[idx]
            email = f'user{i}@octofit.com'
            User.objects.filter(email=email).delete()
            user = User.objects.create(
                name=f'User{i}',
                email=email,
                team=team_dict,
                is_active=True
            )
            users.append(user)

        # Create Workouts
        workouts = []
        for wname in ['Cardio Blast', 'Strength Builder', 'Yoga Flow']:
            Workout.objects.filter(name=wname).delete()
            workout = Workout.objects.create(
                name=wname,
                description=f'{wname} workout'
            )
            workouts.append(workout)

        # Assign suggested workouts (skipped, no suggested_for field in Workout)

        # Create Activities
        for user in users:
            for _ in range(3):
                Activity.objects.create(
                    user={'name': user.name, 'email': user.email},
                    activity_type=random.choice(['Running', 'Cycling', 'Swimming']),
                    duration=random.randint(20, 90),
                    date=timezone.now().date()
                )

        # Create Leaderboard entries
            for team_dict in team_dicts:
                total_points = sum(random.randint(10, 100) for _ in range(3))
                Leaderboard.objects.filter(team=team_dict).delete()
                Leaderboard.objects.create(team=team_dict, total_points=total_points)

        self.stdout.write(self.style.SUCCESS('Database population complete.'))
