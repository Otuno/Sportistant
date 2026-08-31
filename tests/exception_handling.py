import requests

class SportsAPIClient:
    # Existing methods ...

    def _fetch_data(self, url: str) -> dict:
        """Exception Handling: Manages network failures, timeouts, and HTTP errors."""
        try:
            response = requests.get(url, timeout=8)
            response.raise_for_status()
            return response.json()
        except requests.Timeout:
            print("[Error] API request timed out.")
            return None

        except requests.HTTPError as http_err:
            print(f"[Error] HTTP error occurred: {http_err}")
            return None

        except requests.RequestException as req_err:
            print(f"[Error] Network request failed: {req_err}")
            return None
            
        except ValueError:  # JSONDecodeError
            print("[Error] Failed to parse JSON response from server.")
            return None