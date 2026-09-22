# Phase 2 Progress Update


This is our update for this week’s class discussion. We have planned the comparison and started researching costs. We still need evidence before making final choices or claiming savings. Final submission is next week; we need to confirm the exact day.


## What we have done so far


- Reviewed the project requirements and the doctor’s feedback about specific, supported numbers.

- Divided the Phase 2 work between Sultan, Zayed and Ghith.

- Drafted a KU reuse scenario and a fair way to compare the current and proposed processes.

- Checked two hosting options and calculated an example monthly cost from published prices.

## The scenario we propose


We are three KU students proposing a tool for university staff to find and request suitable surplus items. Our first example is moving monitors between two university units. The service owner and participating users still need confirmation.


Example only: a staff member needs two working monitors with the right connections. A custodian lists suitable spare monitors. The requester chooses them, the relevant staff approve the transfer, and the custodian records the handover. Required approvals stay in place.


## What we will compare


| Version | What it means |
| --- | --- |
| Current KU process | The actual system and steps used today. We must confirm these. |
| Our core tool | Listings, ordinary search, requests, approvals and records. |
| Our tool with AI | The same process, with AI suggestions that staff check. |


We have not yet interviewed staff, timed requests, built or deployed the system, or proved a saving. The product name and logo remain open decisions.



# How we will check the numbers


We will compare the same type of request in each version. We will count every person’s working time, including mistakes, checking and extra entry into KU’s existing system. Waiting for approval is different from time spent working.


## The change must explain the benefit


| Possible change | What we need to measure |
| --- | --- |
| Search one shared list | Does it replace enquiries staff make today? |
| Reuse selected item details | How many repeated fields and corrections does it avoid? |
| Add AI suggestions | Does matching improve after counting checking time? |


Record case counts, working minutes, completed requests and errors. Keep failed cases. A small classroom test shows prototype behaviour, not results for all KU users.


## Our first hosting cost estimate


Hosting keeps the website online. Render plus Neon may fit a small free prototype within their limits. Render’s free app sleeps after 15 idle minutes and loses local files on restart. We still need to test the setup and choose lasting storage for uploads. [1, 2]


Railway is a paid option. This example assumes the following average use across the application and database for one month. These are planning inputs, not measured use. [3]


| Assumed resource use | Published rate | Monthly cost |
| --- | --- | --- |
| 0.5 GB memory | USD 10 per GB-month | USD 5.00 |
| 0.05 CPU cores | USD 20 per core-month | USD 1.00 |
| 1 GB stored data | USD 0.15 per GB-month | USD 0.15 |
| 1 GB outbound data | USD 0.05 per GB | USD 0.05 |
| Example subtotal |  | USD 6.20 |


Railway’s USD 5 minimum includes usage, so the example totals USD 6.20. AI, uploaded-file storage, support, tax and other costs still need assessment.


## What counts as money saved


Count only extra purchases avoided compared with the current process. Subtract inspection, repair, transfer and added operating costs. Time released gives staff more capacity; it does not automatically reduce spending. We cannot give a savings percentage yet.



# What we will finish before submission


Next, we will replace open questions with evidence and agree the feasibility report. Feasibility means checking whether the project is practical with our time, people, data and budget.


| Owner | Next work |
| --- | --- |
| Sultan | Finish hosting and cost comparisons. Check workload and team availability. |
| Zayed | Confirm the KU process and scenario. Check staff needs, rules and evidence access. Lead the brand discussion. |
| Ghith | Compare technology and AI choices. Check data needs and run a small trial if access allows. |


## The final report needs six checks


| Area | Simple question |
| --- | --- |
| Technical | Can we build it with suitable tools and our skills? |
| Financial | What will it cost, and which benefits can we support? |
| Operational | Can staff use it in their real work? |
| Schedule | Do we have enough time and people? |
| Data and AI | Do we have suitable data, and does AI help? |
| Legal and ethical | Do we follow rules and handle data fairly and safely? |


## What we need to confirm with the doctor


- Which current KU system and module should we compare with?

- Which KU unit would own the service, and is our monitor example suitable?

- Can we see a demonstration or speak to someone who uses the current process?

- What is the exact submission day next week?

Deployment remains in scope. This example helps us investigate the wider system; it does not remove maintenance, end-of-life actions or sustainability reporting.


## Sources checked


[[1] Render free service limits](https://render.com/docs/free)

[[2] Neon free database limits](https://github.com/neondatabase/website/blob/main/content/faqs/free-plan-limits-and-quotas.md)

[[3] Railway pricing](https://docs.railway.com/pricing)
