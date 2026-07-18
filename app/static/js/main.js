// Confirmation modals for destructive actions
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-confirm]').forEach((form) => {
    form.addEventListener('submit', (ev) => {
      const msg = form.getAttribute('data-confirm') || 'Tem certeza?';
      if (!window.confirm(msg)) ev.preventDefault();
    });
  });
  document.querySelectorAll('.flash button').forEach((btn) => {
    btn.addEventListener('click', () => btn.parentElement.remove());
  });
});
