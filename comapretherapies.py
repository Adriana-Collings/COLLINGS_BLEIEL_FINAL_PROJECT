import No_treatment as NoTreat
import Acupuncture_treatment as Acu
import Cranberry_treatment as Cran
import Daily_antibiotic_treatment as ABX
import Estrogen_treatment as Estro
import CEanalysis as CE


POP_SIZE=10000
N_OF_DAYS=365
ALPHA=0.05



MyCohort=NoTreat.Cohort(id=1, pop_size=POP_SIZE)
cohort_no_treat = MyCohort.simulate(N_OF_DAYS)
print("No Treatment")

print('AVERAGE TOTAL COST:', cohort_no_treat.get_ave_total_cost())

print("")












