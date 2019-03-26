import os
import typing
from json import decoder

from Mod_NeonOcean_Order import Paths

class Mod:
	def __init__ (self, informationDictionary: typing.Dict[str, typing.Any]):
		self.Namespace = informationDictionary["Namespace"]  # type: str
		self.Version = self.GetModVersion()  # type: str

		self.GithubName = informationDictionary["Github Name"]  # type: str

		self.Packages = list()  # type: typing.List[Package]

		for packageInformation in informationDictionary["Packages"]:  # type: typing.Dict[str, str]
			self.Packages.append(Package(Paths.RootPath, Paths.BuildPath, packageInformation["File Name"], packageInformation["Merge Root"]))  # type: str

		self.DistributionInstallerFilePath = os.path.join(Paths.PublishingDistributionInstallerPath, informationDictionary["Publishing"]["Installer File Name"])  # type: str
		self.DistributionInstallerFilePath = self.DistributionInstallerFilePath.format(self.Version)

		self.DistributionFilesFilePath = os.path.join(Paths.PublishingDistributionFilesPath, informationDictionary["Publishing"]["Files File Name"])  # type: str
		self.DistributionFilesFilePath = self.DistributionFilesFilePath.format(self.Version)

		self.SourcesFileName = informationDictionary["Publishing"]["Sources File Name"]  # type: str
		self.SourcesFileName = self.SourcesFileName.format(self.Version)

		self.PythonBuildArchiveFileName = informationDictionary["Python"]["Archive File Name"]  # type: str
		self.PythonBuildArchiveFilePath = os.path.join(Paths.PythonBuildArchivePath, self.PythonBuildArchiveFileName)  # type: str
		self.PythonSourcePath = os.path.join(Paths.PythonPath, self.Namespace)  # type: str
		self.PythonSourceRootPath = os.path.normpath(os.path.join(self.PythonSourcePath, informationDictionary["Python"]["Source Root"]))
		self.PythonSourceTargetPath = os.path.normpath(os.path.join(self.PythonSourcePath, informationDictionary["Python"]["Source Target"]))
		self.PythonSourceExcludedFiles = informationDictionary["Python"]["Source Excluded"]  # type: typing.List[str]
		self.PythonMergeRoot = os.path.join(Paths.BuildPath, informationDictionary["Python"]["Merge Root"])  # type: str

		for pythonExcludedFileIndex in range(0, len(self.PythonSourceExcludedFiles)):  # type: int
			self.PythonSourceExcludedFiles[pythonExcludedFileIndex] = os.path.normpath(os.path.join(self.PythonSourceTargetPath, self.PythonSourceExcludedFiles[pythonExcludedFileIndex]))

		self.UninstallPath = os.path.join(Paths.S4ModsPath, informationDictionary["Uninstall"])  # type: str

	def GetModVersion (self) -> str:
		with open(os.path.join(Paths.LoosePath, self.Namespace, "NeonOcean-Mod.json")) as informationFile:
			informationDictionary = decoder.JSONDecoder().decode(informationFile.read())  # type: typing.Dict[str, typing.Any]

		if not "Version" in informationDictionary:
			raise ValueError("Entry 'Version' does not exist.")

		version = informationDictionary["Version"]

		if not isinstance(version, str):
			raise TypeError("Entry 'Version' is not a string.")

		return version

class Package:
	def __init__ (self, modPath: str, modBuildPath: str, fileName: str, mergeRoot: str):
		self.Name = os.path.splitext(fileName)[0]  # type: str
		self.FileName = fileName  # type: str

		self.PackagePath = os.path.join(modPath, "Packages", self.Name)  # type: str
		self.BuildPath = os.path.join(self.PackagePath, "Build")  # type: str
		self.BuildFilePath = os.path.join(self.BuildPath, self.FileName)  # type: str
		self.BuildManifestFilePath = os.path.join(self.BuildPath, self.Name + "_Manifest.json")  # type: str
		self.MergeRoot = os.path.join(modBuildPath, mergeRoot)  # type: str
		self.SourcePath = os.path.join(self.PackagePath, self.Name)  # type: str
		self.SourceLoosePath = os.path.join(self.SourcePath, "Loose")  # type: str
		self.SourceBaseFilePath = os.path.join(self.SourcePath, "Base", self.FileName)  # type: str

		self.STBLPath = os.path.join(modPath, "STBL", self.Name)  # type: str
		self.STBLBuildPath = os.path.join(self.STBLPath, "Build")  # type: str
		self.STBLSourcePath = os.path.join(self.STBLPath, self.Name)  # type: str

def GetCurrentMod () -> Mod:
	return _mod

def GetVersion () -> str:
	return GetCurrentMod().Version

def GetGithubName () -> str:
	return GetCurrentMod().GithubName

def GetInstallerFilePath () -> str:
	return GetCurrentMod().DistributionInstallerFilePath

def GetFilesFilePath () -> str:
	return GetCurrentMod().DistributionFilesFilePath

def GetSourcesFileName () -> str:
	return GetCurrentMod().SourcesFileName

def _Setup () -> None:
	global _mod

	informationFilePath = os.path.join(os.path.dirname(os.path.dirname(os.path.normpath(__file__))), "Mod.json")  # type: str

	try:
		with open(os.path.join(informationFilePath)) as informationFile:
			_mod = Mod(decoder.JSONDecoder().decode(informationFile.read()))
	except Exception as e:
		raise Exception("Failed to read mod information for '" + informationFilePath + "'. \n") from e

_mod = None  # type: Mod

_Setup()
