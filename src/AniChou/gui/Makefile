
all : data widgets main
DATADIR = ../data/

RESOURCES = images.qrc

data : $(RESOURCES:.qrc=.py)

widgets : force_look
	$(MAKE) -C widgets/ui

main : Main.py

%.py : %.ui
	pyuic4 $< -o $*.py

%.py : $(DATADIR)%.qrc
	pyrcc4 $< -o $*_rc.py

force_look :
