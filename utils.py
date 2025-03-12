import pandas as pd
import json
import collections, functools, operator
import skill_boosts

class monster_hunter_weapon:
    def __init__(self, name, loaded_slots = None):
        with open('data/ig_crafted_weapon_data.json', 'r') as file:
            crafted_weapon_db = json.load(file)
        with open('data/ig_artian_weapon_data.json', 'r') as file:
            artian_weapon_db = json.load(file)

        weapon_db = {**crafted_weapon_db, **artian_weapon_db}
        self.name = name
        self.raw = weapon_db[name]['raw']
        self.element = weapon_db[name]['element']
        self.element_value = weapon_db[name]['element_value']
        self.affinity = weapon_db[name]['affinity']
        self.defense = weapon_db[name]['defense']
        self.skills = weapon_db[name]['skills']
        self.kinsect_level = weapon_db[name]['kinsect_level']
        self.base_sharpness = weapon_db[name]['base_sharpness']
        self.base_sharpness_value = weapon_db[name]['base_sharpness_value']
        self.handicraft_sharpness = weapon_db[name]['handicraft_sharpness']
        self.handicraft_sharpness_value = weapon_db[name]['handicraft_sharpness_value']
        if loaded_slots:
            self.slots = loaded_slots
        else:
            self.slots = weapon_db[name]['slots']

    def count_slots(self):
        counter = 0
        for slot in self.slots:
            if self.slots[slot]['Size'] > 0:
                counter += 1
        return counter

    def set_decoration(self, deco_name, slot = None, verbose = False):
        #get deco from json database
        if deco_name == None:
            return
        with open('data/decoration_data.json', 'r') as file:
            deco_db = json.load(file)
        try:
            deco_object = deco_db[deco_name]
        except:
            raise Exception(f"Sorry, there's no deco by the name \"{deco_name}\"")
        
        #check if there is room for the deco
        deco_size = int(deco_name[-1])
        s1_size = self.slots['Slot 1']['Size']
        s2_size = self.slots['Slot 2']['Size']
        s3_size = self.slots['Slot 3']['Size']

        for slot in self.slots:
            if self.slots[slot]['Size'] < deco_size:
                raise Exception(f"Could not slot decoration \"{deco_name}\" of size \"{deco_size}\" into armor \"{self.name}\" with slot sizes with slot sizes [{s1_size},{s2_size},{s3_size}]")
            if self.slots[slot]['Equipped Deco'] == None:
                self.slots[slot]['Equipped Deco'] = deco_name
                self.slots[slot]['Slotted Skills'] = deco_object['Skills']
                if verbose:
                    print(f'Equipped {deco_name} to {self.name}')
                return
            
    def remove_decoration(self, slot):
        if slot not in [1,2,3]:
            raise Exception("Argument \"slot\" must be one of [1,2,3]")
        if slot == 1:
            if self.slots['Slot 1']['Equipped Deco'] == None:
                print("No deco to remove")
            self.slots['Slot 1']['Equipped Deco'] = None 
            self.slots['Slot 1']['Slotted Skills'] = {}
        elif slot == 2:
            if self.slots['Slot 2']['Equipped Deco'] == None:
                print("No deco to remove")
            self.slots['Slot 2']['Equipped Deco'] = None 
            self.slots['Slot 2']['Slotted Skills'] = {}
        elif slot == 3:
            if self.slots['Slot 3']['Equipped Deco'] == None:
                print("No deco to remove")
            self.slots['Slot 3']['Equipped Deco'] = None 
            self.slots['Slot 3']['Slotted Skills'] = {}
        return

class monster_hunter_armor:
    def __init__(self, name, loaded_slots = None):
        with open('data/armor_data.json', 'r') as file:
            armor_db = json.load(file)
        self.name = name
        self.armorType = armor_db[name]['Type']
        self.skills = armor_db[name]['Skills']
        if loaded_slots:
            self.slots = loaded_slots
        else:
            self.slots = armor_db[name]['Slots']
   
    def set_decoration(self, deco_name, slot = None, verbose = False):
        if deco_name == None:
            return
        #get deco from json database
        with open('data/decoration_data.json', 'r') as file:
            deco_db = json.load(file)
        try:
            deco_object = deco_db[deco_name]
        except:
            raise Exception(f"Sorry, there's no deco by the name \"{deco_name}\"")
        
        #check if there is room for the deco
        deco_size = int(deco_name[-1])
        s1_size = self.slots['Slot 1']['Size']
        s2_size = self.slots['Slot 2']['Size']
        s3_size = self.slots['Slot 3']['Size']

        for slot in self.slots:
            if self.slots[slot]['Size'] < deco_size:
                raise Exception(f"Could not slot decoration \"{deco_name}\" of size \"{deco_size}\" into armor \"{self.name}\" with slot sizes with slot sizes [{s1_size},{s2_size},{s3_size}]")
            if self.slots[slot]['Equipped Deco'] == None:
                self.slots[slot]['Equipped Deco'] = deco_name
                self.slots[slot]['Slotted Skills'] = deco_object['Skills']
                if verbose:
                    print(f'Equipped {deco_name} to {self.name}')
                return
            
    def remove_decoration(self, slot):
        if slot not in [1,2,3]:
            raise Exception("Argument \"slot\" must be one of [1,2,3]")
        if slot == 1:
            if self.slots['Slot 1']['Equipped Deco'] == None:
                print("No deco to remove")
            self.slots['Slot 1']['Equipped Deco'] = None 
            self.slots['Slot 1']['Slotted Skills'] = {}
        elif slot == 2:
            if self.slots['Slot 2']['Equipped Deco'] == None:
                print("No deco to remove")
            self.slots['Slot 2']['Equipped Deco'] = None 
            self.slots['Slot 2']['Slotted Skills'] = {}
        elif slot == 3:
            if self.slots['Slot 3']['Equipped Deco'] == None:
                print("No deco to remove")
            self.slots['Slot 3']['Equipped Deco'] = None 
            self.slots['Slot 3']['Slotted Skills'] = {}
        return
    def count_slots(self):
        counter = 0
        for slot in self.slots:
            if self.slots[slot]['Size'] > 0:
                counter += 1
        return counter
    

        

class monster_hunter_charm:
    def __init__(self, name):
        with open('data/charm_data.json', 'r') as file:
            charm_db = json.load(file)
        self.name = name
        self.skills = charm_db[name]['Skills']

class mixed_set:
    def __init__(self, name, weapon, head, chest, arms, waist, legs, charm):
        self.name = name
        self.weapon = weapon
        self.head = head
        self.chest = chest
        self.arms = arms
        self.waist = waist
        self.legs = legs
        self.charm = charm
        skill_sources = []
        
        if self.weapon:
            skill_sources.extend([
            self.weapon.skills,
            self.weapon.slots['Slot 1']['Slotted Skills'],
            self.weapon.slots['Slot 2']['Slotted Skills'],
            self.weapon.slots['Slot 3']['Slotted Skills']
            ])
        if self.head:
            skill_sources.extend([
            self.head.skills,
            self.head.slots['Slot 1']['Slotted Skills'],
            self.head.slots['Slot 2']['Slotted Skills'],
            self.head.slots['Slot 3']['Slotted Skills']
            ])
        if self.chest:
            skill_sources.extend([
            self.chest.skills,
            self.chest.slots['Slot 1']['Slotted Skills'],
            self.chest.slots['Slot 2']['Slotted Skills'],
            self.chest.slots['Slot 3']['Slotted Skills']
            ])
        if self.arms:
            skill_sources.extend([
            self.arms.skills,
            self.arms.slots['Slot 1']['Slotted Skills'],
            self.arms.slots['Slot 2']['Slotted Skills'],
            self.arms.slots['Slot 3']['Slotted Skills']
            ])
        if self.waist:
            skill_sources.extend([
            self.waist.skills,
            self.waist.slots['Slot 1']['Slotted Skills'],
            self.waist.slots['Slot 2']['Slotted Skills'],
            self.waist.slots['Slot 3']['Slotted Skills']
            ])
        if self.legs:
            skill_sources.extend([
            self.legs.skills,
            self.legs.slots['Slot 1']['Slotted Skills'],
            self.legs.slots['Slot 2']['Slotted Skills'],
            self.legs.slots['Slot 3']['Slotted Skills']
            ])
        if self.charm:
            skill_sources.append(self.charm.skills)
        
        # sum the points of the skills of each equipment piece
        self.active_skills = dict(functools.reduce(operator.add, map(collections.Counter, skill_sources)))

        # add in the unused skills as having 0 points
        with open('data/skills.csv','r') as file:
            skill_list = pd.read_csv(file)
            skill_dict = {skill: 0 for skill in skill_list['name']}
        for skill in self.active_skills:
            skill_dict[skill] = self.active_skills[skill]
        self.skills = skill_dict

    def calculate_efr(self, 
                      base_sharpness = 'default',
                      active_conditional_skills = [],
                      affinity_override = None,
                      triple_up = True, 
                      powercharm = False, 
                      might_seed = False,
                      might_pill = False,
                      food_buff = False,
                      verbose = False):
        base_raw = self.weapon.raw
        element = self.weapon.element
        base_element = self.weapon.element_value
        base_affinity = self.weapon.affinity / 100

        #-----------------------------------------
        # calc sharpness and effective sharpness
        #-----------------------------------------

        # if sharpness is given as a string, convert it to a float
        if base_sharpness == 'default':
            base_sharpness = self.weapon.base_sharpness
        if isinstance(base_sharpness, str):
            if base_sharpness == 'purple':
                sharpness_modifier = 1.39
                ele_sharpness_modifier = 1.27
            elif base_sharpness == 'white':
                sharpness_modifier = 1.32
                ele_sharpness_modifier = 1.15
            elif base_sharpness == 'blue':
                sharpness_modifier = 1.2
                ele_sharpness_modifier = 1.063
            elif base_sharpness == 'green':
                sharpness_modifier = 1.05
                ele_sharpness_modifier = 1
            elif base_sharpness == 'yellow':
                sharpness_modifier = 1.0
                ele_sharpness_modifier = 0.75
            elif base_sharpness == 'orange':
                sharpness_modifier = 0.75
                ele_sharpness_modifier = 0.5
            elif base_sharpness == 'red':
                sharpness_modifier = 0.5
                ele_sharpness_modifier = 0.25
            else:
                raise ValueError('Invalid sharpness value: ' + base_sharpness)
        elif isinstance(base_sharpness, float):
            if base_sharpness not in [1.39, 1.32, 1.2, 1.05, 1.0, 0.75, 0.5]:
                raise ValueError('Invalid sharpness value: ' + str(base_sharpness))
            sharpness_modifier = base_sharpness
        else:
            raise ValueError('Sharpness must be a string or a float, not a ' + type(base_sharpness).__name__)
        
        #-----------------------------------------
        # calc raw damage
        #-----------------------------------------

        
        
        if 'Attack Boost' in self.active_skills:
            base_raw+= base_raw* skill_boosts.attack_boost_percent[self.skills['Attack Boost']]
        raw = base_raw

        #flat boosts
        if 'Adrenaline Rush' in active_conditional_skills:
            raw += skill_boosts.adren_rush[self.skills['Adrenaline Rush']]
        if 'Agitator' in active_conditional_skills:
            raw+= skill_boosts.agitator_attack[self.skills['Agitator']]
        if 'Burst' in active_conditional_skills:
            raw+= skill_boosts.burst_raw[self.skills['Burst']]
        if 'Counterstrike' in active_conditional_skills:
            raw+= skill_boosts.counterstrike[self.skills['Counterstrike']]
        if 'Foray' in active_conditional_skills:
            raw+= skill_boosts.foray_raw[self.skills['Foray']]
        if 'Peak Performance' in active_conditional_skills:
            raw+= skill_boosts.peak_performance[self.skills['Peak Performance']]
        if 'Resentment' in active_conditional_skills:
            raw+= skill_boosts.resentment[self.skills['Resentment']]
        if "Gore Magala's Tyranny" in active_conditional_skills:
            raw+= skill_boosts.black_eclipse_raw_afflicted[self.skills["Gore Magala's Tyranny"]]
        if "Gore Magala's Tyranny" in active_conditional_skills:
            raw+= skill_boosts.black_eclipse_raw_recovered[self.skills["Gore Magala's Tyranny"]]

        
        #if 'Ambush' in active_conditional_skills:
        #    raw+= base_raw* skill_boosts.ambush[self.skills['Ambush']]
        if 'Bludgeoner' in active_conditional_skills:
            raw+= base_raw* skill_boosts.bludgeoner[self.skills['Bludgeoner']]
        if 'Heroics' in active_conditional_skills:
            raw+= base_raw* skill_boosts.heroics[self.skills['Heroics']]
        
        # percentage boosts
        if triple_up:
            raw += base_raw *0.15 
        if 'Attack Boost' in self.active_skills:
            raw+= skill_boosts.attack_boost_raw[self.skills['Attack Boost']]



        #-----------------------------------------
        # calc elemental damage
        #-----------------------------------------

        elemental_damage = base_element

        #percent boost
        if 'Coalescence' in active_conditional_skills:
            elemental_damage+= base_element* skill_boosts.coalescence[self.skills['Coalescence']]

        #flat boost
        if 'Burst' in active_conditional_skills:
            elemental_damage+= skill_boosts.burst_element[self.skills['Burst']]



        #-----------------------------------------
        # calc affinity and crit modifiers
        #-----------------------------------------
        affinity = base_affinity
        #print(f'affinity BEFORE skills: {affinity}')
        if 'Critical Eye' in self.active_skills:
            affinity+= skill_boosts.critical_eye[self.skills['Critical Eye']]
        if 'Agitator' in active_conditional_skills:
            affinity+= skill_boosts.agitator_affinity[self.skills['Agitator']]
        #if 'Critical Draw' in active_conditional_skills:
        #    affinity+= skill_boosts.critical_draw[self.skills['Critical Draw']]
        if 'Foray' in active_conditional_skills:
            affinity+= skill_boosts.foray_affinity[self.skills['Foray']]
        if 'Latent Power' in active_conditional_skills:
            affinity+= skill_boosts.latent_power[self.skills['Latent Power']]
        if 'Maximum Might' in active_conditional_skills:
            affinity+= skill_boosts.maximum_might[self.skills['Maximum Might']]
        if "Gore Magala's Tyranny" in active_conditional_skills:
            affinity+= skill_boosts.black_eclipse_affinity[self.skills["Gore Magala's Tyranny"]]
            if 'Antivirus' in active_conditional_skills:
                affinity+= skill_boosts.antivirus[self.skills['Antivirus']]
        #print(f'affinity AFTER skills: {affinity}')
        
        # crit modifiers
        if 'Critical Boost' in active_conditional_skills:
            crit_boost = min(self.skills['Critical Boost'], 5)
        else:
            crit_boost = 0
        #print(f'Crit boost: ')
        crit_modifier = 0.25 + 0.03 * crit_boost


        #-----------------------------------------
        # Run Formulae
        #-----------------------------------------
        if affinity_override != None:
            affinity = affinity_override
        
        attack_screen_raw = raw
        attack_screen_element = elemental_damage


        effective_raw = raw * sharpness_modifier * (1 + affinity * crit_modifier)
        effective_element = elemental_damage / 10  * ele_sharpness_modifier  
        #effective_sharpness = base_sharpness
        return effective_raw, effective_element, attack_screen_raw, attack_screen_element

    def calculate_damage_number(self, raw_damage, ele_damage, raw_mv, ele_mv, raw_hitzone, ele_hitzone):
        #efr = self.calculate_efr()
        raw_damage_num = raw_damage * raw_mv / 100 * raw_hitzone / 100
        #print(raw_damage_num)
        ele_damage_num = ele_damage * ele_mv * ele_hitzone / 100
        #print(ele_damage_num)
        total_damage_num = raw_damage_num + ele_damage_num
        return total_damage_num, raw_damage_num, ele_damage_num

    def get_damage_stats(self, active_conditional_skills, triple_up = True):
        attack_dict = {}
        stats_dict = {}
        data = pd.read_csv('data/ig_attack_data.csv')
        attacks = {attack_name: {'raw_mv':float(motion_value),'ele_mv' :float(element_mv*1.25)} for attack_name, motion_value,element_mv in zip(data['Attack'], data['Motion Value'],data['Element'])}
        non_crit_raw_dmg, non_crit_ele_dmg, attack_screen_raw, attack_screen_element = self.calculate_efr(active_conditional_skills=active_conditional_skills, affinity_override=0, verbose = True, triple_up=triple_up)
        crit_raw_dmg, crit_ele_dmg, _, _ = self.calculate_efr(active_conditional_skills=active_conditional_skills, affinity_override=1, triple_up=triple_up)
        effective_raw, effective_element, _, _ = self.calculate_efr(active_conditional_skills=active_conditional_skills, triple_up=triple_up)
        
        stats_dict['attack screen raw'] = attack_screen_raw
        stats_dict['attack screen element'] = attack_screen_element
        stats_dict['effective_raw'] = effective_raw
        stats_dict['effective_element'] = effective_element
        stats_dict['total effective damage'] = effective_raw + effective_element
        stats_dict['non_crit_raw_dmg'] = non_crit_raw_dmg
        stats_dict['non_crit_ele_dmg'] = non_crit_ele_dmg
        stats_dict['total_non_crit_damage'] = non_crit_raw_dmg + non_crit_ele_dmg
        stats_dict['crit_raw_dmg'] = crit_raw_dmg
        stats_dict['crit_ele_dmg'] = crit_ele_dmg
        stats_dict['total_crit_damage'] = crit_raw_dmg + crit_ele_dmg
        
        for attack in attacks:
            total_non_crit, raw_portion_non_crit, elemental_portion_non_crit = self.calculate_damage_number(non_crit_raw_dmg, non_crit_ele_dmg, raw_mv = attacks[attack]['raw_mv'], ele_mv = attacks[attack]['ele_mv'], raw_hitzone = 80, ele_hitzone = 23.97)
            total_crit, raw_portion_crit, elemental_portion_crit = self.calculate_damage_number(crit_raw_dmg, crit_ele_dmg, raw_mv = attacks[attack]['raw_mv'], ele_mv = attacks[attack]['ele_mv'], raw_hitzone = 80, ele_hitzone = 23.97)
            expected_total, expected_raw, expected_elemental = self.calculate_damage_number(effective_raw, effective_element, raw_mv = attacks[attack]['raw_mv'], ele_mv = attacks[attack]['ele_mv'], raw_hitzone = 80, ele_hitzone = 23.97)
            
            attack_dict[attack] = {
                'total_non_crit': total_non_crit,
                'total_crit': total_crit,
                'effective_total': expected_total,
                'raw_portion_non_crit': raw_portion_non_crit,
                'raw_portion_crit': raw_portion_crit,
                'effective_raw': expected_raw,
                'elemental_portion_non_crit': elemental_portion_non_crit,
                'elemental_portion_crit': elemental_portion_crit,
                'effective_elemental': expected_elemental
            }
        return attack_dict, stats_dict
    
    def save_set(self, file_name):
        set_as_json = {}
        if self.weapon:
            set_as_json['weapon_name'] = self.weapon.name
            set_as_json['weapon_slots'] = self.weapon.slots
        if self.head:
            set_as_json['head_name'] = self.head.name
            set_as_json['head_slots'] = self.head.slots
        if self.chest:
            set_as_json['chest_name'] = self.chest.name
            set_as_json['chest_slots'] = self.chest.slots
        if self.arms:
            set_as_json['arms_name'] = self.arms.name
            set_as_json['arms_slots'] = self.arms.slots
        if self.waist:
            set_as_json['waist_name'] = self.waist.name
            set_as_json['waist_slots'] = self.waist.slots
        if self.legs:
            set_as_json['legs_name'] = self.legs.name
            set_as_json['legs_slots'] = self.legs.slots
        if self.charm:
            set_as_json['charm_name'] = self.charm.name
        with open(file_name, 'w') as json_file:
            json.dump(set_as_json, json_file, indent=4)

def load_set(file_path):
    try:
        with open(file_path,'r') as file:
            set_as_json = json.load(file)
    except:
        raise Exception(f"could not open json file {file_path}")
        
    wep = monster_hunter_weapon(name=set_as_json['weapon_name'], loaded_slots=set_as_json['weapon_slots']) if 'weapon_name' in set_as_json else None
    head = monster_hunter_armor(name=set_as_json['head_name'], loaded_slots=set_as_json['head_slots']) if 'head_name' in set_as_json else None
    chest = monster_hunter_armor(name=set_as_json['chest_name'], loaded_slots=set_as_json['chest_slots']) if 'chest_name' in set_as_json else None
    arms = monster_hunter_armor(name=set_as_json['arms_name'], loaded_slots=set_as_json['arms_slots']) if 'arms_name' in set_as_json else None
    waist = monster_hunter_armor(name=set_as_json['waist_name'], loaded_slots=set_as_json['waist_slots']) if 'waist_name' in set_as_json else None
    legs = monster_hunter_armor(name=set_as_json['legs_name'], loaded_slots=set_as_json['legs_slots']) if 'legs_name' in set_as_json else None
    charm = monster_hunter_charm(name=set_as_json['charm_name']) if 'charm_name' in set_as_json else None

    loaded_set = mixed_set('loaded_set',wep,head,chest,arms,waist,legs,charm)
    return loaded_set


def roman_to_int(full_name):
    s = full_name.split()[-1]
    roman = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    prev_value = 0
    for char in reversed(s):
        value = roman[char]
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value
    return total

def int_to_roman(num):
    if not (1 <= num <= 5):
        raise ValueError("Input must be an integer between 1 and 5")
    roman_numerals = {1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V'}
    return roman_numerals[num]

#def clear_decos():
#    st.session_state.weapon_deco_selector_1 = None
#    st.session_state.weapon_deco_selector_2 = None
#    st.session_state.weapon_deco_selector_3 = None   