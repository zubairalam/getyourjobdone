from django.core.management.base import BaseCommand
from django.core.management import call_command

from ..commands import fixtures


class Command(BaseCommand):
    """
    Command for Restoring fixtures
    """
    help = "Reset database and load fixtures to Database."

    def load_data(self):
        """
        load data from fixtures.
        """
        for x in fixtures:
            fixture_json_name = str(x) + ".json"
            call_command("loaddata", fixture_json_name)

    def handle(self, *args, **options):
        """
        Handle command event.
        """
        # making this a bit pretty.
        try:
            print("******************************************")
            print("1. Clearing Indexes from ElasticSearch...")
            call_command("clear_index", interactive=False)
            print("\nDone!\n")
            print("******************************************")

            print("******************************************")
            print("2. Deleting Data and Dropping Tables in DB...")
            call_command("reset_db", interactive=False, router="default")
            print("\nDone!\n")
            print("******************************************")

            print("******************************************")
            print("3. Creating and Syncing DB Schema...")
            call_command("syncdb", interactive=False)
            print("\nDone!\n")
            print("******************************************")

            print("******************************************")
            print("4. Loading JSON Fixtures Data into DB...")
            self.load_data()
            print("\nDone!\n")
            print("******************************************")

            print("******************************************")
            print("5. Rebuilding Indexes from ElasticSearch...")
            call_command("rebuild_index", interactive=False)
            print("\nDone!\n")
            print("******************************************")

            print("******************************************")
            print("6. Validating Project code...")
            call_command("validate", interactive=True)
            print("\nDone!\n")
            print("******************************************")

        except(IOError, ValueError, TypeError, AttributeError, ImportError, Exception) as e:
            print("******************************************")
            print("Errors found in resetting data.")
            print(e)
            print("******************************************")
