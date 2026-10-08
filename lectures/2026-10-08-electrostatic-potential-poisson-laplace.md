# Lecture for 8 October 2026

## Electrostatic potential, Poisson's equation and Laplace's equation

**Course:** PHY709 Advanced Electromagnetic Fields and Waves  
**Level:** MS/PhD  
**Duration:** 90 minutes  
**Primary alignment:** Jackson, 3rd ed., §§1.7–1.10, with §1.11 as an energy extension

> The numerical problems below are instructor-authored variants aligned with Jackson's methods. They do not reproduce textbook problem statements. Each scaffold deliberately stops after approximately 30% of the solution.

## Learning outcomes

By the end of the lecture, students should be able to:

1. derive the scalar potential relation from electrostatic Maxwell equations;
2. distinguish source regions governed by Poisson's equation from source-free regions governed by Laplace's equation;
3. state suitable Dirichlet, Neumann and interface data;
4. construct a five-point finite-difference equation;
5. test a numerical solution using its residual, boundary error, units and grid dependence.

## Preparation before class

Read Jackson §§1.7–1.10. Review Gauss's law, the electrostatic scalar potential and the divergence theorem.

Use the repository's **Potential Explorer** to compare one charge-free region with one region containing charge. Record:

- the equation solved in each region;
- the boundary data;
- one physical check that distinguishes a plausible result from an invalid one.

## Baseline check

1. If \(\nabla\times\mathbf E=0\), what follows for \(\oint\mathbf E\cdot d\mathbf l\)?
2. Can \(\rho=0\) while \(\mathbf E\neq0\)?
3. What information is missing from \(\nabla^2\Phi=0\)?
4. What extra condition accompanies a pure Neumann problem?
5. Can a nonconstant harmonic potential have an isolated interior maximum?

## Core relations

\[
\mathbf E=-\nabla\Phi,
\qquad
\nabla^2\Phi=-\frac{\rho}{\varepsilon_0}.
\]

In a charge-free region,

\[
\nabla^2\Phi=0.
\]

For a surface charge density \(\sigma\),

\[
\Phi_1=\Phi_2,
\qquad
\frac{\partial\Phi_2}{\partial n}
-
\frac{\partial\Phi_1}{\partial n}
=
-\frac{\sigma}{\varepsilon_0}.
\]

For a uniform square grid with spacing \(h\), Poisson's equation gives

\[
\Phi_{i,j}
=
\frac14\left(
\Phi_{i+1,j}+\Phi_{i-1,j}
+\Phi_{i,j+1}+\Phi_{i,j-1}
+\frac{h^2\rho_{i,j}}{\varepsilon_0}
\right).
\]

## In-class sequence

| Time | Activity | Evidence of learning |
|---|---|---|
| 0–7 min | Individual baseline check and peer defence | Written prediction and revised response |
| 7–20 min | Board derivation from Maxwell equations | Students identify every assumption |
| 20–32 min | Boundary data, uniqueness and compatibility | Groups classify three boundary-value problems |
| 32–42 min | Potential Explorer investigation | PDE, boundary and physical check recorded |
| 42–68 min | Numerical workshop | One problem setup, first update and algorithm plan |
| 68–80 min | Analytic–numerical comparison | Residual and grid-error strategy |
| 80–87 min | Group defence | One-minute method defence per group |
| 87–90 min | Exit ticket | Individual response collected |

## Numerical problem 1: grounded square with a smooth charge distribution

Consider a two-dimensional cross-section

\[
0\le x,y\le a,
\qquad a=5.0\times10^{-2}\ \mathrm{m},
\]

with \(\Phi=0\) on all four boundaries and

\[
\rho(x,y)=\rho_0
\exp\left[
-\frac{(x-a/2)^2+(y-a/2)^2}{s^2}
\right],
\]

where \(\rho_0=1.0\times10^{-6}\ \mathrm{C\,m^{-3}}\) and
\(s=1.0\times10^{-2}\ \mathrm m\).

Use a \(51\times51\) grid.

### Required work

- derive the finite-difference equation;
- implement Jacobi, Gauss–Seidel or SOR iteration;
- report \(\Phi_{\max}\) and its location;
- plot or tabulate the normalized residual;
- repeat on a \(101\times101\) grid and quantify the change.

### 30% solution scaffold

The grid spacing for the \(51\times51\) grid is

\[
h=\frac{a}{50}=1.0\times10^{-3}\ \mathrm m.
\]

Starting from zero interior values, the first **Jacobi** update at the centre is

\[
\Phi_c^{(1)}
=
\frac{h^2\rho_0}{4\varepsilon_0}
\approx 2.82\times10^{-2}\ \mathrm V.
\]

Stop here. Students must select the convergence criterion, complete the iterations, and perform the grid study.

## Numerical problem 2: Laplace benchmark in a rectangle

Let

\[
0<x<a,\qquad 0<y<b,
\]

with \(a=0.10\ \mathrm m\), \(b=0.05\ \mathrm m\), and

\[
\Phi(0,y)=\Phi(a,y)=\Phi(x,0)=0,
\qquad
\Phi(x,b)=V_0\sin\left(\frac{\pi x}{a}\right),
\]

where \(V_0=100\ \mathrm V\).

Use a \(41\times21\) grid, so that \(h_x=h_y=2.5\times10^{-3}\ \mathrm m\).

### Required work

- solve the discrete Laplace equation;
- derive the analytic separated solution for comparison;
- compare the centre potential;
- calculate the maximum absolute grid error;
- verify the maximum principle.

### 30% solution scaffold

Use \(\Phi=X(x)Y(y)\). Separation gives

\[
\frac{X''}{X}=-k^2,
\qquad
\frac{Y''}{Y}=k^2.
\]

The boundary values select the first sine mode,

\[
X(x)=\sin\left(\frac{\pi x}{a}\right),
\qquad
Y(y)=A\sinh\left(\frac{\pi y}{a}\right).
\]

Stop here. Students determine \(A\), evaluate the analytic benchmark, run the grid solution and calculate its error.

## Optional extension: pure Neumann Poisson problem

On \(0<x<a\), \(0<y<b\), impose \(\partial\Phi/\partial n=0\) on the complete boundary and use

\[
\rho(x,y)=\rho_0
\cos\left(\frac{2\pi x}{a}\right)
\cos\left(\frac{\pi y}{b}\right).
\]

### 30% solution scaffold

Verify the compatibility condition

\[
\int_\Omega \rho\,dA=0
\]

and impose the gauge

\[
\frac{1}{N}\sum_{i,j}\Phi_{i,j}=0.
\]

Students complete the Neumann boundary stencil, solve the singular linear system with the gauge constraint and verify the mean potential.

## Numerical verification checklist

A submitted solution must include:

- the governing equation and domain;
- all boundary conditions;
- a dimensional check;
- the discrete residual;
- a boundary-error check;
- one grid-refinement comparison;
- a physical interpretation of the result.

A smooth-looking contour plot alone does not establish correctness.

## Discussion prompts

1. Why can a charge-free region support a nonzero field?
2. Which numerical symptom violates the maximum principle?
3. How does a pure Neumann problem differ from a Dirichlet problem?
4. Why does a smaller update norm not automatically imply a small PDE residual?
5. Which check would expose an incorrect sign in the Poisson stencil?

## Exit ticket

1. Derive Poisson's equation from \(\nabla\cdot\mathbf E=\rho/\varepsilon_0\) and \(\mathbf E=-\nabla\Phi\).
2. Explain why boundary data determine a Laplace solution.
3. State the compatibility and gauge requirements for a pure Neumann problem.

## Sources

- J. D. Jackson, *Classical Electrodynamics*, 3rd ed., Chapter 1.
- [Wiley chapter outline](https://www.wileyindia.com/classical-electrodynamics-an-indian-adaptation.html)
- [KSU Physics 831 lecture sequence and notes](https://www.phys.ksu.edu/personal/wysin/ED-I/index.html)
- [KSU Physics 831 Chapter 1: Poisson, Laplace and Green functions](https://www.phys.ksu.edu/personal/wysin/ed-i/notes/chap1c.html)
- [MIT OpenCourseWare graduate lecture on Cartesian Laplace solutions](https://ocw.mit.edu/courses/6-641-electromagnetic-fields-forces-and-motion-spring-2009/resources/mit6_641s09_lec10/)
