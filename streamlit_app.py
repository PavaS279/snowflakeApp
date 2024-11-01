# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(":cup_with_straw: Order Smoothie Form :cup_with_straw:")
st.write(
    """Choose the Fruits you want in your Smoothie!.
    """
)


customer_name = st.text_input('Name on Smoothie....')
# st.write(name_input)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)
pd_df =my_dataframe.to_pandas()
ingredients_list = st.multiselect(
    'Choose upto 5 ingredients: ',
    my_dataframe
    , max_selections=5
)

if ingredients_list:
    ingredients_string = ''
    
    for fruit_choosen in ingredients_list:
        ingredients_string += fruit_choosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        fruityvice_response = requests.get("https://webhook.site/f55f66ba-20fc-48bc-840a-f88f449d3dc7")
        # st.text(fruityvice_response.json())
       
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    
    # st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" +customer_name +"""')"""
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered '  + customer_name + '!...', icon="✅")




