/* Pure demonstration edit-check model; fictional study only. */
(function(global){
const rules=[{"id":"EC-01","requirement":"REQ-01","form":"IC/SV","name":"Consent before visits","condition":"Any visit date precedes consent date","action":"Query date chronology","severity":"High"},{"id":"EC-02","requirement":"REQ-02","form":"SV","name":"Visit timing window","condition":"Day 14 outside baseline+11..17 or Day 28 outside baseline+25..31","action":"Review visit window","severity":"Medium"},{"id":"EC-03","requirement":"REQ-03","form":"VS","name":"Required vital signs","condition":"SYSBP or PULSE is missing","action":"Query missing measurement","severity":"Medium"},{"id":"EC-04","requirement":"REQ-04","form":"VS","name":"Plausibility review","condition":"SYSBP < 60 or > 250 OR PULSE < 35 or > 220","action":"Review unusual value; do not alter data","severity":"Medium"},{"id":"EC-05","requirement":"REQ-05","form":"SV","name":"Duplicate visit","condition":"Same subject and visit label occurs more than once","action":"Review duplicate entry","severity":"High"},{"id":"EC-06","requirement":"REQ-06","form":"IC/SV","name":"Date validity","condition":"Missing or malformed dates, or baseline date absent","action":"Review date completeness","severity":"High"},{"id":"EC-07","requirement":"REQ-07","form":"IC","name":"Duplicate subject record","condition":"Subject ID appears more than once in the subject register","action":"Review enrollment duplication","severity":"High"},{"id":"EC-08","requirement":"REQ-08","form":"DM","name":"Illustrative eligibility age","condition":"Age missing or outside 18..75","action":"Review fictional inclusion rule","severity":"Medium"}];
const day=86400000;const severities=Object.fromEntries(rules.map(r=>[r.id,r.severity]));
function date(s){if(typeof s!=='string'||!/^\d{4}-\d{2}-\d{2}$/.test(s)||s.startsWith('0000'))return null;const n=Date.parse(s+'T00:00:00Z');return Number.isFinite(n)&&new Date(n).toISOString().slice(0,10)===s?n:null}
function validate(study){const queries=[];const push=(subject,rule,detail,visit='—')=>queries.push({subject,visit,rule,detail,severity:severities[rule]});const seen=new Set();
for(const s of study.subjects){const validConsent=date(s.consent);
if(seen.has(s.id))push(s.id,'EC-07','Repeated subject identifier');seen.add(s.id);
if(validConsent===null)push(s.id,'EC-06','Consent date is invalid');
if(!Number.isInteger(s.age)||s.age<18||s.age>75)push(s.id,'EC-08','Age outside fictional 18–75 criterion');
const seenVisits=new Set();const baseline=s.visits.find(v=>v.name==='Baseline');const base=baseline?date(baseline.date):null;
if(base===null)push(s.id,'EC-06','Baseline date missing or invalid');
for(const v of s.visits){const d=date(v.date);
if(seenVisits.has(v.name))push(s.id,'EC-05','Duplicate visit label',v.name);seenVisits.add(v.name);
if(d===null)push(s.id,'EC-06','Visit date invalid',v.name);
if(d!==null&&validConsent!==null&&d<validConsent)push(s.id,'EC-01','Visit occurred before consent',v.name);
if(d!==null&&base!==null&&(v.name==='Day 14'||v.name==='Day 28')){const delta=Math.round((d-base)/day),target=v.name==='Day 14'?14:28;if(Math.abs(delta-target)>3)push(s.id,'EC-02','Day '+delta+' is outside '+v.name+' ±3 day window',v.name)}
if(v.sbp==null||v.pulse==null)push(s.id,'EC-03','Systolic BP or pulse missing',v.name);
if((typeof v.sbp==='number'&&Number.isFinite(v.sbp)&&(v.sbp<60||v.sbp>250))||(typeof v.pulse==='number'&&Number.isFinite(v.pulse)&&(v.pulse<35||v.pulse>220)))push(s.id,'EC-04','Unusual vital sign; needs human review',v.name);
}}
return queries.sort((a,b)=>a.subject.localeCompare(b.subject)||a.rule.localeCompare(b.rule));}
const api={rules,validate};if(typeof module!=='undefined'&&module.exports)module.exports=api;global.ClinicalChecks=api;
})(typeof globalThis!=='undefined'?globalThis:this);

