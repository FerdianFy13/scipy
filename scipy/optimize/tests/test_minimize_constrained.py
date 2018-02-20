from __future__ import division, print_function, absolute_import
import numpy as np
import pytest
from scipy.linalg import block_diag
from scipy.sparse import csc_matrix
from numpy.testing import (TestCase, assert_array_almost_equal,
                           assert_array_less)
from pytest import raises
from scipy.optimize import (NonlinearConstraint,
                            LinearConstraint,
                            Bounds,
                            minimize,
                            BFGS,
                            SR1)


class Maratos:
    """Problem 15.4 from Nocedal and Wright

    The following optimization problem:
        minimize 2*(x[0]**2 + x[1]**2 - 1) - x[0]
        Subject to: x[0]**2 + x[1]**2 - 1 = 0
    """

    def __init__(self, degrees=60, constr_jac=None, constr_hess=None):
        rads = degrees/180*np.pi
        self.x0 = [np.cos(rads), np.sin(rads)]
        self.x_opt = np.array([1.0, 0.0])
        self.constr_jac = constr_jac
        self.constr_hess = constr_hess
        self.bounds = None

    def fun(self, x):
        return 2*(x[0]**2 + x[1]**2 - 1) - x[0]

    def grad(self, x):
        return np.array([4*x[0]-1, 4*x[1]])

    def hess(self, x):
        return 4*np.eye(2)

    @property
    def constr(self):
        def fun(x):
            return x[0]**2 + x[1]**2

        if self.constr_jac is None:
            def jac(x):
                return [[2*x[0], 2*x[1]]]
        else:
            jac = self.constr_jac

        if self.constr_hess is None:
            def hess(x, v):
                return 2*v[0]*np.eye(2)
        else:
            hess = self.constr_hess

        return NonlinearConstraint(fun, 1, 1, jac, hess)


class MaratosTestArgs:
    """Problem 15.4 from Nocedal and Wright

    The following optimization problem:
        minimize 2*(x[0]**2 + x[1]**2 - 1) - x[0]
        Subject to: x[0]**2 + x[1]**2 - 1 = 0
    """

    def __init__(self, a, b, degrees=60, constr_jac=None, constr_hess=None):
        rads = degrees/180*np.pi
        self.x0 = [np.cos(rads), np.sin(rads)]
        self.x_opt = np.array([1.0, 0.0])
        self.constr_jac = constr_jac
        self.constr_hess = constr_hess
        self.a = a
        self.b = b
        self.bounds = None

    def _test_args(self, a, b):
        if self.a != a or self.b != b:
            raise ValueError()

    def fun(self, x, a, b):
        self._test_args(a, b)
        return 2*(x[0]**2 + x[1]**2 - 1) - x[0]

    def grad(self, x, a, b):
        self._test_args(a, b)
        return np.array([4*x[0]-1, 4*x[1]])

    def hess(self, x, a, b):
        self._test_args(a, b)
        return 4*np.eye(2)

    @property
    def constr(self):
        def fun(x):
            return x[0]**2 + x[1]**2

        if self.constr_jac is None:
            def jac(x):
                return [[4*x[0], 4*x[1]]]
        else:
            jac = self.constr_jac

        if self.constr_hess is None:
            def hess(x, v):
                return 2*v[0]*np.eye(2)
        else:
            hess = self.constr_hess

        return NonlinearConstraint(fun, 1, 1, jac, hess)


class MaratosGradInFunc:
    """Problem 15.4 from Nocedal and Wright

    The following optimization problem:
        minimize 2*(x[0]**2 + x[1]**2 - 1) - x[0]
        Subject to: x[0]**2 + x[1]**2 - 1 = 0
    """

    def __init__(self, degrees=60, constr_jac=None, constr_hess=None):
        rads = degrees/180*np.pi
        self.x0 = [np.cos(rads), np.sin(rads)]
        self.x_opt = np.array([1.0, 0.0])
        self.constr_jac = constr_jac
        self.constr_hess = constr_hess
        self.bounds = None

    def fun(self, x):
        return (2*(x[0]**2 + x[1]**2 - 1) - x[0],
                np.array([4*x[0]-1, 4*x[1]]))

    @property
    def grad(self):
        return True

    def hess(self, x):
        return 4*np.eye(2)

    @property
    def constr(self):
        def fun(x):
            return x[0]**2 + x[1]**2

        if self.constr_jac is None:
            def jac(x):
                return [[4*x[0], 4*x[1]]]
        else:
            jac = self.constr_jac

        if self.constr_hess is None:
            def hess(x, v):
                return 2*v[0]*np.eye(2)
        else:
            hess = self.constr_hess

        return NonlinearConstraint(fun, 1, 1, jac, hess)


class HyperbolicIneq:
    """Problem 15.1 from Nocedal and Wright

    The following optimization problem:
        minimize 1/2*(x[0] - 2)**2 + 1/2*(x[1] - 1/2)**2
        Subject to: 1/(x[0] + 1) - x[1] >= 1/4
                                   x[0] >= 0
                                   x[1] >= 0
    """
    def __init__(self, constr_jac=None, constr_hess=None):
        self.x0 = [0, 0]
        self.x_opt = [1.952823, 0.088659]
        self.constr_jac = constr_jac
        self.constr_hess = constr_hess
        self.bounds = Bounds(0, np.inf)

    def fun(self, x):
        return 1/2*(x[0] - 2)**2 + 1/2*(x[1] - 1/2)**2

    def grad(self, x):
        return [x[0] - 2, x[1] - 1/2]

    def hess(self, x):
        return np.eye(2)

    @property
    def constr(self):
        def fun(x):
            return 1/(x[0] + 1) - x[1]

        if self.constr_jac is None:
            def jac(x):
                return [[-1/(x[0] + 1)**2, -1]]
        else:
            jac = self.constr_jac

        if self.constr_hess is None:
            def hess(x, v):
                return 2*v[0]*np.array([[1/(x[0] + 1)**3, 0],
                                        [0, 0]])
        else:
            hess = self.constr_hess

        return NonlinearConstraint(fun, 0.25, np.inf, jac, hess)


class Rosenbrock:
    """Rosenbrock function.

    The following optimization problem:
        minimize sum(100.0*(x[1:] - x[:-1]**2.0)**2.0 + (1 - x[:-1])**2.0)
    """

    def __init__(self, n=2, random_state=0):
        rng = np.random.RandomState(random_state)
        self.x0 = rng.uniform(-1, 1, n)
        self.x_opt = np.ones(n)
        self.bounds = None

    def fun(self, x):
        x = np.asarray(x)
        r = np.sum(100.0 * (x[1:] - x[:-1]**2.0)**2.0 + (1 - x[:-1])**2.0,
                   axis=0)
        return r

    def grad(self, x):
        x = np.asarray(x)
        xm = x[1:-1]
        xm_m1 = x[:-2]
        xm_p1 = x[2:]
        der = np.zeros_like(x)
        der[1:-1] = (200 * (xm - xm_m1**2) -
                     400 * (xm_p1 - xm**2) * xm - 2 * (1 - xm))
        der[0] = -400 * x[0] * (x[1] - x[0]**2) - 2 * (1 - x[0])
        der[-1] = 200 * (x[-1] - x[-2]**2)
        return der

    def hess(self, x):
        x = np.atleast_1d(x)
        H = np.diag(-400 * x[:-1], 1) - np.diag(400 * x[:-1], -1)
        diagonal = np.zeros(len(x), dtype=x.dtype)
        diagonal[0] = 1200 * x[0]**2 - 400 * x[1] + 2
        diagonal[-1] = 200
        diagonal[1:-1] = 202 + 1200 * x[1:-1]**2 - 400 * x[2:]
        H = H + np.diag(diagonal)
        return H

    @property
    def constr(self):
        return ()


class IneqRosenbrock(Rosenbrock):
    """Rosenbrock subject to inequality constraints.

    The following optimization problem:
        minimize sum(100.0*(x[1] - x[0]**2)**2.0 + (1 - x[0])**2)
        subject to: x[0] + 2 x[1] <= 1

    Taken from matlab ``fmincon`` documentation.
    """
    def __init__(self, random_state=0):
        Rosenbrock.__init__(self, 2, random_state)
        self.x0 = [-1, -0.5]
        self.x_opt = [0.5022, 0.2489]
        self.bounds = None

    @property
    def constr(self):
        A = [[1, 2]]
        b = 1
        return LinearConstraint(A, -np.inf, b)


class EqIneqRosenbrock(Rosenbrock):
    """Rosenbrock subject to equality and inequality constraints.

    The following optimization problem:
        minimize sum(100.0*(x[1] - x[0]**2)**2.0 + (1 - x[0])**2)
        subject to: x[0] + 2 x[1] <= 1
                    2 x[0] + x[1] = 1

    Taken from matlab ``fimincon`` documentation.
    """
    def __init__(self, random_state=0):
        Rosenbrock.__init__(self, 2, random_state)
        self.x0 = [-1, -0.5]
        self.x_opt = [0.41494, 0.17011]
        self.bounds = None

    @property
    def constr(self):
        A_ineq = [[1, 2]]
        b_ineq = 1
        A_eq = [[2, 1]]
        b_eq = 1
        return (LinearConstraint(A_ineq, -np.inf, b_ineq),
                LinearConstraint(A_eq, b_eq, b_eq))


class Elec:
    """Distribution of electrons on a sphere.

    Problem no 2 from COPS collection [2]_. Find
    the equilibrium state distribution (of minimal
    potential) of the electrons positioned on a
    conducting sphere.

    References
    ----------
    .. [1] E. D. Dolan, J. J. Mor\'{e}, and T. S. Munson,
           "Benchmarking optimization software with COPS 3.0.",
            Argonne National Lab., Argonne, IL (US), 2004.
    """
    def __init__(self, n_electrons=200, random_state=0,
                 constr_jac=None, constr_hess=None):
        self.n_electrons = n_electrons
        self.rng = np.random.RandomState(random_state)
        # Initial Guess
        phi = self.rng.uniform(0, 2 * np.pi, self.n_electrons)
        theta = self.rng.uniform(-np.pi, np.pi, self.n_electrons)
        x = np.cos(theta) * np.cos(phi)
        y = np.cos(theta) * np.sin(phi)
        z = np.sin(theta)
        self.x0 = np.hstack((x, y, z))
        self.x_opt = None
        self.constr_jac = constr_jac
        self.constr_hess = constr_hess
        self.bounds = None

    def _get_cordinates(self, x):
        x_coord = x[:self.n_electrons]
        y_coord = x[self.n_electrons:2 * self.n_electrons]
        z_coord = x[2 * self.n_electrons:]
        return x_coord, y_coord, z_coord

    def _compute_coordinate_deltas(self, x):
        x_coord, y_coord, z_coord = self._get_cordinates(x)
        dx = x_coord[:, None] - x_coord
        dy = y_coord[:, None] - y_coord
        dz = z_coord[:, None] - z_coord
        return dx, dy, dz

    def fun(self, x):
        dx, dy, dz = self._compute_coordinate_deltas(x)
        with np.errstate(divide='ignore'):
            dm1 = (dx**2 + dy**2 + dz**2) ** -0.5
        dm1[np.diag_indices_from(dm1)] = 0
        return 0.5 * np.sum(dm1)

    def grad(self, x):
        dx, dy, dz = self._compute_coordinate_deltas(x)

        with np.errstate(divide='ignore'):
            dm3 = (dx**2 + dy**2 + dz**2) ** -1.5
        dm3[np.diag_indices_from(dm3)] = 0

        grad_x = -np.sum(dx * dm3, axis=1)
        grad_y = -np.sum(dy * dm3, axis=1)
        grad_z = -np.sum(dz * dm3, axis=1)

        return np.hstack((grad_x, grad_y, grad_z))

    def hess(self, x):
        dx, dy, dz = self._compute_coordinate_deltas(x)
        d = (dx**2 + dy**2 + dz**2) ** 0.5

        with np.errstate(divide='ignore'):
            dm3 = d ** -3
            dm5 = d ** -5

        i = np.arange(self.n_electrons)
        dm3[i, i] = 0
        dm5[i, i] = 0

        Hxx = dm3 - 3 * dx**2 * dm5
        Hxx[i, i] = -np.sum(Hxx, axis=1)

        Hxy = -3 * dx * dy * dm5
        Hxy[i, i] = -np.sum(Hxy, axis=1)

        Hxz = -3 * dx * dz * dm5
        Hxz[i, i] = -np.sum(Hxz, axis=1)

        Hyy = dm3 - 3 * dy**2 * dm5
        Hyy[i, i] = -np.sum(Hyy, axis=1)

        Hyz = -3 * dy * dz * dm5
        Hyz[i, i] = -np.sum(Hyz, axis=1)

        Hzz = dm3 - 3 * dz**2 * dm5
        Hzz[i, i] = -np.sum(Hzz, axis=1)

        H = np.vstack((
            np.hstack((Hxx, Hxy, Hxz)),
            np.hstack((Hxy, Hyy, Hyz)),
            np.hstack((Hxz, Hyz, Hzz))
        ))

        return H

    @property
    def constr(self):
        def fun(x):
            x_coord, y_coord, z_coord = self._get_cordinates(x)
            return x_coord**2 + y_coord**2 + z_coord**2 - 1

        if self.constr_jac is None:
            def jac(x):
                x_coord, y_coord, z_coord = self._get_cordinates(x)
                Jx = 2 * np.diag(x_coord)
                Jy = 2 * np.diag(y_coord)
                Jz = 2 * np.diag(z_coord)
                return csc_matrix(np.hstack((Jx, Jy, Jz)))
        else:
            jac = self.constr_jac

        if self.constr_hess is None:
            def hess(x, v):
                D = 2 * np.diag(v)
                return block_diag(D, D, D)
        else:
            hess = self.constr_hess

        return NonlinearConstraint(fun, -np.inf, 0, jac, hess)


class TestTrustRegionConstr(TestCase):

    def test_list_of_problems(self):
        list_of_problems = [Maratos(),
                            Maratos(constr_hess='2-point'),
                            Maratos(constr_hess=SR1()),
                            Maratos(constr_jac='2-point', constr_hess=SR1()),
                            MaratosGradInFunc(),
                            HyperbolicIneq(),
                            HyperbolicIneq(constr_hess='3-point'),
                            HyperbolicIneq(constr_hess=BFGS()),
                            HyperbolicIneq(constr_jac='3-point',
                                           constr_hess=BFGS()),
                            Rosenbrock(),
                            IneqRosenbrock(),
                            EqIneqRosenbrock(),
                            Elec(n_electrons=2),
                            Elec(n_electrons=2, constr_hess='2-point'),
                            Elec(n_electrons=2, constr_hess=SR1()),
                            Elec(n_electrons=2, constr_jac='3-point',
                                 constr_hess=SR1())]

        for prob in list_of_problems:
            for grad in (prob.grad, '3-point', False):
                for hess in (prob.hess,
                             '3-point',
                             SR1(),
                             BFGS(exception_strategy='damped_bfgs'),
                             BFGS(exception_strategy='skip_update')):

                    # Remove exceptions
                    if grad in ('2-point', '3-point', 'cs', False) and \
                       hess in ('2-point', '3-point', 'cs'):
                        continue
                    if prob.grad is True and grad in ('3-point', False):
                        continue

                    result = minimize(prob.fun, prob.x0,
                                      method='trust-constr',
                                      jac=grad, hess=hess,
                                      bounds=prob.bounds,
                                      constraints=prob.constr)

                    if prob.x_opt is not None:
                        assert_array_almost_equal(result.x, prob.x_opt, decimal=5)
                        # gtol
                        if result.status == 1:
                            assert_array_less(result.optimality, 1e-8)
                    # xtol
                    if result.status == 2:
                        assert_array_less(result.tr_radius, 1e-8)

                        if result.method == "tr_interior_point":
                            assert_array_less(result.barrier_parameter, 1e-8)
                    # max iter
                    if result.status in (0, 3):
                        raise RuntimeError("Invalid termination condition.")

    def test_no_constraints(self):
        prob = Rosenbrock()
        result = minimize(prob.fun, prob.x0,
                          method='trust-constr',
                          jac=prob.grad, hess=prob.hess)
        result1 = minimize(prob.fun, prob.x0,
                           method='L-BFGS-B',
                           jac='2-point')
        with pytest.warns(UserWarning):
            result2 = minimize(prob.fun, prob.x0,
                                method='L-BFGS-B',
                                jac='3-point')
        assert_array_almost_equal(result.x, prob.x_opt, decimal=5)
        assert_array_almost_equal(result1.x, prob.x_opt, decimal=5)
        assert_array_almost_equal(result2.x, prob.x_opt, decimal=5)

    def test_hessp(self):
        prob = Maratos()

        def hessp(x, p):
            H = prob.hess(x)
            return H.dot(p)

        result = minimize(prob.fun, prob.x0,
                          method='trust-constr',
                          jac=prob.grad, hessp=hessp,
                          bounds=prob.bounds,
                          constraints=prob.constr)

        if prob.x_opt is not None:
            assert_array_almost_equal(result.x, prob.x_opt, decimal=2)

        # gtol
        if result.status == 1:
            assert_array_less(result.optimality, 1e-8)
        # xtol
        if result.status == 2:
            assert_array_less(result.tr_radius, 1e-8)

            if result.method == "tr_interior_point":
                assert_array_less(result.barrier_parameter, 1e-8)
        # max iter
        if result.status in (0, 3):
            raise RuntimeError("Invalid termination condition.")

    def test_args(self):
        prob = MaratosTestArgs("a", 234)

        result = minimize(prob.fun, prob.x0, ("a", 234),
                          method='trust-constr',
                          jac=prob.grad, hess=prob.hess,
                          bounds=prob.bounds,
                          constraints=prob.constr)

        if prob.x_opt is not None:
            assert_array_almost_equal(result.x, prob.x_opt, decimal=2)

        # gtol
        if result.status == 1:
            assert_array_less(result.optimality, 1e-8)
        # xtol
        if result.status == 2:
            assert_array_less(result.tr_radius, 1e-8)

            if result.method == "tr_interior_point":
                assert_array_less(result.barrier_parameter, 1e-8)
        # max iter
        if result.status in (0, 3):
            raise RuntimeError("Invalid termination condition.")

    def test_raise_exception(self):
        prob = Maratos()

        raises(ValueError, minimize, prob.fun, prob.x0, method='trust-constr',
               jac='2-point', hess='2-point', constraints=prob.constr)
