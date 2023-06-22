import mqttcontroller as con
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-t", "--temperature", type=int)
parser.add_argument("-l", "--logging", type=str)

args = parser.parse_args()
target_temp = args.temperature
logging_string = args.temperature
logging_enabled = logging_string == "enabled"

controller = con.MQTTController()
controller.start_challenge(target_temp=target_temp, logging_enabled=logging_enabled)