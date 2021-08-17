import unittest
from io import BytesIO

from Achievement import *


class AchievementTests(unittest.TestCase):

    def test_Default(self):
        self.__test_style("Default.achst", "Default")

    def test_Magical(self):
        self.__test_style("Magical.achst", "Magical")

    def test_Layout(self):
        self.__test_style("Layout.achs")

    def __test_style(self, style: str, name="Testing", icon=None, description=None, lang="ENG"):
        st = Style(open(f"Styles/{style}", 'rb'), lang)
        ach = Achievement(st, name, icon, description)
        f = ach.generate()

        self.assertIs(type(f), BytesIO)

        saver = open(f"Images/styles/{style.split('.', 1)[0].lower()}.png", 'wb')
        saver.write(f.read())
        saver.close()


if __name__ == '__main__':
    unittest.main()
