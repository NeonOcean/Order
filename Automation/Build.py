
if __name__ == "__main__":
	import os
	import sys
	from importlib import util
		
	sys.path.append(os.path.join(os.path.dirname(__file__), "NeonOcean.Order"))
	Main = util.find_spec("Site_NeonOcean_Order.Main").loader.load_module()
		
	Main.BuildMod("Quick")