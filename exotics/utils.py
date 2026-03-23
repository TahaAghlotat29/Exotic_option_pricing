import numpy as np
from scipy.stats import norm

def black_scholes(S, K, T, r, q, sigma, option_type='call'):

    if T <= 0 or sigma <= 0:
        return np.maximum(S - K, 0) if option_type == 'call' else np.maximum(K - S, 0)
    
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    
    if option_type == 'call':
        return S*np.exp(-q*T)*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    elif option_type == 'put':
        return K*np.exp(-r*T)*norm.cdf(-d2) - S*np.exp(-q*T)*norm.cdf(-d1)
    
def greek_black_scholes(S, K, T, r, q, sigma, greek = 'delta'):
    d1 = (np.log(S/K) + (r-q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)

    if greek == 'delta':
        return np.exp(-q*T)*norm.cdf(d1) 
    elif greek == 'gamma' :
        return np.exp(-q*T)*norm.pdf(d1) / (S*sigma*np.sqrt(T))
    elif greek == 'vega' :
        return S * np.exp(-q*T) * norm.pdf(d1) * np.sqrt(T)
    return None