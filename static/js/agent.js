const chatWindow = document.querySelector('#chatWindow');
const chatForm = document.querySelector('#chatForm');
const chatInput = document.querySelector('#chatInput');
const leadForm = document.querySelector('#leadForm');
const leadStatus = document.querySelector('#leadStatus');

function addMessage(text, role) {
  const item = document.createElement('div');
  item.className = 'message ' + role;
  item.textContent = text;
  chatWindow.appendChild(item);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

async function sendMessage(message) {
  addMessage(message, 'user');
  chatInput.value = '';
  const loading = document.createElement('div');
  loading.className = 'message bot loading';
  loading.textContent = '正在生成方案建议...';
  chatWindow.appendChild(loading);
  chatWindow.scrollTop = chatWindow.scrollHeight;
  try {
    const response = await fetch('/api/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message }) });
    const data = await response.json();
    loading.remove();
    addMessage(data.reply, 'bot');
  } catch (error) {
    loading.remove();
    addMessage('接口暂时不可用，请确认后端服务正在运行。', 'bot');
  }
}

chatForm?.addEventListener('submit', (event) => {
  event.preventDefault();
  const message = chatInput.value.trim();
  if (message) sendMessage(message);
});

document.querySelectorAll('[data-prompt]').forEach((button) => {
  button.addEventListener('click', () => sendMessage(button.dataset.prompt));
});

leadForm?.addEventListener('submit', async (event) => {
  event.preventDefault();
  const payload = Object.fromEntries(new FormData(leadForm).entries());
  leadStatus.textContent = '正在保存...';
  try {
    const response = await fetch('/api/lead', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
    const data = await response.json();
    leadStatus.textContent = data.ok ? '已保存为线索 #' + data.lead_id : '保存失败';
    if (data.ok) leadForm.reset();
  } catch (error) {
    leadStatus.textContent = '保存失败，请确认服务正在运行。';
  }
});
