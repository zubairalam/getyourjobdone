import tarfile
import os
import re
import datetime

from django.core.management.base import BaseCommand
from django.core.management import call_command

from ..commands import fixtures


class Command(BaseCommand):
    """
    Command for Backing up fixtures
    The workflow must be improved to allow fixtures to backed up to a singular file.
    Then support extraction to different app fixtures folder path.s
    """
    help = "Backing up JSON fixtures."

    def handle(self, *args, **options):
        fixtures_dir = os.path.join(os.getcwd(), "fixtures")
        self.purge_json(fixtures_dir)
        self.backup_to_json(fixtures_dir)


    def backup_to_json(self, fixtures_dir):
        try:
            print("\n Backing up data from database... ")
            for fixture in fixtures:
                fixture_json_name = str(fixture) + ".json"
                output_filename = os.path.join(fixtures_dir, fixture_json_name)
                output = open(output_filename, "w")
                call_command("dumpdata", fixture, format="json", indent=4, stdout=output)
                output.close()
            print("\n JSON fixtures have been created successfully in %s." % fixtures_dir)
        except (IOError, ValueError):
            print("\n JSON fixtures could not be created in %s." % fixtures_dir)


    def compress_json(self, fixtures_dir):
        try:
            file_name = os.path.join(fixtures_dir, "fixtures") + "-" + datetime.datetime.now().strftime(
                "%d%m%Y%H%M%S") + ".tar.gz"
            print("Compressing JSON files to %s ..." % file_name)
            tar = tarfile.open(file_name, "w:gz")
            tar.add(fixtures_dir, arcname="fixtures")
            tar.close()
            print("\n Compressed file successfully created: %s" % file_name)
        except (IOError, ValueError):
            print("\n Compressed file could not be created in %s" % fixtures_dir)


    def purge(self, directory, pattern):
        for f in os.listdir(directory):
            if re.search(pattern, f):
                os.remove(os.path.join(directory, f))


    def purge_json(self, fixtures_dir):
        pattern = "^.*.json"
        try:
            self.purge(fixtures_dir, pattern)
            print("\n  Deleted JSON file(s).")
        except (IOError, ValueError):
            print("\n No previous JSON file(s) found.")


    def purge_compressed(self, fixtures_dir):
        pattern = "^(fixtures-\d+)[^\d].*.gz"
        try:
            self.purge(fixtures_dir, pattern)
            print("\n Deleted compressed backup file(s).")
        except (IOError, ValueError):
            print("\n No previous compressed backup file(s) found.")

