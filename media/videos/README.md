# Videos Directory

Place your resort videos here for use in the website.

## Recommended Video Formats:
- **MP4** (H.264 codec) - Best browser compatibility
- **WebM** - Good for modern browsers
- **MOV** - Can be converted to MP4

## Suggested Video Types:
1. **Hero/Background Videos** 
   - Resort overview/aerial shots
   - Pool and beach scenes
   - Sunset/sunrise timelapse
   - Recommended resolution: 1920x1080 or 4K
   - Duration: 30-60 seconds for background loops

2. **Room Tours**
   - Individual room walkthroughs
   - Amenity showcases
   - Duration: 1-2 minutes

3. **Activity Videos**
   - Water sports
   - Spa treatments
   - Dining experiences
   - Duration: 30 seconds - 2 minutes

## File Naming Convention:
- `hero-background.mp4` - Main hero section background
- `room-ocean-suite.mp4` - Room tour videos
- `amenity-pool.mp4` - Amenity videos
- `activity-watersports.mp4` - Activity videos

## File Size Recommendations:
- Background videos: Under 10MB (compressed)
- Feature videos: Under 20MB
- Use online tools like HandBrake to compress videos

## How to Add Videos:
1. Place video files in this directory
2. Update the Django models (Gallery or Resort) to include video fields
3. Reference videos in templates using `{{ MEDIA_URL }}videos/filename.mp4`