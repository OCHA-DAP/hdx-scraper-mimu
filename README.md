### Collector for MIMU's Datasets
[![Build Status](https://travis-ci.org/OCHA-DAP/hdxscraper-mimu.svg?branch=master&ts=1)](https://travis-ci.org/OCHA-DAP/hdxscraper-mimu) [![Coverage Status](https://coveralls.io/repos/github/OCHA-DAP/hdxscraper-mimu/badge.svg?branch=master&ts=1)](https://coveralls.io/github/OCHA-DAP/hdxscraper-mimu?branch=master)

Collector designed to collect MIMU datasets from the [MIMU](http://) website and to automatically register datasets on the [Humanitarian Data Exchange](http://data.humdata.org/) project.

### Usage
python run.py

For the script to run, you will need to have a file called .hdx_configuration.yml in your home directory containing your HDX key eg.

    hdx_key: "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
    hdx_read_only: false
    hdx_site: prod
    
 You will also need to supply the universal .useragents.yml file in your home directory as specified in the parameter *user_agent_config_yaml* passed to facade in run.py. The collector reads the key **hdx-scraper-ucdp** as specified in the parameter *user_agent_lookup*.
 
 Alternatively, you can set up environment variables: USER_AGENT, HDX_KEY, HDX_SITE, TEMP_DIR, LOG_FILE_ONLY