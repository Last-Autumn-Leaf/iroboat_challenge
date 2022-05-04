from API.API_interface import Roboat_API
import argparse

def main():
    api_caller=Roboat_API()




if __name__ == '__main__':
    # password should not be writtin in clear
    # this is an attempt to hide it
    parser = argparse.ArgumentParser("main Program")
    parser.add_argument("--password", help="Password for connection", type=str)
    args = parser.parse_args()
    Roboat_API.password=args.password
    Roboat_API.debug=True

    main()