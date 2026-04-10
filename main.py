import argparse
import sys
from pathlib import Path

from modules.loadData import load_sit_dataset
from modules.preprocess import preprocess_trajectories
from modules.export import export_to_socnav3


def main():
    parser = argparse.ArgumentParser(description='Convert SiT dataset to SocNav3 format')
    
    parser.add_argument('--input', '-i', required=True,
                       help='Path to SiT sequence folder')
    parser.add_argument('--output', '-o', required=True,
                       help='Output JSON file path')
    parser.add_argument('--threshold', '-t', type=float, default=0.01,
                       help='Position threshold in meters (default: 0.01)')
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input path not found: {input_path}")
        sys.exit(1)
    
    print(f"\nConverting: {input_path.name}")
    print("=" * 60)
    
    try:
        print("Loading SiT data...")
        data = load_sit_dataset(str(input_path))
        print(f"  Loaded {data['metadata']['num_frames']} frames")
        
        print("\nPreprocessing trajectories...")
        processed_data = preprocess_trajectories(data, position_threshold=args.threshold)
        print(f"  Kept {len(processed_data['trajectories'])} valid trajectories")
        
        print("\nExporting to SocNav3...")
        output_path = export_to_socnav3(processed_data, args.output, sequence_path=str(input_path))
        
        print(f"\nSuccess! Saved to: {output_path}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()