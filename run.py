import os
import sys
import subprocess
from pathlib import Path
import shutil
from src import pipeline

maf = .1
geno = .1
mind = .1
fn = filtered_name = 'filtered'
cur_dir = Path('.')
data_Path = Path('data/')
staging_Path = Path('data/staging')
test_file_dir = Path('test')
pipeline_vcf_dir = Path('data/pipeline/vcf')

if not data_Path.isdir():
    data_path.mkdir()

def clear_staging_area():
    for P in staging_Path.iterdir():
        P.unlink()

def stage(Paths):
    for Path in Paths:
        shutil.copy(str(Path), str(staging_Path))

def process(Paths):
    clear_staging_area()
    stage(Paths)

    os.chdir(str(staging_Path))
    print("Concatenating VCFs...")
    names = [Path.name for Path in Paths]
    subprocess.call(['bcftools', 'concat', *names, '>', 'concatenated'])
    print("%s files concatenated" % len(Paths))
    print("Filtering file...")
    subprocess.call(['plink2', '--vcf', 'concatenated', '--make-bed',
                     '--snps-only', '--maf', str(maf), '--geno', str(geno),
                     '--mind', str(mind), '--out', fn])
    print('Done filtering')
    print('Running PCA')
    subprocess.call(['plink2', '--bed', fn+'.bed', '--bim', fn+'.bim',
                     '--fam', fn+'.fam', '--pca', '2', '--out', 'fin'])
    os.chdir(str(cur_dir))


def main(argv):
    if argv[0] == 'test-project':
        test_file_Paths = [Path for Path in test_file_dir.iterdir()]
        process(test_file_Paths)
    else:
        pipeline.start()
        file_Paths = [Path for Path in pipeline_vcf_dir.iterdir()]
        process(file_Paths)


if __name__ == '__main__':
    main(sys.argv[1:])
