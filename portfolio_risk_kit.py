import pandas as pd
import scipy.stats  
def drawdown(return_series: pd.Series):
    """
    Takes a time series of asset returns
    Computes and returns a DataFrame that contains:
    the wealth index
    the previous peaks
    % drawdowns
    """
    wealth_index = 1000 * (1+return_series).cumprod()
    previous_peaks = wealth_index.cummax()
    drawdowns = (wealth_index - previous_peaks) / previous_peaks
    return pd.DataFrame({
        "Wealth": wealth_index,
        "Peaks": previous_peaks,
        "Drawdown": drawdowns
    })

def get_ffme_returns():
    """
    Load the Fama-French Dataset for the returns of the Top and Bottom Deciles by MarketCap
    """
    me_m = pd.read_csv("INSERT PATHNAME.csv",
                      header = 0, index_col = 0, na_values = -99.99)
    rets = me_m[['Lo 10','Hi 10']]
    rets.columns = ['SmallCap', 'LargeCap']
    rets = rets / 100
    rets.index = pd.to_datetime(rets.index, format = "%Y%m").to_period('M')
    return rets

def get_xxx_returns():
    """
    Load Index Returns
    """
    xxx = pd.read_csv("INSERT PATHNAME for XXX .csv",
                      header = 0, index_col = 0, parse_dates = True)
    xxx = xxx / 100
    xxx.index = xxx.index.to_period('M')
    return xxx

def semideviation(r):
    """
    Returns the semideviation aka negative semideviation of r
    r must be a Series or a DataFrame
    """
    is_negative = r < 0
    return r[is_negative].std(ddof=0)

def skewness(r):
    """
    Alternative to scipy.stats.skew()
    Computes the skewness of the supplied Series of DataFrame
    Returns a float or a Series
    """
    demeaned_r = r-r.mean()
    # Use the population standard deviation, so set dof = 0
    sigma_r = r.std(ddof=0) #ddof = degree of freedom is 0
    exp = (demeaned_r**3).mean()
    return exp/sigma_r**3

def kurtosis(r):
    """
    Alternative to scipy.stats.kurtosis()
    Computes the kurtosis of the supplied Series of DataFrame
    Returns a float or a Series
    """
    demeaned_r = r-r.mean()
    # Use the population standard deviation, so set dof = 0
    sigma_r = r.std(ddof=0) #ddof = degree of freedom is 0
    exp = (demeaned_r**4).mean()
    return exp/sigma_r**4

def is_normal(r, level = 0.01):
    """
    Applies the Jarque-Bera test to determine if a Series is normal or not
    Test is applied at the 1% level by default
    Returns True if the hypothesis of normality is accepted, False otherwise
    """
    statistics, p_value = scipy.stats.jarque_bera(r)
    return p_value > level

def var_historic(r, level = 5):
    import numpy as np
    """
    Returns the Historic Value at Risk at a specified level
    i.e. returns the number such that 'level' precent of the returns
    fall below that number, and the (100-level) precent are above
    """
    if isinstance(r, pd.DataFrame):
        return r.aggregate(var_historic, level = level)
    elif isinstance(r, pd.Series):
        return -np.percentile(r,level) #We put a "-" there because we prefer to report this number as positive
    else:
        raise TypeError('Expected r to be Series or DataFrame')