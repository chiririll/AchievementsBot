import unittest
import requests
from os import environ as env


class VkTests(unittest.TestCase):

    def test_confirmation(self):
        json = {
            'type': "confirmation",
            'group_id': 198302424
        }
        req = requests.post('http://127.0.0.1:5000/vk', json=json)
        self.assertEqual("23b6ec88", req.json()['code'])

    def test_wrong_secret(self):
        json = {
            'type': "message_new",
            'secret': "no",
            'group_id': 198302424
        }
        req = requests.post('http://127.0.0.1:5000/vk', json=json)
        self.assertEqual("not vk", req.text)

    def test_generator(self):
        json = {
            'type': "message_new",
            'secret': env['VK_SECRET'],
            'group_id': 198302424,
            'object': {
                'message': {
                    'from_id': 241091493,
                    'text': "test",
                    'attachments': []
                }
            }
        }
        req = requests.post('http://127.0.0.1:5000/vk', json=json)
        self.assertEqual('ok', req.text)


if __name__ == '__main__':
    unittest.main()
