/**
 * Illinois MakerLab - Instant 3D Print Quote Calculator
 *
 * Features:
 *   - Binary & ASCII STL parsing
 *   - Basic OBJ parsing (vertices + faces)
 *   - Three.js 3D model preview with orbit controls
 *   - Volume / bounding-box / triangle count extraction
 *   - Real-time cost estimation based on MakerLab pricing
 *
 * Pricing data (source: pricingservices.html / online-ordering.html):
 *   Walk-in: Student 10¢/g, Faculty 25¢/g, General 35¢/g
 *   Online:  Student 12¢/g, Faculty 30¢/g, General 42¢/g  (+20% surcharge)
 *   All prints: $4 base fee + material cost
 */

(function () {
  'use strict';

  // ── Pricing table (cents per gram) ────────────────────────────────────
  // Standard PLA rates. Dual-color or specialty filaments (PVA soluble
  // supports, PETG, etc.) carry a 50% surcharge on these base prices.
  // That surcharge is NOT calculated here — noted in the disclaimer instead.
  var PRICING = {
    walkin: { student: 0.10, faculty: 0.25, general: 0.35 },
    online: { student: 0.12, faculty: 0.30, general: 0.42 }
  };
  var BASE_FEE = 4.00; // $4 base fee applies to all prints
  var PLA_DENSITY = 1.24; // g/cm³

  // ── Analytics helper ────────────────────────────────────────────────
  function trackEvent(action, params) {
    if (typeof gtag === 'function') gtag('event', action, params);
  }
  var quoteCalcTimer;
  function trackQuoteDebounced(params) {
    clearTimeout(quoteCalcTimer);
    quoteCalcTimer = setTimeout(function () { trackEvent('quote_calculated', params); }, 1000);
  }

  // ── DOM refs ──────────────────────────────────────────────────────────
  var dropzone     = document.getElementById('quote-dropzone');
  var fileInput    = document.getElementById('quote-file-input');
  var iface        = document.getElementById('quote-interface');
  var canvas       = document.getElementById('quote-canvas');
  var filenameEl   = document.getElementById('quote-filename');
  var changeFileBtn= document.getElementById('quote-change-file');
  var resetViewBtn = document.getElementById('quote-reset-view');
  var infillSlider = document.getElementById('quote-infill');
  var infillValue  = document.getElementById('quote-infill-value');
  var qtyInput     = document.getElementById('quote-quantity');
  var qtyMinus     = document.getElementById('quote-qty-minus');
  var qtyPlus      = document.getElementById('quote-qty-plus');
  var dimEl        = document.getElementById('quote-dimensions');
  var volEl        = document.getElementById('quote-volume');
  var triEl        = document.getElementById('quote-triangles');
  var weightEl     = document.getElementById('quote-weight');
  var rateEl       = document.getElementById('quote-rate');
  var baseFeeRow   = document.getElementById('quote-base-fee-row');
  var qtyRow       = document.getElementById('quote-qty-row');
  var qtyDisplay   = document.getElementById('quote-qty-display');
  var totalEl      = document.getElementById('quote-total-price');

  if (!dropzone) return; // not on quote page

  // ── State ─────────────────────────────────────────────────────────────
  var modelVolumeMm3 = 0;   // outer-shell volume in mm³ (parser outputs mm³)
  var modelTriangles = 0;

  // ── Three.js setup ────────────────────────────────────────────────────
  var scene, camera, renderer, controls, modelMesh;
  var animFrameId;

  function initThree() {
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf5f5f5);

    // Camera
    camera = new THREE.PerspectiveCamera(45, 1, 0.1, 10000);
    camera.position.set(0, 0, 5);

    // Renderer
    renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // Lights
    var ambient = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambient);

    var dirLight1 = new THREE.DirectionalLight(0xffffff, 0.8);
    dirLight1.position.set(1, 2, 3);
    scene.add(dirLight1);

    var dirLight2 = new THREE.DirectionalLight(0xffffff, 0.3);
    dirLight2.position.set(-2, -1, -1);
    scene.add(dirLight2);

    // Simple orbit controls (inline — avoids extra CDN dependency)
    controls = createOrbitControls(camera, renderer.domElement);

    resizeViewer();
    animate();
  }

  function resizeViewer() {
    var container = document.getElementById('quote-viewer');
    if (!container || !renderer) return;
    var w = container.clientWidth;
    var h = container.clientHeight || 400;
    renderer.setSize(w, h);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }

  function animate() {
    animFrameId = requestAnimationFrame(animate);
    if (controls) controls.update();
    renderer.render(scene, camera);
  }

  // Pause animation when tab is hidden; dispose GPU resources on page unload
  document.addEventListener('visibilitychange', function () {
    if (!renderer) return;
    if (document.hidden) {
      cancelAnimationFrame(animFrameId);
    } else {
      animate();
    }
  });

  window.addEventListener('pagehide', function () {
    cancelAnimationFrame(animFrameId);
    if (renderer) {
      renderer.dispose();
      renderer.forceContextLoss();
    }
  });

  // ── Minimal orbit controls ────────────────────────────────────────────
  function createOrbitControls(cam, domEl) {
    var spherical = { radius: 5, theta: 0, phi: Math.PI / 3 };
    var target = new THREE.Vector3(0, 0, 0);
    var isDragging = false;
    var prevMouse = { x: 0, y: 0 };
    var dampingFactor = 0.004;

    function updateCameraPosition() {
      var sinPhi = Math.sin(spherical.phi);
      cam.position.set(
        target.x + spherical.radius * sinPhi * Math.sin(spherical.theta),
        target.y + spherical.radius * Math.cos(spherical.phi),
        target.z + spherical.radius * sinPhi * Math.cos(spherical.theta)
      );
      cam.lookAt(target);
    }

    domEl.addEventListener('pointerdown', function (e) {
      isDragging = true;
      prevMouse.x = e.clientX;
      prevMouse.y = e.clientY;
      domEl.setPointerCapture(e.pointerId);
    });

    domEl.addEventListener('pointermove', function (e) {
      if (!isDragging) return;
      var dx = e.clientX - prevMouse.x;
      var dy = e.clientY - prevMouse.y;
      spherical.theta -= dx * dampingFactor;
      spherical.phi   = Math.max(0.1, Math.min(Math.PI - 0.1, spherical.phi + dy * dampingFactor));
      prevMouse.x = e.clientX;
      prevMouse.y = e.clientY;
      updateCameraPosition();
    });

    domEl.addEventListener('pointerup', function (e) {
      isDragging = false;
      domEl.releasePointerCapture(e.pointerId);
    });

    domEl.addEventListener('wheel', function (e) {
      e.preventDefault();
      spherical.radius = Math.max(0.5, Math.min(500, spherical.radius * (1 + e.deltaY * 0.001)));
      updateCameraPosition();
    }, { passive: false });

    // Touch pinch-zoom
    var lastPinchDist = 0;
    domEl.addEventListener('touchstart', function (e) {
      if (e.touches.length === 2) {
        var dx = e.touches[0].clientX - e.touches[1].clientX;
        var dy = e.touches[0].clientY - e.touches[1].clientY;
        lastPinchDist = Math.sqrt(dx * dx + dy * dy);
      }
    }, { passive: true });

    domEl.addEventListener('touchmove', function (e) {
      if (e.touches.length === 2) {
        var dx = e.touches[0].clientX - e.touches[1].clientX;
        var dy = e.touches[0].clientY - e.touches[1].clientY;
        var dist = Math.sqrt(dx * dx + dy * dy);
        if (lastPinchDist > 0) {
          spherical.radius *= lastPinchDist / dist;
          spherical.radius = Math.max(0.5, Math.min(500, spherical.radius));
          updateCameraPosition();
        }
        lastPinchDist = dist;
      }
    }, { passive: true });

    return {
      update: function () {},
      reset: function (newTarget, newRadius) {
        target.copy(newTarget);
        spherical.radius = newRadius;
        spherical.theta = 0;
        spherical.phi = Math.PI / 3;
        updateCameraPosition();
      },
      setPosition: function (newTarget, newRadius) {
        target.copy(newTarget);
        spherical.radius = newRadius;
        updateCameraPosition();
      }
    };
  }

  // ── STL Parser ────────────────────────────────────────────────────────

  function parseSTL(buffer) {
    var dv = new DataView(buffer);

    // Check if ASCII
    var header = '';
    for (var i = 0; i < Math.min(80, buffer.byteLength); i++) {
      header += String.fromCharCode(dv.getUint8(i));
    }

    if (header.trim().indexOf('solid') === 0 && !isBinarySTL(buffer)) {
      return parseASCIISTL(buffer);
    }
    return parseBinarySTL(buffer);
  }

  function isBinarySTL(buffer) {
    // Binary STL: 80 header + 4 bytes triangle count + 50 bytes per triangle
    if (buffer.byteLength < 84) return false;
    var dv = new DataView(buffer);
    var numTriangles = dv.getUint32(80, true);
    var expectedSize = 84 + numTriangles * 50;
    // Tolerance of 256 bytes — some exporters (SolidWorks, Magics) pad/align
    return Math.abs(buffer.byteLength - expectedSize) < 256;
  }

  var MAX_TRIANGLES = 5000000; // ~240 MB — guard against malformed files

  function parseBinarySTL(buffer) {
    var dv = new DataView(buffer);
    var numTriangles = dv.getUint32(80, true);
    if (numTriangles > MAX_TRIANGLES) {
      throw new Error('File too large: ' + numTriangles.toLocaleString() + ' triangles (max ' + MAX_TRIANGLES.toLocaleString() + ')');
    }
    var vertices = new Float32Array(numTriangles * 9);
    var offset = 84;
    var totalVolume = 0;

    var minX = Infinity, minY = Infinity, minZ = Infinity;
    var maxX = -Infinity, maxY = -Infinity, maxZ = -Infinity;

    for (var i = 0; i < numTriangles; i++) {
      // Skip normal (12 bytes)
      offset += 12;

      for (var v = 0; v < 3; v++) {
        var x = dv.getFloat32(offset, true); offset += 4;
        var y = dv.getFloat32(offset, true); offset += 4;
        var z = dv.getFloat32(offset, true); offset += 4;
        var idx = i * 9 + v * 3;
        vertices[idx]     = x;
        vertices[idx + 1] = y;
        vertices[idx + 2] = z;

        if (x < minX) minX = x;
        if (x > maxX) maxX = x;
        if (y < minY) minY = y;
        if (y > maxY) maxY = y;
        if (z < minZ) minZ = z;
        if (z > maxZ) maxZ = z;
      }

      // Signed volume of tetrahedron (vertex0, vertex1, vertex2, origin)
      var a = i * 9;
      totalVolume += signedVolumeOfTriangle(
        vertices[a], vertices[a+1], vertices[a+2],
        vertices[a+3], vertices[a+4], vertices[a+5],
        vertices[a+6], vertices[a+7], vertices[a+8]
      );

      // Skip attribute byte count
      offset += 2;
    }

    return {
      vertices: vertices,
      triangleCount: numTriangles,
      volume: Math.abs(totalVolume),  // mm³
      bounds: { minX: minX, maxX: maxX, minY: minY, maxY: maxY, minZ: minZ, maxZ: maxZ }
    };
  }

  function parseASCIISTL(buffer) {
    var text = new TextDecoder().decode(buffer);
    var vertexPattern = /vertex\s+([\-\d.eE+]+)\s+([\-\d.eE+]+)\s+([\-\d.eE+]+)/g;
    var verts = [];
    var match;

    while ((match = vertexPattern.exec(text)) !== null) {
      verts.push(parseFloat(match[1]), parseFloat(match[2]), parseFloat(match[3]));
    }

    var vertices = new Float32Array(verts);
    var numTriangles = vertices.length / 9;
    var totalVolume = 0;
    var minX = Infinity, minY = Infinity, minZ = Infinity;
    var maxX = -Infinity, maxY = -Infinity, maxZ = -Infinity;

    for (var i = 0; i < numTriangles; i++) {
      var a = i * 9;
      for (var v = 0; v < 3; v++) {
        var x = vertices[a + v * 3];
        var y = vertices[a + v * 3 + 1];
        var z = vertices[a + v * 3 + 2];
        if (x < minX) minX = x;
        if (x > maxX) maxX = x;
        if (y < minY) minY = y;
        if (y > maxY) maxY = y;
        if (z < minZ) minZ = z;
        if (z > maxZ) maxZ = z;
      }
      totalVolume += signedVolumeOfTriangle(
        vertices[a], vertices[a+1], vertices[a+2],
        vertices[a+3], vertices[a+4], vertices[a+5],
        vertices[a+6], vertices[a+7], vertices[a+8]
      );
    }

    return {
      vertices: vertices,
      triangleCount: numTriangles,
      volume: Math.abs(totalVolume),
      bounds: { minX: minX, maxX: maxX, minY: minY, maxY: maxY, minZ: minZ, maxZ: maxZ }
    };
  }

  // Signed volume of tetrahedron formed by triangle and origin
  function signedVolumeOfTriangle(x1, y1, z1, x2, y2, z2, x3, y3, z3) {
    return (
      x1 * (y2 * z3 - y3 * z2) +
      x2 * (y3 * z1 - y1 * z3) +
      x3 * (y1 * z2 - y2 * z1)
    ) / 6.0;
  }

  // ── OBJ Parser (basic) ───────────────────────────────────────────────

  function parseOBJ(text) {
    var verts = [];   // raw vertex positions [x,y,z, ...]
    var tris  = [];   // flattened triangle vertices
    var lines = text.split('\n');

    for (var i = 0; i < lines.length; i++) {
      var line = lines[i].trim();
      if (line.indexOf('v ') === 0) {
        var parts = line.split(/\s+/);
        verts.push(parseFloat(parts[1]), parseFloat(parts[2]), parseFloat(parts[3]));
      } else if (line.indexOf('f ') === 0) {
        var fParts = line.split(/\s+/).slice(1);
        // Triangulate faces (fan method)
        var indices = fParts.map(function (f) { return parseInt(f.split('/')[0], 10) - 1; });
        for (var j = 1; j < indices.length - 1; j++) {
          var i0 = indices[0] * 3, i1 = indices[j] * 3, i2 = indices[j + 1] * 3;
          // Skip faces with out-of-bounds vertex indices
          if (i0 < 0 || i1 < 0 || i2 < 0 ||
              i0 + 2 >= verts.length || i1 + 2 >= verts.length || i2 + 2 >= verts.length) continue;
          tris.push(
            verts[i0], verts[i0+1], verts[i0+2],
            verts[i1], verts[i1+1], verts[i1+2],
            verts[i2], verts[i2+1], verts[i2+2]
          );
        }
      }
    }

    var vertices = new Float32Array(tris);
    var numTriangles = vertices.length / 9;
    var totalVolume = 0;
    var minX = Infinity, minY = Infinity, minZ = Infinity;
    var maxX = -Infinity, maxY = -Infinity, maxZ = -Infinity;

    for (var k = 0; k < numTriangles; k++) {
      var a = k * 9;
      for (var v = 0; v < 3; v++) {
        var x = vertices[a + v * 3];
        var y = vertices[a + v * 3 + 1];
        var z = vertices[a + v * 3 + 2];
        if (x < minX) minX = x;
        if (x > maxX) maxX = x;
        if (y < minY) minY = y;
        if (y > maxY) maxY = y;
        if (z < minZ) minZ = z;
        if (z > maxZ) maxZ = z;
      }
      totalVolume += signedVolumeOfTriangle(
        vertices[a], vertices[a+1], vertices[a+2],
        vertices[a+3], vertices[a+4], vertices[a+5],
        vertices[a+6], vertices[a+7], vertices[a+8]
      );
    }

    return {
      vertices: vertices,
      triangleCount: numTriangles,
      volume: Math.abs(totalVolume),
      bounds: { minX: minX, maxX: maxX, minY: minY, maxY: maxY, minZ: minZ, maxZ: maxZ }
    };
  }

  // ── Display model in Three.js ─────────────────────────────────────────

  function displayModel(parsed) {
    if (!renderer) initThree();

    // Remove old model
    if (modelMesh) {
      scene.remove(modelMesh);
      modelMesh.geometry.dispose();
      modelMesh.material.dispose();
    }

    var geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(parsed.vertices, 3));
    geometry.computeVertexNormals();

    var material = new THREE.MeshPhongMaterial({
      color: 0xFF5F05,        // Illinois orange
      specular: 0x333333,
      shininess: 30,
      flatShading: false
    });

    modelMesh = new THREE.Mesh(geometry, material);
    scene.add(modelMesh);

    // Center model
    geometry.computeBoundingBox();
    var bb = geometry.boundingBox;
    var center = new THREE.Vector3();
    bb.getCenter(center);
    modelMesh.position.sub(center);

    // Fit camera
    var size = new THREE.Vector3();
    bb.getSize(size);
    var maxDim = Math.max(size.x, size.y, size.z);
    var fitDistance = maxDim * 1.8;

    controls.reset(new THREE.Vector3(0, 0, 0), fitDistance);
    resizeViewer();
  }

  // ── Pricing calculation ───────────────────────────────────────────────

  function getSelectedValue(name) {
    var el = document.querySelector('input[name="' + name + '"]:checked');
    return el ? el.value : '';
  }

  function estimateWeight(volumeMm3, infillPercent) {
    // Convert mm³ to cm³
    var volumeCm3 = volumeMm3 / 1000;

    // Approximate effective material:
    // Shell walls account for ~10-15% of volume (solid),
    // interior is filled at the infill percentage.
    var shellFraction = 0.12;
    var interiorFraction = 1 - shellFraction;
    var effectiveFill = shellFraction + interiorFraction * (infillPercent / 100);

    return volumeCm3 * PLA_DENSITY * effectiveFill;
  }

  function updatePrice() {
    if (modelVolumeMm3 <= 0) return;

    var userType    = getSelectedValue('userType');
    var orderType   = getSelectedValue('orderType');
    var infill      = parseInt(infillSlider.value, 10);
    var quantity    = Math.max(1, parseInt(qtyInput.value, 10) || 1);

    var weight      = estimateWeight(modelVolumeMm3, infill);
    var rate        = PRICING[orderType][userType];
    var baseFee     = BASE_FEE;
    var unitCost    = baseFee + weight * rate;
    var totalCost   = unitCost * quantity;

    // Update display
    weightEl.textContent = weight.toFixed(1) + ' g';
    rateEl.textContent = (rate * 100).toFixed(0) + '\u00A2/g';

    baseFeeRow.hidden = false;

    if (quantity > 1) {
      qtyRow.hidden = false;
      qtyDisplay.textContent = '\u00D7 ' + quantity;
    } else {
      qtyRow.hidden = true;
    }

    totalEl.textContent = '$' + totalCost.toFixed(2);

    trackQuoteDebounced({
      event_category: 'quote_calculator',
      user_type: userType,
      order_type: orderType,
      infill_pct: infill,
      weight_g: Math.round(weight),
      value: parseFloat(totalCost.toFixed(2))
    });

    // Update infill display + position the label over the thumb
    infillValue.textContent = infill + '%';
    positionInfillLabel();
  }

  function positionInfillLabel() {
    var track = document.querySelector('.quote-slider-track');
    if (!track || !infillSlider) return;
    var min = parseFloat(infillSlider.min);
    var max = parseFloat(infillSlider.max);
    var val = parseFloat(infillSlider.value);
    var pct = (val - min) / (max - min);
    // Offset by half the thumb width (~11px) to stay centred on the thumb
    var trackWidth = track.offsetWidth;
    var offset = 11 + (trackWidth - 22) * pct; // 22 = thumb diameter
    infillValue.style.left = offset + 'px';
  }

  // ── File handling ─────────────────────────────────────────────────────

  function processFile(file) {
    if (!file) return;

    var ext = file.name.split('.').pop().toLowerCase();
    if (ext !== 'stl' && ext !== 'obj') {
      alert('Please upload an .STL or .OBJ file.');
      return;
    }

    filenameEl.textContent = file.name;
    trackEvent('quote_file_upload', {
      event_category: 'quote_calculator',
      event_label: ext.toUpperCase(),
      file_size_kb: Math.round(file.size / 1024)
    });

    var reader = new FileReader();

    if (ext === 'obj') {
      reader.onload = function (e) {
        try {
          var parsed = parseOBJ(e.target.result);
          onModelParsed(parsed);
        } catch (err) {
          alert('Could not parse OBJ file. Please check the file format.');
          console.error(err);
        }
      };
      reader.readAsText(file);
    } else {
      reader.onload = function (e) {
        try {
          var parsed = parseSTL(e.target.result);
          onModelParsed(parsed);
        } catch (err) {
          alert('Could not parse STL file. Please check the file format.');
          console.error(err);
        }
      };
      reader.readAsArrayBuffer(file);
    }
  }

  function onModelParsed(parsed) {
    modelVolumeMm3 = parsed.volume;
    modelTriangles = parsed.triangleCount;

    var b = parsed.bounds;
    var dx = (b.maxX - b.minX).toFixed(1);
    var dy = (b.maxY - b.minY).toFixed(1);
    var dz = (b.maxZ - b.minZ).toFixed(1);

    dimEl.textContent = dx + ' \u00D7 ' + dy + ' \u00D7 ' + dz + ' mm';
    volEl.textContent = (parsed.volume / 1000).toFixed(1) + ' cm\u00B3';
    triEl.textContent = parsed.triangleCount.toLocaleString();

    // Show the interface *before* rendering so the canvas gets a real size
    dropzone.hidden = true;
    iface.hidden = false;

    displayModel(parsed);

    updatePrice();
  }

  // ── Event listeners ───────────────────────────────────────────────────

  // Dropzone
  dropzone.addEventListener('click', function () { fileInput.click(); });
  dropzone.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); fileInput.click(); }
  });

  dropzone.addEventListener('dragover', function (e) {
    e.preventDefault();
    dropzone.classList.add('quote-dropzone-active');
  });

  dropzone.addEventListener('dragleave', function () {
    dropzone.classList.remove('quote-dropzone-active');
  });

  dropzone.addEventListener('drop', function (e) {
    e.preventDefault();
    dropzone.classList.remove('quote-dropzone-active');
    if (e.dataTransfer.files.length) processFile(e.dataTransfer.files[0]);
  });

  fileInput.addEventListener('change', function () {
    if (fileInput.files.length) processFile(fileInput.files[0]);
  });

  // Change file
  changeFileBtn.addEventListener('click', function () { fileInput.click(); });

  // Reset view
  resetViewBtn.addEventListener('click', function () {
    if (modelMesh && controls) {
      var bb = modelMesh.geometry.boundingBox;
      var size = new THREE.Vector3();
      bb.getSize(size);
      controls.reset(new THREE.Vector3(0, 0, 0), Math.max(size.x, size.y, size.z) * 1.8);
    }
  });

  // CTA tracking
  var orderBtn = document.querySelector('.quote-order-btn');
  if (orderBtn) {
    orderBtn.addEventListener('click', function () {
      trackEvent('quote_place_order', {
        event_category: 'quote_calculator',
        event_label: getSelectedValue('orderType'),
        value: parseFloat(totalEl.textContent.replace('$', '')) || 0
      });
    });
  }

  var pricingBtn = document.querySelector('.quote-pricing-btn');
  if (pricingBtn) {
    pricingBtn.addEventListener('click', function () {
      trackEvent('quote_view_pricing', { event_category: 'quote_calculator' });
    });
  }

  // Pricing controls
  infillSlider.addEventListener('input', updatePrice);

  document.querySelectorAll('input[name="userType"]').forEach(function (el) {
    el.addEventListener('change', updatePrice);
  });

  document.querySelectorAll('input[name="orderType"]').forEach(function (el) {
    el.addEventListener('change', updatePrice);
  });

  qtyInput.addEventListener('input', updatePrice);
  qtyMinus.addEventListener('click', function () {
    var v = parseInt(qtyInput.value, 10) || 1;
    qtyInput.value = Math.max(1, v - 1);
    updatePrice();
  });
  qtyPlus.addEventListener('click', function () {
    var v = parseInt(qtyInput.value, 10) || 1;
    qtyInput.value = Math.min(99, v + 1);
    updatePrice();
  });

  // Responsive resize
  window.addEventListener('resize', function () {
    resizeViewer();
    positionInfillLabel();
  });

})();
