import urllib.request
import xml.etree.ElementTree as ET
import pandas as pd


def extract_xml(url):
    """
    Extracts data from an XML file hosted at the given URL and returns it as a Pandas DataFrame.

    Parameters:
    url (str): The URL of the XML file to be extracted.

    Returns:
    pd.DataFrame: A DataFrame containing the extracted data with columns 'Country', 'DATA_DOMAIN',
    'PublishDate', 'BASE_PER', 'Descriptor', 'INDICATOR', 'TIME_PERIOD', 'OBS_VALUE', and 'Link'.

    This function performs the following steps:
    1. Downloads XML data from the specified URL.
    2. Parses the XML data and registers namespaces.
    3. Extracts data from the XML, including attributes and elements.
    4. Creates lists to store the extracted data.
    5. Constructs a Pandas DataFrame from the extracted data.
    6. Converts date columns to datetime format.
    7. Maps indicator codes to their corresponding descriptors.
    8. Returns the resulting DataFrame.

    Note: The function assumes a specific structure and namespaces in the XML file.
    """

    response = urllib.request.urlopen(url)
    xml_data = response.read()

    # # Define namespaces
    namespaces = {
        'message': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message',
        'ns1': 'urn:sdmx:org.sdmx.infomodel.datastructure.DataStructure=IMF:ECOFIN_DSD(1.0):ObsLevelDim:TIME_PERIOD',
        'common': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        # Add more namespaces as needed
    }

    # Parse the XML data and register namespaces
    root = ET.fromstring(xml_data)

    # # Define a function to find elements with namespaces
    def find_element(namespace, tag):
        return root.find(".//{%(namespace)s}%(tag)s" % {'namespace': namespaces[namespace], 'tag': tag})

    # def find_elements(namespace, tag):
    #     return root.findall(".//{%(namespace)s}%(tag)s" % {'namespace': namespaces[namespace], 'tag': tag})

    header = find_element('message', 'Prepared').text.split('T')[0]

    # # Example: Extract the COMMENT attribute from the DataSet element
    dataset = find_element('message', 'DataSet')
    # comment = dataset.get('COMMENT')

    # print(f"Comment: {comment}")

    # Find all <Series> elements
    series_elements = dataset.findall(".//Series")
    # Now, you can iterate through the series_elements list to access each <Series> element
    # print(series_elements)

    # Create empty lists to store the data
    time_periods = []
    obs_values = []
    indicators = []
    domains = []
    base_pers = []
    PublishDate = []
    Country = []
    link = []
    source = []
    update_fq = []

    for series in series_elements:
        # Here, you can access and manipulate each <Series> element as needed
        # For example, you can extract attributes or child elements from each series.
        data_domain = series.get('DATA_DOMAIN')
        ref_area = series.get('REF_AREA')
        indicator = series.get('INDICATOR')
        base_per = series.get('BASE_PER')

        #     print(f"Series: Data Domain={data_domain}, Ref Area={ref_area}, Indicator={indicator}")

        # Iterate through <Obs> elements within the <Series>
        for obs_element in series.findall(".//Obs"):
            time_period = obs_element.get('TIME_PERIOD')
            obs_value = float(obs_element.get('OBS_VALUE'))

            indicators.append(indicator)
            domains.append(data_domain)
            base_pers.append(base_per)

            # Append data to lists
            time_periods.append(time_period)
            obs_values.append(obs_value)
            PublishDate.append(header)
            Country.append('Vietname')
            link.append('https://nsdp.gso.gov.vn/index.htm')
            source.append('GENERAL STATISTICS OFFICE')
            update_fq.append('Monthly')

    # Create a Pandas DataFrame from the extracted data
    data = {'Source': source, 'Update frequency': update_fq, 'Country': Country, 'DATA_DOMAIN': domains,
            'PublishDate': PublishDate, 'BASE_PER': base_pers, 'INDICATOR': indicators, 'TIME_PERIOD': time_periods,
            'OBS_VALUE': obs_values, 'Link': link}
    df = pd.DataFrame(data)

    # Convert the 'Date' column to datetime
    df['TIME_PERIOD'] = pd.to_datetime(df['TIME_PERIOD'], format='%Y-%m', errors='coerce')
    df['PublishDate'] = pd.to_datetime(df['PublishDate'], format='%Y-%m', errors='coerce')

    Descriptor = {'PCPI_IX': 'Consumer Price Index, Index ',
                  'PCPI_CP_01_IX': 'Food and Foodstuffs, Index ',
                  'PCPI_CP_011_IX': 'Food, Index ',
                  'VNM_PCPI_CP_011FS ': 'Foodstuffs, Weight ',
                  'PCPIFFA_IX': 'Food Consumption Outside Home, Index ',
                  'PCPI_CP_02_IX': 'Beverages and Cigarettes, Index ',
                  'PCPI_CP_03_IX': 'Garments, Footwear and Hats, Index ',
                  'PCPI_CP_04_IX': 'Housing and Material Construction including Electricity, Water and Fuel, Index ',
                  'PCPI_CP_05_IX': 'Household Equipment and Goods, Index ',
                  'PCPI_CP_06_IX': 'Medication and Health, Index ',
                  'VNM_PCPI_CP_062T063_IX': 'Of which: Health Care, Index',
                  'PCPI_CP_07_IX': 'Transport, Index ',
                  'PCPI_CP_08_IX': 'Postal Services and Telecommunication, Index ',
                  'PCPI_CP_10_IX': 'Education, Index ',
                  'VNM_PCPI_CP_102T105_IX': 'Of which: Educational Services, Index',
                  'PCPI_CP_09_IX': 'Culture, Entertainment and Tourism, Index',
                  'PCPI_CP_12_IX': 'Other Consumer Goods and Services, Index ',
                  'PCPI_WT': 'Consumer Price Weight, Weight ',
                  'PCPI_CP_01_WT': 'Food and Foodstuffs, Weight ',
                  'PCPI_CP_011_WT': 'Food, Weight ',
                  'VNM_PCPI_PCPIFFA_WT': 'Food Consumption Outside Home, Weight ',
                  'PCPI_CP_02_WT': 'Beverages and Cigarettes, Weight ',
                  'PCPI_CP_03_WT': 'Garments, Footwear and Hats, Weight ',
                  'PCPI_CP_04_WT': 'Housing and Material Construction including Electricity, Water and Fuel, Weight ',
                  'PCPI_CP_05_WT': 'Household Equipment and Goods, Weight ',
                  'PCPI_CP_06_WT': 'Medication and Health, Weight ',
                  'PCPI_CP_07_WT': 'Transport, Weight ',
                  'PCPI_CP_08_WT': 'Postal Services and Telecommunication, Weight ',
                  'PCPI_CP_10_WT': 'Education, Weight ',
                  'PCPI_CP_09_WT': 'Culture, Entertainment and Tourism, Weight',
                  'PCPI_CP_12_WT': 'Other Consumer Goods and Services, Weight ',
                  'PCPICO_BY_CP_A_PT': 'Core CPI ( Y/Y % Change)'}

    df['Descriptor'] = df['INDICATOR'].map(Descriptor)
    df = df[
        ['Country', 'DATA_DOMAIN', 'Source', 'Update frequency', 'PublishDate', 'BASE_PER', 'Descriptor', 'INDICATOR',
         'TIME_PERIOD', 'OBS_VALUE', 'Link']]

    # Print the DataFrame
    return df
