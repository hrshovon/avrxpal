from xml.etree import ElementTree
def get_arduino_list():
	list_arduino=[]
	xmlparserobj=ElementTree.parse("programmer_boards.xml")
	xmlroot=xmlparserobj.getroot()
	for node in xmlroot.findall("dev"):
		type_board=node.get("type")
		name_board=node.find("name").text
		if type_board=="arduino":
			list_arduino.append(name_board)
	return list_arduino
def get_chipname(board_name):
	xmlparserobj=ElementTree.parse("programmer_boards.xml")
	xmlroot=xmlparserobj.getroot()
	for node in xmlroot.findall("dev"):
		type_board=node.get("type")
		name_board=node.find("name").text
		if type_board=="arduino":
			if name_board==board_name:
				print "ok"
				return node.find("mcu").text
				
def get_baudrate(board_name):
	xmlparserobj=ElementTree.parse("programmer_boards.xml")
	xmlroot=xmlparserobj.getroot()
	for node in xmlroot.findall("dev"):
		type_board=node.get("type")
		name_board=node.find("name").text
		if type_board=="arduino":
			if name_board==board_name:
				print "ok"
				return node.find("speed").text





