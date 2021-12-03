from xoroshiro import XOROSHIRO
class Filter:
    nature_list = ["Hardy","Lonely","Brave","Adamant","Naughty","Bold","Docile","Relaxed","Impish","Lax","Timid","Hasty","Serious","Jolly","Naive","Modest","Mild","Quiet","Bashful","Rash","Calm","Gentle","Sassy","Careful","Quirky"]
    shiny_list = ["Star","Square","Star/Square"]

    def __init__(self,iv_min=None,iv_max=None,abilities=None,shininess=None,slot_min=None,slot_max=None,natures=None,marks=None):
        self.iv_min = iv_min
        self.iv_max = iv_max
        self.abilities = abilities
        self.shininess = Filter.shiny_list.index(shininess) if shininess != None else None
        self.slot_min = slot_min
        self.slot_max = slot_max
        self.natures = [Filter.nature_list.index(nature) for nature in natures] if natures != None else None
        self.marks = marks
    
    def compare_ivs(self,state):
        if self.iv_min != None:
            for i in range(6):
                if not self.iv_min[i] <= state.ivs[i] <= self.iv_max[i]:
                    return False
        return True
    
    def compare_fixed(self,state):
        if self.shininess == 0 and state.xor == 0:
            return False
        return self.compare_ivs(state)
    
    def compare_slot(self,state):
        return self.slot_min <= state.slot_rand <= self.slot_max if self.slot_min != None else True
    
    def compare_mark(self,state):
        return state.mark in self.marks if self.marks != None else True
    
    def compare_shiny(self,shiny):
        return shiny if self.shininess != None else True
    
    def compare_ability(self,state):
        return state.ability in self.abilities if self.abilities != None else True
    
    def compare_nature(self,state):
        return state.nature in self.natures if self.natures != None else True
        

class OverworldState:
    natures = ["Hardy","Lonely","Brave","Adamant","Naughty","Bold","Docile","Relaxed","Impish","Lax","Timid","Hasty","Serious","Jolly","Naive","Modest","Mild","Quiet","Bashful","Rash","Calm","Gentle","Sassy","Careful","Quirky"]
    
    def __init__(self):
        self.advance = 0
        self.full_seed = 0
        self.fixed_seed = 0
        self.is_static = True
        self.mark = None
        self.brilliant_rand = 1000
        self.slot_rand = 100
        self.level = 0
        self.nature = 0
        self.ability = 0
        self.ec = 0
        self.pid = 0
        self.xor = 0
        self.ivs = [32]*6
        
    def __str__(self):
        if self.is_static:
            return f"{self.advance} {self.ec:08X} {self.pid:08X} {'No' if self.xor >= 16 else ('Square' if self.xor == 0 else 'Star')} {self.natures[self.nature]} {self.ability} {'/'.join(str(iv) for iv in self.ivs)} {self.mark}"
        else:
            return f"{self.advance} {self.level} {self.slot_rand} {self.ec:08X} {self.pid:08X} {'No' if self.xor >= 16 else ('Square' if self.xor == 0 else 'Star')} {self.natures[self.nature]} {self.ability} {'/'.join(str(iv) for iv in self.ivs)} {self.mark}"

class OverworldRNG:
    personality_marks = ["Rowdy","AbsentMinded","Jittery","Excited","Charismatic","Calmness","Intense","ZonedOut","Joyful","Angry","Smiley","Teary","Upbeat","Peeved","Intellectual","Ferocious","Crafty","Scowling","Kindly","Flustered","PumpedUp","ZeroEnergy","Prideful","Unsure","Humble","Thorny","Vigor","Slump"]
    
    def __init__(self,seed=0,tid=0,sid=0,shiny_charm=False,mark_charm=False,weather_active=False,is_fishing=False,is_static=False,is_legendary=False,is_shiny_locked=False,min_level=0,max_level=0,diff_held_item=False,filter=Filter(),double_mark_gen=False):
        self.rng = XOROSHIRO(seed & 0xFFFFFFFFFFFFFFFF, seed >> 64)
        self.advance = 0
        self.tid = tid
        self.sid = sid
        self.shiny_charm = shiny_charm
        self.mark_charm = mark_charm
        self.weather_active = weather_active
        self.is_fishing = is_fishing
        self.is_static = is_static
        self.is_legendary = is_legendary
        self.is_shiny_locked = is_shiny_locked
        self.double_mark_gen = double_mark_gen
        self.min_level = min_level
        self.max_level = max_level
        self.diff_held_item = diff_held_item
        self.filter = filter
    
    @property
    def tsv(self):
        return self.tid ^ self.sid
        
    def advance_fast(self,advances):
        self.advance += advances
        for _ in range(advances):
            self.rng.next()

    def generate(self):
        state = OverworldState()
        state.full_seed = self.rng.state()
        state.advance = self.advance
        state.is_static = self.is_static
        
        go = XOROSHIRO(*self.rng.seed.copy())
        if self.is_static:
            go.rand(100)
        else:
            if not self.is_fishing:
                go.rand()
            go.rand(100)
            go.rand(100)
            state.slot_rand = go.rand(100)
            if not self.filter.compare_slot(state):
                self.rng.next()
                self.advance += 1
                return
            if self.min_level != self.max_level:
                state.level = self.min_level + go.rand(self.max_level-self.min_level+1)
            else:
                state.level = self.min_level
            state.mark = OverworldRNG.rand_mark(go,self.weather_active,self.is_fishing,self.mark_charm)
            if not self.double_mark_gen and not self.filter.compare_mark(state):
                self.rng.next()
                self.advance += 1
                return
            state.brilliant_rand = go.rand(1000)
        
        if not self.is_shiny_locked:
            for roll in range(3 if self.shiny_charm else 1):
                mock_pid = go.nextuint()
                shiny = (((mock_pid >> 16) ^ (mock_pid & 0xFFFF)) ^ self.tsv) < 16
                if shiny:
                    break
        else:
            shiny = False
        if not self.filter.compare_shiny(shiny):
            self.rng.next()
            self.advance += 1
            return
        go.rand(2) 
        state.nature = go.rand(25)
        if not self.filter.compare_nature(state):
            self.rng.next()
            self.advance += 1
            return
        if not self.is_legendary:
            state.ability = 0 if go.rand(2) == 1 else 1
        else:
            state.ability = 0
        if not self.filter.compare_ability(state):
            self.rng.next()
            self.advance += 1
            return
        if self.diff_held_item:
            go.rand(100)
        state.fixed_seed = go.nextuint()
        
        state.ec, state.pid, state.ivs = OverworldRNG.calculate_fixed(state.fixed_seed,self.tsv,shiny,3 if self.is_legendary else 0)
        state.xor = (((state.pid >> 16) ^ (state.pid & 0xFFFF)) ^ self.tsv)
        if not self.filter.compare_fixed(state):
            self.rng.next()
            self.advance += 1
            return
        
        if self.is_static or self.double_mark_gen:
            state.mark = OverworldRNG.rand_mark(go,self.weather_active,self.is_fishing,self.mark_charm)
            if not self.filter.compare_mark(state):
                self.rng.next()
                self.advance += 1
                return
        
        self.rng.next()
        self.advance += 1
        return state
    
    @staticmethod
    def calculate_fixed(fixed_seed,tsv,shiny,forced_ivs):
        rng = XOROSHIRO(fixed_seed)
        ec = rng.nextuint()
        pid = rng.nextuint()
        if not shiny:
            if (((pid >> 16) ^ (pid & 0xFFFF)) ^ tsv) < 16:
                pid ^= 0x10000000
        else:
            if not (((pid >> 16) ^ (pid & 0xFFFF)) ^ tsv) < 16:
                pid = (((tsv ^ (pid & 0xFFFF)) << 16) | (pid & 0xFFFF)) & 0xFFFFFFFF

        ivs = [32]*6
        for i in range(forced_ivs):
            index = rng.rand(6)
            while ivs[index] != 32:
                index = rng.rand(6)
            ivs[index] = 31
        for i in range(6):
            if ivs[i] == 32:
                ivs[i] = rng.rand(32)

        return [ec,pid,ivs]
    
    @staticmethod
    def rand_mark(go,weather_active,is_fishing,mark_charm):
        for roll in range(3 if mark_charm else 1):
            rare_rand = go.rand(1000)
            personality_rand = go.rand(100)
            uncommon_rand = go.rand(50)
            weather_rand = go.rand(50)
            time_rand = go.rand(50)
            fish_rand = go.rand(25)
            
            if rare_rand == 0:
                return "Rare"
            if personality_rand == 0:
                return OverworldRNG.personality_marks[go.rand(len(OverworldRNG.personality_marks))]
            if uncommon_rand == 0:
                return "Uncommon"
            if weather_rand == 0:
                if weather_active:
                    return "Weather"
            if time_rand == 0:
                return "Time"
            if fish_rand == 0:
                if is_fishing:
                    return "Fishing"
