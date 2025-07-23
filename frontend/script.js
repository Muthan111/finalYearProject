const formatTimeWithMS = secs => {
      const h = Math.floor(secs / 3600);
      const m = Math.floor((secs % 3600) / 60);
      const s = Math.floor(secs % 60);
      const ms = Math.floor((secs % 1) * 10000);
      const pad = (n, l = 2) => String(n).padStart(l, '0');
      return `${pad(h)}:${pad(m)}:${pad(s)}:${pad(ms, 4)}`;
    };

    const fileInput = document.getElementById('audioFile');
    const fileNameDisplay = document.getElementById('fileNameDisplay');
    const detectBtn = document.getElementById('detectBtn');

    const transcriptionBox = document.getElementById('transcriptionBox');
    const alignmentBox = document.getElementById('alignmentBox');
    const feedbackBox = document.getElementById('feedbackBox');
    const rawDetectionBox = document.getElementById('raw_detection');

    const audioElement = document.getElementById('backendAudio');
    const audioContainer = document.getElementById('audioContainer');
    const playPauseBtn = document.getElementById('playPauseBtn');
    const currentTimeTxt = document.getElementById('currentTime');
    const totalTimeTxt = document.getElementById('totalTime');
    const progressBar = document.getElementById('progressBar');
    const progress = document.getElementById('progress');

    fileInput.addEventListener('change', () => {
      fileNameDisplay.textContent = fileInput.files[0]?.name || '';
    });

    detectBtn.addEventListener('click', async () => {
      if (!fileInput.files.length) {
        alert('Please upload an audio file.');
        return;
      }

      const formData = new FormData();
      formData.append('file', fileInput.files[0]);

      transcriptionBox.value = 'Detecting...';
      alignmentBox.value = '';
      feedbackBox.value = '';
      rawDetectionBox.value = 'Processing...';

      try {
        const res = await fetch('http://127.0.0.1:8000/stutter_detection', {
          method: 'POST',
          body: formData
        });
        if (!res.ok) throw new Error('API request failed');
        const data = await res.json();

        transcriptionBox.value = data.transcription || 'No transcription.';
        alignmentBox.value = JSON.stringify(data.alignment || 'No alignment.', null, 2);
        feedbackBox.value = data.personalized_feedback || 'No feedback.';
        rawDetectionBox.value = JSON.stringify(data.detection || 'No detection.', null, 2);

        if (data.audioDisplayURL) {
          audioElement.src = data.audioDisplayURL;
          audioElement.load();
          audioContainer.style.display = 'block';
          currentTimeTxt.textContent = '00:00:00:0000';
          totalTimeTxt.textContent = '00:00:00:0000';
          progress.style.width = '0%';
          playPauseBtn.textContent = '▶️';

          audioElement.addEventListener('loadedmetadata', () => {
            totalTimeTxt.textContent = formatTimeWithMS(audioElement.duration);
          }, { once: true });

          audioElement.play();
        }
      } catch (err) {
        transcriptionBox.value = '';
        alignmentBox.value = '';
        feedbackBox.value = 'Error: ' + err.message;
        rawDetectionBox.value = 'Error: ' + err.message;
      }
    });

    let rafId = null;
    let seeking = false;

    const renderProgress = () => {
      if (!audioElement.duration) return;
      currentTimeTxt.textContent = formatTimeWithMS(audioElement.currentTime);
      const pct = (audioElement.currentTime / audioElement.duration) * 100;
      progress.style.width = `${pct}%`;
    };

    const startRAF = () => {
      cancelRAF();
      const step = () => {
        if (!audioElement.paused && !audioElement.ended && !seeking) {
          renderProgress();
          rafId = requestAnimationFrame(step);
        }
      };
      step();
    };

    const cancelRAF = () => {
      if (rafId) cancelAnimationFrame(rafId);
      rafId = null;
    };

    playPauseBtn.addEventListener('click', () => {
      audioElement[audioElement.paused ? 'play' : 'pause']();
    });

    audioElement.addEventListener('play', () => {
      playPauseBtn.textContent = '⏸️';
      startRAF();
    });

    audioElement.addEventListener('pause', () => {
      playPauseBtn.textContent = '▶️';
      cancelRAF();
      renderProgress();
    });

    audioElement.addEventListener('ended', () => {
      playPauseBtn.textContent = '▶️';
      cancelRAF();
      renderProgress();
    });

    audioElement.addEventListener('timeupdate', () => {
      if (!seeking && audioElement.paused) renderProgress();
    });

    const seekFromClientX = clientX => {
      if (!audioElement.duration) return;
      const rect = progressBar.getBoundingClientRect();
      let pct = (clientX - rect.left) / rect.width;
      pct = Math.max(0, Math.min(1, pct));
      audioElement.currentTime = pct * audioElement.duration;
      renderProgress();
    };

    progressBar.addEventListener('mousedown', e => {
      seeking = true;
      seekFromClientX(e.clientX);
    });

    document.addEventListener('mousemove', e => {
      if (seeking) seekFromClientX(e.clientX);
    });

    document.addEventListener('mouseup', () => (seeking = false));

    progressBar.addEventListener('touchstart', e => {
      seeking = true;
      seekFromClientX(e.touches[0].clientX);
    });

    document.addEventListener('touchmove', e => {
      if (seeking) seekFromClientX(e.touches[0].clientX);
    }, { passive: false });

    document.addEventListener('touchend', () => (seeking = false));

    progressBar.addEventListener('wheel', e => {
      e.preventDefault();
      if (!audioElement.duration) return;
      const STEP = 3;
      const dir = Math.sign(e.deltaY);
      audioElement.currentTime = Math.min(
        Math.max(0, audioElement.currentTime + dir * STEP),
        audioElement.duration
      );
      renderProgress();
    });
