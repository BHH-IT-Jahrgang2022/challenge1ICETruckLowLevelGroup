import mqttcontroller as con
import logging

mqtt_controller = con.MQTTController()

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-t", "--temperature", type=int)
parser.add_argument("-l", "--logging", type=str)
parser.add_argument("-c", "--challenge", action='store_true')

args = parser.parse_args()
target_temp = args.temperature

log_level = args.logging

if log_level == None:
    logging.basicConfig(level=logging.CRITICAL)
elif log_level == "info":
    logging.basicConfig(level=logging.INFO)
elif log_level == "warning":
    logging.basicConfig(level=logging.WARNING)
elif log_level == "error":
    logging.basicConfig(level=logging.ERROR)

is_challenge = False
if args.challenge != None:
    is_challenge = args.challenge
if is_challenge:
    mqtt_controller.start_challenge(target_temp=target_temp)
else:
    mqtt_controller.start()