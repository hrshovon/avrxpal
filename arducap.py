file_str="<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<programmers>"	
with open('boards.txt') as file_handler:
	for line in file_handler:
		parpos=line.find('.name')
		if parpos>=0:
			name_board=line[parpos+6:line.rfind('\n')]
		parpos=line.find('.upload.protocol')
		if parpos>=0:
			name_protocol=line[parpos+17:line.rfind('\n')]
		parpos=line.find('.upload.speed')
		if parpos>=0:
			upload_speed=line[parpos+14:line.rfind('\n')]
		parpos=line.find('.build.mcu')
		if parpos>=0:
			mcu=line[parpos+11:line.rfind('\n')]
			file_str=file_str+"<dev type=\"arduino\">\n"
			file_str=file_str+"<name>"+name_board+"</name>\n"
			file_str=file_str+"<mcu>"+mcu+"</mcu>\n"
			file_str=file_str+"<interface>serial</interface>\n"
			file_str=file_str+'<protocol>'+name_protocol+'</protocol>\n'
			file_str=file_str+'<speed>'+upload_speed+'</speed>\n'
			file_str=file_str+'</dev>\n'
file_str=file_str+"</programmers>"
file_handler=open("programmer_boards.xml","w")
file_handler.write(file_str)
file_handler.close()
			
			
			
    
