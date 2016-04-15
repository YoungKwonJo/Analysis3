
baseWeight = "weight*puweight*mueffweight*eleffweight"
mceventweight=[
{"name":"CEN",       "var": "("+baseWeight+")"},
{"name":"csvweight", "var": "("+baseWeight+"*csvweights[0])"},
{"name":"PW_Up",     "var": "(weight*puweightUp*lepweight*csvweights[0])"},
{"name":"PW_Down",   "var": "(weight*puweightDown*lepweight*csvweights[0])"},
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
{"name":"CQ_Err2_Down",    "var": "("+baseWeight+"*csvweights[18])"} 
]


