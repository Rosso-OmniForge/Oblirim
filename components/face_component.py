"""
Face component for ASCII art display
"""

def render_face_component():
    """Render the face tile HTML component"""
    return """
    <div class="component-tile face-tile">
        <div class="tile-content">
            <pre id="ascii-face" class="ascii-art">
  ╭─────────────╮
 │  ●     ●    │
 │             │
 │      ─      │
 │             │
  ╰─────────────╯
            </pre>
        </div>
    </div>
    """

def get_face_css():
    """Get CSS specific to face component"""
    return """
    .face-tile {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
        border: 1px solid var(--accent-green);
        position: relative;
        overflow: hidden;
    }
    
    .face-tile::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 255, 0, 0.1), transparent);
        animation: scan 3s linear infinite;
    }
    
    @keyframes scan {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .ascii-art {
        color: var(--accent-green);
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        line-height: 1.2;
        text-align: center;
        margin: 0;
        text-shadow: 0 0 10px var(--accent-green);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 5px var(--accent-green); }
        to { text-shadow: 0 0 15px var(--accent-green), 0 0 25px var(--accent-green); }
    }
    """