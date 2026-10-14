# PHY709: 15 October 2026

Maxwell equations, constitutive relations and electromagnetic boundary conditions

Dr. Junaid Ali, COMSATS University Islamabad

## Field equations in matter

$$
\nabla\cdot\mathbf D=\rho_f,\qquad\nabla\cdot\mathbf B=0
$$
$$
\nabla\times\mathbf E=-\partial_t\mathbf B,\qquad
\nabla\times\mathbf H=\mathbf J_f+\partial_t\mathbf D
$$

The sources here are free charge and free current. Polarization and magnetization enter through D and H.

$$
\mathbf D=\epsilon_0\mathbf E+\mathbf P,\qquad
\mathbf B=\mu_0(\mathbf H+\mathbf M)
$$

For a linear, local, isotropic, nondispersive material:

$$
\mathbf D=\epsilon\mathbf E,\quad\mathbf B=\mu\mathbf H,\quad
\mathbf J_{\rm cond}=\sigma\mathbf E
$$

## Charge conservation

Taking divergence of Ampere-Maxwell law and substituting Gauss's law gives:

$$
\partial_t\rho_f+\nabla\cdot\mathbf J_f=0
$$

## Boundary reference

Declare n from medium 1 to medium 2. For a stationary ordinary interface with finite bulk fields:

$$
\hat{\mathbf n}\cdot(\mathbf D_2-\mathbf D_1)=\sigma_f
$$
$$
\hat{\mathbf n}\cdot(\mathbf B_2-\mathbf B_1)=0
$$
$$
\hat{\mathbf n}\times(\mathbf E_2-\mathbf E_1)=\mathbf0
$$
$$
\hat{\mathbf n}\times(\mathbf H_2-\mathbf H_1)=\mathbf K_f
$$

Normal D is continuous only when free sheet charge vanishes. Tangential H is continuous only when free sheet current vanishes. Normal E and tangential B can jump at material interfaces.

## Calculation procedure

1. Draw the interface and declare its normal.
2. Resolve each field into normal and tangential components.
3. Apply the appropriate Maxwell jump condition.
4. Insert the constitutive relation for each medium.
5. Check direction, units, source terms and a limiting case.

## Preparation for the next class

Read the worked dielectric and current-sheet examples. Reproduce one pillbox and one loop proof without using the final formula. The wave-equation preview assumes a homogeneous, source-free, lossless medium.
