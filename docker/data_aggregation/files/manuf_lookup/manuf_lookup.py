from manuf import manuf
import pandas as pd

mac_parser=manuf.MacParser(manuf_name="manuf_lookup/manuf.txt", update=False)
company_id_csv=pd.read_csv("manuf_lookup/company_identifiers.csv")

def get_manuf_from_data(public_addr:bool, mac:str, manuf_data:str, service_uuid:str)->str:
    # if public MAC address derive vendor from MAC
    if public_addr:
        vendor=mac_parser.get_all(mac)
        if vendor.manuf_long:
            return vendor.manuf_long

    # random MAC address or no matching manufacturer

    if manuf_data:
        manuf_string=manuf_data[2:2+2]+manuf_data[0:2]
        manuf_decimal=int(manuf_string, 16)

        # match with list
        line=company_id_csv[company_id_csv['Decimal']==manuf_decimal]
        if not line.empty:
            company=line['Company']
            return company.item()

    # TODO: try to get manufacturer from serviceUUID
    if service_uuid:
        #do someting
        pass

    # if nothing found
    return "unknown"
