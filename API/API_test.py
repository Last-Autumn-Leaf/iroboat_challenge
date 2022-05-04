import unittest
from API.API_interface import Roboat_API
import argparse
class Roboat_API_Test_failed(unittest.TestCase):
    def setUp(self) -> None:
        self.api_caller=Roboat_API(1, 1, 1)
    def test_failed_login(self):
        self.assertEqual(self.api_caller.token, self.api_caller.INVALID_TOKEN)  # add assertion here
    def test_failed_infoFast(self):
        self.assertEqual(self.api_caller.InfosFast(), self.api_caller.INVALID_RESP)
    def test_failed_infoSlow(self):
        self.assertEqual(self.api_caller.InfosSlow(), self.api_caller.INVALID_RESP)
    def test_failed_boatAction(self):
        TS = 1651686030000
        action = [{
            "type": "heading",
            "values": {
                "deg": 200,
                "autoTwa": True}}]
        self.assertEqual(self.api_caller.BoatActions(TS, action), self.api_caller.INVALID_RESP)

class Roboat_API_Test_success(unittest.TestCase):
    def setUp(self) -> None:
        self.api_caller=Roboat_API(531, 1, 1)
    def test_succeed_login(self):
        self.assertNotEqual(self.api_caller.token, self.api_caller.INVALID_TOKEN)
    def test_succeed_InfosFast(self):
        self.assertEqual(self.api_caller.InfosFast()['rc'],'ok')
    def test_succeed_InfosSlow(self):
        self.assertEqual(self.api_caller.InfosSlow()['rc'],'ok')
    def test_succeed_BoatAction(self):
        TS = 1651686030000
        action = [{
            "type": "heading",
            "values": {
                "deg": 200,
                "autoTwa": True}}]
        self.assertEqual(self.api_caller.BoatActions(TS, action)['rc'],'ok')

if __name__ == '__main__':
    parser = argparse.ArgumentParser("unittest for API_interface")
    parser.add_argument("--password", help="Password for connection", type=str)
    args = parser.parse_args()
    Roboat_API.password=args.password
    runner = unittest.TextTestRunner()
    itersuite = unittest.TestLoader().loadTestsFromTestCase(Roboat_API_Test_failed)
    runner.run(itersuite)
