from pyomo import environ as po
from pyomo import dae as pod
import numpy as np
from matplotlib import pyplot as plt


def create_model(sampling_times):
    model = po.ConcreteModel()
    model.t = pod.ContinuousSet(bounds=(0, 1), initialize=sampling_times)
    model.tau = po.Var()
    model.temp = po.Var()

    # state variables
    model.ca = po.Var(model.t, bounds=(0, 50))
    model.cb = po.Var(model.t, bounds=(0, 50))
    model.dca_dt = pod.DerivativeVar(model.ca, wrt=model.t)
    model.dcb_dt = pod.DerivativeVar(model.cb, wrt=model.t)

    # modelparameters
    model.theta_0 = po.Var()
    model.theta_1 = po.Var()
    model.alpha_a = po.Var()
    model.alpha_b = po.Var()
    model.nu = po.Var()

    def _material_balance_a(m, t):
        k = po.exp(m.theta_0 + m.theta_1 * (m.temp - 273.15) / m.temp)
        return m.dca_dt[t] / m.tau == -k * (m.ca[t] ** model.alpha_a) * (model.cb[t] ** model.alpha_b)

    model.material_balance_a = po.Constraint(model.t, rule=_material_balance_a)

    def _material_balance_b(m, t):
        k = po.exp(m.theta_0 + m.theta_1 * (m.temp - 273.15) / m.temp)
        return m.dcb_dt[t] / m.tau == k * m.nu * (m.ca[t] ** model.alpha_a) * (model.cb[t] ** model.alpha_b)

    model.material_balance_b = po.Constraint(model.t, rule=_material_balance_b)

    simulator = pod.Simulator(model, package='casadi')

    return model, simulator


def simulate(ti_controls, sampling_times, model_parameters):
    model, simulator = create_model(sampling_times)

    # fixing the model parameters
    model.theta_0.fix(model_parameters[0])
    model.theta_1.fix(model_parameters[1])
    model.alpha_a.fix(model_parameters[2])
    model.alpha_b.fix(0)
    model.nu.fix(model_parameters[3])

    # fixing the control variables
    model.tau.fix(200)
    model.ca[0].fix(ti_controls[0])
    model.cb[0].fix(0)
    model.temp.fix(ti_controls[1])

    # simulating
    simulator.simulate(integrator='idas')
    simulator.initialize_model()

    ca = np.array([model.ca[t].value for t in model.t])
    cb = np.array([model.cb[t].value for t in model.t])

    return np.array([ca, cb]).T


def plot_ode_model(ti_controls, sampling_times, model_parameters):
    y = simulate(
        ti_controls,
        sampling_times,
        model_parameters,
    )
    fig = plt.figure()
    axes = fig.add_subplot(111)
    axes.plot(
        sampling_times,
        y[:, 0],
        label="$C_A$",
    )
    axes.plot(
        sampling_times,
        y[:, 1],
        label="$C_B$",
    )
    axes.legend()
    plt.show(block= False)



