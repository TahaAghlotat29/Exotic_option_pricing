import numpy as np 
from scipy.stats import norm
from .utils import black_scholes

class ExoticOptions:
    def __init__(self, S, r, q, sigma):
        self.S = S
        self.r = r
        self.q = q
        self.sigma = sigma

    def price_digital_call(self, K, T):
        
        d1 = (np.log(self.S/K) + (self.r - self.q + 0.5*self.sigma**2)*T) / (self.sigma*np.sqrt(T))
        d2 = d1 - self.sigma*np.sqrt(T)

        return np.exp(-self.r * T) * norm.cdf(d2)
    
    def price_digital_replication(self, K, T, epsilon = 1e-4):
        """Replicates the digital call option using a central finite difference of two vanilla call options.
        """
        call_price_up = black_scholes(self.S, K + epsilon, T, self.r, self.q, self.sigma, option_type='call')
        call_price_down = black_scholes(self.S, K - epsilon, T, self.r, self.q, self.sigma, option_type='call')

        return (call_price_down - call_price_up) / (2 * epsilon)
    
    def price_double_digital(self, K1, K2, T, sigma_k1=None, sigma_k2=None):
        """Prices a double digital option with strikes K1 and K2, maturity T
         -  We will use in a second exemple( 03_double_digital_smile) different volatilities at each strike to capture the smile effect.
         - K1: Strike of the lower digital option
         - K2: Strike of the upper digital option
         - T: Time to maturity
         """
        vol1 = sigma_k1 if sigma_k1 is not None else self.sigma
        vol2 = sigma_k2 if sigma_k2 is not None else self.sigma
        
        d1_k1 = (np.log(self.S / K1) + (self.r - self.q + 0.5 * vol1**2) * T) / (vol1 * np.sqrt(T))
        d2_k1 = d1_k1 - vol1 * np.sqrt(T)
        price_k1 = np.exp(-self.r * T) * norm.cdf(d2_k1)
        
        d1_k2 = (np.log(self.S / K2) + (self.r - self.q + 0.5 * vol2**2) * T) / (vol2 * np.sqrt(T))
        d2_k2 = d1_k2 - vol2 * np.sqrt(T)
        price_k2 = np.exp(-self.r * T) * norm.cdf(d2_k2)
        
        return price_k1 - price_k2
