"""
Tests for API client service.

Tests API client methods and error handling.
"""

import unittest.mock

import pytest

from src.services.api_client import HabitronAPIClient


class TestHabitronAPIClient:
    """Test suite for HabitronAPIClient."""

    def setup_method(self):
        """Set up test client."""
        self.client = HabitronAPIClient(
            api_url='http://localhost:5000'
        )

    def test_client_initialization(self):
        """Test client is initialized correctly."""
        assert self.client.api_url == 'http://localhost:5000'
        assert self.client.timeout > 0

    def test_health_check_url(self):
        """Test health check endpoint URL is correct."""
        # This is a simple validation test
        # In real testing, would need mock or running API
        assert self.client.api_url is not None

    def test_log_habits_builds_correct_payload(self):
        """Test log_habits sends POST with all nine expected keys."""
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = {
            'message': 'Record inserted successfully'
        }
        mock_response.raise_for_status.return_value = None

        with unittest.mock.patch('requests.post', return_value=mock_response) as mock_post:
            self.client.log_habits(
                user_key='test-user-key',
                date='2026-05-08',
                sleep_hours=7.5,
                diet_quality=8,
                exercise_minutes=30,
                mood=7,
                screen_time_hours=2.0,
                focus_hours=4.0,
                productivity_score=8
            )

        expected_url = 'http://localhost:5000/api/database/insert'
        mock_post.assert_called_once()

        call_kwargs = mock_post.call_args
        assert call_kwargs[0][0] == expected_url

        sent_payload = call_kwargs[1]['json']
        expected_keys = [
            'user_key',
            'date',
            'sleep_hours',
            'diet_quality',
            'exercise_minutes',
            'mood',
            'screen_time_hours',
            'focus_hours',
            'productivity_score'
        ]
        for key in expected_keys:
            assert key in sent_payload

    def test_get_habit_by_date_builds_correct_url(self):
        """Test get_habit_by_date sends GET to correct endpoint."""
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = {
            'habit': {
                'key': 'habit-key',
                'user_key': 'test-user-key',
                'date': '2026-05-08',
                'sleep_hours': 7.5,
                'diet_quality': 8,
                'exercise_minutes': 30,
                'mood': 7,
                'screen_time_hours': 2.0,
                'focus_hours': 4.0,
                'productivity_score': 8
            }
        }
        mock_response.raise_for_status.return_value = None

        with unittest.mock.patch(
            'requests.get',
            return_value=mock_response
        ) as mock_get:
            result = self.client.get_habit_by_date(
                user_key='test-user-key',
                date='2026-05-08'
            )

        expected_url = (
            'http://localhost:5000/api/database/habit'
            '?user_key=test-user-key&date=2026-05-08'
        )
        mock_get.assert_called_once()

        call_args = mock_get.call_args
        assert call_args[0][0] == expected_url
        assert result['habit'] is not None
        assert result['habit']['date'] == '2026-05-08'

    def test_get_habit_by_date_returns_none_for_missing(self):
        """Test get_habit_by_date returns habit=None for missing date."""
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = {'habit': None}
        mock_response.raise_for_status.return_value = None

        with unittest.mock.patch(
            'requests.get',
            return_value=mock_response
        ) as mock_get:
            result = self.client.get_habit_by_date(
                user_key='test-user-key',
                date='1999-01-01'
            )

        assert result['habit'] is None
