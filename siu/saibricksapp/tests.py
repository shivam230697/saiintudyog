from django.test import TestCase
from django.utils import timezone
from .models import AccountModel
from unittest.mock import patch  # Ensure patch is imported


class ModelTests(TestCase):

    @classmethod
    def setUpClass(cls):
        """Runs once before any tests are executed."""
        super().setUpClass()
        cls.date_str = timezone.now().strftime("%Y%m%d")

    @classmethod
    def tearDownClass(cls):
        """Runs once after all tests have been executed."""
        super().tearDownClass()
        # Clean up code if needed (e.g., deleting test data that should not persist)

    def setUp(self):
        """Runs before each test method."""
        # Set up initial data for each test if needed
        pass

    def tearDown(self):
        """Runs after each test method."""
        # Clean up data specific to each test
        AccountModel.objects.all().delete()

    def test_generate_account_id_no_existing_ids(self):
        """Test case when no IDs exist for today."""
        account = AccountModel(name="Test User", address="123 Test St", type="SALE")
        account.save()
        expected_id = f"{self.date_str}001"
        self.assertEqual(account.account_id, expected_id)

    def test_generate_account_id_with_existing_ids(self):
        """Test case to verify correct ID generation with existing IDs."""
        existing_account = AccountModel(name="Existing User", address="456 Existing St", type="MITTI")
        existing_account.account_id = f"{self.date_str}001"
        existing_account.save()

        new_account = AccountModel(name="New User", address="789 New St", type="TURI")
        new_account.save()
        expected_id = f"{self.date_str}002"
        self.assertEqual(new_account.account_id, expected_id)

    def test_generate_account_id_cross_date(self):
        """Test case to ensure IDs handle different dates correctly."""
        account_today = AccountModel(name="Today User", address="321 Today St", type="SALE")
        account_today.save()
        expected_id_today = f"{self.date_str}001"
        self.assertEqual(account_today.account_id, expected_id_today)

        tomorrow = timezone.now() + timezone.timedelta(days=1)
        with self.modify_datetime(tomorrow):
            new_account_tomorrow = AccountModel(name="Tomorrow User", address="654 Tomorrow St", type="MITTI")
            new_account_tomorrow.save()
            expected_id_tomorrow = tomorrow.strftime("%Y%m%d") + '001'
            self.assertEqual(new_account_tomorrow.account_id, expected_id_tomorrow)

    # Helper class to modify the current datetime in tests
    from unittest.mock import patch

    class modify_datetime:
        def __init__(self, new_datetime):
            self.new_datetime = new_datetime

        def __enter__(self):
            self.patcher = patch('django.utils.timezone.now', return_value=self.new_datetime)
            self.patcher.start()

        def __exit__(self, exc_type, exc_value, traceback):
            self.patcher.stop()
