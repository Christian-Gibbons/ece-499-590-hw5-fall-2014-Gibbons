def multiplyVelocity(params, factor):
	concat = hex((params[1]<<8) | (params[0]))[2:]
	bytes = int(concat, 16)
	direction = bytes & 0x0400
	if(factor < 0.0):
		direction ^= 0x0400
		factor *= -1.0
	magnitude = bytes & 0x03FF
	#magnitude *= mult
	#magnitude /= div
	magnitude = float(magnitude) * factor
	magnitude = int(magnitude) & 0x03FF
	velocity = direction | magnitude
	ret = []
	ret.append(velocity & 0xFF)
	ret.append((velocity >> 8) & 0xFF)
	return ret

