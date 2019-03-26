import os
import shutil
from distutils import dir_util

from Mod_NeonOcean_Order import Mod, Paths
from Mod_NeonOcean_Order.Tools import IO, Merging

def Merge () -> None:
	IO.ClearDirectory(Paths.BuildPath)

	_MergeLoose()
	_MergePython()
	_MergePackage()

	_BuildManifest()

def _MergeLoose () -> None:
	if os.path.exists(Paths.LoosePath):
		dir_util.copy_tree(Paths.LoosePath, Paths.BuildPath)

def _MergePython () -> None:
	if os.path.exists(Mod.GetCurrentMod().PythonBuildArchiveFilePath):
		shutil.copy(Mod.GetCurrentMod().PythonBuildArchiveFilePath, Mod.GetCurrentMod().PythonMergeRoot)

def _MergePackage () -> None:
	for package in Mod.GetCurrentMod().Packages:  # type: Mod.Package
		if os.path.exists(package.BuildFilePath):
			shutil.copy(package.BuildFilePath, package.MergeRoot)

def _BuildManifest () -> None:
	Merging.BuildManifest(os.path.join(Mod.GetCurrentMod().Namespace, "Files.txt"), Paths.BuildPath)
