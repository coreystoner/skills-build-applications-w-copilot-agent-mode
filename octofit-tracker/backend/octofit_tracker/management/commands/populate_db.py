from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from octofit_tracker.test_data import test_users, test_teams, test_activities, test_leaderboard, test_workouts

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Clear existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Populate users
        for user_data in test_users:
            User.objects.create(**user_data)

        # Populate teams
        for team_data in test_teams:
            members = team_data.pop('members', [])
            team = Team.objects.create(**team_data)
            team.members = list(User.objects.filter(_id__in=members).values_list('_id', flat=True))
            team.save()

        # Populate activities
        for activity_data in test_activities:
            user_id = activity_data.pop('user')
            activity = Activity.objects.create(user=User.objects.get(_id=user_id), **activity_data)

        # Populate leaderboard
        for leaderboard_data in test_leaderboard:
            user_id = leaderboard_data.pop('user')
            Leaderboard.objects.create(user=User.objects.get(_id=user_id), **leaderboard_data)

        # Populate workouts
        for workout_data in test_workouts:
            Workout.objects.create(**workout_data)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))