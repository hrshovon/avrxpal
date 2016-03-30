import common_func
global_filepath='signature_data.txt'
selected_programmer='usbasp'
def find_mcu(signature_sent):
        signature=signature_sent.replace(" ","")
        print signature,len(signature)
	f_handle=open(global_filepath,'r')
	for line in f_handle:
		c=str(formatstr(line[line.find(',')+1:].lower()))
		print c
		if c.find(signature)>=0:
                        print line,c
                        f_handle.close()
			return line[0:line.find(',')]
	return "NaN"
def formatstr(a):
	b=a[0:4]+a[7:9]+a[12:]
	return b
def get_mcu(cmd):
	tmp=common_func.run_command_capture(cmd)
	if tmp.find('err')==0:
		return tmp
	linearr=tmp.split('\n')
	for line in linearr:
		linemod=line.replace(' ','')
		#print linemod
		a=linemod.find('avrdude:Devicesignature=')
		if(a>=0):
                        print linemod[24:]       
			return find_mcu(linemod[24:32])
	return tmp
	
	
