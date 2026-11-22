# Rotating Shaft Fatigue Analysis | ANSYS Workbench

**Finite-element verification of a simply supported steel shaft under rotating-bending fatigue.**

![Refined-mesh von Mises stress contour](figures/stress_refined_focus.png)

## Project overview

A **1,000 mm long, 50 mm diameter** solid structural-steel shaft is supported at both ends and subjected to a **2,000 N transverse load at its midpoint**. The shaft is evaluated in **ANSYS Workbench / Mechanical 2026 R1 Student** using a 3D static structural model followed by a stress-life fatigue assessment. The goal is to identify the bending-stress maximum, assess performance against a **10^6-cycle design target**, and determine which shaft region is most fatigue-critical.

This is an **academic portfolio simulation**, not a certified bearing or rotating-machinery design. Model simplifications and the limits of the supplied fatigue data are stated below.

## Results at a glance

| Quantity | Result | Basis |
| --- | ---: | --- |
| Maximum bending stress (beam theory) | **40.744 MPa** | Simple-support formula |
| Maximum von Mises stress (initial mesh) | **40.304 MPa** | ANSYS static structural |
| Maximum von Mises stress (refined mesh) | **40.560 MPa** | ANSYS static structural |
| Maximum displacement (refined mesh) | **0.68345 mm** | ANSYS static structural |
| Maximum displacement (beam theory) | **0.67906 mm** | Euler–Bernoulli beam model |
| Maximum Z-normal stress, initial mesh | **+41.104 / −41.103 MPa** | ANSYS static structural |
| Maximum equivalent alternating stress | **40.304 MPa** | ANSYS fatigue, **initial mesh** |
| Minimum fatigue safety factor at 10^6 cycles | **2.1387** | ANSYS fatigue, **initial mesh** |
| Reported fatigue life | **10^6 cycles everywhere** | **Upper reporting bound of the tabulated S–N data**, not a predicted failure cycle |
| Reported fatigue damage for 10^6 cycles | **1.0 everywhere** | Capped life gives design-life / displayed-life = 1 |

**Key finding:** The refined FEA peak von Mises stress differs by **0.45%** from the elementary bending-stress magnitude, and the refined deflection differs by **0.65%** from beam theory. Between the initial and refined meshes, the maximum stress changes by **0.64%** and displacement by about **0.0015%**. This is a useful two-mesh refinement check, not a full asymptotic convergence study.

**Fatigue interpretation:** The smallest stress amplitude on the supplied ANSYS S–N curve is **86.2 MPa at 10^6 cycles**, greater than the FEA amplitude (40.304 MPa on the initial mesh). ANSYS returns the life of the last S–N point for stresses below its final tabulated stress in this constant-amplitude calculation. Therefore, the all-red Life contour at 10^6 cycles and uniform Damage = 1 **must not** be interpreted as failure at exactly 10^6 cycles. The result supports meeting the selected 10^6-cycle stress criterion **under the adopted reference-curve assumptions**, but does not establish infinite life.

## Model inputs

| Parameter | Value |
| --- | --- |
| Shaft material | Custom copy of ANSYS Structural Steel (`Structural Steel 2`) |
| Shaft length / diameter | 1,000 mm / 50 mm |
| Elastic modulus / Poisson ratio | 200 GPa / 0.30 |
| Density | 7,850 kg/m^3 |
| Tensile yield / ultimate strength | 250 MPa / 450 MPa |
| Load | 2,000 N in global negative Y direction |
| Load application | 10 mm-long split cylindrical-face band at Z = 500 mm |
| Bearing A, Z = 1,000 mm | Remote displacement: UX = UY = UZ = 0; RX, RY free; RZ = 0 for static rigid-mode stabilization |
| Bearing B, Z = 0 mm | Remote displacement: UX = UY = 0; UZ and all rotations free |
| Fatigue approach | Stress life, fully reversed nominal rotating bending (R = −1); one-million-cycle design life |
| S–N assumption | ANSYS-supplied, zero-mean reference curve; **not a steel-grade-specific test curve** |

### Why a static analysis models rotating bending

A stationary transverse force creates approximately stationary bending stresses in the global frame. A material point rotating around the shaft axis moves between the tensile and compressive sides, producing an approximately **fully reversed (R = −1)** bending stress history. The static FEA provides the stress amplitude proxy; the subsequent ANSYS Fatigue Tool evaluates it using the specified S–N curve. Actual bearings, rotating inertia, misalignment, contact effects, and transient dynamics are excluded.

## Figures

| Refined static results | Baseline fatigue results |
| --- | --- |
| ![Refined stress](figures/stress_refined_focus.png) | ![Alternating stress](figures/alternating_stress_baseline_focus.png) |
| ![Refined displacement](figures/deformation_refined_focus.png) | ![Fatigue safety factor](figures/fatigue_safety_baseline_focus.png) |

The original ANSYS screenshots are retained in [`figures/`](figures/) alongside print-focused crops. The fatigue result screenshots show the **initial mesh**, whereas the refined static results were obtained in a later run.

### Life and damage output

| Life (initial mesh) | Damage (initial mesh) |
| --- | --- |
| ![Life capped at one million cycles](figures/fatigue_life_baseline_focus.png) | ![Damage uniform at 1](figures/fatigue_damage_baseline_focus.png) |

The maximum cyclic stress and minimum fatigue safety factor occur near **midspan**, where the bending moment peaks. The uniform capped damage map itself **cannot identify a unique highest-damage location**.

## Analytical verification

For a simply supported circular shaft under a central transverse point load:

```text
Maximum bending moment:         M_max = F L / 4
Second moment of area:          I     = pi d^4 / 64
Maximum nominal bending stress: sigma = M_max (d/2) / I
Midspan deflection:             delta = F L^3 / (48 E I)
```

Using F = 2,000 N, L = 1,000 mm, d = 50 mm, E = 200,000 N/mm^2:

- `I = 306,796.16 mm^4`
- `M_max = 500,000 N·mm`
- `sigma_max = 40.7437 MPa`
- `delta_max = 0.679061 mm`

Run [`scripts/analytical_verification.py`](scripts/analytical_verification.py) with Python 3 to reproduce the calculation and print the FEA differences.

## Mesh refinement

| Mesh | Global target | Midpoint face target | Nodes | Elements | Max. von Mises | Max. displacement |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | 10 mm | 4 mm | Not recorded | Not recorded | 40.304 MPa | 0.68346 mm |
| Refined | 8 mm | 3 mm | **40,722** | **9,045** | **40.560 MPa** | **0.68345 mm** |

A further planned mesh at 7 mm global / 2.5 mm local exceeded the ANSYS Student limit, so no third successfully solved mesh is claimed. The two available grids show good agreement but are insufficient for a formal grid-convergence-index claim. Additional refinement should also inspect stress concentrations at the applied-load and bearing constraint regions.

## How to reproduce

1. Open ANSYS Workbench and create a **Static Structural** system.
2. Model one 1,000 mm × 50 mm solid circular shaft along the global Z-axis in SpaceClaim; split the outer surface to form the 10 mm-wide midpoint loading band.
3. Define the custom material with the properties above and the S–N table in [`data/s_n_curve.csv`](data/s_n_curve.csv).
4. Scope two **deformable Remote Displacement** conditions to opposite circular end faces using the bearing conditions shown above.
5. Apply a **2,000 N total force** in the −Y direction to the midpoint band.
6. Mesh with the global and local target sizes in the mesh table, then solve.
7. Insert Total Deformation, Equivalent (von Mises) Stress and Z-Normal Stress results.
8. Insert a **Fatigue Tool** (Stress Life, Fully Reversed) with Life, Damage, Safety Factor, and Equivalent Alternating Stress. Use a 10^6-cycle design life for the damage and safety-factor results.
9. Confirm or adjust model settings as applicable to your ANSYS installation, run the analyses, and compare outputs with the report.

**Native Workbench project files are not included yet:** screenshots alone cannot reconstruct the editable project. To add it, use **Workbench → File → Archive** to export a `.wbpz` containing your geometry, Engineering Data and model. Put that archive inside `ansys/` if it is reasonably sized and your sharing permissions allow it. Do not assume a lone `.wbpj` is sufficient without its associated `_files` directory.

## Repository contents

```text
Rotating_Shaft_Fatigue_Analysis/
├── README.md
├── report/
│   └── Rotating_Shaft_Fatigue_Analysis_Report.pdf
├── figures/                    # ANSYS screenshots and cropped portfolio figures
├── data/
│   ├── mesh_results.csv
│   └── s_n_curve.csv
├── scripts/
│   └── analytical_verification.py
├── ansys/
│   └── README.md               # Native Workbench archive instructions
└── .gitignore
```

## Important limitations

- Remote displacements on the end faces approximate simply supported bearings; no explicit rolling-element bearing contacts or housings are modeled.
- The midpoint band regularizes a nominal point load and may influence local peak stress.
- The FEA is static; fully reversed rotating stress is imposed in the Fatigue Tool, not produced by a rotating transient model.
- The selected ANSYS reference S–N curve is **not experimentally matched to a specified 450 MPa-ultimate steel grade**, and some low-cycle tabulated stresses exceed the supplied ultimate strength. Use it for the assigned demonstration, not for certification or a trustworthy low-cycle failure prediction.
- An endurance limit or high-cycle extension is **not separately established**, so true infinite fatigue life cannot be concluded from these results.
- A third grid was attempted but exceeded the ANSYS Student limit; only two successful grids are documented.

## References

1. Assignment brief: *Fatigue Analysis of a Rotating Shaft Supported by Bearings at Both Ends Using ANSYS*, supplied with the project.
2. [ANSYS Mechanical Help — Fatigue Results](https://ansyshelp.ansys.com/public/Views/Secured/corp/v251/en/wb_sim/ds_Fatigue_Results.html) — describes final S–N point behavior and damage definition.
3. [ANSYS Knowledge — Fatigue Tool safety factor](https://innovationspace.ansys.com/knowledge/forums/topic/in-the-mechanical-fatigue-tool-what-is-the-calculated-safety-factor/) — stress multiplier at the specified design life.

## Future work

- Repeat stress/fatigue solutions on a third feasible mesh or with locally controlled, higher-order elements.
- Verify bearing support reactions and consider realistic bearing-contact/support geometry.
- Use validated material-specific fatigue data extending beyond 10^6 cycles and include surface finish, size, reliability, and manufacturing factors.
- Investigate a separate higher-force sensitivity case to obtain a finite-life contour; do not conflate it with the required 2,000 N case.
