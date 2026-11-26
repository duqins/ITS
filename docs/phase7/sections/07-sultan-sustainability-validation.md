# 7. Sustainability-Calculation Validation

The dashboard numbers are only useful if they are right. Our Phase 1 success criteria set the target before any code existed: all 10 hand-calculated cases agree at the documented rounding, no benefit is counted twice, and a missing input gives N/A or a labelled estimate instead of a made-up number. The cases had to include repeated events, zero denominators, missing factors, transfer costs and a negative result.

## 7.1 How the Cases Were Checked

Each case uses the formulas of Table 12.1 and the factors of Table 12.2 in our design document. We worked out the expected value by hand first and wrote the working next to the check as a comment. Then the test moves the items through the workflow (request, hold, transfer, both approvals, handover and receipt), by calling the same functions that the pages call, and compares the app's figures with the hand result. SV-01 and SV-02 use the transfers that are already in the demo data.

**One rule that Table 12.1 does not state.** When a category has no cited replacement cost, its avoided purchase is N/A, and the app also leaves its transfer cost out of the net savings, so that reusing it does not look like a loss. In the demo history this leaves out AED 90: three transfers of AED 30 each, for two chair transfers and one desk transfer. If Table 12.1 is applied as written, with every transfer cost, SV-02 would give 5,175 - 325 = AED 4,850 instead of AED 4,940. The expected values below follow the rule the app uses. The tests are in `src/tests/test_sustainability_validation.py`.

**Table 7.1 Factors used in the cases (design Table 12.2)**

<!-- widths: 3400,2700,3260 -->
| Factor | Value | Used for |
|---|---|---|
| F3 Monitor mass | 5.15 kg | Waste diverted |
| F7 Monitor replacement cost | AED 345 | Avoided purchase |
| F1 x F3 Monitor carbon, low | 24.86548 x 5.15 = 128.057 kg CO2e | Carbon saved, low |
| F2 Monitor carbon, high | 327 kg CO2e | Carbon saved, high |
| F4 and F5 Office chair, low and high | 27 and 104 kg CO2e | Carbon saved |
| F6 Van transport | 0.25561 kg CO2e per km | Transport carbon, taken off the carbon saved |

**Rounding.** The app rounds each stored value to 2 decimals, and the transport carbon is rounded before it is taken off. For the worked example, 1 x 10 x 0.25561 = 2.5561 is stored as 2.56, and 2 x 128.057 - 2.56 = 253.554 is stored as 253.55. Table 12.4 of the design rounds the factor to 128.06 first and gives 253.6 to one decimal. At one decimal both give 253.6, which is the precision the design states.

## 7.2 Test Oracle

**Table 7.2 Test oracle for the sustainability cases**

<!-- widths: 820,1650,2200,2350,1640,700 -->
| ID | Case (requirement) | Input | Expected result, worked by hand | Actual result | Pass/Fail |
|---|---|---|---|---|---|
| SV-01 | Worked example of Table 12.4 (SU-02, SU-04, SU-07, SU-08) | 2 monitors, 1 van trip of 10 km, transfer cost AED 40 | Waste 2 x 5.15 = 10.30 kg; avoided AED 690; net 690 - 40 = AED 650; transport 2.56 kg; carbon 253.55 to 651.44 kg (253.6 to 651.4 at one decimal); factor version kept | 10.30; 690.00; 650.00; 2.56; 253.55 and 651.44; "Section 12 v1" | Pass |
| SV-02 | Net savings of the whole demo history (SU-04) | 7 monitor transfers with 15 monitors in total; 2 chair transfers and 1 desk transfer | Avoided 15 x 345 = AED 5,175; costs 40 + 30 + 15 + 50 + 40 + 40 + 20 = AED 235; net AED 4,940; 21 items reused; waste 15 x 5.15 = 77.25 kg; 3 transfers without a price; the graph ends at 4,940 | 5,175; 235; 4,940.00; 21; 77.25; 3; 4,940.00 | Pass |
| SV-03 | Missing price and mass (SU-02, SU-07) | 2 office chairs, 1 trip of 4 km, cost AED 25 | Transport 1.02 kg; carbon 2 x 27 - 1.02 = 52.98 to 2 x 104 - 1.02 = 206.98 kg; avoided purchase and waste N/A, not 0; money total stays AED 690 | 1.02; 52.98 and 206.98; none, none; 690.00 | Pass |
| SV-04 | Category with no carbon factor (SU-07) | 1 projector, the only transfer in the period | The item counts as reused, but carbon is N/A and the dashboard says N/A | 1 reused; carbon none; card shows "N/A" | Pass |
| SV-05 | Avoided purchase counts only after it is confirmed (BR-18, SU-03) | 1 more monitor, 1 trip of 3 km, cost AED 20; then the representative confirms it | Before: 3 items reused, waste 15.45 kg, avoided still AED 690. After: avoided 690 + 345 = AED 1,035; net 1,035 - 60 = AED 975; carbon low 253.55 + (128.057 - 0.77) = 380.84 kg | Before: 3, 15.45, 690.00. After: 1,035.00; 975.00; 380.84 | Pass |
| SV-06 | The same benefit is never counted twice (SU-04, BR-18) | Confirm the avoided purchase of one transfer a second time | Refused with "already confirmed"; every total unchanged; still one impact record | Refused; totals equal; 1 record | Pass |
| SV-07 | Zero denominator in the reuse rate (SU-05) | Computing department, which listed nothing; and the year 2020 | Reuse rate N/A, not 0% and not an error | None; card shows "N/A (nothing listed in this period)" | Pass |
| SV-08 | Reuse rate by hand (SU-05) | 12 units listed in the period (4 monitors, 6 chairs, 1 projector, 1 oscilloscope); 2 received; then 1 more received | 2 / 12 x 100 = 16.7%; then 3 / 12 x 100 = 25.0% | 16.7; 25.0 | Pass |
| SV-09 | A negative result stays negative (SU-04) | 1 monitor moved at a cost of AED 500 | Net 345 - 500 = AED -155, marked as a loss (red) | -155.00; "AED -155", tone "bad" (red) | Pass |
| SV-10 | Period filter (SU-01) | A period that ends the day before the worked example was received | Nothing counted: 0 transfers, AED 0, carbon and reuse rate N/A | 0; 0; none; none | Pass |

## 7.3 Result

All 10 cases agree with the hand calculation, so the Phase 1 target is met for these cases. The cases cover a repeated event (SV-06), zero denominators (SV-07, SV-10), missing factors (SV-03, SV-04), transfer costs (SV-01, SV-05) and a negative result (SV-09).

What these cases do not show: they check that the app applies our formulas correctly. They do not check that the factors themselves are right for Khalifa University. The factors come from the published sources listed in Table 12.2, and the monitor price comes from one retail listing. The data is synthetic, so the savings and carbon figures are a demonstration of the method, not savings that really happened on campus.
