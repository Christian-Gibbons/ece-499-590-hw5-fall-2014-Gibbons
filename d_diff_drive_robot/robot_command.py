from robot_checksum import robotChecksum
#def robotChecksum(commandPacket):
#	checksum = 0
#	length = commandPacket[3]
#	for i in range (2, 3+length):
#		checksum += commandPacket[i]
#	checksum = ~checksum
#	checksum = checksum & 0xFF
#	commandPacket[3+length] = checksum
#	return commandPacket

def createCommandPacket(ID, length, instruction, parameters):
	commandPacket = [0xFF, 0xFF, ID, length, instruction] + parameters + [0]
	commandPacket = robotChecksum(commandPacket)
#	print commandPacket
	return commandPacket

#commandPacket = createCommandPacket(1, 4, 3, [8, 6])
#print commandPacket
