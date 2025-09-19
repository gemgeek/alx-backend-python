#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized # type: ignore
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that org returns the correct value and calls get_json once"""
        # Arrange: fake return value
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        # Act: create client and call org
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert: org property returns expected payload
        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test that _public_repos_url returns expected URL from mocked org"""
        test_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}

        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = test_payload
            client = GithubOrgClient("google")
            result = client._public_repos_url

            self.assertEqual(result, test_payload["repos_url"])  

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns correct repo list"""
        payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = payload

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "https://fake.url"
            client = GithubOrgClient("google")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2"])
            mock_get_json.assert_called_once_with("https://fake.url")
            mock_url.assert_called_once()


if __name__ == '__main__':
    unittest.main()          
