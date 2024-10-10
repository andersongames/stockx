import requests

from flask import redirect, session
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def quote(symbol):
    """Look up quote for symbol."""

    # Prepare API request
    symbol = symbol.upper()

    # Brapi API
    url = (f"https://brapi.dev/api/quote/{symbol}")
    params = {
        'token': '4ExJ1BByJ3aSqkBmCnKcCf',
    }

    # Query API
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        results = data["results"][0]
        logo = "https://placehold.co/190"
        if "logourl" in results:
            logo = results["logourl"]
        return {
            "name": results["shortName"],
            "price": results["regularMarketPrice"],
            "symbol": results["symbol"],
            "logo": logo
        }
    else:
        print(f"Request failed with status code {response.status_code}")
        return None
