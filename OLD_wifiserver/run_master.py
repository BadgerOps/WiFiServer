import master
'''
we can either pass in config options here, or using a cfg file...

'''
# cfg = {demo: 'cfg object1' another: 'cfg object 2'}
m = master.Master(cfg=None)
m.start()
