import bluetooth

print("performing inquiry...")

while True:
	nearby_devices = bluetooth.discover_devices(
	        duration=8, lookup_names=True, flush_cache=True)

	print("found %d devices" % len(nearby_devices))

	for addr, name in nearby_devices:
		print("  %s - %s" % (addr, name.encode('utf-8', 'replace')))
