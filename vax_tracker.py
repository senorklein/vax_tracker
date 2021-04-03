#!/usr/bin/python3

import requests
import argparse


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
    






def main():
        parser = argparse.ArgumentParser( description='Check for available vaccine appointments using vaccinespotter.org API' , formatter_class=argparse.RawTextHelpFormatter )
        parser.add_argument( '-s' , '--state-code' , help='Specify the state code of the JSON from https://www.vaccinespotter.org/api/ ( default: CA )' , default="CA" )
        parser.add_argument( '-z' , '--zip-code' , help='Specify the zip code to search within )' , default="95125" )
        parser.add_argument( '-d' , '--distance-radius' , help='Specify the distance radius to pick which zips file)' , default="30" )
        args = parser.parse_args()
        data = get_data(args.state_code)
        filtered = filter_results(data, args.zip_code, args.distance_radius)
        for f in filtered:
            appointment_count = len(f["appointments"])
            print(f"{f['city']} : {f['state']} : {f['address']} : {f['postal_code']} : {f['name']} : {appointment_count} appts : {f['url']}" )
            

if __name__ == "__main__":
    # execute only if run as a script
    main()
