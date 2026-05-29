"""
Tests for AI-related API client methods.

Tests ask_question, get_weekly_summary, get_recommendations,
predict_tomorrow, and what_if_prediction methods.
"""

import unittest.mock

import pytest

from src.services.api_client import HabitronAPIClient


class TestAIEndpoints:
    """Test suite for AI-related API client methods."""

    def setup_method(self):
        """Set up test client."""
        self.client = HabitronAPIClient(
            api_url='http://localhost:5000'
        )

    def test_ask_question_sends_correct_payload(self):
        """Test ask_question sends POST with question in body."""
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = {
            'answer': 'Based on your data, sleep is important.',
            'confidence': 'high'
        }
        mock_response.raise_for_status.return_value = None

        with unittest.mock.patch(
            'requests.post',
            return_value=mock_response
        ) as mock_post:
            result = self.client.ask_question(
                user_key='test-user-key',
                question='Why was I tired last week?'
            )

        expected_url = (
            'http://localhost:5000/api/ai/ask?user_key=test-user-key'
        )
        mock_post.assert_called_once()

        call_kwargs = mock_post.call_args
        assert call_kwargs[0][0] == expected_url

        sent_payload = call_kwargs[1]['json']
        assert 'question' in sent_payload
        assert sent_payload['question'] == 'Why was I tired last week?'

        assert 'answer' in result
        assert 'confidence' in result

    def test_get_weekly_summary_builds_correct_url(self):
        """Test get_weekly_summary sends GET to correct endpoint."""
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = {
            'summary': 'This week you averaged 7.5 hours of sleep.',
            'confidence': 'high'
        }
        mock_response.raise_for_status.return_value = None

        with unittest.mock.patch(
            'requests.get',
            return_value=mock_response
        ) as mock_get:
            result = self.client.get_weekly_summary(
                user_key='test-user-key'
            )

        expected_url = (
            'http://localhost:5000/api/ai/weekly-summary'
            '?user_key=test-user-key'
        )
        mock_get.assert_called_once()

        call_args = mock_get.call_args
        assert call_args[0][0] == expected_url

        assert 'summary' in result

    def test_get_recommendations_builds_correct_url(self):
        """Test get_recommendations sends GET to correct endpoint."""
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = {
            'recommendations': [
                'Try to get 8 hours of sleep.',
                'Reduce screen time in the evening.'
            ],
            'confidence': 'medium'
        }
        mock_response.raise_for_status.return_value = None

        with unittest.mock.patch(
            'requests.get',
            return_value=mock_response
        ) as mock_get:
            result = self.client.get_recommendations(
                user_key='test-user-key'
            )

        expected_url = (
            'http://localhost:5000/api/ai/recommendations'
            '?user_key=test-user-key'
        )
        mock_get.assert_called_once()

        call_args = mock_get.call_args
        assert call_args[0][0] == expected_url

        assert 'recommendations' in result
        assert isinstance(result['recommendations'], list)


class TestPredictionEndpoints:
    """Test suite for prediction API client methods."""

    def setup_method(self):
        """Set up test client."""
        self.client = HabitronAPIClient(
            api_url='http://localhost:5000'
        )

    def test_predict_tomorrow_builds_correct_url(self):
        """Test predict_tomorrow sends GET to correct endpoint."""
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = {
            'prediction': 'good',
            'probability': 0.78,
            'confidence': 'high',
            'explanation': 'Based on your recent habits...'
        }
        mock_response.raise_for_status.return_value = None

        with unittest.mock.patch(
            'requests.get',
            return_value=mock_response
        ) as mock_get:
            result = self.client.predict_tomorrow(
                user_key='test-user-key'
            )

        expected_url = (
            'http://localhost:5000/api/predictions/tomorrow'
            '?user_key=test-user-key'
        )
        mock_get.assert_called_once()

        call_args = mock_get.call_args
        assert call_args[0][0] == expected_url

        assert 'prediction' in result
        assert 'probability' in result

    def test_what_if_prediction_sends_correct_payload(self):
        """Test what_if_prediction sends POST with habits in body."""
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = {
            'prediction': 'good',
            'probability': 0.85,
            'confidence': 'medium',
            'explanation': 'With 8 hours of sleep...'
        }
        mock_response.raise_for_status.return_value = None

        habits = {
            'sleep_hours': 8.0,
            'focus_hours': 5.0,
            'exercise_minutes': 45,
            'mood': 8,
            'screen_time_hours': 2.0,
            'diet_quality': 8
        }

        with unittest.mock.patch(
            'requests.post',
            return_value=mock_response
        ) as mock_post:
            result = self.client.what_if_prediction(
                user_key='test-user-key',
                habits=habits
            )

        expected_url = (
            'http://localhost:5000/api/predictions/what-if'
            '?user_key=test-user-key'
        )
        mock_post.assert_called_once()

        call_kwargs = mock_post.call_args
        assert call_kwargs[0][0] == expected_url

        sent_payload = call_kwargs[1]['json']
        assert 'sleep_hours' in sent_payload
        assert sent_payload['sleep_hours'] == 8.0
        assert 'focus_hours' in sent_payload
        assert sent_payload['focus_hours'] == 5.0

        assert 'prediction' in result
        assert 'probability' in result

    def test_what_if_prediction_handles_partial_habits(self):
        """Test what_if_prediction works with partial habit data."""
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = {
            'prediction': 'good',
            'probability': 0.72,
            'confidence': 'low',
            'explanation': 'Partial data provided...'
        }
        mock_response.raise_for_status.return_value = None

        partial_habits = {
            'sleep_hours': 9.0,
            'exercise_minutes': 60
        }

        with unittest.mock.patch(
            'requests.post',
            return_value=mock_response
        ) as mock_post:
            result = self.client.what_if_prediction(
                user_key='test-user-key',
                habits=partial_habits
            )

        mock_post.assert_called_once()

        sent_payload = mock_post.call_args[1]['json']
        assert 'sleep_hours' in sent_payload
        assert 'exercise_minutes' in sent_payload
        assert len(sent_payload) == 2

        assert result['prediction'] == 'good'
