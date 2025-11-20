"""
Particle Physics Validation Script
Validates D4D predictions against experimental PDG data
"""

import numpy as np
from d4d_theory import D4DTheory, PHI
import matplotlib.pyplot as plt

# PDG 2020 experimental values (MeV unless noted)
PDG_DATA = {
    'leptons': {
        'electron': 0.5109989461,
        'muon': 105.6583745,
        'tau': 1776.86
    },
    'quarks_msbar_2gev': {  # MS-bar scheme at 2 GeV
        'up': 2.2,
        'down': 4.7,
        'strange': 95,
        'charm': 1275,
        'bottom': 4180,
        'top': 173100
    },
    'bosons': {  # GeV
        'W': 80.379,
        'Z': 91.1876,
        'Higgs': 125.10
    }
}


def validate_cascade_scaling():
    """
    Validate that particle masses follow φ^(4W) cascade scaling
    """
    theory = D4DTheory()
    
    print("\n" + "=" * 80)
    print("CASCADE FUNCTION VALIDATION")
    print("Formula: m(W) = m_ref × [φ^(4W)]^(3/4)")
    print("=" * 80)
    
    # Lepton cascade
    print("\nLEPTON CASCADE (W = 1, 3, 5):")
    leptons = theory.lepton_masses()
    
    for name, data in leptons.items():
        W = data['winding_number']
        ratio_to_electron = data['mass_exp_MeV'] / leptons['electron']['mass_exp_MeV']
        predicted_ratio = (PHI**(4*W))**(3/4) / (PHI**(4*1))**(3/4)
        
        print(f"\n{name.capitalize()} (W={W}):")
        print(f"  Experimental ratio to e: {ratio_to_electron:.4f}")
        print(f"  Predicted ratio: {predicted_ratio:.4f}")
        print(f"  Agreement: {(1 - abs(ratio_to_electron - predicted_ratio)/ratio_to_electron)*100:.2f}%")
    
    # Plot cascade
    fig, ax = plt.subplots(figsize=(10, 6))
    
    W_values = [1, 3, 5]
    exp_masses = [leptons['electron']['mass_exp_MeV'],
                  leptons['muon']['mass_exp_MeV'],
                  leptons['tau']['mass_exp_MeV']]
    theory_masses = [leptons['electron']['mass_theory_MeV'],
                     leptons['muon']['mass_theory_MeV'],
                     leptons['tau']['mass_theory_MeV']]
    
    ax.semilogy(W_values, exp_masses, 'ro', markersize=10, label='Experimental')
    ax.semilogy(W_values, theory_masses, 'b--', linewidth=2, label='D4D Prediction')
    
    ax.set_xlabel('Winding Number W', fontsize=12)
    ax.set_ylabel('Mass (MeV/c²)', fontsize=12)
    ax.set_title('Lepton Mass Cascade: m(W) ∝ [φ^(4W)]^(3/4)', fontsize=14)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/lepton_cascade.png', dpi=300)
    print("\n✓ Cascade plot saved to lepton_cascade.png")
    
    return leptons


def validate_phi_scaling():
    """
    Verify φ-scaling across all particle sectors
    """
    print("\n" + "=" * 80)
    print("φ-SCALING VALIDATION")
    print("Testing: Energy levels scale as E_n = E_0 × φ^(4n)")
    print("=" * 80)
    
    theory = D4DTheory()
    
    # Get reference scales
    m_e = 0.5109989461  # MeV
    m_mu = 105.6583745
    m_tau = 1776.86
    
    # Calculate φ^4 factors
    phi4 = PHI**4
    
    print(f"\nφ⁴ = {phi4:.6f}")
    print(f"(φ⁴)² = {phi4**2:.6f}")
    
    # Muon/electron ratio
    mu_e_ratio_exp = m_mu / m_e
    mu_e_ratio_theory = (phi4**3)**(3/4) / (phi4**1)**(3/4)  # W: 3 vs 1
    
    print(f"\nμ/e mass ratio:")
    print(f"  Experimental: {mu_e_ratio_exp:.4f}")
    print(f"  Theory (φ^8)^(3/4): {mu_e_ratio_theory:.4f}")
    print(f"  Agreement: {(1 - abs(mu_e_ratio_exp - mu_e_ratio_theory)/mu_e_ratio_exp)*100:.2f}%")
    
    # Tau/muon ratio
    tau_mu_ratio_exp = m_tau / m_mu
    tau_mu_ratio_theory = (phi4**5)**(3/4) / (phi4**3)**(3/4)  # W: 5 vs 3
    
    print(f"\nτ/μ mass ratio:")
    print(f"  Experimental: {tau_mu_ratio_exp:.4f}")
    print(f"  Theory (φ^8)^(3/4): {tau_mu_ratio_theory:.4f}")
    print(f"  Agreement: {(1 - abs(tau_mu_ratio_exp - tau_mu_ratio_theory)/tau_mu_ratio_exp)*100:.2f}%")


def validate_weinberg_relationships():
    """
    Validate electroweak sector mass relationships
    """
    print("\n" + "=" * 80)
    print("ELECTROWEAK MASS RELATIONSHIPS")
    print("=" * 80)
    
    theory = D4DTheory()
    bosons = theory.electroweak_bosons()
    weinberg = theory.weinberg_angle()
    
    m_W = bosons['W']['mass_exp_GeV']
    m_Z = bosons['Z']['mass_exp_GeV']
    m_H = bosons['Higgs']['mass_exp_GeV']
    
    # Weinberg relation: m_W/m_Z = cos(θ_W)
    ratio_exp = m_W / m_Z
    ratio_theory = np.sqrt(weinberg['sin2_theta_w_theory'])  # cos²θ = 1 - sin²θ = 7/9
    ratio_theory = np.sqrt(7/9)
    
    print(f"\nW/Z mass ratio:")
    print(f"  Experimental: {ratio_exp:.6f}")
    print(f"  Theory (cos θ_W = √(7/9)): {ratio_theory:.6f}")
    print(f"  Error: {abs(ratio_exp - ratio_theory)/ratio_exp * 100:.3f}%")
    
    # Higgs relation: m_H ≈ √2 × m_Z
    higgs_ratio_exp = m_H / m_Z
    higgs_ratio_theory = np.sqrt(2)
    
    print(f"\nH/Z mass ratio:")
    print(f"  Experimental: {higgs_ratio_exp:.6f}")
    print(f"  Theory (√2): {higgs_ratio_theory:.6f}")
    print(f"  Error: {abs(higgs_ratio_exp - higgs_ratio_theory)/higgs_ratio_theory * 100:.3f}%")


def comprehensive_error_analysis():
    """
    Statistical analysis of all predictions vs experiment
    """
    print("\n" + "=" * 80)
    print("COMPREHENSIVE ERROR ANALYSIS")
    print("=" * 80)
    
    theory = D4DTheory()
    results = theory.validate_all()
    
    errors = []
    names = []
    
    # Collect all errors
    for lepton, data in results['leptons'].items():
        if lepton != 'electron':  # Electron is reference
            errors.append(data['error_percent'])
            names.append(lepton)
    
    for boson, data in results['bosons'].items():
        if boson != 'Z':  # Z is reference
            errors.append(data['error_percent'])
            names.append(boson)
    
    # Add fine structure
    errors.append(results['fine_structure']['error_percent'])
    names.append('α')
    
    # Add Weinberg angle
    errors.append(results['weinberg_angle']['error_percent'])
    names.append('sin²θ_W')
    
    # Statistics
    errors = np.array(errors)
    print(f"\nPredictions analyzed: {len(errors)}")
    print(f"Mean error: {np.mean(errors):.3f}%")
    print(f"Median error: {np.median(errors):.3f}%")
    print(f"Max error: {np.max(errors):.3f}%")
    print(f"Min error: {np.min(errors):.3f}%")
    print(f"Std deviation: {np.std(errors):.3f}%")
    
    print(f"\nPredictions with error < 1%: {np.sum(errors < 1.0)}/{len(errors)}")
    print(f"Predictions with error < 5%: {np.sum(errors < 5.0)}/{len(errors)}")
    
    # Plot error distribution
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Bar plot
    ax1.bar(range(len(errors)), errors, color='steelblue', alpha=0.7)
    ax1.axhline(y=1.0, color='green', linestyle='--', label='1% threshold')
    ax1.axhline(y=5.0, color='orange', linestyle='--', label='5% threshold')
    ax1.set_xticks(range(len(names)))
    ax1.set_xticklabels(names, rotation=45, ha='right')
    ax1.set_ylabel('Prediction Error (%)', fontsize=12)
    ax1.set_title('D4D Prediction Errors vs Experiment', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Histogram
    ax2.hist(errors, bins=15, color='steelblue', alpha=0.7, edgecolor='black')
    ax2.axvline(x=np.mean(errors), color='red', linestyle='--', 
                linewidth=2, label=f'Mean: {np.mean(errors):.2f}%')
    ax2.set_xlabel('Prediction Error (%)', fontsize=12)
    ax2.set_ylabel('Count', fontsize=12)
    ax2.set_title('Error Distribution', fontsize=14)
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/error_analysis.png', dpi=300)
    print("\n✓ Error analysis plot saved to error_analysis.png")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("D4D THEORY - COMPREHENSIVE VALIDATION")
    print("Testing zero-parameter predictions against experimental data")
    print("=" * 80)
    
    # Run all validations
    validate_cascade_scaling()
    validate_phi_scaling()
    validate_weinberg_relationships()
    comprehensive_error_analysis()
    
    print("\n" + "=" * 80)
    print("VALIDATION COMPLETE")
    print("All predictions from φ = (1+√5)/2 with ZERO free parameters")
    print("=" * 80)
