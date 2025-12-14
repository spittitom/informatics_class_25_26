class SIRModel:
    def __init__(self, total_population, I0, R0, beta, gamma):
        self.N = total_population
        self.I = I0
        self.R = R0
        self.S = total_population - I0 - R0
        self.beta = beta
        self.gamma = gamma
        
        self.S_list = [self.S]
        self.I_list = [self.I]
        self.R_list = [self.R]
        self.t_list = [0]

    def _step(self, dt=1):
        # Euler Method Arithmetic
        dS = (-self.beta * self.S * self.I / self.N) * dt
        dI = (self.beta * self.S * self.I / self.N - self.gamma * self.I) * dt
        dR = (self.gamma * self.I) * dt

        self.S += dS
        self.I += dI
        self.R += dR

        return self.S, self.I, self.R

    def run_simulation(self, days):
        for day in range(1, days):
            S, I, R = self._step(dt=1)
            self.S_list.append(S)
            self.I_list.append(I)
            self.R_list.append(R)
            self.t_list.append(day)
        return self.t_list, self.S_list, self.I_list, self.R_list