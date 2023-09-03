#jay maa shaarde
#Developed by TinToSer https://github.com/tintoser
from lxml import etree
import io
import os

def repare(g):        
        d=g.split(" ")
        for i,ts in enumerate( d):
            if "name=" in ts:
                d[i]="name=\"master:const\""
            elif "defn=" in ts:
                d[i]="defn=\"master:const\""
            elif "w=" in ts:
                d[i]="w=\"69\""
            elif "h=" in ts:
                d[i]="h=\"19\""
            elif "z=" in ts:
                d[i]="z=\"-1\""
		
        return  " ".join(d)
	    

def sanitzer(trgtm,trgtd,srcf,tarf):

    k=open(srcf)
    tk=open(tarf,"w+")
        
    cnt=0
    def idchkr(g):
        for isds in trgtm:
            if "id=\"%s\"" % isds in g:
                    return 1
        for isds in trgtd:
            if "id=\"%s\"" % isds in g:
                    return 2         
        return 0

    g=k.readline()
    ss=1
    ssi=1
    hj="@TinToSer"
    while g:
        srfr=idchkr(g)
        if srfr==0 and ss==1:
                tk.write(g)
        elif srfr==1:
                hj=g.split("<")[0]+"</User>"+"\n"
                dat=repare(g)
                tk.write(dat)
                ss=0
                ssi=1
        elif srfr==2:
                hj=g.split("<")[0]+"</User>"+"\n"
                ss=0
                ssi=2
        elif hj != g and ss==0:
                
                if ssi==2:
                   pass
                elif ssi==1:
                   
                   if "name=\"Value\"" in g or "name=\"Name\"" in g :
                       tk.write(g)
                   elif "<paramlist link=\"-1\"" in g:
                       d=g.split(" ")
                       d[-1]="crc=\"8647988\">\n"
                       g=" ".join(d)
                       tk.write(g)
                   elif "</paramlist>" in g:
                       tk.write(g)    
                   else:
                       pass    
        elif  hj == g and ss==0:
                if ssi==2:
                   pass
                elif ssi==1:
                   tk.write(g)     
                ss=1
                
                
        g=k.readline()

    tk.close()
    k.close()

def magic(srcf,tarnm,tarf):
        familmem={}
        trgtm=[]
        trgtd=[]
        tree=etree.parse(srcf)
        r=tree.getroot()
        targ=[]
        namespc=r.get("name")
        parnm=None
        tbrm=["master:var","master:var_button","master:var_switch","master:var_pot"]
        
        reqvl=["Name","Value"]
        def fltr(nmme):
                if nmme != None:  
                    if ":" in nmme:
                         return nmme.split(":")[1]
                else:
                         return nmme
        for nebr in r.iter("hierarchy"):
                  for nebri in nebr.iter("call"):        
                     chldnm=fltr(nebri.attrib['name'])
                     parn=nebri.getparent()
                     
                     if len(parn.attrib) == 0:
                         familmem[chldnm]=[chldnm]
                         continue
                     parnm=fltr(parn.attrib['name'])
                     if not chldnm in familmem:
                             
                             familmem[chldnm]=[chldnm]    #[fltr(parnm.get('name')))]
                             
                     if parnm in familmem:
                         
                             familmem[parnm].append(chldnm)
                            
        for nebr in r.iter("definitions"):
                  for nebri in nebr.iter("Definition"):
                     if len(nebri.attrib)== 0:
                         continue
                     elif nebri.get('name') in familmem[tarnm]:
                         for nebrii in nebri.iter("schematic"):
                             for nebru in nebrii.iter("User"):
                                if nebru.get('classid')=="UserCmp" and nebru.get('defn') in tbrm:
                                    trgtm.append(nebru.get('id'))
                                    
                                    for nebrun in nebru.iter("param"):
                                        tmpchld=nebrun.get("name")
                                        if tmpchld not in reqvl:
                                            parnmhl=nebrun.getparent()
                                elif nebru.get('classid')=="UserCmp" and nebru.get('defn')=="master:pgb":
                                    trgtd.append(nebru.get('id'))

        sanitzer(trgtm,trgtd,srcf,tarf)       



