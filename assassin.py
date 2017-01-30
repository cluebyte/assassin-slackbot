from random import shuffle
import datetime

class assassin_game:
    
    assassin_list = []
    survivor_list = []
    channel = ""
    
    def new_game(self, players, channel_id):
        self.assassin_list = []
        self.survivor_list = []
        self.channel = channel_id
        for name in players:
            new_player = player()
            new_player.name = name
            self.assassin_list.append(new_player)
            self.survivor_list.append(new_player)
        shuffle(self.survivor_list)
        f = open("assassin_chain.txt", "w")
        for a in self.survivor_list:
            f.write(a.name + "\n")
        f.close();
        
    def get_active_channel(self):
        return self.channel
        
    def is_player_alive(self, name):
        for player in self.survivor_list:
            if player.name == name:
                return True
        return False
        
    def get_players_target(self, name):
        for i, player in enumerate(self.survivor_list):
            if player.name == name:
                return self.survivor_list[(i+1)%len(self.survivor_list)].name
        return None
    
    def get_players_assassin(self, name):
        for i, player in enumerate(self.survivor_list):
            if player.name == name:
                return self.survivor_list[(i+len(self.survivor_list)-1)%len(self.survivor_list)].name
        return None
        
    def kill_player(self, name):
        for i, player in enumerate(self.survivor_list):
            if player.name == name:
                assassin = self.survivor_list[(i+len(self.survivor_list)-1)%len(self.survivor_list)]
                self.survivor_list.remove(player)
                assassin.killed_recently = True
                return True
        return False
    
    def kill_replace_player(self, name, newName):
        for i, player in enumerate(self.survivor_list):
            if player.name == name:
                player.name == newName
                player.killed_recently = True
                return True
        return False
    
    def remove_player(self, name):
        for player in self.survivor_list:
            if player.name == name:
                self.survivor_list.remove(player)
                return True
        return
    
    def expire_players(self):
        expired_players = []
        needs_new_target = []
        for i, player in enumerate(self.survivor_list):
            if not player.killed_recently:
                expired_players.append(player.name)
                assassin = self.survivor_list[(i+len(self.survivor_list)-1)%len(self.survivor_list)]
                if assassin.killed_recently:
                    needs_new_target.append(assassin.name)
        
        for name in expired_players:
            for player in self.survivor_list:
                if player.name == name:
                    self.survivor_list.remove(player)
                
        for player in self.survivor_list:
            player.killed_recently = False
            
        return (expired_players, needs_new_target)

    def is_ongoing_game(self):
        return len(self.survivor_list) > 1
        
    def get_remaining_players(self):
        name_list = [x.name for x in self.survivor_list]
        shuffle(name_list)
        return name_list
        
class player:
    name = ""
    killed_recently = False