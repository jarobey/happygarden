from happygarden.discover import finder

finder = finder()
count = finder.reload_arp_report()
print('Found {0} devices'.format(count))
for device in finder.devices:
    print(device)
