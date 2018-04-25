import numpy as np
import scipy as scipy

#  outcomes: number of UTI's per year, annual cost for payer perspective, annual cost from patients perspective,
# quality adjusted life-days
#  cost effectiveness: cost per QALY gained

POP_SIZE = 10000  # for each intervention
DELTA_T = 1
SIM_LENGTH = 365 # days (1 year)
ALPHA = 0.05
DELTA_T = 1/365

NO_TREATMENT = 3  # UTI's / year

PROB_NO_TREATMENT = 1 - np.exp(-3*DELTA_T)


# probabilities
ACUPUNCTURE_RR = 0.68
CRANBERRY_RR = 0.50
DAILY_ANTIBIOTIC_RR = 0.86
ESTROGEN_RR = 0.65
FLUOROQ_RR = 0.94


YEAST_LESS_THAN_3 = 0.05
YEAST_GREATER_THAN_3 = 0.07
MEDICAL_VISIT_YEAST = 0.25

CHANGE_THERAPY = 0.75

URINALYSIS = 0.769
UTI_SYMPTOMS = 0.8481
PYELO = 0.04

PYELO_OUT = 0.80
STI = 0.157
VAGINITIS = 0.133
NO_DISORDER = 0.709


# costs per day
NO_TREATMENT_COST = 0
ACUPUNCTURE_COST = 2.51
CRANBERRY_COST = 0.75
ESTROGEN_COST = 0.50
DAILY_ANTIBIOTIC_COST = 1.95
CIPRO_250 = 4.44
CIPRO_500 = 5.38
SELF_TREAT = 16.14

PYELO_HOSPITAL = 1782.28
OUT_ABX_R = 29.77  # outpatient treatment for infection unresponsive to fluoroquinolones or pyelonephritis
PHYSICIAN_FOLLOW_UP = 97.77
INITIAL_URINALYSIS = 20.78
FOLLOW_UP_URINALYSIS = 20.78
URINE_CULTURE = 46.42
VAGINAL_SMEAR = 13.5
STI_TEST = 67.60


# durations (days)
PYELO_HOSPITAL_DUR = 3
OUT_ABX_R_DUR = 5
PYELO_OUT_DUR = 7