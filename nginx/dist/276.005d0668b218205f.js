"use strict";(self.webpackChunkclient=self.webpackChunkclient||[]).push([[276],{3128:(D,O,e)=>{e.d(O,{O:()=>o});var t=e(3668);let o=(()=>{class r{constructor(a){this.tpl=a}}return r.\u0275fac=function(a){return new(a||r)(t.Y36(t.Rgc))},r.\u0275dir=t.lG2({type:r,selectors:[["","appEditableEdit",""]]}),r})()},5903:(D,O,e)=>{e.d(O,{_:()=>r});var t=e(3668),o=e(1789);let r=(()=>{class c{constructor(u,s){this.editable=u,this.host=s}onEnter(){""!=this.host.nativeElement.value&&this.editable.toViewMode()}}return c.\u0275fac=function(u){return new(u||c)(t.Y36(o.y),t.Y36(t.SBq))},c.\u0275dir=t.lG2({type:c,selectors:[["","appEditableOnEnter",""]],hostBindings:function(u,s){1&u&&t.NdJ("keyup.enter",function(){return s.onEnter()})}}),c})()},9879:(D,O,e)=>{e.d(O,{i:()=>o});var t=e(3668);let o=(()=>{class r{constructor(a){this.tpl=a}}return r.\u0275fac=function(a){return new(a||r)(t.Y36(t.Rgc))},r.\u0275dir=t.lG2({type:r,selectors:[["","appEditableView",""]]}),r})()},1789:(D,O,e)=>{e.d(O,{y:()=>w});var t=e(3668),o=e(9879),r=e(3128),c=e(5433),a=e(5894),u=e(4168),s=e(4352),p=e(8345);class g{constructor(i){this.resultSelector=i}call(i,n){return n.subscribe(new I(i,this.resultSelector))}}class I extends u.L{constructor(i,n,m=Object.create(null)){super(i),this.resultSelector=n,this.iterators=[],this.active=0,this.resultSelector="function"==typeof n?n:void 0}_next(i){const n=this.iterators;(0,a.k)(i)?n.push(new f(i)):n.push("function"==typeof i[s.hZ]?new C(i[s.hZ]()):new _(this.destination,this,i))}_complete(){const i=this.iterators,n=i.length;if(this.unsubscribe(),0!==n){this.active=n;for(let m=0;m<n;m++){let b=i[m];b.stillUnsubscribed?this.destination.add(b.subscribe()):this.active--}}else this.destination.complete()}notifyInactive(){this.active--,0===this.active&&this.destination.complete()}checkIterators(){const i=this.iterators,n=i.length,m=this.destination;for(let y=0;y<n;y++){let M=i[y];if("function"==typeof M.hasValue&&!M.hasValue())return}let b=!1;const v=[];for(let y=0;y<n;y++){let M=i[y],L=M.next();if(M.hasCompleted()&&(b=!0),L.done)return void m.complete();v.push(L.value)}this.resultSelector?this._tryresultSelector(v):m.next(v),b&&m.complete()}_tryresultSelector(i){let n;try{n=this.resultSelector.apply(this,i)}catch(m){return void this.destination.error(m)}this.destination.next(n)}}class C{constructor(i){this.iterator=i,this.nextResult=i.next()}hasValue(){return!0}next(){const i=this.nextResult;return this.nextResult=this.iterator.next(),i}hasCompleted(){const i=this.nextResult;return Boolean(i&&i.done)}}class f{constructor(i){this.array=i,this.index=0,this.length=0,this.length=i.length}[s.hZ](){return this}next(i){const n=this.index++;return n<this.length?{value:this.array[n],done:!1}:{value:null,done:!0}}hasValue(){return this.array.length>this.index}hasCompleted(){return this.array.length===this.index}}class _ extends p.Ds{constructor(i,n,m){super(i),this.parent=n,this.observable=m,this.stillUnsubscribed=!0,this.buffer=[],this.isComplete=!1}[s.hZ](){return this}next(){const i=this.buffer;return 0===i.length&&this.isComplete?{value:null,done:!0}:{value:i.shift(),done:!1}}hasValue(){return this.buffer.length>0}hasCompleted(){return 0===this.buffer.length&&this.isComplete}notifyComplete(){this.buffer.length>0?(this.isComplete=!0,this.parent.notifyInactive()):this.destination.complete()}notifyNext(i){this.buffer.push(i),this.parent.checkIterators()}subscribe(){return(0,p.ft)(this.observable,new p.IY(this))}}var h=e(3405),l=e(6087),T=e(2668),A=e(9204);function P(E,i){return i?(0,A.w)(()=>E,i):(0,A.w)(()=>E)}var S=e(8805),x=e(8735),j=e(8053),F=e(6636),R=e(6019);function N(E,i){1&E&&t.GkF(0)}let w=(()=>{class E{constructor(n,m,b){this.host=n,this.cdr=m,this.update=new t.vpe,this.editMode=new h.xQ,this.editMode$=this.editMode.asObservable(),this.destroyNotifier$=new h.xQ,this.mode=b}ngOnInit(){this.viewModeHander(),this.editModeHandler(),"edit"===this.mode&&this.editMode.next(!0)}ngOnDestroy(){this.destroyNotifier$.next(),this.destroyNotifier$.complete()}toViewMode(){this.update.next(),this.mode="view"}get currentView(){return"view"===this.mode?this.viewModeTpl.tpl:this.editModeTpl.tpl}get element(){return this.host.nativeElement}viewModeHander(){(0,l.R)(this.element,"dblclick").pipe((0,S.R)(this.destroyNotifier$)).subscribe(()=>{this.mode="edit",this.editMode.next(!0),this.cdr.detectChanges()})}editModeHandler(){const b=function(...E){const i=E[E.length-1];return"function"==typeof i&&E.pop(),(0,c.n)(E,void 0).lift(new g(i))}((0,l.R)(document,"mousedown").pipe((0,S.R)(this.destroyNotifier$),(0,x.h)(()=>this.element.querySelector("input")),(0,x.h)(()=>this.element.querySelector("input").value)),(0,l.R)(document,"mouseup").pipe((0,S.R)(this.destroyNotifier$),(0,x.h)(()=>this.element.querySelector("input")),(0,x.h)(()=>this.element.querySelector("input").value))).pipe((0,j.U)(([v,y])=>!1===this.element.contains(v.target)&&!1===this.element.contains(y.target)),(0,x.h)(v=>v),(0,F.q)(1));if("edit"===this.mode){const v=(0,l.R)(this.element,"input").pipe((0,j.U)(y=>y.target.value),(0,x.h)(y=>""!==y),(0,F.q)(1));(0,T.aj)([this.editMode$,v]).pipe(P(b),(0,S.R)(this.destroyNotifier$)).subscribe(y=>{this.element.querySelector("input").value&&(this.update.next(),this.mode="view")})}else this.editMode$.pipe(P(b),(0,S.R)(this.destroyNotifier$)).subscribe(v=>{this.element.querySelector("input").value&&(this.update.next(),this.mode="view",this.cdr.detectChanges())})}}return E.\u0275fac=function(n){return new(n||E)(t.Y36(t.SBq),t.Y36(t.sBO),t.$8M("initialMode"))},E.\u0275cmp=t.Xpm({type:E,selectors:[["app-editable"]],contentQueries:function(n,m,b){if(1&n&&(t.Suo(b,o.i,5),t.Suo(b,r.O,5)),2&n){let v;t.iGM(v=t.CRH())&&(m.viewModeTpl=v.first),t.iGM(v=t.CRH())&&(m.editModeTpl=v.first)}},outputs:{update:"update"},decls:1,vars:1,consts:[[4,"ngTemplateOutlet"]],template:function(n,m){1&n&&t.YNc(0,N,1,0,"ng-container",0),2&n&&t.Q6J("ngTemplateOutlet",m.currentView)},directives:[R.tP],encapsulation:2}),E})()},3991:(D,O,e)=>{e.d(O,{x:()=>o});var t=e(3668);let o=(()=>{class r{constructor(a){this.host=a}ngAfterViewInit(){this.host.nativeElement.focus()}}return r.\u0275fac=function(a){return new(a||r)(t.Y36(t.SBq))},r.\u0275dir=t.lG2({type:r,selectors:[["","appFocusable",""]]}),r})()},3139:(D,O,e)=>{e.d(O,{S:()=>r});var t=e(4099),o=e(3668);let r=(()=>{class c{constructor(){this.textLines=[],this.textMatrix=[],this.fileParseStatusSubject=new t.X(null),this.firstLinesSubject=new t.X(null),this.fileHeadersSubject=new t.X(null),this.fileParseStatus$=this.fileParseStatusSubject.asObservable(),this.firstLines$=this.firstLinesSubject.asObservable(),this.fileHeaders$=this.fileHeadersSubject.asObservable()}initLoadedFile(u){this.fileParseStatusSubject.next({status:"loading",statusValue:"loading"});const s=this._determineFileType(u.target.files[0]);"txt"===s||"TXT"===s?this._parseTextFile(u.target.files[0]):this._parseExcelFile(u)}_determineFileType(u){const p=u.name.split(".");return p[p.length-1]}_parseExcelFile(u){const s=u.target;if(1!==s.files.length)throw new Error("Cannot use multiple files");e.e(981).then(e.t.bind(e,3981,23)).then(p=>{const d=new FileReader;d.onload=g=>{const C=p.read(g.target.result,{raw:!0}),h=p.utils.sheet_to_json(C.Sheets[C.SheetNames[0]],{header:1});this.textMatrix=h,this.firstLinesSubject.next(this.obtainFirstLines(5)),this.fileHeadersSubject.next([...this.textMatrix][0]),this.fileParseStatusSubject.next({status:"finished",statusValue:"finished"})},d.readAsArrayBuffer(s.files[0])})}_parseTextFile(u){let s=new FileReader;s.readAsText(u),s.onload=p=>{this.textLines=s.result.trim().split("\n"),this.textMatrix=this.textLines.map(g=>g.trim().split("\t")),this.firstLinesSubject.next(this.obtainFirstLines(5)),this.fileHeadersSubject.next([...this.textLines][0].split("\t")),this.fileParseStatusSubject.next({status:"finished",statusValue:"finished"})}}obtainFirstLines(u){return[...this.textMatrix].slice(1,u+1)}}return c.\u0275fac=function(u){return new(u||c)},c.\u0275prov=o.Yz7({token:c,factory:c.\u0275fac}),c})()},4813:(D,O,e)=>{e.d(O,{w:()=>u});var t=e(3668),o=e(6019);function r(s,p){if(1&s&&(t.TgZ(0,"p",3),t._uU(1),t.qZA()),2&s){const d=p.$implicit;t.xp6(1),t.Oqu(d)}}function c(s,p){if(1&s){const d=t.EpF();t.TgZ(0,"p",4),t.NdJ("click",function(I){return t.CHM(d),t.oxw().displayAllItems(I)}),t.TgZ(1,"a",5),t._uU(2,"more"),t.qZA(),t.qZA()}}function a(s,p){if(1&s){const d=t.EpF();t.TgZ(0,"p",4),t.NdJ("click",function(I){return t.CHM(d),t.oxw().displayLimitedItems(I)}),t.TgZ(1,"a",6),t._uU(2,"less"),t.qZA(),t.qZA()}}let u=(()=>{class s{constructor(){this.ifDisplayAll=!1}ngOnInit(){this.items&&this._preprocessItems()}ngOnChanges(d){d.items&&!d.items.isFirstChange()&&this._preprocessItems()}_preprocessItems(){this.ifDisplayAll=!1,this.displayedItems=this.items.slice(0,this.displayNum).map(d=>d),this.items.length<=this.displayNum&&(this.ifDisplayAll=!0)}displayAllItems(d){this.displayedItems=this.items,this.ifDisplayAll=!0}displayLimitedItems(d){this._preprocessItems()}}return s.\u0275fac=function(d){return new(d||s)},s.\u0275cmp=t.Xpm({type:s,selectors:[["app-display-limited-items"]],inputs:{items:"items",displayNum:"displayNum"},features:[t.TTD],decls:4,vars:3,consts:[[1,"d-flex","justify-content-start","flex-wrap"],["class","ml-2",4,"ngFor","ngForOf"],["class","ml-2",3,"click",4,"ngIf"],[1,"ml-2"],[1,"ml-2",3,"click"],["href","javascript:void(0)"],["href","javascript:void(0);"]],template:function(d,g){1&d&&(t.TgZ(0,"div",0),t.YNc(1,r,2,1,"p",1),t.YNc(2,c,3,0,"p",2),t.YNc(3,a,3,0,"p",2),t.qZA()),2&d&&(t.xp6(1),t.Q6J("ngForOf",g.displayedItems),t.xp6(1),t.Q6J("ngIf",!g.ifDisplayAll&&(null==g.displayedItems?null:g.displayedItems.length)>0),t.xp6(1),t.Q6J("ngIf",g.ifDisplayAll&&(null==g.displayedItems?null:g.displayedItems.length)>g.displayNum))},directives:[o.sg,o.O5],styles:[""],changeDetection:0}),s})()},6872:(D,O,e)=>{e.d(O,{K:()=>o});var t=e(3668);let o=(()=>{class r{transform(a,u){let p;return p=a.length>u?a.substring(0,u)+"...":a,p}}return r.\u0275fac=function(a){return new(a||r)},r.\u0275pipe=t.Yjl({name:"trimString",type:r,pure:!0}),r})()},9769:(D,O,e)=>{e.d(O,{y:()=>f});var t=e(3668),o=e(9133),r=e(3405),c=e(8735),a=e(8805),u=e(5389),s=e(1789),p=e(9879),d=e(3128),g=e(5903);function I(_,h){if(1&_&&t._uU(0),2&_){const l=t.oxw();t.hij(" ",l.inputStringControl.value," ")}}function C(_,h){if(1&_&&t._UZ(0,"input",3),2&_){const l=t.oxw();t.s9C("placeholder",l.placeholder),t.Q6J("formControl",l.inputStringControl)}}let f=(()=>{class _{constructor(l){this.cdr=l,this.resetToDefault=!1,this.placeholder="default placeholder",this.inputString$=new t.vpe(null),this.inputStringControl=new o.NI(""),this.destroyNotifier$=new r.xQ}ngOnInit(){this.inputStringControl.valueChanges.pipe((0,c.h)(l=>l),(0,a.R)(this.destroyNotifier$),(0,u.x)()).subscribe(l=>{this.inputString$.emit(l),this.cdr.detectChanges()})}ngOnDestroy(){this.destroyNotifier$.next(),this.destroyNotifier$.complete()}}return _.\u0275fac=function(l){return new(l||_)(t.Y36(t.sBO))},_.\u0275cmp=t.Xpm({type:_,selectors:[["app-click-focus-input"]],inputs:{resetToDefault:"resetToDefault",placeholder:"placeholder"},outputs:{inputString$:"inputString$"},decls:3,vars:0,consts:[["initialMode","edit"],["appEditableView",""],["appEditableEdit",""],["appEditableOnEnter","","required","",1,"form-control","form-control-sm",3,"placeholder","formControl"]],template:function(l,T){1&l&&(t.TgZ(0,"app-editable",0),t.YNc(1,I,1,1,"ng-template",1),t.YNc(2,C,1,2,"ng-template",2),t.qZA())},directives:[s.y,p.i,d.O,o.Fj,g._,o.Q7,o.JJ,o.oH],styles:[""],changeDetection:0}),_})()},438:(D,O,e)=>{e.d(O,{w:()=>C});var t=e(3668),o=e(9133),r=e(3405),c=e(8735),a=e(8805),u=e(5389),s=e(6019);function p(f,_){if(1&f&&(t.TgZ(0,"option",5),t._uU(1),t.qZA()),2&f){const h=_.$implicit,l=t.oxw();t.Q6J("value",h[l.idAttribute]),t.xp6(1),t.hij(" ",h[l.displayAttribute]," ")}}function d(f,_){if(1&f&&(t.TgZ(0,"label",6),t._uU(1),t.qZA()),2&f){const h=t.oxw();t.xp6(1),t.hij(" ",h.emptyNote," ")}}const g=function(f){return{"form-inline":f}},I=function(f){return{"max-width":f}};let C=(()=>{class f{constructor(h){this.cdr=h,this.formInlineOrNot=!1,this.ifOutputFirstValue=!1,this.emptyNote="",this.ifWidthAuto=!1,this.formWidth="15rem",this.selectedItemObject$=new t.vpe,this.destroyNotifier$=new r.xQ,this.itemForm=new o.cw({itemValue:new o.NI("",o.kI.required)})}ngOnInit(){}ngAfterViewInit(){this.itemForm.get("itemValue").valueChanges.pipe((0,c.h)(h=>h),(0,a.R)(this.destroyNotifier$),(0,u.x)()).subscribe(h=>{if("VALID"===this.itemForm.get("itemValue").status){let l;for(let T of this.inputObjects)T[this.idAttribute]===h&&(l=T);this.selectedItemObject$.next(l)}else this.selectedItemObject$.next(null);this.cdr.detectChanges()}),this.ifOutputFirstValue&&this._outputSetFirstItemAsSelctedItem()}ngOnChanges(h){h.inputObjects&&h.inputObjects.isFirstChange()&&this.ifOutputFirstValue&&this._outputSetFirstItemAsSelctedItem()}ngOnDestroy(){this.destroyNotifier$.next(),this.destroyNotifier$.complete()}_outputSetFirstItemAsSelctedItem(){this.inputObjects&&this.inputObjects.length>=1&&this.itemForm.patchValue({itemValue:this.inputObjects[0][this.idAttribute]})}}return f.\u0275fac=function(h){return new(h||f)(t.Y36(t.sBO))},f.\u0275cmp=t.Xpm({type:f,selectors:[["app-select-item-object"]],inputs:{inputObjects:"inputObjects",idAttribute:"idAttribute",displayAttribute:"displayAttribute",itemLabel:"itemLabel",formInlineOrNot:"formInlineOrNot",ifOutputFirstValue:"ifOutputFirstValue",emptyNote:"emptyNote",ifWidthAuto:"ifWidthAuto",formWidth:"formWidth"},outputs:{selectedItemObject$:"selectedItemObject$"},features:[t.TTD],decls:7,vars:10,consts:[[3,"ngClass","formGroup"],[1,"align-self-start"],["formControlName","itemValue","data-testid","selectItem",1,"form-control","form-control-sm",3,"ngStyle"],[3,"value",4,"ngFor","ngForOf"],["class","text-danger font-weight-light",4,"ngIf"],[3,"value"],[1,"text-danger","font-weight-light"]],template:function(h,l){1&h&&(t.TgZ(0,"form",0),t.TgZ(1,"div",1),t.TgZ(2,"h5"),t._uU(3),t.qZA(),t.TgZ(4,"select",2),t.YNc(5,p,2,2,"option",3),t.qZA(),t.YNc(6,d,2,1,"label",4),t.qZA(),t.qZA()),2&h&&(t.Q6J("ngClass",t.VKq(6,g,l.formInlineOrNot))("formGroup",l.itemForm),t.xp6(3),t.hij("",l.itemLabel,":"),t.xp6(1),t.Q6J("ngStyle",t.VKq(8,I,l.ifWidthAuto?"none":l.formWidth)),t.xp6(1),t.Q6J("ngForOf",l.inputObjects),t.xp6(1),t.Q6J("ngIf",!((null==l.inputObjects?null:l.inputObjects.length)>=1)))},directives:[o._Y,o.JL,s.mk,o.sg,o.EJ,o.JJ,o.u,s.PC,s.sg,s.O5,o.YN,o.Kr],styles:[""],changeDetection:0}),f})()}}]);