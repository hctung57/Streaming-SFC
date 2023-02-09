import time
import os

# NOTE: 
# - Assume: no removing files.

class DirMonitor: 
    def __init__(self,dir_home,pre,post,handler=lambda x:print(x),delay=0.3) -> None:
        self._dir_home=dir_home
        self._pre=pre
        self._post=post 
        self._handler=handler
        self._delay=delay
        self._pre_file_list=[]
       
    def listen(self):
        ind=0
        pre_mtime=0
        cnt=0
        mtime_stats=[]
        while True: 
            #True(cnt)
            cnt+=1
            file=f"{self._pre}{ind}.{self._post}"
            file_path=os.path.join(self._dir_home,file)
            exists=os.path.exists(file_path) # TODO: optimize
            
            if not exists or not os.path.getsize(file_path) > 0:
                continue
            
            mtime=os.path.getmtime(file_path)
            if mtime > pre_mtime:
            	pre_mtime=mtime
            	cnt=0
            	
            if not cnt%10 and cnt and pre_mtime==mtime:
            	cnt=0
            	print(f"[START PROCESS]: {self._pre}{ind}.{self._post}")
            	ind+=1
            	print(f"[PENDING]: {self._pre}{ind}.{self._post}")
            	file_path=os.path.join(self._dir_home,file)
            	self._handler(file_path)
            time.sleep(self._delay)
           
     
