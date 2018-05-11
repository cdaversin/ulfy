from dolfin import *
from ufl_mms import Expression
import sympy as sp
import ufl


def test_ufl_mms_1d():
    '''
    Let f a sympy polynomial expression, df = Expression(f), v = interpolate(f, V)
    where V is a suitable polynomial space. If e=e(v) is a UFL expression 
    then Expression(e, {v: f}) should be very close.
    '''
    check = lambda a, b: sqrt(abs(assemble(inner(a-b, a-b)*dx))) < 1E-10
    
    x, y, z, t = sp.symbols('x y z t')

    f = 3*x + t
    df = Expression(f, degree=1)
    df.t = 2.

    mesh = UnitIntervalMesh(1000)
    V = FunctionSpace(mesh, 'CG', 1)
    v = interpolate(df, V)

    DEG = 10  # Degree for the final expression; high to get accuracy

    e = v + 3*v
    e_ = Expression(e, subs={v: f}, degree=DEG)
    e_.t = 2.
    assert check(e, e_)

    e = v - 3*v**2
    e_ = Expression(e, subs={v: f}, degree=DEG)
    e_.t = 2.
    assert check(e, e_)

    e = v - 3*v**2 + v.dx(0)
    e_ = Expression(e, subs={v: f}, degree=DEG)
    e_.t = 2.
    assert check(e, e_)

    e = v - 3*v**2 + sin(v).dx(0)
    e_ = Expression(e, subs={v: f}, degree=DEG)
    e_.t = 2.
    assert check(e, e_)

    e = v - 3*v**2 + cos(v)*v.dx(0)
    e_ = Expression(e, subs={v: f}, degree=DEG)
    e_.t = 2.
    assert check(e, e_)


def test_ufl_mms_2d():
    '''
    Let f a sympy polynomial expression, df = Expression(f), v = interpolate(f, V)
    where V is a suitable polynomial space. If e=e(v) is a UFL expression 
    then Expression(e, {v: f}) should be very close.
    '''
    check = lambda a, b: sqrt(abs(assemble(inner(a-b, a-b)*dx))) < 1E-8
    
    x, y, z, t = sp.symbols('x y z t')
    T = 1.2
    
    f = 3*x*y + x**2 + 2*y**2 + t**3
    df = Expression(f, degree=2)
    df.t = T

    g = x+y
    dg = Expression(g, degree=1)

    mesh = UnitSquareMesh(64, 64)
    V = FunctionSpace(mesh, 'CG', 2)
    v = interpolate(df, V)
    u = interpolate(dg, V)

    DEG = 6  # Degree for the final expression; high to get accuracy

    e = u + v
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = u.dx(0) + v.dx(1)
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = grad(u) + grad(v)
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = div(grad(u)) + div(grad(v))
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    uv = as_vector((u, v))
    e = grad(grad(u+v)) + outer(uv, uv)
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = inner(grad(u), grad(v))
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    uv = as_vector((u, v))
    e = det(grad(grad(u+v)))# + tr(outer(uv, 2*uv))
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    uv = as_vector((u, v))
    e = uv
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = tr(outer(uv, 2*uv))
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = det(outer(uv, 2*uv))
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = 2*uv
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = curl(u) + 2*curl(v)
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = curl(grad(u*u)) + 2*curl(grad(v*u))
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    x, y = SpatialCoordinate(mesh)
    e = curl(as_vector((-y**2, x**2)))
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = div(outer(uv, 2*uv))
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    
def test_ufl_mms_2d_vec():
    '''
    Let f a sympy polynomial expression, df = Expression(f), v = interpolate(f, V)
    where V is a suitable polynomial space. If e=e(v) is a UFL expression 
    then Expression(e, {v: f}) should be very close.
    '''
    check = lambda a, b: sqrt(abs(assemble(inner(a-b, a-b)*dx))) < 1E-8
    
    x, y, z, t = sp.symbols('x y z t')
    T = 1.2
    
    f = sp.Matrix([3*x*y + x**2 + 2*y**2 + t**3,
                   x+y])
    df = Expression(f, degree=2)
    df.t = T

    g = sp.Matrix([x+y, 1])
    dg = Expression(g, degree=1)

    mesh = UnitSquareMesh(32, 32)
    V = VectorFunctionSpace(mesh, 'CG', 2)
    v = interpolate(df, V)
    u = interpolate(dg, V)

    DEG = 6

    e = u + v
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = inner(u, v)
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    R = Constant(((1, 2), (3, 4)))
    # e = R*u
    # e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    # e_.t = T
    # print check(e, e_)

    e = dot(R, u)
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = dot(v, R)
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = grad(u+v)
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = div(u - v)
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    
def test_ufl_mms_2d_mat():
    '''
    Let f a sympy polynomial expression, df = Expression(f), v = interpolate(f, V)
    where V is a suitable polynomial space. If e=e(v) is a UFL expression 
    then Expression(e, {v: f}) should be very close.
    '''
    check = lambda a, b: sqrt(abs(assemble(inner(a-b, a-b)*dx))) < 1E-8
    
    x, y, z, t = sp.symbols('x y z t')
    T = 1.2
    
    f = sp.Matrix([[3*x*y + x**2 + 2*y**2 + t**3, x],
                   [y, x+y]])
    df = Expression(f, degree=2)
    df.t = T

    g = sp.Matrix([[x+y, 1], [y, -x]])
    dg = Expression(g, degree=1)

    mesh = UnitSquareMesh(32, 32)
    V = TensorFunctionSpace(mesh, 'CG', 2)
    v = interpolate(df, V)
    u = interpolate(dg, V)

    DEG = 6

    e = u + v
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = inner(u, v)
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    # R = Constant(((1, 2), (3, 4)))
    # e = R*u
    # e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    # e_.t = T
    # print check(e, e_)

    e = det(u)
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = tr(dot(u, v))
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = div(u+v)
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    
def test_ufl_mms_3d():
    '''
    Let f a sympy polynomial expression, df = Expression(f), v = interpolate(f, V)
    where V is a suitable polynomial space. If e=e(v) is a UFL expression 
    then Expression(e, {v: f}) should be very close.
    '''
    check = lambda a, b: sqrt(abs(assemble(inner(a-b, a-b)*dx))) < 1E-8
    
    x, y, z, t = sp.symbols('x y z t')
    T = 1.2
    
    f = 3*x*y + x**2 + 2*y**2 + x*y - 2*z**2 + 4*y*z + t**3
    df = Expression(f, degree=2)
    df.t = T

    g = x+y+z
    dg = Expression(g, degree=1)

    mesh = UnitCubeMesh(8, 8, 8)
    V = FunctionSpace(mesh, 'CG', 2)
    v = interpolate(df, V)
    u = interpolate(dg, V)

    DEG = 4  # Degree for the final expression; high to get accuracy

    e = u + v
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = u.dx(0) + v.dx(1)
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = grad(u) + grad(v)
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = div(grad(u)) + div(grad(v))
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    uv = as_vector((u, v, u+v))
    e = grad(grad(u+v)) + outer(uv, uv)
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = inner(grad(u), grad(v))
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = det(grad(grad(u+v))) + tr(outer(uv, 2*uv))
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = uv
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = tr(outer(uv, 2*uv))
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = det(outer(uv, 2*uv))
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = 2*uv
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = curl(u) + 2*curl(v)
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = curl(grad(u*u)) + 2*curl(grad(v*u))
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    x, y, z = SpatialCoordinate(mesh)
    e = curl(as_vector((-y**2, x**2, z)))
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = div(outer(uv, 2*uv))
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    
def test_ufl_mms_3d_vec():
    '''
    Let f a sympy polynomial expression, df = Expression(f), v = interpolate(f, V)
    where V is a suitable polynomial space. If e=e(v) is a UFL expression 
    then Expression(e, {v: f}) should be very close.
    '''
    check = lambda a, b: sqrt(abs(assemble(inner(a-b, a-b)*dx))) < 1E-8
    
    x, y, z, t = sp.symbols('x y z t')
    T = 1.2
    
    f = sp.Matrix([3*x*y + x*z + 2*y*z + t**3 + z**2 - x**2,
                   x+y*z,
                   y-z])
    df = Expression(f, degree=2)
    df.t = T

    g = sp.Matrix([x+y+z, x-y-z, y])
    dg = Expression(g, degree=1)

    mesh = UnitCubeMesh(8, 8, 8)
    V = VectorFunctionSpace(mesh, 'CG', 2)
    v = interpolate(df, V)
    u = interpolate(dg, V)

    DEG = 3

    e = u + v
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = inner(u, v)
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    R = Constant(((1, 2, 0), (0, 3, 4), (0, 0, 1)))
    # e = R*u
    # e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    # e_.t = T
    # print check(e, e_)

    e = dot(R, u)
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = dot(v, R)
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = grad(u+v)
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = div(u - v)
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = curl(2*u - 3*v)
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)


def test_ufl_mms_3d_mat():
    '''
    Let f a sympy polynomial expression, df = Expression(f), v = interpolate(f, V)
    where V is a suitable polynomial space. If e=e(v) is a UFL expression 
    then Expression(e, {v: f}) should be very close.
    '''
    check = lambda a, b: sqrt(abs(assemble(inner(a-b, a-b)*dx))) < 1E-8
    
    x, y, z, t = sp.symbols('x y z t')
    T = 0.123
    
    f = sp.Matrix([[3*x, x, z],
                   [y, x, z],
                   [x, y-y, z]])
    df = Expression(f, degree=1)
    df.t = T

    g = sp.Matrix([[x+y, 1, x],
                   [y, -x, z],
                   [x+y, y+z, z-x]])
    dg = Expression(g, degree=1)

    mesh = UnitCubeMesh(8, 8, 8)
    V = TensorFunctionSpace(mesh, 'CG', 1)
    v = interpolate(df, V)
    u = interpolate(dg, V)

    DEG = 3

    e = u + v
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = inner(u, v)
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    # R = Constant(((1, 2), (3, 4)))
    # e = R*u
    # e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    # e_.t = T
    # print check(e, e_)

    e = det(u)
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = tr(dot(u, v))
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    e = div(u+v)
    e_ = Expression(e, subs={v: f, u: g}, degree=DEG)
    e_.t = T
    assert check(e, e_)

    
def test_conditional():
    '''
    Let f a sympy polynomial expression, df = Expression(f), v = interpolate(f, V)
    where V is a suitable polynomial space. If e=e(v) is a UFL expression 
    then Expression(e, {v: f}) should be very close.
    '''
    check = lambda a, b: sqrt(abs(assemble(inner(a-b, a-b)*dx))) < 1E-10
    
    x, y, z, t = sp.symbols('x y z t')

    f = 3*x + t
    df = Expression(f, degree=1)
    df.t = 2.

    mesh = UnitIntervalMesh(1000)
    V = FunctionSpace(mesh, 'CG', 1)
    v = interpolate(df, V)

    DEG = 10  # Degree for the final expression; high to get accuracy

    e = conditional(ge(v + 3*v, v), v**2, sin(v))
    e_ = Expression(e, subs={v: f}, degree=DEG)
    e_.t = 2.
    assert check(e, e_)

    e = conditional(ufl.operators.And(gt(v + 2, v), lt(v**2, 3)), v**2, v)
    e_ = Expression(e, subs={v: f}, degree=DEG)
    e_.t = 2.
    assert check(e, e_)


def test_subs():
    '''Sanity for substitutions'''
    from ufl_mms.sympy_expr import check_substitutions
    assert check_substitutions({Constant((2, 2)): sp.Symbol('x')}) == False
    assert check_substitutions({Constant(1): sp.Symbol('x')}) == True

test_subs()
