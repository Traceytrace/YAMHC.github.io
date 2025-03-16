import pandas as pd
import json
import collections, functools, operator
import skill_boosts
import streamlit as st

class monster_hunter_weapon:
    def __init__(self, name, loaded_slots = None, weapon_db = None):
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

    def set_decoration(self, deco_name, deco_db, slot = None, verbose = False):
        if verbose:
            print(f'Equipping {deco_name} to {self.name} in slot {slot}')
        if deco_name == None:
            self.slots[slot]['Equipped Deco'] = None
            self.slots[slot]['Slotted Skills'] = {}
            return
        
        #get deco from json database
        try:
            deco_object = deco_db[deco_name]
        except:
            raise Exception(f"Sorry, there's no deco by the name \"{deco_name}\"")
        
        #check if there is room for the deco
        deco_size = int(deco_name[-1])
        s1_size = self.slots['Slot 1']['Size']
        s2_size = self.slots['Slot 2']['Size']
        s3_size = self.slots['Slot 3']['Size']
        
        if self.slots[slot]['Size'] < deco_size:
            raise Exception(f"Could not slot decoration \"{deco_name}\" of size \"{deco_size}\" into armor \"{self.name}\" with slot sizes [{s1_size},{s2_size},{s3_size}]")
        
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
    def __init__(self, name, loaded_slots = None, armor_db = None):
        self.name = name
        self.armorType = armor_db[name]['Type']
        self.skills = armor_db[name]['Skills']
        if loaded_slots:
            self.slots = loaded_slots
        else:
            self.slots = armor_db[name]['Slots']
   
    def set_decoration(self, deco_name, deco_db, slot = None, key = None, verbose = False):
        if verbose:
            print(f'Equipping {deco_name} to {self.name} in slot {slot}')
        if deco_name == None:
            self.slots[slot]['Equipped Deco'] = None
            self.slots[slot]['Slotted Skills'] = {}
            return
        #if key:
        #    del st.session_state[key]
        #    st.session_state[key] = deco_name
        #get deco from json database
        try:
            deco_object = deco_db[deco_name]
        except:
            raise Exception(f"Sorry, there's no deco by the name \"{deco_name}\"")
        
        #check if there is room for the deco
        deco_size = int(deco_name[-1])
        s1_size = self.slots['Slot 1']['Size']
        s2_size = self.slots['Slot 2']['Size']
        s3_size = self.slots['Slot 3']['Size']
        
        if self.slots[slot]['Size'] < deco_size:
            raise Exception(f"Could not slot decoration \"{deco_name}\" of size \"{deco_size}\" into armor \"{self.name}\" with slot sizes with slot sizes [{s1_size},{s2_size},{s3_size}]")
        
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
    def __init__(self, name, charm_db = None):
        self.name = name
        self.skills = charm_db[name]['Skills']

class mixed_set:
    def __init__(self, name, weapon, head, chest, arms, waist, legs, charm, skill_db = None):
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
        self.equipped_skills = dict(functools.reduce(operator.add, map(collections.Counter, skill_sources)))
        #print(self.equipped_skills)
        # cap skills at their max level
        self.equipped_skills = {skill : min(self.equipped_skills[skill], int(skill_db[skill]['max_level'])) for skill in self.equipped_skills} # remove skills with 0 points
        self.equipped_skills = dict(sorted(self.equipped_skills.items(), key=lambda item: item[1], reverse=True))


        
        # add in the unused skills as having 0 points
        skill_dict = {sk : 0 for sk in skill_db.keys()}
        for skill in self.equipped_skills:
            skill_dict[skill] = self.equipped_skills[skill]
        self.skills_plus_zeroes = skill_dict
        #print(self.skills_plus_zeroes)

    def calculate_efr(self, 
                      base_sharpness = 'default',
                      active_conditional_skills = [],
                      affinity_override = None,
                      triple_up = True, 
                      powercharm = False, 
                      might_seed = False,
                      might_pill = False,
                      food_buff = False,
                      verbose = False,
                      uptime_dict = {}):
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

        
        
        if 'Attack Boost' in self.equipped_skills:
            base_raw+= base_raw* skill_boosts.attack_boost_percent[self.skills_plus_zeroes['Attack Boost']]
        raw = base_raw
    
        #flat boosts
        if 'Adrenaline Rush' in active_conditional_skills:
            boost = skill_boosts.adren_rush[self.skills_plus_zeroes['Adrenaline Rush']]
            raw += boost * (uptime_dict['Adrenaline Rush'] / 100) if ('Adrenaline Rush' in uptime_dict and affinity_override==None) else boost
        if 'Agitator' in active_conditional_skills:
            boost = skill_boosts.agitator_attack[self.skills_plus_zeroes['Agitator']]
            raw += boost * (uptime_dict['Agitator'] / 100) if 'Agitator' in uptime_dict and affinity_override is None else boost
        if 'Burst' in active_conditional_skills:
            boost = skill_boosts.burst_raw[self.skills_plus_zeroes['Burst']]
            raw += boost * (uptime_dict['Burst'] / 100) if 'Burst' in uptime_dict and affinity_override is None else boost
        if 'Counterstrike' in active_conditional_skills:
            boost = skill_boosts.counterstrike[self.skills_plus_zeroes['Counterstrike']]
            raw += boost * (uptime_dict['Counterstrike'] / 100) if 'Counterstrike' in uptime_dict and affinity_override is None else boost
        if 'Foray' in active_conditional_skills:
            boost = skill_boosts.foray_raw[self.skills_plus_zeroes['Foray']]
            raw += boost * (uptime_dict['Foray'] / 100) if 'Foray' in uptime_dict and affinity_override is None else boost
        if 'Peak Performance' in active_conditional_skills:
            boost = skill_boosts.peak_performance[self.skills_plus_zeroes['Peak Performance']]
            raw += boost * (uptime_dict['Peak Performance'] / 100) if 'Peak Performance' in uptime_dict and affinity_override is None else boost
        if 'Resentment' in active_conditional_skills:
            boost = skill_boosts.resentment[self.skills_plus_zeroes['Resentment']]
            raw += boost * (uptime_dict['Resentment'] / 100) if 'Resentment' in uptime_dict and affinity_override is None else boost
        if "Gore Magala's Tyranny" in active_conditional_skills:
            boost = skill_boosts.black_eclipse_raw_afflicted[self.skills_plus_zeroes["Gore Magala's Tyranny"]]
            raw += boost * (uptime_dict["Gore Magala's Tyranny"] / 100) if "Gore Magala's Tyranny" in uptime_dict and affinity_override is None else boost
        if "Gore Magala's Tyranny" in active_conditional_skills:
            boost = skill_boosts.black_eclipse_raw_recovered[self.skills_plus_zeroes["Gore Magala's Tyranny"]]
            raw += boost * (uptime_dict["Gore Magala's Tyranny"] / 100) if "Gore Magala's Tyranny" in uptime_dict and affinity_override is None else boost

        
        #if 'Ambush' in active_conditional_skills:
        #    raw+= base_raw* skill_boosts.ambush[self.skills['Ambush']]
        if 'Bludgeoner' in active_conditional_skills:
            boost = skill_boosts.bludgeoner[self.skills_plus_zeroes['Bludgeoner']]
            raw += boost * (uptime_dict['Bludgeoner'] / 100) if 'Bludgeoner' in uptime_dict else boost
        if 'Heroics' in active_conditional_skills:
            boost = skill_boosts.heroics[self.skills_plus_zeroes['Heroics']]
            raw += boost * (uptime_dict['Heroics'] / 100) if 'Heroics' in uptime_dict else boost
        
        # percentage boosts
        if triple_up:
            raw += base_raw *0.15 
        if 'Attack Boost' in self.equipped_skills:
            raw+= skill_boosts.attack_boost_raw[self.skills_plus_zeroes['Attack Boost']]



        #-----------------------------------------
        # calc elemental damage
        #-----------------------------------------

        elemental_damage = base_element

        # percent boost
        if 'Coalescence' in active_conditional_skills:
            boost = skill_boosts.coalescence[self.skills_plus_zeroes['Coalescence']]
            elemental_damage += base_element * (boost * (uptime_dict['Coalescence'] / 100) if 'Coalescence' in uptime_dict else boost)

        # flat boost
        if 'Burst' in active_conditional_skills:
            boost = skill_boosts.burst_element[self.skills_plus_zeroes['Burst']]
            elemental_damage += boost * (uptime_dict['Burst'] / 100) if 'Burst' in uptime_dict else boost



        #-----------------------------------------
        # calc affinity and crit modifiers
        #-----------------------------------------
        affinity = base_affinity
        #print(f'affinity BEFORE skills: {affinity}')
        if 'Critical Eye' in self.equipped_skills:
            affinity+= skill_boosts.critical_eye[self.skills_plus_zeroes['Critical Eye']]
        if 'Agitator' in active_conditional_skills:
            boost = skill_boosts.agitator_affinity[self.skills_plus_zeroes['Agitator']]
            affinity += boost * (uptime_dict['Agitator'] / 100) if 'Agitator' in uptime_dict else boost
        if 'Foray' in active_conditional_skills:
            boost = skill_boosts.foray_affinity[self.skills_plus_zeroes['Foray']]
            affinity += boost * (uptime_dict['Foray'] / 100) if 'Foray' in uptime_dict else boost
        if 'Latent Power' in active_conditional_skills:
            boost = skill_boosts.latent_power[self.skills_plus_zeroes['Latent Power']]
            affinity += boost * (uptime_dict['Latent Power'] / 100) if 'Latent Power' in uptime_dict else boost
        if 'Maximum Might' in active_conditional_skills:
            boost = skill_boosts.maximum_might[self.skills_plus_zeroes['Maximum Might']]
            affinity += boost * (uptime_dict['Maximum Might'] / 100) if 'Maximum Might' in uptime_dict else boost
        if "Gore Magala's Tyranny" in active_conditional_skills:
            boost = skill_boosts.black_eclipse_affinity[self.skills_plus_zeroes["Gore Magala's Tyranny"]]
            affinity += boost * (uptime_dict["Gore Magala's Tyranny"] / 100) if "Gore Magala's Tyranny" in uptime_dict else boost
            if 'Antivirus' in active_conditional_skills:
                boost = skill_boosts.antivirus[self.skills_plus_zeroes['Antivirus']]
                affinity += boost * (uptime_dict['Antivirus'] / 100) if 'Antivirus' in uptime_dict else boost
        #print(f'affinity AFTER skills: {affinity}')
        
        # crit modifiers
        if 'Critical Boost' in active_conditional_skills:
            crit_boost = self.skills_plus_zeroes['Critical Boost']
        else:
            crit_boost = 0

        crit_modifier = 0.25 + 0.03 * crit_boost


        #-----------------------------------------
        # Run Formulae
        #-----------------------------------------
        attack_screen_affinity = affinity*100
        print(f'attack screen affinity: {attack_screen_affinity}')
        if affinity_override != None:
            affinity = affinity_override
        
        attack_screen_raw = raw
        attack_screen_element = elemental_damage
        

        effective_raw = raw * sharpness_modifier * (1 + affinity * crit_modifier)
        effective_element = elemental_damage / 10  * ele_sharpness_modifier  
        #effective_sharpness = base_sharpness
        return effective_raw, effective_element, attack_screen_raw, attack_screen_element, attack_screen_affinity

    def calculate_damage_number(self, raw_damage, ele_damage, raw_mv, ele_mv, raw_hitzone, ele_hitzone):
        #efr = self.calculate_efr()
        raw_damage_num = raw_damage * raw_mv / 100 * raw_hitzone / 100
        #print(raw_damage_num)
        ele_damage_num = ele_damage * ele_mv * ele_hitzone / 100
        #print(ele_damage_num)
        total_damage_num = raw_damage_num + ele_damage_num
        return total_damage_num, raw_damage_num, ele_damage_num

    def get_damage_stats(self, active_skills, attack_data:dict = {}, triple_up = True, uptime_dict = {}):
        attack_stats_dict = {}
        stats_dict = {}

        # NO UPTIME APPLIED
        _, _, attack_screen_raw, attack_screen_element, attack_screen_affinity = self.calculate_efr(active_conditional_skills=active_skills, affinity_override=0, verbose = True, triple_up=triple_up)
        
        # UPTIME APPLIED
        non_crit_raw_dmg, non_crit_ele_dmg, _, _, _ = self.calculate_efr(active_conditional_skills=active_skills, affinity_override=0, verbose = True, triple_up=triple_up, uptime_dict=uptime_dict)
        crit_raw_dmg, crit_ele_dmg, _, _, _ = self.calculate_efr(active_conditional_skills=active_skills, affinity_override=1, triple_up=triple_up, uptime_dict=uptime_dict)
        effective_raw, effective_element, _, _, _ = self.calculate_efr(active_conditional_skills=active_skills, triple_up=triple_up, uptime_dict=uptime_dict)
        
        stats_dict['attack screen raw'] = attack_screen_raw
        stats_dict['attack screen element'] = attack_screen_element
        stats_dict['attack screen affinity'] = attack_screen_affinity
        stats_dict['effective_raw'] = effective_raw
        stats_dict['effective_element'] = effective_element
        stats_dict['total effective damage'] = effective_raw + effective_element
        stats_dict['non_crit_raw_dmg'] = non_crit_raw_dmg
        stats_dict['non_crit_ele_dmg'] = non_crit_ele_dmg
        stats_dict['total_non_crit_damage'] = non_crit_raw_dmg + non_crit_ele_dmg
        stats_dict['crit_raw_dmg'] = crit_raw_dmg
        stats_dict['crit_ele_dmg'] = crit_ele_dmg
        stats_dict['total_crit_damage'] = crit_raw_dmg + crit_ele_dmg
        
        for attack in attack_data:
            
            total_non_crit, raw_portion_non_crit, elemental_portion_non_crit = self.calculate_damage_number(non_crit_raw_dmg, non_crit_ele_dmg, raw_mv = attack_data[attack]['Motion Value'], ele_mv = attack_data[attack]['Element'], raw_hitzone = 80, ele_hitzone = 23.97)
            
            total_crit, raw_portion_crit, elemental_portion_crit = self.calculate_damage_number(crit_raw_dmg, crit_ele_dmg, raw_mv = attack_data[attack]['Motion Value'], ele_mv = attack_data[attack]['Element'], raw_hitzone = 80, ele_hitzone = 23.97)
            expected_total, expected_raw, expected_elemental = self.calculate_damage_number(effective_raw, effective_element, raw_mv = attack_data[attack]['Motion Value'], ele_mv = attack_data[attack]['Element'], raw_hitzone = 80, ele_hitzone = 23.97)
            
            attack_stats_dict[attack] = {
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
        return attack_stats_dict, stats_dict
    
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

def load_set(file_path, weapon_db = None, armor_db = None, charm_db = None, skill_db = None):
    try:
        with open(file_path,'r') as file:
            set_as_json = json.load(file)
    except:
        raise Exception(f"could not open json file {file_path}")
        
    wep = monster_hunter_weapon(name=set_as_json['weapon_name'], loaded_slots=set_as_json['weapon_slots'], weapon_db=weapon_db) if 'weapon_name' in set_as_json else None
    head = monster_hunter_armor(name=set_as_json['head_name'], loaded_slots=set_as_json['head_slots'], armor_db=armor_db) if 'head_name' in set_as_json else None
    chest = monster_hunter_armor(name=set_as_json['chest_name'], loaded_slots=set_as_json['chest_slots'], armor_db=armor_db) if 'chest_name' in set_as_json else None
    arms = monster_hunter_armor(name=set_as_json['arms_name'], loaded_slots=set_as_json['arms_slots'], armor_db=armor_db) if 'arms_name' in set_as_json else None
    waist = monster_hunter_armor(name=set_as_json['waist_name'], loaded_slots=set_as_json['waist_slots'], armor_db=armor_db) if 'waist_name' in set_as_json else None
    legs = monster_hunter_armor(name=set_as_json['legs_name'], loaded_slots=set_as_json['legs_slots'], armor_db=armor_db) if 'legs_name' in set_as_json else None
    charm = monster_hunter_charm(name=set_as_json['charm_name'], charm_db=charm_db) if 'charm_name' in set_as_json else None

    loaded_set = mixed_set('loaded_set',wep,head,chest,arms,waist,legs,charm, skill_db=skill_db)
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

def filter_charms(charm_db, show_only_max_level = True, alphabetical_order = True):
    # Filter by levels
    if show_only_max_level:
        charm_dict = {}
        for name,details in charm_db.items():
            if details['max_level'] == details['current_level']:
                charm_dict[name] = charm_db[name]
    else:
        charm_dict = charm_db

    #convert to list
    charm_options = [name for name in charm_dict.keys()]

    # filter by alphabetical order or not
    if alphabetical_order:
        return sorted(charm_options)
    return charm_options

def find_item_name_by_alternate_name(charm_db, given_name):
    for item in charm_db.values():
        if item['Alternate Name'] == given_name:
            return item['Item Name']
    for item in charm_db.values():
        if item['Item Name'] == given_name:
            return item['Alternate Name']
    return None

def find_weapon_name_by_alternate_name(charm_db, given_name):
    for item in charm_db.values():
        if item['tree'] == given_name:
            return item['name']
    for item in charm_db.values():
        if item['name'] == given_name:
            return item['tree']
    return None

def rename_charms_in_db(charm_db, name_setting = 'Charm'):
    #print(f'name setting entering function: {name_setting}')
    name_setting = st.session_state.charm_names
    #print(f'name setting after: {name_setting}')
    #print(list(charm_db.keys())[0])
    if name_setting == 'Charm':
        new_charm_db = {details['Item Name']: details for _, details in charm_db.items()}
    elif name_setting == 'Skill':
        new_charm_db = {details['Alternate Name']: details for _, details in charm_db.items()}
    st.session_state['charm_data'] = new_charm_db

    # reset charm selector to new name
    current_entry = st.session_state.charm_selector
    st.session_state.charm_selector = find_item_name_by_alternate_name(new_charm_db, current_entry)
    return

def rename_decos_in_db(deco_db, name_setting = 'Deco'):
    #print(f'name setting entering function: {name_setting}')
    name_setting = st.session_state.deco_names
    #print(f'name setting after: {name_setting}')

    #print(list(deco_db.keys())[0])
    if name_setting == 'Deco':
        new_deco_db = {details['Item Name']: details for _, details in deco_db.items()}
    elif name_setting == 'Skill':
        new_deco_db = {details['Alternate Name']: details for _, details in deco_db.items()}
    st.session_state['decoration_data'] = new_deco_db

    #reset deco selectors to new names
    deco_equipment = ['weapon', 'helm', 'chest', 'arms', 'waist', 'legs']
    for item in deco_equipment:
        for num in [1,2,3]:
            entry_key = item + '_deco_selector' + '_' + str(num)
            if entry_key not in st.session_state:
                continue
            current_entry = st.session_state[entry_key]
            st.session_state[entry_key] = find_item_name_by_alternate_name(new_deco_db, current_entry)
    return

def rename_weapons_in_db(weapon_db, crafted_db, name_setting = 'Weapon'):
    #print(f'name setting entering function: {name_setting}')
    name_setting = st.session_state.weapon_names
    #print(f'name setting after: {name_setting}')

    #print(list(deco_db.keys())[0])
    if name_setting == 'Weapon':
        new_weapon_db = {details['name']: details for _, details in weapon_db.items()}
    elif name_setting == 'Tree':
        new_weapon_db = {details['tree']: details for _, details in weapon_db.items()}

    if name_setting == 'Weapon':
        new_crafted_db = {details['name']: details for _, details in crafted_db.items()}
    elif name_setting == 'Tree':
        new_crafted_db = {details['tree']: details for _, details in crafted_db.items()}

    st.session_state['weapon_data'] = new_weapon_db
    st.session_state['crafted_weapon_data'] = new_crafted_db
    # reset weapon selector to new name
    current_entry = st.session_state.weapon_selector
    st.session_state.weapon_selector = find_weapon_name_by_alternate_name(new_weapon_db, current_entry)
    return
