./clean.sh
python3 setup.py build_ext --inplace
mv src/datasets/CDictDataset* .
mv src/datasets/CListDataset* .
mv src/datasets/CFlight* .
rm -rf src/datasets
rm -rf build
rm -rf CDictDataset.c
rm -rf CListDataset.c
rm -rf CFlight.c
