"""
HTTP client for Habitron API backend.

Provides wrapper methods for all API endpoints with error handling.
"""

import requests

from src.config import Config


class HabitronAPIClient:
    """
    Client for communicating with Habitron API backend.

    All methods handle JSON responses and raise exceptions on errors.
    """

    def __init__(self, api_url=None):
        """
        Initialize API client.

        Args:
            api_url (str): Base URL of API server.
        """
        self.api_url = api_url or Config.API_URL
        self.timeout = Config.API_TIMEOUT

    def _make_request(self, method, endpoint, json_data=None):
        """
        Make HTTP request to API endpoint.

        Args:
            method (str): HTTP method (GET or POST).
            endpoint (str): API endpoint path.
            json_data (dict): Optional JSON payload for POST.

        Returns:
            dict: Parsed JSON response.

        Raises:
            Exception: If request fails.
        """
        url = f"{self.api_url}{endpoint}"

        try:
            if method == 'GET':
                response = requests.get(
                    url,
                    timeout=self.timeout
                )
            elif method == 'POST':
                response = requests.post(
                    url,
                    json=json_data,
                    timeout=self.timeout
                )
            else:
                raise ValueError(f"Unsupported method: {method}")

            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            raise Exception(
                f"API request failed: {endpoint} - {str(error)}"
            )

    def get_all_users(self):
        """Retrieve all users."""
        return self._make_request('GET', '/api/users')

    def get_user_by_email(self, email):
        """
        Retrieve a user by email address.

        Args:
            email (str): Email address to look up.

        Returns:
            dict: API response with user data.
        """
        endpoint = f'/api/users/by-email?email={email}'
        return self._make_request('GET', endpoint)

    def create_user(
        self,
        first_name,
        last_name,
        age,
        gender,
        email
    ):
        """
        Create a new user.

        Args:
            first_name (str): User's first name.
            last_name (str): User's last name.
            age (int): User's age.
            gender (str): User's gender.
            email (str): User's email address.

        Returns:
            dict: API response with new user key.
        """
        payload = {
            'first_name': first_name,
            'last_name': last_name,
            'age': age,
            'gender': gender,
            'email': email
        }
        return self._make_request('POST', '/api/users', payload)

    def load_data(self, user_key):
        """
        Load all habit data for a user.

        Args:
            user_key (str): GUID of the user.

        Returns:
            dict: API response with habit records.
        """
        endpoint = f'/api/data/load?user_key={user_key}'
        return self._make_request('GET', endpoint)

    def get_statistics(self, user_key):
        """
        Get basic statistics for a user.

        Args:
            user_key (str): GUID of the user.

        Returns:
            dict: API response with statistics.
        """
        endpoint = f'/api/data/statistics?user_key={user_key}'
        return self._make_request('GET', endpoint)

    def get_correlations(self, user_key):
        """
        Get correlation matrix for a user.

        Args:
            user_key (str): GUID of the user.

        Returns:
            dict: API response with correlation data.
        """
        endpoint = f'/api/analysis/correlations?user_key={user_key}'
        return self._make_request('GET', endpoint)

    def get_trends(self, user_key):
        """
        Get habit trends for a user.

        Args:
            user_key (str): GUID of the user.

        Returns:
            dict: API response with trend data.
        """
        endpoint = f'/api/analysis/trends?user_key={user_key}'
        return self._make_request('GET', endpoint)

    def get_best_worst_days(self, user_key):
        """
        Get best and worst productivity days for a user.

        Args:
            user_key (str): GUID of the user.

        Returns:
            dict: API response with best/worst days.
        """
        endpoint = (
            f'/api/analysis/best-worst-days?user_key={user_key}'
        )
        return self._make_request('GET', endpoint)

    def detect_anomalies(self, user_key, threshold=2.5):
        """
        Detect anomalies for a user.

        Args:
            user_key (str): GUID of the user.
            threshold (float): Z-score threshold (default: 2.5).

        Returns:
            dict: API response with anomaly records.
        """
        endpoint = (
            f'/api/anomaly/detect'
            f'?user_key={user_key}&threshold={threshold}'
        )
        return self._make_request('GET', endpoint)

    def get_habit_by_date(self, user_key, date):
        """
        Retrieve a habit record for a specific user and date.

        Args:
            user_key (str): GUID of the user.
            date (str): Date string in YYYY-MM-DD format.

        Returns:
            dict: API response with 'habit' key containing the
                  record dict, or None if no record exists.
        """
        endpoint = (
            f'/api/database/habit'
            f'?user_key={user_key}&date={date}'
        )
        return self._make_request('GET', endpoint)

    def log_habits(
        self,
        user_key,
        date,
        sleep_hours,
        diet_quality,
        exercise_minutes,
        mood,
        screen_time_hours,
        focus_hours,
        productivity_score
    ):
        """
        Insert or update a habit record for a user.

        If a record for the same date already exists, it will be
        updated. Otherwise, a new record is inserted.

        Args:
            user_key (str): GUID of the user.
            date (str): Date string in YYYY-MM-DD format.
            sleep_hours (float): Hours slept.
            diet_quality (int): Diet quality rating (1-10).
            exercise_minutes (int): Minutes of exercise.
            mood (int): Mood rating (1-10).
            screen_time_hours (float): Recreational screen time in hours.
            focus_hours (float): Hours of focused work or study.
            productivity_score (int): Productivity rating (1-10).

        Returns:
            dict: API response with 'action' ('inserted' or 'updated').
        """
        payload = {
            'user_key': user_key,
            'date': date,
            'sleep_hours': sleep_hours,
            'diet_quality': diet_quality,
            'exercise_minutes': exercise_minutes,
            'mood': mood,
            'screen_time_hours': screen_time_hours,
            'focus_hours': focus_hours,
            'productivity_score': productivity_score
        }
        return self._make_request('POST', '/api/database/insert', payload)

    def ask_question(self, user_key, question):
        """
        Ask an AI question about habit data.

        Args:
            user_key (str): GUID of the user.
            question (str): Natural language question.

        Returns:
            dict: API response with 'answer' and 'confidence'.
        """
        endpoint = f'/api/ai/ask?user_key={user_key}'
        return self._make_request('POST', endpoint, {'question': question})

    def get_weekly_summary(self, user_key):
        """
        Get AI-generated weekly summary.

        Args:
            user_key (str): GUID of the user.

        Returns:
            dict: API response with 'summary' and 'confidence'.
        """
        endpoint = f'/api/ai/weekly-summary?user_key={user_key}'
        return self._make_request('GET', endpoint)

    def get_recommendations(self, user_key):
        """
        Get AI-generated habit recommendations.

        Args:
            user_key (str): GUID of the user.

        Returns:
            dict: API response with 'recommendations' and 'confidence'.
        """
        endpoint = f'/api/ai/recommendations?user_key={user_key}'
        return self._make_request('GET', endpoint)

    def predict_tomorrow(self, user_key):
        """
        Predict tomorrow's productivity.

        Args:
            user_key (str): GUID of the user.

        Returns:
            dict: API response with prediction, probability,
                  confidence, and explanation.
        """
        endpoint = f'/api/predictions/tomorrow?user_key={user_key}'
        return self._make_request('GET', endpoint)

    def what_if_prediction(self, user_key, habits):
        """
        Predict outcome for hypothetical habit values.

        Args:
            user_key (str): GUID of the user.
            habits (dict): Hypothetical habit values with keys:
                           sleep_hours, focus_hours, exercise_minutes,
                           mood, screen_time_hours, diet_quality.

        Returns:
            dict: API response with prediction, probability,
                  confidence, and explanation.
        """
        endpoint = f'/api/predictions/what-if?user_key={user_key}'
        return self._make_request('POST', endpoint, habits)

    def health_check(self):
        """Check if API is running."""
        return self._make_request('GET', '/api/health')


# Global client instance
client = HabitronAPIClient()
