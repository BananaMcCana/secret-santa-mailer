import unittest
import re
import sys
import os

# Import the is_email_valid function
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from secret_santa.secret_santa_mailer import is_email_valid

class TestEmailValidation(unittest.TestCase):
    def test_valid_emails(self):
        """Test various valid email address formats."""
        valid_emails = [
            "test@example.com",
            "user@domain.co.uk",
            "user.name@domain.com",
            "user+label@domain.com",
            "user123@domain.com",
            "user_name@domain-host.com",
            "firstname.lastname@sub.domain.com",
            "12345@domain.com",
            "email@subdomain.domain.info",
        ]
        
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(is_email_valid(email), f"Email should be valid: {email}")

    def test_invalid_emails(self):
        """Test various invalid email address formats."""
        invalid_emails = [
            "",                         # Empty string
            "plainaddress",            # Missing @ symbol
            "@domain.com",             # Missing username
            "user@",                   # Missing domain
            "user@.com",               # Domain starts with dot
            "user@domain",             # Missing top-level domain
            "user name@domain.com",    # Contains space
            "user@domain..com",        # Double dots in domain
            "@user@domain.com",        # Multiple @ symbols
            ".user@domain.com",        # Username starts with dot
            "user.@domain.com",        # Username ends with dot
            "user..name@domain.com",   # Double dots in username
            "user@domain com",         # Space in domain
            "user@domain.c",           # Single character TLD
            "user@-domain.com",        # Domain starts with hyphen
            "user@domain-.com",        # Domain ends with hyphen
            "\nuser@domain.com",       # Contains newline
            "\tuser@domain.com",       # Contains tab
        ]

        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(is_email_valid(email), f"Email should be invalid: {email}")

    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        edge_cases = [
            ("a@b.c.d.e.f.g", True),    # Multiple subdomains
            ("a@b.com", True),           # Minimal valid email
            ("a" * 64 + "@domain.com", True),  # Long username
            ("user@" + "a" * 250 + ".com", True),  # Long domain name
            (None, False),               # None value
            (123, False),                # Non-string input
            (True, False),               # Boolean input
        ]

        for email, expected in edge_cases:
            with self.subTest(email=email):
                if isinstance(email, str):
                    result = is_email_valid(email)
                else:
                    with self.assertRaises((AttributeError, TypeError)):
                        is_email_valid(email)
                    continue
                self.assertEqual(result is not None, expected, 
                               f"Email validation failed for {email}, expected {expected}")

if __name__ == '__main__':
    unittest.main()