
all : main data widgets
DATADIR = ../data/

RESOURCES = images.qrc
RESOURCESPY = $(RESOURCES:.qrc=_rc.py)

data : $(RESOURCESPY)

widgets : force_look
	$(MAKE) -C widgets/ui

main : Main.py

%.py : %.ui
	pyuic4 $< -o $*.py
	sed -i 's/^import \([A-z]*\)_rc/import AniChou.gui.\1_rc/' $*.py

%_rc.py : $(DATADIR)%.qrc
	pyrcc4 $< -o $*_rc.py

force_look :

clean :
	rm -f Main.py Main.pyc $(RESOURCESPY) $(RESOURCESPY:.py=.pyc)
	$(MAKE) clean -C widgets/ui