# PHY709: 15 October 2026

Maxwell equations, constitutive relations and electromagnetic boundary conditions

Dr. Junaid Ali, COMSATS University Islamabad



Use macroscopic fields and free sources consistently:

$$
\nabla\cdot\mathbf D=\rho_f,\qquad \nabla\cdot\mathbf B=0,
$$
$$
\nabla\times\mathbf E=-\frac{\partial\mathbf B}{\partial t},\qquad
\nabla\times\mathbf H=\mathbf J_f+\frac{\partial\mathbf D}{\partial t}.
$$

For a fixed volume V with outward closed surface S, and a fixed open surface A bounded by an oriented contour C:

$$
\oiint_S\mathbf D\cdot d\mathbf a=\int_V\rho_f\,dV,
\quad \oiint_S\mathbf B\cdot d\mathbf a=0,
$$
$$
\oint_C\mathbf E\cdot d\boldsymbol\ell=-\frac{d}{dt}\int_A\mathbf B\cdot d\mathbf a,
$$
$$
\oint_C\mathbf H\cdot d\boldsymbol\ell=\int_A\mathbf J_f\cdot d\mathbf a+
\frac{d}{dt}\int_A\mathbf D\cdot d\mathbf a.
$$

The contour orientation follows the right-hand rule relative to the surface normal. Moving contours require the appropriate motional-emf treatment and are outside this session.

Derivation: apply the divergence theorem to each closed-surface law. Apply Stokes’s theorem to each circulation law. Because each equality holds for arbitrary small regions in a smooth bulk medium, the integrands agree. At discontinuities, use the integral laws or a distributional interpretation instead of differentiating a discontinuous field as if it were smooth.

Physical interpretation: free charge sources D flux; B has no magnetic-charge source; changing magnetic flux induces E circulation; free current and changing D flux generate H circulation.

Units: E in V/m; D in C/m²; B in T; H in A/m; J_f in A/m²; ρ_f in C/m³. Do not mix microscopic total-source equations with macroscopic free-source equations.

## displacement current and conservation

Take the divergence of Ampère–Maxwell law:

$$
0=\nabla\cdot\mathbf J_f+\frac{\partial}{\partial t}(\nabla\cdot\mathbf D)
=\nabla\cdot\mathbf J_f+\frac{\partial\rho_f}{\partial t}.
$$

Thus:

$$
\boxed{\frac{\partial\rho_f}{\partial t}+\nabla\cdot\mathbf J_f=0}.
$$

The displacement term makes the curl equation compatible with changing charge density. It is not necessarily transport of free charges through an insulator.

Charging-capacitor example: neglect fringing in a parallel-plate vacuum capacitor of area A. D_n = Q/A, so the displacement current through the gap is I_d = A∂D_n/∂t = dQ/dt = I. Different spanning surfaces for the same Ampèrian loop give consistent circulation when the displacement term is included.

Numerical illustration: A = 0.010 m², gap d = 1.0 mm, dV/dt = 1.0×10⁶ V/s. C = ε₀A/d = 8.85×10⁻¹¹ F and I_d = C dV/dt = 8.85×10⁻⁵ A = 88.5 μA. Assumptions: uniform gap field, fixed plates, negligible fringing.

## material response

Definitions:

$$
\mathbf D=\epsilon_0\mathbf E+\mathbf P,\qquad
\mathbf H=\frac{\mathbf B}{\mu_0}-\mathbf M.
$$

P describes electric dipole moment per volume; M describes magnetic dipole moment per volume. Bound volume charge is ρ_b = −∇·P. For a polarized body with outward normal n, bound surface charge is σ_b = P·n. Bound bulk current is J_b = ∂P/∂t + ∇×M, with the appropriate magnetization surface current at boundaries.

For a linear, local, isotropic, nondispersive material:

$$
\mathbf P=\epsilon_0\chi_e\mathbf E,\quad
\mathbf M=\chi_m\mathbf H,
$$
$$
\boxed{\mathbf D=\epsilon\mathbf E,\quad \mathbf B=\mu\mathbf H,\quad
\mathbf J_{\mathrm{cond}}=\sigma\mathbf E},
$$

where ε = ε₀(1+χ_e) and μ = μ₀(1+χ_m). The free current may also contain impressed or other free-current contributions; do not identify all J_f with σE without a model assumption. Use σ only for conductivity and σ_f for free surface-charge density.

These are constitutive models, not additional universal Maxwell laws. In anisotropic material D_i = Σ_j ε_ij E_j. In dispersive material the response has time memory; in a frequency-domain model ε = ε(ω). Nonlinear response depends on field strength. Scalar component formulas used later require scalar isotropic ε and μ. Maxwell interface laws themselves are more general.

Local phasor extension, using e^(−iωt): ∇×E = iωB, ∇×H = J_f − iωD. For an Ohmic conductor with scalar σ and J_f = σE only, write ∇×H = −iωε_eff E with ε_eff = ε + iσ/ω. This incorporates conductivity once; do not add σE again if it is already absorbed in ε_eff. Treat this as a short extension, not the main lecture.

## guided component calculation

At z = 0, medium 1 occupies z < 0 and medium 2 occupies z > 0. Define n = +ẑ. Let ε₁ = 2ε₀, ε₂ = 5ε₀, σ_f = 0 and E₁ = 30x̂ + 50ẑ V/m. Predict E₂ before the boundary derivations.

After identifying tangential E continuity and normal D continuity, E₂ = 30x̂ + 20ẑ V/m. D₁n = D₂n = 100ε₀ C/m². E_n changes because ε changes, despite zero free surface charge. The total sheet charge inferred from the E jump is ε₀(20−50) = −30ε₀ C/m², entirely bound in this example.

## derive the boundary conditions

Declare n from medium 1 to medium 2. Use stationary interfaces, ordinary finite bulk fields, and possible free electric surface charge σ_f and tangential free sheet current K_f. Exclude ideal dipole layers and singular magnetic-flux sheets from these standard derivations.

### Normal D: Gaussian pillbox

For face area ΔA and height h, Gauss’s law gives (D₂n−D₁n)ΔA plus side flux = enclosed free charge. Side flux vanishes as h→0 for finite fields; regular volume charge also vanishes, while σ_fΔA remains. Therefore:

$$
\boxed{\hat{\mathbf n}\cdot(\mathbf D_2-\mathbf D_1)=\sigma_f}.
$$

### Normal B: Gaussian pillbox

The same construction with ∮B·da = 0 gives:

$$
\boxed{\hat{\mathbf n}\cdot(\mathbf B_2-\mathbf B_1)=0}.
$$

### Tangential E: shrinking rectangular loop

Use long sides of length Δℓ tangent to the interface and short sides h normal to it. Faraday’s law gives the difference of tangential line integrals. The magnetic-flux time derivative is proportional to hΔℓ and vanishes as h→0 when ∂B/∂t remains finite. Therefore:

$$
\boxed{\hat{\mathbf n}\times(\mathbf E_2-\mathbf E_1)=\mathbf 0}.
$$

This condition is valid for ordinary time-dependent interfaces; it does not require electrostatics. Nonzero bulk curl E does not force a tangential interface jump.

### Tangential H: shrinking rectangular loop

Ampère–Maxwell law retains a finite sheet-current contribution. Regular bulk current and displacement flux through the shrinking loop vanish. The vector result, with the declared normal, is:

$$
\boxed{\hat{\mathbf n}\times(\mathbf H_2-\mathbf H_1)=\mathbf K_f}.
$$

Since K_f is tangential, H₂t−H₁t = K_f×n. Check the sign by taking n = ẑ and K_f = Kx̂: the H jump must be −Kŷ, because ẑ×(−Kŷ) = Kx̂.

| Component | General jump | Continuity condition |
|---|---|---|
| D normal | D₂n−D₁n = σ_f | σ_f = 0 |
| B normal | B₂n−B₁n = 0 | Ordinary interface, no magnetic charge |
| E tangential | E₂t−E₁t = 0 | Ordinary finite-field interface |
| H tangential | n×(H₂−H₁) = K_f | K_f = 0 |

For scalar media: ε₂E₂n−ε₁E₁n = σ_f and μ₂H₂n = μ₁H₁n. With K_f = 0, B_t can still jump if μ changes. With σ_f = 0, E_n can still jump if ε changes.

Graduate consistency extension: surface charge conservation at a planar stationary sheet is ∂σ_f/∂t + ∇_s·K_f + n·(J_f2−J_f1) = 0. Explain the signs: normal current leaving into medium 2 minus current entering from medium 1 contributes to charge depletion. For uniform steady conditions, J_f2n = J_f1n.

## worked problems

### Problem 1: charged dielectric interface

At z = 0 take n = ẑ, ε₁ = 2ε₀, ε₂ = 4ε₀, E₁ = 100x̂ + 200ẑ V/m, and σ_f = 3.542×10⁻⁹ C/m². Find E₂.

Tangential continuity gives E₂x = 100 V/m. Normal D gives 4ε₀E₂z − 2ε₀(200) = σ_f. Since σ_f/ε₀ ≈ 400 V/m, E₂z ≈ 200 V/m. Thus E₂ ≈ 100x̂ + 200ẑ V/m. Equal normal E here is a consequence of the selected free sheet charge, not a universal boundary condition. D₂n−D₁n ≈ 400ε₀ C/m² matches σ_f.

### Problem 2: free current sheet

At z = 0 take n = ẑ, K_f = 6x̂ A/m, H₁ = 2ŷ + 3ẑ A/m, μ₁ = μ₀, μ₂ = 2μ₀. Find H₂.

Tangential jump: H₂t−H₁t = K_f×n = −6ŷ A/m, hence H₂y = −4 A/m and H₂x = 0. Normal B continuity: 2μ₀H₂z = μ₀(3), hence H₂z = 1.5 A/m. Therefore H₂ = −4ŷ + 1.5ẑ A/m. Verify ẑ×(H₂−H₁) = 6x̂ A/m and B₂n = B₁n. These conditions determine the local interface mapping from given H₁; a global field still requires source and geometry data.

### Paired extension if pace permits

Use the uncharged example ε₁ = 2ε₀, ε₂ = 5ε₀, E₁ = 30x̂+50ẑ. Let θ be the angle E makes with the normal. Derive tanθ₂/tanθ₁ = ε₂/ε₁ from E_t continuity and ε₂E₂n = ε₁E₁n. Values: θ₁ ≈ 30.96°, θ₂ ≈ 56.31°. This is a relation for electric-field direction at the interface, not optical Snell refraction.

## perfect conductor and continuity with the previous lecture

For an ideal perfect electric conductor in the usual initially field-free model, E = 0 inside and B = 0 inside. Take medium 1 to be the conductor and n pointing outward into medium 2. Then:

$$
\mathbf E_{2t}=0,\quad D_{2n}=\sigma_f,\quad B_{2n}=0,\quad
\hat{\mathbf n}\times\mathbf H_2=\mathbf K_f.
$$

Do not claim that infinite conductivity alone expels a pre-existing static magnetic field. With E = 0, Faraday’s law fixes ∂B/∂t = 0 inside, allowing trapped static flux. The usual B_n = 0 condition assumes zero internal B. Superconducting Meissner expulsion is a distinct physical statement.

In electrostatics E = −∇Φ. In a simple dielectric, Gauss’s law becomes:

$$
\nabla\cdot(\epsilon\nabla\Phi)=-\rho_f.
$$

Only for uniform scalar ε does this reduce to ∇²Φ = −ρ_f/ε. At an ordinary interface without an ideal dipole layer, Φ₁ = Φ₂ and:

$$
\epsilon_1\frac{\partial\Phi_1}{\partial n}-
\epsilon_2\frac{\partial\Phi_2}{\partial n}=\sigma_f,
$$

using the same n direction for both derivatives. These are the potential counterparts of tangential E and normal D conditions. Tangential E continuity fixes equality of tangential derivatives; ordinary potential continuity also requires exclusion of an ideal dipole sheet.

Preview only: in a homogeneous, source-free, lossless scalar medium, curl Faraday plus Ampère–Maxwell produces ∇²E − με∂²E/∂t² = 0, using ∇·E = 0. The interface conditions will determine reflected and transmitted amplitudes. Leave the full wave and Fresnel derivations to the next session.


## Reading



- Jackson, Classical Electrodynamics, 3rd edition: Chapters 4 (dielectric response), 5 (magnetostatics and magnetic media), 6 (Maxwell equations), and 7 (plane waves and interfaces). This is a topic map, not a page or problem-number assertion.
- MIT OpenCourseWare, 6.641 Electromagnetic Fields, Forces, and Motion, Spring 2005, graduate lecture notes: L1–L3 for Maxwell equations and boundary conditions; L7–L8 for polarization, conduction and magnetization. https://ocw.mit.edu/courses/6-641-electromagnetic-fields-forces-and-motion-spring-2005/pages/lecture-notes/
- MIT OpenCourseWare, 6.013 Electromagnetics and Applications, Spring 2009, Lecture 2: Media and Boundary Conditions. https://ocw.mit.edu/courses/6-013-electromagnetics-and-applications-spring-2009/0ec2c39ffccb37e83b43f6f59868f8d7_MIT6_013S09_lec02.pdf
- Richard Fitzpatrick, University of Texas at Austin, Classical Electromagnetism: Maxwell equations, dielectric media and magnetic media. https://farside.ph.utexas.edu/teaching/jk1/Electromagnetism/index.html

The external resources support derivations; their teaching order does not replace the official course outline. Modern SI note: μ₀ is approximately 4π×10⁻⁷ H/m, rather than an exact defining constant in the post-2019 SI; older notes may state otherwise.



## Lecture resources

[Slides, handwritten derivations, handout and assignment](2026-10-15-maxwell-constitutive-boundaries/README.md)
