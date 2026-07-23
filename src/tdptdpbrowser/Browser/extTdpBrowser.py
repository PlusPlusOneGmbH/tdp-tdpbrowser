'''Info Header Start
Name : extTdpBrowser
Author : WielandHilkerPlusPlu@AzureAD
Saveorigin : Project.toe
Saveversion : 2025.32460
Info Header End'''

from importlib.metadata import distributions, packages_distributions, files
from importlib import import_module
from touchutilcollection.extensions import EnsureExtension, parfield, partypes
import json


class extTdpBrowser(EnsureExtension):
	"""
	extTdpBrowser description
	"""

	class par:
		Searchviaprefix = parfield( partypes.ParToggle, default= True, label="Search with Prefix", help = "Includes all packages that start with tdp-")
		Searchviakeyword = parfield( partypes.ParToggle, default= True, label="Search with Keyword", help = "Includes all packages that include TouchDesignerPackage in their keywords.")

	def __init__(self, ownerComp:containerCOMP):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		super().__init__( ownerComp )
		self.package_table = self.ownerComp.opex("installed_packages").asType(tableDAT)

		self.Update()


	def Update(self):
		self.package_table.clear()
		self.package_table.appendRow(["name", "version", "modules", "toxfiles", "readme"])
		lookup = {}
		for modulename, package_references in packages_distributions().items():
			for package_reference in package_references:
				lookup.setdefault( package_reference, set()).add( modulename )

		for package in distributions():
			if ( self.par.Searchviaprefix.eval() and package.name.startswith("tdp-") 
	   			or 
				self.par.Searchviakeyword.eval() and "TouchDesignerPackage" in package.metadata.get("keywords", [])):
				package_files = self.load_package_toxfiles( lookup.get( package.name, [] ) )
				if not package_files: continue
		
					

				self.package_table.appendRow([
					package.name, 
					package.version, 
					json.dumps( list( lookup[ package.name ] )),
					json.dumps( package_files ),
					package.metadata["Description"]
				])
	
	def load_package_toxfiles(self, module_names):
		tox_files = set()
		for module_name in module_names:
			for name, path in getattr(import_module( module_name ) , "_ToxFiles", {}).items():
				tox_files.add((module_name, name, str(path.relative_to(project.folder))))
				#tox_files.add({
				#	"module" : module_name, 
				#	"tox_name" : name, 
				#	"path" : str(path.relative_to(project.folder))
				#}
				#)

		return list(tox_files)
		
		
	def Place(self, module_name, tox_name):
		
		if ui.panes.current.type != PaneType.NETWORKEDITOR: return
		current_active_comp:COMP = ui.panes.current.owner
		
		new_tox = current_active_comp.loadTox( getattr( import_module( module_name ), tox_name).ToxFile )
		new_tox.par.externaltox.expr = f"mod.{module_name}.{tox_name}.ToxFile"
		new_tox.par.enableexternaltox.val = True
		new_tox.par.enableexternaltoxpulse.pulse()
		ui.panes.current.placeOPs([ new_tox ])
