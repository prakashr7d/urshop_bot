

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormAction
from userside import validate_pincode, get_shops, convert_category_name, client_type, user_update, get_items, set_items_and_return_quantity_type,get_quantity
from rasa_sdk.events import AllSlotsReset
from paymentrequest import create_payment_request
from paymentrequest import create_transanction
# TODO: to make the fuzzy wizzy in items selected and make it right
class UserForm(FormAction):

    def name(self) -> Text:
        return "user_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["pincode", "email"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:

        return []

class ActionGetName(FormAction):
    
    def name(self) -> Text:
        return "action_set_name"
    @staticmethod
    def run(
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        name = str((tracker.latest_message)['text'])

        return [SlotSet("name",name)]

class ActionGetAddress(FormAction):
    
    def name(self) -> Text:
        return "action_set_address"

    @staticmethod
    def run(
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        address = str((tracker.latest_message)['text'])

        return [SlotSet("address",address)]

class ActionValidationpincode(Action):
    def name(self) -> Text:
        return "action_validate_pincode"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        pincode = tracker.get_slot('pincode')
        result, city = validate_pincode(pincode)
        if (result != True):
            dispatcher.utter_message("We are not currently delivering in your area")
            return [AllSlotsReset(), SlotSet("status", "False")]
        else:
            name = tracker.get_slot('name')
            pincode = tracker.get_slot('pincode')
            email = tracker.get_slot('email')
            address = tracker.get_slot('address')
            phone_number = tracker.sender_id.split(':')[1]
            user_update(name, pincode, email, address, city, phone_number)
            result = "Welcome to urshop, you are successfully registered as urshop customer from {} \nUrshop menu \n. Place order\n. View past order\n. Support".format(city)
            dispatcher.utter_message(result)
        return [SlotSet("city", city), SlotSet("status","True"), SlotSet("phone_number", phone_number)]


class ActionDisplaycategory(Action):
    def name(self) -> Text:
        return "action_display_category"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        pincode = tracker.get_slot('pincode')
        city = tracker.get_slot('city')
        type = client_type(pincode)
        try:
            result = "Categories available in " + city + " are \n"
            for i in range(len(type)):
                cat = convert_category_name(type[i])
                result = result + "{}".format(i + 1) + ". " + cat + "\n"
            dispatcher.utter_message(result)
        except:
            dispatcher.utter_message("Shops not available in ", city)
        return []


class ActionDisplayStores(Action):
    def name(self) -> Text:
        return "action_display_stores"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        pincode = tracker.get_slot('pincode')
        type = tracker.get_slot('main_category')
        shops, match = get_shops(pincode, type)
        if match is False:
            dispatcher.utter_message("You have entered the shop that is not available!! or badly spelled the name of the shop")
            return [SlotSet("main_category", None)]
        else:
            city = tracker.get_slot('city')
            try:
                print(shops[0])
                result = "Categories available in " + city + " are \n"
                for i in range(len(shops)):
                    result = result + "{}".format(i + 1) + ". " + shops[i] + "\n"
                dispatcher.utter_message(result)
            except:
                dispatcher.utter_message("Shops not available in ", city)
        return [SlotSet("main_category", match)]


class ActionDisplayItems(Action):
    def name(self) -> Text:
        return "action_display_items"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        shop = tracker.get_slot('shop')
        pincode = tracker.get_slot('pincode')
        type = tracker.get_slot('main_category')
        item, match = get_items(shop, type, pincode)
        if item is False:
            return [SlotSet("shop", None), SlotSet("disp_items", item), SlotSet("main_category", None)]    
        else:
            return [SlotSet("shop", match), SlotSet("disp_items", item)]


class ActionGetItems(Action):
    def name(self) -> Text:
        return "action_get_items"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        shop = tracker.get_slot('shop')
        item = tracker.get_slot('item')
        pincode = tracker.get_slot('pincode')
        wrong_name, available_item, dict_quantity = set_items_and_return_quantity_type(item, shop, pincode)
        respond = "The wrong items selected(that is wrongly mispelled or not available) are:\n"

        for i in range(len(wrong_name)):
            respond =  respond + ". " + str(wrong_name[i]) + "\n"
        respond = respond + "Select the quantity type for the following items in this format(1kg,2lit,6kg):\n"

        for i in range(len(available_item)):
            repond = respond + ". " + str(available_item[i]) + "\n" 
        respond = respond + "This are the quantity types available '\' implies the other forms of the available item"

        for i in range(len(dict_quantity)):
            quantity = dict_quantity[i]
            identity = 0
            for i in range(len(quantity)):
                if identity == 0:
                    respond = respond + ". " + str(quantity[i])
                else:
                    respond = respond + "/" + str(quantity(i))
            respond = respond + "\n"

        dispatcher.utter_message(respond)
        return [SlotSet("items_stored", available_item)]


class ActionGetQuantity(Action):
    def name(self) -> Text:
        return "action_get_quantity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        shop = tracker.get_slot('shop')
        quantity = tracker.get_slot('quantity_type')
        items = tracker.get_slot('items_stored')
        quantity_num = tracker.get_slot('quantity')
        phone_number = tracker.get_slot("phone_number")
        total_price, price_list, quantity = get_quantity(quantity, shop, items, quantity_num, pincode)
        try:
            quantity_num = quantity_num.split(',')
            items = items.split(',')
        except:
            pass
        if total_price == price_list == quantity == False:
            dispatcher.utter_message('We experienced an error in our end!!!, we will try to rectify it. /n For assistance contact: url')
        else:
            statement = "Here is your CART!!! \n "
            for i in range(len(quantity)):
                quantity_num[i], price_list[i] = str(quantity_num[i]), str(price_list[i])
                statement = statement + items[i] + '(' + quantity[i] + ')' + "   " + quantity_num[i] + "unit" + "  ₹" + \
                            price_list[i] + "\-\n"
            dispatcher.utter_message(statement)
        return [SlotSet("quantity_type", quantity), SlotSet("price_list", price_list),
                SlotSet("total_price", total_price)]
get_user_id(phone_number):
    sql_update_querry = "select user_id"

class ActionAffirmYes(Action):
    def name(self) -> Text:
        return "action_affirm_yes"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        phone_number = tracker.get_slot("phone_number")
        total_price = tracker.get_slot("total_price")
        name = tracker.get_slot()
        if total_price is None:
            dispatcher.utter_message("oops!!!! you missed some steps type 'Hi' to start the conversation again")
        else:
            long_url = create_transanction(phone_number, total_price, name)

             
                

        return [SlotSet("menu", None), SlotSet("main_category", None), SlotSet("shop", None), SlotSet("item", None), SlotSet("quantity", None), SlotSet("quantity_stored", None), SlotSet("quantity_type", None), SlotSet("price_list", None), SlotSet("total_price", None), SlotSet("affirm", None)]


#TODO: to correct the name and address nlu
