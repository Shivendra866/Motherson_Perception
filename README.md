<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Motherson Perception - README</title>
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>
    <style>
        /* ── Reset & Base ── */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: linear-gradient(145deg, #0b0e1a 0%, #1a1f33 100%);
            color: #e8edf5;
            padding: 2rem 1.5rem;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            animation: fadeIn 0.8s ease;
        }

        .container {
            max-width: 1200px;
            width: 100%;
            background: rgba(18, 24, 44, 0.65);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: 2.5rem;
            padding: 2.8rem 3rem;
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.7), 0 0 0 1px rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.03);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        /* subtle animated glow orbs */
        .container::before,
        .container::after {
            content: '';
            position: absolute;
            border-radius: 50%;
            filter: blur(80px);
            opacity: 0.2;
            pointer-events: none;
            z-index: 0;
        }
        .container::before {
            width: 400px;
            height: 400px;
            background: #4f7aff;
            top: -120px;
            right: -120px;
            animation: floatGlow 12s infinite alternate ease-in-out;
        }
        .container::after {
            width: 350px;
            height: 350px;
            background: #b84aff;
            bottom: -100px;
            left: -100px;
            animation: floatGlow 15s infinite alternate-reverse ease-in-out;
        }

        /* all content sits above pseudo elements */
        .container > * {
            position: relative;
            z-index: 1;
        }

        /* ── Animations ── */
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        @keyframes floatGlow {
            0% { transform: translate(0, 0) scale(1); }
            100% { transform: translate(30px, 30px) scale(1.2); }
        }

        @keyframes pulse {
            0% { transform: scale(1); opacity: 0.7; }
            50% { transform: scale(1.05); opacity: 1; }
            100% { transform: scale(1); opacity: 0.7; }
        }

        @keyframes slideUp {
            0% { opacity: 0; transform: translateY(30px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        @keyframes shimmer {
            0% { background-position: -200% 0; }
            100% { background-position: 200% 0; }
        }

        /* ── Header ── */
        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 1.2rem;
            margin-bottom: 2.2rem;
            padding-bottom: 1.2rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        }

        .logo-area {
            display: flex;
            align-items: center;
            gap: 1.2rem;
        }

        .logo-icon {
            font-size: 2.6rem;
            color: #7c9bff;
            animation: pulse 3s infinite ease-in-out;
            filter: drop-shadow(0 0 12px rgba(79, 122, 255, 0.4));
        }

        .title h1 {
            font-size: 2.2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #ffffff 0%, #9bb8ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -0.5px;
        }

        .title .sub {
            font-size: 0.95rem;
            color: #8e9ccf;
            font-weight: 400;
            display: flex;
            align-items: center;
            gap: 0.6rem;
            flex-wrap: wrap;
        }

        .title .sub i {
            color: #4f7aff;
            font-size: 0.8rem;
        }

        .badge-group {
            display: flex;
            gap: 0.8rem;
            flex-wrap: wrap;
        }

        .badge {
            background: rgba(79, 122, 255, 0.15);
            border: 1px solid rgba(79, 122, 255, 0.25);
            border-radius: 40px;
            padding: 0.4rem 1.2rem;
            font-size: 0.8rem;
            font-weight: 500;
            color: #b2c7ff;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.25s ease;
            backdrop-filter: blur(4px);
        }
        .badge i {
            color: #7c9bff;
        }
        .badge:hover {
            background: rgba(79, 122, 255, 0.25);
            border-color: #4f7aff;
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(79, 122, 255, 0.15);
        }

        /* ── Description ── */
        .description {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 1.8rem;
            padding: 1.8rem 2.2rem;
            margin-bottom: 2.8rem;
            border: 1px solid rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(8px);
            animation: slideUp 0.8s ease 0.1s both;
        }

        .description p {
            font-size: 1.08rem;
            line-height: 1.7;
            color: #d0daf5;
            display: flex;
            align-items: center;
            gap: 1rem;
            flex-wrap: wrap;
        }

        .description p i {
            color: #7c9bff;
            font-size: 1.6rem;
        }

        .feature-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 0.7rem;
            margin-top: 0.8rem;
        }

        .feature-tags span {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 30px;
            padding: 0.25rem 1rem;
            font-size: 0.8rem;
            color: #a8bae6;
            border: 1px solid rgba(255, 255, 255, 0.06);
        }

        /* ── Grid Layout ── */
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            margin: 2.2rem 0 2.2rem 0;
        }

        @media (max-width: 900px) {
            .container { padding: 1.8rem; }
            .grid-2 { grid-template-columns: 1fr; }
        }

        /* ── Cards ── */
        .card {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 1.8rem;
            padding: 1.8rem 2rem;
            border: 1px solid rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(8px);
            transition: all 0.3s ease;
            animation: slideUp 0.7s ease both;
        }

        .card:nth-child(1) { animation-delay: 0.1s; }
        .card:nth-child(2) { animation-delay: 0.2s; }
        .card:nth-child(3) { animation-delay: 0.3s; }
        .card:nth-child(4) { animation-delay: 0.4s; }

        .card:hover {
            background: rgba(255, 255, 255, 0.06);
            border-color: rgba(79, 122, 255, 0.2);
            transform: translateY(-4px);
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.3);
        }

        .card h3 {
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 0.8rem;
            display: flex;
            align-items: center;
            gap: 0.8rem;
            color: #eef3ff;
        }

        .card h3 i {
            color: #4f7aff;
            font-size: 1.4rem;
            width: 2rem;
            text-align: center;
        }

        .card ul, .card p {
            color: #c5d0ed;
            line-height: 1.7;
            font-size: 0.95rem;
        }

        .card ul {
            list-style: none;
            padding-left: 0;
        }

        .card ul li {
            padding: 0.2rem 0 0.2rem 1.8rem;
            position: relative;
        }

        .card ul li::before {
            content: '▹';
            position: absolute;
            left: 0;
            color: #4f7aff;
            font-weight: 700;
        }

        /* ── Code Block ── */
        .code-block {
            background: #0c0f1e;
            border-radius: 1.4rem;
            padding: 1.4rem 1.8rem;
            margin: 1rem 0;
            border: 1px solid rgba(255, 255, 255, 0.06);
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            font-size: 0.85rem;
            color: #bcc9f0;
            overflow-x: auto;
            white-space: pre-wrap;
            word-break: break-word;
            position: relative;
        }

        .code-block .copy-btn {
            position: absolute;
            top: 0.6rem;
            right: 0.8rem;
            background: rgba(255, 255, 255, 0.06);
            border: none;
            color: #8e9ccf;
            padding: 0.2rem 0.8rem;
            border-radius: 30px;
            font-size: 0.7rem;
            cursor: pointer;
            transition: 0.2s;
            backdrop-filter: blur(4px);
        }
        .code-block .copy-btn:hover {
            background: rgba(79, 122, 255, 0.2);
            color: #fff;
        }

        /* ── Table (3D Output) ── */
        .table-wrap {
            overflow-x: auto;
            margin: 1.2rem 0 0.4rem 0;
            border-radius: 1.2rem;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
            background: rgba(0, 0, 0, 0.2);
        }

        th {
            background: rgba(79, 122, 255, 0.12);
            color: #b2c7ff;
            font-weight: 500;
            padding: 0.7rem 1rem;
            text-align: left;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        }

        td {
            padding: 0.6rem 1rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.03);
            color: #d0daf5;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
        }

        tr:last-child td {
            border-bottom: none;
        }

        .highlight-blue {
            color: #7c9bff;
        }

        .highlight-green {
            color: #5fdc9c;
        }

        /* ── Controls Grid ── */
        .key-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 0.6rem;
            margin: 0.6rem 0 0.2rem 0;
        }

        .key-item {
            background: rgba(0, 0, 0, 0.25);
            border-radius: 0.8rem;
            padding: 0.4rem 0.8rem;
            display: flex;
            align-items: center;
            gap: 0.6rem;
            font-size: 0.85rem;
            border: 1px solid rgba(255, 255, 255, 0.04);
        }

        .key-item kbd {
            background: #1e2440;
            padding: 0.1rem 0.6rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
            color: #bcc9f0;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        .key-item span {
            color: #a8bae6;
        }

        /* ── Footer ── */
        .footer {
            margin-top: 2.8rem;
            padding-top: 1.6rem;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
            font-size: 0.85rem;
            color: #6f7faa;
        }

        .footer i {
            color: #4f7aff;
            margin: 0 0.2rem;
        }

        .footer a {
            color: #8e9ccf;
            text-decoration: none;
            transition: 0.2s;
            border-bottom: 1px dotted transparent;
        }
        .footer a:hover {
            color: #b2c7ff;
            border-bottom-color: #4f7aff;
        }

        /* ── responsive tweaks ── */
        @media (max-width: 600px) {
            .container { padding: 1.2rem; }
            .title h1 { font-size: 1.6rem; }
            .header { flex-direction: column; align-items: flex-start; }
            .badge-group { width: 100%; }
            .description p { font-size: 0.95rem; }
            .card { padding: 1.4rem; }
        }

        /* scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb {
            background: #2e3a66;
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #4f7aff;
        }
    </style>
</head>
<body>
<div class="container">

    <!-- HEADER -->
    <div class="header">
        <div class="logo-area">
            <div class="logo-icon"><i class="fas fa-robot"></i></div>
            <div class="title">
                <h1>Motherson Perception</h1>
                <div class="sub">
                    <i class="fas fa-camera"></i> Real‑time Tail Lamp / Dome Segmentation
                    <span style="color:#4f7aff;">·</span>
                    <i class="fas fa-microchip"></i> RF‑DETR + Intel RealSense
                </div>
            </div>
        </div>
        <div class="badge-group">
            <span class="badge"><i class="fas fa-cube"></i> 3D</span>
            <span class="badge"><i class="fas fa-layer-group"></i> Segmentation</span>
            <span class="badge"><i class="fas fa-chart-line"></i> Real‑time</span>
            <span class="badge"><i class="fas fa-code"></i> v1.0</span>
        </div>
    </div>

    <!-- DESCRIPTION -->
    <div class="description">
        <p>
            <i class="fas fa-bolt"></i>
            <span>Real‑time segmentation &amp; 3D coordinate estimation for automotive parts using <strong>RF‑DETR</strong> and <strong>Intel RealSense</strong> RGB‑Depth cameras.</span>
        </p>
        <div class="feature-tags">
            <span>🔹 RF‑DETR Segmentation</span>
            <span>🔹 Depth alignment</span>
            <span>🔹 3D (X, Y, Z)</span>
            <span>🔹 Keypoint extraction</span>
            <span>🔹 Temporal smoothing</span>
            <span>🔹 Outlier filtering</span>
        </div>
    </div>

    <!-- GRID: left 2 cards, right 2 cards -->
    <div class="grid-2">

        <!-- Project Structure -->
        <div class="card">
            <h3><i class="fas fa-folder-open"></i> Project Structure</h3>
            <div class="code-block" style="font-size:0.8rem; padding:1rem 1.2rem;">
                <span style="color:#6f7faa;">Motherson_Perception/</span><br/>
                ├── <span style="color:#7c9bff;">app.py</span>                 <span style="color:#6f7faa;"># Main</span><br/>
                ├── <span style="color:#7c9bff;">dome_seg.py</span>            <span style="color:#6f7faa;"># Dome seg</span><br/>
                ├── <span style="color:#7c9bff;">TailLamp_seg.py</span>        <span style="color:#6f7faa;"># Tail lamp seg</span><br/>
                ├── <span style="color:#7c9bff;">dome_seg.pth</span>           <span style="color:#6f7faa;"># Dome model</span><br/>
                ├── <span style="color:#7c9bff;">TailLamp_seg.pth</span>       <span style="color:#6f7faa;"># Tail lamp model</span><br/>
                ├── <span style="color:#7c9bff;">requirements.txt</span><br/>
                └── <span style="color:#7c9bff;">README.md</span>
            </div>
        </div>

        <!-- Features -->
        <div class="card">
            <h3><i class="fas fa-star"></i> Features</h3>
            <ul>
                <li>RF‑DETR Segmentation inference</li>
                <li>Intel RealSense RGB + Depth</li>
                <li>Automatic depth alignment</li>
                <li>3D coordinate estimation (X, Y, Z)</li>
                <li>Border keypoint extraction <span style="color:#6f7faa;">(Top, Bottom, Left, Right, Center)</span></li>
                <li>Temporal smoothing &amp; outlier filtering</li>
                <li>Live visualization: Detection + 3D, Mask, Depth</li>
            </ul>
        </div>

        <!-- Installation & Running -->
        <div class="card">
            <h3><i class="fas fa-terminal"></i> Installation &amp; Run</h3>
            <div class="code-block" style="font-size:0.8rem;">
                <span style="color:#6f7faa;"># clone &amp; setup</span><br/>
                git clone &lt;repository_url&gt;<br/>
                cd Motherson_Perception<br/>
                python3 -m venv venv<br/>
                source venv/bin/activate<br/>
                pip install -r requirements.txt<br/><br/>
                <span style="color:#6f7faa;"># run</span><br/>
                python app.py
            </div>
            <p style="margin-top:0.8rem; font-size:0.9rem;">
                <i class="fas fa-info-circle" style="color:#4f7aff;"></i>
                Requires Intel RealSense SDK &amp; camera connected.
            </p>
        </div>

        <!-- Keyboard Controls -->
        <div class="card">
            <h3><i class="fas fa-keyboard"></i> Controls</h3>
            <div class="key-grid">
                <div class="key-item"><kbd>q</kbd> <span>Quit</span></div>
                <div class="key-item"><kbd>+</kbd> <span>Increase smoothing</span></div>
                <div class="key-item"><kbd>−</kbd> <span>Decrease smoothing</span></div>
            </div>
            <p style="margin-top:0.8rem; font-size:0.9rem; color:#a8bae6;">
                <i class="fas fa-arrows-alt-h" style="color:#4f7aff;"></i>
                Output: Detection + 3D &nbsp;·&nbsp; Segmentation Mask &nbsp;·&nbsp; Depth Map
            </p>
        </div>
    </div>

    <!-- 3D OUTPUT TABLE -->
    <div class="card" style="margin: 1.2rem 0 0 0; animation-delay:0.5s;">
        <h3><i class="fas fa-cube"></i> 3D Coordinate Output</h3>
        <p style="color:#c5d0ed; font-size:0.9rem; margin-bottom:0.6rem;">
            For every detected object, the following keypoints are computed.
        </p>
        <div class="table-wrap">
            <table>
                <thead>
                    <tr>
                        <th>Point</th>
                        <th>Pixel</th>
                        <th>X (m)</th>
                        <th>Y (m)</th>
                        <th>Z (m)</th>
                        <th>Depth</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>TOP</td><td>(320, 120)</td><td class="highlight-blue">-0.0241</td><td class="highlight-blue">-0.0562</td><td class="highlight-green">0.4821</td><td class="highlight-green">0.4821</td></tr>
                    <tr><td>BOTTOM</td><td>(318, 360)</td><td class="highlight-blue">-0.0198</td><td class="highlight-blue">0.0613</td><td class="highlight-green">0.4795</td><td class="highlight-green">0.4795</td></tr>
                    <tr><td>LEFT</td><td>(200, 240)</td><td class="highlight-blue">-0.0634</td><td class="highlight-blue">0.0021</td><td class="highlight-green">0.4812</td><td class="highlight-green">0.4812</td></tr>
                    <tr><td>RIGHT</td><td>(436, 242)</td><td class="highlight-blue">0.0587</td><td class="highlight-blue">0.0019</td><td class="highlight-green">0.4804</td><td class="highlight-green">0.4804</td></tr>
                    <tr><td>CENTER</td><td>(318, 240)</td><td class="highlight-blue">-0.0012</td><td class="highlight-blue">0.0034</td><td class="highlight-green">0.4788</td><td class="highlight-green">0.4788</td></tr>
                </tbody>
            </table>
        </div>
        <p style="color:#6f7faa; font-size:0.8rem; margin-top:0.6rem;">
            <i class="fas fa-info-circle"></i> Values are illustrative – actual values depend on camera &amp; scene.
        </p>
    </div>

    <!-- FOOTER -->
    <div class="footer">
        <div>
            <i class="fas fa-copyright"></i> 2025 Motherson · for internal development &amp; research
        </div>
        <div>
            <i class="fas fa-code"></i> RF‑DETR · 
            <i class="fas fa-camera"></i> Intel RealSense · 
            <i class="fas fa-fire"></i> PyTorch
        </div>
        <div>
            <i class="fas fa-tag"></i> v1.0 · 
            <a href="#"><i class="fab fa-github"></i> GitHub</a>
        </div>
    </div>

</div>
</body>
</html>
