from escenas.ES_base import EscenaBase


class Tutorial(EscenaBase):
    def __init__(self):
        super().__init__()

    def HandleEvents(self, events):
        return super().HandleEvents(events)

    def Update(self, dt, keys):
        return super().Update(dt, keys)

    def draw(self, screen):
        return super().draw(screen)
