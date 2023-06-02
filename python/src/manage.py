#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import thermo.databasemanager as dbm
import thermo.controller as con
import thermo.mqttbroker as mqtt


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

def start_controller():
    controller = con.Controller(dbm.DatabaseManager(), mqtt.Broker())
    controller.start_mqtt()

if __name__ == '__main__':
    start_controller()
    main()
