from flask import Flask, request, jsonify
import json
import random
import tempfile
import os
import uuid

app = Flask(__name__)

# Health check endpoint
@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'running',
        'message': 'Video generation service is active',
        'endpoints': ['/generate_video', '/generate_thumbnail']
    })

@app.route('/generate_video', methods=['POST'])
def generate_video():
    try:
        # Get data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No JSON data received'
            }), 400
        
        # Extract parameters
        frequency = data.get('frequency', 528)
        duration_minutes = data.get('loop_duration_minutes', 60)
        video_style = data.get('video_style', 'nebula')
        audio_style = data.get('audio_style', 'ambient pads')
        
        # Generate unique video ID
        video_id = str(uuid.uuid4())
        
        # For now, return simulated response
        # In production, replace with actual video generation
        return jsonify({
            'status': 'success',
            'video_url': f'https://example.com/videos/{video_id}.mp4',
            'video_id': video_id,
            'frequency': frequency,
            'duration_minutes': duration_minutes,
            'video_style': video_style,
            'audio_style': audio_style,
            'message': 'Video generation completed'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/generate_thumbnail', methods=['POST'])
def generate_thumbnail():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No JSON data received'
            }), 400
        
        frequency = data.get('frequency', 528)
        text = data.get('text', f'{frequency} Hz Healing')
        background_style = data.get('background_style', 'aurora')
        
        thumb_id = str(uuid.uuid4())
        
        return jsonify({
            'status': 'success',
            'thumbnail_url': f'https://example.com/thumbnails/{thumb_id}.jpg',
            'thumbnail_id': thumb_id,
            'frequency': frequency,
            'text': text,
            'background_style': background_style,
            'message': 'Thumbnail generation completed'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        data = request.get_json()
        return jsonify({
            'status': 'success',
            'message': 'Test endpoint working',
            'received_data': data
        })
    else:
        return jsonify({
            'status': 'success',
            'message': 'Test endpoint working - GET method',
            'port': os.environ.get('PORT', 'not set')
        })

if __name__ == '__main__':
    # For local development
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
