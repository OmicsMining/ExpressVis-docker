"use strict";(self.webpackChunkclient=self.webpackChunkclient||[]).push([[636],{648:(L,v,a)=>{a.d(v,{n:()=>O});var h=a(3856),p=a(5043),f=a(9637),y=a(3668);let O=(()=>{class d{constructor(g,T,x){this.vcr=g,this.ele=T,this.renderer=x,this.pngName="",this.faDownload=p.q7m;const N=this.vcr.createComponent(h.BN);N.instance.icon=p.q7m,N.instance.classes=["hoverBigger"],N.instance.render(),this.renderer.listen(N.location.nativeElement,"click",()=>{const M=this.ele.nativeElement.querySelector("svg");(0,f.saveSvgAsPng)(M,this.pngName,{backgroundColor:"white",scale:5})})}ngAfterViewInit(){}}return d.\u0275fac=function(g){return new(g||d)(y.Y36(y.s_b),y.Y36(y.SBq),y.Y36(y.Qsj))},d.\u0275dir=y.lG2({type:d,selectors:[["","appD3Download",""]],inputs:{pngName:"pngName"}}),d})()},6520:(L,v,a)=>{function h(f){return function(){return this.matches(f)}}function p(f){return function(E){return E.matches(f)}}a.d(v,{Z:()=>h,P:()=>p})},3438:(L,v,a)=>{a.d(v,{Z:()=>p});var h=a(3183);function p(f){var E=f+="",y=E.indexOf(":");return y>=0&&"xmlns"!==(E=f.slice(0,y))&&(f=f.slice(y+1)),h.Z.hasOwnProperty(E)?{space:h.Z[E],local:f}:f}},3183:(L,v,a)=>{a.d(v,{P:()=>h,Z:()=>p});var h="http://www.w3.org/1999/xhtml";const p={svg:"http://www.w3.org/2000/svg",xhtml:h,xlink:"http://www.w3.org/1999/xlink",xml:"http://www.w3.org/XML/1998/namespace",xmlns:"http://www.w3.org/2000/xmlns/"}},766:(L,v,a)=>{a.d(v,{Z:()=>p});var h=a(5284);function p(f){return"string"==typeof f?new h.Y1([[document.querySelector(f)]],[document.documentElement]):new h.Y1([[f]],h.Jz)}},5284:(L,v,a)=>{a.d(v,{Y1:()=>w,ZP:()=>vn,Jz:()=>Y});var h=a(1626);function f(t){return null==t?[]:Array.isArray(t)?t:Array.from(t)}var E=a(566),d=a(6520),m=Array.prototype.find;function T(){return this.firstElementChild}var N=Array.prototype.filter;function M(){return Array.from(this.children)}function F(t){return new Array(t.length)}function S(t,n){this.ownerDocument=t.ownerDocument,this.namespaceURI=t.namespaceURI,this._next=null,this._parent=t,this.__data__=n}function nt(t){return function(){return t}}function et(t,n,r,i,e,s){for(var o,u=0,l=n.length,c=s.length;u<c;++u)(o=n[u])?(o.__data__=s[u],i[u]=o):r[u]=new S(t,s[u]);for(;u<l;++u)(o=n[u])&&(e[u]=o)}function rt(t,n,r,i,e,s,u){var o,l,A,c=new Map,_=n.length,P=s.length,C=new Array(_);for(o=0;o<_;++o)(l=n[o])&&(C[o]=A=u.call(l,l.__data__,o,n)+"",c.has(A)?e[o]=l:c.set(A,l));for(o=0;o<P;++o)A=u.call(t,s[o],o,s)+"",(l=c.get(A))?(i[o]=l,l.__data__=s[o],c.delete(A)):r[o]=new S(t,s[o]);for(o=0;o<_;++o)(l=n[o])&&c.get(C[o])===l&&(e[o]=l)}function it(t){return t.__data__}function ot(t){return"object"==typeof t&&"length"in t?t:Array.from(t)}function _t(t,n){return t<n?-1:t>n?1:t>=n?0:NaN}S.prototype={constructor:S,appendChild:function(t){return this._parent.insertBefore(t,this._next)},insertBefore:function(t,n){return this._parent.insertBefore(t,n)},querySelector:function(t){return this._parent.querySelector(t)},querySelectorAll:function(t){return this._parent.querySelectorAll(t)}};var U=a(3438);function gt(t){return function(){this.removeAttribute(t)}}function wt(t){return function(){this.removeAttributeNS(t.space,t.local)}}function At(t,n){return function(){this.setAttribute(t,n)}}function Et(t,n){return function(){this.setAttributeNS(t.space,t.local,n)}}function Pt(t,n){return function(){var r=n.apply(this,arguments);null==r?this.removeAttribute(t):this.setAttribute(t,r)}}function Ct(t,n){return function(){var r=n.apply(this,arguments);null==r?this.removeAttributeNS(t.space,t.local):this.setAttributeNS(t.space,t.local,r)}}var Lt=a(6521);function Ot(t){return function(){delete this[t]}}function Tt(t,n){return function(){this[t]=n}}function Nt(t,n){return function(){var r=n.apply(this,arguments);null==r?delete this[t]:this[t]=r}}function Z(t){return t.trim().split(/^|\s+/)}function b(t){return t.classList||new K(t)}function K(t){this._node=t,this._names=Z(t.getAttribute("class")||"")}function W(t,n){for(var r=b(t),i=-1,e=n.length;++i<e;)r.add(n[i])}function I(t,n){for(var r=b(t),i=-1,e=n.length;++i<e;)r.remove(n[i])}function St(t){return function(){W(this,t)}}function Bt(t){return function(){I(this,t)}}function xt(t,n){return function(){(n.apply(this,arguments)?W:I)(this,t)}}function bt(){this.textContent=""}function Ft(t){return function(){this.textContent=t}}function Ut(t){return function(){var n=t.apply(this,arguments);this.textContent=null==n?"":n}}function Kt(){this.innerHTML=""}function Wt(t){return function(){this.innerHTML=t}}function It(t){return function(){var n=t.apply(this,arguments);this.innerHTML=null==n?"":n}}function Vt(){this.nextSibling&&this.parentNode.appendChild(this)}function Yt(){this.previousSibling&&this.parentNode.insertBefore(this,this.parentNode.firstChild)}K.prototype={add:function(t){this._names.indexOf(t)<0&&(this._names.push(t),this._node.setAttribute("class",this._names.join(" ")))},remove:function(t){var n=this._names.indexOf(t);n>=0&&(this._names.splice(n,1),this._node.setAttribute("class",this._names.join(" ")))},contains:function(t){return this._names.indexOf(t)>=0}};var k=a(3183);function Ht(t){return function(){var n=this.ownerDocument,r=this.namespaceURI;return r===k.P&&n.documentElement.namespaceURI===k.P?n.createElement(t):n.createElementNS(r,t)}}function Jt(t){return function(){return this.ownerDocument.createElementNS(t.space,t.local)}}function V(t){var n=(0,U.Z)(t);return(n.local?Jt:Ht)(n)}function $t(){return null}function qt(){var t=this.parentNode;t&&t.removeChild(this)}function tn(){var t=this.cloneNode(!1),n=this.parentNode;return n?n.insertBefore(t,this.nextSibling):t}function nn(){var t=this.cloneNode(!0),n=this.parentNode;return n?n.insertBefore(t,this.nextSibling):t}function on(t){return t.trim().split(/^|\s+/).map(function(n){var r="",i=n.indexOf(".");return i>=0&&(r=n.slice(i+1),n=n.slice(0,i)),{type:n,name:r}})}function un(t){return function(){var n=this.__on;if(n){for(var s,r=0,i=-1,e=n.length;r<e;++r)s=n[r],t.type&&s.type!==t.type||s.name!==t.name?n[++i]=s:this.removeEventListener(s.type,s.listener,s.options);++i?n.length=i:delete this.__on}}}function ln(t,n,r){return function(){var e,i=this.__on,s=function(t){return function(n){t.call(this,n,this.__data__)}}(n);if(i)for(var u=0,o=i.length;u<o;++u)if((e=i[u]).type===t.type&&e.name===t.name)return this.removeEventListener(e.type,e.listener,e.options),this.addEventListener(e.type,e.listener=s,e.options=r),void(e.value=n);this.addEventListener(t.type,s,r),e={type:t.type,name:t.name,value:n,listener:s,options:r},i?i.push(e):this.__on=[e]}}var an=a(1196);function X(t,n,r){var i=(0,an.Z)(t),e=i.CustomEvent;"function"==typeof e?e=new e(n,r):(e=i.document.createEvent("Event"),r?(e.initEvent(n,r.bubbles,r.cancelable),e.detail=r.detail):e.initEvent(n,!1,!1)),t.dispatchEvent(e)}function fn(t,n){return function(){return X(this,t,n)}}function _n(t,n){return function(){return X(this,t,n.apply(this,arguments))}}var Y=[null];function w(t,n){this._groups=t,this._parents=n}function z(){return new w([[document.documentElement]],Y)}w.prototype=z.prototype={constructor:w,select:function(t){"function"!=typeof t&&(t=(0,h.Z)(t));for(var n=this._groups,r=n.length,i=new Array(r),e=0;e<r;++e)for(var l,c,s=n[e],u=s.length,o=i[e]=new Array(u),_=0;_<u;++_)(l=s[_])&&(c=t.call(l,l.__data__,_,s))&&("__data__"in l&&(c.__data__=l.__data__),o[_]=c);return new w(i,this._parents)},selectAll:function(t){t="function"==typeof t?function(t){return function(){return f(t.apply(this,arguments))}}(t):(0,E.Z)(t);for(var n=this._groups,r=n.length,i=[],e=[],s=0;s<r;++s)for(var l,u=n[s],o=u.length,c=0;c<o;++c)(l=u[c])&&(i.push(t.call(l,l.__data__,c,u)),e.push(l));return new w(i,e)},selectChild:function(t){return this.select(null==t?T:function(t){return function(){return m.call(this.children,t)}}("function"==typeof t?t:(0,d.P)(t)))},selectChildren:function(t){return this.selectAll(null==t?M:function(t){return function(){return N.call(this.children,t)}}("function"==typeof t?t:(0,d.P)(t)))},filter:function(t){"function"!=typeof t&&(t=(0,d.Z)(t));for(var n=this._groups,r=n.length,i=new Array(r),e=0;e<r;++e)for(var l,s=n[e],u=s.length,o=i[e]=[],c=0;c<u;++c)(l=s[c])&&t.call(l,l.__data__,c,s)&&o.push(l);return new w(i,this._parents)},data:function(t,n){if(!arguments.length)return Array.from(this,it);var r=n?rt:et,i=this._parents,e=this._groups;"function"!=typeof t&&(t=nt(t));for(var s=e.length,u=new Array(s),o=new Array(s),l=new Array(s),c=0;c<s;++c){var _=i[c],P=e[c],C=P.length,A=ot(t.call(_,_&&_.__data__,c,i)),D=A.length,H=o[c]=new Array(D),J=u[c]=new Array(D),yn=l[c]=new Array(C);r(_,P,H,J,yn,A,n);for(var Q,$,R=0,B=0;R<D;++R)if(Q=H[R]){for(R>=B&&(B=R+1);!($=J[B])&&++B<D;);Q._next=$||null}}return(u=new w(u,i))._enter=o,u._exit=l,u},enter:function(){return new w(this._enter||this._groups.map(F),this._parents)},exit:function(){return new w(this._exit||this._groups.map(F),this._parents)},join:function(t,n,r){var i=this.enter(),e=this,s=this.exit();return"function"==typeof t?(i=t(i))&&(i=i.selection()):i=i.append(t+""),null!=n&&(e=n(e))&&(e=e.selection()),null==r?s.remove():r(s),i&&e?i.merge(e).order():e},merge:function(t){for(var n=t.selection?t.selection():t,r=this._groups,i=n._groups,e=r.length,u=Math.min(e,i.length),o=new Array(e),l=0;l<u;++l)for(var A,c=r[l],_=i[l],P=c.length,C=o[l]=new Array(P),D=0;D<P;++D)(A=c[D]||_[D])&&(C[D]=A);for(;l<e;++l)o[l]=r[l];return new w(o,this._parents)},selection:function(){return this},order:function(){for(var t=this._groups,n=-1,r=t.length;++n<r;)for(var u,i=t[n],e=i.length-1,s=i[e];--e>=0;)(u=i[e])&&(s&&4^u.compareDocumentPosition(s)&&s.parentNode.insertBefore(u,s),s=u);return this},sort:function(t){function n(P,C){return P&&C?t(P.__data__,C.__data__):!P-!C}t||(t=_t);for(var r=this._groups,i=r.length,e=new Array(i),s=0;s<i;++s){for(var c,u=r[s],o=u.length,l=e[s]=new Array(o),_=0;_<o;++_)(c=u[_])&&(l[_]=c);l.sort(n)}return new w(e,this._parents).order()},call:function(){var t=arguments[0];return arguments[0]=this,t.apply(null,arguments),this},nodes:function(){return Array.from(this)},node:function(){for(var t=this._groups,n=0,r=t.length;n<r;++n)for(var i=t[n],e=0,s=i.length;e<s;++e){var u=i[e];if(u)return u}return null},size:function(){let t=0;for(const n of this)++t;return t},empty:function(){return!this.node()},each:function(t){for(var n=this._groups,r=0,i=n.length;r<i;++r)for(var o,e=n[r],s=0,u=e.length;s<u;++s)(o=e[s])&&t.call(o,o.__data__,s,e);return this},attr:function(t,n){var r=(0,U.Z)(t);if(arguments.length<2){var i=this.node();return r.local?i.getAttributeNS(r.space,r.local):i.getAttribute(r)}return this.each((null==n?r.local?wt:gt:"function"==typeof n?r.local?Ct:Pt:r.local?Et:At)(r,n))},style:Lt.Z,property:function(t,n){return arguments.length>1?this.each((null==n?Ot:"function"==typeof n?Nt:Tt)(t,n)):this.node()[t]},classed:function(t,n){var r=Z(t+"");if(arguments.length<2){for(var i=b(this.node()),e=-1,s=r.length;++e<s;)if(!i.contains(r[e]))return!1;return!0}return this.each(("function"==typeof n?xt:n?St:Bt)(r,n))},text:function(t){return arguments.length?this.each(null==t?bt:("function"==typeof t?Ut:Ft)(t)):this.node().textContent},html:function(t){return arguments.length?this.each(null==t?Kt:("function"==typeof t?It:Wt)(t)):this.node().innerHTML},raise:function(){return this.each(Vt)},lower:function(){return this.each(Yt)},append:function(t){var n="function"==typeof t?t:V(t);return this.select(function(){return this.appendChild(n.apply(this,arguments))})},insert:function(t,n){var r="function"==typeof t?t:V(t),i=null==n?$t:"function"==typeof n?n:(0,h.Z)(n);return this.select(function(){return this.insertBefore(r.apply(this,arguments),i.apply(this,arguments)||null)})},remove:function(){return this.each(qt)},clone:function(t){return this.select(t?nn:tn)},datum:function(t){return arguments.length?this.property("__data__",t):this.node().__data__},on:function(t,n,r){var e,u,i=on(t+""),s=i.length;if(!(arguments.length<2)){for(o=n?ln:un,e=0;e<s;++e)this.each(o(i[e],n,r));return this}var o=this.node().__on;if(o)for(var _,l=0,c=o.length;l<c;++l)for(e=0,_=o[l];e<s;++e)if((u=i[e]).type===_.type&&u.name===_.name)return _.value},dispatch:function(t,n){return this.each(("function"==typeof n?_n:fn)(t,n))},[Symbol.iterator]:function*(){for(var t=this._groups,n=0,r=t.length;n<r;++n)for(var u,i=t[n],e=0,s=i.length;e<s;++e)(u=i[e])&&(yield u)}};const vn=z},6521:(L,v,a)=>{a.d(v,{Z:()=>y,S:()=>O});var h=a(1196);function p(d){return function(){this.style.removeProperty(d)}}function f(d,m,g){return function(){this.style.setProperty(d,m,g)}}function E(d,m,g){return function(){var T=m.apply(this,arguments);null==T?this.style.removeProperty(d):this.style.setProperty(d,T,g)}}function y(d,m,g){return arguments.length>1?this.each((null==m?p:"function"==typeof m?E:f)(d,m,null==g?"":g)):O(this.node(),d)}function O(d,m){return d.style.getPropertyValue(m)||(0,h.Z)(d).getComputedStyle(d,null).getPropertyValue(m)}},1626:(L,v,a)=>{function h(){}function p(f){return null==f?h:function(){return this.querySelector(f)}}a.d(v,{Z:()=>p})},566:(L,v,a)=>{function h(){return[]}function p(f){return null==f?h:function(){return this.querySelectorAll(f)}}a.d(v,{Z:()=>p})},1196:(L,v,a)=>{function h(p){return p.ownerDocument&&p.ownerDocument.defaultView||p.document&&p||p.defaultView}a.d(v,{Z:()=>h})}}]);