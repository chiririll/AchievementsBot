import unittest
import requests
import json as j
from os import environ as env


class VkTests(unittest.TestCase):

    def test_confirmation(self):
        json = {
            'type': "confirmation",
            'group_id': 198302424
        }
        req = requests.post('http://127.0.0.1:5000/vk', json=json)
        self.assertEqual(env['VK_CONFIRM'], req.text)

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

    def test_custom_image(self):
        json = j.load(open('data/attachments.json', 'r'))
        req = requests.post('http://127.0.0.1:5000/vk', json=json)
        self.assertEqual('ok', req.text)

    def test_no_name(self):
        json = j.load(open('data/attachments_no_text.json', 'r'))
        req = requests.post('http://127.0.0.1:5000/vk', json=json)
        self.assertEqual('ok', req.text)

    def test_long_name(self):
        json = {
            'type': "message_new",
            'secret': env['VK_SECRET'],
            'group_id': 198302424,
            'object': {
                'message': {
                    'from_id': 241091493,
                    'text': 40 * 'a',
                    'attachments': []
                }
            }
        }
        req = requests.post('http://127.0.0.1:5000/vk', json=json)
        self.assertEqual('ok', req.text)


if __name__ == '__main__':
    unittest.main()
