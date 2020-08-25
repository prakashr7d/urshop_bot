## new_customer path_1
* greet
  - utter_greet
  - user_form
  - form{"name":"user_form"}
  - form{"name": null}
  - utter_ask_name
* name_collection
  - action_set_name
  - utter_ask_address
* addresss_collection
  - action_set_address
  - utter_submit
  - action_validate_pincode
  - slot{"status":"True"}
* menu_selection
## new_customer path_2
* greet
  - utter_greet
  - user_form
  - form{"name":"user_form"}
   - utter_ask_name
* name_collection
  - action_set_name
  - utter_ask_address
* addresss_collection
  - action_set_address
  - utter_submit
  - action_validate_pincode
  - slot{"status":"False"}
* menu_selection
  
## main_part
* menu_selection
  - slot{"menu":"place_order"}
  - action_display_category
* main_category_selection
  - action_display_stores
* shop_selection
  - action_display_items
  - utter_display_items
* item_selection
  - action_get_items
* quantity_selection
  - utter_ask_number
* quantity
  - action_get_quantity
  - utter_show_price
* ask_affirm
  - slot{"affirm":"yes"}
  - action_affirm_yes
* good_bye
  - utter_good_bye
## shop_bug
* greet
  - utter_greet
  - user_form
  - form{"name":"user_form"}
  - form{"name": null}
  - utter_ask_name
* shop_selction
  - action_set_name
  - utter_ask_address
* addresss_collection
  - action_set_address
  - utter_submit
  - action_validate_pincode
  - slot{"status":"True"}
* menu_selection
## name
* name_collection
  - action_set_name
  - utter_ask_address
* addresss_collection
  - action_set_address
  - utter_submit
  - action_validate_pincode
  - slot{"status":"True"}
* menu_selection

## address 
* addresss_collection
  - action_set_address
  - utter_submit
  - action_validate_pincode
  - slot{"status":"True"}
* menu_selection

## New Story

* greet
    - utter_greet
    - user_form
    - form{"name":"user_form"}
    - slot{"requested_slot":"pincode"}
    - slot{"pincode":"608001"}
* quantity{"pincode":"608001"}
    - slot{"pincode":"608001"}
    - user_form
    - slot{"pincode":"608001"}
    - slot{"email":"prakashr7d@gmail.com"}
* email_collection{"email":"prakashr7d@gmail.com"}
    - slot{"email":"prakashr7d@gmail.com"}
    - user_form
    - form{"name":null}
    - slot{"email":"prakashr7d@gmail.com"}
    - utter_ask_name
* Name_collecting
    - action_set_name
    - slot{"name":"naveen"}
    - utter_ask_address
* address_collection
    - action_set_address
    - slot{"address":"6th block rajaraman street, chidambaram"}
    - utter_submit
    - action_validate_pincode
    - slot{"city":"Chidambaram"}
* menu_selection{"menu":"place  order"}
    - slot{"menu":"place  order"}
    - action_display_category
    - slot{"client_type":["dairy","food"]}
* main_category_selection{"main_category":"food"}
    - slot{"main_category":"food"}
    - action_display_stores
    - slot{"main_category":"food"}
* shop_selection{"shop":"nmc"}
    - slot{"shop":"nmc"}
    - action_display_items
    - slot{"shop":"nmc"}
    - utter_display_items
    - slot{"item":"milk,rice"}
* item_selection{"item":"milk,rice"}
    - action_get_items
    - slot{"items_stored":"milk,rice"}
    - slot{"quantity_type":"1 lit, 2kg"}
* quantity_selection{"quantity_type":"1 lit, 2kg"}
    - utter_ask_number
    - slot{"quantity":"1,2"}
* quantity{"quantity":"1,2"}
    - action_get_quantity
    - slot{"quantity_type":["1 lit ","2 kg"]}
    - utter_show_price
    - slot{"affirm":"yes"}
* ask_affirm{"affirm":"yes"}
    - action_affirm_yes
    - slot{"menu":null}
    - action_payment_part

  