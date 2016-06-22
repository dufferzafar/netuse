"""
A small wrapper over notify-send - used to create notifications.

Usage:

import notify
notify.send("Title", "Body")
"""

import subprocess


def send(summary, body, **kwargs):
    """
    Wrapper over notify-send.

    Arguments:
    ----------

    summary     - title of the notification
    body        - contents
    urgency     - the urgency level (low, normal, critical).
    expire-time - the timeout in milliseconds at which to expire the notification.
    app-name    - the app name for the icon
    icon        - an icon filename or stock icon to display.
    category    - the notification category.
    hint        - basic extra data to pass. Valid types are int, double, string and byte.
    """

    cmd = ["notify-send", summary, body]

    for arg, val in kwargs.items():
        if val:
            cmd.extend(["-" + arg[0], str(val)])

    # print(" ".join(cmd))
    subprocess.call(cmd)

if __name__ == '__main__':
    send("Title", "Body")
