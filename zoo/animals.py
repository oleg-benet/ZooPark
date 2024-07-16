class Animal:
    def __init__(self, name, habitat, food, activity, size,
                 social, time_day, humanity, file):
        self.name = name
        self.habitat = habitat
        self.food = food
        self.activity = activity
        self.size = size
        self.social = social
        self.time_day = time_day
        self.humanity = humanity
        self.file = file

    def compare(self, answers, asks):
        attributes = [self.habitat, self.food, self.activity, self.size, self.social, self.time_day, self.humanity]
        sum = 0
        for i in range(len(attributes)):
            if attributes[i] == answers[i]:
                sum += asks[i].weight
        return sum

path = 'animal_img/'

deer = Animal('олень','суша','трава','быстрый',
              'крупный','группа','день', 'спокойствие', 'animal_img/deer.jpg')
kangaroo = Animal('кенгуру','суша','трава','быстрый',
              'крупный','группа','ночь', 'вспыльчивость', 'animal_img/kangaroo.jpg')
fox = Animal('лиса','суша','мясо','быстрый',
              'средний','один','день', 'хитрость', 'animal_img/fox.jpg')
lion = Animal('лев','суша','мясо','быстрый',
              'крупный','группа','переход', 'уверенность', 'animal_img/lion.jpg')
wolf = Animal('волк','суша','мясо','быстрый',
              'средний','группа','ночь', 'выносливость', 'animal_img/wolf.jpg')
bear = Animal('медведь','суша','всё','быстрый',
              'крупный','один','день', 'сила', 'animal_img/bear.jpg')
otter = Animal('выдра','суша_вода','мясо','быстрый',
              'малый','один','ночь', 'осторожность', 'animal_img/otter.jpg')
beaver = Animal('бобр','суша_вода','трава','быстрый',
              'средний','группа','ночь', 'трудолюбие', 'animal_img/beaver.jpeg')
capybara = Animal('капибара','суша_вода','трава','медлительный',
              'средний','группа','день', 'доброта', 'animal_img/capybara.jpg')
dolphin = Animal('дельфин','вода','мясо','быстрый',
              'крупный','группа','сутки', 'дружелюбие', 'animal_img/dolphin.jpg')
salmon = Animal('лосось','вода','мясо','быстрый',
              'малый','группа','день', 'мудрость', 'animal_img/salmon.jpg')
falcon = Animal('сокол','воздух','мясо','быстрый',
              'средний','один','переход', 'зоркость', 'animal_img/falcon.jpg')
owl = Animal('сова','воздух','мясо','быстрый',
              'средний','один','ночь', 'рассудительность', 'animal_img/owl.jpg')
raven = Animal('ворон','воздух','всё','быстрый',
              'малый','группа','переход', 'ум', 'animal_img/raven.jpg')
goose = Animal('гусь','воздух','трава','медлительный',
              'средний','группа','день', 'упрямство', 'animal_img/goose.jpg')
butterfly = Animal('бабочка','воздух','трава','медлительный',
              'малый','один','день', 'чувственность', 'animal_img/butterfly.jpg')

animals = [deer, kangaroo, fox, lion, wolf, bear, otter, beaver, capybara,
           dolphin, salmon, falcon, owl, raven, goose, butterfly]

