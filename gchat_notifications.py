# This is a Python implementation for sending Google Chat notifications
# It works only on my own GChat channel
# To make it work globally the URL must be passed (it is the webhook to the target channel)

import sys

from json import dumps
from httplib2 import Http


def main(status_message):
    """Google Chat incoming webhook quickstart."""
    url = "https://chat.googleapis.com/v1/spaces/AAAAzxPyOJ4/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=VN-HvyYZRrnSK8Qh9k5gYEcbBnhuQUOtiaYbvV4hGRQ"  # noqa: E501
    app_message = {"text": status_message}
    message_headers = {"Content-Type": "application/json; charset=UTF-8"}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method="POST",
        headers=message_headers,
        body=dumps(app_message),
    )
    # print(response)


if __name__ == "__main__":
    status_message = sys.argv[1] if len(sys.argv) > 1 else "No status received"
    main(status_message)
