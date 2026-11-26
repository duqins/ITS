# Appendix A. Every Automated Test

All 191 tests passed in the final run on 26 Nov 2026 (`python manage.py test`: "Ran 191 tests", "OK"). "Page" is yes when the test opens at least one page with the test browser.

**Table A.1 test_units.py (14 tests)**

<!-- widths: 7160,1100,1100 -->
| Test | Page | Result |
|---|---|---|
| database refuses more units than exist | no | Pass |
| missing fields for confirmation | no | Pass |
| reserve quantity classes | no | Pass |
| state table classes | no | Pass |
| figures check classes | no | Pass |
| condition points classes | no | Pass |
| meaning points follow the ai number | no | Pass |
| total is the sum of the factors | no | Pass |
| role action table | no | Pass |
| sign in lockout classes | no | Pass |
| classification threshold classes | no | Pass |
| finance threshold classes | no | Pass |
| match confidence label classes | no | Pass |
| working days skip the weekend | no | Pass |

**Table A.2 test_c1_login_roles.py (7 tests)**

<!-- widths: 7160,1100,1100 -->
| Test | Page | Result |
|---|---|---|
| five wrong passwords lock the account | yes | Pass |
| menu hides sections the role cannot use | yes | Pass |
| nine roles exist | no | Pass |
| pages need sign in | yes | Pass |
| refused page offers the users other role and returns to the page | yes | Pass |
| server refuses an action the role does not allow | yes | Pass |
| switching role changes what the server allows | yes | Pass |

**Table A.3 test_c2_c3_assets.py (7 tests)**

<!-- widths: 7160,1100,1100 -->
| Test | Page | Result |
|---|---|---|
| a second user confirms | yes | Pass |
| custodian of another department cannot open the asset | yes | Pass |
| quantity must be positive | yes | Pass |
| register with category condition department and status | yes | Pass |
| listing is released by the department representative | yes | Pass |
| no results offers a request | yes | Pass |
| search by keyword category condition and department | yes | Pass |

**Table A.4 test_c4_requests.py (4 tests)**

<!-- widths: 7160,1100,1100 -->
| Test | Page | Result |
|---|---|---|
| cancel needs a reason | yes | Pass |
| requester only sees own requests | yes | Pass |
| required by date in the past is refused | yes | Pass |
| staff submit a request and see its status | yes | Pass |

**Table A.5 test_c5_transfers.py (6 tests)**

<!-- widths: 7160,1100,1100 -->
| Test | Page | Result |
|---|---|---|
| full transfer changes owner and department on receipt | yes | Pass |
| high value procurement item needs policy approval | yes | Pass |
| no self approval | yes | Pass |
| other department cannot approve and reject needs reason | yes | Pass |
| receiver must record a discrepancy when the quantity differs | yes | Pass |
| the last item cannot go to two people | yes | Pass |

**Table A.6 test_c6_history.py (5 tests)**

<!-- widths: 7160,1100,1100 -->
| Test | Page | Result |
|---|---|---|
| audit entries cannot be changed or deleted | no | Pass |
| audit log search and csv for the business administrator | yes | Pass |
| every state change is logged | no | Pass |
| history page shows who did what and when | yes | Pass |
| moves outside the cycle are refused | no | Pass |

**Table A.7 test_c7_sustainability.py (4 tests)**

<!-- widths: 7160,1100,1100 -->
| Test | Page | Result |
|---|---|---|
| dashboard shows measures with formula and source | yes | Pass |
| requester cannot open the dashboard | yes | Pass |
| reversed dates are refused | yes | Pass |
| worked example figures | no | Pass |

**Table A.8 test_c8_notifications.py (6 tests)**

<!-- widths: 7160,1100,1100 -->
| Test | Page | Result |
|---|---|---|
| a request opened again is not called approved | no | Pass |
| approved and rejected reach the requester | no | Pass |
| receipt reaches the requester | no | Pass |
| request made notifies the department representative | yes | Pass |
| unread count and mark as read | yes | Pass |
| users only open their own notifications | yes | Pass |

**Table A.9 test_c9_reports.py (5 tests)**

<!-- widths: 7160,1100,1100 -->
| Test | Page | Result |
|---|---|---|
| csv cells cannot run as formulas | yes | Pass |
| csv contains filters records and totals | yes | Pass |
| representative reports on own department only | yes | Pass |
| requester cannot open reports | yes | Pass |
| tables of requests and transfers | yes | Pass |

**Table A.10 test_ai.py (12 tests)**

<!-- widths: 7160,1100,1100 -->
| Test | Page | Result |
|---|---|---|
| below 0.60 is an option only | yes | Pass |
| claude can only pick an allowed category and answers at low effort | yes | Pass |
| suggestion with confidence and human accept | yes | Pass |
| choosing a lower ranked item needs a reason | yes | Pass |
| top matches have a score equal to the factor total | no | Pass |
| classic path without ai | yes | Pass |
| draft is edited and published by a reviewer | yes | Pass |
| numbers not in the figures are caught | no | Pass |
| a rejected suggestion cannot be applied later | yes | Pass |
| choosing one match rejects the rest and a match can be rejected | yes | Pass |
| figures check catches years words and signs | no | Pass |
| published summary only shows for its own scope | yes | Pass |

**Table A.11 test_ai_search.py (7 tests)**

<!-- widths: 7160,1100,1100 -->
| Test | Page | Result |
|---|---|---|
| a too short request is refused and results are private | yes | Pass |
| arabic users get reasons in arabic | yes | Pass |
| it runs only on a click | yes | Pass |
| only published items with units are sent and no names of people or departments | yes | Pass |
| results are ranked checked and saved and the json is shown | yes | Pass |
| the service keeps at most eight results | no | Pass |
| without the ai the normal search still works | yes | Pass |

**Table A.12 test_document_gaps.py (26 tests)**

<!-- widths: 7160,1100,1100 -->
| Test | Page | Result |
|---|---|---|
| a request approval shows its stages and the next one | yes | Pass |
| a transfer approval shows release receipt and approved | yes | Pass |
| a custodian adds photos and a document when registering | yes | Pass |
| a draft edit can remove a photo | yes | Pass |
| a partial transfer keeps the photos on the new record | no | Pass |
| a possible duplicate needs a second confirmation | yes | Pass |
| a value cannot be negative | yes | Pass |
| confirmation needs the mandatory fields | yes | Pass |
| only real jpg or png photos and pdf documents are accepted | yes | Pass |
| only two photos go to the ai and the panel says so | yes | Pass |
| panoramas are accepted but huge progressive jpegs are not | yes | Pass |
| photos of a draft stay in the department but published items show them | yes | Pass |
| the classification reads the photos | yes | Pass |
| a request can carry an optional description | yes | Pass |
| an old check shows verification needed until the custodian verifies again | yes | Pass |
| search shows restrictions and when the item was last verified | yes | Pass |
| the home page counts assets needing verification and lists them | yes | Pass |
| a business administrator requests a role from the page | yes | Pass |
| a rejection needs a reason and gives no role | yes | Pass |
| a role needs a request an independent authorisation and an application | yes | Pass |
| nobody decides their own role request and application needs authorisation | yes | Pass |
| only administrators see the menu entry | yes | Pass |
| the administration site cannot change roles or business records | yes | Pass |
| the page shows the proposed thresholds | yes | Pass |
| the requester can withdraw a role request | yes | Pass |
| the three steps are done by three different people | yes | Pass |

**Table A.13 test_edge_cases.py (11 tests)**

<!-- widths: 7160,1100,1100 -->
| Test | Page | Result |
|---|---|---|
| a decided task cannot be decided again | no | Pass |
| a listing cannot hold more than was released | no | Pass |
| a rejected transfer gives the units back to the listing | no | Pass |
| closing a listing cancels the holds still waiting | no | Pass |
| editing a draft quantity keeps every unit available | yes | Pass |
| finance and procurement decide in either order | yes | Pass |
| missing units cannot be accepted and received quantity is limited | no | Pass |
| negative costs are refused | yes | Pass |
| overdue holds expire and free the units | no | Pass |
| two partial transfers can both be received | no | Pass |
| withdrawing a listing closes its release task | no | Pass |

**Table A.14 test_demo_checks.py (12 tests)**

<!-- widths: 7160,1100,1100 -->
| Test | Page | Result |
|---|---|---|
| a department cannot transfer to itself | no | Pass |
| a not working item cannot be offered | no | Pass |
| a second start of the same hold opens the transfer | yes | Pass |
| a tampered hold request is not a server error | yes | Pass |
| an avoided purchase is confirmed once | no | Pass |
| carbon counts only confirmed avoided purchases | no | Pass |
| editing an it draft keeps the new values | yes | Pass |
| every refused page is logged | yes | Pass |
| export csv works without pressing apply | yes | Pass |
| listing stays open while another hold is running | no | Pass |
| one open listing per asset | no | Pass |
| the representative gets a link to the approval task | yes | Pass |

**Table A.15 test_walkthrough_fixes.py (21 tests)**

<!-- widths: 7160,1100,1100 -->
| Test | Page | Result |
|---|---|---|
| a hold needs the right category condition and date | yes | Pass |
| a missing building earns no location points | no | Pass |
| a refused publish keeps the edited summary | yes | Pass |
| consequential buttons ask first and history shows record codes | yes | Pass |
| editing a draft shows its own custodian | yes | Pass |
| help and error texts have the ids the inputs point to | yes | Pass |
| refused attempts stay in the audit log but not on the request | yes | Pass |
| the home page shows what ui 02 lists | yes | Pass |
| the next step and where a request stopped are shown | yes | Pass |
| a finished request and transfer show every stage as done | yes | Pass |
| a missing page keeps the app around it | yes | Pass |
| a wrong password marks the sign in card | yes | Pass |
| forms tell the browser the same limits as the server | yes | Pass |
| handover and receipt times use the same format as the history | yes | Pass |
| history lines with a code or a refused action are translated | no | Pass |
| money has thousands separators in both languages | yes | Pass |
| one ranked item is singular | no | Pass |
| report dates read like other dates and the csv keeps iso dates | yes | Pass |
| the report department filter is translated | yes | Pass |
| the required note is marked so pages without fields can hide it | yes | Pass |
| the server error page needs nothing that could fail | no | Pass |

**Table A.16 test_history_and_graph.py (8 tests)**

<!-- widths: 7160,1100,1100 -->
| Test | Page | Result |
|---|---|---|
| a loss is drawn in red below the zero line | no | Pass |
| without history the dashboard still works | yes | Pass |
| the demo path is unchanged | no | Pass |
| the graph ends at the net savings card | yes | Pass |
| the graph follows the department filter and the representative scope | yes | Pass |
| the history spans months and money only comes from priced monitors | no | Pass |
| the section 12 worked example is still there | no | Pass |
| there is more to search and some work is overdue | yes | Pass |

**Table A.17 test_home_glance.py (6 tests)**

<!-- widths: 7160,1100,1100 -->
| Test | Page | Result |
|---|---|---|
| a representative sees only their department and their own late tasks | yes | Pass |
| a requester sees no money but sees requests held up | yes | Pass |
| finance and custodians see the late items that concern them | yes | Pass |
| the sustainability officer sees campus savings in green and late work in red | yes | Pass |
| the row is in arabic for arabic users | yes | Pass |
| the worked example alone shows its savings and nothing late | yes | Pass |

**Table A.18 test_language.py (7 tests)**

<!-- widths: 7160,1100,1100 -->
| Test | Page | Result |
|---|---|---|
| an unknown language falls back to english | yes | Pass |
| each person gets notifications in their own language | yes | Pass |
| english stays left to right | yes | Pass |
| history is saved in english and shown in the readers language | yes | Pass |
| the header button switches to arabic and saves it | yes | Pass |
| the right to left and arabic files exist | no | Pass |
| the sign in page can switch before signing in | yes | Pass |

**Table A.19 test_settings.py (5 tests)**

<!-- widths: 7160,1100,1100 -->
| Test | Page | Result |
|---|---|---|
| an unknown theme is ignored | yes | Pass |
| every user can open settings and save them | yes | Pass |
| signed out pages follow the device | yes | Pass |
| the header button saves the theme | yes | Pass |
| the style and script files exist | no | Pass |

**Table A.20 test_system_workflows.py (5 tests)**

<!-- widths: 7160,1100,1100 -->
| Test | Page | Result |
|---|---|---|
| ai assisted path with a person deciding each time | yes | Pass |
| asset goes from registration to search | yes | Pass |
| every role reaches only its own pages | yes | Pass |
| everything still works without the ai | yes | Pass |
| request to completed transfer | yes | Pass |

**Table A.21 test_ai_failures.py (3 tests)**

<!-- widths: 7160,1100,1100 -->
| Test | Page | Result |
|---|---|---|
| a timeout on the page keeps the draft and offers the classic way | yes | Pass |
| every failure becomes ai unavailable | no | Pass |
| no key and spent deadline | no | Pass |

**Table A.22 test_sustainability_validation.py (10 tests)**

<!-- widths: 7160,1100,1100 -->
| Test | Page | Result |
|---|---|---|
| case 02 net savings of the whole demo history | no | Pass |
| case 01 worked example of section 12 | no | Pass |
| case 03 chairs have a carbon range but no money value | no | Pass |
| case 04 a category without a factor shows na | no | Pass |
| case 05 an avoided purchase counts only after it is confirmed | no | Pass |
| case 06 the same avoided purchase is never counted twice | no | Pass |
| case 07 a reuse rate with nothing listed is na | no | Pass |
| case 08 reuse rate by hand | no | Pass |
| case 09 a loss stays negative | no | Pass |
| case 10 a transfer outside the period is not counted | no | Pass |
