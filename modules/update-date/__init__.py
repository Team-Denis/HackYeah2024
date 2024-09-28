import datetime
import math

class UpdateDateModule(Module):

    def __init__(self, name, dependencies=None):
        super().__init__(name, dependencies)

    def run(self):
        w = self.dependencies["whois"]
        last_update = datetime.date(w["update_date"][:5], w["update_date"][6:8], w["update_date"][9:])
        now = datetime.date.today()
        delta = now - last_update

        # Get number of days between those two dates
        return -math.exp(-(( delta.days/100)**2)) + 1