import typing

import services
from NeonOcean.Order import Debug, Director, Settings, SettingsShared, This
from NeonOcean.Order.Interactions.Support import Categories, Dependent, Events, Registration
from interactions.base import immediate_interaction
from objects import script_object
from sims4 import resources
from sims4.tuning import instance_manager

ModSettingInteractions = list()  # type: typing.List[typing.Type[ModSettingInteraction]]

class ModSettingInteraction(Dependent.DependentExtension, Events.EventsExtension, Registration.RegistrationExtension, immediate_interaction.ImmediateSuperInteraction):
	DependentMod = This.Mod

	def __init_subclass__ (cls, *args, **kwargs):
		try:
			super().__init_subclass__(*args, **kwargs)

			ModSettingInteractions.append(cls)
		except Exception as e:
			Debug.Log("Failed to initialize new sub class for '" + cls.__name__ + "'.", This.Mod.Namespace, Debug.LogLevels.Exception, group = This.Mod.Namespace, owner = __name__, exception = e)
			raise e

class _Announcer(Director.Controller):
	Host = This.Mod

	@classmethod
	def OnInstanceManagerLoaded (cls, instanceManager: instance_manager.InstanceManager):
		if instanceManager.TYPE != resources.Types.OBJECT:
			return

		modSettingCategory = services.get_instance_manager(resources.Types.PIE_MENU_CATEGORY).get(Categories.OrderModSettingsID)  # type: script_object.ScriptObject

		for setting in Settings.GetAllSettings():  # type: SettingsShared.SettingBase
			if setting.DialogType == SettingsShared.DialogTypes.NoDialog:
				continue

			settingInteraction = ModSettingInteraction.generate_tuned_type(This.Mod.Namespace + ".Interactions.ModSetting." + setting.Key)  # type: typing.Type[ModSettingInteraction]

			settingInteraction.display_name = setting.Name.GetCallableLocalizationString()
			settingInteraction.category = modSettingCategory

			# noinspection SpellCheckingInspection
			settingInteraction._saveable = None

			settingInteraction.OnStarted = CreateOnStartedMethod(setting)

			Registration.RegisterAllObjectsInteraction(settingInteraction)

def CreateOnStartedMethod (setting: SettingsShared.SettingBase):
	# noinspection PyUnusedLocal
	def OnStarted (self) -> None:
		setting.ShowDialog()

	return OnStarted
