from pydex.core.designer import Designer
from matplotlib import pyplot as plt
import numpy as np
import Pydex_ODE_Model as pyMod

ti_controls = [1, 300.15]
spt = np.linspace(0, 1, 11)
theta_nom = [-4.5, 2.2, 1.0, 0.5]
#theta_nom = np.random.multivariate_normal(
#    mean=[-4.5, 2.2, 1.0, 0.5],
#    cov=[
#        [0.10, 0.0, 0.0, 0.0,],
#        [0.0, 0.10, 0.0, 0.0],
#        [0.0, 0.0, .10, 0.0],
#        [0.0, 0.0, 0.0, 0.01],
#    ],
#    size=100,
#)
#theta_nom[:, 2] = np.round(theta_nom[:, 2])
pyMod.plot_ode_model(ti_controls, spt, theta_nom)

designer_1 = Designer()
designer_1.simulate = pyMod.simulate
designer_1.model_parameters = theta_nom

tic = designer_1.enumerate_candidates(bounds=[[1, 5], [273.15, 323.15], ], levels=[5, 5])

designer_1.ti_controls_candidates = tic

print(np.array2string(tic, separator=','))

figure2 = plt.figure(2)
plt.scatter(tic[:, 0], tic[:, 1], )
plt.xlabel(r"$C_A^0\quad (\frac{mol}{L})$")
plt.ylabel("$T\quad (k)$")

spt = np.array([np.linspace(0, 1, 11) for _ in tic])
designer_1.sampling_times_candidates = spt
print(np.array2string(spt, separator=","))

designer_1.initialize(verbose=2)

designer_1.measurable_responses = [0, 1]

designer_1.candidate_names = np.array([f"Candidate {i + 1}" for i, _ in enumerate(tic)])

designer_1.response_names = ["c_A", "c_B"]
designer_1.model_parameter_names = [
    r"\theta_0",
    r"\theta_1",
    r"\alpha",
    r"\nu",
]

package = "scipy"  # @param ["scipy", "cvxpy"]
optimizer = "SLSQP"  # @param ["SCS", "SLSQP", "l-bfgs-b", "bfgs", "nelder-mead", "TNC", "COBYLA", "MOSEK"]

""" solve OED problem """
criterion = designer_1.d_opt_criterion
scipy_result = designer_1.design_experiment(
    criterion=criterion,
    package=package,
    optimizer=optimizer,
    optimize_sampling_times=False,
    write=False,
)

plt.show()

designer_1.print_optimal_candidates(
    write=False,
)

designer_1.plot_optimal_efforts()

designer_1.plot_optimal_efforts(force_3d=True)


designer_1.plot_optimal_predictions()


designer_1.plot_optimal_sensitivities(interactive=False)
designer_1.show_plots()
