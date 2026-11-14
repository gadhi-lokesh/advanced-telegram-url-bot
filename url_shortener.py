
import requests
from urllib.parse import urlsplit


def validate_url(url):

    if not isinstance(url, str):
        return False

    url = url.strip()

    if len(url) > 5000 or any(ch.isspace() for ch in url):
        return False

    try:
        parsed = urlsplit(url)

        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.hostname)
            and "." in parsed.hostname
            and parsed.username is None
            and parsed.password is None
        )

    except ValueError:
        return False


def cleanuri_api(url):

    endpoint = "https://cleanuri.com/api/v1/shorten"

    response = requests.post(
        endpoint,
        data={"url": url},
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    short_url = data.get("result_url")

    if not short_url:
        raise ValueError(data.get("error", "CleanURI failed"))

    return short_url


def onept_api(url):

    endpoint = (
        "https://csclub.uwaterloo.ca/"
        "~phthakka/1pt-express/addURL"
    )

    response = requests.post(
        endpoint,
        data={"long": url},
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    short_code = data.get("short")

    if not short_code:
        raise ValueError("1pt did not return a short code")

    return "https://1pt.co/" + short_code



def isgd_api(url):
    endpoint = "https://is.gd/create.php"

    response = requests.get(
        endpoint,
        params={"format": "json", "url": url},
        timeout=15
    )

    response.raise_for_status()
    data = response.json()

    if "shorturl" not in data:
        raise ValueError(
            data.get("errormessage", "is.gd failed")
        )

    return data["shorturl"]


def vgd_api(url):
    endpoint = "https://v.gd/create.php"

    response = requests.get(
        endpoint,
        params={"format": "json", "url": url},
        timeout=15
    )

    response.raise_for_status()
    data = response.json()

    if "shorturl" not in data:
        raise ValueError(
            data.get("errormessage", "v.gd failed")
        )

    return data["shorturl"]


def shorten_url(long_url):
    long_url = long_url.strip()

    if not validate_url(long_url):
        raise ValueError("Invalid HTTP or HTTPS URL.")

    providers = [
        ("is.gd", isgd_api),
        ("v.gd", vgd_api),
        ("CleanURI", cleanuri_api)
    ]

    errors = []

    for name, function in providers:
        try:
            short_url = function(long_url)

            if not validate_url(short_url):
                raise ValueError("Invalid API response URL")

            print(f"[SUCCESS] {name}")

            return {
                "success": True,
                "short_url": short_url,
                "provider": name
            }

        except (requests.RequestException, ValueError) as error:
            print(f"[FAILED] {name}: {error}")
            errors.append(f"{name}: {error}")

    return {
        "success": False,
        "errors": errors
    }
