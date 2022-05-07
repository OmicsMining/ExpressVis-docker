"use strict";(self.webpackChunkclient=self.webpackChunkclient||[]).push([[576],{6576:(d,g,r)=>{r.r(g),r.d(g,{HomeModule:()=>u});var a=r(6019),l=r(3928),n=r(1144),e=r(3668);let s=(()=>{class t{constructor({nativeElement:i}){"loading"in HTMLImageElement.prototype&&i.setAttribute("loading","lazy")}}return t.\u0275fac=function(i){return new(i||t)(e.Y36(e.SBq))},t.\u0275dir=e.lG2({type:t,selectors:[["","imgLazy",""]]}),t})();const Z=[{path:"",component:(()=>{class t{constructor(){}ngOnInit(){}}return t.\u0275fac=function(i){return new(i||t)},t.\u0275cmp=e.Xpm({type:t,selectors:[["app-home"]],decls:139,vars:0,consts:[[1,"row"],[1,"col-12",2,"background","url('/static/images/homePage01.png')","background-size","cover","height","30vh"],[1,"row","align-items-center","mt-2"],[1,"col-12","col-lg-10","offset-lg-1","text-center","text-md-left"],[1,"mb-3","bd-text-purple-bright",2,"color","#7952b3"],[1,"lead"],[1,"lead","mb-4"],[1,"text-info","font-weight-bold"],[1,"d-flex","flex-column","flex-md-row","lead","mb-3"],["routerLink","/importData",1,"btn","btn-lg","btn-expressvis","mb-3","mb-md-0","mr-md-3"],[1,"col-12","col-lg-10","offset-lg-1","d-flex","flex-wrap"],["routerLink","/DiffExp",1,"btn","btn-expressvis","mt-2","mr-2","mb-2"],["routerLink","/ClusterExp",1,"btn","btn-expressvis","m-2"],["routerLink","/SurvivalExp",1,"btn","btn-expressvis","m-2"],["routerLink","/KeggExp",1,"btn","btn-expressvis","m-2"],["routerLink","/PPIExp",1,"btn","btn-expressvis","m-2"],[1,"row","mt-4","ml-1","mr-1","ml-md-5","mr-md-5","ml-lg-5","mr-lg-5","navImage"],["clustering",""],[1,"col-12","col-lg-10","offset-lg-1","border"],[1,"row","flex-container","d-flex","align-items-center"],[1,"flex-container01","p-lg-5","p-md-3","p-sm-2","p-2"],["type","button","routerLink","/importData",1,"btn","fgvisBtn"],[1,"row","d-flex","align-items-center","mb-5"],["imgLazy","","src","/static/images/interactiveClustering.gif",1,"img-fluid","rounded","mx-auto","d-block","p-lg-5","p-md-3","p-sm-2","p-2"],["animateOnScroll","","animationName","fadeIn",1,"row","mt-5","ml-1","mr-1","ml-md-5","mr-md-5","ml-lg-5","mr-lg-5","navImage","animated"],["keggExploring",""],["imgLazy","","src","/static/images/keggExploring.gif",1,"img-fluid","rounded","mx-auto","d-block","p-lg-5","p-md-3","p-sm-2","p-2"],[1,"row","mt-5","ml-1","mr-1","ml-md-5","mr-md-5","ml-lg-5","mr-lg-5","navImage"],["dynamicNetwork",""],["imgLazy","","src","/static/images/networkExploring.gif",1,"img-fluid","rounded","mx-auto","d-block","p-lg-5","p-md-3","p-sm-2","p-2"],[1,"row","border","border-right-0","border-left-0","ml-5","mr-5","mb-5","mt-5",2,"background-color","#fff"],[1,"col-12","col-md-3","col-lg-3"],["href","http://mentha.uniroma2.it/index.php"],["href","http://geneontology.org/"],["href","http://www.genome.jp/kegg/pathway.html"],["href","https://reactome.org/"],["href","https://www.wikipathways.org/index.php/WikiPathways"],["href","http://homer.ucsd.edu/homer/index.html"],["href","https://angular.io/"],["href","http://js.cytoscape.org/"],["href","https://d3js.org/"],["href","https://getbootstrap.com/"],["href","https://www.djangoproject.com/"],["href","https://www.scipy.org/"],["routerLink","/dataPolicy"]],template:function(i,p){1&i&&(e.TgZ(0,"div",0),e._UZ(1,"div",1),e.qZA(),e.TgZ(2,"div",2),e.TgZ(3,"div",3),e.TgZ(4,"h1",4),e._uU(5,"ExpressVis"),e.qZA(),e.TgZ(6,"p",5),e._uU(7,"Take advantage of interactive visualization to obtain more biological insights and generate more testable hypotheses from your expression profile data."),e.qZA(),e._UZ(8,"p"),e.TgZ(9,"p",6),e._uU(10,"ExpressVis is an integrated visual analytic platform to speed up and improve a user's ability to generate and check hypothesis from expression profile data generated by Microarray, RNA-seq or Mass Spectrometry. It aims to get more biologists - including those without programming skills - involved into data analysis."),e.qZA(),e.TgZ(11,"p",7),e._uU(12,"ExpressVis is free and open to all and there is no login requirement"),e.qZA(),e.TgZ(13,"div",8),e.TgZ(14,"a",9),e._uU(15,"Data Import"),e.qZA(),e.qZA(),e.qZA(),e.qZA(),e.TgZ(16,"div",0),e.TgZ(17,"div",10),e.TgZ(18,"button",11),e._uU(19,"DiffExp"),e.qZA(),e.TgZ(20,"button",12),e._uU(21,"ClusterExp"),e.qZA(),e.TgZ(22,"button",13),e._uU(23,"SurvivalExp"),e.qZA(),e.TgZ(24,"button",14),e._uU(25,"KeggExp"),e.qZA(),e.TgZ(26,"button",15),e._uU(27,"PPIExp"),e.qZA(),e.qZA(),e.qZA(),e.TgZ(28,"div",16,17),e.TgZ(30,"div",18),e.TgZ(31,"div",19),e.TgZ(32,"div",20),e.TgZ(33,"h4"),e._uU(34,"Hirarchical clustering"),e.qZA(),e.TgZ(35,"p"),e._uU(36,"Cluster genes using using hirarchical clutering method and identify the genes with special expression pattern. Interactively select the genes from the Dendgrogram and perform pathway enrichment analysis."),e.qZA(),e.TgZ(37,"button",21),e._uU(38,"Get Started"),e.qZA(),e.qZA(),e.qZA(),e.TgZ(39,"div",22),e._UZ(40,"img",23),e.qZA(),e.qZA(),e.qZA(),e.TgZ(41,"div",24,25),e.TgZ(43,"div",18),e.TgZ(44,"div",19),e.TgZ(45,"div",20),e.TgZ(46,"h4"),e._uU(47,"KeggExp"),e.qZA(),e.TgZ(48,"p"),e._uU(49,"Visualize the expression pattern of all genes in the kegg pathway and dynamically highlight the genes in the pathway map"),e.qZA(),e.TgZ(50,"button",21),e._uU(51,"Get Started"),e.qZA(),e.qZA(),e.qZA(),e.TgZ(52,"div",22),e._UZ(53,"img",26),e.qZA(),e.qZA(),e.qZA(),e.TgZ(54,"div",27,28),e.TgZ(56,"div",18),e.TgZ(57,"div",19),e.TgZ(58,"div",20),e.TgZ(59,"h4"),e._uU(60,"PPIExp"),e.qZA(),e.TgZ(61,"p"),e._uU(62,"Construct the protein-protein interaction network. Visualize the genes expression pattern, and dynamically highlight the genes in the network map"),e.qZA(),e.TgZ(63,"button",21),e._uU(64,"Get Started"),e.qZA(),e.qZA(),e.qZA(),e.TgZ(65,"div",22),e._UZ(66,"img",29),e.qZA(),e.qZA(),e.qZA(),e.TgZ(67,"div",30),e.TgZ(68,"div",31),e.TgZ(69,"h5"),e._uU(70,"Contact"),e.qZA(),e.TgZ(71,"ul"),e.TgZ(72,"li"),e.TgZ(73,"strong"),e._uU(74,"Institute:"),e.qZA(),e._uU(75," State Key Laboratory of Proteomics"),e.qZA(),e.TgZ(76,"li"),e.TgZ(77,"strong"),e._uU(78,"Institute:"),e.qZA(),e._uU(79,"Beijing Institute of LifeOmics"),e.qZA(),e.TgZ(80,"li"),e.TgZ(81,"strong"),e._uU(82,"Address:"),e.qZA(),e._uU(83," No 38, life science road, Beijing, China"),e.qZA(),e.TgZ(84,"li"),e.TgZ(85,"strong"),e._uU(86,"E-mail:"),e.qZA(),e._uU(87," Xian Liu, Liux.bio@gmail.com"),e.qZA(),e.TgZ(88,"li"),e.TgZ(89,"strong"),e._uU(90,"E-mail:"),e.qZA(),e._uU(91," Cheng Chang, changchengbio@163.com"),e.qZA(),e.qZA(),e.qZA(),e.TgZ(92,"div",31),e.TgZ(93,"h5"),e._uU(94,"Resources"),e.qZA(),e.TgZ(95,"ul"),e.TgZ(96,"li"),e.TgZ(97,"a",32),e._uU(98,"Mentha"),e.qZA(),e.qZA(),e.TgZ(99,"li"),e.TgZ(100,"a",33),e._uU(101,"Gene Ontology"),e.qZA(),e.qZA(),e.TgZ(102,"li"),e.TgZ(103,"a",34),e._uU(104,"KEGG PATHWAY Database"),e.qZA(),e.qZA(),e.TgZ(105,"li"),e.TgZ(106,"a",35),e._uU(107,"Reactome"),e.qZA(),e.qZA(),e.TgZ(108,"li"),e.TgZ(109,"a",36),e._uU(110,"WikiPathways"),e.qZA(),e.qZA(),e.TgZ(111,"li"),e.TgZ(112,"a",37),e._uU(113,"HOMER"),e.qZA(),e.qZA(),e.qZA(),e.qZA(),e.TgZ(114,"div",31),e.TgZ(115,"h5"),e._uU(116,"Development Tools"),e.qZA(),e.TgZ(117,"ul"),e.TgZ(118,"li"),e.TgZ(119,"a",38),e._uU(120,"Angular"),e.qZA(),e.qZA(),e.TgZ(121,"li"),e.TgZ(122,"a",39),e._uU(123,"Cytoscape.js"),e.qZA(),e.qZA(),e.TgZ(124,"li"),e.TgZ(125,"a",40),e._uU(126,"d3.js"),e.qZA(),e.qZA(),e.TgZ(127,"li"),e.TgZ(128,"a",41),e._uU(129,"Bootstrap"),e.qZA(),e.qZA(),e.TgZ(130,"li"),e.TgZ(131,"a",42),e._uU(132,"Django"),e.qZA(),e.qZA(),e.TgZ(133,"li"),e.TgZ(134,"a",43),e._uU(135,"Scipy"),e.qZA(),e.qZA(),e.qZA(),e.qZA(),e.TgZ(136,"div",31),e.TgZ(137,"a",44),e._uU(138,"Data Privacy Statement"),e.qZA(),e.qZA(),e.qZA())},directives:[n.yS,n.rH,s],styles:[""]}),t})()}];let m=(()=>{class t{}return t.\u0275fac=function(i){return new(i||t)},t.\u0275mod=e.oAB({type:t}),t.\u0275inj=e.cJS({imports:[[n.Bz.forChild(Z)],n.Bz]}),t})(),u=(()=>{class t{}return t.\u0275fac=function(i){return new(i||t)},t.\u0275mod=e.oAB({type:t}),t.\u0275inj=e.cJS({imports:[[a.ez,l.m,m]]}),t})()}}]);