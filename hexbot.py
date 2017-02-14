import os
import time
import json

from assassin import assassin_game

from slackclient import SlackClient

BOT_ID = 'U3HBS30BS'
AT_BOT = "<@U3HBS30BS>"
TOKEN = "xoxb-119400102400-Hn1rAt5jkc8Ah29RmempFmAO"

slack_client = SlackClient(TOKEN)


        
class assassinbot:

    HELP_COMMAND = "help"
    NEW_GAME_COMMAND = "newgame"
    TARGET_COMMAND = "target"
    SURVIVORS_COMMAND = "survivors"
    REMOVE_COMMAND = "remove"
    KILL_COMMAND = "kill"
    EXPIRE_COMMAND = "expire"
    LOAD_LAST_GAME_COMMAND = "thomas_is_a_really_terrible_coder"
    

    game = assassin_game()
    
    def help(self):
        response = "Commands are:\n"
        response += "`@hexbot assassin help`\n"
        response += "`@hexbot assassin newgame` - I'll start a new game and whisper everyone their targets.\n"
        response += "`@hexbot assassin target` - I'll pm you your target\n"
        response += "`@hexbot assassin survivors` - see remaining players in current game\n"
        response += "`@hexbot assassin kill @player` - kill a player (I will pm their assassin)\n"
        response += "`@hexbot assassin expire` - expire all players who haven't gotten a kill since last expiration\n"
        response += "`@hexbot assassin remove @player` - remove a player without giving anyone a kill\n"
        response += "Ask Thomas for questions."
        return response
        
    def new_game(self, players, channel):
        #only allow games to be made in 'assassin' and 'bot_sandbox'
        if channel != "C3DHYM12S" and channel != "C3K4GSMFH": 
            return "Please only make a new game in the assassin channel"
        self.game.new_game(players, channel)
        for player in players:
            target = self.game.get_players_target(player)
            im_user(player, "Your target is <@" + target + ">")
        return "A new game has started!"
        
    def load_last_game(self,  channel):
        #only allow games to be made in 'assassin' and 'bot_sandbox'
        if channel != "C3DHYM12S" and channel != "C3K4GSMFH": 
            return "Please only make a load game in the assassin channel"
        self.game.load_last_game(channel)
        for player in self.game.get_remaining_players():
            target = self.game.get_players_target(player)
            im_user(player, "Your target is <@" + target + ">")
        return "I agree that he's a terrible coder. Please make sure your target hasn't changed."
        
    def target(self, user):
        if not self.game.is_ongoing_game():
            return "Game not ongoing"
        target = self.game.get_players_target(user)
        im_user(user, "Your target is <@" + target + ">")
        return ""
        
    def survivors(self):
        if not self.game.is_ongoing_game():
            return "Game not ongoing"
        survivors = self.game.get_remaining_players()
        response = "In a random order, the remaining players are:\n"
        for player in survivors:
            response += get_user(player)["name"] + "\n"
        return response
        
    def kill(self, killer, command):
        if not self.game.is_ongoing_game():
            return False, "Game not ongoing"
        if len(command) < 2:
            return False, "Please enter the player to kill"
        player = command[1][2:-1].upper()
        if not self.game.is_player_alive(player):
            return False, "<@" + player + "> was not found for some reason."
        if self.game.is_player_alive(killer):
            assassin = self.game.get_players_assassin(player)b
            target = self.game.get_players_target(player)
            if len(self.game.get_remaining_players()) == 2:
                return True, "<@" + player + "> was killed. <@" + assassin + "> won the game!"
            self.game.kill_player(player, killer)
            im_user(assassin, "Your target is <@" + target + ">")
            return True, "<@" + player + "> was killed."
        else:
            assassin = self.game.get_players_assassin(player)
            target = self.game.get_players_target(player)
            self.game.kill_replace_player(player, killer)
            im_user(assassin, "Your target is <@" + killer + ">")
            im_user(killer, "Your target is <@" + target + ">")
            return True, "<@" + player + "> was killed. <@" + killer + "> is back in the game!"
        
    def expire(self, channel):
        if not self.game.is_ongoing_game():
            return "Game not ongoing"
        if channel != self.game.get_active_channel(): 
            return "Please only expire players in the main channel"
        expired, needs_new = self.game.expire_players()
        survivors = self.game.get_remaining_players()
        if len(survivors) == 0:
            return "All players expired, the game ends in a draw. Yay."
        if len(survivors) == 1:
            return "<@" + survivors[0]  + "> won the game!. Everyone else expired."
        if len(expired) == 0:
            return "Nobody expired this time. Countdown timer reset"
        response = "The following players expired:\n"
        for player in expired:
            response += "<@" + player + ">" + "\n"
        for assassin in needs_new:
            target = self.game.get_players_target(assassin)
            im_user(assassin, "Your target is <@" + target + ">")
            
        return response
        
    def remove(self, command, channel):
        if not self.game.is_ongoing_game():
            return "Game not ongoing"
        if channel != self.game.get_active_channel(): 
            return "Please only expire players in the main channel"
        if len(command) < 2:
            return "Please enter the player to remove"
        player = command[1][2:-1].upper()
        if not self.game.is_player_alive(player):
            return "<@" + player + "> was not found for some reason."
        assassin = self.game.get_players_assassin(player)
        target = self.game.get_players_target(player)
        if len(self.game.get_remaining_players()) == 2:
            return "<@" + player + "> was removed. <@" + assassin + "> won the game!"
        self.game.remove_player(player)
        im_user(assassin, "Your target is <@" + target + ">")
        return "<@" + player + "> was removed."
        
        
    def handle_command(self, command, players, user, channel):
        """
            Receives commands directed at the bot and determines if they
            are valid commands. If so, then acts on the commands. If not,
            returns back what it needs for clarification.
        """
        response = self.help()
            
        if len(command) == 0:
            return response
        
        elif command[0] == self.NEW_GAME_COMMAND:
            return self.new_game(players, channel)
            
        elif command[0] == self.TARGET_COMMAND:
            return self.target(user)
            
        elif command[0] == self.SURVIVORS_COMMAND:
            return self.survivors()
            
        elif command[0] == self.EXPIRE_COMMAND:
            return self.expire(channel)
            
        elif command[0] == self.REMOVE_COMMAND:
            return self.remove(command, channel)
                
        elif command[0] == self.KILL_COMMAND:
            (success, response) = self.kill(user, command)
            if success and self.game.get_active_channel() != "" and channel != self.game.get_active_channel():
                post_to_channel(self.game.get_active_channel(), response)
                return ""
                
        elif command[0] == self.LOAD_LAST_GAME_COMMAND:
            return self.load_last_game(channel)
            
        return response
        
class hexbot:
    DEBUG_COMMAND = "debug"
    ASSASSIN_COMMAND = "assassin"
    HELP_COMMAND = "help"
    
    assassinbot = assassinbot()
    
    def assassin(self, command, channel_id, user_id):
        user_ids = []
        channel = get_channel(channel_id)
        if channel:
            user_ids = channel["members"]
            user_ids.remove(BOT_ID)
        return self.assassinbot.handle_command(command, user_ids, user_id, channel_id)
        
    def debug(self, command, channel_id):
        """
            Get debug information about the channel.
        """
        channel = get_channel(channel_id)
        if not channel:
            return "Failed to figure out channel: " + channel_id
        user_ids = channel["members"]
        response = "*```######DEBUG######```*\n"
        response = "Command: " + command + "\n\n"
        response += "*Channel*: " + json.dumps(channel, indent=4) + "\n\n"
        for user_id in user_ids:
            response += "*User*: " + json.dumps(get_user(user_id), indent=4) + "\n\n"
        return response
        
    def help(self):
        response = "Commands are:\n"
        response += "`@hexbot help`\n"
        response += "`@hexbot assassin` - Assassin game stuff\n"
        response += "`@hexbot debug` - Get debug information about the channel.\n"
        response += "Ask Thomas for questions."
        return response
        
    def handle_command(self, command, channel, user):
        """
            Receives commands directed at the bot and determines if they
            are valid commands. If so, then acts on the commands. If not,
            returns back what it needs for clarification.
        """
        response = "Hello. Type \"@hexbot help\" for more information"
        command = command.split()
        
        if len(command) == 0:
            return response
            
        if command[0] == self.HELP_COMMAND:
            response = self.help()
        elif command[0] == self.DEBUG_COMMAND:
            response = self.debug(command, channel);
        elif command[0] == self.ASSASSIN_COMMAND:
            command.pop(0)
            response = self.assassin(command, channel, user);
            
        return response

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and output['text'].startswith(AT_BOT):
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel'], output['user']
    return None, None, None

def get_user(user_id):
    """
        Get user info and return things of interest.
    """
    data = slack_client.api_call("users.info", user=user_id)
    if not data["ok"]:
        return False
    response = {}
    response["username"] = data["user"]["name"]
    response["name"] = data["user"]["profile"]["real_name_normalized"]
    response["user_id"] = data["user"]["id"]
    return response
    
def get_channel(channel_id):
    """
        Get channel info and return things of interest.
    """
    if channel_id[0] == 'C':
        type = "channel"
    elif channel_id[0] == 'G':
        type = "group"
    elif channel_id[0] == 'D':
        return False
    else:
        return False
    data = slack_client.api_call(type + "s.info", channel=channel_id)
    if not data["ok"]:
        return False
    response = {}
    response["name"] = data[type]["name"]
    response["members"] = data[type]["members"]
    response["channel_id"] = data[type]["id"]
    return response

def im_user(user_id, message):
    data = slack_client.api_call("im.open", user=user_id)
    channel_id = data["channel"]["id"]
    post_to_channel(channel_id, message)
                          
def post_to_channel(channel_id, message):
    print(channel_id, message)
    slack_client.api_call("chat.postMessage", channel=channel_id,
                          text=message, as_user=True)
        
if __name__ == "__main__":
    hexbot = hexbot()
    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print("HexBot connected and running!")
        while True:
            command, channel, user = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                try:
                    response = hexbot.handle_command(command, channel, user)
                    post_to_channel(channel, response)
                except:
                    post_to_channel(channel, "Something broke. But I'm still alive! `@hexbot assassin help` for help.")
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
