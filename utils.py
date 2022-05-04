
import argparse
from API.API_interface import Roboat_API
def setup_password():
    # password should not be writtin in clear
    # this is an attempt to hide it
    parser = argparse.ArgumentParser("main Program")
    parser.add_argument("--password", help="Password for connection", type=str)
    args = parser.parse_args()
    Roboat_API.password = args.password
    Roboat_API.debug = True