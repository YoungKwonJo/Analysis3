
baseWeight = "weight*puweight*mueffweight*eleffweight*tri"
baseWeightNOPU = "weight*mueffweight*eleffweight*tri"
mceventweight=[
{"name":"CEN",       "var": "("+baseWeight+")"},
{"name":"NoPU",       "var": "("+baseWeightNOPU+")"},
{"name":"csvweight", "var": "("+baseWeight+"*csvweights[0])"},
{"name":"PW_Up",     "var": "(weight*puweightUp*mueffweight*eleffweight*tri*csvweights[0])"},
{"name":"PW_Down",   "var": "(weight*puweightDown*mueffweight*eleffweight*tri*csvweights[0])"},
{"name":"JER_NOM",   "var": "("+baseWeight+"*csvweights[0])"},
{"name":"JER_Up",    "var": "("+baseWeight+"*csvweights[0])"},
{"name":"JER_Down",  "var": "("+baseWeight+"*csvweights[0])"},
{"name":"JES_Up",    "var": "("+baseWeight+"*csvweights[1])"},        
{"name":"JES_Down",  "var": "("+baseWeight+"*csvweights[2])"},      
{"name":"LF_Up",     "var": "("+baseWeight+"*csvweights[3])"},         
{"name":"LF_Down",   "var": "("+baseWeight+"*csvweights[4])"},       
#]
#=[
{"name":"HF_Up",           "var": "("+baseWeight+"*csvweights[5])"},           
{"name":"HF_Down",         "var": "("+baseWeight+"*csvweights[6])"},         
{"name":"HF_Stats1_Up",    "var": "("+baseWeight+"*csvweights[7])"},    
{"name":"HF_Stats1_Down",  "var": "("+baseWeight+"*csvweights[8])"},  
{"name":"HF_Stats2_Up",    "var": "("+baseWeight+"*csvweights[9])"},    
{"name":"HF_Stats2_Down",  "var": "("+baseWeight+"*csvweights[10])"},  
{"name":"LF_Stats1_Up",    "var": "("+baseWeight+"*csvweights[11])"},    
{"name":"LF_Stats1_Down",  "var": "("+baseWeight+"*csvweights[12])"},  
{"name":"LF_Stats2_Up",    "var": "("+baseWeight+"*csvweights[13])"},    
{"name":"LF_Stats2_Down",  "var": "("+baseWeight+"*csvweights[14])"},  
{"name":"CQ_Err1_Up",      "var": "("+baseWeight+"*csvweights[15])"},   
{"name":"CQ_Err1_Down",    "var": "("+baseWeight+"*csvweights[16])"}, 
{"name":"CQ_Err2_Up",      "var": "("+baseWeight+"*csvweights[17])"},   
{"name":"CQ_Err2_Down",    "var": "("+baseWeight+"*csvweights[18])"},
#]
#mceventweight=[
{"name":"Mu_Up",     "var": "(weight*puweight*mueffweight_up*eleffweight*tri*csvweights[0])"},
{"name":"Mu_Down",   "var": "(weight*puweight*mueffweight_dn*eleffweight*tri*csvweights[0])"},
{"name":"El_Up",     "var": "(weight*puweight*mueffweight*eleffweight_up*tri*csvweights[0])"},
{"name":"El_Down",   "var": "(weight*puweight*mueffweight*eleffweight_dn*tri*csvweights[0])"},
#
{"name":"Trig_Up",   "var": "(weight*puweight*mueffweight*eleffweight*tri_up*csvweights[0])"},
{"name":"Trig_Down",   "var": "(weight*puweight*mueffweight*eleffweight*tri_dn*csvweights[0])"}
]


mceventweightMG5 = [{'name':i['name'],'var':i['var'].replace("(weight*","(").replace('*weight*','*')} for i in mceventweight]

