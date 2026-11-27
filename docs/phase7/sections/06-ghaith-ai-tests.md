# 6. AI Tests and AI Classification Evaluation

The AI features are tested in two ways. The automated tests in section 6.1 replace the AI service with a stand-in that gives fixed answers, so they check what our code does with an answer: the rules, the thresholds, the human decision and the fallback. They do not check whether the AI itself is right. That is what the evaluation in section 6.2 does, with the real AI service on a fixed labelled set.

## 6.1 Automated AI Tests

The stand-in is `FakeClaude` in `src/tests/helpers.py`. A second stand-in, `FailingClaude` in `src/tests/test_ai_failures.py`, fails on purpose in the way it is told to. Every automated AI test runs without an API key and without the internet.

**Table 6.1 Test oracle for the AI features**

<!-- widths: 820,1700,2300,2200,1640,700 -->
| ID | Feature (requirement) | Input | Expected result | Actual result | Pass/Fail |
|---|---|---|---|---|---|
| AT-01 | Classification, a person decides (AI-01.3, AI-01.4) | Khalid asks for a suggestion on a new monitor draft; the stand-in answers "IT equipment / Monitor" 3 times; then Khalid accepts | 3 AI calls, confidence 1.00; the asset is unchanged until Khalid accepts; then its category is Monitor | 3 calls; 1.00; category empty before, Monitor after | Pass |
| AT-02 | Low confidence (AI-05.4, NFR-07) | The 3 answers disagree: Monitor, Laptop, Projector | Confidence below 0.60; the fields are not filled in; accepting does not apply it | Below 0.60; not filled in; category still empty | Pass |
| AT-03 | Only allowed categories (AI-01.1) | Any classification request | The answer format only allows the 8 active categories; the AI is asked at low effort | The format lists exactly the 8 categories; effort "low" | Pass |
| AT-04 | Match score and explanation (AI-04.1, AI-05.1) | Matches for the projector request | At most 5 matches; the top match's score equals its 7 factor points added up; confidence saved as unavailable, not 0; a reason is given | 5 or fewer; equal; 7 factors; confidence empty; reason given | Pass |
| AT-05 | Choosing a lower match (AI-05.2, AI-12.3) | Aisha chooses the match ranked 2nd, first without a reason, then with "Nearer to our room" | Refused without a reason; with it, the request moves to Reservation requested and the match is marked overridden | Still Open; then Reservation requested, "overridden" | Pass |
| AT-06 | A rejected suggestion stays rejected (AI-12.3, BR-15) | Khalid rejects a suggestion with a reason, then tries to accept it | The asset is not changed | Category still empty | Pass |
| AT-07 | Report summary checked before publishing (AI-10.1, AI-10.2, BR-10) | The draft says "avoiding 5 purchases", which is not a report figure; the officer then publishes "2 items were reused." | The first is refused; the corrected text is published and shown on the dashboard | Still pending; then "corrected" and shown | Pass |
| AT-08 | AI search answer is checked (AI-04.1) | The stand-in returns relevance 140, an item id the app never sent, and a repeated item | 140 becomes 100; the unknown and the repeated items are dropped; the result is saved and the JSON is shown | Projector 100 then laptops; 999999 not on the page; JSON shown | Pass |
| AT-09 | Data sent to the AI (NFR-04) | An AI search by Aisha | Only published items with free units are sent; none of these 7 texts is sent: Khalid, Mariam, Fatima, Aisha, Omar, "Department:" and "Engineering Building" | Same ids as the published list; none of the 7 texts found | Pass |
| AT-10 | AI runs only on a click (AI-02.1) | Opening the AI search address with GET | Refused (405) and no AI record is made | 405; no record | Pass |
| AT-11 | Photos sent to the AI (AI-01.1, AI-01.2) | A draft with 3 photos is classified | Only the first 2 photos are sent, and the page says which photo was not checked | 2 images and the text; "first 2 of 3 photos ... p2.png" | Pass |
| AT-12 | Failure: timeout (AI-13.2, NFR-07) | The AI service times out | "The AI did not answer within 15 seconds."; the wait given to the service is 15 seconds or less | That message; wait within 15 s | Pass |
| AT-13 | Failure: rate limit (AI-13.1, NFR-07) | The AI service answers 429 Too Many Requests | "The AI service is busy. Try again in a minute." | That message | Pass |
| AT-14 | Failure: service unavailable (AI-13.4, NFR-07) | No connection to the service; and no API key at all | "The AI service could not be reached."; with no key the AI is not called | That message; AIUnavailable with no key | Pass |
| AT-15 | Failure: malformed answer (AI-13.1, NFR-07) | An answer with no readable content; an answer cut short; a refusal; an answer whose fields have the wrong type | "The AI answer was incomplete." twice; "The AI declined this request."; "The AI answer did not have the expected structure." | Those four messages | Pass |
| AT-16 | Time limit already spent (AI-13.2) | Less than 1 second of the 15 is left | The AI is not called: "The 15-second limit was reached." | That message | Pass |
| AT-17 | Classic way after a failure (AI-13.2, NFR-07) | Khalid presses Classify while the service times out | No server error; the page tells him to choose the category himself; the draft is kept and unchanged | Page 200 with that text; still Draft, category empty | Pass |
| AT-18 | No AI at all (AI-13.4, FR-08.6) | No API key; the projector request | Matches are given in the classic order without scores; a draft page says "AI unavailable" and keeps the fields | Classic order, no scores; message shown | Pass |

Requirement NFR-07 names five failure conditions. Table 6.2 shows where each one is tested.

**Table 6.2 The five AI failure conditions of NFR-07**

<!-- widths: 2300,2000,5060 -->
| Condition | Test cases | Result |
|---|---|---|
| Unavailable service | AT-14, AT-18 | Pass: a clear message, and the classic search, form and order still work |
| Timeout | AT-12, AT-16, AT-17 | Pass: a clear message, the draft is kept, and the classic form is offered |
| Rate limit | AT-13 | Pass: a clear message |
| Malformed output | AT-15 | Pass: a clear message |
| Insufficient confidence | AT-02, UT-07, UT-08 | Pass: the suggestion is shown only as an option, and nothing is filled in |

The stand-in fails at once, so these tests show that the app turns each failure into a message and keeps the classic way open. The 15-second limit itself is passed to the AI client as its time limit (AT-12). We did not measure a real slow answer on a live connection.

## 6.2 AI Classification Evaluation

**Target.** Requirement AI-01.5: in a fixed set of 20 labelled assets, the system suggests the correct category for at least 16. A missing, invalid or failed answer counts as wrong.

**The set.** `src/ai/evaluation/classification_set.json` has 20 assets, each with a name, a description, specifications and the expected category. It covers all 8 active categories: 3 monitors, 3 laptops, 2 projectors, 3 office chairs, 2 desks, 3 measurement instruments, 2 textbooks and 2 stationery items. Some items are named plainly, such as "Dell P2422H display", and some only describe the use, such as "Second screen for a desk".

**How it was run.** The command `python manage.py evaluate_classification --output classification_run.json` saves each item as a draft, asks the real AI service for a suggestion in the same way as the Classify button, and compares the answer with the label. The app asks the AI 3 times per item, so the run made 60 calls. Every change is rolled back at the end, so nothing stays in the database. The run was on the laptop copy on 24 Nov 2026 at 20:00, with the model claude-haiku-5-5 and prompt version 2. The full output is saved in `docs/phase7/results/classification_run.json`.

**Table 6.3 Result of the classification evaluation**

<!-- widths: 3800,2780,2780 -->
| Measure | Target | Result |
|---|---|---|
| Correct category | At least 16 of 20 (AI-01.5) | 20 of 20, Pass |
| Failed or missing answers | Counted as wrong | 0 |
| Confidence of 0.60 or more | No target | 20 of 20, all at 1.00 |
| Slowest item (3 calls) | No target | 2.6 seconds; fastest 1.7 seconds |

**What this result does and does not show.** The target in AI-01.5 is met on this set. The result should not be read as "the AI is 100% accurate".

- The set is small. 20 items cannot show an error rate of a few percent.
- We wrote the items and the labels ourselves, after the system was built. Every item is clearly one of 8 very different categories, so the set is easy.
- The items are text only. No photos were used, so the photo part of the classification is not evaluated.
- Only the category is scored. The condition and the tags in the same answer are not checked against a label.
- A confidence of 1.00 means that the 3 answers agreed with each other. It does not mean that the answer is certain to be right.
- The result is for one model and one prompt version on one day. A change to either needs a new run on the same set.

## 6.3 AI Features Not Evaluated with the Real AI

The match usefulness test of AI-02.2 and AI-02.3 (20 requests with known suitable assets, labelled by two members, compared with classic search) was not run, so we make no claim about how useful the matches are. The same holds for the review of 20 sampled recommendations (AI-05.3) and the five generated summaries (AI-10.3). Section 9 lists these with the other targets that were not tested.
