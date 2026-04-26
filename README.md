# SiT to SocNav3 Converter
 
A tool that converts SiT dataset sequences into the SocNav3 JSON format for social navigation benchmarking.
 
## What it does
 
Takes raw SiT dataset folders (pedestrian annotations + robot trajectories) and outputs structured JSON files compatible with the SocNav3 evaluation tools.
 
## Setup
 
```
pip install -r requirements.txt
```
 
## Usage
 
```
python main.py --input path/to/SiT/sequence --output output/filename.json
```
 
## Example
 
```
python main.py --input data/Cafeteria_1 --output test_output/cafeteria_1.json
```
 
## Running tests
 
```
pytest test_tools/test_dataLoader.py -v
```
 
## Speed comparison
 
To compare average trajectory speeds against original SocNav3 data:
 
1. Put original SocNav3 JSON files in a folder called `socnav3_traj/`
2. Put converted files in `test_output/`
3. Run:
```
python test_tools\speed_comparison.py
```
 
This generates a `speed_comparison.png` plot.
 
## Visualisation
 
To visualise the converted output, use the official SocNav3 visualisation tool:
https://github.com/SocNavData/SocNavData2026

## Project structure
 
```
sit-to-socnav3-converter/
├── modules/
│   ├── loadData.py          - Loads SiT sequences
│   ├── preprocess.py        - Cleans trajectories, computes velocities
│   ├── export.py            - Exports to SocNav3 JSON
│   └── wallExtraction.py    - LiDAR wall extraction (experimental)
├── test_tools/
│   └── test_dataLoader.py   - Unit tests for data loading
├── test_output/             - Converted JSON files
├── main.py                  - Command line interface
├── speed_comparison.py      - Speed analysis script
├── requirements.txt
└── README.md
```
 
## Dependencies
 
- Python 3.8+
- NumPy
- pytest (for testing)
- pypcd4(experimental, refer to wallExtraction.py)
- matplotlib (for speed comparison)