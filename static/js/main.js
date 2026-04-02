// ── Tab Navigation ──────────────────────────────────────────────────────────
document.querySelectorAll('.tab').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('panel-' + btn.dataset.tab).classList.add('active');
    if (btn.dataset.tab === 'records') loadStudents(currentFilter);
  });
});

// ── Form: Save / Update Student ─────────────────────────────────────────────
let currentFilter = 'active';

async function saveStudent() {
  const id    = document.getElementById('edit-id').value;
  const name  = document.getElementById('name').value.trim();
  const roll  = document.getElementById('roll').value.trim();

  if (!name || !roll) {
    showFormMsg('Name and Roll Number are required.', 'error');
    return;
  }

  const payload = {
    name,
    roll,
    phone:      document.getElementById('phone').value.trim(),
    email:      document.getElementById('email').value.trim(),
    course:     document.getElementById('course').value,
    department: document.getElementById('department').value,
    notes:      document.getElementById('notes').value.trim(),
  };

  try {
    const url    = id ? `/api/students/${id}` : '/api/students';
    const method = id ? 'PUT' : 'POST';
    const res    = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (data.success) {
      showFormMsg(id ? '✅ Student record updated!' : '✅ Student registered successfully!', 'success');
      clearForm();
    } else {
      showFormMsg('❌ Something went wrong.', 'error');
    }
  } catch (e) {
    showFormMsg('❌ Server error. Is Flask running?', 'error');
  }
}

function showFormMsg(msg, type) {
  const el = document.getElementById('form-msg');
  el.textContent = msg;
  el.className = `form-msg ${type}`;
  el.classList.remove('hidden');
  setTimeout(() => el.classList.add('hidden'), 3500);
}

function clearForm() {
  ['edit-id','name','roll','phone','email','notes'].forEach(id => document.getElementById(id).value = '');
  document.getElementById('course').value = '';
  document.getElementById('department').value = '';
  document.getElementById('save-btn').querySelector('span').textContent = 'Save Student';
}

function cancelEdit() { clearForm(); }

// ── Records: Load & Render ───────────────────────────────────────────────────
async function loadStudents(filter = 'active') {
  currentFilter = filter;

  // update filter button styles
  document.querySelectorAll('.filter-btn').forEach(b => {
    b.classList.toggle('active',
      (filter === 'active' && b.textContent.includes('Active')) ||
      (filter === 'all'    && b.textContent.includes('All'))
    );
  });

  const container = document.getElementById('records-list');
  container.innerHTML = '<div class="loading-state">Loading…</div>';

  try {
    const res  = await fetch(`/api/students?filter=${filter}`);
    const data = await res.json();

    if (!data.length) {
      container.innerHTML = '<div class="empty-state">No student records found.</div>';
      return;
    }

    container.innerHTML = data.map(s => `
      <div class="student-card ${s.status === 'inactive' ? 'inactive' : ''}">
        <div class="sc-header">
          <div style="display:flex;gap:.75rem;align-items:center;">
            <div class="sc-avatar">${s.name ? s.name[0].toUpperCase() : '?'}</div>
            <div>
              <div class="sc-name">${esc(s.name)}</div>
              <div class="sc-roll">${esc(s.roll)}</div>
            </div>
          </div>
          <span class="status-badge ${s.status}">${s.status}</span>
        </div>
        <div class="sc-details">
          ${s.phone      ? `<span>📞 ${esc(s.phone)}</span>` : ''}
          ${s.email      ? `<span>✉️ ${esc(s.email)}</span>` : ''}
          ${s.course     ? `<span>🎓 ${esc(s.course)}</span>` : ''}
          ${s.department ? `<span>🏛 ${esc(s.department)}</span>` : ''}
        </div>
        ${s.notes ? `<div class="sc-notes">"${esc(s.notes)}"</div>` : ''}
        <div class="sc-actions">
          <button class="btn-edit"   onclick="editStudent(${JSON.stringify(s).replace(/"/g,'&quot;')})">✏ Edit</button>
          <button class="btn-delete" onclick="deleteStudent('${s._id}')">✕ Remove</button>
        </div>
      </div>
    `).join('');

  } catch(e) {
    container.innerHTML = '<div class="empty-state">❌ Could not load records. Is Flask running?</div>';
  }
}

// ── Edit Student ─────────────────────────────────────────────────────────────
function editStudent(s) {
  document.getElementById('edit-id').value     = s._id;
  document.getElementById('name').value        = s.name        || '';
  document.getElementById('roll').value        = s.roll        || '';
  document.getElementById('phone').value       = s.phone       || '';
  document.getElementById('email').value       = s.email       || '';
  document.getElementById('course').value      = s.course      || '';
  document.getElementById('department').value  = s.department  || '';
  document.getElementById('notes').value       = s.notes       || '';
  document.getElementById('save-btn').querySelector('span').textContent = 'Update Student';

  // Switch to registration panel
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.querySelector('[data-tab="register"]').classList.add('active');
  document.getElementById('panel-register').classList.add('active');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ── Delete Student ───────────────────────────────────────────────────────────
async function deleteStudent(id) {
  if (!confirm('Mark this student as inactive?')) return;
  try {
    await fetch(`/api/students/${id}`, { method: 'DELETE' });
    loadStudents(currentFilter);
  } catch(e) {
    alert('Error removing student.');
  }
}

// ── DBMS Console ─────────────────────────────────────────────────────────────
async function runSQL() {
  const sql = document.getElementById('sql-input').value.trim();
  if (!sql) return;

  const output   = document.getElementById('sql-output');
  const msgEl    = document.getElementById('sql-msg');
  const tableWrap = document.getElementById('sql-table-wrap');

  output.classList.remove('hidden');
  msgEl.textContent    = 'Running…';
  tableWrap.innerHTML  = '';

  try {
    const res  = await fetch('/api/dbms', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sql })
    });
    const data = await res.json();
    msgEl.textContent = data.message;

    if (data.rows && data.rows.length) {
      const keys = Object.keys(data.rows[0]).filter(k => k !== '__v');
      tableWrap.innerHTML = `
        <table class="sql-table">
          <thead><tr>${keys.map(k => `<th>${esc(k)}</th>`).join('')}</tr></thead>
          <tbody>
            ${data.rows.map(row =>
              `<tr>${keys.map(k => `<td>${esc(String(row[k] ?? ''))}</td>`).join('')}</tr>`
            ).join('')}
          </tbody>
        </table>`;
    }
  } catch(e) {
    msgEl.textContent = '❌ Network error. Is Flask running?';
  }
}

// ── Utility ───────────────────────────────────────────────────────────────────
function esc(str) {
  return String(str)
    .replace(/&/g,'&amp;')
    .replace(/</g,'&lt;')
    .replace(/>/g,'&gt;')
    .replace(/"/g,'&quot;');
}

// ── Init ──────────────────────────────────────────────────────────────────────
loadStudents('active');
