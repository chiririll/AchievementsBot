from vk_api.keyboard import VkKeyboard


class Button:
    def __init__(self, label, payload=None):
        """
        Class for keyboard button
        :param label: Text on button
        :param payload: payload
        """

        if payload is None:
            payload = {}

        self.label = label
        self.payload = payload


class Keyboard:

    inline = False
    one_time = False

    buttons = [[]]

    def __init__(self, **params):
        """
        Class for universal keyboard
        :param params: keyboard types (inline, one_time)
        """
        if 'inline' in params.keys() and params['inline']:
            self.inline = True
        if 'one_time' in params.keys() and params['one_time']:
            self.one_time = True

    def add_button(self, button: Button):
        self.buttons[-1].append(button)

    def add_line(self):
        self.buttons.append([])

    def add_buttons(self, buttons: list):
        self.buttons = buttons

    def add_buttons_range(self, start, stop, step=1, **params):
        payload = {}
        index_field = None

        if 'payload' in params.keys():
            payload = params['payload']

        if 'index_field' in params.keys():
            index_field = params['index_field']

        # Generating keyboard
        count = 0
        for i in range(start, stop, step):
            if count >= 4:
                self.buttons.append([])
            count += 1
            payload[index_field] = i
            self.buttons[-1].append(Button(str(i), payload))

    def get_vk(self):
        kb = VkKeyboard(self.one_time, self.inline)

        for line in self.buttons:
            for button in line:
                kb.add_button(button.label, payload=button.payload)
            if self.buttons.index(line) != len(self.buttons) - 1:
                kb.add_line()

        return kb.get_keyboard()

    def get_telegram(self):
        pass
