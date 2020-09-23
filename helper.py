import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from io import BytesIO
import base64

def load_data():
    # Read data
    insurance = pd.read_csv('data/autoinsurance.csv')
    
    return(insurance)


def plot_age(data):
    
    # ---- Age group of customer

    def age_grouping(data):
        if(data.age <= 24):
            return '19 - 24'
        elif(data.age > 24 and data.age <= 30) : 
            return '24 - 30'
        elif(data.age > 30 and data.age <= 35) : 
            return '31 - 35'
        elif(data.age > 35 and data.age <= 40) : 
            return '36 - 40'
        elif(data.age > 40 and data.age <= 45) : 
            return '41 - 45'
        elif(data.age > 45 and data.age <= 50) : 
            return '46 - 50'
        elif(data.age > 50 and data.age <= 55) : 
            return '51 - 55'
        elif(data.age > 55 and data.age <= 59) : 
            return '56 - 59'
        else : 
            return '60+'

    data['age group'] = data.apply(age_grouping,axis = 1)

    fraud_data = data[data['fraud_reported'] == 'Y']
    age_profile = pd.crosstab(index=fraud_data['age group'],columns='count')

    ax = age_profile.plot.barh(title = "Fraud Reported by Age group", 
    legend= False, 
    color = '#c34454', 
    figsize = (8,6))
    
    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png', transparent=True)
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_premium(data):

    def tocolor(data):
        if(data.fraud_reported == 'Y'):
            return '#53a4b1'
        else : 
            return '#c34454'
    
    data.fcolor = data.apply(tocolor,axis=1)
    
    # ---- Months as Customer per Policy Annual Premium

    ax = data.plot.scatter(x= 'months_as_customer', 
                       y = 'policy_annual_premium', 
                       c=data.fcolor,title = "Months as Customer per Policy Annual Premium",
                       figsize=(8, 6))


    # Plot Configuration
    lab_y = mpatches.Patch(color='#53a4b1', label='Y')
    lab_n = mpatches.Patch(color='#c34454', label='N')
    plt.legend(handles = [lab_y ,lab_n])
    plt.xlabel("Months as Customer")
    plt.ylabel("Policy Annual Premium")

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)



def plot_incident(data):

    def tonum(data):
        if(data.fraud_reported == 'Y'):
            return 1
        else : 
            return 0
    
    data['fnum'] = data.apply(tonum,axis=1)

    timeseries = data.pivot_table(
                index='incident_date',
                values='fnum',
                aggfunc='count').ffill()

    # ---- Number of Report per Day

    ax = timeseries.plot(legend=False, title = "Number of Fraud per Day",color='#c34454', figsize=(8, 6))

    # Plot Configuration
    plt.xlabel('incident_date')

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_report(data):

    df_fraud = data[data.fraud_reported == 'Y'].pivot_table(index='police_report_available',values='fraud_reported',aggfunc='count')
    
    df_nfraud = data[data.fraud_reported == 'N'].pivot_table(index='police_report_available', values='fraud_reported',aggfunc='count')

    # ---- Police Report Availability

    ax = pd.concat([df_fraud,df_nfraud],axis=1).plot.bar(stacked = True,color =['#c34454','#53a4b1'],title = "Police Report Availability", figsize=(8, 6))
    
    # Plot Configuration
    plt.legend(['fraud','not fraud'], bbox_to_anchor=(1, 1))
    plt.xlabel("police report available'")

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_witness(data):

    wit_fraud = data[data.fraud_reported == 'Y'].pivot_table(index='witnesses',values='fraud_reported',aggfunc='count')
    
    wit_nfraud = data[data.fraud_reported == 'N'].pivot_table(index='witnesses', values='fraud_reported',aggfunc='count')

    # ---- Witnesses Availability

    wit = pd.concat([wit_fraud,wit_nfraud],axis=1).plot.bar(stacked = True,color =['#FF5722','#66BB6A'],title = "Witnesses Availability", figsize=(8, 6))
    
    # Plot Configuration
    plt.legend(['fraud','not fraud'], bbox_to_anchor=(1, 1))
    plt.xlabel("Number of Witnesses")

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_city(data):

    city_claim = data.groupby(['incident_date','incident_city']).agg({'total_claim_amount': 'sum'})

    # ---- Claim Amount by Incident City

    city = city_claim.boxplot(column = 'total_claim_amount', by='incident_city')
    
    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_severity(data):

    ss_male = data[data.insured_sex == 'MALE'].pivot_table(index='incident_severity',values='insured_sex',aggfunc='count')
    
    ss_female = data[data.insured_sex == 'FEMALE'].pivot_table(index='incident_severity',values='insured_sex',aggfunc='count')

    # ---- Incident Severity Based on Insured Sex

    sev = pd.concat([ss_male,ss_female],axis=1).plot.bar(stacked = True,color =['#64B5F6','#F06292'],title = "Incident Severity Based on Insured Sex", figsize=(8, 6))
    
    # Plot Configuration
    plt.legend(['MALE','FEMALE'], bbox_to_anchor=(1, 1))
    plt.xlabel("Insured Sex")

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)