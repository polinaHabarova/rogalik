from base_monsters import BaseMonster


class Goblin(BaseMonster):
    def __init__(self, position, floor):
        stats = [
            10 * (1.2 * floor), #хп
            10, #урон
            10, #скорость(цифры везде условные)
        ]# с каждым новым этажом можно увеличивать статы на какой-то процент
        super().__init__(position, stats)

    # другие нужные функции либо новые, либо переопределенные


class Skelet(BaseMonster):
    def __init__(self, position, floor):
        stats = [
            5 * (1.1 * floor),  # хп
            5,  # урон
            5,  # скорость(цифры везде условные)
        ]  # с каждым новым этажом можно увеличивать статы на какой-то процент
        super().__init__(position, stats)

    # другие нужные функции либо новые, либо переопределенные