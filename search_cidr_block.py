import sys
import json
import datetime
import ipaddress
import configparser
import requests

def ask_for_cidr():
    ''' Ask for CIDR block until a valid CIDR block is provided
    '''
    while True:
        reply = str(input('Enter a CIDR block: ')).strip()
        validated = validate_cidr(reply)
        if validated:
            return validated

def validate_cidr(address):
    ''' Validate the provided input is a valid CIDR block
    '''
    try:
        network_object = ipaddress.ip_network(address, strict=False)
        return network_object
    except ValueError as error:
        print(error)
        return False

def write_output(container):
    ''' Write the output to output.json
    '''
    print('Writing results to output.json')
    with open('output.json', 'w') as file:
        file.write(json.dumps(container))

def main():
    ''' Main script logic
    '''
    # Specify the config file
    config_file = 'api.cfg'

    # Reading the config file to get settings
    config = configparser.RawConfigParser()
    config.read(config_file)
    client_id = config.get('AMPE', 'client_id')
    api_key = config.get('AMPE', 'api_key')

    # Creat session object
    # http://docs.python-requests.org/en/master/user/advanced/
    # Using a session object gains efficiency when making multiple requests
    amp_session = requests.Session()
    amp_session.auth = (client_id, api_key)

    # Containers for output
    query_output = {'total_hits':0,
                    'timestamp': str(datetime.datetime.now()),
                    'endpoints':{},
                    'ip_addresses_hits':[]}

    # Vreify that a valid CIDR block was provided otherwise ask for one
    try:
        address = validate_cidr(sys.argv[1])
        if not address:
            address = ask_for_cidr()
    except IndexError:
        address = ask_for_cidr()

    # Store the CIDR block for output
    query_output.setdefault('cidr_block', address.with_prefixlen)

    num_addresses = address.num_addresses

    if num_addresses > 3000:
        sys.exit('Number of IP addresses ({}) exceeds API rate limit of 3000'.format(num_addresses))

    if num_addresses is 1:
        hosts = [address.network_address]
    else:
        hosts = address.hosts()

    print('Querying {} IP addresses'.format(num_addresses))

    # Query the IP addresses in the CIDR block
    for ip_address in hosts:
        # Output the current IP address without creating a new line
        sys.stdout.write('\rSearching for {}'.format(ip_address))
        sys.stdout.flush()

        # URL for the computers endpoint
        activity_url = 'https://api.amp.cisco.com/v1/computers'

        # Parameters for the query
        parameters = {'internal_ip':ip_address}

        # Query the Computers API endpoint
        response = amp_session.get(activity_url, params=parameters)

        # Decoded JSON
        response_json = response.json()

        # Name the data object of the JSON
        data = response_json['data']

        # Name the total value
        total = response_json['metadata']['results']['total']

        # Update total hits
        query_output['total_hits'] += total

        # Print the number of computers that have seen the file
        if total > 0:
            if total == 1:
                print('\rFound {} host with {}'.format(total, ip_address))
            else:
                print('\rFound {} hosts with {}'.format(total, ip_address))

            # Store the IP for output
            query_output['ip_addresses_hits'].append(str(ip_address))

            # Parse computers from the JSON
            for computer in data:
                # Name the elements that will be saved
                hostname = computer['hostname']
                connector_guid = computer['connector_guid']
                last_seen = computer['last_seen']
                network_addresses = computer['network_addresses']

                # Store the elements in the computers dictionary
                query_output['endpoints'].setdefault(connector_guid, {'hostname':hostname,
                                                                      'last_seen':last_seen,
                                                                      'network_addresses':network_addresses})
    # Clear the last printed line
    sys.stdout.write('\x1b[2K')
    print('\rFinished!')

    print('Found {} GUIDs from {} IP Addresses'.format(len(query_output['endpoints']),
                                                       query_output['total_hits']))

    write_output(query_output)

if __name__ == '__main__':
    main()
