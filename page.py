import streamlit as st
import pandas as pd
from utils import monster_hunter_armor, monster_hunter_charm, monster_hunter_weapon, mixed_set, load_set, roman_to_int, int_to_roman, filter_charms, rename_charms_in_db, rename_decos_in_db, rename_weapons_in_db
import collections, functools, operator
import math
print('----------start-----------------')
print('Running Page!')
try:
    print('include_artian_weapons = ', st.session_state.include_artian_weapons)
except:
    print('include_artian_weapons not in session state')

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
if 'user_deco_name_setting' not in st.session_state:
    st.session_state.user_deco_name_setting = 'Deco'
if 'user_charm_name_setting' not in st.session_state:
    st.session_state.user_charm_name_setting = 'Charm'
if 'user_weapon_name_setting' not in st.session_state:
    st.session_state.user_weapon_name_setting = 'Weapon'
if 'user_armor_rank_setting' not in st.session_state:
    st.session_state.user_armor_rank_setting = 'High'
if 'equipped_helm' not in st.session_state:
    st.session_state.equipped_helm = None
if 'actoveskillcontrol' not in st.session_state:
    st.session_state.activeskillscontrol = []


if 'charm_names' in st.session_state:
    if st.session_state.user_charm_name_setting != st.session_state.charm_names:
        #print(f'charm_names = {st.session_state.charm_names} but user_charm_name_setting = {st.session_state.user_charm_name_setting}')
        rename_charms_in_db(charm_db=st.session_state['charm_data'], name_setting=st.session_state.charm_names)
if 'deco_names' in st.session_state:
    if st.session_state.user_deco_name_setting != st.session_state.deco_names:
        #print(f'deco_names = {st.session_state.deco_names} but user_deco_name_setting = {st.session_state.user_deco_name_setting}')
        rename_decos_in_db(deco_db=st.session_state['decoration_data'], name_setting=st.session_state.user_deco_name_setting)
if 'weapon_names' in st.session_state:
    if st.session_state.user_weapon_name_setting != st.session_state.weapon_names:
        #print(f'deco_names = {st.session_state.deco_names} but user_deco_name_setting = {st.session_state.user_deco_name_setting}')
        rename_weapons_in_db(weapon_db=st.session_state['weapon_data'], crafted_db=st.session_state['crafted_weapon_data'], name_setting=st.session_state.user_weapon_name_setting)

try:
    include_artian_weapons = st.session_state.include_artian_weapons
except:
    include_artian_weapons = 'Yes'

# if include_artian_weapons == 'No':
#     print('include_artian_weapons = No, setting weapon_data to crafted_weapon_data')
#     weapon_data = st.session_state.crafted_weapon_data
# if include_artian_weapons == 'Yes':
#     print('include_artian_weapons = Yes, setting weapon_data to all weapons')
#     weapon_data = st.session_state.weapon_data

armor_data = st.session_state.armor_data
charm_data = st.session_state.charm_data
decoration_data = st.session_state.decoration_data
attack_data = st.session_state.attack_data
skill_data = st.session_state.skill_data
weapon_data = st.session_state.weapon_data

# create options for user selection
armor_options = [name for name,details in armor_data.items()]
armor_options = sorted(armor_options)

if include_artian_weapons == 'Yes':
    weapon_options = [name for name,details in weapon_data.items()]
else:
    weapon_options = [name for name,details in st.session_state.crafted_weapon_data.items()]
    
weapon_options = sorted(weapon_options)

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

expander_col_1, expander_col_2 = st.columns(2)
with expander_col_1:
    with st.popover("Equipment Option Settings", use_container_width=True):
        button_col_1, button_col_2, button_col_3 = st.columns(3, gap = 'large')
        with button_col_1:
            # Select whether to limit armor rank to low or high
            st.session_state.user_armor_rank_setting = st.segmented_control(label = "Armor Rank", options = ['Low', 'High'], default= 'High', key = 'armor_rank_selector')
            # select whether to use decoration names or skill names for decorations in dropdown list
            st.session_state.user_deco_name_setting = st.segmented_control(label = "Deco Names", options = ['Deco', 'Skill'], default= 'Deco', key = 'deco_names')
        with button_col_2:    
            # select whether to include artian weapons in dropdown list
            st.session_state.user_include_artian_weapon_setting = st.segmented_control(label = "Include Artian Weapons", options = ['No', 'Yes'], default= 'Yes', key = 'include_artian_weapons')
            st.session_state.user_charm_name_setting = st.segmented_control(label = "Charm Names", options = ['Charm', 'Skill'], default= 'Charm', key = 'charm_names')

        with button_col_3:
            # select whether to use weapon names or tree names for weapons in dropdown list
            st.session_state.user_weapon_name_setting= st.segmented_control(label = "Weapon Names", options = ['Weapon', 'Tree'], default= 'Weapon', key = 'weapon_names')



###########################################
# Select Weapon
###########################################
col1, col2 = st.columns(2)

with col1:
    try:
        equipped_weapon = monster_hunter_weapon(st.selectbox(label = "Weapon", options = weapon_options, index = None, placeholder='Select a weapon', key = 'weapon_selector'), weapon_db=weapon_data, )
    except Exception as e:
        print(f"Error selecting weapon: {e}")
        equipped_weapon = None

    # create decoration slots
    if equipped_weapon != None:
        if equipped_weapon.count_slots() > 0:
            for i, col in enumerate(st.columns(3)):
                if i >= equipped_weapon.count_slots():
                    continue
                with col:
                    slot_size = equipped_weapon.slots[f'Slot {i+1}']['Size']
                    key = f'weapon_deco_selector_{i+1}'

                    decoration_options = [name for name,details in decoration_data.items() if int(name[-1]) <= slot_size and details['Type'] == 'sword']
                    decoration_options = sorted(decoration_options, key=lambda x: (x[-1]), reverse=True)
                    if key in st.session_state:
                        try:
                            if int(st.session_state[key][-1]) > slot_size:
                                print(f"Invalid decoration size for {key}: {st.session_state[key]} > {slot_size}. Setting to None.")
                                st.session_state[key] = None
                            else:
                                print('valid decoration size')
                                st.session_state[key] = st.session_state[key]
                        except Exception as e:
                            #print(f"Error getting default value for {key}: {e}")
                            st.session_state[key] = None
                    else:
                        st.session_state[key] = None
                    equipped_weapon.set_decoration(
                        st.selectbox(label=f"{slot_size}-slot decoration", 
                        options=decoration_options, 
                        #index = default_value, 
                        placeholder='Set a decoration', 
                        key=f'weapon_deco_selector_{i+1}'),
                        deco_db=decoration_data,
                        slot = f'Slot {i+1}',
                        verbose=False)
        
    ############################################
    # Select Helm
    ############################################
    helm_options = [name for name,details in armor_data.items() if details.Type == 'Helm' and (details['Rank'] == st.session_state.user_armor_rank_setting)]
    helm_options = sorted(helm_options)

    try:
        equipped_helm = monster_hunter_armor(st.selectbox(label = "Helm", options = helm_options, index = None, placeholder='Select helm armor', key = 'helm_selector'),armor_db=armor_data)
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
                    key = f'helm_deco_selector_{i+1}'
                    decoration_options = [name for name,details in decoration_data.items() if int(name[-1]) <= slot_size and details['Type'] == 'shield']
                    decoration_options = sorted(decoration_options, key=lambda x: (x[-1]), reverse=True)
                    if key in st.session_state:
                        try:
                            if int(st.session_state[key][-1]) > slot_size:
                                print(f"Invalid decoration size for {key}: {st.session_state[key]} > {slot_size}. Setting to None.")
                                st.session_state[key] = None
                            else:
                                print('valid decoration size')
                                st.session_state[key] = st.session_state[key]
                        except Exception as e:
                            #print(f"Error getting default value for {key}: {e}")
                            st.session_state[key] = None
                    else:
                        st.session_state[key] = None
                    equipped_helm.set_decoration(
                        st.selectbox(label=f"{slot_size}-slot decoration", 
                        options=decoration_options, 
                        #index = default_value, 
                        placeholder='Set a decoration', 
                        key=key),
                        deco_db=decoration_data,
                        slot = f'Slot {i+1}')
                    
    ############################################
    # Select Chest
    ############################################

    chest_options = [name for name,details in armor_data.items() if details.Type == 'Body' and (details['Rank'] == st.session_state.user_armor_rank_setting)]
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
                    key = f'chest_deco_selector_{i+1}'
                    decoration_options = [name for name,details in decoration_data.items() if int(name[-1]) <= slot_size and details['Type'] == 'shield']
                    decoration_options = sorted(decoration_options, key=lambda x: (x[-1]), reverse=True)
                    if key in st.session_state:
                        try:
                            if int(st.session_state[key][-1]) > slot_size:
                                print(f"Invalid decoration size for {key}: {st.session_state[key]} > {slot_size}. Setting to None.")
                                st.session_state[key] = None
                            else:
                                print('valid decoration size')
                                st.session_state[key] = st.session_state[key]
                        except Exception as e:
                            #print(f"Error getting default value for {key}: {e}")
                            st.session_state[key] = None
                    else:
                        st.session_state[key] = None
                    equipped_chest.set_decoration(
                        st.selectbox(label=f"{slot_size}-slot decoration", 
                        options=decoration_options, 
                        #index = default_value, 
                        placeholder='Set a decoration', 
                        key=key),
                        deco_db=decoration_data,
                        slot = f'Slot {i+1}')

    ############################################
    # Select Arms
    ############################################

    arms_options = [name for name,details in armor_data.items() if details.Type == 'Arms' and (details['Rank'] == st.session_state.user_armor_rank_setting)]
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
                    key = f'arms_deco_selector_{i+1}'
                    decoration_options = [name for name,details in decoration_data.items() if int(name[-1]) <= slot_size and details['Type'] == 'shield']
                    decoration_options = sorted(decoration_options, key=lambda x: (x[-1]), reverse=True)
                    if key in st.session_state:
                        try:
                            if int(st.session_state[key][-1]) > slot_size:
                                print(f"Invalid decoration size for {key}: {st.session_state[key]} > {slot_size}. Setting to None.")
                                st.session_state[key] = None
                            else:
                                print('valid decoration size')
                                st.session_state[key] = st.session_state[key]
                        except Exception as e:
                            #print(f"Error getting default value for {key}: {e}")
                            st.session_state[key] = None
                    else:
                        st.session_state[key] = None
                    equipped_arms.set_decoration(
                        st.selectbox(label=f"{slot_size}-slot decoration", 
                        options=decoration_options, 
                        #index = default_value, 
                        placeholder='Set a decoration', 
                        key=key),
                        deco_db=decoration_data,
                        slot = f'Slot {i+1}')
    ############################################
    # Select Waist
    ############################################

    waist_options = [name for name,details in armor_data.items() if details.Type == 'Waist' and (details['Rank'] == st.session_state.user_armor_rank_setting)]
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
                    key = f'waist_deco_selector_{i+1}'
                    decoration_options = [name for name,details in decoration_data.items() if int(name[-1]) <= slot_size and details['Type'] == 'shield']
                    decoration_options = sorted(decoration_options, key=lambda x: (x[-1]), reverse=True)
                    if key in st.session_state:
                        try:
                            if int(st.session_state[key][-1]) > slot_size:
                                print(f"Invalid decoration size for {key}: {st.session_state[key]} > {slot_size}. Setting to None.")
                                st.session_state[key] = None
                            else:
                                print('valid decoration size')
                                st.session_state[key] = st.session_state[key]
                        except Exception as e:
                            #print(f"Error getting default value for {key}: {e}")
                            st.session_state[key] = None
                    else:
                        st.session_state[key] = None
                    equipped_waist.set_decoration(
                        st.selectbox(label=f"{slot_size}-slot decoration", 
                        options=decoration_options, 
                        #index = default_value, 
                        placeholder='Set a decoration', 
                        key=key),
                        deco_db=decoration_data,
                        slot = f'Slot {i+1}')

    ############################################
    # Select Legs
    ############################################

    legs_options = [name for name,details in armor_data.items() if details.Type == 'Legs' and (details['Rank'] == st.session_state.user_armor_rank_setting)]
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
                    key = f'legs_deco_selector_{i+1}'
                    decoration_options = [name for name,details in decoration_data.items() if int(name[-1]) <= slot_size and details['Type'] == 'shield']
                    decoration_options = sorted(decoration_options, key=lambda x: (x[-1]), reverse=True)
                    if key in st.session_state:
                        try:
                            if int(st.session_state[key][-1]) > slot_size:
                                print(f"Invalid decoration size for {key}: {st.session_state[key]} > {slot_size}. Setting to None.")
                                st.session_state[key] = None
                            else:
                                print('valid decoration size')
                                st.session_state[key] = st.session_state[key]
                        except Exception as e:
                            #print(f"Error getting default value for {key}: {e}")
                            st.session_state[key] = None
                    else:
                        st.session_state[key] = None
                    equipped_legs.set_decoration(
                        st.selectbox(label=f"{slot_size}-slot decoration", 
                        options=decoration_options, 
                        #index = default_value, 
                        placeholder='Set a decoration', 
                        key=key),
                        deco_db=decoration_data,
                        slot = f'Slot {i+1}')
                    
    ############################################
    # Select Charm
    ############################################
    charm_options = filter_charms(charm_db=charm_data, show_only_max_level=True, alphabetical_order=True)
    try:
        equipped_charm = monster_hunter_charm(st.selectbox(label = "Charm", options = charm_options, index = None, placeholder='Select a charm', key = 'charm_selector'), charm_db=charm_data)
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
        print(f"Error creating mixed set: {e}")
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
        
        with expander_col_2:
            with st.popover("Calculator Settings", use_container_width=True):
                st.write('placeholder')

        active_conditional_skills = st.pills("Conditional Skills", options=conditional_skills, selection_mode="multi", key='activeskillscontrol')
        active_skills = non_conditional_skills + active_conditional_skills


        # Kinsect Extract Buff Selector
        buff_mode = st.segmented_control(label = "Buffs", options = ["Triple Up", "Red Buff Only", 'No Buffs'],default=["Triple Up"], selection_mode='single', key='triple_up', label_visibility="collapsed")
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
            