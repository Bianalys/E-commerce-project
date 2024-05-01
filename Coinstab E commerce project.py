#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[3]:


order=pd.read_excel('Company X - Order Report.xlsx')
pincode=pd.read_excel('Company X - Pincode Zones.xlsx')
invoice=pd.read_excel('Courier Company - Invoice.xlsx')
rates=pd.read_excel('Courier Company - Rates.xlsx')
productid=pd.read_excel('Company X - SKU Master.xlsx')


# In[4]:


pwd

order.tail()
# In[5]:


order.tail()


# In[6]:


order.describe()


# In[7]:


rates.head(5)


# In[8]:


productid.drop_duplicates(inplace=True)


# In[9]:


order.drop_duplicates(inplace=True)
pincode.drop_duplicates(inplace=True)
rates.drop_duplicates(inplace=True)
invoice.drop_duplicates(inplace=True)


# In[10]:


order.shape
productid.shape


# In[11]:


invoice.shape


# In[12]:


pd.merge(productid,order,on="SKU",how="inner")


# In[14]:


#rates["Zone"]==rates["Zone"].str.lower()
rates[Zone]=rates[Zone.astype(str)]


# In[15]:


rates.head(1)


# In[16]:


comp=pd.merge(
    pd.merge(
        invoice,pd.merge(
            pincode,rates,on="Zone",how="inner"),
        on="Customer Pincode",how="inner"),
    pd.merge(
        productid,order,on="SKU",how = "inner"),
    left_on="Order ID",right_on="ExternOrderNo",how="inner")


# In[17]:


comp.describe()


# In[18]:


comp['Actual Weight(kg)']=(comp['Weight (g)']*comp['Order Qty']/1000)


# In[19]:


comp


# In[20]:


AWb_data=comp.groupby('AWB Code').agg({'Order ID':'first','Charged Weight':'first',
                              'Warehouse Pincode_x':'first','Customer Pincode':'first',
                              'Type of Shipment':'first','Billing Amount (Rs.)':'first',
                              'Zone_y':'first','Weight Slabs':'first','Forward Fixed Charge':'first',
                              'Forward Additional Weight Slab Charge':'first','RTO Fixed Charge':'first',
                              'RTO Additional Weight Slab Charge':'first','SKU':'count','Order Qty':'sum',
                              'Actual Weight(kg)':'sum'})


# In[21]:


AWb_data.head(1)


# In[22]:


AWb_data['Slab_count']=np.ceil(AWb_data['Actual Weight(kg)']/AWb_data['Weight Slabs'])


# In[23]:


AWb_data.head(5)


# In[24]:


def actual_price(x):
    if x["Type of Shipment"]=="Forward charges":
        return x["Slab_count"]*x["Forward Additional Weight Slab Charge"]+x["Forward Fixed Charge"]
    elif x["Type of Shipment"]=="Forward and RTO charges" :
        return (x["Slab_count"]*x["Forward Additional Weight Slab Charge"]+x["Forward Fixed Charge"]
               )+(x["Slab_count"]*x["RTO Additional Weight Slab Charge"]+x["RTO Fixed Charge"])
    else:
        return "Error"


# In[25]:


AWb_data.head(1)


# In[26]:


AWb_data["Actual_Price"]=AWb_data.apply(lambda x: actual_price(x),axis=1)


# In[27]:


AWb_data["Acutal vs invoice"]= AWb_data["Actual_Price"]-AWb_data["Billing Amount (Rs.)"]


# In[28]:


AWb_data["Actual vs invoice"]=AWb_data["Acutal vs invoice"].astype(int)


# In[29]:


def finds(x):
    if x["Actual vs invoice"]<0:
        return "under charged"
    elif x["Actual vs invoice"]==0:
        return "correctly charged"
    else:
        return "over charged"


# In[30]:


AWb_data.head(5)


# In[31]:


AWb_data = AWb_data.drop('Acutal vs invoice', axis=1)


# In[32]:


AWb_data["Status"] = AWb_data.apply(lambda x: finds(x),axis=1)


# In[33]:


AWb_data.head(5)


# In[34]:


AWb_data.groupby("Status").agg({"Order ID":"count","Actual vs invoice":"sum"})


# In[35]:


AWb_data.groupby("Status").agg({"Order ID":"count","Actual vs invoice":"sum"}).values[1:2,1:2][0]


# In[36]:


int(list(AWb_data.groupby("Status").agg({"Order ID":"count","Actual vs invoice":"sum"}).values[1:2,1:2])[0])


# In[37]:


int(list(AWb_data.groupby("Status").agg({"Order ID":"count","Actual vs invoice":"sum"}).values[2:3,1:2])[0])


# In[38]:


per_order=int(list(AWb_data.groupby("Status").agg({"Order ID":"count","Actual vs invoice":"sum"}).values[1:2,1:2])[0])/int(list(AWb_data.groupby("Status").agg({"Order ID":"count","Actual vs invoice":"sum"}).values[2:3,1:2])[0])


# In[39]:


per_order


# In[40]:


3663/920


# In[ ]:




