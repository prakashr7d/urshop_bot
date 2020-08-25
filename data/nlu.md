## intent:greet
- hey
- hello
- hi
- hola
- hai

## intent:Name_collecting
- prakash
- Aryan
- dipesh sherashasta
- Mahaboob Shaik
- shalini
- shamruthi
- naveen
- lavanya
- chandra mouli
- darwin
- ezhil
- fizal
- janani
- gayatri
- harini
- ilakiya
- janani
- karthikeyan
- lavanya
- mano
- other
- prakash
- qantik
- ravi
- saravanan
- shamruthi
- shruthi
- thilak karthieyan
- udaya kumar
- vaishali 
- washim akaram
- xayala
- yamini
- zed

## intent:address_collection
- 6a bava street chidambaram
- 7/d race course street coimbatore
- 6 hopes college coimbatore
- 65 Hb block rathiyar nagar kanpur
- 6th cross race course kanpur
- 386 H2 block sarvar street kanpur
- 386 H2 block Kidwai Nagar Kanpur

## intent:email_collection
- [prakashr7d@gmail.com](email)
- [arwaanagarwal@gmail.com](email)
- [janagam.cdm@gmail.com](email)
- [naveenkumar@gmail.com](email)
- [notalang@userid.com](email)

## intent:pin_code
- [608001](pincode)
- [600500](pincode)
- [608000](pincode)

## intent:menu_selection
- [want to order]{"entity": "menu", "value": "place_order"}
- [order]{"entity": "menu", "value": "place_order"}
- [place_order](menu)
- [place order]{"entity": "menu", "value": "place_order"}
- [want to enquire]{"entity": "menu", "value": "view_past_order"}
- [view past order]{"entity": "menu", "value": "view_past_order"}
- [view_past_order](menu)
- [enquire_order]{"entity": "menu", "value": "view_past_order"}
- [want your support]{"entity": "menu", "value": "support"}
- [support](menu)
- [place order]{"entity": "menu", "value": "place_order"}\

## intent:main_category_selection
- [Grocery](main_category)
- [Food](main_category)
- [Diary](main_category)
- [food](main_category)
- [food](main_category)

## intent:shop_selection
- [nmc](shop) store
- [janagam](shop) store
- [nmc](shop) store

## intent:item_selection
- [Rice,sugar,milk](item)
- [rice,sugar,milk,sugar](item)
- [rice](item)
- [rice,milk](item)
- [milk,rice](item)

## intent:quantity_selection
- [1kg,2grm,1kg](quantity_type)
- [1 kg](quantity_type)
- [500 grm](quantity_type)
- [1000 grm](quantity_type)
- [1lit,2kg](quantity_type)
- [2kg,1lit](quantity_type)
- [1 lit, 2kg](quantity_type)

## intent:quantity
- [1,2,4,5,1](quantity)
- [2](quantity)
- [3](quantity)
- [4](quantity)
- [608001](pincode)
- [2,4](quantity)
- [608001](pincode)
- [2,4](quantity)

## intent:ask_affirm
- [yes](affirm)
- [no](affirm)
- [yes](affirm)

## intent:good_bye
- bye
- see you again

## synonym:place_order
- want to order
- order
- place order

## synonym:support
- want your support

## synonym:view_past_order
- want to enquire
- view past order
- enquire_orde
## lookup:email
  D:\projects\urshop\urshop bot\lookups\emails.txt
## lookup:pincode
  D:\projects\urshop\urshop bot\lookups\pincode.txt
## regex:email
- ^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$

## regex:pincode
- [0-9]{6}