import streamlit as st
import pandas as pd
from utils import monster_hunter_armor, monster_hunter_charm, monster_hunter_weapon, mixed_set, load_set, roman_to_int, int_to_roman
import collections, functools, operator
import math
print('Running Page!')
#################################
# Initialisation
#################################

st.set_page_config(layout = "wide")
# Remove whitespace from the top of the page and sidebar
# Reducing whitespace on the top of the page
st.markdown("""
<style>

.block-container
{
    padding-top: 1rem;
    padding-bottom: 4rem;
    margin-top: 0rem;
}

</style>
""", unsafe_allow_html=True)
# Streamlit UI



if 'equipped_set' not in st.session_state:
    st.session_state.equipped_set = None


##################################
# load in data
##################################

# load dbs
if 'armor_data' not in st.session_state:
    st.session_state.armor_data = pd.read_json('data/armor_data.json')
if 'artian_weapon_data' not in st.session_state:
    st.session_state.artian_weapon_data = pd.read_json('data/ig_artian_weapon_data.json')
if 'crafted_weapon_data' not in st.session_state:
    st.session_state.crafted_weapon_data = pd.read_json('data/ig_crafted_weapon_data.json')
if 'weapon_data' not in st.session_state:
    st.session_state.weapon_data = {**st.session_state.crafted_weapon_data, **st.session_state.artian_weapon_data}
if 'charm_data' not in st.session_state:
    st.session_state.charm_data = pd.read_json('data/charm_data.json')
if 'decoration_data' not in st.session_state:
    st.session_state.decoration_data = pd.read_json('data/decoration_data.json')
if 'attack_data' not in st.session_state:
    st.session_state.attack_data = pd.read_json('data/ig_attack_data.json')
if 'skill_data' not in st.session_state:
    st.session_state.skill_data = pd.read_json('data/skills.json')

armor_data = st.session_state.armor_data
weapon_data = st.session_state.weapon_data
charm_data = st.session_state.charm_data
decoration_data = st.session_state.decoration_data
attack_data = st.session_state.attack_data
skill_data = st.session_state.skill_data
# create options for user selection
armor_options = [name for name,details in armor_data.items()]
armor_options = sorted(armor_options)
weapon_options = [name for name,details in weapon_data.items()]
weapon_options = sorted(weapon_options)
charm_options = [name for name,details in charm_data.items()]
charm_options = sorted(charm_options)

#st.session_state['loaded_set'] = load_set('sets/meta_frenzy.json'

col1, col2 = st.columns(2)
with col1:
    # Equipment selection
    st.title("Equipment Set")
with col2:
    # Equipment selection
    st.title("Calculations")

button_col_1, button_col_2, button_col_3, button_col_4, button_col_5, button_col_6, button_col_7, button_col_8 = st.columns(8)

with button_col_1:
    if st.button('Load Set From File', key=19, use_container_width = True):
        loaded_set = load_set('sets/meta_frenzy.json', weapon_db=weapon_data, armor_db=armor_data, charm_db=charm_data, skill_db=skill_data)
        if loaded_set.weapon:
            equipped_weapon = loaded_set.weapon
            equipped_deco_1_name = loaded_set.weapon.slots['Slot 1']['Equipped Deco']
            equipped_deco_2_name = loaded_set.weapon.slots['Slot 2']['Equipped Deco']
            equipped_deco_3_name = loaded_set.weapon.slots['Slot 3']['Equipped Deco']
            st.session_state.weapon_selector = equipped_weapon.name
            st.session_state.weapon_deco_selector_1 = equipped_deco_1_name
            st.session_state.weapon_deco_selector_2 = equipped_deco_2_name
            st.session_state.weapon_deco_selector_3 = equipped_deco_3_name

        if loaded_set.head:
            equipped_helm = loaded_set.head
            equipped_helm_name = loaded_set.head.name
            st.session_state.helm_selector = equipped_helm_name
            equipped_helm_deco_1_name = loaded_set.head.slots['Slot 1']['Equipped Deco']
            equipped_helm_deco_2_name = loaded_set.head.slots['Slot 2']['Equipped Deco']
            equipped_helm_deco_3_name = loaded_set.head.slots['Slot 3']['Equipped Deco']
            st.session_state.helm_deco_selector_1 = equipped_helm_deco_1_name
            st.session_state.helm_deco_selector_2 = equipped_helm_deco_2_name
            st.session_state.helm_deco_selector_3 = equipped_helm_deco_3_name

        if loaded_set.chest:
            equipped_chest = loaded_set.chest
            equipped_chest_name = loaded_set.chest.name
            st.session_state.chest_selector = equipped_chest_name
            equipped_chest_deco_1_name = loaded_set.chest.slots['Slot 1']['Equipped Deco']
            equipped_chest_deco_2_name = loaded_set.chest.slots['Slot 2']['Equipped Deco']
            equipped_chest_deco_3_name = loaded_set.chest.slots['Slot 3']['Equipped Deco']
            st.session_state.chest_deco_selector_1 = equipped_chest_deco_1_name
            st.session_state.chest_deco_selector_2 = equipped_chest_deco_2_name
            st.session_state.chest_deco_selector_3 = equipped_chest_deco_3_name

        if loaded_set.arms:
            equipped_arms = loaded_set.arms
            equipped_arms_name = loaded_set.arms.name
            st.session_state.arms_selector = equipped_arms_name
            equipped_arms_deco_1_name = loaded_set.arms.slots['Slot 1']['Equipped Deco']
            equipped_arms_deco_2_name = loaded_set.arms.slots['Slot 2']['Equipped Deco']
            equipped_arms_deco_3_name = loaded_set.arms.slots['Slot 3']['Equipped Deco']
            st.session_state.arms_deco_selector_1 = equipped_arms_deco_1_name
            st.session_state.arms_deco_selector_2 = equipped_arms_deco_2_name
            st.session_state.arms_deco_selector_3 = equipped_arms_deco_3_name

        if loaded_set.waist:
            equipped_waist = loaded_set.waist
            equipped_waist_name = loaded_set.waist.name
            st.session_state.waist_selector = equipped_waist_name
            equipped_waist_deco_1_name = loaded_set.waist.slots['Slot 1']['Equipped Deco']
            equipped_waist_deco_2_name = loaded_set.waist.slots['Slot 2']['Equipped Deco']
            equipped_waist_deco_3_name = loaded_set.waist.slots['Slot 3']['Equipped Deco']
            st.session_state.waist_deco_selector_1 = equipped_waist_deco_1_name
            st.session_state.waist_deco_selector_2 = equipped_waist_deco_2_name
            st.session_state.waist_deco_selector_3 = equipped_waist_deco_3_name

        if loaded_set.legs:
            equipped_legs = loaded_set.legs
            equipped_legs_name = loaded_set.legs.name
            st.session_state.legs_selector = equipped_legs_name
            equipped_legs_deco_1_name = loaded_set.legs.slots['Slot 1']['Equipped Deco']
            equipped_legs_deco_2_name = loaded_set.legs.slots['Slot 2']['Equipped Deco']
            equipped_legs_deco_3_name = loaded_set.legs.slots['Slot 3']['Equipped Deco']
            st.session_state.legs_deco_selector_1 = equipped_legs_deco_1_name
            st.session_state.legs_deco_selector_2 = equipped_legs_deco_2_name
            st.session_state.legs_deco_selector_3 = equipped_legs_deco_3_name

        if loaded_set.charm:
            equipped_charm = loaded_set.charm
            equipped_charm_name = loaded_set.charm.name
            st.session_state.charm_selector = equipped_charm_name

with button_col_2:
    if st.button('Save set to file', key=20, use_container_width = True):
        if not st.session_state['equipped_set']:
            raise ValueError("No set to save.")
        st.session_state['equipped_set'].save_set('sets/test_save.json')

with button_col_3:
    if st.button('Clear All Equipment', key=21, use_container_width = True):
        st.session_state.weapon_selector = None
        st.session_state.helm_selector = None
        st.session_state.chest_selector = None
        st.session_state.arms_selector = None
        st.session_state.waist_selector = None
        st.session_state.legs_selector = None
        st.session_state.charm_selector = None
        st.session_state.equipped_set = None

with button_col_4:
    if st.button('Clear Decorations', key=22, use_container_width = True):
        st.session_state.weapon_deco_selector_1 = None
        st.session_state.weapon_deco_selector_2 = None
        st.session_state.weapon_deco_selector_3 = None
        st.session_state.helm_deco_selector_1 = None
        st.session_state.helm_deco_selector_2 = None
        st.session_state.helm_deco_selector_3 = None
        st.session_state.chest_deco_selector_1 = None
        st.session_state.chest_deco_selector_2 = None
        st.session_state.chest_deco_selector_3 = None
        st.session_state.arms_deco_selector_1 = None
        st.session_state.arms_deco_selector_2 = None
        st.session_state.arms_deco_selector_3 = None
        st.session_state.waist_deco_selector_1 = None
        st.session_state.waist_deco_selector_2 = None
        st.session_state.waist_deco_selector_3 = None
        st.session_state.legs_deco_selector_1 = None
        st.session_state.legs_deco_selector_2 = None
        st.session_state.legs_deco_selector_3 = None



###########################################
# Select Weapon
###########################################
col1, col2 = st.columns(2)
with col1:

    # Select armor rank
    user_armor_rank_setting = st.segmented_control(label = "Armor Rank", options = ['Low', 'High'], default= 'High', key = 'armor_rank_selector')
    
    try:
        equipped_weapon = monster_hunter_weapon(st.selectbox(label = "Weapon", options = weapon_options, index = None, placeholder='Select a weapon', key = 'weapon_selector'), weapon_db=weapon_data)
    except:
        equipped_weapon = None

    # create decoration slots
    if equipped_weapon != None:
        if equipped_weapon.count_slots() > 0:
            for i, col in enumerate(st.columns(equipped_weapon.count_slots())):
                with col:
                    slot_size = equipped_weapon.slots[f'Slot {i+1}']['Size']
                    decoration_options = [name for name,details in decoration_data.items() if int(name[-1]) <= slot_size and details['Type'] == 'sword']
                    decoration_options = sorted(decoration_options, key=lambda x: (x[-1]), reverse=True)
                    equipped_weapon.set_decoration(
                        st.selectbox(label=f"{slot_size}-slot decoration", 
                        options=decoration_options, 
                        index = None, 
                        placeholder='Set a decoration', 
                        key=f'weapon_deco_selector_{i+1}'),
                        deco_db=decoration_data,
                        slot = f'Slot {i+1}')
        
    ############################################
    # Select Helm
    ############################################
    helm_options = [name for name,details in armor_data.items() if details.Type == 'Helm' and (details['Rank'] == user_armor_rank_setting)]
    helm_options = sorted(helm_options)

    try:
        equipped_helm = monster_hunter_armor(st.selectbox(label = "Helm", options = helm_options, index = None, placeholder='Select head armor', key = 'helm_selector'),armor_db=armor_data)
    except:
        equipped_helm = None

    # create decoration slots
    if equipped_helm != None:
        if equipped_helm.count_slots() > 0:
            for i, col in enumerate(st.columns(3)):
                if i >= equipped_helm.count_slots():
                    continue
                with col:
                    slot_size = equipped_helm.slots[f'Slot {i+1}']['Size']
                    decoration_options = [name for name,details in decoration_data.items() if int(name[-1]) <= slot_size and details['Type'] == 'shield']
                    decoration_options = sorted(decoration_options, key=lambda x: (x[-1]), reverse=True)
                    print(f'Slot {i+1}')
                    print(equipped_helm.slots)
                    equipped_helm.set_decoration(
                        st.selectbox(label=f"{slot_size}-slot decoration", 
                        options=decoration_options, 
                        index = None, 
                        placeholder='Set a decoration', 
                        key=f'helm_deco_selector_{i+1}'),
                        slot = f'Slot {i+1}',
                        deco_db=decoration_data,
                        verbose=True)
                    print(equipped_helm.slots)
                    
    ############################################
    # Select Chest
    ############################################

    chest_options = [name for name,details in armor_data.items() if details.Type == 'Body' and (details['Rank'] == user_armor_rank_setting)]
    chest_options = sorted(chest_options)

    try:
        equipped_chest = monster_hunter_armor(st.selectbox(label = "Chest", options = chest_options, index = None, placeholder='Select chest armor', key = 'chest_selector'),armor_db=armor_data)
    except:
        equipped_chest = None

    # create decoration slots
    if equipped_chest != None:
        if equipped_chest.count_slots() > 0:
            for i, col in enumerate(st.columns(3)):
                if i >= equipped_chest.count_slots():
                    continue
                with col:
                    slot_size = equipped_chest.slots[f'Slot {i+1}']['Size']
                    decoration_options = [name for name,details in decoration_data.items() if int(name[-1]) <= slot_size and details['Type'] == 'shield']
                    decoration_options = sorted(decoration_options, key=lambda x: (x[-1]), reverse=True)
                    equipped_chest.set_decoration(
                        st.selectbox(label=f"{slot_size}-slot decoration", 
                        options=decoration_options, 
                        index = None, 
                        placeholder='Set a decoration', 
                        key=f'chest_deco_selector_{i+1}'),
                        deco_db=decoration_data,
                        slot = f'Slot {i+1}')

    ############################################
    # Select Arms
    ############################################

    arms_options = [name for name,details in armor_data.items() if details.Type == 'Arms' and (details['Rank'] == user_armor_rank_setting)]
    arms_options = sorted(arms_options)

    try:
        equipped_arms = monster_hunter_armor(st.selectbox(label = "Arms", options = arms_options, index = None, placeholder='Select arm armor', key = 'arms_selector'),armor_db=armor_data)
    except:
        equipped_arms = None

    # create decoration slots
    if equipped_arms != None:
        if equipped_arms.count_slots() > 0:
            for i, col in enumerate(st.columns(3)):
                if i >= equipped_arms.count_slots():
                    continue
                with col:
                    slot_size = equipped_arms.slots[f'Slot {i+1}']['Size']
                    decoration_options = [name for name,details in decoration_data.items() if int(name[-1]) <= slot_size and details['Type'] == 'shield']
                    decoration_options = sorted(decoration_options, key=lambda x: (x[-1]), reverse=True)
                    equipped_arms.set_decoration(
                        st.selectbox(label=f"{slot_size}-slot decoration", 
                        options=decoration_options, 
                        index = None, 
                        placeholder='Set a decoration', 
                        key=f'arms_deco_selector_{i+1}'),
                        deco_db=decoration_data,
                        slot = f'Slot {i+1}')

    ############################################
    # Select Waist
    ############################################

    waist_options = [name for name,details in armor_data.items() if details.Type == 'Waist' and (details['Rank'] == user_armor_rank_setting)]
    waist_options = sorted(waist_options)

    try:
        equipped_waist = monster_hunter_armor(st.selectbox(label = "Waist", options = waist_options, index = None, placeholder='Select waist armor', key = 'waist_selector'),armor_db=armor_data)
    except:
        equipped_waist = None

    # create decoration slots
    if equipped_waist != None:
        if equipped_waist.count_slots() > 0:
            for i, col in enumerate(st.columns(3)):
                if i >= equipped_waist.count_slots():
                    continue
                with col:
                    slot_size = equipped_waist.slots[f'Slot {i+1}']['Size']
                    decoration_options = [name for name,details in decoration_data.items() if int(name[-1]) <= slot_size and details['Type'] == 'shield']
                    decoration_options = sorted(decoration_options, key=lambda x: (x[-1]), reverse=True)
                    equipped_waist.set_decoration(
                        st.selectbox(label=f"{slot_size}-slot decoration", 
                        options=decoration_options, 
                        index = None, 
                        placeholder='Set a decoration', 
                        key=f'waist_deco_selector_{i+1}'),
                        deco_db=decoration_data,
                        slot = f'Slot {i+1}'
                        )

    ############################################
    # Select Legs
    ############################################

    legs_options = [name for name,details in armor_data.items() if details.Type == 'Legs' and (details['Rank'] == user_armor_rank_setting)]
    legs_options = sorted(legs_options)

    try:
        equipped_legs = monster_hunter_armor(st.selectbox(label = "Legs", options = legs_options, index = None, placeholder='Select leg armor', key = 'legs_selector'),armor_db=armor_data)
    except:
        equipped_legs = None

    # create decoration slots
    if equipped_legs != None:
        if equipped_legs.count_slots() > 0:
            for i, col in enumerate(st.columns(3)):
                if i >= equipped_legs.count_slots():
                    continue
                with col:
                    slot_size = equipped_legs.slots[f'Slot {i+1}']['Size']
                    decoration_options = [name for name,details in decoration_data.items() if int(name[-1]) <= slot_size and details['Type'] == 'shield']
                    decoration_options = sorted(decoration_options, key=lambda x: (x[-1]), reverse=True)
                    equipped_legs.set_decoration(
                        st.selectbox(label=f"{slot_size}-slot decoration", 
                        options=decoration_options, 
                        index = None, 
                        placeholder='Set a decoration', 
                        key=f'legs_deco_selector_{i+1}'),
                        deco_db=decoration_data,
                        slot = f'Slot {i+1}')
                    
    ############################################
    # Select Charm
    ############################################

    # Filter charm options to only show the max level of each charm
    max_level_charms = {}
    for charm in charm_options:
        if charm.split()[-1] == 'Charm':
            max_level_charms[charm] = charm
            continue
        base_name = ' '.join(charm.split()[:-1])
        level = roman_to_int(charm)
        if base_name not in max_level_charms or level > roman_to_int(max_level_charms[base_name]):
            max_level_charms[base_name] = int_to_roman(level)

    filtered_charm_options = [f"{name} {level}" for name, level in max_level_charms.items()]
    filtered_charm_options = sorted(filtered_charm_options)


    try:
        equipped_charm = monster_hunter_charm(st.selectbox(label = "Charm", options = filtered_charm_options, index = None, placeholder='Select a charm', key = 'charm_selector'),charm_db=charm_data)
    except:
        equipped_charm = None



    ############################################

    try: 
        st.session_state['equipped_set'] = mixed_set(
            name='Test Set',
            weapon=equipped_weapon,
            head=equipped_helm,
            chest=equipped_chest,
            arms=equipped_arms,
            waist=equipped_waist,
            legs=equipped_legs,
            charm=equipped_charm,
            skill_db=skill_data
        )   
    except Exception as e:
        st.session_state['equipped_set'] = None

     
 
    
    # Display active skills in the sidebar
    
    
    st.sidebar.title("Equipped Skills", anchor="sidebar-title")
    st.sidebar.write("Uptime Tuning")
    show_unconditional_skills = st.sidebar.checkbox("Hide Unconditional Skills", value=False, key='show_unconditional_skills')

    if st.session_state['equipped_set']:
        equipped_skills = st.session_state['equipped_set'].equipped_skills
        #print(equipped_skills)
        uptime_dict = {}
        st.sidebar.markdown("""
        <style>
        .stSlider {
            margin-top: 0rem;
            margin-bottom: 0.1rem;
            font-size: 0.8rem;
            padding: 0.0rem;
            width: 100%;
            max-width: 300px;
            height: 3rem;
        }
        </style>
        """, unsafe_allow_html=True)
        st.sidebar.markdown("""
        <style>
        .small-text {
            line-height: 0.1;
            padding: 0rem;
            margin: 0rem;
        }
        </style>
        """, unsafe_allow_html=True)
        for skill, level in equipped_skills.items():
            capped_level = min(level, skill_data[skill]['max_level'])
            skill_name = f"{skill} {capped_level}"

            if skill_data[skill]["conditional"] == "true":
                st.sidebar.markdown(f'<div class="small-text">{skill_name}</div>', unsafe_allow_html=True)
                uptime_dict[skill] = st.sidebar.slider(label = skill_name, min_value=0, max_value=100, value=100, key = f"active_skill_{skill}_uptime", label_visibility="collapsed")
            elif not show_unconditional_skills:
                
                st.sidebar.markdown(f'<div class="small-text">{skill_name}</div>', unsafe_allow_html=True)
                uptime_dict[skill] = st.sidebar.slider(label = skill_name, min_value=0, max_value=100, value=100, key = f"active_skill_{skill}_uptime",disabled=True, label_visibility="collapsed")
            
with col2:

    #################################################
    # Display the calculations
    #################################################

    def format_sig_figs(value, sig_figs,mode):
        value = value * 10**sig_figs
        if mode == 'down':
            value = math.floor(value)
        elif mode == 'up':
            value = math.ceil(value)
        elif mode == 'nearest':
            value = round(value)

        value = value / 10**sig_figs
        return f"{value:.{sig_figs}f}"
        
        
    
    if st.session_state['equipped_set'] and st.session_state['equipped_set'].weapon:

        ################################################################
        # Active Skills Selection
        ################################################################

    
        
        skill_options = list(st.session_state['equipped_set'].equipped_skills.keys())
        conditional_skills = [skill for skill in skill_options if skill_data[skill]["conditional"] == "true"]
        non_conditional_skills = [skill for skill in skill_options if skill_data[skill]["conditional"] == "false"]

        with button_col_5:
            if st.button('Deselect All Skills', use_container_width = True):
                st.session_state.activeskillscontrol = []
        with button_col_6:
            if st.button('Select All Skills', use_container_width = True):
                st.session_state.activeskillscontrol = conditional_skills
        
        active_conditional_skills = st.pills("Conditional Skills", options=conditional_skills, selection_mode="multi", default=[], key='activeskillscontrol')
        active_skills = non_conditional_skills + active_conditional_skills


        # Kinsect Extract Buff Selector
        buff_mode = st.segmented_control(label = "Buffs", options = ["Triple Up", "Red Buff Only", 'No Buffs'],default=["No Buffs"], selection_mode='single', key='triple_up', label_visibility="collapsed")
        attack_prerequisites = ['none']
        if buff_mode == "Triple Up":
            triple_up = True
            attack_prerequisites.append("triple up")
        elif buff_mode == "Red Buff Only":
            triple_up = False
            attack_prerequisites.append("red buff")
            attack_prerequisites.append("no triple up")
        else:
            triple_up = False
            attack_prerequisites.append("no triple up")
        
        available_attacks = {attack: details for attack, details in attack_data.items() if (details.get('prerequisite') in attack_prerequisites)}

        #active_conditional_skills = {skill: st.session_state['equipped_set'].active_skills[skill] for skill in selected_skills}
        #print(uptime_dict)
        damage_number_dict, damage_stats_dict = st.session_state['equipped_set'].get_damage_stats(active_skills, attack_data = attack_data, triple_up = triple_up, uptime_dict = uptime_dict)
        
        ################################################################
        # Display Pause Screen Stats
        ################################################################ 

        with st.expander("Pause Screen Stats", expanded = True):
            sig_figs_pause_screen = st.number_input("Significant Figures", min_value=0, max_value=5, value=0, step=1, key = 'sig_figs_pause_screen')

            mode = 'down'

            pause_screen_stat_cols = st.columns(3)

            with pause_screen_stat_cols[0]:
                st.write(f":red[Raw portion]")
                st.write(f"{format_sig_figs(damage_stats_dict['attack screen raw'], sig_figs_pause_screen, mode=mode)}")

            with pause_screen_stat_cols[1]:
                st.write(f":red[Elemental portion]")
                st.write(f"{format_sig_figs(damage_stats_dict['attack screen element'], sig_figs_pause_screen, mode=mode)}")
            


        ################################################################
        # Display Armor Set Stats
        ################################################################

        with st.expander("Armor Set Damage Stats"):

            values = damage_stats_dict
            sig_figs_equip_set = st.number_input("Significant Figures", min_value=0, max_value=5, value=1, step=1, key = 'sig_figs_equip_set')

            mode = 'nearest'

            equip_set_stat_cols = st.columns(3)
            with equip_set_stat_cols[0]:
                    st.write(f":red[Total Non-Crit]")
                    st.write(f"{format_sig_figs(values['total_non_crit_damage'], sig_figs_equip_set, mode=mode)}")
                    st.write(f":blue[Total Crit]")
                    st.write(f"{format_sig_figs(values['total_crit_damage'], sig_figs_equip_set, mode=mode)}")
                    st.write(":green[Effective Total]")
                    st.write(f"{format_sig_figs(values['total effective damage'], sig_figs_equip_set, mode=mode)}")
                    
            with equip_set_stat_cols[1]:
                st.write(f":red[Raw Portion Non-Crit]")
                st.write(f"{format_sig_figs(values['non_crit_raw_dmg'], sig_figs_equip_set, mode=mode)}")
                st.write(f":blue[Raw Portion Crit]")
                st.write(f"{format_sig_figs(values['crit_raw_dmg'], sig_figs_equip_set, mode=mode)}")
                st.write(":green[Effective Raw]")
                st.write(f"{format_sig_figs(values['effective_raw'], sig_figs_equip_set, mode=mode)}")
                
            with equip_set_stat_cols[2]:
                st.write(f":red[Elemental Portion Non-Crit]")
                st.write(f"{format_sig_figs(values['non_crit_ele_dmg'], sig_figs_equip_set, mode=mode)}")
                st.write(f":blue[Elemental Portion Crit]")
                st.write(f"{format_sig_figs(values['crit_ele_dmg'], sig_figs_equip_set, mode=mode)}")
                st.write(":green[Effective Elemental]")
                st.write(f"{format_sig_figs(values['effective_element'], sig_figs_equip_set, mode=mode)}")
            
       

        ################################################################
        # Display Weapon Attack Damage
        ################################################################

        with st.expander("Damage Numbers"):
            st.selectbox("Target", options=["Training Dummy"], index=0, disabled=True)

            selected_attack = st.selectbox("Select Attack", options=available_attacks, index=0)

            if selected_attack:
                values = damage_number_dict[selected_attack]
                attack_num_cols = st.columns(3)
                sig_figs_wep_attack = st.number_input("Significant Figures", min_value=0, max_value=5, value=1, step=1, key= 'sig_figs_wep_attack')

                mode = 'nearest'

                with attack_num_cols[0]:
                    st.write(f":red[Total Non-Crit]")
                    st.write(f"{format_sig_figs(values['total_non_crit'], sig_figs_wep_attack, mode=mode)}")
                    st.write(f":blue[Total Crit]")
                    st.write(f"{format_sig_figs(values['total_crit'], sig_figs_wep_attack, mode=mode)}")
                    st.write(":green[Effective Total]")
                    st.write(f"{format_sig_figs(values['effective_total'], sig_figs_wep_attack, mode=mode)}")
                    
                with attack_num_cols[1]:
                    st.write(f":red[Raw Portion Non-Crit]")
                    st.write(f"{format_sig_figs(values['raw_portion_non_crit'], sig_figs_wep_attack, mode=mode)}")
                    st.write(f":blue[Raw Portion Crit]")
                    st.write(f"{format_sig_figs(values['raw_portion_crit'], sig_figs_wep_attack, mode=mode)}")
                    st.write(":green[Effective Raw]")
                    st.write(f"{format_sig_figs(values['effective_raw'], sig_figs_wep_attack, mode=mode)}")

                with attack_num_cols[2]:
                    st.write(f":red[Elemental Portion Non-Crit]")
                    st.write(f"{format_sig_figs(values['elemental_portion_non_crit'], sig_figs_wep_attack, mode=mode)}")
                    st.write(f":blue[Elemental Portion Crit]")
                    st.write(f"{format_sig_figs(values['elemental_portion_crit'], sig_figs_wep_attack, mode=mode)}")
                    st.write(":green[Effective Elemental]")
                    st.write(f"{format_sig_figs(values['effective_elemental'], sig_figs_wep_attack, mode=mode)}")
            