class Player(pygame.sprite.Sprite):
    def __init__(self, position:list, stats:list):
        super().__init__()
        self.image = ... # загрузка спрайта
        self.rect = ... # хитбокс
        self.HP = ... #кол-во хп (увеличивается с повышением уровня) условно stats[0]
        self.damage = ... # урон (увеличивается с повышением уровня) условно stats[1]
        self.speed = ... #скорость (увеличивается с повышением уровня) условно stats[2]
        self.experience = ... # опыт
        self.level = ... #уровень
        self.position = position #координата персонажа  по оси х, y на текущий момент [0,0]




    def update(self):
        #обработка перемещения  и проверка столкновений персонажа с объектами и стенами
        pass

    def shoot(self):
        #логика стрельбы, генерация снаряда
        pass

    def gain_experience(self):
        #получение опыта, проверка на достижение нужного кол-ва
        pass

    def level_up(self):
        #повышение уровня персонажа
        pass

    def take_damage(self):
        pass

    def die(self):
        pass
