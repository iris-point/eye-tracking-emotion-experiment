"""
Gaze Plot GIF Generator for Eye Tracking Experiment

This script generates animated GIFs showing participant gaze trajectories
overlaid on experiment images. It shows the full 8-second timeline with
tracking status indicators and participant ratings.

Screen resolution: 2560x1600
Images are vertically filled and horizontally centered
"""

import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image
import os
import warnings
warnings.filterwarnings('ignore')

# Configuration
SCREEN_WIDTH = 2560
SCREEN_HEIGHT = 1600
OUTPUT_DIR = 'output_gifs'
MAX_FRAMES = 100  # Maximum frames for GIF to keep file size reasonable
FPS = 12.5  # Frames per second for GIF animation


def load_experiment_data(limit=None, csv_file='data/data_full.csv'):
    """Load experiment data with proper rating extraction"""
    print(f"Loading experiment data from {csv_file}...")
    
    # Load CSV data
    df = pd.read_csv(csv_file)
    
    # Filter for image trials with eye tracking data
    img_trials = df[(df['trial_type'] == 'image-keyboard-response') & 
                    (df['stimulus'].str.contains('.jpg|.JPG', na=False, case=False)) & 
                    (df['cogix_eye_tracking'].notna()) &
                    (df['cogix_eye_tracking'] != '')]
    
    # Extract ratings from the next trial
    trials_with_ratings = []
    for idx, trial in img_trials.iterrows():
        trial_dict = trial.to_dict()
        
        # Check if next trial is a rating trial
        next_idx = idx + 1
        if next_idx < len(df) and df.iloc[next_idx]['trial_type'] == 'custom-rating-scale':
            trial_dict['rating'] = df.iloc[next_idx]['response']
        else:
            trial_dict['rating'] = None
        
        trials_with_ratings.append(trial_dict)
    
    # Convert back to DataFrame
    result_df = pd.DataFrame(trials_with_ratings)
    
    total_trials = len(result_df)
    print(f"Found {total_trials} image trials with gaze data")
    
    if limit:
        result_df = result_df.head(limit)
        print(f"Processing first {limit} trials")
    
    return result_df


def parse_gaze_data(gaze_json_str):
    """Parse gaze data from JSON string, keeping all samples to show full timeline"""
    try:
        gaze_data = json.loads(gaze_json_str)
        samples = gaze_data.get('samples', [])
        
        parsed_samples = []
        for sample in samples:
            x = sample.get('x', 0)
            y = sample.get('y', 0)
            t = sample.get('t', 0)
            
            # Convert normalized coordinates to screen pixels
            x_px = x * SCREEN_WIDTH
            y_px = y * SCREEN_HEIGHT
            
            # Mark if this is a valid gaze point (not lost tracking)
            is_valid = (x != 0 or y != 0)
            
            parsed_samples.append({
                'x': x_px,
                'y': y_px,
                't': t,
                'valid': is_valid
            })
        
        return parsed_samples
    except Exception as e:
        print(f"  Error parsing gaze data: {e}")
        return []


def load_and_scale_image(image_path):
    """Load image and scale to fit screen (vertical fill, horizontal center)"""
    # Try different possible paths
    possible_paths = [
        image_path,
        image_path.replace('./assets/', 'assets/'),
        image_path.replace('./assets/', 'experiment-design/assets/'),
        f"experiment-design/{image_path.replace('./', '')}",
    ]
    
    img = None
    for path in possible_paths:
        if os.path.exists(path):
            img = Image.open(path)
            break
    
    if img is None:
        # Create placeholder if image not found
        img = Image.new('RGB', (1920, 1080), color=(128, 128, 128))
    
    # Calculate scaling to fit height
    orig_width, orig_height = img.size
    scale = SCREEN_HEIGHT / orig_height
    new_width = int(orig_width * scale)
    new_height = SCREEN_HEIGHT
    
    # Resize image
    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Create full screen canvas (black background)
    canvas = Image.new('RGB', (SCREEN_WIDTH, SCREEN_HEIGHT), color='black')
    
    # Paste image centered horizontally
    x_offset = (SCREEN_WIDTH - new_width) // 2
    canvas.paste(img_resized, (x_offset, 0))
    
    return np.array(canvas)


def create_gaze_gif(trial_data, output_dir=OUTPUT_DIR):
    """Create animated GIF for a single trial"""
    
    # Extract trial information
    participant_id = trial_data['participant_id']
    image_path = trial_data['stimulus']
    image_name = trial_data.get('image_name', os.path.basename(image_path))
    rating = trial_data.get('rating', None)
    strategy = trial_data.get('strategy', None)
    
    print(f"\nProcessing: {participant_id} - {image_name}")
    
    # Parse gaze data
    gaze_samples = parse_gaze_data(trial_data['cogix_eye_tracking'])
    if not gaze_samples:
        print("  No gaze samples found")
        return None
    
    # Calculate statistics
    times = [s['t'] for s in gaze_samples]
    duration_ms = max(times) - min(times)
    min_time = min(times)
    
    valid_samples = sum(1 for s in gaze_samples if s['valid'])
    tracking_rate = (valid_samples / len(gaze_samples)) * 100
    
    print(f"  Duration: {duration_ms/1000:.1f}s")
    print(f"  Samples: {len(gaze_samples)} total, {valid_samples} tracked ({tracking_rate:.1f}%)")
    print(f"  Rating: {rating}")
    
    # Downsample if too many frames
    if len(gaze_samples) > MAX_FRAMES:
        downsample_rate = len(gaze_samples) // MAX_FRAMES
        gaze_samples = gaze_samples[::downsample_rate]
        print(f"  Downsampled to {len(gaze_samples)} frames")
    
    # Load and prepare image
    img_array = load_and_scale_image(image_path)
    
    # Create figure
    fig = plt.figure(figsize=(12.8, 8), dpi=100)
    ax = fig.add_subplot(111)
    
    # Setup plot
    ax.set_xlim(0, SCREEN_WIDTH)
    ax.set_ylim(SCREEN_HEIGHT, 0)  # Invert Y for screen coordinates
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Display background image
    ax.imshow(img_array, extent=[0, SCREEN_WIDTH, SCREEN_HEIGHT, 0])
    
    # Title
    title = f'Participant: {participant_id} | Image: {image_name}'
    if rating is not None:
        title += f' | Rating: {rating}'
    title += f' | Duration: {duration_ms/1000:.1f}s | Tracking: {tracking_rate:.1f}%'
    ax.set_title(title, fontsize=12, pad=10)
    
    # Animation elements
    trajectory_line, = ax.plot([], [], 'yellow', linewidth=2, alpha=0.7)
    current_point = ax.scatter([], [], s=150, c='red', edgecolors='yellow', 
                              linewidths=2, zorder=5)
    
    # Status indicators
    time_text = ax.text(0.02, 0.98, '', transform=ax.transAxes,
                       fontsize=10, va='top',
                       bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    
    lost_text = ax.text(0.5, 0.05, '', transform=ax.transAxes,
                       fontsize=14, ha='center', color='red',
                       bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9))
    
    # Track valid points for trajectory
    trajectory_x = []
    trajectory_y = []
    
    def init():
        trajectory_line.set_data([], [])
        current_point.set_offsets(np.empty((0, 2)))
        time_text.set_text('')
        lost_text.set_text('')
        return trajectory_line, current_point, time_text, lost_text
    
    def animate(frame):
        if frame >= len(gaze_samples):
            return trajectory_line, current_point, time_text, lost_text
        
        sample = gaze_samples[frame]
        current_time = (sample['t'] - min_time) / 1000
        
        # Update time display
        time_text.set_text(f'Time: {current_time:.2f}s / {duration_ms/1000:.1f}s')
        
        if sample['valid']:
            # Valid gaze point
            trajectory_x.append(sample['x'])
            trajectory_y.append(sample['y'])
            
            # Show last 30 points of trajectory
            if len(trajectory_x) > 1:
                recent_x = trajectory_x[-30:] if len(trajectory_x) > 30 else trajectory_x
                recent_y = trajectory_y[-30:] if len(trajectory_y) > 30 else trajectory_y
                trajectory_line.set_data(recent_x, recent_y)
            
            current_point.set_offsets([[sample['x'], sample['y']]])
            lost_text.set_text('')
        else:
            # Tracking lost
            current_point.set_offsets(np.empty((0, 2)))
            lost_text.set_text('TRACKING LOST')
        
        return trajectory_line, current_point, time_text, lost_text
    
    # Create animation
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                 frames=len(gaze_samples),
                                 interval=1000/FPS, blit=True, repeat=True)
    
    # Save GIF
    os.makedirs(output_dir, exist_ok=True)
    clean_name = image_name.replace('.jpg', '').replace('.JPG', '').replace('(', '').replace(')', '')
    output_file = os.path.join(output_dir, f'{participant_id}_{clean_name}_gaze.gif')
    
    try:
        print(f"  Saving GIF...")
        anim.save(output_file, writer='pillow', fps=FPS)
        print(f"  Success: {output_file}")
        plt.close()
        return output_file
    except Exception as e:
        print(f"  Error saving GIF: {e}")
        plt.close()
        return None


if __name__ == "__main__":
    import sys
    import argparse
    
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate gaze plot GIFs from eye tracking data')
    parser.add_argument('--input', '-i', type=str, default='data/data_full.csv',
                        help='Path to CSV file (default: data/data_full.csv)')
    parser.add_argument('--limit', '-l', type=int, default=None,
                        help='Limit number of trials to process (default: all)')
    
    args = parser.parse_args()
    
    # Process with specified file
    print(f"Processing: {args.input}")
    trials = load_experiment_data(limit=args.limit, csv_file=args.input)
    
    if len(trials) == 0:
        print("No valid trials found in the data!")
        sys.exit(1)
    
    participants = trials['participant_id'].unique()
    print(f"\nParticipants: {participants}")
    print("=" * 70)
    
    successful = 0
    failed = 0
    
    # Process each trial
    for idx, trial in trials.iterrows():
        try:
            result = create_gaze_gif(trial)
            if result:
                successful += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  Error processing trial: {e}")
            failed += 1
    
    # Summary
    print("\n" + "=" * 70)
    print("Processing Complete!")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Total: {successful + failed}")
    print(f"\nGIFs saved in '{OUTPUT_DIR}' directory")