(self.webpackChunkclient=self.webpackChunkclient||[]).push([[592],{2473:function(E,b){var d;void 0!==(d=function(){"use strict";function h(o,i,m){var s=new XMLHttpRequest;s.open("GET",o),s.responseType="blob",s.onload=function(){T(s.response,i,m)},s.onerror=function(){console.error("could not download file")},s.send()}function g(o){var i=new XMLHttpRequest;i.open("HEAD",o,!1);try{i.send()}catch(m){}return 200<=i.status&&299>=i.status}function C(o){try{o.dispatchEvent(new MouseEvent("click"))}catch(m){var i=document.createEvent("MouseEvents");i.initMouseEvent("click",!0,!0,window,0,0,0,80,20,!1,!1,!1,!1,0,null),o.dispatchEvent(i)}}var _="object"==typeof window&&window.window===window?window:"object"==typeof self&&self.self===self?self:"object"==typeof global&&global.global===global?global:void 0,v=_.navigator&&/Macintosh/.test(navigator.userAgent)&&/AppleWebKit/.test(navigator.userAgent)&&!/Safari/.test(navigator.userAgent),T=_.saveAs||("object"!=typeof window||window!==_?function(){}:"download"in HTMLAnchorElement.prototype&&!v?function(o,i,m){var s=_.URL||_.webkitURL,c=document.createElement("a");c.download=i=i||o.name||"download",c.rel="noopener","string"==typeof o?(c.href=o,c.origin===location.origin?C(c):g(c.href)?h(o,i,m):C(c,c.target="_blank")):(c.href=s.createObjectURL(o),setTimeout(function(){s.revokeObjectURL(c.href)},4e4),setTimeout(function(){C(c)},0))}:"msSaveOrOpenBlob"in navigator?function(o,i,m){if(i=i||o.name||"download","string"!=typeof o)navigator.msSaveOrOpenBlob(function(o,i){return void 0===i?i={autoBom:!1}:"object"!=typeof i&&(console.warn("Deprecated: Expected third argument to be a object"),i={autoBom:!i}),i.autoBom&&/^\s*(?:text\/\S*|application\/xml|\S*\/\S*\+xml)\s*;.*charset\s*=\s*utf-8/i.test(o.type)?new Blob(["\ufeff",o],{type:o.type}):o}(o,m),i);else if(g(o))h(o,i,m);else{var s=document.createElement("a");s.href=o,s.target="_blank",setTimeout(function(){C(s)})}}:function(o,i,m,s){if((s=s||open("","_blank"))&&(s.document.title=s.document.body.innerText="downloading..."),"string"==typeof o)return h(o,i,m);var c="application/octet-stream"===o.type,y=/constructor/i.test(_.HTMLElement)||_.safari,x=/CriOS\/[\d]+/.test(navigator.userAgent);if((x||c&&y||v)&&"undefined"!=typeof FileReader){var P=new FileReader;P.onloadend=function(){var w=P.result;w=x?w:w.replace(/^data:[^;]*;/,"data:attachment/file;"),s?s.location.href=w:location=w,s=null},P.readAsDataURL(o)}else{var A=_.URL||_.webkitURL,S=A.createObjectURL(o);s?s.location=S:location.href=S,s=null,setTimeout(function(){A.revokeObjectURL(S)},4e4)}});_.saveAs=T.saveAs=T,E.exports=T}.apply(b,[]))&&(E.exports=d)},4080:(E,b,l)=>{"use strict";l.d(b,{y:()=>d});const e=["rgb(160,227,183)","rgb(92,47,142)","rgb(141,186,34)","rgb(197,81,220)","rgb(30,123,32)","rgb(255,107,151)","rgb(63,244,76)","rgb(133,30,57)","rgb(33,240,182)","rgb(44,69,125)","rgb(106,179,225)","rgb(10,79,78)","rgb(248,166,112)","rgb(101,61,40)","rgb(226,198,39)","rgb(43,63,255)","rgb(233,180,245)","rgb(98,125,227)","rgb(128,151,118)","rgb(209,31,11)"],d=function(f){return e.slice(0,f)}},1113:(E,b,l)=>{"use strict";l.d(b,{v:()=>w});var e=l(3668),d=l(277),f=l(5043),h=l(7582),g=l(9232),C=l(471),_=l(6019),v=l(8638),T=l(9133),o=l(4250),i=l(3856);function m(r,p){if(1&r){const t=e.EpF();e.TgZ(0,"app-define-filter-steps",12),e.NdJ("filterStepsInfo$",function(a){return e.CHM(t),e.oxw().filterTerms(a)}),e.qZA()}if(2&r){const t=e.oxw();e.Q6J("dataAttributes",t.features)}}function s(r,p){1&r&&(e.TgZ(0,"th"),e._uU(1,"Select"),e.qZA())}function c(r,p){if(1&r&&(e.TgZ(0,"th"),e._uU(1),e.qZA()),2&r){const t=e.oxw();e.xp6(1),e.Oqu(t.viewPlotName)}}function y(r,p){if(1&r){const t=e.EpF();e.TgZ(0,"th",13),e.NdJ("sort",function(a){return e.CHM(t),e.oxw().onSort(a)}),e._uU(1),e.qZA()}if(2&r){const t=p.$implicit;e.s9C("sortableColumn",t),e.xp6(1),e.hij(" ",t," ")}}function x(r,p){if(1&r){const t=e.EpF();e.TgZ(0,"td"),e.TgZ(1,"input",15),e.NdJ("click",function(a){return e.CHM(t),e.oxw(2).selectedOrCancelItem(a)}),e.qZA(),e.qZA()}if(2&r){const t=e.oxw().$implicit,n=e.oxw();e.xp6(1),e.Q6J("checked",n.selectedIndexColumns.includes(t[n.uniqueFeature]))("value",t[n.uniqueFeature])}}function P(r,p){if(1&r){const t=e.EpF();e.TgZ(0,"td",16),e.NdJ("click",function(){e.CHM(t);const a=e.oxw().$implicit,u=e.oxw();return u.processSelectedGeneForPlot(a[u.uniqueFeature])}),e.TgZ(1,"div",17),e._UZ(2,"fa-icon",18),e.qZA(),e.qZA()}if(2&r){const t=e.oxw(2);e.xp6(2),e.Q6J("icon",t.faChartLine)("size","1x")("ngbTooltip",t.viewPlotName)}}function A(r,p){if(1&r&&(e.TgZ(0,"td"),e._uU(1),e.qZA()),2&r){const t=p.$implicit,n=e.oxw().$implicit;e.xp6(1),e.hij(" ",n[t]," ")}}function S(r,p){if(1&r&&(e.TgZ(0,"tr"),e.YNc(1,x,2,2,"td",3),e.YNc(2,P,3,3,"td",14),e.YNc(3,A,2,1,"td",6),e.qZA()),2&r){const t=e.oxw();e.xp6(1),e.Q6J("ngIf",t.ifShowSelectIcon),e.xp6(1),e.Q6J("ngIf",t.ifShowViewPlotIcon),e.xp6(1),e.Q6J("ngForOf",t.features)}}let w=(()=>{class r{constructor(t){this.cdr=t,this.ifShowViewPlotIcon=!0,this.ifShowSelectIcon=!0,this.ifShowFilterIcon=!0,this.selectedItems$=new e.vpe,this.clickedTermForPlot$=new e.vpe,this.page=1,this.pageSize=5,this.faArrowUp=f.FPD,this.faArrowDown=f.r5q,this.faChartLine=f.Stf,this.selectedIndexColumns=[]}ngOnInit(){this.termsInfoForTable&&(this.selectedIndexColumns=[],this._prepareForTable(),this.refreshSubTermsInfo())}ngOnChanges(t){t.termsInfoForTable&&!t.termsInfoForTable.isFirstChange()&&(this.selectedIndexColumns=[],this._prepareForTable(),this.refreshSubTermsInfo())}_prepareForTable(){this.features=[...this.termsInfoForTable.features],this.termsInfo=[...this.termsInfoForTable.termsInfo],this.filteredTermsInfo=[...this.termsInfoForTable.termsInfo],this.collectionSize=this.termsInfo.length}refreshSubTermsInfo(){this.subTermsInfo=this.filteredTermsInfo.slice((this.page-1)*this.pageSize,(this.page-1)*this.pageSize+this.pageSize),this.cdr.detectChanges()}onSort({column:t,direction:n}){this.headers.forEach(a=>{a.sortableColumn!==t&&(a.direction="")}),(""!=n||""!=t)&&(this.filteredTermsInfo=[...this.filteredTermsInfo].sort((a,u)=>{const I=(0,h.q)(a[t],u[t]);return"asc"===n?I:-I}),this.refreshSubTermsInfo())}selectedOrCancelItem(t){const a=t.target.value;t.target.checked?this.selectedIndexColumns.push(a):this.selectedIndexColumns.splice(this.selectedIndexColumns.indexOf(a),1),this.selectedItems$.next(this.selectedIndexColumns)}processSelectedGeneForPlot(t){this.clickedTermForPlot$.next(t)}filterTerms(t){const n=t.matchType;let a=[];if(t.filterSteps.length>=1){for(let I of t.filterSteps){const D=I.attribute,F=I.filterType,O=I.filterValue.toLowerCase();let M=this.termsInfo.map(U=>U[D]);const Z=g.qP[F](M,O);a.push(new Set(Z))}const u=a.reduce(C.JN[n]);this.filteredTermsInfo=[...u].map(I=>this.termsInfo[I])}else this.filteredTermsInfo=[...this.termsInfo];this.collectionSize=this.filteredTermsInfo.length,this.refreshSubTermsInfo()}}return r.\u0275fac=function(t){return new(t||r)(e.Y36(e.sBO))},r.\u0275cmp=e.Xpm({type:r,selectors:[["app-display-terms-info-table-pagination"]],viewQuery:function(t,n){if(1&t&&e.Gf(d.Y,5),2&t){let a;e.iGM(a=e.CRH())&&(n.headers=a)}},inputs:{termsInfoForTable:"termsInfoForTable",termName:"termName",uniqueFeature:"uniqueFeature",viewPlotName:"viewPlotName",ifShowViewPlotIcon:"ifShowViewPlotIcon",ifShowSelectIcon:"ifShowSelectIcon",ifShowFilterIcon:"ifShowFilterIcon"},outputs:{selectedItems$:"selectedItems$",clickedTermForPlot$:"clickedTermForPlot$"},features:[e.TTD],decls:21,vars:15,consts:[["class","mt-1",3,"dataAttributes","filterStepsInfo$",4,"ngIf"],[1,"table-responsive",2,"margin-left","10px","margin-right","10px"],[1,"table"],[4,"ngIf"],["sortable","",3,"sortableColumn","sort",4,"ngFor","ngForOf"],[1,"border-bottom"],[4,"ngFor","ngForOf"],[1,"d-flex","justify-content-between","align-items-center","p-2"],["data-testid","termsNum"],[3,"collectionSize","page","pageSize","maxSize","pageChange"],[1,"custom-select","mb-3",2,"width","auto",3,"ngModel","ngModelChange"],[3,"ngValue"],[1,"mt-1",3,"dataAttributes","filterStepsInfo$"],["sortable","",3,"sortableColumn","sort"],[3,"click",4,"ngIf"],["type","checkbox",3,"checked","value","click"],[3,"click"],[1,"form-inline"],[1,"hoverBigger",3,"icon","size","ngbTooltip"]],template:function(t,n){1&t&&(e.YNc(0,m,1,1,"app-define-filter-steps",0),e.TgZ(1,"div",1),e.TgZ(2,"table",2),e.TgZ(3,"thead"),e.TgZ(4,"tr"),e.YNc(5,s,2,0,"th",3),e.YNc(6,c,2,1,"th",3),e.YNc(7,y,2,2,"th",4),e.qZA(),e.qZA(),e.TgZ(8,"tbody",5),e.YNc(9,S,4,3,"tr",6),e.qZA(),e.qZA(),e.qZA(),e.TgZ(10,"div",7),e.TgZ(11,"p",8),e._uU(12),e.qZA(),e.TgZ(13,"ngb-pagination",9),e.NdJ("pageChange",function(u){return n.page=u})("pageChange",function(){return n.refreshSubTermsInfo()}),e.qZA(),e.TgZ(14,"select",10),e.NdJ("ngModelChange",function(u){return n.pageSize=u})("ngModelChange",function(){return n.refreshSubTermsInfo()}),e.TgZ(15,"option",11),e._uU(16,"5 per page"),e.qZA(),e.TgZ(17,"option",11),e._uU(18,"10 per page"),e.qZA(),e.TgZ(19,"option",11),e._uU(20,"20 per page"),e.qZA(),e.qZA(),e.qZA()),2&t&&(e.Q6J("ngIf",n.ifShowFilterIcon),e.xp6(5),e.Q6J("ngIf",n.ifShowSelectIcon),e.xp6(1),e.Q6J("ngIf",n.ifShowViewPlotIcon),e.xp6(1),e.Q6J("ngForOf",n.features),e.xp6(2),e.Q6J("ngForOf",n.subTermsInfo),e.xp6(3),e.AsE(" ",n.collectionSize," ",n.termName," "),e.xp6(1),e.Q6J("collectionSize",n.collectionSize)("page",n.page)("pageSize",n.pageSize)("maxSize",5),e.xp6(1),e.Q6J("ngModel",n.pageSize),e.xp6(1),e.Q6J("ngValue",5),e.xp6(2),e.Q6J("ngValue",10),e.xp6(2),e.Q6J("ngValue",20))},directives:[_.O5,_.sg,v.N9,T.EJ,T.JJ,T.On,T.YN,T.Kr,o.u,d.Y,i.BN,v._L],styles:[""],changeDetection:0}),r})()},5346:(E,b,l)=>{"use strict";l.d(b,{B:()=>d});var e=l(3668);let d=(()=>{class f{transform(g,...C){if(g&&g.length>=1)return[...g].reverse()}}return f.\u0275fac=function(g){return new(g||f)},f.\u0275pipe=e.Yjl({name:"reverse",type:f,pure:!0}),f})()}}]);