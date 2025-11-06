"""
System specs component for displaying system information
"""

def render_system_specs_component():
    """Render the system specs tile HTML component"""
    return """
    <div class="component-tile specs-tile">
        <div class="tile-content">
            <div class="specs-grid">
                <div class="spec-row">
                    <span class="spec-label">MODEL</span>
                    <span class="spec-value" id="pi-model">LOADING...</span>
                </div>
                <div class="spec-row">
                    <span class="spec-label">IP</span>
                    <span class="spec-value" id="ip">LOADING...</span>
                </div>
                <div class="spec-row">
                    <span class="spec-label">WLAN0</span>
                    <span class="spec-value status-indicator" id="wlan0">LOADING...</span>
                </div>
                <div class="spec-row">
                    <span class="spec-label">WLAN1</span>
                    <span class="spec-value status-indicator" id="wlan1">LOADING...</span>
                </div>
                <div class="spec-row">
                    <span class="spec-label">ETH0</span>
                    <span class="spec-value status-indicator" id="eth0">LOADING...</span>
                </div>
                <div class="spec-row">
                    <span class="spec-label">BT</span>
                    <span class="spec-value status-indicator" id="bluetooth">LOADING...</span>
                </div>
                <div class="spec-row">
                    <span class="spec-label">TEMP</span>
                    <span class="spec-value" id="temperature">LOADING...</span>
                </div>
                <div class="spec-row">
                    <span class="spec-label">CPU</span>
                    <span class="spec-value" id="cpu">LOADING...</span>
                </div>
                <div class="spec-row">
                    <span class="spec-label">RAM</span>
                    <span class="spec-value" id="memory-percent">LOADING...</span>
                </div>
                <div class="spec-row">
                    <span class="spec-label">DISK</span>
                    <span class="spec-value" id="disk-percent">LOADING...</span>
                </div>
            </div>
        </div>
    </div>
    """

def get_specs_css():
    """Get CSS specific to system specs component"""
    return """
    .specs-tile {
        background: linear-gradient(135deg, #0a0a0a 0%, #151515 100%);
        border: 1px solid var(--accent-blue);
        position: relative;
    }
    
    .specs-tile::after {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 3px;
        height: 100%;
        background: linear-gradient(to bottom, transparent, var(--accent-blue), transparent);
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 1; }
    }
    
    .specs-grid {
        display: grid;
        gap: 0.5rem;
        font-family: 'Courier New', monospace;
    }
    
    .spec-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.3rem 0;
        border-bottom: 1px solid rgba(0, 255, 255, 0.1);
    }
    
    .spec-row:last-child {
        border-bottom: none;
    }
    
    .spec-label {
        color: var(--accent-blue);
        font-weight: bold;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        min-width: 60px;
    }
    
    .spec-value {
        color: var(--text-primary);
        font-size: 0.8rem;
        text-align: right;
        font-weight: bold;
        text-shadow: 0 0 3px currentColor;
    }
    """