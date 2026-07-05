#!/usr/bin/env python3
import json, re, os

SRC = "/Volumes/Sistema/GitHub/publico/cal/2026/en"
DST = "/Volumes/Sistema/GitHub/publico/cal/2026/ru"

tiempo_map = {
    "Christmas Time": "Рождественское время", "Ordinary Time": "Обычное время",
    "Lent": "Великий пост", "Easter Time": "Пасхальное время",
    "Holy Week": "Страстная неделя", "Paschal Triduum": "Пасхальное триденствие",
    "Advent": "Адвент",
}

dia_sem_map = {
    "Monday": "Понедельник", "Tuesday": "Вторник", "Wednesday": "Среда",
    "Thursday": "Четверг", "Friday": "Пятница", "Saturday": "Суббота",
    "Sunday": "Воскресенье", "Lunes": "Понедельник",
}

rank_map = {
    "Solemnity": "Торжество", "Feast": "Праздник",
    "Obligatory Memorial": "Обязательное воспоминание",
    "Optional Memorial": "Факультативное воспоминание",
    "Memorial": "Воспоминание", "Commemoration": "Поминовение",
}

color_map = {
    "White": "Белый", "Green": "Зеленый", "Red": "Красный",
    "Violet": "Фиолетовый", "Purple": "Фиолетовый",
    "Pink": "Розовый", "Rose": "Розовый", "Black": "Черный",
}

day_ru = {"Monday":"Понедельник","Tuesday":"Вторник","Wednesday":"Среда",
          "Thursday":"Четверг","Friday":"Пятница","Saturday":"Суббота","Sunday":"Воскресенье"}

FEST_TR = {
"Holy Mary, Mother of God": "Святая Мария, Богородица",
"Saints Basil the Great and Gregory of Nazianzus, bishops and doctors of the Church": "Святые Василий Великий и Григорий Назианзин, епископы и учители Церкви",
"Saturday of the II Week of Christmas": "Суббота II седмицы Рождества",
"The Most Holy Name of Jesus": "Пресвятое Имя Иисуса",
"The Epiphany of the Lord": "Богоявление Господне",
"Monday after the Epiphany": "Понедельник после Богоявления",
"Tuesday after the Epiphany": "Вторник после Богоявления",
"Wednesday after the Epiphany": "Среда после Богоявления",
"Saint Raymond of Penyafort, priest": "Святой Раймонд Пеньяфортский, священник",
"Thursday after the Epiphany": "Четверг после Богоявления",
"Friday after the Epiphany": "Пятница после Богоявления",
"Saturday after the Epiphany": "Суббота после Богоявления",
"The Baptism of the Lord": "Крещение Господне",
"Saint Hilary, bishop and doctor of the Church": "Святой Иларий, епископ и учитель Церкви",
"Saint Anthony, abbot": "Святой Антоний, аббат",
"Saint Fabian, pope and martyr": "Святой Фабиан, папа и мученик",
"Saint Sebastian, martyr": "Святой Себастьян, мученик",
"Saint Agnes, virgin and martyr": "Святая Агнесса, дева и мученица",
"Saint Vincent, deacon and martyr": "Святой Викентий, диакон и мученик",
"Saint Francis de Sales, bishop and doctor of the Church": "Святой Франциск Сальский, епископ и учитель Церкви",
"Saints Timothy and Titus, bishops": "Святые Тимофей и Тит, епископы",
"Saint Angela Merici, virgin": "Святая Анжела Меричи, дева",
"Saint Thomas Aquinas, priest and doctor of the Church": "Святой Фома Аквинский, священник и учитель Церкви",
"Saint John Bosco, priest": "Святой Иоанн Боско, священник",
"The Presentation of the Lord": "Сретение Господне",
"Saint Blase, bishop and martyr": "Святой Власий, епископ и мученик",
"Saint Ansgar, bishop": "Святой Ансгар, епископ",
"Saint Agatha, virgin and martyr": "Святая Агата, дева и мученица",
"Saints Paul Miki and Companions, martyrs": "Святые Павел Мики и сподвижники, мученики",
"Saint Scholastica, virgin": "Святая Схоластика, дева",
"Our Lady of Lourdes": "Богородица Лурдская",
"Saints Cyril, monk, and Methodius, bishop": "Святые Кирилл, монах, и Мефодий, епископ",
"The Seven Holy Founders of the Servite Order": "Семь святых основателей Ордена сервитов",
"Saint Peter Damian, bishop and doctor of the Church": "Святой Петр Дамиан, епископ и учитель Церкви",
"Saint Polycarp, bishop and martyr": "Святой Поликарп, епископ и мученик",
"Saint Casimir": "Святой Казимир",
"Saints Perpetua and Felicity, martyrs": "Святые Перпетуя и Фелицитата, мученицы",
"Saint Frances of Rome, religious": "Святая Франциска Римская, монахиня",
"Saint Patrick, bishop": "Святой Патрик, епископ",
"Saint Cyril of Jerusalem, bishop and doctor of the Church": "Святой Кирилл Иерусалимский, епископ и учитель Церкви",
"Saint Joseph, Spouse of the Blessed Virgin Mary": "Святой Иосиф, Обручник Пресвятой Девы Марии",
"Saint Turibius of Mogrovejo, bishop": "Святой Турибий Могровехский, епископ",
"The Annunciation of the Lord": "Благовещение Господне",
"Easter Sunday of the Resurrection of the Lord": "Пасхальное воскресенье Воскресения Господня",
"Monday within the Octave of Easter": "Понедельник в Октаве Пасхи",
"Tuesday within the Octave of Easter": "Вторник в Октаве Пасхи",
"Wednesday within the Octave of Easter": "Среда в Октаве Пасхи",
"Thursday within the Octave of Easter": "Четверг в Октаве Пасхи",
"Friday within the Octave of Easter": "Пятница в Октаве Пасхи",
"Saturday within the Octave of Easter": "Суббота в Октаве Пасхи",
"Saint Martin I, pope and martyr": "Святой Мартин I, папа и мученик",
"Saint Anselm, bishop and doctor of the Church": "Святой Ансельм, епископ и учитель Церкви",
"Saint George, martyr": "Святой Георгий, мученик",
"Saint Adalbert, bishop and martyr": "Святой Адальберт, епископ и мученик",
"Saint Fidelis of Sigmaringen, priest and martyr": "Святой Фиделий Зигмарингенский, священник и мученик",
"Saint Mark, evangelist": "Святой Марк, евангелист",
"Saint Peter Chanel, priest and martyr": "Святой Петр Шанель, священник и мученик",
"Saint Louis Mary Grignion de Montfort, priest": "Святой Людовик Мария Гриньон де Монфор, священник",
"Saint Catherine of Siena, virgin and doctor of the Church": "Святая Екатерина Сиенская, дева и учитель Церкви",
"Saint Pius V, pope": "Святой Пий V, папа",
"Saint Joseph the Worker": "Святой Иосиф Труженик",
"Saint Athanasius, bishop and doctor of the Church": "Святой Афанасий, епископ и учитель Церкви",
"Saints Nereus and Achilleus, martyrs": "Святые Нерей и Ахилл, мученики",
"Saint Pancras, martyr": "Святой Панкратий, мученик",
"Our Lady of Fatima": "Богородица Фатимская",
"Saint Matthias, apostle": "Святой Матфий, апостол",
"The Ascension of the Lord": "Вознесение Господне",
"Saint John I, pope and martyr": "Святой Иоанн I, папа и мученик",
"Saint Bernardine of Siena, priest": "Святой Бернардин Сиенский, священник",
"Saint Christopher Magallanes, priest, and companions, martyrs": "Святой Христофор Магальянес, священник, и сподвижники, мученики",
"Saint Rita of Cascia, religious": "Святая Рита Кашийская, монахиня",
"Pentecost Sunday": "Пятидесятница",
"The Blessed Virgin Mary, Mother of the Church": "Пресвятая Дева Мария, Матерь Церкви",
"Saint Philip Neri, priest": "Святой Филипп Нери, священник",
"Saint Augustine of Canterbury, bishop": "Святой Августин Кентерберийский, епископ",
"Saint Paul VI, pope": "Святой Павел VI, папа",
"The Most Holy Trinity": "Пресвятая Троица",
"Saint Justin, martyr": "Святой Иустин, мученик",
"Saints Marcellinus and Peter, martyrs": "Святые Маркеллин и Петр, мученики",
"Saints Charles Lwanga and Companions, martyrs": "Святые Карл Лванга и сподвижники, мученики",
"Saint Boniface, bishop and martyr": "Святой Бонифаций, епископ и мученик",
"Saint Norbert, bishop": "Святой Норберт, епископ",
"The Most Holy Body and Blood of Christ (Corpus Christi)": "Пресвятые Тело и Кровь Христовы (Corpus Christi)",
"Saint Ephrem, deacon and doctor of the Church": "Святой Ефрем, диакон и учитель Церкви",
"Saint Barnabas, apostle": "Святой Варнава, апостол",
"The Most Sacred Heart of Jesus": "Пресвященное Сердце Иисуса",
"The Immaculate Heart of the Blessed Virgin Mary": "Непорочное Сердце Пресвятой Девы Марии",
"Saint Romuald, abbot": "Святой Ромуальд, аббат",
"Saint Paulinus of Nola, bishop": "Святой Павлин Ноланский, епископ",
"Saints John Fisher, bishop, and Thomas More, martyrs": "Святые Иоанн Фишер, епископ, и Фома Мор, мученики",
"The Nativity of Saint John the Baptist": "Рождество святого Иоанна Крестителя",
"Saint Cyril of Alexandria, bishop and doctor of the Church": "Святой Кирилл Александрийский, епископ и учитель Церкви",
"Saints Peter and Paul, apostles": "Святые Петр и Павел, апостолы",
"The First Martyrs of the Holy Roman Church": "Первые мученики Святой Римской Церкви",
"Saint Junípero Serra, priest": "Святой Хуниперо Серра, священник",
"Saint Thomas, apostle": "Святой Фома, апостол",
"Saint Elizabeth of Portugal": "Святая Елизавета Португальская",
"Saint Maria Goretti, virgin and martyr": "Святая Мария Горетти, дева и мученица",
"Saint Augustine Zhao Rong, priest, and companions, martyrs": "Святой Августин Чжао Жун, священник, и сподвижники, мученики",
"Saint Benedict, abbot": "Святой Бенедикт, аббат",
"Saint Henry": "Святой Генрих",
"Saint Camillus de Lellis, priest": "Святой Камилл де Леллис, священник",
"Saint Bonaventure, bishop and doctor of the Church": "Святой Бонавентура, епископ и учитель Церкви",
"Our Lady of Mount Carmel": "Богородица Кармельская",
"Saint Apollinaris, bishop and martyr": "Святой Аполлинарий, епископ и мученик",
"Saint Lawrence of Brindisi, priest and doctor of the Church": "Святой Лаврентий Бриндизийский, священник и учитель Церкви",
"Saint Mary Magdalene": "Святая Мария Магдалина",
"Saint Bridget, religious": "Святая Бригитта, монахиня",
"Saint Sharbel Makhlūf, priest": "Святой Шарбель Махлуф, священник",
"Saint James, apostle": "Святой Иаков, апостол",
"Saints Martha, Mary and Lazarus": "Святые Марфа, Мария и Лазарь",
"Saint Peter Chrysologus, bishop and doctor of the Church": "Святой Петр Хрисолог, епископ и учитель Церкви",
"Saint Ignatius of Loyola, priest": "Святой Игнатий Лойола, священник",
"Saint Alphonsus Mary de Liguori, bishop and doctor of the Church": "Святой Альфонс Мария Лигуори, епископ и учитель Церкви",
"Saint John Vianney, priest": "Святой Иоанн Вианней, священник",
"The Dedication of the Basilica of Saint Mary Major": "Освящение базилики Святой Марии Великой",
"The Transfiguration of the Lord": "Преображение Господне",
"Saint Sixtus II, pope, and companions, martyrs": "Святой Сикст II, папа, и сподвижники, мученики",
"Saint Cajetan, priest": "Святой Каетан, священник",
"Saint Dominic, priest": "Святой Доминик, священник",
"Saint Lawrence, deacon and martyr": "Святой Лаврентий, диакон и мученик",
"Saint Clare, virgin": "Святая Клара, дева",
"Saint Jane Frances de Chantal, religious": "Святая Иоанна Франциска де Шанталь, монахиня",
"Saints Pontian, pope, and Hippolytus, priest, martyrs": "Святые Понтиан, папа, и Ипполит, священник, мученики",
"Saint Maximilian Mary Kolbe, priest and martyr": "Святой Максимилиан Мария Кольбе, священник и мученик",
"The Assumption of the Blessed Virgin Mary": "Успение Пресвятой Девы Марии",
"Saint John Eudes, priest": "Святой Иоанн Евд, священник",
"Saint Bernard, abbot and doctor of the Church": "Святой Бернард, аббат и учитель Церкви",
"Saint Pius X, pope": "Святой Пий X, папа",
"The Queenship of the Blessed Virgin Mary": "Царица Пресвятой Девы Марии",
"Saint Bartholomew, apostle": "Святой Варфоломей, апостол",
"Saint Louis": "Святой Людовик",
"Saint Joseph Calasanz, priest": "Святой Иосиф Каласанс, священник",
"Saint Monica": "Святая Моника",
"Saint Augustine, bishop and doctor of the Church": "Святой Августин, епископ и учитель Церкви",
"The Passion of Saint John the Baptist": "Усекновение главы святого Иоанна Крестителя",
"Saint Gregory the Great, pope and doctor of the Church": "Святой Григорий Великий, папа и учитель Церкви",
"The Nativity of the Blessed Virgin Mary": "Рождество Пресвятой Девы Марии",
"Saint Peter Claver, priest": "Святой Петр Клавер, священник",
"The Most Holy Name of Mary": "Пресвятое Имя Марии",
"The Exaltation of the Holy Cross": "Воздвижение Святого Креста",
"Our Lady of Sorrows": "Богородица Скорбящая",
"Saints Cornelius, pope, and Cyprian, bishop, martyrs": "Святые Корнелий, папа, и Киприан, епископ, мученики",
"Saint Robert Bellarmine, bishop and doctor of the Church": "Святой Роберт Беллармин, епископ и учитель Церкви",
"Saint Hildegard of Bingen, virgin and doctor of the Church": "Святая Хильдегарда Бингенская, дева и учитель Церкви",
"Saint Januarius, bishop and martyr": "Святой Януарий, епископ и мученик",
"Saint Matthew, apostle and evangelist": "Святой Матфей, апостол и евангелист",
"Saint Pius of Pietrelcina (Padre Pio), priest": "Святой Пиий Пиетрельчинский (Падре Пио), священник",
"Saints Cosmas and Damian, martyrs": "Святые Косма и Дамиан, мученики",
"Saint Wenceslaus, martyr": "Святой Вацлав, мученик",
"Saint Lawrence Ruiz and companions, martyrs": "Святой Лаврентий Руис и сподвижники, мученики",
"Saints Michael, Gabriel and Raphael, archangels": "Святые Михаил, Гавриил и Рафаил, архангелы",
"Saint Jerome, priest and doctor of the Church": "Святой Иероним, священник и учитель Церкви",
"Saint Thérèse of the Child Jesus, virgin and doctor of the Church": "Святая Тереза Младенца Иисуса, дева и учитель Церкви",
"Holy Guardian Angels": "Святые Ангелы-Хранители",
"Saint Faustina Kowalska, virgin": "Святая Фаустина Ковальская, дева",
"Blessed Francis Xavier Seelos, priest": "Блаженный Франциск Ксаверий Сеелос, священник",
"Saint Bruno, priest": "Святой Бруно, священник",
"Our Lady of the Rosary": "Богородица Розария",
"Saint Denis, bishop, and companions, martyrs": "Святой Дионисий, епископ, и сподвижники, мученики",
"Saint John Leonardi, priest": "Святой Иоанн Леонарди, священник",
"Saint Callistus I, pope and martyr": "Святой Каллист I, папа и мученик",
"Saint Teresa of Jesus, virgin and doctor of the Church": "Святая Тереза Иисусова, дева и учитель Церкви",
"Saint Hedwig, religious": "Святая Ядвига, монахиня",
"Saint Margaret Mary Alacoque, virgin": "Святая Маргарита Мария Алакок, дева",
"Saint Ignatius of Antioch, bishop and martyr": "Святой Игнатий Антиохийский, епископ и мученик",
"Saints Isaac Jogues and John de Brébeuf, priests, and companions, martyrs": "Святые Исаак Жог и Иоанн де Бребёф, священники, и сподвижники, мученики",
"Saint Paul of the Cross, priest": "Святой Павел Креста, священник",
"Saint John Paul II, pope": "Святой Иоанн Павел II, папа",
"Saint John of Capistrano, priest": "Святой Иоанн Капистранский, священник",
"Saint Anthony Mary Claret, bishop": "Святой Антоний Мария Кларет, епископ",
"Saints Simon and Jude, apostles": "Святые Симон и Иуда, апостолы",
"All Saints": "Всех Святых",
"The Commemoration of All the Faithful Departed (All Souls' Day)": "Поминовение всех усопших верных (День всех душ)",
"Saint Martin de Porres, religious": "Святой Мартин де Поррес, монах",
"Saint Charles Borromeo, bishop": "Святой Карл Борромео, епископ",
"The Dedication of the Lateran Basilica": "Освящение Латеранской базилики",
"Saint Leo the Great, pope and doctor of the Church": "Святой Лев Великий, папа и учитель Церкви",
"Saint Martin of Tours, bishop": "Святой Мартин Турский, епископ",
"Saint Josaphat, bishop and martyr": "Святой Иосафат, епископ и мученик",
"Saint Frances Xavier Cabrini, virgin": "Святая Франциска Ксаверия Кабрини, дева",
"Saint Margaret of Scotland": "Святая Маргарита Шотландская",
"Saint Gertrude, virgin": "Святая Гертруда, дева",
"Saint Elizabeth of Hungary, religious": "Святая Елизавета Венгерская, монахиня",
"The Dedication of the Basilicas of Saints Peter and Paul, apostles": "Освящение базилик святых Петра и Павла, апостолов",
"The Presentation of the Blessed Virgin Mary": "Введение во храм Пресвятой Девы Марии",
"Our Lord Jesus Christ, King of the Universe": "Господа нашего Иисуса Христа, Царя Вселенной",
"Saint Clement I, pope and martyr": "Святой Климент I, папа и мученик",
"Saint Columban, abbot": "Святой Колумбан, аббат",
"Saint Andrew Dũng-Lạc, priest, and companions, martyrs": "Святой Андрей Зунг-Лак, священник, и сподвижники, мученики",
"Saint Catherine of Alexandria, virgin and martyr": "Святая Екатерина Александрийская, дева и мученица",
"Saint Andrew, apostle": "Святой Андрей, апостол",
"Saint Francis Xavier, priest": "Святой Франциск Ксаверий, священник",
"Saint John Damascene, priest and doctor of the Church": "Святой Иоанн Дамаскин, священник и учитель Церкви",
"Saint Ambrose, bishop and doctor of the Church": "Святой Амвросий, епископ и учитель Церкви",
"The Immaculate Conception of the Blessed Virgin Mary": "Непорочное Зачатие Пресвятой Девы Марии",
"Saint Juan Diego Cuauhtlatoatzin": "Святой Хуан Диего Куаухтлатоатцин",
"Our Lady of Loreto": "Богородица Лоретанская",
"Saint Damasus I, pope": "Святой Дамасий I, папа",
"Our Lady of Guadalupe": "Богородица Гваделупская",
"Saint John of the Cross, priest and doctor of the Church": "Святой Иоанн Креста, священник и учитель Церкви",
"Saint Peter Canisius, priest and doctor of the Church": "Святой Петр Канизий, священник и учитель Церкви",
"Saint John of Kanty, priest": "Святой Иоанн Кант, священник",
"The Nativity of the Lord (Christmas)": "Рождество Господа нашего Иисуса Христа",
"Saint Stephen, the First Martyr": "Святой Стефан, первомученик",
"The Holy Family of Jesus, Mary and Joseph": "Святое Семейство Иисуса, Марии и Иосифа",
"The Holy Innocents, martyrs": "Святые Невинные Младенцы, мученики",
"Saint Thomas Becket, bishop and martyr": "Святой Фома Бекет, епископ и мученик",
"Saint Sylvester I, pope": "Святой Сильвестр I, папа",
"V Day within the Octave of the Nativity of the Lord": "V День в Октаве Рождества Господня",
"VI Day within the Octave of the Nativity of the Lord": "VI День в Октаве Рождества Господня",
"VII Day within the Octave of the Nativity of the Lord": "VII День в Октаве Рождества Господня",
"December 17": "17 декабря",
"December 18": "18 декабря",
"December 19": "19 декабря",
"December 21": "21 декабря",
"December 22": "22 декабря",
"December 23": "23 декабря",
"December 24 (Morning)": "24 декабря (Утро)",
"Ash Wednesday": "Пепельная среда",
"Thursday after Ash Wednesday": "Четверг после Пепельной среды",
"Friday after Ash Wednesday": "Пятница после Пепельной среды",
"Saturday after Ash Wednesday": "Суббота после Пепельной среды",
"Monday of Holy Week": "Понедельник Страстной седмицы",
"Tuesday of Holy Week": "Вторник Страстной седмицы",
"Wednesday of Holy Week": "Среда Страстной седмицы",
"Palm Sunday of the Passion of the Lord": "Вербное воскресенье Страстей Господних",
"Holy Thursday (Mass of the Lord's Supper)": "Великий Четверг (Месса Тайной Вечери)",
"Good Friday (Passion of the Lord)": "Страстная Пятница (Страсти Господни)",
"Holy Saturday (Easter Vigil)": "Великая Суббота (Пасхальное бдение)",
}

def tr_pattern(desc):
    m = re.match(r'(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday) of the ([IVXLCDM]+) Week of (Ordinary Time|Lent|Easter Time|Advent|Christmas Time|Easter)$', desc)
    if m:
        g = {"Ordinary Time":"обычного времени","Lent":"Великого поста","Easter Time":"Пасхи","Advent":"Адвента","Christmas Time":"Рождества","Easter":"Пасхи"}
        return f"{day_ru[m.group(1)]} {m.group(2)} седмицы {g[m.group(3)]}"
    m = re.match(r'([IVXLCDM]+) Sunday of (?:Easter|Ordinary Time|Lent|Advent|Christmas Time)\s*(?:\((.+)\))?\s*$', desc)
    if m:
        w = m.group(1)
        g = {"Ordinary Time":"обычного времени","Lent":"Великого поста","Easter":"Пасхи","Advent":"Адвента","Christmas Time":"Рождества","Easter Time":"Пасхи"}
        # find which season
        for k in g:
            if k in desc:
                base = f"{w} Неделя {g[k]}"
                if m.group(2):
                    em = {"Sunday of Divine Mercy":"Неделя Божьего Милосердия","Laetare Sunday":"Laetare (Неделя радости)","Gaudete Sunday":"Gaudete (Неделя радости)","or Sunday of Divine Mercy":"Неделя Божьего Милосердия","Sunday of the Word of God":"Неделя Слова Божия"}
                    extra = em.get(m.group(2), m.group(2))
                    return f"{base} ({extra})"
                return base
    return None

def tr_festejo(s):
    # Handle "Color: X or Y" before individual colors
    s = re.sub(r'Color:\s*(Violet|Purple|Pink|Rose|Black|White|Green|Red)\s+or\s+(Violet|Purple|Pink|Rose|Black|White|Green|Red)',
               lambda m: f'Цвет: {color_map[m.group(1)]} или {color_map[m.group(2)]}', s)
    # Individual colors
    s = re.sub(r'Color:\s*(White|Green|Red|Violet|Purple|Pink|Rose|Black)',
               lambda m: f'Цвет: {color_map[m.group(1)]}', s)
    # Ranks
    for eng, rus in rank_map.items():
        s = s.replace(f'({eng})', f'({rus})')

    # Try to extract description and translate it
    m = re.match(r'(.*?Цвет:\s*\S+(?:\s+или\s+\S+)?)\s*-\s*(.*)', s)
    if m:
        prefix = m.group(1) + " - "
        desc = m.group(2)
    elif re.match(r'^\([^)]+\)\s*-', s):
        m2 = re.match(r'(\([^)]+\)\s*-\s*.*?Цвет:\s*\S+(?:\s+или\s+\S+)?)\s*-\s*(.*)', s)
        if m2:
            prefix = m2.group(1) + " - "
            desc = m2.group(2)
        else:
            prefix = ""
            desc = s
    else:
        prefix = ""
        desc = s

    t = tr_pattern(desc)
    if t:
        return prefix + t
    if desc in FEST_TR:
        return prefix + FEST_TR[desc]

    return s

for fname in sorted(os.listdir(SRC)):
    if not fname.endswith('.json'):
        continue
    with open(os.path.join(SRC, fname), encoding='utf-8') as f:
        data = json.load(f)

    month_key = list(data.keys())[0]
    for entry in data[month_key]:
        if entry.get("tiempo") in tiempo_map:
            entry["tiempo"] = tiempo_map[entry["tiempo"]]
        if entry.get("dia-sem") in dia_sem_map:
            entry["dia-sem"] = dia_sem_map[entry["dia-sem"]]
        if "festejo" in entry:
            entry["festejo"] = {k: tr_festejo(v) for k, v in entry["festejo"].items()}

    with open(os.path.join(DST, fname), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"✓ {fname}")

print("\nDone!")
