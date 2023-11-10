class RechargeEnergyMixin:

    def recharge_energy(self, amount: int):
        if self.energy + amount > 100:
            self.energy = 100
        else:
            self.energy += amount

        self.save()
