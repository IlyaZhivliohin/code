class RLS:
    def __init__(self, choice, id, name, source, country, carrier,
                 type, carry_freq, carry_freq_set, period_mks, period_mks_set,
                 width_mks, width_mks_set, rotate_period_sec, rotate_period_sec_set,
                 description_of_the_object, description_of_the_source, signals):

        self.choice = choice
        self.id = id
        self.name = name
        self.source = source
        self.country = country
        self.carrier = carrier
        self.type = type
        self.carry_freq = carry_freq
        self.carry_freq_set = carry_freq_set
        self.period_mks = period_mks
        self.period_mks_set = period_mks_set
        self.width_mks = width_mks
        self.width_mks_set = width_mks_set
        self.rotate_period_sec = rotate_period_sec
        self.rotate_period_sec_set = rotate_period_sec_set
        self.description_of_the_object = description_of_the_object
        self.description_of_the_source = description_of_the_source
        self.signals = signals


