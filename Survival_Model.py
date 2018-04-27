from enum import Enum
import numpy as np
import InputData as Data
from scipy.stats import expon
import scr.SamplePathClasses as PathCls
import scr.StatisticalClasses as Stat

class HealthStat(Enum):
    UTI = 1 # previously alive
    NO_UTI = 0 #previously dead

class Patient:
    def __init__(self, id):
        self._id = id
        self._rnd = np.random
        self._rnd.seed(self._id)
        self._healthState = HealthStat.NO_UTI
        self._probUTI = expon.cdf(3 * Data.DELTA_T)
        self._countUTIs = 0

    def simulate(self, n_of_days):
        t = 0

        while self._healthState == HealthStat.NO_UTI and t < n_of_days:
            if self._rnd.sample() < self._probUTI:
                self._countUTIs += 1

            t +=1

    def get_count_utis(self):
        return self._countUTIs

class Cohort:
    def __init__(self, id, pop_size):
        self._initialPopSize = pop_size
        self._patients = []
        self._countUTIs = []

        for i in range(pop_size):
            patient = Patient(id*pop_size + i)
            self._patients.append(patient)

    def simulate(self, n_of_days):
        for patient in self._patients:
            patient.simulate(n_of_days)
            value = patient.get_count_utis()
            self._countUTIs.append(value)

        return CohortOutcomes(self)

    def get_number_utis(self):
        return self._countUTIs

class CohortOutcomes:
    def __init__(self, simulated_cohort):
        self._simulatedCohort = simulated_cohort
        self._sumStat_patientcountUTIs = \
            Stat.SummaryStat('Patient # UTIs', self._simulatedCohort.get_number_utis())

    def get_ave_number_utis(self):
        return self._sumStat_patientcountUTIs.get_mean()

    def get_CI_number_utis(self, alpha):
        return self._sumStat_patientcountUTIs.get_t_CI(alpha)

SIM_POP_SIZE = 10000
TIME_STEPS = 365
ALPHA = 0.05
# create a cohort of patients
myCohort = Cohort(id=1, pop_size=SIM_POP_SIZE)

# simulate the cohort
cohortOutcome = myCohort.simulate(TIME_STEPS)

# print the patient survival time
print('Average number UTIs:', cohortOutcome.get_ave_number_utis())
print('95% CI of average number UTIs', cohortOutcome.get_CI_number_utis(ALPHA))
