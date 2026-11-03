"""Build only Zayed's two section files from his screen and diagram source data."""
from pathlib import Path
from copy import deepcopy
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
DATA=json.loads((HERE/'design-data.json').read_text(encoding='utf-8'))
SCREENS={s['id']:s for s in DATA['screens']}

def table(headers,rows,widths):
 return '<!-- widths: '+','.join(map(str,widths))+' -->\n| '+' | '.join(headers)+' |\n|'+ '|'.join('---' for _ in headers)+'|\n'+''.join('| '+' | '.join(str(c) for c in row)+' |\n' for row in rows)+'\n'

intro='''<!-- pagebreak -->
# 7. Mockups

These mockups cover the eight screen areas in the project brief. Transfer approval includes the approval view (UI-08) and the handover and receipt view (UI-09). Sustainability Dashboard and Reports are two views of UI-13. Their Phase 3 IDs stay the same.

We use the supplied Dawra Campus logo, navy for main actions and teal for AI advice. We compared one shared layout for all roles with a separate layout for each role. We chose one shared layout because the same record passes between roles and each person should find it in the same place. We give up screens tuned to each role. Labelled forms keep entered details separate from AI suggestions. Each screen shows the active role, department, record state and the person's next decision. A state is the current step, such as Draft or Open. A version identifies the saved revision being reviewed.

Compatibility scores how well an item meets a request, from 0 to 100. Confidence is the AI's reported certainty; it does not prove that an answer is correct. Matching confidence of at least 0.75 is shown normally. From 0.50 to below 0.75, it is marked Check carefully. Below 0.50, the AI recommendation is withheld and ordinary keyword search and filters remain available. Classification confidence of at least 0.60 can fill suggestions for review; below 0.60, the suggestion is an option only. Missing confidence or model information is labelled unavailable (SRS Table 4.2; AI-01, AI-04, AI-05).

Fallback means using normal forms, search or review when AI cannot help. Input is kept and the alternative appears within 15 seconds of the original AI request, including repeated attempts (AI-13.2, NFR-07). People still decide every approval. Access, independent approval and the latest saved version are checked by the application (FR-02.2, FR-10.4, FR-10.7, BR-02, BR-20).

All shown records, scores and outputs are made-up examples, called synthetic data. Money uses AED and action times use Gulf Standard Time (GST, UTC+4). The design targets keyboard use, visible focus, labelled fields and readable phone and laptop layouts. Checks against the Web Content Accessibility Guidelines (WCAG) remain part of implementation (DR-02, NFR-01, NFR-04, SRS section 3.1.1).

'''

def screen(section,title,s,figure,notes=None,field_rows=None,fields_title=None):
 name,caption=figure
 level='###' if section.count('.')>1 else '##'
 text='<!-- pagebreak -->\n'+level+' '+section+' '+title+'\n\n'
 text+=f"**Screen:** {s['id']}. **Role:** {s['role']} in {s['dept']}. **Example state:** {s['state']}.\n\n"
 figure_id,figure_title=caption.split(' ',2)[1:]
 text+=f'![Figure {figure_id}a {figure_title} top half](images/{name}-top.png)\n\n<!-- pagebreak -->\n\n![Figure {figure_id}b {figure_title} bottom half](images/{name}-bottom.png)\n\n'
 text+='<!-- pagebreak -->\n'+level+'# '+(fields_title or s['id']+' Fields and decisions')+'\n\n'
 text+=(notes or DATA['screen_notes'][s['id']])+'\n\n'
 text+='**Table 7.'+str(int(name.split('-')[2]))+' '+s['id']+' '+('report fields' if fields_title else 'fields')+'**\n\n'
 text+=table(['Field','Synthetic example'],field_rows or s['fields'],[2600,6760])
 confidence=s['confidence']+'.' if s['confidence'] else 'Unavailable - check carefully.'
 text+=f"**AI result:** {s['ai']}\n\n**Confidence:** {confidence} Model: {("text-embedding-3-small, saved with the match and its time." if s["id"] in ("UI-07","UI-08","UI-09") else "gpt-4.1-mini-2025-04-14, saved with the suggestion and its time.")}\n\n**Reason:** {s['reason']}\n\n**Human decision:** {s['decision']}\n\n**Low or unavailable confidence:** {s['low']}\n\n**AI unavailable:** {s['down']}\n\n"
 detail=s['detail']
 text+=detail+'\n\n**Phase 3 references:** '+s['refs']+'.\n\n'
 return text

md=intro
md+=screen('7.1','Asset Registration',SCREENS['UI-03'],('figure-7-1-ui-03','Figure 7.1 Asset registration UI-03'))
md+=screen('7.2','Request Submission',SCREENS['UI-06'],('figure-7-2-ui-06','Figure 7.2 Request submission UI-06'))
md+=screen('7.3','Recommendation Review',SCREENS['UI-07'],('figure-7-3-ui-07','Figure 7.3 Recommendation review UI-07'))
md+=screen('7.4','Transfer Approval',SCREENS['UI-08'],('figure-7-4-ui-08','Figure 7.4 Assigned transfer approval UI-08'))
md+=screen('7.4.1','Handover and receipt',SCREENS['UI-09'],('figure-7-5-ui-09','Figure 7.5 Handover and receipt UI-09'))
md+=screen('7.5','Maintenance Tracking',SCREENS['UI-10'],('figure-7-6-ui-10','Figure 7.6 Maintenance tracking UI-10'))
dashboard=deepcopy(SCREENS['UI-13']);dashboard['title']='Sustainability dashboard'
md+=screen('7.6','Sustainability Dashboard',dashboard,('figure-7-7-ui-13-dashboard','Figure 7.7 Sustainability dashboard UI-13'))
report=deepcopy(SCREENS['UI-13'])
report['title']='Review report draft'
report['decision']='Compare each written claim with snapshot S06 and its source records. Sustainability reviews environmental figures, Finance reviews money and Business administration reviews operations. Return unsupported claims with comments. The mixed report stays Draft until all owners review it.'
report['down']='AI narrative unavailable. No new AI draft is generated. Conventional totals and linked records remain available for the same owner review.'
report['detail']='The report uses the same S06 monitor records, prices and carbon assumptions as the dashboard. AI-written text stays Draft until its owners review it. Carbon is an estimated range after fan-part emissions. Asset-life extension remains N/A because retirement dates are missing. The Sustainability officer can approve only the sustainability figures.'
md+=screen('7.7','Reports',report,('figure-7-8-ui-13-reports','Figure 7.8 Report draft and source review UI-13'),notes='The report view uses the same filters and snapshot as the dashboard in 7.6.',field_rows=[report['fields'][i] for i in [0,1,2,4,5,8,9,10,11]],fields_title='UI-13 Report fields and decisions')
md+=screen('7.8','Campus Assistant',SCREENS['UI-12'],('figure-7-9-ui-12','Figure 7.9 Campus assistant UI-12'))
md+='<!-- pagebreak -->\n'
(ROOT/'sections/07-zayed-mockups.md').write_text(md,encoding='utf-8')

md='''<!-- pagebreak -->
# 9. Use-Case, Sequence and Activity Diagrams

The diagrams keep the Phase 3 roles, use-case IDs, state codes and approval rules. The use-case diagram shows tasks and their participants. Sequence diagrams show messages in time order. Activity diagrams show process steps and choices. The names Asset, ResourceRequest, MatchRecommendation, Reservation, Approval, Transfer and AuditLog follow the data model in section 8.

## 9.1 Use-Case Diagram

A use case is a task the system helps someone complete. An actor is a staff role or outside service involved in a task. Figure 9.1 is the original Phase 3 diagram, with its nine staff roles and fourteen use-case IDs. Its actor links and include and extend links are preserved.

![Figure 9.1 Dawra Campus use-case diagram from Phase 3, turned sideways to fit the page](images/figure-9-1-use-case-diagram.png)

An include link identifies a step used as part of another task. Check eligibility is included in UC-06 and UC-07. Send notification is included in UC-08. An extend link identifies additional behaviour under a condition. The existing extend link from UC-06 to UC-04 is retained.

Every staff role may also search (UC-05) and use the assistant (UC-12) within its access rights. Phase 3 draws these shared tasks for the Requester to keep the figure readable. Other permitted participants and approval stages stay in the Phase 3 use-case descriptions. AI supplies advice and drafts; it cannot approve a task.

**Phase 3 references:** SRS sections 2.3 and 7; UC-01 to UC-14; BR-01, BR-02, BR-15.

<!-- pagebreak -->
### 9.1.1 Use cases and responsible roles

'''
coverage=[
('UC-01','Manage accounts and roles','Business administrator authorises; System administrator applies'),
('UC-02','Register asset','Asset custodian or Department representative; AI supports'),
('UC-03','Publish asset listing','Custodian prepares; Department representative releases'),
('UC-04','Submit resource request','Requester submits; department decides independently'),
('UC-05','Search and filter assets','All nine staff roles within permitted listings'),
('UC-06','Review ranked matches','Requester; AI ranks eligible results only'),
('UC-07','Reserve asset','Requester; independent releasing custodian or representative confirms'),
('UC-08','Approve workflow step','Assigned approver for the current stage; Business administration for authorised role tasks'),
('UC-09','Confirm handover and receipt','Releasing and receiving custodians'),
('UC-10','Manage maintenance work','Custodian, Maintenance staff and spending approvers'),
('UC-11','Decide end-of-life action','Department/custodian; Sustainability and Finance; optional AI advice'),
('UC-12','Ask the campus assistant','All nine staff roles within their permissions'),
('UC-13','Generate and review report','Business, Finance and Sustainability owners; Procurement view'),
('UC-14','View asset history and audit log','Custodian history; Business administrator audit access'),
]
md+='**Table 9.1 Use cases and responsible roles**\n\n'
md+=table(['ID','Existing use case','Who may act'],coverage,[900,2700,5760])
md+='''<!-- pagebreak -->
## 9.2 Sequence Diagrams

We use four sequences: registering an asset, approving a request, matching and reserving, and transferring an asset. Their participants are people and parts of one Django application, not new separately deployed services. Django is the framework used to build the web application. PostgreSQL is the database that stores its records. The server runs the application and contacts the outside AI service. Section 11 gives the detailed architecture, meaning how the software parts fit together.

Solid arrows show requests, decisions or notifications. Dashed open arrows show replies. An arrow that loops back to the same lifeline is a step the participant performs itself. A lifeline is the dashed vertical line under a participant. Narrow boxes show when a participant is handling a call, from the incoming message until its reply or last related message. An alt frame separates alternative paths. An opt frame contains steps used only when its condition applies. Each sequence is enlarged in two consecutive printed parts so its labels remain readable.

A transaction saves related changes together. An atomic transaction saves all of them or none. State, quantity and AuditLog evidence must save successfully together. Otherwise, rollback undoes the attempted changes. Repeating a confirmation returns the saved result without creating a second receipt or hold. The application also checks access, approval independence and the latest record version before changes.

The normal form, search or review becomes available within 15 seconds of the original user request, including retries (AI-13.2, NFR-07). NFR-16 separately targets matching results within 5 seconds for 95 of 100 measured requests. Matching confidence follows SRS Table 4.2. Compatibility measures fit to the request; confidence reports the AI's certainty.

Reservation expiry is the deadline for a temporary hold. It still applies after a pending transfer is created (BR-12). If approval misses the deadline, release the units once, cancel the transfer with a reason, withdraw pending tasks and return the request to Open. Approval and expiry use a lock to check and update the same reservation one at a time, preventing conflicting quantity changes (FR-09.4, FR-09.5, FR-11.6, BR-11, BR-12, BR-20).

'''
titles=['Register with AI classification','Request and department approval','Review matches and reserve with fallback','Transfer approvals, handover and receipt']
for i,(seq,title) in enumerate(zip(DATA['sequences'],titles),1):
 number=i+1;name=seq['name']
 md+='<!-- pagebreak -->\n### 9.2.'+str(i)+' '+title+'\n\n'
 for part in (1,2):
  if part==2:md+='<!-- pagebreak -->\n'
  md+=f'![Figure 9.{number}{"a" if part==1 else "b"} {title} part {part} of 2](images/{name}-part-{part}.png)\n\n'
  notes_part=1 if number in (3,5) else 2
  if part==notes_part:
   md+=DATA['diagram_notes'][name]+'\n\n**Phase 3 references:** '+seq['refs']+'.\n\n'

md+='''<!-- pagebreak -->
## 9.3 Activity Diagrams

An activity diagram shows the steps in a process and the choices between them. Actions name the responsible role where a person acts. Actions without a role are updates the system records. Filled circles start the process. A circle with a filled centre ends it. Rounded boxes are actions. Large diamonds are decisions. Small diamonds are merge nodes, where alternative paths join before the next action. A guard is a written condition, such as [approve], that selects the next path. Connector A joins the two printed parts of each activity.

'''
activities=[(6,'figure-9-6-request-activity','Request to transfer','UC-04 to UC-09; FR-07 to FR-11; BR-02, BR-05, BR-11 to BR-16'),(7,'figure-9-7-maintenance-activity','Maintenance to end of life','UC-10, UC-11; FR-12 to FR-14; AI-06; BR-07 to BR-09')]
for i,(number,name,title,refs) in enumerate(activities,1):
 md+=f'### 9.3.{i} {title}\n\n'+DATA['diagram_notes'][name]+'\n\n**Phase 3 references:** '+refs+'.\n\n'
for number,name,title,refs in activities:
 for part in (1,2):
  md+='<!-- pagebreak -->\n'
  md+=f'![Figure 9.{number}{"a" if part==1 else "b"} {title} part {part} of 2](images/{name}-part-{part}.png)\n\n'

(ROOT/'sections/09-zayed-use-case-sequence-activity.md').write_text(md.rstrip()+'\n',encoding='utf-8')
print('Updated only the two Zayed section files.')
