import ConfigParser
import sys
import os
import glob
import inspect
import logging

FORMAT = '%(asctime)-15s [%(levelname)s] %(message)s'

def main():
    try:
        config = ConfigParser.ConfigParser()
        config.readfp(open('aws_inventory.ini'))
        output_folder = config.get('General', 'site_root')
        module_dir = config.get('General', 'module_dir')
        log_file = config.get('General', 'log_file')
        sections = config.sections()
        aws_credentials = []
        for section in sections:
            if section.startswith('AWS'):
                aws_key = config.get(section, 'aws_key')
                aws_secret = config.get(section, 'aws_secret')
                aws_account_name = config.get(section, 'aws_account_name')
                aws_credentials.append((aws_key, aws_secret, aws_account_name))
    except:
        print 'Invalid config file.'
        exit(0)
    logging.basicConfig(filename=log_file, level=logging.INFO, format=FORMAT)
    Items = {}
    data = {}
    logging.info('Locating data modules')
    module_list = glob.glob(''.join([module_dir, os.sep, 'data_*.py']))
    sys.path.append(module_dir)
    dataPriority = [i for i in range(len(module_list))]
    logging.info('Importing modules')
    for module in module_list:
        mod = __import__(module.split(os.sep)[-1].split('.')[0])
        inst = mod.data(aws_credentials, Items)
        inst.skipRegions = ['cn-north-1','us-gov-west-1']
        data[inst.Name] = inst
        dataPriority[inst.Priority] = inst.Name
    dataNames = data.keys()
    for name in dataPriority:
        logging.info("Geting data for %s" % name)
        Items[name] = data[name].getData()
    logging.info("Updating data")
    for name in dataPriority:
        members = inspect.getmembers(data[name])
        for member in members:
            if member[0] == 'updateItems':
                member[1](Items)
    renders = []
    module_list = glob.glob(''.join([module_dir,os.sep,'render_*.py']))
    logging.info('Starting output')
    for module in module_list:
        mod = __import__(module.split(os.sep)[-1].split('.')[0])
        renders.append(mod.render(output_folder, [ item[2] for item in aws_credentials ], [ item for item in dataPriority if data[item].show ]))
    for render in renders:
        logging.info("Rendering %s" % render.Name)
        for dataProvider in dataPriority:
            if data[dataProvider].show:
                render.configPage(dataProvider, data[dataProvider].HeaderNames, data[dataProvider].HeaderWidths, data[dataProvider].HeaderKeys, Items[dataProvider])
        render.render()

if __name__ == '__main__':
    main()
