#
# PowerAdmin Plugin for BigBrotherBot(B3) (www.bigbrotherbot.com)
# Copyright (C) 2005 www.xlr8or.com
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# Changelog:
# 1.4.0 : Initial push (after download from spacepig)
#

__version__ = '1.4.0'
__author__  = 'xlr8or'

import b3, re
import b3.events

#--------------------------------------------------------------------------------------------------
class PoweradminPlugin(b3.plugin.Plugin):
  _adminPlugin = None

  def startup(self):
    """\
    Initialize plugin settings
    """

    # get the admin plugin so we can register commands
    self._adminPlugin = self.console.getPlugin('admin')
    if not self._adminPlugin:
      # something is wrong, can't start without admin plugin
      self.error('Could not find admin plugin')
      return False
    
    # register our commands
    if 'commands' in self.config.sections():
      for cmd in self.config.options('commands'):
        level = self.config.get('commands', cmd)
        sp = cmd.split('-')
        alias = None
        if len(sp) == 2:
          cmd, alias = sp

        func = self.getCmd(cmd)
        if func:
          self._adminPlugin.registerCommand(self, cmd, level, func, alias)

    self.debug('Started')


  def getCmd(self, cmd):
    cmd = 'cmd_%s' % cmd
    if hasattr(self, cmd):
      func = getattr(self, cmd)
      return func

    return None


  def onEvent(self, event):
    """\
    Handle intercepted events
    """


#--Commands implementation ------------------------------------------------------------------------

  def cmd_paexec(self, data, client, cmd=None):
    """\
    <configfile.cfg> - Execute a server configfile.
    (You must use the command exactly as it is! )
    """
    if not data:
      client.message('^7Invalid or missing data, try !help paexec')
      return False
    else:
      if re.match('^[a-z0-9_.]+.cfg$', data, re.I):
        self.debug('Executing configfile = [%s]', data)
        self.console.write('exec %s' % data)
      else:
        self.error('%s is not a valid configfile', data)

    return True


  def cmd_pamaprestart(self, data, client, cmd=None):
    """\
    Restart the current map.
    (You can safely use the command without the 'pa' at the beginning)
    """
    self.console.write('map_restart')
    return True


  def cmd_paset(self, data, client, cmd=None):
    """\
    <cvar> <value> - Set a server cvar to a certain value.
    (You must use the command exactly as it is! )
    """
    if not data:
      client.message('^7Invalid or missing data, try !help paset')
      return False
    else:
      # are we still here? Let's write it to console
      input = data.split(' ',1)
      cvarName = input[0]
      value = input[1]
      self.console.setCvar( cvarName, value )

    return True


  def cmd_paget(self, data, client, cmd=None):
    """\
    <cvar> - Returns the value of a servercvar.
    (You must use the command exactly as it is! )
    """
    if not data:
      client.message('^7Invalid or missing data, try !help paget')
      return False
    else:
      # are we still here? Let's write it to console
      getcvar = data.split(' ')
      getcvarvalue = self.console.getCvar( '%s' % getcvar[0] )
      cmd.sayLoudOrPM(client, '%s' % getcvarvalue)

    return True


  def cmd_pasaybold(self, data, client, cmd=None):
    """\
    <message> - Print a Bold message on the center of all screens.
    (You can safely use the command without the 'pa' at the beginning)
    """
    if not data:
      client.message('^7Invalid or missing data, try !help pasaybold')
      return False
    else:
      # are we still here? Let's write it to console
      self.console.setCvar( 'b3_saybold','%s' % data )

    return True


  def cmd_paendmap(self, data, client, cmd=None):
    """\
    End the current map gracefully.
    (You can safely use the command without the 'pa' at the beginning)
    """
    #Simply set the b3_endmap dvar to 1 and the mod will do the rest
    self.console.setCvar( 'b3_endmap','1' )

    return True


  def cmd_pashock(self, data, client, cmd=None):
    """\
    <player> [<duration>] - Shock a player. 
    (You can safely use the command without the 'pa' at the beginning)
    """
    # this will split the player name and the message
    input = self._adminPlugin.parseUserCmd(data)
    if input:
      # input[0] is the player id
      sclient = self._adminPlugin.findClientPrompt(input[0], client)
      if not sclient:
        # a player matchin the name was not found, a list of closest matches will be displayed
        # we can exit here and the user will retry with a more specific player
        return False
    else:
      client.message('^7Invalid data, try !help pashock')
      return False

    if re.match('^([0-9]+)\s*$', input[1]):
      duration = int(input[1])
    else:
      client.message('^7Using 7 seconds timespan.')
      duration = 7
    #else:
    #  duration = int(duration)
    if duration > 60:
      client.message('^7Using 60 seconds timespan.')
      duration = 60
    sclient.message('^3You\'re shocked for ^7%s ^3seconds' % duration)


    # are we still here? Let's write it to console
    self.console.setCvar( 'b3_shocktime','%s' % duration )
    self.console.setCvar( 'b3_shock','%s' % sclient.cid )

    return True


  def cmd_paburn(self, data, client, cmd=None):
    """\
    <player> [<reason>] - Set a player on fire and kill him. 
    (You can safely use the command without the 'pa' at the beginning)
    """
    # this will split the player name and the message
    input = self._adminPlugin.parseUserCmd(data)
    if input:
      # input[0] is the player id
      sclient = self._adminPlugin.findClientPrompt(input[0], client)
      if not sclient:
        # a player matchin the name was not found, a list of closest matches will be displayed
        # we can exit here and the user will retry with a more specific player
        return False
    else:
      client.message('^7Invalid data, try !help switch')
      return False

    if len(input) > 1:
      sclient.message('^3You are being burned: ^7%s' % (input[1]))

    # are we still here? Let's execute the kill
    self.console.setCvar( 'b3_burn','%s' % sclient.cid )

    return True


  def cmd_paexplode(self, data, client, cmd=None):
    """\
    <player> [<reason>] - Blow the player up. 
    (You can safely use the command without the 'pa' at the beginning)
    """
    # this will split the player name and the message
    input = self._adminPlugin.parseUserCmd(data)
    if input:
      # input[0] is the player id
      sclient = self._adminPlugin.findClientPrompt(input[0], client)
      if not sclient:
        # a player matchin the name was not found, a list of closest matches will be displayed
        # we can exit here and the user will retry with a more specific player
        return False
    else:
      client.message('^7Invalid data, try !help switch')
      return False

    if len(input) > 1:
      sclient.message('^3You are being killed: ^7%s' % (input[1]))

    # are we still here? Let's execute the kill
    self.console.setCvar( 'b3_explode','%s' % sclient.cid )

    return True


  def cmd_parename(self, data, client, cmd=None):
    """\
    <player> <newname> - Force a clients Name
    (You can safely use the command without the 'pa' at the beginning)
    """
    # this will split the player name and the message
    input = self._adminPlugin.parseUserCmd(data)
    if input:
      # input[0] is the player id
      sclient = self._adminPlugin.findClientPrompt(input[0], client)
      if not sclient:
        # a player matchin the name was not found, a list of closest matches will be displayed
        # we can exit here and the user will retry with a more specific player
        return False
    else:
      client.message('^7Invalid data, try !help rename')
      return False

    if len(input) > 1:
      sclient.message('^3Your name is forced to: ^7%s' % (input[1]))
    else:
      client.message('^7Invalid or missing data, try !help rename')
      return False

    # are we still here? Let's write it to console
    self.console.setCvar( 'b3_rname','%s' % input[1] )
    self.console.setCvar( 'b3_rcid','%s' % sclient.cid )

    return True


  def cmd_palosepoint(self, data, client, cmd=None):
    """\
    <player> [<reason>] - Make the player loose a scorepoint. 
    (You can safely use the command without the 'pa' at the beginning)
    """
    # this will split the player name and the message
    input = self._adminPlugin.parseUserCmd(data)
    if input:
      # input[0] is the player id
      sclient = self._adminPlugin.findClientPrompt(input[0], client)
      if not sclient:
        # a player matchin the name was not found, a list of closest matches will be displayed
        # we can exit here and the user will retry with a more specific player
        return False
    else:
      client.message('^7Invalid data, try !help switch')
      return False

    if len(input) > 1:
      sclient.message('^3You lost a point: ^7%s' % (input[1]))

    # are we still here? Let's execute
    self.console.setCvar( 'b3_losepoint','%s' % sclient.cid )

    return True


  def cmd_pacompensate(self, data, client, cmd=None):
    """\
    <player> [<reason>] - Compensate the player. Score +1 and Deaths -1 
    (You can safely use the command without the 'pa' at the beginning)
    """
    # this will split the player name and the message
    input = self._adminPlugin.parseUserCmd(data)
    if input:
      # input[0] is the player id
      sclient = self._adminPlugin.findClientPrompt(input[0], client)
      if not sclient:
        # a player matchin the name was not found, a list of closest matches will be displayed
        # we can exit here and the user will retry with a more specific player
        return False
    else:
      client.message('^7Invalid data, try !help switch')
      return False

    if len(input) > 1:
      sclient.message('^3You were compensated: ^7%s' % (input[1]))

    # are we still here? Let's execute
    self.console.setCvar( 'b3_compensate','%s' % sclient.cid )

    return True


  def cmd_pascore(self, data, client, cmd=None):
    """\
    <player> <number> - Alter a clients score (ie. 5 or -3)
    (You can safely use the command without the 'pa' at the beginning)
    """
    # this will split the player name and the message
    input = self._adminPlugin.parseUserCmd(data)
    if input:
      # input[0] is the player id
      sclient = self._adminPlugin.findClientPrompt(input[0], client)
      if not sclient:
        # a player matchin the name was not found, a list of closest matches will be displayed
        # we can exit here and the user will retry with a more specific player
        return False
    else:
      client.message('^7Invalid data, try !help pascore')
      return False

    if not len(input[1]):
      client.message('^7Missing data, try !help pascore')
      return False

    if re.match('^[+-]?([0-9]+)\s*$', input[1], re.I):
      score = int(input[1])
    else:
      client.message('^7Invalid data, try !help pascore')
      return False

    if score == 0:
      return False

    # are we still here? Let's write it to console
    self.console.setCvar( 'b3_score','%s' % input[1] )
    self.console.setCvar( 'b3_scorecid','%s' % sclient.cid )

    return True


  def cmd_padeath(self, data, client, cmd=None):
    """\
    <player> <number> - Alter a clients deathcount (ie. 5 or -3)
    (You can safely use the command without the 'pa' at the beginning)
    """
    # this will split the player name and the message
    input = self._adminPlugin.parseUserCmd(data)
    if input:
      # input[0] is the player id
      sclient = self._adminPlugin.findClientPrompt(input[0], client)
      if not sclient:
        # a player matchin the name was not found, a list of closest matches will be displayed
        # we can exit here and the user will retry with a more specific player
        return False
    else:
      client.message('^7Invalid data, try !help padeath')
      return False

    if not len(input[1]):
      client.message('^7Missing data, try !help padeath')
      return False

    if re.match('^[+-]?([0-9]+)\s*$', input[1], re.I):
      score = int(input[1])
    else:
      client.message('^7Invalid data, try !help padeath')
      return False

    if score == 0:
      return False

    # are we still here? Let's write it to console
    self.console.setCvar( 'b3_death','%s' % input[1] )
    self.console.setCvar( 'b3_deathcid','%s' % sclient.cid )

    return True


  def cmd_paforce(self, data, client, cmd=None):
    """\
    <player> <allies/axis/spectator> - Force a client to allies/axis/spec
    (You can safely use the command without the 'pa' at the beginning)
    """
    # this will split the player name and the message
    input = self._adminPlugin.parseUserCmd(data)
    if input:
      # input[0] is the player id
      sclient = self._adminPlugin.findClientPrompt(input[0], client)
      if not sclient:
        # a player matchin the name was not found, a list of closest matches will be displayed
        # we can exit here and the user will retry with a more specific player
        return False
    else:
      client.message('^7Invalid data, try !help paforce')
      return False

    if not len(input[1]):
      client.message('^7Missing data, try !help paforce')
      return False

    team = input[1]
    
    if team == 'spec':
      team = 'spectator'
    
    if team in ('allies','axis','spectator'):
      sclient.message('^3Your are forced to: ^7%s' % (team))
    else:
      client.message('^7Invalid or missing data, try !help paforce')
      return False

    # in case we mistype the forcespec command or some fancy multiuseagestuff
    if team == 'spectator':
      self.console.setCvar( 'g_switchspec','%s' % sclient.cid )
      return False

    # are we still here? Let's write it to console
    self.console.setCvar( 'b3_forceteamname','%s' % team )
    self.console.setCvar( 'b3_forceteamcid','%s' % sclient.cid )

    return True


  def cmd_paenforce(self, data, client, cmd=None):
    """\
    <player> <cvarname> <value> - Force a clients Cvar/Dvar! Be Carefull! Very Powerfull!
    (You can safely the command without the 'pa' at the beginning)
    """
    # this will split the player name and the message
    input = self._adminPlugin.parseUserCmd(data)
    if input:
      # input[0] is the player id
      sclient = self._adminPlugin.findClientPrompt(input[0], client)
      if not sclient:
        # a player matchin the name was not found, a list of closest matches will be displayed
        # we can exit here and the user will retry with a more specific player
        return False
    else:
      client.message('^7Invalid data, try !help enforce')
      return False

    cvarinfo = input[1].split()
    
    if (len(cvarinfo[0]) and len(cvarinfo[1])):
      sclient.message('^3Your setting: ^7%s ^3is forced to: ^7%s' % (cvarinfo[0], cvarinfo[1]))
    else:
      client.message('^7Invalid or missing data, try !help enforce')
      return False

    # are we still here? Let's write it to console
    self.console.setCvar( 'b3_ccvar','%s' % cvarinfo[0] )
    self.console.setCvar( 'b3_cvalue','%s' % cvarinfo[1] )
    self.console.setCvar( 'b3_ccid','%s' % sclient.cid )

    return True
    
    
  def cmd_paretaliate(self, data, client, cmd=None):
    """\
    <player> [<reason>] - Will make the game unplayable for the client. Be Carefull! Very Nasty!
    (You can safely the command without the 'pa' at the beginning)
    """
    # this will split the player name and the message
    input = self._adminPlugin.parseUserCmd(data)
    if input:
      # input[0] is the player id
      sclient = self._adminPlugin.findClientPrompt(input[0], client)
      if not sclient:
        # a player matchin the name was not found, a list of closest matches will be displayed
        # we can exit here and the user will retry with a more specific player
        return False
    else:
      client.message('^7Invalid data, try !help switch')
      return False

    if len(input) > 1:
      sclient.message('^3Admin Retaliation: ^7%s' % (input[1]))

    # are we still here? Let's execute the retaliation
    self.console.setCvar( 'b3_r2cid','%s' % sclient.cid )

    return True


#--Original Code below by Ravir / Bulletworm ------------------------------------------------------

  def cmd_paswitch(self, data, client, cmd=None):
    """\
    <name> - Force a player to the other team.
    (You can safely use the command without the 'pa' at the beginning)
    """
    # this will split the player name and the message
    input = self._adminPlugin.parseUserCmd(data)
    if input:
      # input[0] is the player id
      sclient = self._adminPlugin.findClientPrompt(input[0], client)
      if not sclient:
        # a player matchin the name was not found, a list of closest matches will be displayed
        # we can exit here and the user will retry with a more specific player
        return False
    else:
      client.message('^7Invalid data, try !help switch')
      return False

    if len(input) > 1:
      sclient.message('^3You are being switched: ^7%s' % (input[1]))

    # are we still here? Let's execute the switch
    self.console.setCvar( 'g_switchteam','%s' % sclient.cid )

    return True


  def cmd_paswitchall(self, data, client, cmd=None):
    """\
    Force all players to switch teams.
    (You can safely use the command without the 'pa' at the beginning)
    """
    # Setting it to -1 is same as setting it to all... all was not an option in the orig Ravir code.
    self.console.setCvar( 'g_switchteam','-1' )

    return True


  def cmd_paforcespec(self, data, client, cmd=None):
    """\
    <player> [<reason>] - Switch a player to spectator
    (You can safely use the command without the 'pa' at the beginning)
    """
    # this will split the player name and the message
    input = self._adminPlugin.parseUserCmd(data)
    if input:
      # input[0] is the player id
      sclient = self._adminPlugin.findClientPrompt(input[0], client)
      if not sclient:
        # a player matchin the name was not found, a list of closest matches will be displayed
        # we can exit here and the user will retry with a more specific player
        return False
    else:
      client.message('^7Invalid data, try !help switch')
      return False

    if len(input) > 1:
      sclient.message('^3You are being forced to spectator: ^7%s' % (input[1]))

    # are we still here? Let's execute the switch
    self.console.setCvar( 'g_switchspec','%s' % sclient.cid )

    return True


  def cmd_paforceallspec(self, data, client, cmd=None):
    """\
    Force all players to switch teams.
    (You can safely use the command without the 'pa' at the beginning)
    """
    # Setting it to -1 is same as setting it to all... all was not an option in the orig Ravir code.
    self.console.setCvar( 'g_switchspec','-1' )

    return True


  def cmd_pakillplayer(self, data, client, cmd=None):
    """\
    <player> - Kill a player on the spot
    (You can safely use the command without the 'pa' at the beginning)
    """
    # this will split the player name and the message
    input = self._adminPlugin.parseUserCmd(data)
    if input:
      # input[0] is the player id
      sclient = self._adminPlugin.findClientPrompt(input[0], client)
      if not sclient:
        # a player matchin the name was not found, a list of closest matches will be displayed
        # we can exit here and the user will retry with a more specific player
        return False
    else:
      client.message('^7Invalid data, try !help switch')
      return False

    if len(input) > 1:
      sclient.message('^3You are being killed: ^7%s' % (input[1]))

    # are we still here? Let's execute the kill
    self.console.setCvar( 'g_killplayer','%s' % sclient.cid )

    return True
