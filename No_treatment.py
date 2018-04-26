from enum import Enum
import numpy as np
from scipy.stats import expon
import scr.SamplePathClasses as PathCls
import scr.StatisticalClasses as Stat
import InputData as Data
import matplotlib as matplotlib

class Patient(object):
    def __init__(self, id):
        self._id = id
        self._rnd = np.random
        self._rnd.seed(id)
        self._probUTI = expon.cdf(3*Data.DELTA_T)
        self._countUTIs = 0

    def simulate(self, n_of_days):
        count_UTIs = 0

        for i in range(n_of_days):
            if self._rnd.random_sample() < self._probUTI:
                count_UTIs += 1
                self._countUTIs +=1

    def get_number_utis(self):
        return self._countUTIs

    def get_costs(self):
        return Data.NO_TREATMENT_COST*self._countUTIs

class Cohort:
    def __init__(self, n_days):
        self._numberUTIs = []
        self._UTICosts = []

        for n in range(n_days):
            cohort = Patient(id=n)
            cohort.simulate(365)
            self._UTICosts.append(cohort.get_costs())
            self._numberUTIs.append(cohort.get_number_utis())

    def get_ave_cost(self):
        return sum(self._UTICosts) / len(self._UTICosts)

    def get_number_utis(self):
        return self._numberUTIs

    def get_ave_uti_count(self):
        return sum(self._numberUTIs)/len(self._numberUTIs)

trial = Cohort(n_days = 365)
print("average cost = ", trial.get_ave_cost())
print("number of utis = ", trial.get_number_utis())
print("ave number of utis = ", trial.get_ave_uti_count())

