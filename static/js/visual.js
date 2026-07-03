const canvas = document.querySelector('#towerCanvas');
const ctx = canvas?.getContext('2d');
let tick = 0;

function roundRect(x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.arcTo(x + w, y, x + w, y + h, r);
  ctx.arcTo(x + w, y + h, x, y + h, r);
  ctx.arcTo(x, y + h, x, y, r);
  ctx.arcTo(x, y, x + w, y, r);
  ctx.closePath();
}

function card(x, y, w, h, title, value, note, color) {
  roundRect(x, y, w, h, 8);
  ctx.fillStyle = '#ffffff';
  ctx.fill();
  ctx.strokeStyle = '#d7e0ea';
  ctx.stroke();
  ctx.fillStyle = '#697789';
  ctx.font = '12px sans-serif';
  ctx.textAlign = 'left';
  ctx.fillText(title, x + 16, y + 22);
  ctx.fillStyle = '#172033';
  ctx.font = '700 22px sans-serif';
  ctx.fillText(value, x + 16, y + 52);
  ctx.fillStyle = color;
  roundRect(x + 16, y + h - 17, Math.max(38, w * 0.52), 5, 3);
  ctx.fill();
  ctx.fillStyle = '#8a96a6';
  ctx.font = '11px sans-serif';
  ctx.fillText(note, x + 16, y + h - 28);
}

function draw() {
  if (!ctx) return;
  const w = canvas.width;
  const h = canvas.height;
  tick += 0.01;
  ctx.clearRect(0, 0, w, h);
  ctx.fillStyle = '#f8fafc';
  ctx.fillRect(0, 0, w, h);

  ctx.strokeStyle = '#e7edf4';
  ctx.lineWidth = 1;
  for (let y = 46; y < h; y += 58) { ctx.beginPath(); ctx.moveTo(24, y); ctx.lineTo(w - 24, y); ctx.stroke(); }

  card(34, 30, 180, 96, '任务执行', '1,284', '本周处理量', '#1e4f91');
  card(246, 30, 180, 96, '知识调用', '8,642', '资料检索与引用', '#2d9a8f');
  card(458, 30, 180, 96, '复核节点', '326', '人工确认记录', '#b9812f');

  roundRect(34, 154, 604, 170, 8);
  ctx.fillStyle = '#ffffff';
  ctx.fill();
  ctx.strokeStyle = '#d7e0ea';
  ctx.stroke();
  ctx.fillStyle = '#172033';
  ctx.font = '700 16px sans-serif';
  ctx.fillText('岗位任务运行概览', 54, 184);
  ctx.fillStyle = '#697789';
  ctx.font = '12px sans-serif';
  ctx.fillText('销售 / 采购 / 财务 / 人事 / 生产 / 运营 / 客服 / 质量', 54, 206);

  const bars = [0.72, 0.58, 0.82, 0.46, 0.68, 0.76, 0.62, 0.54];
  const labels = ['销售', '采购', '财务', '人事', '生产', '运营', '客服', '质量'];
  bars.forEach((base, i) => {
    const x = 58 + i * 69;
    const barH = 80 * (base + Math.sin(tick * 2 + i) * 0.025);
    ctx.fillStyle = '#edf2f7';
    roundRect(x, 224, 34, 78, 5);
    ctx.fill();
    ctx.fillStyle = i % 3 === 0 ? '#1e4f91' : i % 3 === 1 ? '#2d9a8f' : '#b9812f';
    roundRect(x, 302 - barH, 34, barH, 5);
    ctx.fill();
    ctx.fillStyle = '#697789';
    ctx.font = '12px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(labels[i], x + 17, 344);
  });

  roundRect(34, 348, 604, 28, 8);
  ctx.fillStyle = '#eef2f7';
  ctx.fill();
  ctx.fillStyle = '#1e4f91';
  roundRect(34, 348, 604 * (0.66 + Math.sin(tick) * 0.015), 28, 8);
  ctx.fill();
  ctx.fillStyle = '#ffffff';
  ctx.font = '13px sans-serif';
  ctx.textAlign = 'left';
  ctx.fillText('流程协同完成率  66.8%', 52, 367);

  requestAnimationFrame(draw);
}

draw();
