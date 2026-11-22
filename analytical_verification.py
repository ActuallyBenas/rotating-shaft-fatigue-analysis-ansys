#!/usr/bin/env python3
"""Analytical check for a simply supported circular shaft under a central force.
Units: N, mm, MPa (N/mm^2). Uses only the standard library.
These are ideal beam-theory values, not substitutes for a 3D stress model.
"""
import math
F_N = 2_000.0
L_MM = 1_000.0
D_MM = 50.0
E_MPA = 200_000.0
BASELINE_VON_MISES_MPA = 40.304
REFINED_VON_MISES_MPA = 40.560
BASELINE_DEFLECTION_MM = 0.68346
REFINED_DEFLECTION_MM = 0.68345

I_MM4 = math.pi * D_MM**4 / 64.0
M_MAX_NMM = F_N * L_MM / 4.0
SIGMA_MAX_MPA = M_MAX_NMM * (D_MM/2.0) / I_MM4
DEFLECTION_MAX_MM = F_N * L_MM**3 / (48.0 * E_MPA * I_MM4)

def relative_difference_pct(simulated, reference):
    return 100 * (simulated - reference) / reference

if __name__ == '__main__':
    print(f'I: {I_MM4:,.5f} mm^4')
    print(f'M_max: {M_MAX_NMM:,.2f} N mm')
    print(f'Beam-theory bending stress: {SIGMA_MAX_MPA:.5f} MPa')
    print(f'Beam-theory midspan deflection: {DEFLECTION_MAX_MM:.6f} mm')
    for label,sigma,delta in [('Baseline', BASELINE_VON_MISES_MPA, BASELINE_DEFLECTION_MM),
                             ('Refined', REFINED_VON_MISES_MPA, REFINED_DEFLECTION_MM)]:
        print(f'{label} stress difference vs theory: '
              f'{relative_difference_pct(sigma,SIGMA_MAX_MPA):+.4f}%')
        print(f'{label} displacement difference vs theory: '
              f'{relative_difference_pct(delta,DEFLECTION_MAX_MM):+.4f}%')
    print('Baseline -> refined stress change: '
          f'{relative_difference_pct(REFINED_VON_MISES_MPA,BASELINE_VON_MISES_MPA):+.4f}%')
    print('Baseline -> refined displacement change: '
          f'{relative_difference_pct(REFINED_DEFLECTION_MM,BASELINE_DEFLECTION_MM):+.4f}%')
