import React,{useMemo,useState} from 'react';
import {ArrowDownRight,ArrowUpRight,BrainCircuit,CheckCircle2,ChevronRight,Download,Info,Lightbulb,Target,TrendingUp,TriangleAlert} from 'lucide-react';
import {ResponsiveContainer,ComposedChart,Area,Line,CartesianGrid,XAxis,YAxis,Tooltip,Legend,PieChart,Pie,Cell,ScatterChart,Scatter,ZAxis} from 'recharts';

const fmt=v=>Number(v||0).toLocaleString('en-US');
const pct=v=>Number.isFinite(v)?(v*100).toFixed(2)+'%':'—';
const COLORS=['#9d7aff','#5de0d0','#ffb879','#7caeff','#f18fc6','#ffe08d'];
const tooltip={contentStyle:{background:'#161b2d',border:'1px solid #3c4560',borderRadius:12,color:'#e7edff'},labelStyle:{color:'#c9d5ed'}};
const Panel=({title,subtitle,children,extra})=><div className="panel"><div className="panelHead"><div><h3>{title}</h3><small>{subtitle}</small></div>{extra}</div>{children}</div>;
const Empty=({message})=><div className="empty"><span>{message}</span></div>;
export function Insights({daily=[],purchases=[],channels=[],funnel=[],demo=false}){
 const [sort,setSort]=useState('sessions');
 const sorted=useMemo(()=>[...channels].sort((a,b)=>Number(b[sort])-Number(a[sort])),[channels,sort]);
 const total=channels.reduce((s,x)=>s+Number(x.sessions||0),0);
 const top=sorted[0],bestRate=[...channels].filter(c=>Number(c.sessions)>0).sort((a,b)=>Number(b.session_purchase_rate)-Number(a.session_purchase_rate))[0];
 const last= daily.length?daily.slice(-7).reduce((s,x)=>s+Number(x.sessions||0),0):0;
 const previous=daily.length>=14?daily.slice(-14,-7).reduce((s,x)=>s+Number(x.sessions||0),0):0;
 const trend=previous?(last-previous)/previous:null;
 const sessionsWithPurchase=funnel.length?Number(funnel[0].sessions_purchase||0):null;
 const totalSessions=funnel.length?Number(funnel[0].sessions||0):null;
 const rate=totalSessions? sessionsWithPurchase/totalSessions:null;
 const cards=[
 {icon:TrendingUp,title:'Traffic momentum',metric:trend===null?'—':(trend>=0?'+':'')+pct(trend),desc:'Last 7 days versus previous 7 days',tone:trend===null?'neutral':trend>=0?'good':'warn'},
 {icon:Target,title:'Session purchase rate',metric:rate===null?'—':pct(rate),desc:'Sessions with purchase / total sessions',tone:'good'},
 {icon:BrainCircuit,title:'Highest-volume source',metric:top?.first_user_source||'—',desc:top?fmt(top.sessions)+' sessions':'Load channel data',tone:'neutral'},
 {icon:Lightbulb,title:'Best observed source rate',metric:bestRate?.first_user_source||'—',desc:bestRate?pct(Number(bestRate.session_purchase_rate))+' session purchase rate':'Load channel data',tone:'good'}
 ];
 return <><div className="insightGrid">{cards.map(({icon:Icon,title,metric,desc,tone})=><div className="insightCard" key={title}><div className={'insightIcon '+tone}><Icon size={19}/></div><div className="insightTitle">{title}</div><div className="insightMetric">{metric}</div><div className="insightDesc">{desc}</div></div>)}</div>
 <div className="panels"><Panel title="Channel distribution" subtitle="Share of sessions by first-user source" extra={<Info size={17} color="#a38aff"/>}>{channels.length?<><ResponsiveContainer width="100%" height={300}><PieChart><Pie data={channels.slice(0,7).map(c=>({name:c.first_user_source,value:Number(c.sessions)}))} dataKey="value" nameKey="name" innerRadius={85} outerRadius={116} paddingAngle={3}>{channels.slice(0,7).map((_,i)=><Cell key={i} fill={COLORS[i%COLORS.length]}/>)}</Pie><Tooltip {...tooltip}/><Legend iconType="circle" wrapperStyle={{fontSize:11}}/></PieChart></ResponsiveContainer><p className="note">Share uses first-user acquisition, not GA4 session attribution.</p></>:<Empty message="Upload channel data to view distribution."/>}</Panel>
 <Panel title="Marketing opportunities" subtitle="Data-dependent recommendations, not causal claims" extra={<Lightbulb size={18} color="#f2bc75"/>}><div className="recommendations">
 <div className="recommendation"><span className="recNum">01</span><div><b>Audit top acquisition sources</b><p>{top?top.first_user_source+' contributes '+pct(Number(top.sessions)/Math.max(total,1))+' of recorded sessions. Compare purchase rates and campaign costs before reallocating spend.':'Load acquisition data to identify top sources.'}</p></div></div>
 <div className="recommendation"><span className="recNum">02</span><div><b>Investigate checkout friction</b><p>Use the ordered funnel SQL to inspect drop-offs. Event-presence counts alone cannot establish the cause of abandonment.</p></div></div>
 <div className="recommendation"><span className="recNum">03</span><div><b>Strengthen measurement quality</b><p>Validate purchase IDs, currency, consent signals and duplicate-event prevention before making budget decisions.</p></div></div></div></Panel></div>
 <div className="panel sectionTable"><div className="panelHead"><div><h3>Channel performance matrix</h3><small>Click a column to change the ranking</small></div><span className="tag">{channels.length} channels</span></div>{channels.length?<div className="tableWrap"><table><thead><tr><th>Acquisition source</th><th>Medium</th><th><button className="sortButton" onClick={()=>setSort('sessions')}>Sessions ↕</button></th><th><button className="sortButton" onClick={()=>setSort('purchases')}>Purchases ↕</button></th><th><button className="sortButton" onClick={()=>setSort('session_purchase_rate')}>Purchase rate ↕</button></th><th>Share</th></tr></thead><tbody>{sorted.map((r,i)=><tr key={i}><td><span className="tag">{r.first_user_source}</span></td><td>{r.first_user_medium}</td><td>{fmt(r.sessions)}</td><td>{fmt(r.purchases)}</td><td>{pct(Number(r.session_purchase_rate))}</td><td><div className="miniTrack"><span style={{width:pct(Number(r.sessions)/Math.max(total,1))}}/></div></td></tr>)}</tbody></table></div>:<Empty message="Upload channels CSV to populate this table."/>}</div>
 <p className="note">Interpretation note: This view shows descriptive signals only. Historical obfuscated data, first-user attribution and missing ad costs limit marketing conclusions.</p></>
}
export function Journey({funnel=[],demo=false}){
 const [mode,setMode]=useState('Volume');
 const data=funnel.length?[['Product views','sessions_view_item'],['Added to cart','sessions_add_to_cart'],['Checkout','sessions_begin_checkout'],['Purchases','sessions_purchase']].map(([name,key])=>({name,count:Number(funnel[0][key]||0)})):[];
 const first=data[0]?.count||0;
 return <><div className="journeyHeader"><div><h3>Customer journey explorer</h3><p className="note">Visualize event presence across the four e-commerce stages.</p></div><div className="segmented"><button className={mode==='Volume'?'on':''} onClick={()=>setMode('Volume')}>Volume</button><button className={mode==='Share'?'on':''} onClick={()=>setMode('Share')}>Share of views</button></div></div>
 {data.length?<div className="journeyGrid">{data.map((step,i)=><div className="journeyCard" key={step.name}><div className="journeyStep">STAGE 0{i+1}</div><div className="journeyValue">{mode==='Volume'?fmt(step.count):pct(first?step.count/first:0)}</div><div className="journeyLabel">{step.name}</div><div className="journeyTrack"><span style={{width:pct(first?step.count/first:0),background:COLORS[i]}}/></div>{i>0&&<div className="journeyFoot">{step.count<=data[i-1].count?'-'+fmt(data[i-1].count-step.count)+' versus previous stage':'+'+fmt(step.count-data[i-1].count)+' versus previous stage'}</div>}</div>)}</div>:<Empty message="Upload funnel CSV to explore customer journey."/>}
 <div className="panel sectionTable"><div className="panelHead"><div><h3>Interpretation & next steps</h3><small>What this analysis can and cannot tell us</small></div><TriangleAlert size={18} color="#ffbf79"/></div><p className="note">These four stages are measured independently as event presence in a session. They are not necessarily sequential and can increase between stages. To measure an ordered journey, execute <code>sql/05_ordered_funnel.sql</code> in BigQuery. Do not treat the differences above as verified abandonment rates.</p></div></>
}
