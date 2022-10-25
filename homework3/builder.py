from dataclasses import dataclass

import faker


faker = faker.Faker()


class Builder:
    @staticmethod
    def campaign(name=None, text=None):
        @dataclass
        class Topic:
            name: str
            text: str
        if name is None:
            name = faker.bothify('?????????')
        if text is None:
            text = faker.bothify('????????????????')

        return Topic(name=name, text=text)

    @staticmethod
    def segment(name=None):
        @dataclass
        class Topic:
            name: str

        if name is None:
            name = faker.bothify('?????????')

        return Topic(name=name)
