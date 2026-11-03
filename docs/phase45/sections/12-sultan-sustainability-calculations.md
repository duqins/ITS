# 12. Sustainability Calculations

This section gives the formula behind each sustainability number in SRS section 6.1 (SRS Table 6.1, SU-01 to SU-09). Only completed and approved actions count, never AI suggestions that nobody accepted (BR-18). Every result keeps its inputs, the factor source and version, and whether its values are measured, estimated or synthetic (SU-08). Our data is made up, so the results show how the method works, not real KU savings.

## 12.1 Formulas

**Table 12.1 Sustainability formulas**

<!-- widths: 1900,4560,1300,1600 -->
| Indicator | Formula for a reporting period | Unit | Source records |
|---|---|---|---|
| Waste diverted | Sum of the quantities that left service through reuse, repair back to service, donation, disassembly or recycling instead of disposal. Each item counts once per period. | Items, and kg where mass is recorded | TR-06, MW-06, EL-05 |
| Avoided purchases | Count of fulfilled requests confirmed under BR-18. Value = quantity × replacement cost. | Count, AED | TR-06 and the confirmation by the receiving Department representative |
| Net financial savings | Avoided purchase value - (transfer cost + inspection cost + repair cost + refurbishment cost) | AED | Avoided purchases, TR-06, MW-06 |
| Reuse rate | Quantity from a chosen group of listed assets that was transferred and received by the end of the period ÷ total quantity in that group × 100. N/A when the group is empty. | % | LS-03, TR-06 |
| Repair success rate | Work orders completed with the asset back in service ÷ work orders closed as Completed or Not repairable × 100. N/A when none closed. | % | MW-06, MW-07 |
| Asset-life extension | Revised retirement date - planned retirement date, for each asset reused, repaired or refurbished. Reported as a total and an average. | Months (estimated) | MW-06, TR-06 |
| Carbon saved, low | Sum of (quantity × low factor of its category) - transport - parts | kg CO2e (estimated) | Avoided purchases, Table 12.3 |
| Carbon saved, high | Sum of (quantity × high factor of its category) - transport - parts | kg CO2e (estimated) | Avoided purchases, Table 12.3 |
| Transport | Number of van trips × distance in km × 0.25561 | kg CO2e | Transfer records |
| Parts | Mass of new parts in kg × the material factor of the part, per kg | kg CO2e | MW-06 |

We always show carbon as a range, written as "low to high kg CO2e", because the published factors for the same item differ a lot. Negative results are kept, and a category without a cited factor shows N/A instead of a number (SU-07). The results are stored in SustainabilityImpact as co2eLowKg and co2eHighKg (section 8).

## 12.2 Factors and Their Sources

**Table 12.2 Factors**

<!-- widths: 500,2200,2100,4560 -->
| # | Factor | Value | Source |
|---|---|---|---|
| F1 | IT equipment, materials and production | 24,865.48 kg CO2e per tonne (24.87 per kg) | UK DESNZ, Greenhouse gas reporting: conversion factors 2024, Material use, "IT (primary material production)". The same value is in the 2021 to 2024 sets. |
| F2 | 24-inch monitor, manufacturing | 327 kg CO2e per monitor | Dell product carbon footprint for the P2422H monitor (2024), manufacturing stage only. |
| F3 | 24-inch monitor mass, with stand | 5.15 kg | Dell P2422H specifications. |
| F4 | Office chair, low | 27 kg CO2e per chair | Average for contract chairs from the Furniture Industry Research Association, cradle to gate, as given in the Casala Onyx IV EPD (issued 11 December 2025). |
| F5 | Office chair, high | 104 kg CO2e per chair | Steelcase Leap EPD (NSF EPD11372, issued 5 October 2026), materials and production (A1 to A3), not counting biogenic carbon. |
| F6 | Van transport | 0.25561 kg CO2e per km | UK DESNZ, Greenhouse gas reporting: conversion factors 2025 (published 10 June 2025), "Diesel van, average (up to 3.5 tonnes), freighting goods". |
| F7 | Replacement cost of a 24-inch monitor | AED 345 including VAT | Our Phase 2 feasibility study, retail listing [S15]. |

**Table 12.3 Factor range for each category**

<!-- widths: 2600,3380,3380 -->
| Category | Low factor | High factor |
|---|---|---|
| Monitor (24-inch) | F1 × F3 = 128 kg CO2e | F2 = 327 kg CO2e |
| Office chair | F4 = 27 kg CO2e | F5 = 104 kg CO2e |
| Any other category | N/A until a cited factor is added | N/A until a cited factor is added |

Each category keeps its low and high factor in Category.emissionFactorLow and emissionFactorHigh, with factorSource and factorVersion (section 8.3). A business administrator adds or changes a factor (FR-03.2). A change creates a new version, and older results keep the version they were calculated with. These factors answer TBD-6 for monitors and office chairs. Other categories show N/A until we add a cited factor for them.

## 12.3 Worked Example

A department receives two 24-inch monitors from another department in one van trip of 10 km. The request was approved, and the receiving department's Department representative confirmed that a new purchase would otherwise have been needed (BR-18). The move cost AED 40. All values are synthetic.

**Table 12.4 Worked example**

<!-- widths: 2400,4400,2560 -->
| Indicator | Working | Result |
|---|---|---|
| Waste diverted | 2 monitors × 5.15 kg | 2 items, 10.3 kg |
| Avoided purchases | 2 × AED 345 | 1 request, AED 690 |
| Net financial savings | AED 690 - AED 40 | AED 650 |
| Transport | 1 trip × 10 km × 0.25561 | 2.56 kg CO2e |
| Carbon saved, low | 2 × 128.06 - 2.56 | 253.6 kg CO2e |
| Carbon saved, high | 2 × 327 - 2.56 | 651.4 kg CO2e |
| Shown on the dashboard | | About 254 to 651 kg CO2e saved (estimated, synthetic data) |

The range is wide because the two factors measure different things: F1 counts only the materials by mass, while F2 is the full manufacturing footprint of one monitor model. Showing both keeps the report honest about how sure we are.
