(function () {
  const form = document.getElementById('form');
  const urlInput = document.getElementById('url');
  const fileInput = document.getElementById('file');
  const modelSelect = document.getElementById('model');
  const submitBtn = document.getElementById('submit');
  const progressSection = document.getElementById('progress');
  const progressMessage = document.getElementById('progress-message');
  const progressFill = document.getElementById('progress-fill');
  const errorSection = document.getElementById('error');
  const errorText = document.getElementById('error-text');
  const resultSection = document.getElementById('result');
  const transcriptPre = document.getElementById('transcript');
  const copyBtn = document.getElementById('copy-btn');
  const downloadBtn = document.getElementById('download-btn');

  function hideAll() {
    progressSection.classList.add('hidden');
    errorSection.classList.add('hidden');
    resultSection.classList.add('hidden');
  }

  function showProgress(message, percent) {
    hideAll();
    progressSection.classList.remove('hidden');
    progressMessage.textContent = message || 'Processing…';
    progressFill.style.width = (percent != null ? percent : 0) + '%';
  }

  function showError(message) {
    hideAll();
    errorSection.classList.remove('hidden');
    errorText.textContent = message;
  }

  function showResult(text) {
    hideAll();
    resultSection.classList.remove('hidden');
    transcriptPre.textContent = text || '';
    downloadBtn.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text || ''));
    downloadBtn.download = 'transcript.txt';
  }

  function setBusy(busy) {
    submitBtn.disabled = busy;
  }

  // Toggle URL vs file: clear the other
  urlInput.addEventListener('input', function () {
    if (urlInput.value.trim()) fileInput.value = '';
  });
  fileInput.addEventListener('change', function () {
    if (fileInput.files.length) urlInput.value = '';
  });

  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    const url = urlInput.value.trim();
    const file = fileInput.files[0];
    if (!url && !file) {
      showError('Enter a URL or choose a file.');
      return;
    }
    if (url && file) {
      showError('Use either a URL or a file, not both.');
      return;
    }

    setBusy(true);
    showProgress('Starting…', 0);

    const formData = new FormData();
    formData.append('model', modelSelect.value);
    if (url) formData.append('url', url);
    if (file) formData.append('file', file);

    let jobId;
    try {
      const res = await fetch('/api/transcribe', {
        method: 'POST',
        body: formData,
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: res.statusText }));
        throw new Error(err.detail || res.statusText);
      }
      const data = await res.json();
      jobId = data.job_id;
    } catch (err) {
      showError(err.message || 'Failed to start job.');
      setBusy(false);
      return;
    }

    const poll = setInterval(async function () {
      try {
        const res = await fetch('/api/jobs/' + jobId);
        if (!res.ok) return;
        const job = await res.json();
        showProgress(job.message || 'Processing…', job.progress ?? 0);

        if (job.status === 'completed') {
          clearInterval(poll);
          setBusy(false);
          showResult(job.transcript || '');
          return;
        }
        if (job.status === 'error') {
          clearInterval(poll);
          setBusy(false);
          showError(job.error || 'Something went wrong.');
        }
      } catch (_) {}
    }, 800);
  });

  copyBtn.addEventListener('click', function () {
    const text = transcriptPre.textContent;
    if (!text) return;
    navigator.clipboard.writeText(text).then(
      function () {
        const label = copyBtn.textContent;
        copyBtn.textContent = 'Copied!';
        setTimeout(function () {
          copyBtn.textContent = label;
        }, 2000);
      },
      function () {
        showError('Copy failed.');
      }
    );
  });
})();
