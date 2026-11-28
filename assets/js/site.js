/* ============================================================
   SITE-00 · 站点公共脚本（所有页面共用）
   ------------------------------------------------------------
   1) CRT 开关：状态存 localStorage，跨页面保持
   2) 顶栏时钟
   3) 主页的终端回显
   4) 筛选 chips / 分页 / 目录：仅切换视觉状态
   ============================================================ */
(function () {
  "use strict";

  var root = document.documentElement;

  /* ---------- 1. CRT 开关 ---------- */
  var crtBtn = document.getElementById('crtBtn');
  if (crtBtn) {
    // <head> 里的内联脚本已经应用过保存的状态，这里只把按钮文字对齐
    function syncCrt() {
      crtBtn.textContent = (root.dataset.crt === 'off') ? 'CRT 关' : 'CRT 开';
    }
    syncCrt();
    crtBtn.addEventListener('click', function () {
      var on = root.dataset.crt === 'on';
      root.dataset.crt = on ? 'off' : 'on';
      try { localStorage.setItem('crt', root.dataset.crt); } catch (e) { /* 隐私模式下忽略 */ }
      syncCrt();
    });
  }

  /* ---------- 2. 时钟 ---------- */
  var clock = document.getElementById('clock');
  if (clock) {
    (function tick() {
      var d = new Date();
      var p = function (n) { return String(n).padStart(2, '0'); };
      clock.textContent = p(d.getHours()) + ':' + p(d.getMinutes()) + ':' + p(d.getSeconds());
      setTimeout(tick, 1000);
    })();
  }

  /* ---------- 3. 终端回显（只有主页有这个输入框） ---------- */
  var termIn = document.getElementById('termIn');
  var termOut = document.getElementById('termOut');
  if (termIn && termOut) {
    termIn.addEventListener('keydown', function (e) {
      if (e.key !== 'Enter' || !termIn.value.trim()) return;
      var cmd = termIn.value.trim();
      var replies = [
        '正在检索「' + cmd + '」… 0 条结果。（版式占位）',
        '错误：未连接资料库后端。（版式占位）',
        '权限不足：该条目需要 Level 4 权限。（版式占位）'
      ];
      termOut.textContent += '\n> ' + cmd + '\n' + replies[Math.floor(Math.random() * replies.length)];
      termIn.value = '';
    });
  }

  /* ---------- 4. 筛选 chips ---------- */
  document.querySelectorAll('.chip-btn').forEach(function (b) {
    b.addEventListener('click', function () {
      b.parentElement.querySelectorAll('.chip-btn').forEach(function (x) { x.classList.remove('on'); });
      b.classList.add('on');
    });
  });

  /* ---------- 5. 分页 ---------- */
  document.querySelectorAll('.pager .pg').forEach(function (p) {
    p.addEventListener('click', function () {
      var t = p.textContent;
      if (t === '…' || t === '‹' || t === '›') return;
      document.querySelectorAll('.pager .pg').forEach(function (x) { x.classList.remove('on'); });
      p.classList.add('on');
    });
  });

  /* ---------- 6. 右栏目录 ---------- */
  document.querySelectorAll('.toc li').forEach(function (li) {
    li.addEventListener('click', function () {
      li.parentElement.querySelectorAll('li').forEach(function (x) { x.classList.remove('active'); });
      li.classList.add('active');
    });
  });
})();
