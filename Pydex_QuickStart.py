from pydex.core.designer import Designer
from matplotlib import pyplot as plt
import numpy as np


def model(ti_controls, model_parameters):
    return np.array([
        # constant term
        model_parameters[0] +
        # linear term
        model_parameters[1] * ti_controls[0] +
        model_parameters[2] * ti_controls[1] +
        model_parameters[3] * ti_controls[0] * ti_controls[1] +
        model_parameters[4] * ti_controls[0] ** 2 +
        model_parameters[5] * ti_controls[1] ** 2
    ])


# testing model
y = model(ti_controls=[1, 2], model_parameters=[1, 2, 3, 4, 5, 6])
print(y)

designer_1 = Designer()
designer_1.simulate = model

designer_1.model_parameters = np.ones(6)

bounds = [[-1, 1], [-1, 1], ]
levels = [6, 6, ]
tic = designer_1.enumerate_candidates(bounds, [6, 6, ])
print(np.array2string(tic, separator=","))

designer_1.ti_controls_candidates = tic

designer_1.initialize(verbose=2)

result = designer_1.design_experiment(criterion=designer_1.d_opt_criterion, package="scipy", optimizer="SLSQP", )

designer_1.print_optimal_candidates(write=False)

designer_1.plot_optimal_controls(non_opt_candidates=True)

designer_1.show_plots()


#Iterate
for i in range(3):
    finalcandidates = []
    for optimal_candidate in designer_1.optimal_candidates:
        boundsAroundCandidates =[]
        for x in range(len(levels)):
            delta = (bounds[x][1] - bounds[x][0]) / ((levels[x] - 1) * 2)/2**i
            optimal_candidate[1]
            if optimal_candidate[1][x] == bounds[x][0]:
                #newcandidates = designer_1.enumerate_candidates([optimal_candidates[x], optimal_candidates[x] + delta], [6, 6, ])
                newbounds = [optimal_candidate[1][x], optimal_candidate[1][x] + delta]
            elif optimal_candidate[1][x] == bounds[x][1]:
                #newcandidates = designer_1.enumerate_candidates([optimal_candidates[x] - delta, optimal_candidates[x]], [6, 6, ])
                newbounds = [optimal_candidate[1][x] - delta, optimal_candidate[1][x]]
            else:
                #newcandidates = designer_1.enumerate_candidates([optimal_candidates[x] - delta, optimal_candidates[x] + delta], [6, 6, ])
                newbounds = [optimal_candidate[1][x] - delta, optimal_candidate[1][x] + delta]
            boundsAroundCandidates.append(newbounds)
        newcandidates = designer_1.enumerate_candidates(boundsAroundCandidates, [3,3,])
        newcandidateslist = newcandidates.tolist()
        finalcandidates.append(newcandidates)

    mat = np.concatenate(finalcandidates)

    designer_1.ti_controls_candidates = mat

    designer_1.initialize(verbose=2)

    result = designer_1.design_experiment(criterion=designer_1.d_opt_criterion, package="scipy", optimizer="SLSQP", )

    designer_1.print_optimal_candidates(write=False)

    designer_1.plot_optimal_controls(non_opt_candidates=True)

    designer_1.show_plots()