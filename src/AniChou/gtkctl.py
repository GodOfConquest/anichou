# Copyright (c) 2008 Gareth Latty
# Copyright (c) 2009 Sebastian Bartos
# See COPYING for details

"""
This module contains the GTK+ GUI subsystem of AniChou. It sets up the
user interface and enters the main event loop.

MODULE GLOBALS
==============
They are not nice, but the best in this situation. This file has two globals
defined in the gtkctl class constructor:

 - MODCTL: pointer to the gtkctl class instance.
 - WIDGETS: pointer to the widgets wrapper.
"""

import os, gtk, gtk.glade, gobject, webbrowser, datetime
from AniChou import settings, players, recognizinig
from AniChou.services.data.base import ( LOCAL_STATUS,
        LOCAL_STATUS_DICT, LOCAL_STATUS_R, LOCAL_STATUS_TABS )


def sb_push(msg):
    WIDGETS['bottom_statusbar'].push(-1, msg)

def sb_clear():
    """
    Clear the status bar.

    This is a callback for glib.timeout_add which is executed until it returns
    False, the first time after the interval specified.
    """
    # Not necessary to sleep here, in fact that would lock up the GUI.
    WIDGETS['bottom_statusbar'].pop(-1)
    try:
        WIDGETS['bottom_statusbar'].pop(-1)
    except:
        pass
    return False

class glade_handlers(object):
    """
    We put all of our glade gtk signal handlers into this class.
    This lets us bind all of them at once, because their names are in the class
    dict. If you want to know where these signals are assigned, then take a look
    at the data/ui.glade file (glade XML).
    """

    def gtk_main_quit(event):
        gtk.main_quit()

    def on_button_ac_clicked(event):
        webbrowser.open('https://github.com/SirAnthony/ac', 2)

    def on_button_mal_clicked(event):
        webbrowser.open('http://myanimelist.net', 2)

    def on_button_sync_clicked(event):
        sb_push('Syncing with current server..')
        gtk.main_iteration()
        for name in MODCTL.manager.sync():
            WIDGETS['bottom_statusbar'].pop(-1)
            if not name:
                sb_push('Sync failed..')
            else:
                sb_push('Syncing with {0}..'.format(name))
        MODCTL.update_from_db_all()
        sb_push('Syncing done..')
        # Clear the status bar in five seconds.
        gobject.timeout_add(5000, sb_clear)

    def on_playbar_toggled(event):
        if not INIT:
            if WIDGETS['statusbar_now_playing'].flags() & gtk.VISIBLE:
                WIDGETS['statusbar_now_playing'].hide()
            else:
                WIDGETS['statusbar_now_playing'].show()

    def on_about(event):
        WIDGETS['aboutdialog'].show_all()

    def on_about_close(widget, event):
        WIDGETS['aboutdialog'].hide_all()
        return True

    def on_menuitem_prefs_activate(event):
        WIDGETS['preferences'].show_all()

    def on_prefs_close(widget=None, event=None):
        WIDGETS['preferences'].hide_all()

        new_name = WIDGETS['entry_maluser'].get_text()
        new_pw = WIDGETS['entry_malpasswd'].get_text()
        new_path = WIDGETS['entry_searchdir'].get_text()

        MODCTL.cfg.mal['username'] = new_name
        MODCTL.cfg.mal['password'] = new_pw
        MODCTL.cfg.search_dir['dir1'] = new_path
        MODCTL.cfg.save()
        MODCTL.manager.updateConfig()
        return True

    def sync_on_start_toggled(event):
        if not INIT:
            old = MODCTL.cfg.startup.get('sync', True)
            new = not old
            MODCTL.cfg.startup['sync'] = new
            WIDGETS['sync_on_start'].set_active(new)
            MODCTL.cfg.save()

    def tracker_on_start_toggled(event):
        if not INIT:
            old = MODCTL.cfg.startup.get('tracker', True)
            new = not old
            MODCTL.cfg.startup['tracker'] =  new
            WIDGETS['playtracker_on_start'].set_active(new)
            MODCTL.cfg.save()

class widget_wrapper(object):
    """
    Load and set up the glade user interface and connect the signal hanlers.
    Provide a convenient way to access the glade widgets.
    """

    def __init__(self):
        """ Load user interface and connect signal handlers. """
        self.widgets = \
                gtk.glade.XML(
                os.path.join(settings.PACKAGE_PATH, 'data', 'ui.glade'))
        self.widgets.signal_autoconnect(glade_handlers.__dict__)

    def __getitem__(self, key):
        """ Make widgets accessable by name.

        It's simply done by overriding the aquisiton default of the class. Makes
        referencing widgets by name much more convinient:

        EXAMPLE
        =======
        To reference a widget by name (based on the glade file) and perform a
        GTK action with it you use:

           widgets['widget_name'].action()
        """
        return self.widgets.get_widget(key)


class list_treeview(gtk.TreeView):
    """ This is one of the two more interesting classes in the GUI subsystem.

    It is used to create and control the anime list treeview's (the big table in
    the middle that shows anime enries). It also handles manual editing on the
    table via callbacks, which are called when an episode, status or score entry
    is edited (slow double click on one of these enries).
    """

    def __init__(self, tab_id):
        """ Initialize the treeview.

        Call the parent constructor, store some references, define some class
        constants, add columns to the treeview and glue this together.

        The exciting part is the clomuns schemata setup, which tells the columns
        how they look like and what they should do when edited (connect
        callbacks).

        ARGUMENTS
        =========
        - tab_id: Schema based (LOCAL_STATUS) tab id

        PROPERTIES
        ==========
        - liststore: probably the most interseting property, as it stores the
          data of the table. It can be accessed by index, like
          liststore[row][column], both starting with 0.
        - col: reference to the tree view columns the class has. Not really
          interesting outside init, but may come in handy for plugin
          development.
        """

        # Call parrent constructor
        gtk.TreeView.__init__(self)

        # Mal tab type id
        self.tab_id = tab_id
        self.data = {}
        # This one is used to keep the db keys addresseble with the row indices
        self.keylist = list()

        # Some treeview specific constants (column id's)
        ( self.NAME, self.EPISODE, self.STATUS, self.SCORE, self.PROGRESS ) = \
                range (5)

        # Add columns to self and store references by name
        self.col = dict()
        for colname in ['Title', 'Episodes', 'Status', 'Score', 'Progress']:
            self.col[colname] = gtk.TreeViewColumn(colname)
            self.append_column(self.col[colname])


        ## Set up the column schemata

        # Title column schema
        titlecell = gtk.CellRendererText()
        self.col['Title'].pack_start(titlecell, True)
        self.col['Title'].add_attribute(titlecell, 'text', 0)

        # Episode column schema
        # Editable spin column that is connected with a callback
        epcell = gtk.CellRendererSpin()
        epcell.set_property("editable", True)
        adjustment = gtk.Adjustment(0, 0, 999, 1)
        epcell.set_property("adjustment", adjustment)
        epcell.connect('edited', self.cell_episode_edited)
        self.col['Episodes'].pack_start(epcell, False)
        self.col['Episodes'].add_attribute(epcell, 'text', 1)

        # Status column schema
        # Combo box column with selectable status
        # The first part contains the choices
        combomodel = gtk.ListStore(str)
        for i, item in LOCAL_STATUS:
            combomodel.append([item])

        statuscell = gtk.CellRendererCombo()
        statuscell.set_property('model', combomodel)
        statuscell.set_property('has-entry', False)
        statuscell.set_property('editable', True)
        statuscell.set_property('text-column', 0)
        statuscell.connect('edited', self.cell_status_edited)
        self.col['Status'].pack_start(statuscell, False)
        self.col['Status'].add_attribute(statuscell, 'text', 2)

        # Score column schema
        # Basically the same as the episodes one.
        scorecell = gtk.CellRendererSpin()
        scorecell.set_property("editable", True)
        adjustment = gtk.Adjustment(0, 0, 10, 1)
        scorecell.set_property("adjustment", adjustment)
        scorecell.connect('edited', self.cell_score_edited)
        self.col['Score'].pack_start(scorecell, False)
        self.col['Score'].add_attribute(scorecell, 'text', 3)

        # Progress column schema
        # Progress bar, nothing fancy
        progresscell = gtk.CellRendererProgress()
        self.col['Progress'].pack_start(progresscell, True)
        self.col['Progress'].add_attribute(progresscell, 'value', 4)


        ## Create liststore model (table containing the treeview data) and hook
        # it up to the treeview (self).
        self.liststore = gtk.ListStore(str, str, str, int, int)
        self.set_model(self.liststore)


    def repopulate(self):
        """ Resets/Initializes data to liststore (data table)
        INPUT
        =====
        - self.tv_data: the update is performed with this data
        """

        # clear previous data
        self.liststore.clear()

        # comupte and add new data based on self.data
        for key, anime in self.data.items():

            # Extract series title
            name = anime['title']
            name = name.replace('&apos;', '\'')

            # Extract episodes/max and construct display string
            if anime['episodes']:
                max_episodes = anime['episodes']
            else:
                max_episodes = '-'
            current_episode = anime['status_episodes']
            epstr = str(current_episode) + ' / ' + str(max_episodes)

            # Calculate progress bar
            progress = 0
            if isinstance(max_episodes, int):
                try:
                    progress = \
                        int(float(current_episode) / float(max_episodes) * 100)
                except:
                    progress = 0

            # Extract score
            score = anime['status_score']

            # Construct row list and add it to the liststore
            row = [name, epstr, LOCAL_STATUS_DICT.get(self.tab_id), score, progress]
            self.liststore.append(row)

            # Store key in row position
            self.keylist.append(key)


    def cell_score_edited(self, spinr, row, value):
        """ Handles editing / change of score cells.

        Not too much here, only database update.
        """
        maxvalue = 10
        if int(value) <= maxvalue and \
                int(value) != self.liststore[row][self.SCORE]:
            self.liststore[row][self.SCORE] = int(value)
            self.push_change_to_db(row, {'status_score': int(value)})


    def cell_status_edited(self, combr, row, value):
        """ Handles selection of status combo cells.

        Pushes the entry in other categories and eventually updates the episode
        number (from non-complete to complete -> maximize status_episodes)
        """
        # We don't move to self?
        if value != self.liststore[row][self.STATUS]:
            # Prepare data
            maxepisodes = self.liststore[row][self.EPISODE].split(' / ')[1]
            self.liststore[row][self.STATUS] = value
            if value == LOCAL_STATUS_DICT.get(LOCAL_STATUS_R['completed']):
                # We move to the comleted tab?
                self.liststore[row][self.PROGRESS] = 100
                self.liststore[row][self.EPISODE] = \
                        maxepisodes + ' / ' + maxepisodes
                #FIXME:
                self.push_change_to_db(row, {
                        'status_episodes': int(maxepisodes),
                        'status_status': LOCAL_STATUS_R['completed'] })
            else:
                # we move to another tab?
                self.push_change_to_db(row, {
                        'status_status': LOCAL_STATUS_R[value] })
            # Move row
            MODCTL.tv[LOCAL_STATUS_R[value]].liststore.append(
                    self.liststore[row])
            del self.liststore[row]



    def cell_episode_edited(self, spinr, row, value):
        """ Handles the modification of the episode number spin button.

        If all a valid new value is entered, the row is updated and parrent
        update function is called to update the local database.

        If maximal episode is entered as new value, the enry is pushed to the
        completed table.

        If entry is in the completed table and the ep count is lowered, it is
        pushed in the watching table.
        """

        # Prepare data set
        oldstr = self.liststore[row][self.EPISODE].replace('-','0')
        (old, max) = oldstr.split(' / ')
        oldvalue = int(old)
        maxvalue = int(max)
        newvalue = int(value)

        # Determine if action is required
        if newvalue != oldvalue and \
                (newvalue <= maxvalue or maxvalue == 0):
            # Compute new common row data
            newstr = str(newvalue) + ' / ' + str(maxvalue)
            self.liststore[row][self.EPISODE] = newstr
            self.liststore[row][self.PROGRESS] = \
                    int(float(newvalue) / float(maxvalue) * 100)
            # Stuff to be done with smaller than max ep count
            COMPLETED = LOCAL_STATUS_R['completed']
            if newvalue < maxvalue:
                # In the completd table
                if self.tab_id == COMPLETED:
                    WATCHING = LOCAL_STATUS_R['watching']
                    self.push_change_to_db(row,
                            {'status_episodes': newvalue,
                             'status_status': WATCHING })
                    self.liststore[row][self.STATUS] = \
                            LOCAL_STATUS_DICT[WATCHING]
                    MODCTL.tv[WATCHING].liststore.append(
                            self.liststore[row])
                    del self.liststore[row]
                # In all other tables that are not complete
                else:
                    self.push_change_to_db(row,
                            {'status_episodes': newvalue})
            # Did we reach treashhold and was not completed?
            if self.tab_id != COMPLETED and newvalue == maxvalue:
                # Send to compted
                self.push_change_to_db(row,
                        {'status_episodes': newvalue,
                         'status_status': COMPLETED})
                self.liststore[row][self.STATUS] = \
                        LOCAL_STATUS_DICT[COMPLETED]
                MODCTL.tv[COMPLETED].liststore.append(
                        self.liststore[row])
                del self.liststore[row]


    def push_change_to_db(self, row, changes):
        """ Shorthand for pusing changes to the anime database

        It's called from the treeview callbacks to commit a local change to the
        local anime database.

        ARGUMENTS
        =========
        - row: the row we are in, which is used to look up the keyname we want
               to change
        - changes: dict with changes that have to be done
        """
        # set new values in database
        for key, value in changes.items():
            MODCTL.manager.db[self.keylist[int(row)]][key] = value

        # set update timestamp
        MODCTL.manager.db[self.keylist[int(row)]]\
                ['status_updated'] = datetime.datetime.now()

        # save changes in local database
        MODCTL.manager.save()


class guictl(object):
    """ GUI control interface class.

    This class starts up and controls the general user interface. Simply
    initialize it with a config and manager reference pointer and a shiny GTK
    GUI will pop up in the middle of your screen (if all goes well).
    """

    def __init__(self, manager, config):
        """
        Load interface and enter main loop.

        ARGUMENTS
        =========
        - config: reference to BaseConfig instance
        - manager: reference to manager instance
        """

        global INIT
        INIT = True

        # Hook to make the conrol module reachable from all over the
        # file, especially from the autoconnect handlers.
        global MODCTL
        MODCTL = self

        # Store the references to the config and data instances
        self.cfg = config
        self.manager = manager

        # Initialize base widgets from XML and connect signal handlers
        # Set widget hook
        global WIDGETS
        WIDGETS = widget_wrapper()

        # Initialize treeviews
        self.tv = dict()
        for tab_id, name in LOCAL_STATUS_TABS:
            tv = list_treeview(tab_id)
            self.tv[tab_id] = tv
            WIDGETS['scrolledwindow_' + name].add(tv)

        # Check if we need to sync, and sync
        sb_push('Syncing..')
        if self.cfg.get('startup', 'sync'):
            for name in self.manager.sync():
                sb_push(u'Syncing witn {0}..'.format(name))
                WIDGETS['bottom_statusbar'].pop(-1)
            # Clear the status bar in five seconds.
            gobject.timeout_add(5000, sb_clear)

        self.update_from_db_all()

        # Set preferences dialog from config
        WIDGETS['entry_maluser'].set_text(
                self.cfg.mal.get('username', ''))
        WIDGETS['entry_malpasswd'].set_text(
                self.cfg.mal.get('password', ''))
        WIDGETS['sync_on_start'].set_active(
                self.cfg.startup.get('sync'))
        WIDGETS['playtracker_on_start'].set_active(
                self.cfg.startup.get('tracker'))

        WIDGETS['entry_searchdir'].set_text(self.cfg.search_dir.get('dir1'))

        ## Show main window, connect the quit signal handler and hide the
        # now_playing statusbar
        WIDGETS['main_window'].show_all()
        WIDGETS['main_window'].connect('delete_event', lambda e,w:
                gtk.main_quit())
        if not self.cfg.startup.get('tracker'):
            WIDGETS['statusbar_now_playing'].hide()
        else:
            WIDGETS['menuitem_playbar'].set_active(True)


        gobject.timeout_add(500, self.idle_cb)

        INIT = False

        # Run main loop
        gtk.main()


    def idle_cb(self):
        if WIDGETS['statusbar_now_playing'].flags() & gtk.VISIBLE:
            track = players.get_playing(
                ['mplayer', 'totem'], [self.cfg.search_dir.get('dir1')])
            for key in track.keys():
                e = recognizinig.engine(key, self.manager.db)
                m = e.match()
                try:
                    ep = int(e._getEpisode().strip('/'))
                    if m:
                        #print m, ep
                        if self.manager.db[m]['status_episodes'] == \
                                ep - 1 and \
                                self.manager.db[m]['status_status'] == \
                                data.WATCHING:
                            msg = u'Playing: {0} -- Episode: {1}'.format(m, ep)
                            WIDGETS['statusbar_now_playing'].push(-1, msg)
                            if ep < self.manager.db[m]['episodes']:
                                self.manager.db[m]['status_episodes'] = ep
                                MODCTL.manager.db[m]\
                                        ['status_updated'] = datetime.datetime.now()
                                MODCTL.manager.save()
                                newep = str(ep) + ' / ' + str(self.manager.db[m]['episodes'])

                                sw = self.tv[1].keylist
                                i = 0 # row tracker
                                for key in sw:
                                    if key == m:
                                        break
                                    else:
                                        i += 1

                                self.tv[1].liststore[str(i)][1] = newep
                except:
                    break
        return True


    def update_from_db_all(self):
        """ Update all anime tables views from database.

        This is used on initialization and after syncronization.
        """

        # We copy (references to) data from manager.db into
        # list_treeview.tb and from there into liststore.
        # Might be better to give manager a facade to act
        # as TreeModel.

        # Remove old data
        for tab in self.tv.values():
            tab.data = {}

        # Just changing self.tv[].data is not enough, as after deletion on
        # the site a sync will remove keys from manager.db and we have
        # to mirror that.

        # Separate anime data according to their status
        for key, value in self.manager.db.items():
            status = value['status_status']

            self.tv[status].data[key] = value

        # Populate tree views
        for tab in self.tv.values():
            tab.repopulate()
