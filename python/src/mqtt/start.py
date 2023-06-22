import mqttcontroller as con

mqtt_controller = con.MQTTController()

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-t", "--temperature", type=int)
parser.add_argument("-l", "--logging", type=str)
parser.add_argument("-c", "--challenge", type=str)

args = parser.parse_args()
target_temp = args.temperature

logging_enabled = False
if args.logging != None:
    logging_enabled = args.logging = "enabled"

is_challenge = False
if args.challenge != None:
    is_challenge = args.challenge == "yes" or args.challenge == "y"

if is_challenge:
    mqtt_controller.start_challenge(target_temp=target_temp, logging_enabled=logging_enabled)
else:
    mqtt_controller.start()