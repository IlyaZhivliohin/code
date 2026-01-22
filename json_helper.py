import json, math, os, shutil


class JsonHelper:
    def __init__(self):
        with open('json/settings.json', 'r') as f:
            self.settings = json.load(f)
        with open('json/paths.json', 'r') as f:
            self.paths = json.load(f)

    # Сохранение пути к СПО
    def saveSettings(self, path_rtr_model):
        data = {
            "path_rtr_model": path_rtr_model
        }
        with open('json/settings.json', 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # Создание набора
    def createSet(self, data, data_name, data_country, data_type, data_date, data_other):
        set = []
        other_prm = None
        with open('json/other_prm.json', 'r') as f:
            other_prm = json.load(f)
        for obj in data:
            dict = {
                "name": obj.name,
                "country": obj.country,
                "type": obj.type,
                "carry_freq": self.pow(self.toFloat(obj.carry_freq_set)),
                "period_mks": self.toFloat(obj.period_mks_set),
                "width_mks": self.toFloat(obj.width_mks_set),
                "rotate_period_sec": float(obj.rotate_period_sec_set)
            }
            dict.update(other_prm)
            set.append(dict)
        name = (self.settings['path_rtr_model'] + self.paths['path_rls_parameters'] + os.path.sep + data_name +
                ('' if data_country == '' else '_' + data_country) + ('' if data_type == '' else '_' + data_type) +
                ('' if data_date == '..' else '_' + data_date) + ('' if data_other == '' else '_' + data_other) + '.json')

        with open(name, 'w') as f:
            json.dump(set, f, ensure_ascii=False, indent=2)

    # Загрузка набора В СПО
    def dwnSet(self, set_name):
        list = []
        path = self.settings['path_rtr_model'] + self.paths['path_rls_parameters'] + os.path.sep + set_name
        with open(path, 'r') as f:
            list = json.load(f)

        file = (self.settings['path_rtr_model'] + self.paths['path_rls_parameters'] + os.path.sep +
                'rls_parameters.json')
        shutil.copyfile(path, file)

        names = []
        for obj in list:
            names.append(obj['name'])
        print(names)
        self.dwnNames(names)

    # Загрузка названий объектов из набора
    # (Необходимо для корректной работы СПО)
    def dwnNames(self, names):
        path = self.settings['path_rtr_model'] + self.paths['path_rts_rtr_radar_proxy']
        list = []
        with open(path, 'r') as f:
            list = json.load(f)
        list['settings']['radar']['items'] = names
        list['settings']['radar']['value'] = names[0]
        with open(path, 'w') as f:
            json.dump(list, f, ensure_ascii=False, indent=2)

    # Возвращает данные из набора
    # для отображения их в таблице
    def getDataFromSelItem(self, name):
        list = []
        path = self.settings['path_rtr_model'] + self.paths['path_rls_parameters'] + os.path.sep + name
        with open(path, 'r') as f:
            list = json.load(f)
        return list

    # Добавляет выбранные объекты из БД
    # в набор
    def addInSet(self, data, name):
        set = []
        other_prm = None
        path = self.settings['path_rtr_model'] + self.paths['path_rls_parameters'] + os.path.sep + name


        with open('json/other_prm.json', 'r') as f:
            other_prm = json.load(f)

        with open(path, 'r') as f:
            set = json.load(f)

        for obj in data:
            dict = {
                "name": obj.name,
                "country": obj.country,
                "type": obj.type,
                "carry_freq": self.pow(self.toFloat(obj.carry_freq_set)),
                "period_mks": self.toFloat(obj.period_mks_set),
                "width_mks": self.toFloat(obj.width_mks_set),
                "rotate_period_sec": float(obj.rotate_period_sec_set)
            }

            dict.update(other_prm)
            set.append(dict)
        with open(path, 'w') as f:
            json.dump(set, f, ensure_ascii=False, indent=2)

        if name == 'rls_parameters.json':
            names = []
            for obj in set:
                names.append(obj['name'])
            self.dwnNames(names)

    # Возвращает объект из выбранного набора
    def getObj(self, name, obj_name):
        path = self.settings['path_rtr_model'] + self.paths['path_rls_parameters'] + os.path.sep + name
        with open(path, 'r') as f:
            set = json.load(f)
        for obj in set:
            if obj['name'] == obj_name:
                return obj

    # Обновляет набор при удалении из него объектов
    def updateSet(self, name, list):
        path = self.settings['path_rtr_model'] + self.paths['path_rls_parameters'] + os.path.sep + name
        with open(path, 'w') as f:
            json.dump(list, f, ensure_ascii=False, indent=2)

        if name == 'rls_parameters.json':
            names = []
            for obj in list:
                names.append(obj['name'])
            self.dwnNames(names)

    def toFloat(self, data):
        data = data.split(',')
        list = []
        for i in range(len(data)):
            if data[i].strip() != '':
                list.append(float(data[i].strip()))
        return list

    def pow(self, data):
        for i in range(len(data)):
            data[i] = data[i] * math.pow(10, 6)
        return data

