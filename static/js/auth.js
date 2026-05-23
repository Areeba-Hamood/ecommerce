// 1. Password show/hide
function togglePw(inputId, iconId) {
  const input = document.getElementById(inputId);
  const icon  = document.getElementById(iconId);
  input.type  = input.type === 'password' ? 'text' : 'password';
  icon.className = input.type === 'password' ? 'bi bi-eye' : 'bi bi-eye-slash';
}

// 2. Password strength check
function checkStrength(pw) {
  const segs   = [0,1,2,3].map(i => document.getElementById('s' + i));
  const lbl    = document.getElementById('slabel');
  const checks = [
    pw.length >= 8,
    /[A-Z]/.test(pw),
    /[0-9]/.test(pw),
    /[^A-Za-z0-9]/.test(pw)
  ];
  const ruleIds = ['r1','r2','r3','r4'];
  let score = 0;

  checks.forEach((ok, i) => {
    score += ok ? 1 : 0;
    const li   = document.getElementById(ruleIds[i]);
    if (!li) return;
    const icon = li.querySelector('i');
    li.classList.toggle('ok', ok);
    icon.className = ok ? 'bi bi-check-circle-fill' : 'bi bi-circle';
  });

  const colors = ['#e74c3c','#e67e22','#f1c40f','#c9a84c'];
  const labels = ['Weak','Fair','Good','Strong'];

  if (segs[0]) {
    segs.forEach((s,i) => s.style.background = i < score ? colors[score-1] : '#3a3640');
  }
  if (lbl) {
    lbl.textContent = pw.length === 0 ? '' : (labels[score-1] || 'Too short');
    lbl.style.color = colors[score-1] || '#e74c3c';
  }
}

// 3. Password match check
function checkMatch() {
  const pw1 = document.getElementById('new_password') || document.getElementById('id_password1');
  const pw2 = document.getElementById('confirm_password') || document.getElementById('id_password2');
  const msg = document.getElementById('matchMsg');
  if (!pw1 || !pw2 || !msg) return;
  if (!pw2.value) { msg.textContent = ''; return; }
  if (pw1.value === pw2.value) {
    msg.textContent = '✓ Passwords match';
    msg.style.color = '#c9a84c';
  } else {
    msg.textContent = '✗ Passwords do not match';
    msg.style.color = '#e87b6e';
  }
}