+ MAYAVERSION:2019 PLATFORM:win64 NemoMayaNodes 1 ./
plug-ins: plug-ins/windows-2019
scripts: ./
MAYA_CUSTOM_TEMPLATE_PATH+:= ui_templates
NEMO_MODULES:= modules
PYTHONPATH+:= lib/windows-2019
PYTHONPATH+:= extern

+ MAYAVERSION:2022 PLATFORM:win64 NemoMayaNodes 1 ./
plug-ins: plug-ins/windows-2022
scripts: ./
MAYA_CUSTOM_TEMPLATE_PATH+:= ui_templates
NEMO_MODULES:= modules
PYTHONPATH+:= lib/windows-2022
PYTHONPATH+:= extern

+ MAYAVERSION:2019 PLATFORM:linux NemoMayaNodes 1 ./
plug-ins: plug-ins/centos7-2019
scripts: ./
MAYA_CUSTOM_TEMPLATE_PATH+:= ui_templates
NEMO_MODULES:= modules
PYTHONPATH+:= lib/centos7-2019
PYTHONPATH+:= extern
