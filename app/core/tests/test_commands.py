"""
Test custom Django management commands.
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# patch is used to mock the behavior of the code that we don't want to test
# in this case, we are mocking the behavior of the database
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    # patched_check is the mock object that we are patching
    # it is used to simulate the behavior of the database
    # in this case, we are patching the check method of the Command class
    # and we are saying that it should return True
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""

        # side_effect is used to simulate the behavior of the database
        # in this case, we are saying that it should raise an error 5 times
        # and then return True. In this case, the first 2 times it will raise
        # a Psycopg2Error, the next 3 times it will raise an OperationalError
        # and the last time it will return True.
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
