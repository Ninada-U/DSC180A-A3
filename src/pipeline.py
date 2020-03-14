import numpy as np
import pandas as pd
import urllib.request
import os
import json
import doctest
from HelperFunctions import get_bytes
from pathlib import Path
from hurry.filesize import size as filesize
import sys, urllib


def check_dir(dir):
    if not os.path.isdir("./data/pipeline/%s" % dir):
        os.mkdir("data/pipeline/%s" % dir)


def skipped(df, config):
    if 'index' in config:  # skip to index
        return df.iloc[config['index']:]
    return df


VCF_FILEPATH = "http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/"


def reporthook(a, b, c):
    print("% 3.1f%% of %s\r" % (min(100, float(a * b) / c * 100), filesize(c)))
    sys.stdout.flush()


def download_url(url):
    url = url.replace("ftp:/ftp", "ftp://ftp")
    if '.gz' not in url and '.cram' not in url:
        return
    i = url.rfind('/')
    file = 'data/pipeline/vcf/' + url[i + 1:]
    print(url)
    urllib.request.urlretrieve(url, file, reporthook)


def download_variant(config):
    print('vcf')
    check_dir('vcf')
    df = pd.read_html(VCF_FILEPATH, skiprows=3)[0].iloc[:, [1, 3]]
    df.columns = ['path', 'size']
    df = df[df['path'].apply(lambda x: type(x) == str and '.gz' in x)]

    df = skipped(df, config)
    print("%d files, %s" % (len(df), filesize(np.sum(df['size'].apply(get_bytes)))))

    for url in df['path']:
        download_url(VCF_FILEPATH + url)


def start():
    with open("../config/config.json", "r") as f:
        doctest.testmod()
        config = json.load(f)

    if 'vcf' in config:
        download_variant(config)

    if 'fastq' in config:
        print('retrieving fastq data')
        check_dir('fastq')
        df = pd.read_csv("src/reqs/sequence.index", header=None, skiprows=29, usecols=[0, 2, 4, 10, 13, 20, 23, 25],
                         sep='\t', error_bad_lines=False)
        df.columns = ['path', 'run id', 'study name', 'population', 'instrument model', 'withdrawn',
                      'read count', 'analysis group']

        for setting in config['fastq']:
            df = df[df[setting] == config['fastq'][setting]]

        df.reset_index(drop=True, inplace=True)

        df = skipped(df, config)
        Gbs = round(sum(df['read count'].unique().astype(np.int64)) / 1.2e7, 2)
        print("%s files to download totalling %sG" % (str(len(df)), Gbs))

        for i, row in df.iterrows():
            download_url(row['path'])

    if 'aligned' in config:
        paths = {
            'low coverage': "src/reqs/low_coverage.alignment.index",
            'high coverage': "src/reqs/high_coverage.alignment.index",
            'exome': "src/reqs/exome.alignment.index"
        }
        df = pd.read_csv(paths[config['aligned']['analysis group']], header=None, skiprows=9, usecols=[0],
                         sep='\t', error_bad_lines=False)
        df.columns = ['path']

        df = skipped(df, config)
        print("%s files to download." % len(df))

        check_dir('aligned')

        for i, row in df.iterrows():
            path = row['path']

            d = urllib.request.urlopen(path)
            print("%s: fetching %s, approximately %s" % (i, path, filesize(int(d.info()['Content-length']))))
            urllib.request.urlretrieve(path, "data/pipeline/aligned/" + Path(path).name)
