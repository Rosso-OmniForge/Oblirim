"""
Emotions system for ASCII face display
Manages different emotional states based on system metrics
"""

import random

class EmotionEngine:
    def __init__(self):
        self.faces = {
            'happy': {
                'ascii': """
    ╭─────────────╮
   │  ◉     ◉    │
   │      ◡      │
   │   ╲     ╱   │
   │    ╲___╱    │
    ╰─────────────╯
                """,
                'triggers': {
                    'cpu_low': True,
                    'temp_normal': True,
                    'memory_ok': True
                }
            },
            'neutral': {
                'ascii': """
    ╭─────────────╮
   │  ●     ●    │
   │             │
   │      ─      │
   │             │
    ╰─────────────╯
                """,
                'triggers': {
                    'default': True
                }
            },
            'concerned': {
                'ascii': """
    ╭─────────────╮
   │  ◉     ◉    │
   │      ~      │
   │    ╱───╲    │
   │   ╱     ╲   │
    ╰─────────────╯
                """,
                'triggers': {
                    'cpu_high': True,
                    'temp_warm': True
                }
            },
            'stressed': {
                'ascii': """
    ╭─────────────╮
   │  ×     ×    │
   │      ○      │
   │    ╱───╲    │
   │   ╱  !  ╲   │
    ╰─────────────╯
                """,
                'triggers': {
                    'cpu_critical': True,
                    'temp_hot': True,
                    'memory_critical': True
                }
            },
            'sleepy': {
                'ascii': """
    ╭─────────────╮
   │  ╲     ╱    │
   │   ╲___╱     │
   │      ○      │
   │    ~~~~     │
    ╰─────────────╯
                """,
                'triggers': {
                    'low_activity': True
                }
            },
            'excited': {
                'ascii': """
    ╭─────────────╮
   │  ★     ★    │
   │      ◇      │
   │   ╲  ○  ╱   │
   │    ╲___╱    │
    ╰─────────────╯
                """,
                'triggers': {
                    'high_activity': True,
                    'network_active': True
                }
            },
            'error': {
                'ascii': """
    ╭─────────────╮
   │  !     !    │
   │      ×      │
   │    ╱───╲    │
   │   ╱ ERR ╲   │
    ╰─────────────╯
                """,
                'triggers': {
                    'system_error': True
                }
            }
        }
    
    def get_emotion(self, system_data):
        """Determine emotion based on system metrics"""
        try:
            # Parse system metrics
            cpu_percent = float(system_data.get('cpu', '0%').replace('%', ''))
            temp_str = system_data.get('temperature', '0°C')
            
            # Extract temperature value
            temp = 0
            if temp_str != 'N/A' and '°C' in temp_str:
                try:
                    temp = float(temp_str.replace('°C', ''))
                except:
                    temp = 0
            
            # Check for errors
            if any('Error' in str(v) for v in system_data.values()):
                return 'error'
            
            # Determine emotion based on metrics
            if cpu_percent > 90 or temp > 80:
                return 'stressed'
            elif cpu_percent > 70 or temp > 70:
                return 'concerned'
            elif cpu_percent < 10:
                return 'sleepy'
            elif cpu_percent > 50:
                return 'excited'
            else:
                return 'happy'
                
        except Exception as e:
            print(f"Error determining emotion: {e}")
            return 'neutral'
    
    def get_face(self, emotion='neutral'):
        """Get ASCII face for given emotion"""
        return self.faces.get(emotion, self.faces['neutral'])['ascii']
    
    def get_random_face(self):
        """Get a random face"""
        emotion = random.choice(list(self.faces.keys()))
        return self.get_face(emotion)

# Global instance
emotion_engine = EmotionEngine()