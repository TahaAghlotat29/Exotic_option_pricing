import numpy as np 
from scipy.stats import norm

class Greeks:
    def __init__(self, engine):
        self.engine = engine
    
    def digital_delta(self, K, T):
        d1 = (np.log(self.engine.S / K) + (self.engine.r - self.engine.q + 0.5 * self.engine.sigma ** 2) * T) / (self.engine.sigma * np.sqrt(T))
        d2 = d1 - self.engine.sigma * np.sqrt(T)

        return np.exp(-self.engine.r * T) * norm.pdf(d2) / (self.engine.S * self.engine.sigma * np.sqrt(T))
    
    def digital_gamma(self, K, T):
        d1 = (np.log(self.engine.S / K) + (self.engine.r - self.engine.q + 0.5 * self.engine.sigma ** 2) * T) / (self.engine.sigma * np.sqrt(T))
        d2 = d1 - self.engine.sigma * np.sqrt(T)

        return -np.exp(-self.engine.r * T) * norm.pdf(d2) * d1 / (self.engine.S ** 2 * self.engine.sigma ** 2 * T)
    
    def digital_vega(self, K, T):
        d1 = (np.log(self.engine.S / K) + (self.engine.r - self.engine.q + 0.5 * self.engine.sigma ** 2) * T) / (self.engine.sigma * np.sqrt(T))
        d2 = d1 - self.engine.sigma * np.sqrt(T)

        return - np.exp(-self.engine.r * T) * norm.pdf(d2) * d1 / (self.engine.sigma)
    
    def double_digital_delta(self, K1, K2, T):
        """ Delta of a Double Digital = Delta(K1) - Delta(K2) """
        return self.digital_delta(K1, T) - self.digital_delta(K2, T)
    
    def double_digital_gamma(self, K1, K2, T):
        """ Gamma of a Double Digital = Gamma(K1) - Gamma(K2) """
        return self.digital_gamma(K1, T) - self.digital_gamma(K2, T)
    
    def double_digital_vega(self, K1, K2, T):
        """ Vega of a Double Digital = Vega(K1) - Vega(K2) """
        return self.digital_vega(K1, T) - self.digital_vega(K2, T)



