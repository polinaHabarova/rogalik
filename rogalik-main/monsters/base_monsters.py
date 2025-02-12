class BaseMonster(pygame.sprite.Sprite):
    def __init__(self, position:list, stats:list):
        super().__init__()
        self.image = ...  # загрузка спрайта
        self.rect = ...  # хитбокс
        self.HP = ...  # кол-во хп (увеличивается с повышением этажа) условно stats[0]
        self.damage = ...  # урон (увеличивается с повышением этажа) условно stats[1]
        self.speed = ...  # скорость (увеличивается с повышением этажах) условно stats[2]
        self.position = position  # координата монстра  по оси х, y на текущий момент [0,0]


    def update(self):
        #обработка перемещения  и проверка столкновений персонажа с объектами и стенами
        pass


    def take_damage(self):
        pass

    def die(self):
        pass

