
WGT =   Ui_ACAboutDialog.ui Ui_ACTextDialog.ui Ui_ACPreferencesDialog.ui\
	Ui_ACServiceTab.ui Ui_ACSimpleInputWidget.ui Ui_ACComboBoxWidget.ui

SCRIPTS = $(WGT:.ui=.py)

all : $(SCRIPTS)

%.py : %.ui
	pyuic4 $< -o $*.py
	sed -i 's/^import \([A-z]*\)_rc/import AniChou.gui.\1_rc/' $*.py

clean:
	rm -f $(SCRIPTS) $(SCRIPTS:.py=.pyc)
