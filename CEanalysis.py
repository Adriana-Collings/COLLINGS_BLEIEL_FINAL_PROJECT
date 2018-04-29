import No_treatment as NoTreat
import Acupuncture_treatment as Acu
import Cranberry_treatment as Cran
import Daily_antibiotic_treatment as ABX
import Estrogen_treatment as Estro
import scr.EconEvalClasses as Econ

def report_CEA_CBA_single(cohort_no_treat,cohort_acu,cohort_cran,cohort_abx,cohort_estro):
    no_treatment_strategy = Econ.Strategy(
        name="No treatment",
        cost_obs=cohort_no_treat.get_ave_total_cost(),
        effect_obs=cohort_no_treat.get_ave_number_utis()
    )

    acu_strategy = Econ.Strategy(
        name="Acupunture",
        cost_obs=cohort_acu.get_ave_total_cost(),
        effect_obs=cohort_acu.get_ave_number_utis()
    )

    cran_strategy = Econ.Strategy(
        name="Cranberry",
        cost_obs=cohort_cran.get_ave_total_cost(),
        effect_obs=cohort_cran.get_ave_number_utis()
    )

    abx_strategy = Econ.Strategy(
        name="Antibiotics",
        cost_obs=cohort_abx.get_ave_total_cost(),
        effect_obs=cohort_abx.get_ave_number_utis()
    )

    estro_strategy = Econ.Strategy(
        name="Estrogen",
        cost_obs=cohort_estro.get_ave_total_cost(),
        effect_obs=cohort_estro.get_ave_number_utis()
    )

    CEA=Econ.CEA(
        strategies=[no_treatment_strategy,acu_strategy,cran_strategy,abx_strategy,estro_strategy],
        if_paired=False
    )
    CEA.show_CE_plane(
        title='Cost-Effectiveness Analysis',
        x_label='Difference in total number of UTIs',
        y_label='Difference in total cost',
        show_names=True,
        show_clouds=True,
        show_legend=True,
        figure_size=6,
        transparency=0.3
    )

