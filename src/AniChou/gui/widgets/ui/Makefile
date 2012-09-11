
WGT = Ui_ACStatusTab.ui Ui_ACAboutDialog.ui Ui_ACTextDialog.ui

SCRIPTS = $(WGT:.ui=.py)

all : $(SCRIPTS)

%.py : %.ui
	pyuic4 $< -o $*.py
	sed -i 's/^import \([A-z]*\)_rc/import AniChou.gui.\1_rc/' $*.py

clean:
	rm -f $(SCRIPTS) $(SCRIPTS:.py=.pyc)