'''Info Header Start
Name : extTdpBrowser
Author : WielandHilkerPlusPlu@AzureAD
Saveorigin : Project.toe
Saveversion : 2025.33070
Info Header End'''

from importlib.metadata import distributions, packages_distributions, files
from importlib import import_module
from touchutilcollection.extensions import EnsureExtension, parfield, partypes
import json
from pathlib import Path
import td
from types import ModuleType


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

				package_files = self.load_package_files( lookup.get( package.name, [] ) )
				if not package_files: continue
					
				self.package_table.appendRow([
					package.name, 
					package.version, 
					json.dumps( list( lookup[ package.name ] )),
					json.dumps( package_files ),
					package.metadata["Description"]
				])
	
	def load_package_files(self, module_names):
		files = set()
		for module_name in module_names:

			imported_module = import_module( module_name )
			match getattr( imported_module, "TDP_SPEC_VERSION", 1 ):
				case 1:
					for submodule_name in dir( imported_module ):
						item = getattr( imported_module, submodule_name )
						if ( hasattr(td, submodule_name) or 
							(not hasattr(item, "__name__")) or 
							(not isinstance( getattr( item, "ToxFile", None), Path))): continue
						
						files.add((
							module_name, 
							item.__name__.split(".")[-1],
							item.__name__, 
							str(item.ToxFile.relative_to(project.folder)),
							"Tox",
							"ToxFile"
						))

				case 2:
					#TDP V2 
					submodules = getattr( imported_module, "Modules", tuple())
					# we have to do some assumptions as (Submodule) and (Submodule,) are different....
					for submodule in (submodules,) if isinstance( submodules, ModuleType) else submodules:
						filepath = getattr( submodule, "File", None)
						if not isinstance(filepath,  Path ): continue
						files.add((
							module_name, 
							submodule.__name__.split(".")[-1],
							submodule.__name__, 
							str(filepath.relative_to(project.folder)),
							getattr(submodule, "Style", "Tox"),
							"File"
						))

		return list(files)
		



	def Place(self, module_path, style, attr_name):
		print("Foobar")
		debug( module_path, style, attr_name )
		if ui.panes.current.type != PaneType.NETWORKEDITOR: return
		current_active_comp:COMP = ui.panes.current.owner

		if style == "Tox":
			new_tox = current_active_comp.loadTox( getattr( import_module( module_path ), attr_name ) )
			new_tox.par.externaltox.expr = f"mod.{module_path}.{attr_name}"
			new_tox.par.enableexternaltox.val = True
			new_tox.par.enableexternaltoxpulse.pulse()
			ui.panes.current.placeOPs([ new_tox ])
		else:
			raise NotImplemented(f"{style} nopt yet supported")