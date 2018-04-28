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
        self._probpyelonphritis = 0.04
        self._countnopyelonephritis = 0
        self._proburinalysis = 0.769
        self._counturinalysis = 0
        self._countnourinalysis = 0
        self._probUTIdiagnosed = 0.8481
        self._countUTIdiagnosis = 0
        self._noUTIdiagnosis = 0
        self._probUTIcured = 0.94
        self._countUTIcured = 0
        self._countUTInotcured = 0
        self._probpersistantinfection = 0.96  # inverse of prob of pylonephritis
        self._countpersistantinfection = 0
        self._countpyelonephritis = 0
        self._probmodifiedantibiotics = 0.75
        self._countmodifiedantibiotics = 0
        self._countextendedtreatment = 0
        self._probinpatienttreatment = 0.2  # inverse of prob of outpatient treatment
        self._countinpatienttreatment = 0
        self._countoutpatienttreatment = 0
        self._probSTIorvaginitis = 0.291
        self._countSTIorvaginitis = 0
        self._countnodisorderpresent = 0
        self._extended_treatment_cost = 0
        self._inpatient_treatment_cost = 0
        self._outpatient_treatment_cost = 0

    def simulate(self, n_of_days):
        t = 0

        while self._healthState == HealthStat.NO_UTI and t < n_of_days:
            if self._rnd.sample() < (self._probUTI*Data.DAILY_ANTIBIOTIC_RR):
                self._countUTIs += 1

            t +=1

            # pylenophritis
        for i in range(self._countUTIs):
            if self._rnd.random_sample() < self._probpyelonphritis:
                self._countpyelonephritis += 1
            else:
                self._countnopyelonephritis += 1
        for i in range(self._countpyelonephritis):
            if self._rnd.random_sample() < self._probinpatienttreatment:
                self._countinpatienttreatment += 1
            else:
                self._countoutpatienttreatment += 1

        # no pylenophritis
        for i in range(self._countnopyelonephritis):
            if self._rnd.random_sample() < self._proburinalysis:
                self._counturinalysis += 1
            else:
                self._countnourinalysis += 1
        # urinalysis
        for i in range(self._counturinalysis):
            if self._rnd.random_sample() < self._probUTIdiagnosed:
                self._countUTIdiagnosis += 1  # RX cipro
            else:
                self._noUTIdiagnosis += 1  # must continue on to lab tests
        for i in range(self._countUTIdiagnosis):
            if self._rnd.random_sample() < self._probUTIcured:
                self._countUTIcured += 1  # cost taken into account with UTI_diagnosis cost
            else:
                self._countUTInotcured += 1
        for i in range(self._countUTInotcured):
            if self._rnd.random_sample() < self._probpersistantinfection:
                self._countpersistantinfection += 1
            else:
                self._countpyelonephritis += 1
        for i in range(self._countpersistantinfection):
            if self._rnd.random_sample() < self._probmodifiedantibiotics:
                self._countmodifiedantibiotics += 1
            else:
                self._countextendedtreatment += 1
        for i in range(self._countpyelonephritis):
            if self._rnd.random_sample() < self._probinpatienttreatment:
                self._countinpatienttreatment += 1
            else:
                self._countoutpatienttreatment += 1

        # lab test branch under urinalysis
        for i in range(self._noUTIdiagnosis):
            if self._rnd.random_sample() < self._probSTIorvaginitis:
                self._countSTIorvaginitis += 1
            else:
                self._countnodisorderpresent += 1

        # no urinalysis
        for i in range(self._countnourinalysis):
            if self._rnd.random_sample() < self._probUTIdiagnosed:
                self._countUTIdiagnosis += 1  # RX cipro
            else:
                self._noUTIdiagnosis += 1  # must continue on to lab tests
        for i in range(self._countUTIdiagnosis):
            if self._rnd.random_sample() < self._probUTIcured:
                self._countUTIcured += 1  # cost taken into account with UTI_diagnosis cost
            else:
                self._countUTInotcured += 1
        for i in range(self._countUTInotcured):
            if self._rnd.random_sample() < self._probpersistantinfection:
                self._countpersistantinfection += 1
            else:
                self._countpyelonephritis += 1
        for i in range(self._countpersistantinfection):
            if self._rnd.random_sample() < self._probmodifiedantibiotics:
                self._countmodifiedantibiotics += 1
            else:
                self._countextendedtreatment += 1
        for i in range(self._countpyelonephritis):
            if self._rnd.random_sample() < self._probinpatienttreatment:
                self._countinpatienttreatment += 1
            else:
                self._countoutpatienttreatment += 1

    def get_count_utis(self):
        return self._countUTIs

    def get_cost_treatment(self):
        return Data.DAILY_ANTIBIOTIC_COST*365

    def get_number_uranlysis(self):
        return self._counturinalysis

    def get_uranlysis_cost(self):
        return Data.URINALYSIS_COST*self._counturinalysis

    def get_number_UTI_diagnosis(self):
        return self._countUTIdiagnosis

    def get_UTI_diagnosis_cost(self):
        return Data.CIPRO_COST*self._countUTIdiagnosis

    def get_number_UTI_not_cured(self):
        return self._countUTInotcured

    def get_UTI_not_cured_cost(self):
        return Data.MD_VISIT_COST*self._countUTInotcured

    def get_number_persistant_infection(self):
        return self._countpersistantinfection

    def get_modified_antibiotics_cost(self):
        return Data.MODIFIED_ANTIBIOTIC_COST * self._countmodifiedantibiotics

    def get_number_modified_antibiotics(self):
        return self._countmodifiedantibiotics

    def get_extended_treatment_cost(self):
        if self._countextendedtreatment >= 1:
            self._extended_treatment_cost = Data.EXTENDED_TREATMENT_COST * 5
        return self._extended_treatment_cost

    def get_number_extended_treatment_(self):
        return self._countextendedtreatment

    def get_number_pyelonephritis(self):
        return self._countpyelonephritis

    def get_number_inpatient_treatment(self):
        return self._countinpatienttreatment

    def get_inpatient_treatment_cost(self):
        if self._countinpatienttreatment >= 1:
            self._inpatient_treatment_cost = Data.INPATIENT_TREATMENT_COST * 3
        return self._inpatient_treatment_cost  # treatment lasts 3 daysdays

    def get_number_outpatient_treatment(self):
        return self._countoutpatienttreatment

    def get_outpatient_treatment_cost(self):
        if self._countoutpatienttreatment >= 1:
            self._outpatient_treatment_cost = Data.OUTPATIENT_TREATMENT_COST * 7
        return self._outpatient_treatment_cost

    def get_number_STI_or_vaginitis(self):
        return self._countSTIorvaginitis

    def get_STI_or_vaginitis_cost(self):
        return Data.STI_OR_VAGINITIS_COST*self._countSTIorvaginitis

    def get_number_no_disorder_present(self):
        return self._countnodisorderpresent

    def get_total_costs(self):
        cost_treatment = Data.DAILY_ANTIBIOTIC_COST*365
        cost_urinalysis = Data.URINALYSIS_COST*self._counturinalysis
        cost_UTI_diagnosis = Data.CIPRO_COST*self._countUTIdiagnosis
        cost_UTI_not_cured = Data.MD_VISIT_COST*self._countUTInotcured
        cost_modified_antibiotics = Data.MODIFIED_ANTIBIOTIC_COST * self._countmodifiedantibiotics
        cost_extended_treatment = self._extended_treatment_cost
        cost_inpatient = self._inpatient_treatment_cost
        cost_outpatient = self._outpatient_treatment_cost
        cost_STI_or_vaginitis = Data.STI_OR_VAGINITIS_COST*self._countSTIorvaginitis
        total_costs = cost_treatment + cost_urinalysis + cost_UTI_diagnosis + cost_UTI_not_cured + \
                      cost_modified_antibiotics + cost_extended_treatment + cost_inpatient + cost_outpatient + \
                      cost_STI_or_vaginitis

        return total_costs

class Cohort:
    def __init__(self, id, pop_size):
        self._initialPopSize = pop_size
        self._patients = []
        self._countUTIs = []
        self._UTICosts = []
        self._countUrinalysis = []
        self._urinalysisCost = []
        self._countUTIdiag = []
        self._costUTIdiag = []
        self._countUTIsNotCured = []
        self._costUTIsnotcured = []
        self._countPersistentinfections = []
        self._countModAntibiotic = []
        self._costModAntibiotic = []
        self._countExtendedTreat = []
        self._costExtendedTreat = []
        self._countPyelo = []
        self._countInpatient = []
        self._costInpatient = []
        self._countOutpatient = []
        self._costOutpatient = []
        self._countSTIVag = []
        self._costSTIVag = []
        self._noDisorder = []
        self._totalcost = []

        for i in range(pop_size):
            patient = Patient(id*pop_size + i)
            self._patients.append(patient)

    def simulate(self, n_of_days):
        for patient in self._patients:
            patient.simulate(n_of_days)
            value = patient.get_count_utis()
            self._countUTIs.append(value)
            cost = patient.get_cost_treatment()
            self._UTICosts.append(cost)
            urinalysis = patient.get_number_uranlysis()
            self._countUrinalysis.append(urinalysis)
            urin_cost = patient.get_uranlysis_cost()
            self._urinalysisCost.append(urin_cost)
            uti_diag = patient.get_number_UTI_diagnosis()
            self._countUTIdiag.append(uti_diag)
            diag_cost = patient.get_UTI_diagnosis_cost()
            self._costUTIdiag.append(diag_cost)
            utisnotcured = patient.get_number_UTI_not_cured()
            self._countUTIsNotCured.append(utisnotcured)
            cost_not_cured = patient.get_UTI_not_cured_cost()
            self._costUTIsnotcured.append(cost_not_cured)
            persistent = patient.get_number_persistant_infection()
            self._countPersistentinfections.append(persistent)
            ct_modanti = patient.get_number_modified_antibiotics()
            self._countModAntibiotic.append(ct_modanti)
            cost_modanti = patient.get_modified_antibiotics_cost()
            self._costModAntibiotic.append(cost_modanti)
            ct_exttreat = patient.get_number_extended_treatment_()
            self._countExtendedTreat.append(ct_exttreat)
            cost_exttreat = patient.get_extended_treatment_cost()
            self._costExtendedTreat.append(cost_exttreat)
            ct_pyelo = patient.get_number_pyelonephritis()
            self._countPyelo.append(ct_pyelo)
            ct_inpatient = patient.get_number_inpatient_treatment()
            self._countInpatient.append(ct_inpatient)
            cost_inpatient = patient.get_inpatient_treatment_cost()
            self._costInpatient.append(cost_inpatient)
            ct_outpatient = patient.get_number_outpatient_treatment()
            self._countOutpatient.append(ct_outpatient)
            cost_outpatient = patient.get_outpatient_treatment_cost()
            self._costOutpatient.append(cost_outpatient)
            ct_stivag = patient.get_number_STI_or_vaginitis()
            self._countSTIVag.append(ct_stivag)
            cost_stivag = patient.get_STI_or_vaginitis_cost()
            self._costSTIVag.append(cost_stivag)
            ct_nodisorder = patient.get_number_no_disorder_present()
            self._noDisorder.append(ct_nodisorder)
            total_cost = patient.get_total_costs()
            self._totalcost.append(total_cost)

        return CohortOutcomes(self)

    def get_number_utis(self):
        return self._countUTIs

    def get_cost_treatments(self):
        return self._UTICosts

    def get_count_urinalysis(self):
        return self._countUrinalysis

    def get_urinalysis_cost(self):
        return self._urinalysisCost

    def get_count_uti_diag(self):
        return self._countUTIdiag

    def get_cost_uti_diag(self):
        return self._costUTIdiag

    def get_count_uti_notcured(self):
        return self._countUTIsNotCured

    def get_cost_uti_notcured(self):
        return self._costUTIsnotcured

    def get_count_persistent(self):
        return self._countPersistentinfections

    def get_count_mod_antibiotic(self):
        return self._countModAntibiotic

    def get_cost_modantibiotic(self):
        return self._costModAntibiotic

    def get_count_extended_treat(self):
        return self._countExtendedTreat

    def get_cost_extended_treat(self):
        return self._costExtendedTreat

    def get_count_pyelo(self):
        return self._countPyelo

    def get_count_inpatient(self):
        return self._countInpatient

    def get_cost_inpatient(self):
        return self._costInpatient

    def get_count_outpatient(self):
        return self._countOutpatient

    def get_cost_outpatient(self):
        return self._costOutpatient

    def get_count_stivag(self):
        return self._countSTIVag

    def get_cost_stivag(self):
        return self._costSTIVag

    def get_count_no_disorder(self):
        return self._noDisorder

    def get_total_cost(self):
        return self._totalcost

class CohortOutcomes:
    def __init__(self, simulated_cohort):
        self._simulatedCohort = simulated_cohort
        self._sumStat_patientcountUTIs = \
            Stat.SummaryStat('Patient # UTIs', self._simulatedCohort.get_number_utis())
        self._sumStat_patientCosts = \
            Stat.SummaryStat('Cost of treatment', self._simulatedCohort.get_cost_treatments())
        self._sumStat_countUrin = Stat.SummaryStat('Count Urinalysis:',self._simulatedCohort.get_count_urinalysis())
        self._sumStat_costUrin = Stat.SummaryStat('Cost Urinalysis:',self._simulatedCohort.get_urinalysis_cost())
        self._sumStat_countUTIDiag = Stat.SummaryStat('Count UTI Diagnosis:',self._simulatedCohort.get_count_uti_diag())
        self._sumStat_costUTIDiag = Stat.SummaryStat('Cost UTI Diagnosis:',self._simulatedCohort.get_cost_uti_diag())
        self._sumStat_countUTInotcured = Stat.SummaryStat('Count UTI Not Cured:',self._simulatedCohort.get_count_uti_notcured())
        self._sumStat_costUTInotcured = Stat.SummaryStat('Cost UTI Not Cured:', self._simulatedCohort.get_cost_uti_notcured())
        self._sumStat_countPersistent = Stat.SummaryStat('Count Persistent Infections:', self._simulatedCohort.get_count_persistent())
        self._sumStat_countModAnti = Stat.SummaryStat('Count Modified Antibiotic Treatment:', self._simulatedCohort.get_count_mod_antibiotic())
        self._sumStat_costModAnti = Stat.SummaryStat('Cost Modified Antibiotic Treatment:', self._simulatedCohort.get_cost_modantibiotic())
        self._sumStat_countExtended = Stat.SummaryStat('Count Extended Treatment:', self._simulatedCohort.get_count_extended_treat())
        self._sumStat_costExtended = Stat.SummaryStat('Cost Extended Treatment:', self._simulatedCohort.get_cost_extended_treat())
        #####
        self._sumStat_countPyelo = Stat.SummaryStat('Count Pyelonephritis:', self._simulatedCohort.get_count_pyelo()) #
        self._sumStat_countInpatient = Stat.SummaryStat('Count Inpatient Treatment:', self._simulatedCohort.get_count_inpatient())#
        self._sumStat_costInpatient = Stat.SummaryStat('Cost Inpatient Treatment:', self._simulatedCohort.get_cost_inpatient())#
        self._sumStat_countOutpatient = Stat.SummaryStat('Count Outpatient Treatment:', self._simulatedCohort.get_count_outpatient())#
        self._sumStat_costOutpatient = Stat.SummaryStat('Cost Outpatient Treatment:', self._simulatedCohort.get_cost_outpatient())#
        self._sumStat_countSTI = Stat.SummaryStat('Count STI or Vaginitis:', self._simulatedCohort.get_count_stivag())#
        self._sumStat_costSTI = Stat.SummaryStat('Cost STI or Vaginitis:', self._simulatedCohort.get_cost_stivag())#
        self._sumStat_countNoDisorder = Stat.SummaryStat('Count No Disorder Present:', self._simulatedCohort.get_count_no_disorder())
        self._sumStat_total_cost = Stat.SummaryStat('Total Cost per Patient:', self._simulatedCohort.get_total_cost())

    def get_ave_number_utis(self):
        return self._sumStat_patientcountUTIs.get_mean()

    def get_CI_number_utis(self, alpha):
        return self._sumStat_patientcountUTIs.get_t_CI(alpha)

    def get_ave_treatment_cost(self):
        return self._sumStat_patientCosts.get_mean()

    def get_CI_treatment_cost(self, alpha):
        return self._sumStat_patientCosts.get_t_CI(alpha)

    def get_ave_number_urinalysis(self):
        return self._sumStat_countUrin.get_mean()

    def get_CI_number_urinalysis(self, alpha):
        return self._sumStat_countUrin.get_t_CI(alpha)

    def get_ave_cost_urin(self):
        return self._sumStat_costUrin.get_mean()

    def get_CI_cost_urin(self):
        return self._sumStat_costUrin.get_t_CI(alpha)

    def get_ave_number_count_UTI_diag(self):
        return self._sumStat_countUTIDiag.get_mean()

    def get_CI_number_UTI_diag(self, alpha):
        return self._sumStat_countUTIDiag.get_t_CI(alpha)

    def get_ave_cost_UTI_diag(self):
        return self._sumStat_costUTIDiag.get_mean()

    def get_CI_cost_UTI_diag(self, alpha):
        return self._sumStat_costUTIDiag.get_t_CI(alpha)

    def get_ave_number_UTI_notcured(self):
        return self._sumStat_countUTInotcured.get_mean()

    def get_CI_number_UTI_notcured(self, alpha):
        return self._sumStat_countUTInotcured.get_t_CI(alpha)

    def get_ave_cost_UTI_notcured(self):
        return self._sumStat_costUTInotcured.get_mean()

    def get_CI_cost_UTI_notcured(self, alpha):
        return self._sumStat_costUTInotcured.get_t_CI(alpha)

    def get_ave_number_persistant(self):
        return self._sumStat_countPersistent.get_mean()

    def get_CI_number_persistant(self, alpha):
        return self._sumStat_countPersistent.get_t_CI(alpha)

    def get_ave_number_mod_anti(self):
        return self._sumStat_countModAnti.get_mean()

    def get_CI_number_mod_anti(self, alpha):
        return self._sumStat_countModAnti.get_t_CI(alpha)

    def get_ave_cost_mod_anti(self):
        return self._sumStat_costModAnti.get_mean()

    def get_CI_cost_mod_anti(self, alpha):
        return self._sumStat_costModAnti.get_t_CI(alpha)

    def get_ave_count_extended_treat(self):
        return self._sumStat_countExtended.get_mean()

    def get_CI_count_extended_treat(self, alpha):
        return self._sumStat_countExtended.get_t_CI(alpha)

    def get_ave_cost_extended_treat(self):
        return self._sumStat_costExtended.get_mean()

    def get_CI_cost_extended_treat(self,alpha):
        return self._sumStat_costExtended.get_t_CI(alpha)

    def get_ave_count_pyelo(self):
        return self._sumStat_countPyelo.get_mean()

    def get_CI_count_pyelo(self, alpha):
        return self._sumStat_countPyelo.get_t_CI(alpha)

    def get_ave_count_inpatient(self):
        return self._sumStat_countInpatient.get_mean()

    def get_CI_count_inpatient(self, alpha):
        return self._sumStat_countInpatient.get_t_CI(alpha)

    def get_ave_cost_inpatient(self):
        return self._sumStat_costInpatient.get_mean()

    def get_CI_cost_inpatient(self, alpha):
        return self._sumStat_costInpatient.get_t_CI(alpha)

    def get_ave_count_outpatient(self):
        return self._sumStat_countOutpatient.get_mean()

    def get_CI_count_outpatient(self, alpha):
        return self._sumStat_countOutpatient.get_t_CI(alpha)

    def get_ave_cost_outpatient(self):
        return self._sumStat_costOutpatient.get_mean()

    def get_CI_cost_outpatient(self, alpha):
        return self._sumStat_costOutpatient.get_t_CI(alpha)

    def get_ave_count_stivag(self):
        return self._sumStat_countSTI.get_mean()

    def get_CI_count_stivag(self, alpha):
        return self._sumStat_countSTI.get_t_CI(alpha)

    def get_ave_cost_stivag(self):
        return self._sumStat_costSTI.get_mean()

    def get_CI_cost_stivag(self, alpha):
        return self._sumStat_costSTI.get_t_CI(alpha)

    def get_ave_count_no_disorder(self):
        return self._sumStat_countNoDisorder.get_mean()

    def get_CI_count_no_disorder(self, alpha):
        return self._sumStat_countNoDisorder.get_t_CI(alpha)

    def get_ave_total_cost(self):
        return self._sumStat_total_cost.get_mean()

    def get_CI_total_cost(self, alpha):
        return self._sumStat_total_cost.get_t_CI(alpha)



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
print('Average treatment cost:', cohortOutcome.get_ave_treatment_cost())
print('95% CI of treatment cost:', cohortOutcome.get_CI_treatment_cost(ALPHA))

print('AVERAGE TOTAL COST:', cohortOutcome.get_ave_total_cost())
print('95% CI TOTAL COST:', cohortOutcome.get_CI_total_cost(ALPHA))