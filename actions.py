from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormAction
from userside import validate_pincode, get_shops, get_category, user_update, get_items, set_items_and_return_quantity,get_quantity
from rasa_sdk.events import AllSlotsReset

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

class ActionGetName(FormAction):
    
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
            address = tracker.sender_id
            user_update(name, pincode, email, address, city)
            result = "Welcome to urshop, you are successfully registered as urshop customer from {} \nUrshop menu \n. Place order\n. View past order\n. Support".format(city)
            dispatcher.utter_message(result)
        return [SlotSet("address", address), SlotSet("status","True")]


class ActionDisplaycategory(Action):
    def name(self) -> Text:
        return "action_display_category"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        pincode = tracker.get_slot('pincode')
        city = tracker.get_slot('city')
        type = get_category(pincode)
        try:
            result = "Categories available in " + city + " are \n"
            for i in range(len(type)):
                result = result + "{}".format(i + 1) + ". " + type[i] + "\n"
            dispatcher.utter_message(result)
        except:
            dispatcher.utter_message("Shops not available in ", city)
        return [SlotSet("client_type", type)]


class ActionDisplayStores(Action):
    def name(self) -> Text:
        return "action_display_stores"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        pincode = tracker.get_slot('pincode')
        type = tracker.get_slot('main_category')
        shops, match = get_shops(pincode, type)
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
        item, match = get_items(shop, pincode)
        if item is None:
            dispatcher.utter_message("Items not available in ", match)
        
        return [SlotSet("shop", match), SlotSet("disp_items", item)]


class ActionGetItems(Action):
    def name(self) -> Text:
        return "action_get_items"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        shop = tracker.get_slot('shop')
        item = tracker.get_slot('item')
        items, quantity = set_items_and_return_quantity(item, shop)
        item = ""
        for i in range(len(items)):
            if i == 0:
                item = item + items[i]
            else:
                item = item + ',' + items[i]
        statement = "Select the type of quantities needed: \n"
        j = 0
        for single in items:
            if j == 0:
                quan = quantity[single]
                j = 1
            else:
                quan = quantity[single]
                statement = statement + ","
            for i in range(len(quan)):
                if i == 0:
                    statement = statement + str(quan[i])
                else:
                    statement = statement + "\\" + str(quan[i])

        dispatcher.utter_message(statement)
        return [SlotSet("items_stored", item)]


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
        total_price, price_list, quantity = get_quantity(quantity, shop, items, quantity_num)
        try:
            quantity_num = quantity_num.split(',')
            items = items.split(',')
        except:
            pass
        if total_price == price_list == quantity == False:
            dispatcher.utter_message('your entries are wrong')
        else:
            statement = "Here is your CART!!! \n "
            for i in range(len(quantity)):
                quantity_num[i], price_list[i] = str(quantity_num[i]), str(price_list[i])
                statement = statement + items[i] + '(' + quantity[i] + ')' + "   " + quantity_num[i] + "unit" + "  " + \
                            price_list[i] + "\-\n"

            dispatcher.utter_message(statement)
        return [SlotSet("quantity_type", quantity), SlotSet("price_list", price_list),
                SlotSet("total_price", total_price)]


class ActionAffirmYes(Action):
    def name(self) -> Text:
        return "action_affirm_yes"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        total_price = tracker.get_slot("total_price")
        if total_price is None:
            dispatcher.utter_message("oops!!!! you missed some steps type 'Hi' to start the conversation again")
        else:
            dispatcher.utter_message("your order is being confirmed.... will get delivery soon")
        return [SlotSet("menu", None), SlotSet("main_category", None), SlotSet("shop", None), SlotSet("item", None), SlotSet("quantity", None), SlotSet("quantity_stored", None), SlotSet("quantity_type", None), SlotSet("price_list", None), SlotSet("total_price", None), SlotSet("affirm", None)]


#TODO: to correct the name and address nlu
