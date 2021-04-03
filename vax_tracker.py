#!/usr/bin/python3

import requests
import argparse
import twilio_imp
import time
import pytz
from datetime import datetime

def get_data(state):
        raw_data = requests.get( 'https://www.vaccinespotter.org/api/v0/states/' + state + '.json' )
        data = raw_data.json()
        return data


def filter_results(data, zip, distance):
    radius_zip = load_zips(zip, distance)
    ret = []
    for d in data["features"]:
        p = d["properties"]
        if p["postal_code"] and str(p["postal_code"]) in str(radius_zip) and \
                p["appointments_available_all_doses"] and \
                len(p["appointments"]) > 0:
            ret.append(p)
    return ret

def load_zips(zip, distance):
    # zips are in the format from this website;
    # https://www.zipcodeapi.com/API#radius
    zfile = open(f"zips_{zip}_{distance}.txt", "+r")
    zfile_list = zfile.readlines()
    zips = []
    for z in zfile_list[1:]:
        sub_list = z.split(",")
        zips.append(sub_list[0])
    return zips
    



def do_stuff(args):
        data = get_data(args.state_code)
        filtered = filter_results(data, args.zip_code, args.distance_radius)
        text_report = []
        if len(filtered) == 0:
            print(f"no appointents found in {args.distance_radius} miles of {args.zip_code}")
            return
        for f in filtered:
            appointment_count = len(f["appointments"])
            print(f"{f['city']} : {f['state']} : {f['address']} : {f['postal_code']} : {f['name']} : {appointment_count} appts : {f['url']}" )
            msg = f"{appointment_count} | {f['city']} {f['name']} {f['postal_code']}"
            text_report.append(msg)
            
        if args.sms_phone_number != "" and len(text_report) > 0:
            print("sending results")
            twilio_imp.send_sms(args.sms_phone_number, "\n".join(text_report))





def main():
        parser = argparse.ArgumentParser( description='Check for available vaccine appointments using vaccinespotter.org API' , formatter_class=argparse.RawTextHelpFormatter )
        parser.add_argument( '-s' , '--state-code' , help='Specify the state code of the JSON from https://www.vaccinespotter.org/api/ ( default: CA )' , default="CA" )
        parser.add_argument( '-z' , '--zip-code' , help='Specify the zip code to search within )' , default="95125" )
        parser.add_argument( '-d' , '--distance-radius' , help='Specify the distance radius to pick which zips file)' , default="30" )
        parser.add_argument( '-n' , '--sms_phone_number' , help='Specify what phone number to sms the results to' , default="")
        parser.add_argument( '-server' , '--server' , help='start it as server and check every 1 minute' , action="store_true")
        args = parser.parse_args()
        if args.server:

            pst = pytz.timezone('America/Los_Angeles')
            print("starting as a server")
            while(1):
                print(f"checking {datetime.now(pst)}")
                do_stuff(args)
                time.sleep(60)
        else:
            do_stuff(args)


if __name__ == "__main__":
    # execute only if run as a script
    main()
